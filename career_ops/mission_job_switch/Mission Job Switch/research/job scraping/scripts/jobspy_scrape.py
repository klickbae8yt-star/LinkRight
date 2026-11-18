"""
jobspy_scrape.py — Scrape LinkedIn, Indeed India, Google Jobs, Naukri via JobSpy.

Usage (direct):
  python3 scripts/jobspy_scrape.py
  python3 scripts/jobspy_scrape.py --search-terms "ai product manager,founding pm" --sectors "CONSUMER_AI,GAMING"
  python3 scripts/jobspy_scrape.py --hours-old 168 --remote

Usage (via skill — Claude constructs args from natural language):
  /job-scrape I want founding PM roles at consumer AI startups, Series A/B, remote preferred

CLI args:
  --search-terms   Comma-separated job title keywords to search
                   Default: full PM-adjacent list
  --sectors        Comma-separated B2C sector filter for tagging
                   Values: CONSUMER_AI | CAREER_NAV_B2C | GAMING | SOCIAL_COMMERCE | ALL
                   Default: ALL
  --location       Job location string  (default: India)
  --remote         Flag — filter for remote roles only
  --hours-old      Freshness window in hours  (default: 72, first run use 168)
  --results        Max results per search term per site  (default: 25)
  --dry-run        Print what would run, no DB writes
"""

import argparse
import csv
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE    = Path(__file__).parent.parent
DB_PATH = BASE / "db" / "jobs.db"

# ─── DEFAULT SEARCH TERMS ──────────────────────────────────────────────────────
DEFAULT_SEARCH_TERMS = [
    "product manager",
    "senior product manager",
    "ai product manager",
    "growth manager",
    "growth product manager",
    "product marketing manager",
    "customer success manager",
    "implementation manager",
    "solutions architect",
    "technical program manager",
    "founding product manager",
    "product analyst",
    "data product manager",
    "chief of staff",
    "product owner",
]

# ─── SECTOR COMPANY LISTS ──────────────────────────────────────────────────────
SECTOR_COMPANIES: dict[str, list[str]] = {
    "CAREER_NAV_B2C": [
        "linkedin", "glassdoor", "handshake", "unstop", "internshala",
        "apna", "foundit", "topmate", "superpeer", "cutshort", "hirist",
        "rezi", "kickresume", "enhancv", "pramp", "exponent", "naukri",
        "indeed", "wellfound", "angel", "instahyre",
    ],
    "CONSUMER_AI": [
        "perplexity", "character.ai", "character ai", "notion",
        "superhuman", "motion", "reclaim", "otter",
        "sarvam", "krutrim", "setu", "frammer", "leher",
        "sharechat", "moj", "josh", "locket",
        "openai", "anthropic", "cohere", "mistral", "inflection",
        "runway", "midjourney", "stability", "elevenlabs",
    ],
    "SOCIAL_COMMERCE": [
        "meesho", "glowroad", "shop101", "whatnot", "temu",
        "tiktok", "pinterest", "instagram", "snapchat",
    ],
    "GAMING": [
        "dream11", "mpl", "mobile premier league", "nazara", "winzo",
        "games24x7", "gameskraft", "krafton", "ncore", "supergaming",
        "junglee games", "playtika", "zynga", "electronic arts",
        "riot games", "riot", "scopely", "unity", "epic games",
        "activision", "ubisoft", "niantic", "jam city", "a23",
        "fantasy akhada", "fanatics",
    ],
}


def detect_sector(company: str) -> str | None:
    c = (company or "").lower()
    for sector, names in SECTOR_COMPANIES.items():
        if any(name in c for name in names):
            return sector
    return None


# ─── INCLUDE / EXCLUDE (reuse filter_pm_jobs logic inline) ────────────────────
INCLUDE_PATTERNS = re.compile(
    r"\b(product manager|product management|product owner|product lead|"
    r"head of product|vp product|vp of product|director of product|"
    r"chief product|principal product|staff product|group product|"
    r"associate product|senior product manager|"
    r"ai product|ai builder|ai applications|ai solutions|llm product|"
    r"generative ai|machine learning product|ml product|applied ai|"
    r"ai agent|agentic|ai platform|"
    r"growth product|product growth|growth manager|growth lead|"
    r"head of growth|growth marketing|growth pm|growth hacker|"
    r"product marketing|pmm|go.to.market|gtm manager|"
    r"product analyst|data product|analytics product|product insights|"
    r"customer success|client success|customer experience manager|"
    r"implementation lead|implementation manager|implementation consultant|"
    r"solutions architect|technical solutions|solutions consultant|"
    r"technical account manager|onboarding manager|launch manager|"
    r"compliance product|risk product|fintech product|payments product|"
    r"aml product|fraud product|banking product|"
    r"founding pm|founding product|chief of staff|"
    r"technical program manager|program manager|delivery manager|"
    r"product specialist|product strategist|product operations|"
    r"product ops|product consultant|product head)\b",
    re.IGNORECASE,
)

EXCLUDE_PATTERNS = re.compile(
    r"\b(software engineer|sde\b|swe\b|backend engineer|frontend engineer|"
    r"full.?stack engineer|software developer|mobile engineer|"
    r"data scientist|ml engineer|machine learning engineer|data engineer|"
    r"ai engineer|ux designer|ui designer|graphic designer|"
    r"account executive|sales executive|sales development|sdr\b|bdr\b|"
    r"recruiter|talent acquisition|hr manager|hr business partner|"
    r"accountant|controller|financial analyst|cfo\b|finance manager|"
    r"content writer|copywriter|devops engineer|sre\b|site reliability|"
    r"infrastructure engineer|qa engineer|test engineer|"
    r"intern\b|trainee|fresher|apprentice)\b",
    re.IGNORECASE,
)


def classify_title(title: str) -> str | None:
    t = (title or "").lower()
    if EXCLUDE_PATTERNS.search(t):
        return None
    if INCLUDE_PATTERNS.search(t):
        return "KEEP"
    return "UNCERTAIN"


# ─── DB ────────────────────────────────────────────────────────────────────────
def ensure_schema(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT, segment TEXT, portal_type TEXT,
            title TEXT, department TEXT, location TEXT,
            job_url TEXT, posted_at TEXT, scraped_at TEXT,
            job_description TEXT, compensation TEXT,
            years_experience TEXT, employment_type TEXT,
            is_remote INTEGER DEFAULT 0,
            role_category TEXT, sector TEXT,
            relevance_score REAL, is_ghost INTEGER DEFAULT 0,
            source_portal TEXT, company_id INTEGER
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_url ON jobs(job_url)")
    conn.commit()


def url_exists(conn: sqlite3.Connection, url: str) -> bool:
    if not url:
        return False
    return bool(conn.execute(
        "SELECT 1 FROM jobs WHERE job_url=?", (url,)
    ).fetchone())


def title_company_exists(conn: sqlite3.Connection, title: str, company: str) -> bool:
    return bool(conn.execute(
        "SELECT 1 FROM jobs WHERE lower(title)=lower(?) AND lower(company)=lower(?)",
        (title, company)
    ).fetchone())


def insert_job(conn: sqlite3.Connection, row: dict) -> bool:
    """Returns True if inserted, False if duplicate."""
    url     = (row.get("job_url") or "").strip()
    title   = (row.get("title") or "").strip()
    company = (row.get("company") or "").strip()

    if url and url_exists(conn, url):
        return False
    if title and company and title_company_exists(conn, title, company):
        return False

    conn.execute("""
        INSERT INTO jobs (company, title, location, job_url, posted_at,
            scraped_at, job_description, is_remote, role_category,
            sector, source_portal, employment_type)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        company,
        title,
        str(row.get("location") or ""),
        url,
        str(row.get("date_posted") or ""),
        datetime.now().isoformat(),
        str(row.get("description") or "")[:8000],
        1 if row.get("is_remote") else 0,
        row.get("role_category"),
        row.get("sector"),
        str(row.get("site") or "jobspy"),
        str(row.get("job_type") or ""),
    ))
    return True


# ─── ARGS ─────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="JobSpy multi-board scraper for PM roles")
    p.add_argument(
        "--search-terms", default="",
        help="Comma-separated search terms. Empty = use default list."
    )
    p.add_argument(
        "--sectors", default="ALL",
        help="Comma-separated sector filter for tagging. ALL = tag all known sectors."
    )
    p.add_argument("--location", default="India")
    p.add_argument("--remote", action="store_true", help="Remote roles only")
    p.add_argument(
        "--hours-old", type=int, default=72,
        help="Only return jobs posted within this many hours (default 72; use 168 for first run)"
    )
    p.add_argument(
        "--results", type=int, default=25,
        help="Max results per search term per site (default 25)"
    )
    p.add_argument("--dry-run", action="store_true", help="Print config, skip scraping")
    return p.parse_args()


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    args = parse_args()

    search_terms = (
        [t.strip() for t in args.search_terms.split(",") if t.strip()]
        if args.search_terms
        else DEFAULT_SEARCH_TERMS
    )

    active_sectors = (
        None  # None = tag all known sectors
        if args.sectors.upper() == "ALL"
        else {s.strip().upper() for s in args.sectors.split(",") if s.strip()}
    )

    print(f"JobSpy scraper")
    print(f"  Search terms  : {search_terms}")
    print(f"  Location      : {args.location}")
    print(f"  Remote only   : {args.remote}")
    print(f"  Hours old     : {args.hours_old}")
    print(f"  Results/term  : {args.results} per site")
    print(f"  Sectors       : {args.sectors}")
    print(f"  DB            : {DB_PATH}")

    if args.dry_run:
        print("\n[DRY RUN] No scraping performed.")
        return

    try:
        from jobspy import scrape_jobs
    except ImportError:
        print("\nERROR: jobspy not installed. Run: pip install python-jobspy")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    ensure_schema(conn)

    total_inserted = total_skipped = total_excluded = 0
    errors = []

    for term in search_terms:
        print(f"\n  Searching: '{term}'")
        try:
            df = scrape_jobs(
                site_name=["indeed", "linkedin", "google", "naukri"],
                search_term=term,
                google_search_term=f"{term} jobs {args.location}",
                location=args.location,
                country_indeed="India",
                results_wanted=args.results,
                hours_old=args.hours_old,
                is_remote=args.remote if args.remote else None,
                description_format="markdown",
                linkedin_fetch_description=False,  # True = much slower, enable if needed
                verbose=0,
            )
            print(f"    Raw results: {len(df)}")
        except Exception as e:
            msg = str(e)[:120]
            print(f"    ERROR: {msg}")
            errors.append(f"'{term}': {msg}")
            continue

        inserted = skipped = excluded = 0
        for _, row in df.iterrows():
            title   = str(row.get("title") or "")
            company = str(row.get("company") or "")
            site    = str(row.get("site") or "")

            verdict = classify_title(title)
            if verdict is None:
                excluded += 1
                continue

            sector = detect_sector(company)
            if active_sectors is not None and sector not in active_sectors:
                # If user specified sectors, still insert but only if sector matches
                # — unless no sector detected (new/unknown company, keep anyway)
                if sector is not None:
                    excluded += 1
                    continue

            job_row = {
                "title":       title,
                "company":     company,
                "location":    str(row.get("location") or ""),
                "job_url":     str(row.get("job_url") or ""),
                "date_posted": str(row.get("date_posted") or ""),
                "description": str(row.get("description") or ""),
                "is_remote":   bool(row.get("is_remote")),
                "job_type":    str(row.get("job_type") or ""),
                "site":        f"jobspy_{site}",
                "role_category": verdict,
                "sector":      sector,
            }

            if insert_job(conn, job_row):
                inserted += 1
            else:
                skipped += 1

        conn.commit()
        print(f"    Inserted: {inserted}  |  Skipped (dup): {skipped}  |  Excluded (irrelevant): {excluded}")
        total_inserted += inserted
        total_skipped  += skipped
        total_excluded += excluded

    conn.close()

    print(f"\n{'='*55}")
    print(f"Total inserted : {total_inserted}")
    print(f"Total skipped  : {total_skipped}  (already in DB)")
    print(f"Total excluded : {total_excluded}  (title filter)")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
    print(f"\nNext: python3 scripts/score_jobs.py")


if __name__ == "__main__":
    main()
