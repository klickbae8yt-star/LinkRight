# Career Intelligence & Job Search System

## 6-Stage Pipeline Architecture

| Stage | Directory | Purpose |
|---|---|---|
| **1** | [`01_company_discovery/`](01_company_discovery/) | Discover high-signal funded companies (`YC`, `Peak XV Surge`, `HN`, `TechCrunch`, `Inc42`), detect ATS portals, enrich founders (Exa + optional `linkedin_burner`), and promote `>=55` to `companies/watchlist.json`. |
| **2** | [`02_job_search/`](02_job_search/) | Monitor watchlisted companies across **Track 1** (LinkedIn human hiring posts), **Track 2** (direct `/careers` & ATS APIs: Ashby, Greenhouse, Lever, Google DS1, custom HAR portals), and **Track 3** (aggregators). |
| **3** | [`03_job_enrichment/`](03_job_enrichment/) | Filter by Remote India/Global/Dubai/UK (reject US/Canada-only & Java/C++/SWE coding roles), score JD-to-resume fit via **BM25 + Semantic Vector + RRF (`k=60`)**, and tag 6 phrase-level intent categories. |
| **4** | [`04_outreach/`](04_outreach/) | Cold outreach & founder/hiring-manager networking campaigns for unlisted roles at top-scoring companies. |
| **5** | [`05_resume_portfolio/`](05_resume_portfolio/) | Master resume pack (`Satvik_Resume_v7/`), YouTube SPM signals reference PDF, `agentic_builder_addendum.md`, and archived originals (`archives/`). |
| **6** | [`06_application_tracking/`](06_application_tracking/) | Application ledger and future **Simplify Copilot** Chrome extension reverse-engineering (`simplify_copilot/`). |

## Shared Infrastructure & Specs
- [`_shared/dashboard/server.py`](_shared/dashboard/server.py) — Localhost Auth, Cookie Vault & Workflow Health Dashboard (`http://127.0.0.1:8765`) with CDP login capture.
- [`_shared/scripts/`](_shared/scripts/) — `har_to_api.py`, `build_workflow.py`, `run_portals.py`, and `auth/` (`vault.py`, `cdp_capture.py`).
- [`_secrets/`](_secrets/) — Gitignored AES-256-CBC encrypted credentials, cookies, Chrome profiles, and `registry.json`.
- [`vendor/`](vendor/) — Local references: `api-anything`, `rea`, and `agent-reach`.
- [`N8N_CLOUD_BUILDER_SPEC.md`](N8N_CLOUD_BUILDER_SPEC.md) — Modular 4-workflow + 4-Data-Table spec for Cloud n8n Builder.
