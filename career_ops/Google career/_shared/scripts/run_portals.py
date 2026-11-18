#!/usr/bin/env python3
"""Fault-isolated local runner across all enabled career portals."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "portals" / "google"))
import google_careers_api as gc  # noqa: E402

USER_AGENT = gc.USER_AGENT


def _get_path(obj: Any, dotted: str) -> Any:
    cur = obj
    for part in (dotted or "").split("."):
        if not part:
            continue
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, list) and part.isdigit():
            idx = int(part)
            cur = cur[idx] if idx < len(cur) else None
        else:
            return None
    return cur


def _render_template(val: Any, ctx: dict[str, str]) -> Any:
    if isinstance(val, str):
        out = val
        for k, v in ctx.items():
            out = out.replace("{{" + k + "}}", v)
        return out
    if isinstance(val, dict):
        return {k: _render_template(v, ctx) for k, v in val.items()}
    if isinstance(val, list):
        return [_render_template(v, ctx) for v in val]
    return val


def _run_json_portal(cfg: dict[str, Any], query: str, location: str, scraped_at: str) -> dict[str, Any]:
    req_cfg = cfg["request"]
    ctx = {
        "search_query": query,
        "search_location": location,
        "hl": str(cfg.get("hl", "en-GB")),
    }
    raw_query = _render_template(req_cfg.get("query", {}), ctx)
    query_dict = {k: v for k, v in raw_query.items() if v not in ("", None)}
    url = req_cfg["url"]
    if query_dict:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}{urllib.parse.urlencode(query_dict)}"

    headers = {"User-Agent": USER_AGENT, **req_cfg.get("headers", {})}
    body_obj = _render_template(req_cfg.get("body"), ctx)
    data_bytes = None
    if body_obj is not None:
        data_bytes = (body_obj if isinstance(body_obj, str) else json.dumps(body_obj)).encode("utf-8")

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=req_cfg.get("method", "GET"))
    with urllib.request.urlopen(req, timeout=25) as resp:
        payload = json.loads(resp.read().decode("utf-8", errors="replace"))

    pcfg = cfg.get("parser_config", {})
    items_path = pcfg.get("items_path", "jobs")
    raw_items = payload if items_path in ("$", "") else _get_path(payload, items_path)
    if not isinstance(raw_items, list):
        raise ValueError(f"Expected list at items_path='{items_path}'")

    fmap = pcfg.get("fields", {})
    company = cfg["company"]
    portal_id = cfg["portal_id"]
    rows = []
    max_jobs = int(cfg.get("max_jobs") or 0)
    for idx, item in enumerate(raw_items, 1):
        raw_id = str(_get_path(item, fmap.get("job_id", "id")) or idx)
        job_id = raw_id if portal_id == "google" else f"{portal_id}:{raw_id}"
        title = str(_get_path(item, fmap.get("title", "title")) or "")
        loc_val = _get_path(item, fmap.get("locations", "location"))
        loc_str = loc_val.get("name", "") if isinstance(loc_val, dict) else str(loc_val or "")
        if query and query.strip('"').lower() not in title.lower():
            continue
        if location and location.lower() not in loc_str.lower():
            continue
        rows.append({
            "job_id": job_id,
            "title": title,
            "company": company,
            "is_product_manager_role": bool(re.search(r"product (manager|lead|management)", title, re.I)),
            "experience_level": None,
            "experience_level_code": None,
            "experience_level_description": None,
            "min_years_experience": None,
            "locations": loc_str,
            "primary_location": loc_str.split(";")[0].strip() if loc_str else None,
            "location_count": 1 if loc_str else 0,
            "cities": None,
            "country_codes": None,
            "has_india_location": bool(re.search(r"India", loc_str, re.I)),
            "locations_json": None,
            "remote_eligible": bool(re.search(r"remote", loc_str, re.I)),
            "education_levels": None,
            "minimum_qualifications": None,
            "preferred_qualifications": None,
            "about_the_job": _get_path(item, fmap.get("about_the_job", "description")),
            "responsibilities": None,
            "applicant_notes": None,
            "location_note": None,
            "job_url": _get_path(item, fmap.get("job_url", "url")),
            "apply_url": _get_path(item, fmap.get("apply_url", "applyUrl")),
            "job_created_at": None,
            "job_published_at": _get_path(item, fmap.get("job_published_at", "publishedAt")),
            "job_updated_at": None,
            "search_query": query,
            "search_location": location,
            "search_result_rank": len(rows) + 1,
            "source_page_url": url,
            "page_saved_at": scraped_at,
            "detail_status": "ok",
            "last_scraped_at": scraped_at,
        })
        if max_jobs > 0 and len(rows) >= max_jobs:
            break

    return {"portal_id": portal_id, "ok": True, "count": len(rows), "jobs": rows}


def load_enabled_portals(only_portal: str = "") -> list[dict[str, Any]]:
    portals_dir = ROOT / "portals"
    configs = []
    for pfile in sorted(portals_dir.glob("*/portal.json")):
        if pfile.parent.name.startswith("_"):
            continue
        cfg = json.loads(pfile.read_text(encoding="utf-8"))
        if not cfg.get("enabled", False):
            continue
        if only_portal and cfg.get("portal_id") != only_portal:
            continue
        configs.append(cfg)
    return configs


def run_all(
    portals: list[dict[str, Any]],
    *,
    query_override: str = "",
    location_override: str = "",
) -> dict[str, Any]:
    scraped_at = dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    all_jobs: list[dict[str, Any]] = []
    report: list[dict[str, Any]] = []

    for cfg in portals:
        pid = cfg["portal_id"]
        q = query_override or cfg.get("search_query", '"Product Manager"')
        loc = location_override or cfg.get("search_location", "India")
        try:
            if cfg["parser_type"] == "google_ds1":
                res = gc.search_jobs(
                    query=q,
                    location=loc,
                    max_jobs=int(cfg.get("max_jobs") or 0),
                    hl=cfg.get("hl", "en-GB"),
                )
                jobs = res["jobs"]
            else:
                res = _run_json_portal(cfg, q, loc, scraped_at)
                jobs = res["jobs"]

            all_jobs.extend(jobs)
            report.append({"portal_id": pid, "status": "ok", "count": len(jobs), "error": None})
        except Exception as exc:
            report.append({"portal_id": pid, "status": "failed", "count": 0, "error": str(exc)})

    return {
        "ok": any(r["status"] == "ok" for r in report),
        "portals_total": len(report),
        "portals_ok": sum(1 for r in report if r["status"] == "ok"),
        "portals_failed": sum(1 for r in report if r["status"] == "failed"),
        "total_jobs": len(all_jobs),
        "report": report,
        "jobs": all_jobs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all enabled career portals with per-portal fault isolation")
    parser.add_argument("--portal", default="", help="Run only one portal_id")
    parser.add_argument("--q", default="", help="Override search query across portals")
    parser.add_argument("--location", default="", help="Override location across portals")
    parser.add_argument("--format", choices=("json", "csv"), default="json", help="Output format")
    parser.add_argument("--out", default="", help="Write output file path")
    parser.add_argument("--dry-run", action="store_true", help="Print portal summary only, do not write output")
    args = parser.parse_args()

    portals = load_enabled_portals(only_portal=args.portal)
    if not portals:
        print("No enabled portals found under portals/*/portal.json", file=sys.stderr)
        return 1

    result = run_all(portals, query_override=args.q, location_override=args.location)
    for r in result["report"]:
        print(f"[{r['status'].upper()}] {r['portal_id']}: {r['count']} jobs" + (f" ({r['error']})" if r["error"] else ""), file=sys.stderr)

    if args.dry_run:
        print(json.dumps({k: v for k, v in result.items() if k != "jobs"}, indent=2))
        return 0 if result["ok"] else 1

    output = gc.to_csv_string(result["jobs"]) if args.format == "csv" else json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        enc = "utf-8-sig" if args.format == "csv" else "utf-8"
        Path(args.out).write_text(output, encoding=enc)
    else:
        print(output)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

