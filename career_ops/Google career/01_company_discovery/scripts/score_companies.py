#!/usr/bin/env python3
"""Stage 1C: Company Scoring, Founder Intel & Watchlist Promotion.

Enriches companies in master_list.json with:
  1. Free YC public founder bios + LinkedIn URLs (from data-page JSON)
  2. Optional rate-limited LinkedIn burner profile data (from cache or --use-linkedin-burner)
  3. Accurate company scoring (0-100 across Investors, Education, Pedigree, Exits, Industry, Location, Stage)
  4. Promoted watchlist output -> watchlist.json + watchlist.md
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
COMPANIES_DIR = ROOT / "01_company_discovery" / "companies"
MASTER_LIST_FILE = COMPANIES_DIR / "master_list.json"
WATCHLIST_JSON = COMPANIES_DIR / "watchlist.json"
WATCHLIST_MD = COMPANIES_DIR / "watchlist.md"

sys.path.insert(0, str(ROOT / "01_company_discovery" / "scripts"))
import linkedin_burner_enricher as lbe  # noqa: E402

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

ELITE_EDU = (
    "iit", "indian institute of technology", "iim", "harvard", "stanford", "mit",
    "yale", "princeton", "columbia", "upenn", "university of pennsylvania", "wharton",
    "dartmouth", "brown", "cornell",
)
TOP100_EDU = (
    "berkeley", "uc berkeley", "cmu", "carnegie mellon", "caltech", "oxford",
    "cambridge", "imperial college", "eth zurich", "nus", "ntu", "ucla",
    "uchicago", "university of michigan", "waterloo", "bits pilani", "iisc",
    "georgia tech", "ut austin", "nyu", "epita", "ecole polytechnique", "oxford",
)
BIG_PEDIGREE = (
    "google", "meta", "facebook", "amazon", "apple", "microsoft", "netflix",
    "stripe", "uber", "airbnb", "openai", "anthropic", "palantir", "databricks",
    "snowflake", "mckinsey", "bcg", "bain", "goldman sachs", "morgan stanley",
    "flipkart", "swiggy", "razorpay", "linkedin", "twitter", "dropbox",
)
EXIT_WORDS = ("acquired", "sold to", "exited", "acquisition", "ipo", "went public")

INDUSTRY_FIX: list[tuple[str, str, int, tuple[str, ...]]] = [
    ("Hiring & Recruitment Tech", "A+", 10, ("recruiting", "recruitment", "applicant tracking", "talent acquisition", "hr tech", "hrtech", "hiring platform", "staffing", "payroll", "background check")),
    ("AI & Automation", "A", 9, ("ai", "llm", "agent", "machine learning", "automation", "genai", "copilot", "inference", "voice ai", "speech")),
    ("Ecommerce & Dropshipping", "A-", 8, ("ecommerce", "e-commerce", "dropship", "shopify", "d2c", "wholesale", "retail", "marketplace")),
    ("Marketing & Sales Tech", "B+", 7, ("marketing", "sales", "crm", "growth", "seo", "outreach", "adtech", "martech", "search api")),
    ("Trading & Finance", "B", 6, ("fintech", "trading", "finance", "payments", "banking", "401(k)", "retirement", "wealth", "lending", "credit")),
]


def fetch_yc_founders(yc_url: str) -> tuple[list[dict[str, Any]], str]:
    """Fetch founders list & company LinkedIn from public YC company page."""
    if not yc_url or "ycombinator.com/companies/" not in yc_url:
        return [], ""
    req = urllib.request.Request(yc_url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return [], ""

    m = re.search(r'data-page="([^"]+)"', raw)
    if not m:
        return [], ""
    try:
        comp = json.loads(html.unescape(m.group(1))).get("props", {}).get("company", {})
    except Exception:
        return [], ""

    founders = []
    for f in comp.get("founders", []):
        founders.append({
            "name": f.get("full_name", "").strip(),
            "title": f.get("title", "").strip(),
            "linkedin": (f.get("linkedin_url") or "").strip(),
            "twitter": (f.get("twitter_url") or "").strip(),
            "bio": (f.get("founder_bio") or "").strip(),
        })
    return founders, (comp.get("linkedin_url") or "").strip()


def refine_industry(summary: str, current_ind: str) -> tuple[str, str, int]:
    low = summary.lower()
    for name, grade, score, kws in INDUSTRY_FIX:
        if any(re.search(rf"\b{re.escape(kw)}\b", low) if len(kw) <= 3 else kw in low for kw in kws):
            return name, grade, score
    return "Other", "C", 4


def exa_search_founder(founder_name: str, company_name: str) -> str:
    """Query Exa's keyless hosted MCP (pattern from vendor/agent-reach) for founder bio/edu/exits."""
    query = f'"{founder_name}" "{company_name}" education university previous startup acquired'
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "web_search_exa", "arguments": {"query": query, "numResults": 3}},
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://mcp.exa.ai/mcp",
        data=payload,
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
        lines = [ln[5:].strip() for ln in raw.splitlines() if ln.startswith("data:")] or [raw]
        msg = json.loads(lines[-1])
        return "\n".join(c.get("text", "") for c in msg.get("result", {}).get("content", []) if c.get("type") == "text")[:3000]
    except Exception:
        return ""


def score_founder(founder: dict[str, Any], li_prof: dict[str, Any] | None, exa_text: str = "") -> dict[str, Any]:
    parts = [founder.get("bio", ""), founder.get("title", ""), exa_text]
    if li_prof:
        parts.append(li_prof.get("headline", ""))
        parts.append(li_prof.get("summary", ""))
        parts.extend(f"{e.get('school','')} {e.get('degree','')} {e.get('field','')}" for e in li_prof.get("educations", []))
        parts.extend(f"{p.get('company','')} {p.get('title','')} {p.get('description','')}" for p in li_prof.get("positions", []))
    blob = " ".join(parts).lower()

    # Education (max 15)
    edu_score = 0
    edu_note = "unknown (needs LinkedIn check)"
    if any(re.search(rf"\b{re.escape(k)}\b", blob) for k in ELITE_EDU):
        edu_score = 15
        edu_note = "IIT / IIM / Ivy League signal"
    elif any(k in blob for k in TOP100_EDU):
        edu_score = 10
        edu_note = "Top-100 / notable engineering school"
    elif any(w in blob for w in ("university", "college", "phd", "b.s.", "m.s.", "btech", "degree")):
        edu_score = 5
        edu_note = "University degree mentioned"

    # Career pedigree (max 20)
    career_hits = [c for c in BIG_PEDIGREE if re.search(rf"\b{re.escape(c)}\b", blob)]
    serial = any(p in blob for p in ("previously founded", "co-founded", "serial", "prior startup", "earlier founded", "founded"))
    career_score = min(20, len(career_hits) * 9 + (10 if serial else 0) + (5 if len(blob) > 120 and not career_hits else 0))

    # Past exits (max 15)
    exit_hits = sum(1 for w in EXIT_WORDS if w in blob)
    exit_score = 15 if exit_hits >= 2 else (10 if exit_hits == 1 else 0)

    return {
        **founder,
        "education_score": edu_score,
        "education_signal": edu_note,
        "career_score": career_score,
        "career_signals": career_hits + (["serial_founder"] if serial else []),
        "exit_score": exit_score,
        "has_exa_detail": bool(exa_text),
        "has_linkedin_detail": bool(li_prof),
        "needs_linkedin_lookup": bool(founder.get("linkedin")) and (edu_score == 0 or career_score < 10) and not li_prof,
    }


def score_company(
    rec: dict[str, Any],
    li_cache: dict[str, dict[str, Any]],
    exa_cache: dict[str, str] | None = None,
) -> dict[str, Any]:
    founders_raw, company_li = fetch_yc_founders(rec.get("source_url", ""))
    exa_cache = exa_cache or {}
    scored_founders: list[dict[str, Any]] = []
    for f in founders_raw:
        pid = lbe.extract_public_id(f.get("linkedin", ""))
        ekey = f"{f.get('name', '').lower()}::{rec.get('company_name', '').lower()}"
        scored_founders.append(score_founder(f, li_cache.get(pid), exa_cache.get(ekey, "")))

    best_edu = max((f["education_score"] for f in scored_founders), default=0)
    best_career = max((f["career_score"] for f in scored_founders), default=0)
    best_exit = max((f["exit_score"] for f in scored_founders), default=0)

    tier = rec.get("investor_tier", 0)
    investor_score = 20 if tier == 1 else (14 if tier == 2 else (8 if tier == 3 else 0))

    ind_name, ind_grade, ind_score = refine_industry(rec.get("summary", ""), rec.get("industry", "Other"))
    locs = " ".join(rec.get("locations", [])).lower()
    loc_score = 10 if ("remote" in locs or "india" in locs) else (8 if ("uk" in locs or "london" in locs or "dubai" in locs) else 5)

    team = int(rec.get("team_size") or 0)
    # Series A+ and large highly-funded companies are both great; penalize only very early (<15)
    stage_score = 10 if team >= 15 else (6 if team >= 8 else 2)

    total = investor_score + best_edu + best_career + best_exit + ind_score + loc_score + stage_score
    recommendation = "strong_match" if total >= 75 else ("consider" if total >= 55 else "watch_needs_intel")

    rec.update({
        "company_linkedin": company_li,
        "industry": ind_name,
        "industry_grade": ind_grade,
        "industry_score": ind_score,
        "founders": scored_founders,
        "score": total,
        "recommendation": recommendation,
        "score_breakdown": {
            "investor_quality": investor_score,
            "founder_education": best_edu,
            "founder_career": best_career,
            "past_exits": best_exit,
            "industry_match": ind_score,
            "location_compliance": loc_score,
            "product_stage_fit": stage_score,
        },
        "needs_linkedin_burner_lookup": any(f.get("needs_linkedin_lookup") for f in scored_founders),
        "research_status": "scored",
    })
    return rec


EXA_CACHE_FILE = lbe.vault.REFRESHES_DIR / "exa_founder_cache.json"


def _rescore_from_caches(companies: list[dict[str, Any]], li_cache: dict[str, Any], exa_cache: dict[str, str]) -> list[dict[str, Any]]:
    """Recompute founder & company scores from already-fetched founders + caches."""
    out: list[dict[str, Any]] = []
    for rec in companies:
        scored_founders = []
        for f in rec.get("founders", []):
            pid = lbe.extract_public_id(f.get("linkedin", ""))
            ekey = f"{f.get('name', '').lower()}::{rec.get('company_name', '').lower()}"
            scored_founders.append(score_founder(f, li_cache.get(pid), exa_cache.get(ekey, "")))
        best_edu = max((f["education_score"] for f in scored_founders), default=0)
        best_career = max((f["career_score"] for f in scored_founders), default=0)
        best_exit = max((f["exit_score"] for f in scored_founders), default=0)
        sb = rec["score_breakdown"]
        sb["founder_education"] = best_edu
        sb["founder_career"] = best_career
        sb["past_exits"] = best_exit
        total = (
            sb["investor_quality"] + best_edu + best_career + best_exit
            + sb["industry_match"] + sb["location_compliance"] + sb["product_stage_fit"]
        )
        rec["founders"] = scored_founders
        rec["score"] = total
        rec["recommendation"] = "strong_match" if total >= 75 else ("consider" if total >= 55 else "watch_needs_intel")
        rec["needs_linkedin_burner_lookup"] = any(f.get("needs_linkedin_lookup") for f in scored_founders)
        out.append(rec)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Score discovered companies and promote qualified watchlist")
    parser.add_argument("--use-exa", action="store_true", help="Query keyless Exa MCP (from agent-reach) before LinkedIn burner")
    parser.add_argument("--exa-limit", type=int, default=8, help="Max live Exa founder lookups (default: 8)")
    parser.add_argument("--use-linkedin-burner", action="store_true", help="Fetch missing founder profiles via linkedin_burner")
    parser.add_argument("--burner-limit", type=int, default=2, help="Max live burner LinkedIn lookups (default: 2)")
    parser.add_argument("--ignore-hours", action="store_true", help="Override IST business-hours guard for 1-2 test calls")
    args = parser.parse_args()

    if not MASTER_LIST_FILE.exists():
        raise SystemExit(f"Run detect_ats_and_enrich.py first ({MASTER_LIST_FILE} missing)")

    master = json.loads(MASTER_LIST_FILE.read_text(encoding="utf-8"))
    companies = master.get("companies", [])
    li_cache = lbe._load_json(lbe.CACHE_FILE, {})
    exa_cache: dict[str, str] = lbe._load_json(EXA_CACHE_FILE, {})

    scored: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(score_company, dict(c), li_cache, exa_cache) for c in companies]
        for fut in as_completed(futs):
            scored.append(fut.result())

    if args.use_exa:
        fetched = 0
        for c in sorted(scored, key=lambda x: -x["score"]):
            if fetched >= args.exa_limit:
                break
            if not c.get("needs_linkedin_burner_lookup"):
                continue
            for f in c.get("founders", []):
                if fetched >= args.exa_limit:
                    break
                ekey = f"{f.get('name', '').lower()}::{c.get('company_name', '').lower()}"
                if f.get("needs_linkedin_lookup") and ekey not in exa_cache:
                    txt = exa_search_founder(f.get("name", ""), c.get("company_name", ""))
                    exa_cache[ekey] = txt
                    fetched += 1
                    print(f"[exa] {f.get('name')} ({c.get('company_name')}): {len(txt)} chars")
        lbe._save_json(EXA_CACHE_FILE, exa_cache)
        scored = _rescore_from_caches(scored, li_cache, exa_cache)

    if args.use_linkedin_burner:
        needed_urls: list[str] = []
        for c in sorted(scored, key=lambda x: -x["score"]):
            if c.get("needs_linkedin_burner_lookup"):
                for f in c.get("founders", []):
                    if f.get("needs_linkedin_lookup") and f.get("linkedin"):
                        needed_urls.append(f["linkedin"])
        if needed_urls:
            updated_cache = lbe.enrich_urls(
                needed_urls,
                limit=args.burner_limit,
                ignore_hours=args.ignore_hours,
            )
            li_cache.update(updated_cache)
            scored = _rescore_from_caches(scored, li_cache, exa_cache)

    profiles_dir = COMPANIES_DIR / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    scored.sort(key=lambda x: (-x["score"], -x.get("open_jobs_detected", 0), x["company_name"]))
    for c in scored:
        (profiles_dir / f"{c['company_slug']}.json").write_text(json.dumps(c, indent=2) + "\n", encoding="utf-8")

    master["_meta"]["last_updated"] = datetime.now(timezone.utc).isoformat()
    master["_meta"]["scored"] = len(scored)
    master["companies"] = scored
    MASTER_LIST_FILE.write_text(json.dumps(master, indent=2) + "\n", encoding="utf-8")

    watchlist = [c for c in scored if c["score"] >= 55]
    WATCHLIST_JSON.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_watchlist": len(watchlist),
        "strong_match_count": sum(1 for c in watchlist if c["score"] >= 75),
        "consider_count": sum(1 for c in watchlist if 55 <= c["score"] < 75),
        "companies": watchlist,
    }, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Stage 1 Watchlist (Qualified Companies)",
        "",
        f"Total Qualified (>=55): **{len(watchlist)}** | Strong Match (>=75): **{sum(1 for c in watchlist if c['score'] >= 75)}**",
        "",
        "| Score | Tier | Company | Industry | ATS (Jobs) | Career Portal | Founders & LinkedIn |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in watchlist:
        tier_icon = "🟢" if c["score"] >= 75 else "🟡"
        f_links = ", ".join(
            f"[{f['name']}]({f['linkedin']})" if f.get("linkedin") else f["name"]
            for f in c.get("founders", [])
        ) or "—"
        lines.append(
            f"| **{c['score']}** | {tier_icon} {c['recommendation']} | **{c['company_name']}** | "
            f"{c['industry_grade']} {c['industry']} | {c['ats_platform']} ({c['open_jobs_detected']}) | "
            f"{c['career_portal_url']} | {f_links} |"
        )
    WATCHLIST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Scored {len(scored)} companies -> {len(watchlist)} qualified for watchlist ({WATCHLIST_MD})")
    for c in scored[:12]:
        flag = "🟢" if c["score"] >= 75 else ("🟡" if c["score"] >= 55 else "⚪")
        print(f"  {flag} {c['score']:3d}/100 | {c['company_name']:22s} | {c['industry_grade']:2s} {c['industry']:25s} | ats={c['ats_platform']}({c['open_jobs_detected']}) | need_li={c['needs_linkedin_burner_lookup']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

