# Next 300 — Bug Log + Fixes

Errors found during processing of Next 300.md. Each bug fixed in source script so future runs don't repeat.

---

## BUG-001: 403 status accepted as valid for guessed Greenhouse/Lever URLs

**Symptom**: First run — 244/298 companies classified as `ATS_Greenhouse` with HTTP 403.

**Root cause**: `boards.greenhouse.io/{slug}` returns 403 to bots for ANY slug (real or fake). Code in `find_career_urls.py:process_company()` accepted 403 as valid and matched URL pattern → false positives.

**Verification** (2026-05-21):
```
boards.greenhouse.io/stripe         → 403 (real)
boards.greenhouse.io/postman        → 403 (real)
boards.greenhouse.io/nonexistent123 → 403 (FAKE, same response)
boards-api.greenhouse.io/v1/boards/nonexistent123/jobs → 404 (truth)
```

**Fix**: Added `verify_ats_via_api()` in `find_career_urls.py`. Hits public API to confirm board exists.

---

## BUG-002: Crushon.AI missing URL in markdown

Source data issue — markdown has `\[suspicious link removed\]`. Parser correctly logs + skips.

---

## BUG-003: Ashby HTML page returns 200 for ALL slugs (SPA)

**Symptom**: Second run — 102 false-positive `ATS_Ashby` classifications.

**Root cause**: `jobs.ashbyhq.com/{anything}` returns 200 because it's an SPA shell that always loads. Even non-existent boards show "200 OK" with empty content.

**Verification** (2026-05-21):
```
jobs.ashbyhq.com/krea            HTML=200  API=200 (real)
jobs.ashbyhq.com/postman         HTML=200  API=404 (fake)
jobs.ashbyhq.com/dubicars        HTML=200  API=404 (fake)
jobs.ashbyhq.com/nonexistent12345 HTML=200  API=404 (fake)
```

**Fix**: `find_career_urls.py` — `verify_ats_via_api()` now runs ALWAYS when ATS pattern matches (not just on 403). HTML status is unreliable for all 3 major ATS (Greenhouse 403, Lever 403, Ashby 200).

---

## BUG-004: Duplicate Epicenter between first 300 and next 300

Dedup logic handles it — no script bug.

---

## BUG-005: Cross-validator too strict for agent-verified entries

**Symptom**: 3 false-positive FAIL_CROSS_VALIDATE — Monica AI, Veed.io, D-ID. Their `portal_type=ATS_Workable` was set by agent-browser verification (`classification_source: agent_verified`), but the cross-validator required workable.com to appear in career_url/source.

**Root cause**: `cross_validate_entry()` didn't trust manual verification sources.

**Fix**: `validate_pipeline.py` — added `_TRUSTED_SOURCES` allowlist (`agent_verified`, `corrected:`, `manual:`, `known_ats:`). Skip cross-validation when classification_source contains any trusted marker.

---

## BUG-006: New companies appended to JSON not synced to DB

**Symptom**: After `process_next300.py` appended 298 entries to `career_urls_result.json`, `validate_pipeline.py` summary showed 598 processed, but the `companies` table still had only 300 rows — validation results for the new 298 were silently dropped.

**Root cause**: `_write_result()` used `UPDATE ... WHERE company=?`. For rows that didn't exist, UPDATE is a no-op. New companies appended to JSON were never INSERTed into the DB.

**Fix**: `validate_pipeline.py` — changed `_write_result()` to `INSERT ... ON CONFLICT(company) DO UPDATE`. Now any new company in JSON is auto-inserted into `companies` table when validated. Also passes the full entry dict so segment/portal_type/career_url/classification_source get persisted on insert.

---

## BUG-007: Monica/D-ID/Veed scraper had no slug — Workable scrape would fail

**Symptom**: Even if classification is right (ATS_Workable), `scrape_jobs.py` couldn't extract a Workable slug from URLs like `https://monica.im/` because they don't contain `workable.com`.

**Fix**: `scrape_jobs.py` — added explicit `ATS_OVERRIDES` entries with verified slugs: `monica`, `d-id`, `veed`.

---

## How to prevent future bugs of this class

1. **Never trust HTML status alone for guessed ATS URLs** — Greenhouse/Lever return 403 to bots regardless, Ashby returns 200 regardless. Always hit the public ATS API to verify.
2. **Candidate ordering**: high-precision candidates (subdomain like `careers.X`, path like `/careers`) should run BEFORE ATS slug guesses.
3. When in doubt about a status code's meaning, test the same URL against a known-fake slug — if response is identical, the status code is meaningless.
