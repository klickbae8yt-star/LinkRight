# Step 6: Job Application & Tracking (`06_application_tracking/`)

## Purpose
Automate, log, and track every job application submitted from matched opportunities (`03_job_enrichment/`) using tailored resumes (`05_resume_portfolio/`), plus integrate with **Simplify Copilot**'s backend/tracking APIs.

---

## Folder Map
- `simplify_copilot/` — Reverse-engineering workspace for the **Simplify Copilot** Google Chrome extension:
  - `captures/` — Drop Simplify Copilot HAR captures, extension network logs, or unpacked `.crx` manifests/service-worker notes here.
  - *(Future)* `simplify_api.py` & `simplify.api-anything.json` — Plain-HTTP API wrapper for syncing saved jobs, application statuses, autofill profile payloads, and custom Q&A memory.
- `applications/` — Local application ledger (`applications.json` / `applications.md`) linking each submitted role to:
  - Company score & watchlist entry (`01_company_discovery/`)
  - Source track (`Track 1` LinkedIn post / `Track 2` Company portal / `Track 3` Aggregator)
  - Tailored resume PDF & matched bullet IDs (`05_resume_portfolio/`)
  - Application status (`saved`, `applied`, `referred`, `outreach_sent`, `interview`, `offer`, `rejected`, `ghosted`)

---

## Planned Simplify Copilot Reverse-Engineering Workflow
1. Capture a Chrome DevTools HAR while using Simplify Copilot (autofill + job tracker save + status update) and drop it into `06_application_tracking/simplify_copilot/captures/`.
2. Run `_shared/scripts/har_to_api.py` (and inspect `vendor/api-anything` / `vendor/rea` patterns) to extract Simplify's REST/GraphQL endpoints and auth token lifecycle.
3. Register Simplify's auth session in `_secrets/registry.json` (`_shared/dashboard/server.py`) so token expiry is monitored alongside LinkedIn and job portals.
4. Connect `03_job_enrichment/matched_jobs/` → `06_application_tracking/applications/` → Simplify Tracker + n8n Cloud (`N8N_CLOUD_BUILDER_SPEC.md`).

