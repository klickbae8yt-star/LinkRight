import os
#!/usr/bin/env python3
"""Delete duplicate job_discoveries rows using per-URL index-backed deletes."""
import psycopg2
import time

CONN_STR = dict(l.strip().split("=", 1) for l in open(os.path.expanduser("~/Desktop/Secrets/linkright/job_automation.env")) if "=" in l and not l.startswith("#"))["JOBS_DB_URL"]


def main():
    conn = psycopg2.connect(CONN_STR)
    conn.autocommit = True
    cur = conn.cursor()

    print("Fetching distinct job_urls ...", flush=True)
    t0 = time.time()
    cur.execute("""
        SELECT DISTINCT job_url
        FROM job_discoveries
        WHERE user_id IS NULL
        ORDER BY job_url
    """)
    urls = [r[0] for r in cur.fetchall()]
    print(f"Got {len(urls)} distinct URLs in {time.time()-t0:.1f}s", flush=True)

    deleted_total = 0
    errors = 0
    t_start = time.time()

    for i, url in enumerate(urls):
        try:
            cur.execute("""
                DELETE FROM job_discoveries
                WHERE user_id IS NULL AND job_url = %s
                AND id != (
                    SELECT id FROM job_discoveries
                    WHERE user_id IS NULL AND job_url = %s
                    ORDER BY (jd_text IS NOT NULL) DESC,
                             discovered_at DESC NULLS LAST
                    LIMIT 1
                )
            """, (url, url))
            deleted_total += cur.rowcount
        except Exception as e:
            errors += 1
            print(f"  ERROR on url {url}: {e}", flush=True)

        if (i + 1) % 200 == 0:
            elapsed = time.time() - t_start
            rate = deleted_total / elapsed if elapsed > 0 else 0
            print(f"[{i+1}/{len(urls)}] deleted {deleted_total} rows total | {rate:.0f} rows/s", flush=True)

    elapsed = time.time() - t_start
    print(f"\nDone in {elapsed:.1f}s. Total deleted: {deleted_total}  Errors: {errors}", flush=True)

    # Verify
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT job_url) FROM job_discoveries WHERE user_id IS NULL")
    total, unique = cur.fetchone()
    print(f"Remaining: {total} rows | {unique} unique job_urls", flush=True)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
