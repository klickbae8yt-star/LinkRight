# n8n Cloud Builder Specification
## Project: Company-First Career Intelligence & Job Signal Platform
**Target Runtime:** n8n Cloud (n8n v2.x `@n8n/task-runner` compatible)  
**Purpose:** Hand this specification directly to an n8n Cloud Builder / AI Workflow Builder plugin to generate the complete multi-workflow n8n Cloud setup.

---

## 1. Critical n8n v2.x Engineering Constraints (Mandatory)

Every generated Code node and workflow **must** obey these rules (learned from `RULES.md` and tested in `tests/test_framework.mjs`):

1. **Isolated `node:vm` Task Runner (`Code` nodes):**
   - **NEVER** use `URLSearchParams`, `URL`, `fetch`, `require(...)`, `import`, `process`, or `Buffer` inside Code nodes.
   - Use pure ECMAScript (`encodeURIComponent`, `JSON.parse`, `JSON.stringify`, regex, `try/catch`).
2. **Multi-Trigger Safety:**
   - Every workflow with both `Schedule Trigger` and `Execute Workflow Trigger` / `Manual Trigger` / `Webhook` **MUST** pass through a single `Config` (Set / Code) node immediately after all triggers.
   - Downstream nodes **MUST** read `$('Config').first().json` and **NEVER** reference a trigger node directly (`$('Schedule Trigger')` crashes when triggered manually or via webhook).
3. **Fault Isolation Per Portal / Per Company:**
   - All `HTTP Request` nodes inside loops **MUST** set `"onError": "continueRegularOutput"` (or `"continueErrorOutput"` routed to the Auth Health logger) and loop via `SplitInBatches` (`batchSize: 1`).
   - All parser `Code` nodes **MUST** wrap parsing in `try { ... } catch (err) { ... }` per item so one broken portal/company never stops the rest of the run.

---

## 2. Architecture Overview (4 Modular Workflows)

Build **4 separate workflows** connected via n8n Data Tables and `Execute Workflow` / `Webhook`:

```text
WF_01_Company_Discovery        (Daily Schedule)
   └── Finds funded/high-signal companies → Scores them → Upserts to `companies_watchlist`

WF_02_Job_Signal_Monitor       (Schedule: every 2–6 hours)
   ├── Track 1: LinkedIn Human Hiring Posts (cookie-authenticated)
   ├── Track 2: Direct Company Career Portals (Ashby / Greenhouse / Lever / Google DS1 / Custom APIs)
   └── Track 3: Aggregator Boards (Wellfound, Himalayas, RemoteOK, Cutshort — daily)
   └── Deduplicates against `jobs_seen` → Sends new jobs to WF_03; auth errors to WF_04

WF_03_Job_Enrichment_And_Alert (Sub-workflow triggered by WF_02)
   └── Applies Hard Filters + Role Priority + Industry Grade → Sends instant Slack/Telegram/Email Alert

WF_04_Cookie_Health_And_Sync   (Webhook + Daily Health Check)
   ├── Receives refreshed cookies from Localhost Auth Dashboard (`http://127.0.0.1:8765`)
   ├── Updates `portal_auth_vault` Data Table
   └── Marks expired cookies on 401/403 & alerts user with clickable localhost re-auth URL
```

---

## 3. n8n Data Tables Schema

Create these **4 Data Tables** in n8n Cloud:

### Table 1: `companies_watchlist` (Primary Key: `company_slug`)
| Column | Type | Notes |
|--------|------|-------|
| `company_slug` | string | Unique lowercase slug (e.g. `supabase`, `glean`) |
| `company_name` | string | Display name |
| `website` | string | Company homepage |
| `career_portal_url` | string | Direct `/careers` URL |
| `ats_platform` | string | `ashby` \| `greenhouse` \| `lever` \| `google_ds1` \| `custom` \| `none` |
| `ats_slug` | string | ATS board identifier |
| `company_score` | number | 0–100 normalized rubric score |
| `watchlist_tier` | string | `strong_match` (>=75) \| `consider` (55–74) \| `skip` (<55) |
| `funding_stage` | string | `Series A`, `Series B`, `YC`, etc. |
| `investors` | string | Comma-separated investor names |
| `industry` | string | e.g. `Hiring & Recruitment Tech`, `AI & Automation` |
| `industry_grade` | string | `A+`, `A`, `A-`, `B+`, `B`, `C` |
| `b2c_or_b2b` | string | `B2C` \| `B2B` |
| `ai_native` | boolean | `true` / `false` |
| `founders_json` | string | JSON array: `[{name, linkedin, education, exits, previous_companies}]` |
| `monitoring_enabled` | boolean | `true` only if `company_score >= 55` |
| `discovered_via` | string | Source ID (`yc_companies`, `techcrunch`, `inc42`, `hacker_news`, etc.) |
| `last_checked_at` | date | Timestamp of last Track 2 poll |

### Table 2: `jobs_seen` (Primary Key: `job_id`)
Based on existing `DATA_TABLE_COLUMNS` in `_shared/scripts/build_workflow.py`, extended with signal tracking:
- Keep all existing columns: `job_id`, `title`, `company`, `is_product_manager_role`, `experience_level`, `experience_level_code`, `experience_level_description`, `min_years_experience`, `locations`, `primary_location`, `location_count`, `cities`, `country_codes`, `has_india_location`, `locations_json`, `remote_eligible`, `education_levels`, `minimum_qualifications`, `preferred_qualifications`, `about_the_job`, `responsibilities`, `applicant_notes`, `location_note`, `job_url`, `apply_url`, `job_created_at`, `job_published_at`, `job_updated_at`, `search_query`, `search_location`, `search_result_rank`, `source_page_url`, `page_saved_at`, `detail_status`, `last_scraped_at`.
- **Add these columns:**
  - `company_slug` (string)
  - `first_seen_track` (number: `1` = LinkedIn Human Post, `2` = Direct Company Portal, `3` = Aggregator)
  - `signal_quality` (string: `high` | `medium` | `low`)
  - `role_priority_rank` (number: `1`..`4`)
  - `match_score` (number: `0`..`100`)
  - `hiring_manager_linkedin` (string)
  - `alert_sent` (boolean)

### Table 3: `portal_auth_vault` (Primary Key: `portal_id`)
Stores synced session cookies & auth health for cookie-gated portals (pushed by localhost dashboard `http://127.0.0.1:8765`):
| Column | Type | Notes |
|--------|------|-------|
| `portal_id` | string | `linkedin`, `wellfound`, `cutshort`, `instahyre`, `iimjobs`, `otta`, `crunchbase`, `the_ken`, `twitter_founders` |
| `cookie_header` | string | Full `Cookie` HTTP header string |
| `extra_headers_json` | string | JSON object (e.g. `{"csrf-token": "..."}` for LinkedIn Voyager) |
| `captured_at` | date | When user last signed in |
| `expires_at` | date | Computed earliest critical cookie expiry |
| `cookie_status` | string | `healthy` \| `expiring_soon` \| `expired` \| `missing` |
| `workflow_status` | string | `ok` \| `broken` |
| `last_error` | string | Last HTTP/parser error |
| `local_reauth_url` | string | `http://127.0.0.1:8765/auth/start?portal=<portal_id>` |

### Table 4: `portal_registry` (Primary Key: `portal_id`)
Stores custom reverse-engineered portal configs (`method`, `url`, `query_json`, `headers_json`, `parser_type`, `parser_config_json`, `track`, `enabled`).

---

## 4. Detailed Workflow Specifications

### Workflow 1: `WF_01_Company_Discovery`
- **Trigger:** `Schedule Trigger` (Daily 07:00 IST) + `Manual Trigger`
- **Nodes:**
  1. `Config` (`Set`): holds API limits, search keywords (`AI`, `recruitment`, `ecommerce`, `remote`), and LLM scoring prompt parameters.
  2. `Fetch Discovery Feeds` (Parallel branches, all `onError: continueRegularOutput`):
     - **Hacker News Who Is Hiring:** `GET https://hn.algolia.com/api/v1/search?query=Ask+HN+Who+is+hiring&tags=ask_hn&hitsPerPage=1` → `GET https://hacker-news.firebaseio.com/v0/item/{{objectID}}.json` → fetch comment items.
     - **TechCrunch Funding:** `GET https://techcrunch.com/wp-json/wp/v2/posts?per_page=20&search=Series+A`
     - **Inc42 Funding:** `GET https://inc42.com/wp-json/wp/v2/posts?per_page=20&search=Series+A`
     - **YC Directory / ProductHunt / Surge / Antler:** Configured HTTP endpoints (populated from HAR reverse-engineering).
  3. `Normalize Candidate Companies` (`Code`): Extracts `{company_name, website, source_id, raw_context}` using pure JS.
  4. `Deduplicate Against Watchlist` (`Data Table` Lookup on `companies_watchlist`): Keeps only new/unscored companies.
  5. `Research & Score Company` (`AI Agent / LLM Node` + HTTP search tool):
     - Evaluates **Hard Filters**: Stage >= Series A (or Tier 1/2 funded / >$5M ARR), non-US-only remote friendly.
     - Computes **110-point rubric normalized to 100**:
       - Investor Quality (20): Tier 1 (`a16z`, `Sequoia`, `Peak XV`, `Accel`, `YC`, `Lightspeed`, `Benchmark`, etc.) = 20; Tier 2 = 14; Tier 3 = 8; Tier 0 = 0.
       - Founder Education (15): IIT / Ivy League (Harvard, Stanford, MIT, etc.) = 15; Top-100 Global = 10; Other = 5.
       - Founder Career Pedigree (20): C-suite/VP at FAANG/Unicorn, serial founder, McKinsey/BCG/Bain.
       - Past Exits (15): 1 exit = 10; 2+ exits = 15.
       - Industry Match (10): Hiring/Recruitment AI (10), AI & Automation (9), eCommerce/Dropshipping AI (8), Marketing & Sales Tech (7), Trading/FinTech (6), Others (1–5).
       - Role Match (10), Location Compliance (10), Product Stage Fit (10).
     - Extracts **Founders LinkedIn URLs** + detects **ATS Platform** (`ashby` / `greenhouse` / `lever` / `custom`) by inspecting `/careers` HTML links.
  6. `Upsert companies_watchlist` (`Data Table` Upsert): Sets `monitoring_enabled = (company_score >= 55)`.

---

### Workflow 2: `WF_02_Job_Signal_Monitor`
- **Trigger:** `Schedule Trigger` (Every 2 hours) + `Manual Trigger`
- **Nodes:**
  1. `Config` (`Set`): holds target role regexes, location allow/deny regexes, and `track3_enabled` flag.
  2. **Branch A — Track 1: LinkedIn Human Signals (Highest Priority):**
     - Read `linkedin` row from `portal_auth_vault`.
     - If `cookie_status == 'expired'` or missing → route to `WF_04` alert and skip HTTP call.
     - Loop over `companies_watchlist` (`watchlist_tier == 'strong_match'`) via `SplitInBatches` (`batchSize: 1`).
     - `HTTP Request` to LinkedIn Voyager search (`onError: continueRegularOutput`) with `Cookie` + `csrf-token` headers.
     - If HTTP status is `401` / `403` / `999` → trigger `WF_04` with `{portal_id: 'linkedin', status: 'broken', error: 'HTTP 401/403'}`.
     - Parse recent (<48h) human hiring posts mentioning company + PM/FDE/PMM/CoS; emit with `first_seen_track = 1`, `signal_quality = 'high'`.
  3. **Branch B — Track 2: Direct Company Career Portals (Primary):**
     - Read active `companies_watchlist` rows (`monitoring_enabled == true`).
     - `Switch` on `ats_platform`:
       - `ashby` → `GET https://api.ashbyhq.com/posting-api/job-board/{{ats_slug}}?includeCompensation=true`
       - `greenhouse` → `GET https://boards-api.greenhouse.io/v1/boards/{{ats_slug}}/jobs?content=true`
       - `lever` → `GET https://api.lever.co/v0/postings/{{ats_slug}}?mode=json&limit=250`
       - `google_ds1` → `GET https://www.google.com/about/careers/applications/jobs/results?...`
       - `custom` → lookup `portal_registry` and execute custom reverse-engineered request.
     - Parse & normalize every job in `try/catch` (`Code` node), tagging `first_seen_track = 2`, `signal_quality = 'high'`.
  4. **Branch C — Track 3: Aggregator Boards (Catch-All, Daily Guard):**
     - Run only when hour == 08 IST (or manual override).
     - Fetch `remoteok`, `himalayas`, `wellfound`, `cutshort`, `instahyre`, `iimjobs`, `otta` using `portal_auth_vault` cookies where needed.
     - Tag `first_seen_track = 3`, `signal_quality = 'low'`.
     - **Feedback Loop:** If an unknown company appears with matching role + location, send its name/URL to `WF_01` (`Execute Workflow`) to score and potentially add to `companies_watchlist`.
  5. `Deduplicate Against jobs_seen` (`Data Table` Lookup by `job_id`): Keep only unseen jobs.
  6. `Call WF_03_Job_Enrichment_And_Alert` (`Execute Workflow`).

---

### Workflow 3: `WF_03_Job_Enrichment_And_Alert`
- **Trigger:** `Execute Workflow Trigger`
- **Hard Filter Gate (`Code` node):**
  - **Location Filter (STRICT):**
    - PASS only if location matches: `Remote India`, `Remote (Global/Worldwide/Anywhere)`, `India`, `Dubai / UAE`, or `United Kingdom / London`.
    - **HARD REJECT** if location is `Remote - US`, `Remote (USA)`, `Remote - North America`, `Remote - Canada`, or requires US/Canada work authorization without India/Global/UK/Dubai option.
  - **Role Priority Classifier:**
    - Rank 1: `Forward Deployed Engineer` / `AI Customer Engineer` / `AI Builder` / `Solutions Engineer (AI)`
    - Rank 2: `Product Manager` / `Founding PM` / `AI PM` / `Head of Product`
    - Rank 3: `Product Marketing Manager` / `PMM`
    - Rank 4: `Chief of Staff` / `Founder's Office` / `Strategy & Operations`
  - **Product Type Classifier (for PM/PMM):**
    - Priority: `B2C AI` (1) > `B2B AI` (2) > `B2C Core` (3) > `B2B Core` (4).
  - **Zero-to-One Signal:** Boost if JD mentions `0-to-1`, `zero to one`, `founding`, `greenfield`, `build from scratch`.
- **Persistence:** `Data Table` Upsert into `jobs_seen` (`alert_sent = true`).
- **Notification (`Telegram` / `Slack` / `Gmail`):**
  - Immediate alert formatted as:
    - `[Track 1/2/3 Badge] Company Name (Score: XX/100 | Grade: A+)`
    - `Role Title (Priority #1–4) | Location | B2C/B2B AI`
    - `Funding & Investors | Founder Name + LinkedIn URL`
    - `Direct Apply URL + Hiring Manager Post URL (if Track 1)`

---

### Workflow 4: `WF_04_Cookie_Health_And_Sync`
- **Trigger 1:** `Webhook` (`POST /webhook/auth-cookie-sync`, Header Auth: `X-Sync-Token`)
  - Called automatically by `_shared/dashboard/server.py` whenever you sign in via `http://127.0.0.1:8765/auth/start?portal=<id>`.
  - Upserts `{portal_id, cookie_header, extra_headers_json, captured_at, expires_at, cookie_status: 'healthy', workflow_status: 'ok', last_error: ''}` into `portal_auth_vault`.
- **Trigger 2:** `Execute Workflow Trigger` (called by `WF_02` on HTTP 401/403) + `Schedule Trigger` (Daily 09:00 IST)
  - Marks broken portal as `cookie_status = 'expired'`, `workflow_status = 'broken'`.
  - Scans `portal_auth_vault` for any row where `expires_at < now + 24h` or `cookie_status == 'expired'`.
  - Sends an alert (Telegram/Slack/Email) listing broken/expiring portals with clickable local re-auth links:
    - `👉 Refresh LinkedIn: http://127.0.0.1:8765/auth/start?portal=linkedin`
    - `👉 Refresh Wellfound: http://127.0.0.1:8765/auth/start?portal=wellfound`

---

## 5. Local-to-Cloud Auth Handshake Flow

```text
1. WF_02 detects 401 on LinkedIn → calls WF_04 → Telegram alert sent to user
2. User clicks link in alert or dashboard:
     http://127.0.0.1:8765/auth/start?portal=linkedin
3. Localhost server launches isolated Chrome window at linkedin.com/login
4. User logs in manually (supports Google SSO, 2FA, any anti-bot check)
5. Localhost server reads cookies via Chrome DevTools Protocol (CDP)
6. Server encrypts cookies locally in _secrets/cookies/linkedin.enc
7. Server POSTs fresh cookie_header + expires_at to n8n Cloud WF_04 Webhook
8. n8n Cloud updates `portal_auth_vault` → next WF_02 run resumes cleanly
```

