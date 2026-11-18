#!/usr/bin/env python3
"""
Safe dedup:
1. Fetch keeper row per job_url → export to CSV backup
2. TRUNCATE job_discoveries CASCADE
3. Re-insert from backup
"""
import psycopg2
import psycopg2.extras
import csv
import time
import os

CONN_STR = dict(l.strip().split("=", 1) for l in open(os.path.expanduser("~/Desktop/Secrets/linkright/job_automation.env")) if "=" in l and not l.startswith("#"))["JOBS_DB_URL"]
BACKUP_CSV = "/Users/satvikjain/Downloads/Job automate/data/job_discoveries_keepers_backup.csv"

COLS = [
    'id', 'user_id', 'watchlist_id', 'external_job_id', 'title', 'company_name',
    'location', 'job_url', 'description_snippet', 'auto_score_grade',
    'liveness_status', 'status', 'discovered_at', 'liveness_checked_at',
    'company_slug', 'jd_text', 'apply_url', 'remote_ok', 'work_type',
    'employment_type', 'experience_level', 'department', 'salary_min',
    'salary_max', 'salary_currency', 'skills_required', 'company_stage',
    'reporting_to', 'industry', 'posted_date', 'source_type', 'enriched_at',
    'enrichment_status', 'min_years_experience'
]

COL_LIST = ', '.join(COLS)
PLACEHOLDER = ', '.join(['%s'] * len(COLS))

PHASE = os.environ.get('PHASE', 'backup')  # 'backup' or 'restore'


def do_backup(cur):
    # Single DISTINCT ON query — one roundtrip, no per-URL loops, ~30s
    print("Fetching 3141 keeper rows via single DISTINCT ON query ...", flush=True)
    t0 = time.time()
    cur.execute(f"""
        SELECT DISTINCT ON (job_url) {COL_LIST}
        FROM job_discoveries
        WHERE user_id IS NULL
        ORDER BY job_url,
                 (jd_text IS NOT NULL) DESC,
                 discovered_at DESC NULLS LAST
    """)
    keepers = cur.fetchall()
    print(f"  {len(keepers)} keepers fetched in {time.time()-t0:.1f}s", flush=True)

    print(f"Writing backup CSV → {BACKUP_CSV}", flush=True)
    with open(BACKUP_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(COLS)
        writer.writerows(keepers)

    size_mb = os.path.getsize(BACKUP_CSV) / 1024 / 1024
    print(f"  Backup saved: {len(keepers)} rows, {size_mb:.1f} MB", flush=True)
    print(f"\nBackup complete. Verify CSV then run with PHASE=restore.", flush=True)
    return keepers


def do_restore(cur):
    if not os.path.exists(BACKUP_CSV):
        print(f"ERROR: backup not found at {BACKUP_CSV}")
        return

    print(f"Loading backup from {BACKUP_CSV} ...", flush=True)
    keepers = []
    with open(BACKUP_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            keepers.append(tuple(None if v == '' else v for v in row))
    print(f"  Loaded {len(keepers)} rows from backup", flush=True)

    cur.execute("SELECT COUNT(*) FROM job_discoveries")
    total_before = cur.fetchone()[0]
    print(f"  Rows before truncate: {total_before}", flush=True)
    print(f"  Will re-insert: {len(keepers)} rows", flush=True)

    print("TRUNCATE job_discoveries CASCADE ...", flush=True)
    t0 = time.time()
    cur.execute("TRUNCATE TABLE job_discoveries CASCADE")
    print(f"  Truncated in {time.time()-t0:.2f}s", flush=True)

    print(f"Re-inserting {len(keepers)} keeper rows ...", flush=True)
    t0 = time.time()
    insert_sql = f"INSERT INTO job_discoveries ({COL_LIST}) VALUES ({PLACEHOLDER})"
    psycopg2.extras.execute_batch(cur, insert_sql, keepers, page_size=500)
    print(f"  Inserted in {time.time()-t0:.1f}s", flush=True)

    cur.execute("SELECT COUNT(*), COUNT(DISTINCT job_url) FROM job_discoveries")
    total, unique = cur.fetchone()
    print(f"\nFinal: {total} rows | {unique} unique job_urls")
    print("Done.")


def main():
    conn = psycopg2.connect(CONN_STR)
    conn.autocommit = True
    cur = conn.cursor()

    if PHASE == 'backup':
        do_backup(cur)
    elif PHASE == 'restore':
        do_restore(cur)
    else:
        print(f"Unknown PHASE={PHASE}. Use 'backup' or 'restore'.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
