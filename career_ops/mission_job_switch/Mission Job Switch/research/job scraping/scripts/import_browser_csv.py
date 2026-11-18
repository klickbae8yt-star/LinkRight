"""
import_browser_csv.py — Import CSV from browser job_scraper.js into jobs.db

Usage:
  python3 scripts/import_browser_csv.py <csv_file> [<csv_file2> ...]

Examples:
  python3 scripts/import_browser_csv.py ~/Downloads/jobs_LinkedIn_2026-05-21.csv
  python3 scripts/import_browser_csv.py ~/Downloads/*.csv

What it does:
  1. Reads the CSV downloaded by job_scraper.js
  2. Normalises column names (handles slight variations)
  3. Skips duplicates already in jobs.db (matched by title+company)
  4. Inserts new jobs with source='browser_scrape' and the portal name
  5. Prints a summary: new / skipped / total
"""

import csv
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE    = Path(__file__).parent.parent
DB_PATH = BASE / "db" / "jobs.db"

# Column aliases: various scraper output names → canonical names
COL_MAP = {
    'job title':      'title',
    'job_title':      'title',
    'jobtitle':       'title',
    'position':       'title',
    'role':           'title',
    'company name':   'company',
    'company_name':   'company',
    'companyname':    'company',
    'employer':       'company',
    'job location':   'location',
    'job_location':   'location',
    'city':           'location',
    'link':           'url',
    'job_url':        'url',
    'apply_url':      'url',
    'href':           'url',
    'posted_date':    'date_posted',
    'date posted':    'date_posted',
    'posted':         'date_posted',
    'portal':         'source_portal',
    'source':         'source_portal',
    'scraped_from':   'scraped_url',
    'scraped_url':    'scraped_url',
}


def normalise_row(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        canonical = COL_MAP.get(k.lower().strip(), k.lower().strip())
        out[canonical] = v.strip() if isinstance(v, str) else v
    return out


def ensure_browser_columns(conn: sqlite3.Connection):
    """Add source columns to jobs table if not present."""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(jobs)")}
    for col, defn in [
        ('source_portal', 'TEXT'),
        ('scraped_url',   'TEXT'),
        ('company_id',    'INTEGER'),
    ]:
        if col not in cols:
            conn.execute(f"ALTER TABLE jobs ADD COLUMN {col} {defn}")
    conn.commit()


def import_csv(path: str, conn: sqlite3.Connection) -> tuple[int, int]:
    """Returns (inserted, skipped)."""
    inserted = skipped = 0

    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = [normalise_row(r) for r in reader]

    if not rows:
        print(f"  {path}: empty file")
        return 0, 0

    for row in rows:
        title   = row.get('title', '').strip()
        company = row.get('company', '').strip()
        loc     = row.get('location', '').strip()
        url     = row.get('url', '').strip()
        date    = row.get('date_posted', '').strip()
        portal  = row.get('source_portal', Path(path).stem).strip()
        scrape_url = row.get('scraped_url', '').strip()

        if not title:
            skipped += 1
            continue

        # Dedup: same title + company, or same URL already in DB
        exists = conn.execute(
            "SELECT 1 FROM jobs WHERE (lower(title)=lower(?) AND lower(company)=lower(?)) OR (job_url=? AND job_url!='')",
            (title, company, url)
        ).fetchone()

        if exists:
            skipped += 1
            continue

        # Find company_id if company exists in companies table
        comp_row = conn.execute(
            "SELECT id FROM companies WHERE lower(company)=lower(?)", (company,)
        ).fetchone()
        company_id = comp_row[0] if comp_row else None

        conn.execute("""
            INSERT INTO jobs (company_id, company, title, location, job_url,
                              source_portal, scraped_url, posted_at, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (company_id, company, title, loc, url,
              portal, scrape_url, date, datetime.now().isoformat()))
        inserted += 1

    conn.commit()
    return inserted, skipped


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    # Ensure jobs table has needed columns
    try:
        ensure_browser_columns(conn)
    except Exception as e:
        print(f"Schema check error: {e}")

    total_new = total_skip = 0

    for pattern in sys.argv[1:]:
        # Support glob patterns passed as strings
        paths = list(Path('.').glob(pattern)) or [Path(pattern)]
        for path in paths:
            if not path.exists():
                print(f"  NOT FOUND: {path}")
                continue
            ins, skip = import_csv(str(path), conn)
            total_new  += ins
            total_skip += skip
            print(f"  {path.name}: +{ins} new jobs, {skip} skipped (duplicate)")

    conn.close()

    print(f"\n{'='*40}")
    print(f"Total imported : {total_new}")
    print(f"Total skipped  : {total_skip} (already in DB)")
    print(f"DB location    : {DB_PATH}")

    if total_new > 0:
        print("\nNext: python3 scripts/update_excel.py  ← refresh Excel with new jobs")


if __name__ == '__main__':
    main()
