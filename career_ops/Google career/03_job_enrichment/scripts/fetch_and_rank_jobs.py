#!/usr/bin/env python3
"""Stage 2 + Stage 3 Runner: Fetch live jobs & score work-profile fit via BM25+Vector+RRF.

Updates per user preferences:
  - NO pure Forward Deployed Engineer / Java / C++ / backend-coding SWE roles.
  - Title-agnostic matching for non-SWE roles: Forward Deployed PM, AI Builder,
    Product Manager, Product Marketing Manager, Strategic Partner Manager, Chief of Staff,
    or any hybrid role whose JD matches Satvik's verified Bullet Bank v7 via RRF.
  - Strict location filter: Remote India / Global / Dubai / UK only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
COMPANIES_DIR = ROOT / "01_company_discovery" / "companies"
WATCHLIST_FILE = COMPANIES_DIR / "watchlist.json"
MASTER_FILE = COMPANIES_DIR / "master_list.json"
OUT_DIR = ROOT / "03_job_enrichment" / "matched_jobs"
OUT_JSON = OUT_DIR / "top10_test_report.json"
OUT_MD = OUT_DIR / "top10_test_report.md"

sys.path.insert(0, str(ROOT / "03_job_enrichment" / "scripts"))
import jd_resume_matcher as jrm  # noqa: E402

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

ACCEPT_LOC_RE = re.compile(
    r"\b(remote.*india|india.*remote|dubai|uae|united arab emirates|uk|united kingdom|london|england|"
    r"global|worldwide|anywhere)\b",
    re.I,
)
US_CA_RE = re.compile(
    r"\b(usa|u\.s\.|united states|utah|lehi|san francisco|new york|nyc|california|texas|austin|"
    r"seattle|boston|chicago|los angeles|canada|toronto|vancouver|north america|amer|namer|"
    r"us remote|us - remote|remote - us|remote, us|remote \(us\)|remote-us|united states only|us only|"
    r"latam|remote - europe|europe|emea only|eu remote|germany|france|spain|italy|netherlands|poland)\b"
    r"|,\s*us\b",
    re.I,
)

NON_SWE_ROLE_PRIORITIES: list[tuple[int, str, re.Pattern[str]]] = [
    (1, "Forward Deployed PM / AI Builder", re.compile(
        r"\b(forward deployed product|ai builder|ai product manager|founding product|"
        r"solutions consultant|implementation consultant|deployment strategist|ai solutions)\b", re.I
    )),
    (2, "Product Manager", re.compile(
        r"\b(product manager|head of product|vp of product|director of product|"
        r"founding pm|principal pm|group pm|product lead|product owner)\b", re.I
    )),
    (3, "Product Marketing Manager", re.compile(
        r"\b(product marketing|pmm)\b", re.I
    )),
    (4, "CoS / Strategic Partner / Growth", re.compile(
        r"\b(chief of staff|founder'?s office|founders office|strategic partner|partnerships|"
        r"business operations|strategy & operations)\b", re.I
    )),
]

HARD_SKIP_TITLES = (
    "intern", "associate product manager", "apm", "product operations",
    "product design", "product designer", "ux ", "ui/ux",
    "account executive", "sales development", "sdr", "bdr", "recruiter",
    "software engineer", "backend engineer", "frontend engineer", "full-stack",
    "full stack", "devops", "site reliability", "sre", "qa engineer",
    "security engineer", "data engineer", "research scientist", "machine learning engineer",
    "applied ai engineer", "ai engineer",
    "engineering manager", "director of engineering", "director, engineering", "vp engineering",
    "mechanical", "electrical engineer", "hardware engineer", "legal fellow", "medical fellow", "stem fellow",
    "counsel", "paralegal", "accountant", "controller",
    "italian speaking", "german speaker", "french speaker", "spanish speaker", "japanese speaker", "dutch speaking",
)


def http_get_json(url: str, timeout: int = 12) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_company_jobs(comp: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    ats = comp.get("ats_platform", "unknown")
    slug = comp.get("ats_slug", "")
    if not slug or ats not in ("ashby", "greenhouse", "lever"):
        return [], f"skipped (ats={ats})"

    try:
        if ats == "greenhouse":
            data = http_get_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true")
            return [
                {
                    "job_id": f"gh_{slug}_{j['id']}",
                    "title": j.get("title", ""),
                    "location": (j.get("location") or {}).get("name", ""),
                    "job_url": j.get("absolute_url", ""),
                    "published_at": j.get("updated_at", ""),
                    "description": re.sub(r"<[^>]+>", " ", j.get("content") or "")[:3500],
                }
                for j in data.get("jobs", [])
            ], "ok"

        if ats == "ashby":
            data = http_get_json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true")
            jobs = []
            for j in data.get("jobs", []):
                loc = j.get("location", "")
                if j.get("isRemote") and "remote" not in loc.lower():
                    loc = f"Remote ({loc})" if loc else "Remote"
                jobs.append({
                    "job_id": f"ashby_{slug}_{j['id']}",
                    "title": j.get("title", ""),
                    "location": loc,
                    "job_url": j.get("jobUrl", ""),
                    "published_at": j.get("publishedAt", ""),
                    "description": (j.get("descriptionPlain") or "")[:3500],
                })
            return jobs, "ok"

        if ats == "lever":
            data = http_get_json(f"https://api.lever.co/v0/postings/{slug}?mode=json&limit=250")
            return [
                {
                    "job_id": f"lever_{slug}_{j['id']}",
                    "title": j.get("text", ""),
                    "location": f"{(j.get('categories') or {}).get('location', '')} ({j.get('workplaceType', '')})".strip(),
                    "job_url": j.get("hostedUrl", ""),
                    "published_at": str(j.get("createdAt", "")),
                    "description": (j.get("descriptionPlain") or "")[:3500],
                }
                for j in (data if isinstance(data, list) else [])
            ], "ok"
    except Exception as exc:
        return [], f"error: {exc}"

    return [], "unsupported"


def location_passes(loc: str) -> tuple[bool, str]:
    text = (loc or "").strip()
    if not text:
        return False, "no_location"
    has_accept = bool(ACCEPT_LOC_RE.search(text))
    has_us_ca = bool(US_CA_RE.search(text))
    is_plain_remote = "remote" in text.lower() and not has_us_ca

    if has_accept:
        return True, "explicit_target_geo"
    if is_plain_remote:
        return True, "unrestricted_remote"
    if has_us_ca:
        return False, "rejected_us_ca_only"
    return False, "rejected_other_onsite"


def classify_title(title: str) -> tuple[int, str] | None:
    low = (title or "").lower()
    if any(bad in low for bad in HARD_SKIP_TITLES):
        return None
    if re.search(r"\b(product marketing|pmm)\b", low):
        return 3, "Product Marketing Manager"
    for rank, label, rx in NON_SWE_ROLE_PRIORITIES:
        if rx.search(title):
            return rank, label
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage 2+3 live fetch + RRF Resume-to-JD Matcher")
    parser.add_argument("--top", type=int, default=35, help="Max companies to test")
    parser.add_argument("--require-ats", action="store_true", help="Only pick companies with live ATS APIs")
    parser.add_argument("--min-fit", type=float, default=15.0, help="Min RRF resume fit score (0-100)")
    args = parser.parse_args()

    src = WATCHLIST_FILE if WATCHLIST_FILE.exists() else MASTER_FILE
    companies = json.loads(src.read_text(encoding="utf-8")).get("companies", [])
    if args.require_ats:
        companies = [c for c in companies if c.get("has_portal_api") and c.get("open_jobs_detected", 0) > 0]
    selected = companies[:args.top]

    bullets = jrm.load_bullet_bank()
    rrf_index = jrm.HybridRRFIndex(bullets)

    company_summaries: list[dict[str, Any]] = []
    matched_jobs: list[dict[str, Any]] = []

    for c in selected:
        jobs, status = fetch_company_jobs(c)
        geo_hits = 0
        final_hits = 0
        for j in jobs:
            ok_loc, loc_reason = location_passes(j["location"])
            if not ok_loc:
                continue
            geo_hits += 1

            role_cls = classify_title(j["title"])
            if any(bad in (j["title"] or "").lower() for bad in HARD_SKIP_TITLES):
                continue

            eval_res = jrm.evaluate_jd(j["title"], j["description"], rrf_index)
            if eval_res["rejected_for_coding_swe"]:
                continue
            if not role_cls and eval_res["fit_score"] < 35.0:
                continue
            if eval_res["fit_score"] < args.min_fit:
                continue

            final_hits += 1
            rank, role_label = role_cls or (2, "Hybrid / Work-Profile Match")
            zero_to_one = bool(re.search(r"0[- ]to[- ]1|zero to one|founding|from scratch|greenfield", j["description"], re.I))
            matched_jobs.append({
                "company_name": c["company_name"],
                "company_score": c["score"],
                "industry": f"{c['industry_grade']} {c['industry']}",
                "ats_platform": c["ats_platform"],
                "role_priority": rank,
                "role_category": role_label,
                "title": j["title"],
                "location": j["location"],
                "location_reason": loc_reason,
                "resume_fit_score": eval_res["fit_score"],
                "matched_phrases": f"{eval_res['matched_phrases']}/{eval_res['total_jd_phrases']}",
                "top_bullets": [b["bullet_id"] for b in eval_res["top_strength_bullets"][:4]],
                "top_gap": eval_res["top_gaps"][0]["phrase"][:100] if eval_res["top_gaps"] else "",
                "zero_to_one_signal": zero_to_one,
                "job_url": j["job_url"],
                "career_portal_url": c["career_portal_url"],
                "founders": [{"name": f["name"], "linkedin": f.get("linkedin", "")} for f in c.get("founders", [])],
            })

        company_summaries.append({
            "company_name": c["company_name"],
            "score": c["score"],
            "ats_platform": c["ats_platform"],
            "fetch_status": status,
            "total_jobs_fetched": len(jobs),
            "geo_pass_jobs": geo_hits,
            "matched_jobs": final_hits,
        })

    matched_jobs.sort(key=lambda x: (-x["resume_fit_score"], -x["company_score"], x["role_priority"]))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "companies_tested": len(selected),
        "company_summaries": company_summaries,
        "matched_jobs_count": len(matched_jobs),
        "matched_jobs": matched_jobs,
    }, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# Stage 2 & 3 Matched Roles (RRF Resume Matcher + Non-Coding Filter)",
        "",
        f"Generated: `{datetime.now(timezone.utc).isoformat()}` | Companies Tested: **{len(selected)}** | Matched Jobs: **{len(matched_jobs)}**",
        "",
        "| Fit % | Co Score | Company | Prio | Role Title | Location | Matched Bullets | Apply |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for m in matched_jobs:
        lines.append(
            f"| **{m['resume_fit_score']}%** | {m['company_score']} | **{m['company_name']}** | P{m['role_priority']} | "
            f"{m['title']} | {m['location']} | `{', '.join(m['top_bullets'])}` | [Job Link]({m['job_url']}) |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Tested {len(selected)} companies -> {len(matched_jobs)} RRF-matched non-coding roles -> {OUT_MD}")
    for m in matched_jobs[:15]:
        print(f"  - fit={m['resume_fit_score']:5.1f}% | co={m['company_score']:3d} | P{m['role_priority']} | {m['company_name']:16s} | {m['title'][:45]:45s} | {m['location']} | {m['top_bullets']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
