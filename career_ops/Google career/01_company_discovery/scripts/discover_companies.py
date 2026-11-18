#!/usr/bin/env python3
"""Stage 1: Live Company Discovery across public APIs (YC, HN, TechCrunch, Inc42).

Finds high-signal companies BEFORE job-board scraping, applies location & stage
pre-filters, grades target industries, and writes deduplicated candidates to:
  01_company_discovery/companies/discovered_candidates.json
"""

from __future__ import annotations

import argparse
import html
import json
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "01_company_discovery" / "companies"
OUT_JSON = OUT_DIR / "discovered_candidates.json"
OUT_MD = OUT_DIR / "discovered_candidates.md"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

ALLOWED_LOCATION_HINTS = (
    "remote", "india", "bengaluru", "bangalore", "mumbai", "delhi", "gurgaon",
    "dubai", "uae", "united arab emirates", "uk", "united kingdom", "london",
    "worldwide", "anywhere", "global",
)
US_CA_ONLY_HINTS = (
    "us only", "usa only", "u.s. only", "remote (us)", "remote - us",
    "united states only", "canada only", "north america only", "must be authorized to work in the us",
)
ROLE_HINTS = (
    "product manager", "product management", "founding pm", "head of product",
    "product marketing", "pmm", "chief of staff", "founder's office", "founders office",
    "forward deployed", "customer engineer", "solutions engineer", "ai engineer",
)

INDUSTRY_RULES: list[tuple[str, str, int, tuple[str, ...]]] = [
    ("Hiring & Recruitment Tech", "A+", 10, ("recruiting", "recruitment", "applicant tracking", "talent acquisition", "hr tech", "hrtech", "hiring platform", "staffing", "payroll", "background check", "workforce")),
    ("AI & Automation", "A", 9, ("ai", "llm", "agent", "machine learning", "automation", "genai", "copilot", "inference")),
    ("Ecommerce & Dropshipping", "A-", 8, ("ecommerce", "e-commerce", "dropship", "shopify", "d2c", "retail", "commerce", "marketplace")),
    ("Marketing & Sales Tech", "B+", 7, ("marketing", "sales", "crm", "growth", "seo", "outreach", "adtech", "martech", "revenue")),
    ("Trading & Finance", "B", 6, ("fintech", "trading", "finance", "payments", "banking", "crypto", "wealth", "lending", "derivatives")),
]


def http_get_json(url: str, timeout: int = 15) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def strip_html(text: str) -> str:
    cleaned = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", html.unescape(cleaned)).strip()


def grade_industry(text: str) -> tuple[str, str, int]:
    low = text.lower()
    for name, grade, score, kws in INDUSTRY_RULES:
        if any(re.search(rf"\b{re.escape(kw)}\b", low) if len(kw) <= 3 else kw in low for kw in kws):
            return name, grade, score
    return "Other", "C", 3


def normalize_domain(url: str) -> str:
    if not url:
        return ""
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def location_allowed(text: str) -> bool:
    low = text.lower()
    if any(bad in low for bad in US_CA_ONLY_HINTS) and "india" not in low and "global" not in low and "worldwide" not in low:
        return False
    return any(good in low for good in ALLOWED_LOCATION_HINTS)


def fetch_yc_companies(max_pages: int = 5) -> list[dict[str, Any]]:
    """Fetch actively hiring YC companies filtered to India, Remote, and UK regions."""
    results: list[dict[str, Any]] = []
    region_queries = [
        ("India", 4),
        ("United%20Kingdom", 3),
        ("Remote", max_pages),
    ]
    for region, pages in region_queries:
        for page in range(1, pages + 1):
            data = http_get_json(
                f"https://api.ycombinator.com/v0.1/companies?isHiring=true&regions={region}&page={page}"
            )
            companies = data.get("companies", [])
            if not companies:
                break
            for c in companies:
                regions = c.get("regions") or []
                locs = c.get("locations") or []
                team_size = int(c.get("teamSize") or 0)
                if team_size and team_size < 10:
                    continue
                text_blob = f"{c.get('oneLiner', '')} {c.get('longDescription', '')} {' '.join(c.get('tags') or [])} {' '.join(c.get('industries') or [])}"
                ind_name, ind_grade, ind_score = grade_industry(text_blob)
                results.append({
                    "company_name": c.get("name", "").strip(),
                    "slug": c.get("slug", "").strip(),
                    "website": c.get("website", "").strip(),
                    "domain": normalize_domain(c.get("website", "")),
                    "source_id": "yc_companies",
                    "source_url": c.get("url", ""),
                    "batch_or_round": f"YC {c.get('batch', '')}".strip(),
                    "investors": ["Y Combinator"],
                    "investor_tier": 1,
                    "team_size": team_size,
                    "locations": regions + locs,
                    "industry": ind_name,
                    "industry_grade": ind_grade,
                    "industry_score": ind_score,
                    "summary": c.get("oneLiner", "").strip(),
                    "role_signal": f"hiring_badge ({urllib.parse.unquote(region)})",
                })
    return results


def fetch_surge_companies() -> list[dict[str, Any]]:
    """Fetch Peak XV (Sequoia India) Surge portfolio companies from surgeahead.com."""
    req = urllib.request.Request("https://www.surgeahead.com/companies", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
    except Exception:
        return []
    slugs = list(dict.fromkeys(re.findall(r'href="https://www\.surgeahead\.com/companies/([a-z0-9-]+)"', raw)))
    if not slugs:
        slugs = list(dict.fromkeys(re.findall(r'href="/companies/([a-z0-9-]+)"', raw)))
    results: list[dict[str, Any]] = []
    for slug in slugs[:40]:
        name = slug.replace("-", " ").title()
        results.append({
            "company_name": name,
            "slug": slug,
            "website": "",
            "domain": "",
            "source_id": "surge_peakxv",
            "source_url": f"https://www.surgeahead.com/companies/{slug}",
            "batch_or_round": "Peak XV Surge",
            "investors": ["Peak XV Partners"],
            "investor_tier": 1,
            "team_size": 25,
            "locations": ["India", "Global"],
            "industry": "Other",
            "industry_grade": "C",
            "industry_score": 4,
            "summary": f"Peak XV Surge portfolio company ({name})",
            "role_signal": "surge_portfolio",
        })
    return results


def _parse_hn_comment(cid: int) -> dict[str, Any] | None:
    try:
        item = http_get_json(f"https://hacker-news.firebaseio.com/v0/item/{cid}.json", timeout=10)
    except Exception:
        return None
    if not item or item.get("deleted") or item.get("dead") or not item.get("text"):
        return None
    raw_html = item["text"]
    plain = strip_html(raw_html)
    first_line = strip_html(raw_html.split("<p>")[0])
    if not location_allowed(plain):
        return None

    low = plain.lower()
    matched_roles = [r for r in ROLE_HINTS if r in low]
    ind_name, ind_grade, ind_score = grade_industry(plain)
    if not matched_roles and ind_score < 7:
        return None

    urls = re.findall(r"https?://[^\s<>\"')]+", raw_html)
    website = next((u for u in urls if "ycombinator.com" not in u and "linkedin.com" not in u), "")
    company_name = first_line.split("|")[0].strip()[:80]
    if not company_name:
        return None

    return {
        "company_name": company_name,
        "slug": re.sub(r"[^a-z0-9]+", "-", company_name.lower()).strip("-"),
        "website": website,
        "domain": normalize_domain(website),
        "source_id": "hacker_news",
        "source_url": f"https://news.ycombinator.com/item?id={cid}",
        "batch_or_round": "HN Who Is Hiring",
        "investors": [],
        "investor_tier": 0,
        "team_size": 0,
        "locations": [seg.strip() for seg in first_line.split("|")[1:4]],
        "industry": ind_name,
        "industry_grade": ind_grade,
        "industry_score": ind_score,
        "summary": plain[:240],
        "role_signal": ", ".join(matched_roles) if matched_roles else "domain_match",
    }


def fetch_hn_hiring(max_comments: int = 80) -> list[dict[str, Any]]:
    """Fetch companies from the latest 'Ask HN: Who is hiring?' thread."""
    search = http_get_json(
        "https://hn.algolia.com/api/v1/search_by_date?query=Who+is+hiring&tags=story,author_whoishiring&hitsPerPage=3"
    )
    hits = [h for h in search.get("hits", []) if "who is hiring" in h.get("title", "").lower()]
    if not hits:
        return []
    thread_id = hits[0]["objectID"]
    thread = http_get_json(f"https://hacker-news.firebaseio.com/v0/item/{thread_id}.json")
    kids = (thread.get("kids") or [])[:max_comments]

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(_parse_hn_comment, cid) for cid in kids]
        for fut in as_completed(futures):
            parsed = fut.result()
            if parsed:
                results.append(parsed)
    return results


def fetch_wp_funding_news(source_id: str, base_url: str, per_page: int = 20) -> list[dict[str, Any]]:
    """Fetch recent funding articles from WordPress REST API (TechCrunch / Inc42)."""
    posts = http_get_json(f"{base_url}?per_page={per_page}")
    results: list[dict[str, Any]] = []
    funding_kw = ("series a", "series b", "series c", "raises", "raised", "funding", "backed by", "led by")
    exclude_kw = ("layoff", "shuts down", "shutdown", "bankrupt", "ipo filing")

    for post in posts:
        title = strip_html(post.get("title", {}).get("rendered", ""))
        excerpt = strip_html(post.get("excerpt", {}).get("rendered", ""))
        blob = f"{title} {excerpt}".lower()
        if any(bad in blob for bad in exclude_kw):
            continue
        if not any(kw in blob for kw in funding_kw):
            continue

        # Guess company name from leading phrase before raises/secures/closes/gets
        m = re.match(r"^([A-Z0-9][A-Za-z0-9&.\- ]{1,40}?)\s+(?:raises|raised|secures|closes|bags|nabs|lands|gets)\b", title)
        company_name = m.group(1).strip() if m else title[:50]
        ind_name, ind_grade, ind_score = grade_industry(blob)
        results.append({
            "company_name": company_name,
            "slug": re.sub(r"[^a-z0-9]+", "-", company_name.lower()).strip("-"),
            "website": "",
            "domain": "",
            "source_id": source_id,
            "source_url": post.get("link", ""),
            "batch_or_round": "Funding News",
            "investors": [],
            "investor_tier": 0,
            "team_size": 0,
            "locations": ["India"] if source_id == "inc42" else ["Global"],
            "industry": ind_name,
            "industry_grade": ind_grade,
            "industry_score": ind_score,
            "summary": f"{title} — {excerpt[:140]}",
            "role_signal": "fresh_funding_round",
        })
    return results


def deduplicate(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for c in candidates:
        key = c.get("domain") or re.sub(r"[^a-z0-9]", "", c.get("company_name", "").lower())
        if not key:
            continue
        if key not in seen:
            c["sources_seen"] = [c["source_id"]]
            seen[key] = c
        else:
            existing = seen[key]
            if c["source_id"] not in existing["sources_seen"]:
                existing["sources_seen"].append(c["source_id"])
            if not existing.get("website") and c.get("website"):
                existing["website"] = c["website"]
                existing["domain"] = c["domain"]
            if c.get("investor_tier", 0) > existing.get("investor_tier", 0):
                existing["investor_tier"] = c["investor_tier"]
                existing["investors"] = c["investors"]
    return sorted(seen.values(), key=lambda x: (-x.get("investor_tier", 0), -x.get("industry_score", 0), x.get("company_name", "")))


def write_outputs(candidates: list[dict[str, Any]]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_candidates": len(candidates),
        "candidates": candidates,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Stage 1: Discovered Candidate Companies",
        "",
        f"Generated: `{payload['generated_at']}` | Total: **{len(candidates)}**",
        "",
        "| # | Company | Grade | Industry | Source | Round / Batch | Website | Signal |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for idx, c in enumerate(candidates, 1):
        site = c.get("website") or "—"
        lines.append(
            f"| {idx} | **{c['company_name']}** | {c['industry_grade']} | {c['industry']} | "
            f"{', '.join(c.get('sources_seen', [c['source_id']]))} | {c.get('batch_or_round', '—')} | "
            f"{site} | {c.get('role_signal', '')} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage 1 Company Discovery")
    parser.add_argument("--sources", default="yc,surge,hn,techcrunch,inc42", help="Comma-separated sources")
    parser.add_argument("--yc-pages", type=int, default=6, help="YC Remote API pages to scan")
    parser.add_argument("--hn-comments", type=int, default=80, help="HN thread comments to inspect")
    args = parser.parse_args()

    wanted = {s.strip().lower() for s in args.sources.split(",") if s.strip()}
    raw: list[dict[str, Any]] = []

    if "yc" in wanted:
        yc = fetch_yc_companies(max_pages=args.yc_pages)
        print(f"[yc] discovered {len(yc)} India/UK/Remote hiring companies (team>=10)")
        raw.extend(yc)
    if "surge" in wanted:
        surge = fetch_surge_companies()
        print(f"[surge] discovered {len(surge)} Peak XV Surge portfolio companies")
        raw.extend(surge)
    if "hn" in wanted:
        hn = fetch_hn_hiring(max_comments=args.hn_comments)
        print(f"[hn] discovered {len(hn)} matching companies from latest Who Is Hiring")
        raw.extend(hn)
    if "techcrunch" in wanted:
        tc = fetch_wp_funding_news("techcrunch", "https://techcrunch.com/wp-json/wp/v2/posts", per_page=25)
        print(f"[techcrunch] discovered {len(tc)} funding articles")
        raw.extend(tc)
    if "inc42" in wanted:
        inc = fetch_wp_funding_news("inc42", "https://inc42.com/wp-json/wp/v2/posts", per_page=25)
        print(f"[inc42] discovered {len(inc)} funding articles")
        raw.extend(inc)

    deduped = deduplicate(raw)
    write_outputs(deduped)
    print(f"Saved {len(deduped)} deduplicated candidates -> {OUT_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

