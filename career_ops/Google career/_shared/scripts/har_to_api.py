#!/usr/bin/env python3
"""Reverse-engineer Chrome HAR captures into Career Portal API specs.

Inspired by morluto/rea (evidence-backed network inspection) and
goodnight000/api-anything (plain-HTTP operation specs).
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
from pathlib import Path
from typing import Any

NOISE_DOMAINS = (
    "google-analytics.com",
    "analytics.google.com",
    "googletagmanager.com",
    "doubleclick.net",
    "adtrafficquality.google",
    "feedback-pa.clients6.google.com",
    "play.google.com/log",
    "sentry.io",
    "datadoghq.com",
    "segment.io",
    "segment.com",
    "hotjar.com",
    "clarity.ms",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
)

STATIC_EXTS = (
    ".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".svg",
    ".webp", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".map",
)

JOB_URL_HINTS = (
    "job", "jobs", "career", "careers", "position", "opening",
    "requisition", "vacancy", "vacancies", "posting", "greenhouse",
    "lever", "ashby", "workday", "smartrecruiters", "graphql",
    "search", "batchexecute", "algolia",
)

JOB_TEXT_HINTS = (
    "responsibilities", "qualifications", "minimum qualifications",
    "applyurl", "apply_url", "department", "location", "jobid",
    "requisition", "posting", "employmenttype", "af_initdatacallback",
    "__next_data__", "jobposting",
)


def _is_noise(url: str, mime: str, rtype: str) -> bool:
    low = url.lower()
    path = urllib.parse.urlparse(low).path
    if any(dom in low for dom in NOISE_DOMAINS):
        return True
    if path.endswith(STATIC_EXTS):
        return True
    if rtype in ("image", "stylesheet", "font", "media", "script"):
        return True
    if any(t in mime.lower() for t in ("image/", "text/css", "font/", "javascript")):
        return True
    return False


def _detect_platform(url: str, text: str) -> str:
    low = url.lower()
    if "about/careers/applications/jobs/results" in low and "ds:1" in text:
        return "google_ds1"
    if "boards-api.greenhouse.io" in low or "boards.greenhouse.io" in low:
        return "greenhouse_v1"
    if "api.lever.co/v0/postings" in low:
        return "lever_v0"
    if "api.ashbyhq.com/posting-api" in low:
        return "ashby_v1"
    if "myworkdayjobs.com" in low:
        return "workday_cxs"
    if "batchexecute" in low:
        return "google_batchexecute"
    if "__next_data__" in text.lower():
        return "nextjs_ssr"
    if "application/json" in low or text.lstrip().startswith(("{", "[")):
        return "json_path"
    return "html_or_unknown"


def _find_json_arrays(obj: Any, path: str = "") -> list[tuple[str, int, list[str]]]:
    """Find list-of-dicts inside JSON payloads that look like job lists."""
    found: list[tuple[str, int, list[str]]] = []
    if isinstance(obj, list):
        if len(obj) >= 2 and isinstance(obj[0], dict):
            keys = list(obj[0].keys())[:12]
            found.append((path or "$", len(obj), keys))
        elif len(obj) >= 2 and isinstance(obj[0], list) and len(obj[0]) >= 5:
            found.append((path or "$", len(obj), [f"tuple[{len(obj[0])}]"]))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            sub = f"{path}.{k}" if path else k
            found.extend(_find_json_arrays(v, sub))
    return found


def _score_entry(entry: dict[str, Any]) -> dict[str, Any] | None:
    req = entry.get("request", {})
    res = entry.get("response", {})
    url = req.get("url", "")
    method = req.get("method", "GET")
    status = res.get("status", 0)
    content = res.get("content", {})
    mime = content.get("mimeType", "")
    text = content.get("text", "") or ""
    rtype = entry.get("_resourceType", "")

    if status < 200 or status >= 400 or not text:
        return None
    if _is_noise(url, mime, rtype):
        return None

    low_url = url.lower()
    low_sample = text[:50000].lower()
    score = 0
    reasons: list[str] = []

    if rtype in ("xhr", "fetch") or "json" in mime.lower():
        score += 20
        reasons.append("api/json")
    for kw in JOB_URL_HINTS:
        if kw in low_url:
            score += 8
            reasons.append(f"url:{kw}")
    for kw in JOB_TEXT_HINTS:
        if kw in low_sample:
            score += 6
            reasons.append(f"body:{kw}")

    arrays: list[tuple[str, int, list[str]]] = []
    stripped = text.lstrip()
    if stripped.startswith(")]}'"):
        for line in text.splitlines():
            if line.startswith("[["):
                try:
                    outer = json.loads(line)
                    if outer and len(outer[0]) > 2 and isinstance(outer[0][2], str):
                        inner = json.loads(outer[0][2])
                        arrays.extend(_find_json_arrays(inner, "batchexecute"))
                except Exception:
                    pass
    elif stripped.startswith(("{", "[")):
        try:
            parsed = json.loads(text)
            arrays.extend(_find_json_arrays(parsed))
        except Exception:
            pass
    elif "AF_initDataCallback({key: 'ds:1'" in text:
        score += 25
        reasons.append("ssr:ds1")

    if arrays:
        best_arr = max(arrays, key=lambda x: x[1])
        score += min(30, best_arr[1] * 2)
        reasons.append(f"array:{best_arr[0]}[{best_arr[1]}]")

    if score < 15:
        return None

    headers = {
        h["name"]: h["value"]
        for h in req.get("headers", [])
        if h["name"].lower() not in ("cookie", "x-client-data", "content-length")
        and not h["name"].startswith(":")
    }
    has_cookie = any(h["name"].lower() == "cookie" and h["value"] for h in req.get("headers", []))
    post_text = (req.get("postData") or {}).get("text")
    platform = _detect_platform(url, text)

    return {
        "score": score,
        "platform": platform,
        "method": method,
        "status": status,
        "url": url,
        "resource_type": rtype,
        "mime": mime,
        "size": len(text),
        "has_cookie": has_cookie,
        "headers": headers,
        "post_data": post_text,
        "arrays": arrays[:5],
        "reasons": sorted(set(reasons)),
    }


def analyze_har(har_path: Path, top_n: int = 8) -> list[dict[str, Any]]:
    """Parse HAR file and return top ranked job-API candidates."""
    data = json.loads(har_path.read_text(encoding="utf-8", errors="replace"))
    entries = data.get("log", {}).get("entries", [])
    candidates = []
    for idx, entry in enumerate(entries):
        scored = _score_entry(entry)
        if scored:
            scored["entry_index"] = idx
            candidates.append(scored)
    candidates.sort(key=lambda c: (-c["score"], -c["size"]))
    return candidates[:top_n]


def _safe_headers(headers: dict[str, str]) -> dict[str, str]:
    keep = ("accept", "accept-language", "content-type", "origin", "referer", "user-agent")
    out = {k: v for k, v in headers.items() if k.lower() in keep}
    if "User-Agent" not in out and "user-agent" not in out:
        out["User-Agent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )
    return out


def scaffold_portal(
    portal_dir: Path,
    *,
    portal_id: str,
    company: str,
    candidates: list[dict[str, Any]],
    har_name: str,
) -> None:
    """Create portal.json, api-anything spec, and HAR evidence report."""
    portal_dir.mkdir(parents=True, exist_ok=True)
    (portal_dir / "captures").mkdir(exist_ok=True)
    (portal_dir / "output").mkdir(exist_ok=True)

    # Prefer plain GET/JSON candidate over authenticated batchexecute when available
    top = candidates[0]
    for c in candidates:
        if c["platform"] in ("google_ds1", "greenhouse_v1", "lever_v0", "ashby_v1"):
            top = c
            break

    parsed = urllib.parse.urlparse(top["url"])
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    clean_url = f"{base_url}{parsed.path}"
    query_params = {k: v[0] if len(v) == 1 else v[-1] for k, v in urllib.parse.parse_qs(parsed.query).items()}
    items_path = top["arrays"][0][0] if top["arrays"] else "jobs"

    portal_cfg = {
        "portal_id": portal_id,
        "company": company,
        "enabled": False,
        "parser_type": top["platform"] if top["platform"] in ("google_ds1", "greenhouse_v1", "lever_v0", "ashby_v1") else "json_path",
        "search_query": "",
        "search_location": "",
        "max_jobs": 0,
        "max_pages": 5,
        "request": {
            "method": top["method"],
            "url": clean_url,
            "query": query_params,
            "headers": _safe_headers(top["headers"]),
            "body": top["post_data"],
        },
        "parser_config": {
            "items_path": items_path,
            "fields": {
                "job_id": "id",
                "title": "title",
                "locations": "location",
                "job_url": "url",
                "apply_url": "applyUrl",
                "about_the_job": "description",
                "job_published_at": "publishedAt",
            },
        },
        "notes": f"Auto-scaffolded from {har_name} (platform={top['platform']}, score={top['score']}). Verify parser_config & set enabled=true.",
    }
    (portal_dir / "portal.json").write_text(json.dumps(portal_cfg, indent=2) + "\n", encoding="utf-8")

    api_spec = {
        "name": f"{portal_id}-careers",
        "displayName": f"{company} Careers",
        "baseUrl": base_url,
        "description": f"Auto-discovered from {har_name} ({top['platform']}).",
        "operations": [
            {
                "name": "search",
                "request": {
                    "method": top["method"],
                    "url": top["url"],
                    "headers": _safe_headers(top["headers"]),
                },
                "readOnly": True,
                "minTier": 1,
                "learnedLoggedIn": top["has_cookie"],
            }
        ],
    }
    (portal_dir / f"{portal_id}-careers.api-anything.json").write_text(
        json.dumps(api_spec, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        f"# HAR Reverse-Engineering Report: {company} (`{portal_id}`)",
        "",
        f"- Source HAR: `{har_name}`",
        f"- Selected primary candidate: `{top['method']} {clean_url}` (`{top['platform']}`)",
        "",
        "## Top Candidate Endpoints",
        "",
    ]
    for i, c in enumerate(candidates, 1):
        lines.append(f"### {i}. [{c['score']}] `{c['method']} {c['url'][:140]}`")
        lines.append(f"- Platform guess: `{c['platform']}` | Status: `{c['status']}` | Size: `{c['size']}` bytes | Cookie sent: `{c['has_cookie']}`")
        lines.append(f"- Signals: `{', '.join(c['reasons'])}`")
        if c["arrays"]:
            lines.append(f"- Detected arrays: `{c['arrays']}`")
        lines.append("")
    (portal_dir / "captures" / "har_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Chrome HAR files to discover Career Portal APIs")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("analyze", help="Rank candidate API calls in a HAR file")
    p.add_argument("--har", required=True, help="Path to Chrome .har / HAR JSON file")
    p.add_argument("--portal", default="", help="Portal slug under portals/ (required for --scaffold)")
    p.add_argument("--company", default="", help="Company display name")
    p.add_argument("--top", type=int, default=8, help="Number of candidates to show")
    p.add_argument("--scaffold", action="store_true", help="Write portals/<portal>/portal.json, api-anything spec & har_report.md")

    args = parser.parse_args()
    har_path = Path(args.har)
    candidates = analyze_har(har_path, top_n=args.top)

    if not candidates:
        print("No strong job API candidates found in HAR.")
        return 1

    print(f"Found {len(candidates)} candidate requests in {har_path.name}:")
    for i, c in enumerate(candidates, 1):
        print(
            f"  {i}. score={c['score']:3d} platform={c['platform']:18s} "
            f"{c['method']:4s} {c['status']} size={c['size']:7d} cookie={c['has_cookie']} "
            f"{c['url'][:110]}"
        )
        if c["arrays"]:
            print(f"     arrays={c['arrays'][:2]}")

    if args.scaffold:
        if not args.portal:
            raise SystemExit("--portal is required when --scaffold is set")
        root = Path(__file__).resolve().parent.parent
        portal_dir = root / "portals" / args.portal
        scaffold_portal(
            portal_dir,
            portal_id=args.portal,
            company=args.company or args.portal.title(),
            candidates=candidates,
            har_name=har_path.name,
        )
        print(f"\nScaffolded {portal_dir}/ (portal.json, {args.portal}-careers.api-anything.json, captures/har_report.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

