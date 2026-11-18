import os
#!/usr/bin/env python3
"""
Fast dedup via truncate+reinsert:
1. Fetch keeper row per job_url using index (3141 rows, ~30s)
2. TRUNCATE job_discoveries CASCADE (instant)
3. Re-insert keepers (instant)
"""
import psycopg2
import psycopg2.extras
import time

CONN_STR = dict(l.strip().split("=", 1) for l in open(os.path.expanduser("~/Desktop/Secrets/linkright/job_automation.env")) if "=" in l and not l.startswith("#"))["JOBS_DB_URL"]

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


def main():
    conn = psycopg2.connect(CONN_STR)
    conn.autocommit = True
    cur = conn.cursor()

    # Step 1: get distinct URLs (~9s, seq scan)
    print("Step 1: fetching distinct job_urls ...", flush=True)
    t0 = time.time()
    cur.execute("SELECT DISTINCT job_url FROM job_discoveries WHERE user_id IS NULL ORDER BY job_url")
    urls = [r[0] for r in cur.fetchall()]
    print(f"  {len(urls)} URLs in {time.time()-t0:.1f}s", flush=True)

    # Step 2: fetch keeper row per URL using index (user_id IS NULL, job_url = X)
    print("Step 2: fetching keeper rows via index ...", flush=True)
    t0 = time.time()
    keepers = []
    for i, url in enumerate(urls):
        cur.execute(f"""
            SELECT {COL_LIST}
            FROM job_discoveries
            WHERE user_id IS NULL AND job_url = %s
            ORDER BY (jd_text IS NOT NULL) DESC,
                     discovered_at DESC NULLS LAST
            LIMIT 1
        """, (url,))
        row = cur.fetchone()
        if row:
            keepers.append(row)
        if (i + 1) % 500 == 0:
            print(f"  [{i+1}/{len(urls)}] fetched {len(keepers)} keepers so far ...", flush=True)

    print(f"  {len(keepers)} keepers fetched in {time.time()-t0:.1f}s", flush=True)

    # Step 3: verify before truncate
    cur.execute("SELECT COUNT(*) FROM job_discoveries")
    total_before = cur.fetchone()[0]
    print(f"\nStep 3: Verifying — rows before truncate: {total_before}", flush=True)
    print(f"  Will re-insert: {len(keepers)} rows", flush=True)
    print(f"  Will free: {total_before - len(keepers)} rows", flush=True)

    # Step 4: TRUNCATE (instant)
    print("\nStep 4: TRUNCATE job_discoveries CASCADE ...", flush=True)
    t0 = time.time()
    cur.execute("TRUNCATE TABLE job_discoveries CASCADE")
    print(f"  Truncated in {time.time()-t0:.1f}s", flush=True)

    # Step 5: re-insert keepers
    print(f"\nStep 5: Re-inserting {len(keepers)} keeper rows ...", flush=True)
    t0 = time.time()
    insert_sql = f"INSERT INTO job_discoveries ({COL_LIST}) VALUES ({PLACEHOLDER})"
    psycopg2.extras.execute_batch(cur, insert_sql, keepers, page_size=500)
    print(f"  Inserted in {time.time()-t0:.1f}s", flush=True)

    # Verify
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT job_url) FROM job_discoveries")
    total, unique = cur.fetchone()
    print(f"\nFinal: {total} rows | {unique} unique job_urls")
    print("Done.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
