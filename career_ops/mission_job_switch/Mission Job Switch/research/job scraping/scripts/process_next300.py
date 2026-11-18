"""
Process Next 300.md — parse markdown, discover career URLs, classify, append to career_urls_result.json.

Pipeline:
  1. Parse Next 300.md (5 batches × 3 segments × 20 = 300 companies)
  2. Build candidate career URLs from each homepage
  3. Reuse find_career_urls logic (process_company) to discover + classify
  4. Append to db/career_urls_result.json

Tracks errors → docs/next300_bug_log.md
"""

import asyncio
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
from collections import Counter

import httpx

# Reuse pipeline functions
sys.path.insert(0, str(Path(__file__).parent))
from find_career_urls import process_company, OUTPUT_FILE

BASE = Path(__file__).parent.parent
MD_PATH = BASE / "Next 300.md"
BUG_LOG = BASE / "db" / "next300_runtime_bugs.md"  # auto-generated; persistent record is docs/next300_bug_log.md

SEGMENT_MAP = {
    1: "india_mnc",
    2: "global_ai_startup",
    3: "dubai_visa",
}

# Common career page paths to try when only homepage is known
CAREER_PATHS = [
    "/careers",
    "/jobs",
    "/about/careers",
    "/company/careers",
    "/about-us/careers",
    "/en/careers",
    "/about/jobs",
    "/work-with-us",
    "/join-us",
    "/team",
]

bug_log: list[str] = []


def log_bug(stage: str, company: str, detail: str):
    bug_log.append(f"- **{stage}** | `{company}` | {detail}")


def parse_md(path: Path) -> list[dict]:
    """Parse Next 300.md → list of {company, segment, homepage}."""
    text = path.read_text(encoding="utf-8")

    # Split into segments by header markers
    # Each "## **Segment N:" starts a new segment block
    rows: list[dict] = []
    current_segment = None

    for line in text.split("\n"):
        # Detect segment header
        m_seg = re.match(r"##\s+\*\*Segment\s+(\d+)", line)
        if m_seg:
            current_segment = int(m_seg.group(1))
            continue

        # Detect table row: | **Company** | ... | ... | ... | [https://...](...) |
        if current_segment and line.strip().startswith("|") and "**" in line:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) < 5:
                continue
            # Skip header row
            if cells[0].lower().startswith("company name"):
                continue

            # Company name in **bold**
            m_name = re.search(r"\*\*([^*]+)\*\*", cells[0])
            if not m_name:
                continue
            company = m_name.group(1).strip()

            # URL — first [https://...] in last cell
            m_url = re.search(r"\[(https?://[^\]\s]+)\]", cells[-1])
            if not m_url:
                log_bug("parse_md", company, f"no URL found in row")
                continue
            homepage = m_url.group(1).rstrip("/")

            rows.append({
                "company": company,
                "segment": SEGMENT_MAP.get(current_segment, "unknown"),
                "homepage": homepage,
            })

    return rows


def build_candidates(homepage: str) -> list[str]:
    """Generate candidate career URLs from a company homepage.

    ORDER MATTERS — first match wins:
      1. Career subdomain (careers.X, jobs.X) — high-precision real URL
      2. Path candidates on the homepage (/careers, /jobs, etc.)
      3. ATS guesses (greenhouse/lever/ashby/{bare}) — verified via API in process_company
      4. Homepage itself — last resort
    """
    parsed = urlparse(homepage)
    if not parsed.netloc:
        return [homepage]

    root = f"{parsed.scheme}://{parsed.netloc}"
    domain = parsed.netloc.lstrip("www.")
    bare = domain.split(".")[0]

    candidates = []

    # 1. Career subdomain (high precision)
    candidates.append(f"https://careers.{domain}")
    candidates.append(f"https://jobs.{domain}")

    # 2. Path candidates on homepage
    candidates.extend(root + path for path in CAREER_PATHS)

    # 3. ATS guesses (will be API-verified inside process_company)
    candidates.extend([
        f"https://boards.greenhouse.io/{bare}",
        f"https://jobs.lever.co/{bare}",
        f"https://jobs.ashbyhq.com/{bare}",
    ])

    # 4. Homepage itself
    candidates.append(homepage)

    # Dedupe while preserving order
    seen = set()
    out = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


async def run():
    companies = parse_md(MD_PATH)
    print(f"Parsed {len(companies)} companies from Next 300.md")

    # Check for duplicates with existing career_urls_result.json
    existing = []
    if OUTPUT_FILE.exists():
        existing = json.loads(OUTPUT_FILE.read_text())
    existing_names = {e["company"].lower().strip() for e in existing}

    to_process = []
    for c in companies:
        if c["company"].lower().strip() in existing_names:
            log_bug("duplicate", c["company"], "already in career_urls_result.json — skipping")
            continue
        to_process.append({
            "company": c["company"],
            "segment": c["segment"],
            "candidates": build_candidates(c["homepage"]),
        })

    print(f"After dedup: {len(to_process)} new companies to process")

    # Process in batches of 20
    results = []
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)
    async with httpx.AsyncClient(limits=limits, timeout=8) as client:
        BATCH = 20
        for i in range(0, len(to_process), BATCH):
            batch = to_process[i:i+BATCH]
            tasks = [process_company(client, e) for e in batch]
            batch_res = await asyncio.gather(*tasks, return_exceptions=True)

            for entry, res in zip(batch, batch_res):
                if isinstance(res, Exception):
                    log_bug("process_company", entry["company"], f"exception: {str(res)[:120]}")
                    res = {
                        "company": entry["company"],
                        "segment": entry["segment"],
                        "career_url": entry["candidates"][0] if entry["candidates"] else "",
                        "http_status": 0,
                        "portal_type": "URL_Not_Verified",
                        "source_candidate": entry["candidates"][0] if entry["candidates"] else "",
                    }
                if res["portal_type"] == "URL_Not_Verified":
                    log_bug("discovery", res["company"], f"no candidate reached 200/30x/403")
                results.append(res)
                status = res["http_status"]
                ind = "✓" if status == 200 else f"~{status}" if status else "✗"
                print(f"  [{len(results):3d}/{len(to_process)}] {ind} {res['company'][:35]:35s} → {res['portal_type']}")

    # Append to career_urls_result.json
    combined = existing + results
    OUTPUT_FILE.write_text(json.dumps(combined, indent=2, ensure_ascii=False))
    print(f"\n✓ Appended {len(results)} → {OUTPUT_FILE} (total: {len(combined)})")

    # Portal type distribution
    types = Counter(r["portal_type"] for r in results)
    print("\n=== Portal type distribution (new 300) ===")
    for t, c in types.most_common():
        print(f"  {c:3d}  {t}")

    # Write bug log
    if bug_log:
        BUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        BUG_LOG.write_text(
            "# Next 300 — Bug Log\n\n"
            + "\n".join(bug_log)
            + "\n"
        )
        print(f"\n⚠ Bug log → {BUG_LOG} ({len(bug_log)} issues)")


if __name__ == "__main__":
    asyncio.run(run())
