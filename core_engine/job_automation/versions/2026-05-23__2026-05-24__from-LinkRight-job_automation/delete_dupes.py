import os
#!/usr/bin/env python3
"""Delete duplicate job_discoveries rows, keeping best row per job_url per company_slug."""
import psycopg2
import time

CONN_STR = dict(l.strip().split("=", 1) for l in open(os.path.expanduser("~/Desktop/Secrets/linkright/job_automation.env")) if "=" in l and not l.startswith("#"))["JOBS_DB_URL"]
BATCH = 3000


def delete_dupes_for_slug(cur, slug):
    """Return (total_in_slug, kept, deleted)."""
    where = "company_slug = %s AND user_id IS NULL"
    params = (slug,)
    if slug is None:
        where = "company_slug IS NULL AND user_id IS NULL"
        params = ()

    # Fetch all IDs to KEEP (best row per job_url)
    cur.execute(f"""
        SELECT DISTINCT ON (job_url) id
        FROM job_discoveries
        WHERE {where}
        ORDER BY job_url,
                 (jd_text IS NOT NULL) DESC,
                 discovered_at DESC NULLS LAST
    """, params)
    keeper_ids = {r[0] for r in cur.fetchall()}

    # Fetch ALL IDs for this slug
    cur.execute(f"SELECT id FROM job_discoveries WHERE {where}", params)
    all_ids = [r[0] for r in cur.fetchall()]

    delete_ids = [i for i in all_ids if i not in keeper_ids]
    total = len(all_ids)
    kept = len(keeper_ids)
    deleted = 0

    # Batch delete by PK — very fast, well within 2min per batch
    for start in range(0, len(delete_ids), BATCH):
        chunk = delete_ids[start:start + BATCH]
        cur.execute("DELETE FROM job_discoveries WHERE id = ANY(%s::uuid[])", (chunk,))
        deleted += len(chunk)
        label = str(slug) if slug else "NULL"
        print(f"  [{label}] deleted {deleted}/{len(delete_ids)} so far...", flush=True)

    return total, kept, deleted


def main():
    conn = psycopg2.connect(CONN_STR)
    conn.autocommit = True
    cur = conn.cursor()

    # Get all distinct slugs (including NULL)
    cur.execute("""
        SELECT company_slug, COUNT(*) as cnt
        FROM job_discoveries
        WHERE user_id IS NULL
        GROUP BY company_slug
        ORDER BY cnt DESC
    """)
    slugs = [(r[0], r[1]) for r in cur.fetchall()]
    print(f"Processing {len(slugs)} distinct company_slugs\n")

    grand_deleted = 0
    for slug, cnt in slugs:
        label = str(slug) if slug else "NULL"
        print(f"[{label}] {cnt} rows ...", flush=True)
        t0 = time.time()
        total, kept, deleted = delete_dupes_for_slug(cur, slug)
        elapsed = time.time() - t0
        grand_deleted += deleted
        print(f"  -> kept {kept}, deleted {deleted} in {elapsed:.1f}s\n", flush=True)

    print(f"\nDone. Total deleted: {grand_deleted}")

    # Verify
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT job_url) FROM job_discoveries WHERE user_id IS NULL")
    total, unique = cur.fetchone()
    print(f"Remaining rows: {total} | Unique job_urls: {unique}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
