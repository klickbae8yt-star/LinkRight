# Supabase Database Issue Report
**Date:** 2026-05-24  
**Table:** `public.job_discoveries`  
**Project:** `ahjapzyslbhyjekswqpt`

---

## TL;DR

The `job_discoveries` table has a critical deduplication bug. Out of **678,085 total rows**, only **3,141 are unique jobs**. The remaining **674,944 rows (99.5%) are duplicates**. The database is 3.94 GB in size for what is effectively ~3k jobs. The scraper re-inserts the same jobs every run because the unique constraint silently fails when `user_id` is `NULL`.

---

## Database Size Breakdown

| Component | Size |
|---|---|
| Table heap (row data) | 207 MB |
| TOAST (`jd_text` column) | 3,647 MB |
| Indexes | 99 MB |
| **Total** | **3,998 MB (~4 GB)** |

The `jd_text` column (full job description text) stored in TOAST accounts for **91% of DB size**. Every duplicate row carries its own copy of the JD text.

---

## Duplication Stats

| Metric | Value |
|---|---|
| Total rows | 678,085 |
| Unique job URLs | 3,141 |
| Duplicate rows | **674,944 (99.5%)** |
| Rows with `user_id = NULL` | 678,085 (100%) |
| Rows with `jd_text` populated | 663,848 |
| Rows marked `liveness_status = active` | 678,085 (100%) |

**Every single row has `user_id = NULL`.** These are "global" (non-user-specific) jobs.

**Worst offenders (most copies of same job):**

| Job URL | Copies |
|---|---|
| stripe.com/jobs/search?gh_jid=7118945 | 695 |
| ashbyhq.com/linear/d3bc1ced-... | 686 |
| ashbyhq.com/linear/453f1ba0-... | 676 |
| greenhouse.io/phonepe/jobs/7711699003 | 659 |

---

## Root Cause

### The Bug: NULL defeats the unique constraint

The table has a unique constraint:
```sql
UNIQUE INDEX job_discoveries_user_id_job_url_key ON (user_id, job_url)
```

**In PostgreSQL, `NULL != NULL` for unique index purposes.** This means:

```
(NULL, "https://stripe.com/jobs/...") — row 1 ✓
(NULL, "https://stripe.com/jobs/...") — row 2 ✓  ← should be rejected, isn't
(NULL, "https://stripe.com/jobs/...") — row 3 ✓  ← same
... 695 times
```

The constraint intended to prevent duplicate `(user, job_url)` pairs, but since all global jobs have `user_id = NULL`, the constraint never fires. Every scraper run inserts all jobs as fresh rows.

### Data Sources

| Source | Total rows | Ingestion rate |
|---|---|---|
| `ats` (ATS scrapers: Greenhouse, Lever, Ashby) | 663,148 | ~60–70k/day |
| `api_themuse` | 14,863 | ~1,500/day |
| `api_jobicy` | 48 | ~50/day |
| `api_remotive` | 26 | ~26/day |

The ATS scraper runs daily, hits Greenhouse/Lever/Ashby APIs for configured companies, and blindly inserts all results. Because dedup fails, the same ~3k jobs accumulate ~200 new copies every day per job.

### Daily Growth (last 7 days)

| Date | New rows inserted |
|---|---|
| 2026-05-23 | 63,626 |
| 2026-05-22 | 64,584 |
| 2026-05-21 | 66,699 |
| 2026-05-20 | 68,157 |
| 2026-05-19 | 72,486 |
| 2026-05-18 | 54,563 |
| 2026-05-17 | 61,860 |

At this rate: **~65k rows/day → ~2 GB additional TOAST/month**.

---

## Impact

1. **Storage cost** — 4 GB for 3,141 unique jobs. Should be ~30 MB.
2. **Egress cost** — Any query on this table without strict dedup filtering pulls hundreds of copies of each job. If the app does `SELECT * WHERE liveness_status='active'`, it returns 678k rows instead of 3k.
3. **Query performance** — Every COUNT, GROUP BY, or search scans 678k rows.
4. **JD enrichment waste** — `jd_text` is fetched and stored 695× per job, meaning the LLM enrichment pipeline may be running on duplicates too (check `llm_cache_jd_enrichment`).

---

## Fix (in order of priority)

### Fix 1 — Stop new duplicates immediately (1 line, no data loss)

Add a partial unique index for global jobs (`user_id IS NULL`):

```sql
CREATE UNIQUE INDEX CONCURRENTLY idx_job_discoveries_global_url_dedup
ON job_discoveries (job_url)
WHERE user_id IS NULL;
```

`CONCURRENTLY` = no table lock, runs in background. After this, any insert of a duplicate `job_url` with `user_id = NULL` will be rejected with a conflict error. The scraper should use `INSERT ... ON CONFLICT DO NOTHING` or `ON CONFLICT DO UPDATE` (upsert).

**Warning:** This index creation will fail if duplicate `job_url` rows already exist (they do). Must clean duplicates first (Fix 2), then create this index.

### Fix 2 — Delete duplicate rows (keeps 1 copy per job_url)

```sql
-- Keep the row with the most complete data (has jd_text, latest discovered_at)
DELETE FROM job_discoveries
WHERE id NOT IN (
  SELECT DISTINCT ON (job_url) id
  FROM job_discoveries
  WHERE user_id IS NULL
  ORDER BY job_url, (jd_text IS NOT NULL) DESC, discovered_at DESC
);
```

**After deletion: ~3,141 rows remain from 678,085. Frees ~3.9 GB.**

Then run:
```sql
VACUUM FULL job_discoveries;
```

### Fix 3 — Update scraper to upsert, not insert

Change the scraper's insert logic from:
```sql
INSERT INTO job_discoveries (...) VALUES (...)
```
to:
```sql
INSERT INTO job_discoveries (...) VALUES (...)
ON CONFLICT (job_url) WHERE user_id IS NULL
DO UPDATE SET
  liveness_status = EXCLUDED.liveness_status,
  liveness_checked_at = EXCLUDED.liveness_checked_at,
  -- update only non-null fields
  jd_text = COALESCE(job_discoveries.jd_text, EXCLUDED.jd_text)
```

### Fix 4 — Separate `jd_text` into its own table (optional, long-term)

```sql
CREATE TABLE job_jd (
  job_id UUID PRIMARY KEY REFERENCES job_discoveries(id) ON DELETE CASCADE,
  jd_text TEXT NOT NULL
);

INSERT INTO job_jd (job_id, jd_text)
SELECT id, jd_text FROM job_discoveries WHERE jd_text IS NOT NULL;

ALTER TABLE job_discoveries DROP COLUMN jd_text;
VACUUM FULL job_discoveries;
```

**Benefit:** Any query that doesn't need JD text (listing, filtering, scoring metadata) won't pull 3.6 GB of TOAST. JD text only fetched on explicit JOIN.

---

## Recommended Action Order

1. **Immediately:** Run Fix 2 (delete duplicates) → then Fix 1 (unique index) → then Fix 3 (scraper upsert). This stops the bleeding and clears 3.9 GB.
2. **Later:** Fix 4 (jd_text separation) if egress from JD text remains high after Fix 2.

---

## Queries for Verification

```sql
-- Check current duplicate count
SELECT COUNT(*) as total, COUNT(DISTINCT job_url) as unique_jobs
FROM job_discoveries;

-- Check if new index exists after Fix 1
SELECT indexname FROM pg_indexes
WHERE tablename = 'job_discoveries' AND indexname LIKE '%dedup%';

-- Post-cleanup size check
SELECT pg_size_pretty(pg_total_relation_size('job_discoveries'));
```
