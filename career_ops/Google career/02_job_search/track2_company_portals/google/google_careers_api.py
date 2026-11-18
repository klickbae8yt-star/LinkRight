#!/usr/bin/env python3
"""Direct Google Careers API client, CLI, and local HTTP server.

Fetches job listings directly over plain HTTP from Google Careers' SSR
AF_initDataCallback(ds:1) payload—no browser, cookies, or MHTML needed.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html as html_lib
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

BASE_URL = "https://www.google.com/about/careers/applications/jobs/results"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

LEVELS = {
    1: ("Early", "Experience completing work as directed and collaborating with teammates; developing knowledge of relevant concepts and processes."),
    2: ("Mid", "Experience driving progress, solving problems and mentoring more junior team members; deeper expertise and applied knowledge within relevant areas."),
    3: ("Advanced", "Experience owning outcomes and decision making, solving ambiguous problems and influencing stakeholders; deep expertise in a domain."),
    4: ("Director", "Experience leading teams and defining long-term product and organizational strategy across multiple domains."),
}

DEGREES = {1: "Associate", 2: "Bachelor's", 3: "Master's", 4: "PhD"}

CSV_FIELDS = [
    "job_id", "title", "company", "is_product_manager_role",
    "experience_level", "experience_level_code", "experience_level_description",
    "min_years_experience", "locations", "primary_location", "location_count",
    "cities", "country_codes", "has_india_location", "locations_json",
    "remote_eligible", "education_levels", "minimum_qualifications",
    "preferred_qualifications", "about_the_job", "responsibilities",
    "applicant_notes", "location_note", "job_url", "apply_url",
    "job_created_at", "job_published_at", "job_updated_at",
    "search_query", "search_location", "search_result_rank",
    "source_page_url", "page_saved_at", "detail_status", "last_scraped_at",
]


def _extract_balanced_json(text: str, start_idx: int) -> Any:
    """Parse a JSON array starting at start_idx using balanced bracket tracking."""
    depth = 0
    in_string = False
    escaped = False
    for i in range(start_idx, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start_idx : i + 1])
    raise ValueError("Unterminated ds:1 JSON array in Google Careers HTML")


def _extract_ds1(page_html: str) -> list[Any]:
    """Locate and decode AF_initDataCallback({key: 'ds:1', ...}) payload."""
    marker = re.search(r"AF_initDataCallback\(\{key:\s*'ds:1'[^}]*?data:(\[)", page_html)
    if not marker:
        raise ValueError("Could not find ds:1 job payload in Google Careers HTML")
    return _extract_balanced_json(page_html, marker.start(1))


def _rich(cell: Any) -> str:
    """Extract HTML string from a Google rich-text tuple [null, html] or str."""
    if isinstance(cell, list) and len(cell) > 1 and isinstance(cell[1], str):
        return cell[1]
    return cell if isinstance(cell, str) else ""


def _html_to_text(raw_html: str) -> str:
    """Convert rich HTML fragment into clean normalized plain text."""
    if not raw_html:
        return ""
    s = re.sub(r"<br\s*/?>", "\n", raw_html, flags=re.I)
    s = re.sub(r"</(p|div|h\d|li)>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html_lib.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\s*\n\s*\n\s*", "\n\n", s)
    s = re.sub(r"[ \t]*\n[ \t]*", "\n", s)
    return s.strip()


def _bullets(raw_html: str) -> str:
    """Extract <li> items from HTML as markdown bullet lines."""
    items = []
    for match in re.finditer(r"<li[^>]*>([\s\S]*?)</li>", raw_html or "", flags=re.I):
        line = re.sub(r"\n+", " ", _html_to_text(match.group(1))).strip()
        if line:
            items.append(f"- {line}")
    return "\n".join(items)


def _section(raw_html: str, pattern: str) -> str:
    """Return first regex capture group or empty string."""
    match = re.search(pattern, raw_html or "", flags=re.I)
    return match.group(1) if match else ""


def _ts(cell: Any) -> str | None:
    """Convert Google [seconds, nanos] timestamp pair into ISO-8601 UTC string."""
    if not isinstance(cell, list) or not cell or not isinstance(cell[0], (int, float)):
        return None
    nanos = cell[1] if len(cell) > 1 and isinstance(cell[1], (int, float)) else 0
    epoch = cell[0] + nanos / 1e9
    return dt.datetime.fromtimestamp(epoch, tz=dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _slugify(title: str) -> str:
    """Build Google Careers URL slug from job title."""
    return re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")


def normalize_job(
    job: list[Any],
    *,
    rank: int,
    query: str,
    location: str,
    source_url: str,
    scraped_at: str,
) -> dict[str, Any]:
    """Map a 21-element ds:1 job array into the flat 35-field record."""
    job_id = str(job[0])
    title = str(job[1] or "")
    company = job[7] if len(job) > 7 and job[7] else None
    apply_url = job[2] if len(job) > 2 and isinstance(job[2], str) else None

    qual_html = _rich(job[4] if len(job) > 4 else None)
    min_q = (
        _bullets(_section(qual_html, r"Minimum qualifications:?</h3>\s*<ul>([\s\S]*?)</ul>"))
        or _bullets(_rich(job[19] if len(job) > 19 else None))
    )
    pref_q = _bullets(_section(qual_html, r"Preferred qualifications:?</h3>\s*<ul>([\s\S]*?)</ul>"))
    resp = _bullets(_rich(job[3] if len(job) > 3 else None)) or _html_to_text(_rich(job[3] if len(job) > 3 else None))
    about = _html_to_text(_rich(job[10] if len(job) > 10 else None))
    notes = _html_to_text(_rich(job[15] if len(job) > 15 else None))
    loc_note = _html_to_text(_rich(job[18] if len(job) > 18 else None))

    level_code = job[20] if len(job) > 20 and isinstance(job[20], int) else None
    level_name, level_desc = LEVELS.get(level_code, (None, None))
    edu_codes = [c for c in (job[11] if len(job) > 11 and isinstance(job[11], list) else []) if isinstance(c, int)]
    edu_str = (
        f"{', '.join(DEGREES.get(c, f'code {c}') for c in edu_codes)} [{','.join(map(str, edu_codes))}]"
        if edu_codes
        else None
    )

    raw_locs = job[9] if len(job) > 9 and isinstance(job[9], list) else []
    locs = [
        {
            "display": l[0] if len(l) > 0 else None,
            "city": l[2] if len(l) > 2 else None,
            "region": l[4] if len(l) > 4 else None,
            "country": l[5] if len(l) > 5 else None,
        }
        for l in raw_locs
        if isinstance(l, list)
    ]
    display_locs = [l["display"] for l in locs if l.get("display")]
    cities = list(dict.fromkeys(l["city"] for l in locs if l.get("city")))
    countries = list(dict.fromkeys(l["country"] for l in locs if l.get("country")))
    years_match = re.search(r"(\d+)\+?\s+years? of experience", min_q, flags=re.I)

    slug = _slugify(title)
    job_url = f"{BASE_URL}/{job_id}-{slug}" if slug else f"{BASE_URL}/{job_id}"

    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "is_product_manager_role": bool(re.search(r"product (manager|lead|management)", title, flags=re.I)),
        "experience_level": level_name,
        "experience_level_code": level_code,
        "experience_level_description": level_desc,
        "min_years_experience": int(years_match.group(1)) if years_match else None,
        "locations": "; ".join(display_locs),
        "primary_location": display_locs[0] if display_locs else None,
        "location_count": len(display_locs),
        "cities": "; ".join(cities) or None,
        "country_codes": ", ".join(countries) or None,
        "has_india_location": bool(
            re.search(r"India", " ".join(display_locs), flags=re.I)
            or any(l.get("country") == "IN" for l in locs)
        ),
        "locations_json": json.dumps(locs, separators=(",", ":")) if locs else None,
        "remote_eligible": bool(re.search(r"Remote (eligible|location)", f"{notes} {loc_note}", flags=re.I)),
        "education_levels": edu_str,
        "minimum_qualifications": min_q or None,
        "preferred_qualifications": pref_q or None,
        "about_the_job": about or None,
        "responsibilities": resp or None,
        "applicant_notes": notes or None,
        "location_note": loc_note or None,
        "job_url": job_url,
        "apply_url": apply_url,
        "job_created_at": _ts(job[12] if len(job) > 12 else None),
        "job_published_at": _ts(job[13] if len(job) > 13 else None),
        "job_updated_at": _ts(job[14] if len(job) > 14 else None),
        "search_query": query,
        "search_location": location,
        "search_result_rank": rank,
        "source_page_url": source_url,
        "page_saved_at": scraped_at,
        "detail_status": "ok",
        "last_scraped_at": scraped_at,
    }


def fetch_page(
    query: str,
    location: str = "",
    page: int = 1,
    hl: str = "en-GB",
    timeout: int = 25,
) -> dict[str, Any]:
    """Fetch a single Google Careers results page over plain HTTP and decode ds:1."""
    params: dict[str, str] = {"q": query, "hl": hl}
    if location:
        params["location"] = location
    if page > 1:
        params["page"] = str(page)

    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")

    ds1 = _extract_ds1(body)
    raw_jobs = ds1[0] if len(ds1) > 0 and isinstance(ds1[0], list) else []
    total = int(ds1[2]) if len(ds1) > 2 and isinstance(ds1[2], int) else len(raw_jobs)
    page_size = int(ds1[3]) if len(ds1) > 3 and isinstance(ds1[3], int) else 20
    return {
        "source_url": url,
        "total": total,
        "page_size": page_size,
        "page": page,
        "raw_jobs": raw_jobs,
    }


def search_jobs(
    query: str,
    location: str = "",
    *,
    max_jobs: int = 0,
    all_pages: bool = True,
    hl: str = "en-GB",
) -> dict[str, Any]:
    """Fetch and normalize Google Careers jobs across one or all result pages."""
    scraped_at = dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    seen_ids: set[str] = set()
    rows: list[dict[str, Any]] = []
    page = 1
    total = 0
    first_source_url = ""

    while True:
        res = fetch_page(query=query, location=location, page=page, hl=hl)
        if page == 1:
            total = res["total"]
            first_source_url = res["source_url"]

        raw_jobs = res["raw_jobs"]
        if not raw_jobs:
            break

        for raw in raw_jobs:
            job_id = str(raw[0])
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)
            rows.append(
                normalize_job(
                    raw,
                    rank=len(rows) + 1,
                    query=query,
                    location=location,
                    source_url=res["source_url"],
                    scraped_at=scraped_at,
                )
            )
            if max_jobs > 0 and len(rows) >= max_jobs:
                return {
                    "ok": True,
                    "query": query,
                    "location": location,
                    "total": total,
                    "count": len(rows),
                    "source_url": first_source_url,
                    "jobs": rows,
                }

        if not all_pages or len(rows) >= total or len(raw_jobs) < res["page_size"]:
            break
        page += 1

    return {
        "ok": True,
        "query": query,
        "location": location,
        "total": total,
        "count": len(rows),
        "source_url": first_source_url,
        "jobs": rows,
    }


def to_csv_string(rows: list[dict[str, Any]]) -> str:
    """Serialize normalized job records to UTF-8 CSV matching google_careers_jobs.csv."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for r in rows:
        flat = {
            k: ("true" if v is True else "false" if v is False else "" if v is None else v)
            for k, v in r.items()
        }
        writer.writerow(flat)
    return buf.getvalue()


class JobsApiHandler(BaseHTTPRequestHandler):
    """Lightweight HTTP API server for n8n, scripts, and agents."""

    def _send_json(self, code: int, payload: Any) -> None:
        raw = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/health":
            self._send_json(200, {"ok": True, "service": "google-careers-api"})
            return

        if parsed.path in ("/jobs", "/jobs.csv"):
            qs = urllib.parse.parse_qs(parsed.query)
            query = qs.get("q", ['"Product Manager"'])[0]
            location = qs.get("location", [""])[0]
            max_jobs = int(qs.get("max_jobs", ["0"])[0] or "0")
            all_pages = qs.get("all_pages", ["true"])[0].lower() != "false"
            hl = qs.get("hl", ["en-GB"])[0]
            try:
                result = search_jobs(
                    query=query,
                    location=location,
                    max_jobs=max_jobs,
                    all_pages=all_pages,
                    hl=hl,
                )
            except Exception as exc:  # pragma: no cover
                self._send_json(502, {"ok": False, "error": str(exc)})
                return

            if parsed.path == "/jobs.csv":
                csv_bytes = to_csv_string(result["jobs"]).encode("utf-8-sig")
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Length", str(len(csv_bytes)))
                self.end_headers()
                self.wfile.write(csv_bytes)
                return

            self._send_json(200, result)
            return

        self._send_json(404, {"ok": False, "error": "Use GET /health, /jobs?q=...&location=..., or /jobs.csv"})

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        sys.stderr.write(f"[google-careers-api] {format % args}\n")


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Direct Google Careers API client and local server")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="Fetch jobs directly from Google Careers")
    p_search.add_argument("--q", required=True, help='Job title / query, e.g. \'"Product Manager"\'')
    p_search.add_argument("--location", default="", help="Location filter, e.g. India")
    p_search.add_argument("--max-jobs", type=int, default=0, help="Max jobs to return (0 = all)")
    p_search.add_argument("--no-all-pages", action="store_true", help="Fetch only page 1 (max 20 jobs)")
    p_search.add_argument("--hl", default="en-GB", help="Language code (default: en-GB)")
    p_search.add_argument("--format", choices=("json", "csv"), default="json", help="Output format")
    p_search.add_argument("--out", default="", help="Write output to file path instead of stdout")

    p_serve = sub.add_parser("serve", help="Start local REST API server for n8n / scripts")
    p_serve.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    p_serve.add_argument("--port", type=int, default=8787, help="Port (default: 8787)")

    args = parser.parse_args()

    if args.cmd == "serve":
        server = ThreadingHTTPServer((args.host, args.port), JobsApiHandler)
        print(f"Listening on http://{args.host}:{args.port} (GET /jobs?q=...&location=...)", file=sys.stderr)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()
        return 0

    result = search_jobs(
        query=args.q,
        location=args.location,
        max_jobs=args.max_jobs,
        all_pages=not args.no_all_pages,
        hl=args.hl,
    )
    output = (
        to_csv_string(result["jobs"])
        if args.format == "csv"
        else json.dumps(result, ensure_ascii=False, indent=2)
    )
    if args.out:
        encoding = "utf-8-sig" if args.format == "csv" else "utf-8"
        with open(args.out, "w", encoding=encoding) as f:
            f.write(output)
        print(f"Wrote {result['count']} jobs (total={result['total']}) to {args.out}", file=sys.stderr)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

