#!/usr/bin/env python3
"""Stage 1B: Auto-detect career portal URLs & ATS platforms for discovered companies.

Reads 01_company_discovery/companies/discovered_candidates.json, probes each
company's /careers and /jobs pages plus Ashby/Greenhouse/Lever APIs, and writes:
  - 01_company_discovery/companies/<slug>.json
  - 01_company_discovery/companies/master_list.json
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
COMPANIES_DIR = ROOT / "01_company_discovery" / "companies"
CANDIDATES_FILE = COMPANIES_DIR / "discovered_candidates.json"
MASTER_LIST_FILE = COMPANIES_DIR / "master_list.json"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

ATS_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ashby", re.compile(r"https?://jobs\.ashbyhq\.com/([A-Za-z0-9_.\-]+)", re.I)),
    ("greenhouse", re.compile(r"https?://(?:boards|job-boards)\.greenhouse\.io/([A-Za-z0-9_.\-]+)", re.I)),
    ("greenhouse", re.compile(r"https?://boards-api\.greenhouse\.io/v1/boards/([A-Za-z0-9_.\-]+)", re.I)),
    ("lever", re.compile(r"https?://jobs\.lever\.co/([A-Za-z0-9_.\-]+)", re.I)),
    ("workable", re.compile(r"https?://apply\.workable\.com/([A-Za-z0-9_.\-]+)", re.I)),
    ("workday", re.compile(r"https?://([A-Za-z0-9\-]+\.wd\d+\.myworkdayjobs\.com/[^\s\"'<>]+)", re.I)),
]


def http_fetch(url: str, timeout: int = 8) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(250_000).decode("utf-8", errors="ignore")
            return resp.status, resp.geturl(), raw
    except Exception:
        return 0, url, ""


def probe_ats_api(ats: str, slug: str) -> int | None:
    """Return open job count if public ATS API responds, else None."""
    if not slug:
        return None
    if ats == "ashby":
        _, _, body = http_fetch(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
        if body.startswith("{"):
            try:
                return len(json.loads(body).get("jobs", []))
            except Exception:
                return None
    elif ats == "greenhouse":
        _, _, body = http_fetch(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
        if body.startswith("{"):
            try:
                return len(json.loads(body).get("jobs", []))
            except Exception:
                return None
    elif ats == "lever":
        _, _, body = http_fetch(f"https://api.lever.co/v0/postings/{slug}?mode=json&limit=100")
        if body.startswith("["):
            try:
                return len(json.loads(body))
            except Exception:
                return None
    return None


def detect_for_candidate(cand: dict[str, Any]) -> dict[str, Any]:
    website = (cand.get("website") or "").rstrip("/")
    slug = cand.get("slug") or re.sub(r"[^a-z0-9]+", "-", cand["company_name"].lower()).strip("-")

    career_url = ""
    ats_platform = "unknown"
    ats_slug = ""
    open_jobs_count = 0

    if website:
        base = f"{urllib.parse.urlparse(website).scheme or 'https'}://{urllib.parse.urlparse(website).netloc}"
        for path in ("/careers", "/jobs", ""):
            status, final_url, html_text = http_fetch(f"{base}{path}")
            if status == 200 and html_text:
                if path in ("/careers", "/jobs") and not career_url:
                    career_url = final_url
                for ats, rx in ATS_PATTERNS:
                    m = rx.search(html_text) or rx.search(final_url)
                    if m:
                        ats_platform = ats
                        ats_slug = m.group(1).strip("/")
                        break
                if ats_platform != "unknown":
                    break

    # Fallback: directly probe Ashby / Greenhouse / Lever with normalized slug (require >0 live jobs)
    slug_variants = list(dict.fromkeys([slug, slug.replace("-", "")]))
    if ats_platform == "unknown":
        for ats in ("ashby", "greenhouse", "lever"):
            for s in slug_variants:
                cnt = probe_ats_api(ats, s)
                if cnt is not None and cnt > 0:
                    ats_platform = ats
                    ats_slug = s
                    open_jobs_count = cnt
                    break
            if ats_platform != "unknown":
                break
    elif ats_platform in ("ashby", "greenhouse", "lever"):
        cnt = probe_ats_api(ats_platform, ats_slug)
        if cnt is not None:
            open_jobs_count = cnt

    if not career_url and ats_platform in ("ashby", "greenhouse", "lever") and ats_slug:
        url_map = {
            "ashby": f"https://jobs.ashbyhq.com/{ats_slug}",
            "greenhouse": f"https://boards.greenhouse.io/{ats_slug}",
            "lever": f"https://jobs.lever.co/{ats_slug}",
        }
        career_url = url_map[ats_platform]

    return {
        "company_slug": slug,
        "company_name": cand["company_name"],
        "website": website,
        "career_portal_url": career_url or (f"{website}/careers" if website else ""),
        "ats_platform": ats_platform,
        "ats_slug": ats_slug,
        "has_portal_api": ats_platform in ("ashby", "greenhouse", "lever"),
        "portal_needs_har": ats_platform == "unknown" and bool(website),
        "open_jobs_detected": open_jobs_count,
        "industry": cand.get("industry", "Other"),
        "industry_grade": cand.get("industry_grade", "C"),
        "industry_score": cand.get("industry_score", 3),
        "investor_tier": cand.get("investor_tier", 0),
        "investors": cand.get("investors", []),
        "batch_or_round": cand.get("batch_or_round", ""),
        "team_size": cand.get("team_size", 0),
        "locations": cand.get("locations", []),
        "summary": cand.get("summary", ""),
        "sources_seen": cand.get("sources_seen", [cand.get("source_id", "")]),
        "source_url": cand.get("source_url", ""),
        "research_status": "needs_founder_scoring",
        "added_on": datetime.now(timezone.utc).date().isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect career portals & ATS platforms for Stage 1 candidates")
    parser.add_argument("--limit", type=int, default=25, help="Max candidates with websites to probe")
    args = parser.parse_args()

    if not CANDIDATES_FILE.exists():
        raise SystemExit(f"Run discover_companies.py first ({CANDIDATES_FILE} missing)")

    data = json.loads(CANDIDATES_FILE.read_text(encoding="utf-8"))
    with_sites = [c for c in data.get("candidates", []) if c.get("website")][:args.limit]

    profiles_dir = COMPANIES_DIR / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    enriched: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(detect_for_candidate, c) for c in with_sites]
        for fut in as_completed(futures):
            rec = fut.result()
            enriched.append(rec)
            (profiles_dir / f"{rec['company_slug']}.json").write_text(
                json.dumps(rec, indent=2) + "\n", encoding="utf-8"
            )

    enriched.sort(key=lambda x: (-x["has_portal_api"], -x["open_jobs_detected"], -x["industry_score"], x["company_name"]))
    master = {
        "_meta": {
            "description": "Stage 1 Company Discovery registry (ready for deep founder scoring + Stage 2 monitoring).",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_companies": len(enriched),
            "ats_api_ready": sum(1 for r in enriched if r["has_portal_api"]),
        },
        "companies": enriched,
    }
    MASTER_LIST_FILE.write_text(json.dumps(master, indent=2) + "\n", encoding="utf-8")

    print(f"Enriched {len(enriched)} companies ({master['_meta']['ats_api_ready']} with live ATS APIs) -> {MASTER_LIST_FILE}")
    for r in enriched[:12]:
        print(f"  - {r['company_name']:24s} | {r['industry_grade']:2s} | ats={r['ats_platform']:10s} | jobs={r['open_jobs_detected']:3d} | {r['career_portal_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

