# Job-Seeker Contact-Finding Pipeline: Two-Part Self-Prompt

- **Part 1: Deep research prompt.** Paste it into a deep-research tool (Claude Research, Perplexity, ChatGPT, or Gemini Deep Research). It produces the research report.
- **Part 2: Claude Code build prompt.** Paste it into Claude Code together with the Part 1 report. It audits the existing n8n workflows and lead ingestion pipeline, designs the enrichment layer, then builds and ships a **working** pipeline that enriches each lead in the mode the user picks: **email only, phone only, or both**.

---

# PART 1: DEEP RESEARCH PROMPT

## ROLE

Act as a senior RevOps / data-enrichment architect and a job-search outreach strategist. You understand B2B contact databases, enrichment waterfalls, email verification, phone data sourcing, API automation, deliverability, and data-privacy law. You are skeptical of vendor marketing and verify every claim against primary sources.

## CONTEXT

- I am building a reusable system for **multiple job seekers** (me, my brother, and eventually many more people), mostly based in **India**, targeting roles in India and abroad.
- Goal: find contact details of the **right people** at target companies (hiring managers, team leads, recruiters / talent acquisition, and founders at startups) so we can send personalised cold outreach.
- Budget philosophy: **exhaust every legitimate free credit first**, then move to the **cheapest reliable paid tool**, then climb to more expensive tools **in increasing order of cost**, only when cheaper layers fail.
- Each job seeker will run the pipeline under **their own accounts** (one person = one set of free accounts). Do NOT recommend creating fake or duplicate accounts to farm credits. Flag any tool whose ToS restricts this.

## THE THREE OUTPUT MODES (design for all three)

The pipeline must work for each of these requests independently:

1. **Email only:** verified work email (preferred) or personal email.
2. **Phone only:** mobile / direct dial (for WhatsApp or a call).
3. **Both:** email + phone for the same person.

Phone credits usually cost 5–10x email credits, so the cost logic must be different per mode.

## TOOL UNIVERSE

Research at minimum the tools below. Also **discover and add** any other relevant tool active in 2026 (new entrants, India-focused providers, open-source options).

**Email + phone finders / databases:** Apollo.io, Hunter.io, Snov.io, Prospeo, ContactOut, GetProspect, Skrapp.io, Lusha, RocketReach, Kaspr, SignalHire, Seamless.ai, Surfe, Swordfish, UpLead, AeroLeads, Tomba, Icypeas, LeadMagic, Datagma, Anymail Finder, Voila Norbert, Findymail, Wiza, Dropcontact, Clearbit/HubSpot Breeze. Include Cognism and ZoomInfo as benchmarks only.

**Waterfall / aggregator tools:** Clay, FullEnrich, BetterContact, and any similar multi-source enrichers.

**Email verifiers:** NeverBounce, ZeroBounce, MillionVerifier, Reoon, Bouncer, Hunter Verifier, MailTester, and free SMTP-check methods.

**DIY / zero-cost methods:** email permutator + verifier, Google dorking, company website / press pages, GitHub commit emails, conference speaker lists, public company filings, Gmail/Outlook profile-check trick, LinkedIn "Contact info" section.

## DATA TO COLLECT PER TOOL

For each tool, capture all of these fields. Write "Unknown" if a value is not found; never guess.

| Field | Detail |
|---|---|
| Free tier | Credits per month, refresh cycle, and whether it resets monthly or is one-time |
| Credit cost | Credits per email reveal vs per phone reveal vs per verification |
| Charged on miss? | Whether credits are deducted when there is no result or the result is invalid |
| Data types | Work email, personal email, mobile, direct dial |
| India coverage | Specific evidence of Indian contact / +91 mobile coverage |
| Input methods | LinkedIn URL, name + domain, Chrome extension, bulk CSV, Sales Navigator |
| API access | Available on free tier? Paid only? Rate limits (per second / minute / day / month) |
| API details | Auth method, base URL, find / verify / credits-balance endpoints, required inputs, a sample response, async vs sync (webhook/polling), and whether a native n8n node or community node exists |
| Accuracy | Vendor claim AND independent benchmark (separate columns) |
| Verification | Built-in verification? Catch-all handling? |
| Entry paid plan | Price (USD and INR if listed), credits included, annual vs monthly |
| Pay-as-you-go | Available? Price per credit |
| Rollover | Whether unused credits roll over |
| Cost per verified email | Calculated from entry paid plan |
| Cost per verified phone | Calculated from entry paid plan |
| ToS restrictions | Multi-account rules, resale / sharing rules, LinkedIn-scraping risk |
| Source + date checked | Official pricing page URL + date verified |

## VERIFICATION RULES

1. Use **official pricing pages and docs first**, then independent benchmarks (e.g. third-party waterfall tests, G2/Capterra patterns, and Reddit threads in r/sales, r/coldemail and r/developersIndia).
2. Treat any figure older than 6 months as **stale** and flag it.
3. When sources conflict, show both values and explain which you trust and why.
4. Mark each key number with confidence: **High / Medium / Low**.
5. Re-verify these claims from my earlier notes, which may be outdated or wrong: Apollo "unlimited email searches", Prospeo 100 free credits, ContactOut ~50 free credits, Hunter 25–50 free searches, Lusha 5–40 credits, RocketReach 5 lookups, Skrapp $29–39 for 2,000 credits.

## ANALYSIS TASKS

### Task 1: Free Pool Calculation
- Total free credits per person per month across all tools, split into emails, phones and verifications.
- The realistic number of **verified contacts** per person per month after applying each tool's hit rate (not raw credits).
- How this scales for 1, 5, 20 and 100 job seekers (each with their own accounts).

### Task 2: Waterfall Order (per mode)
Build three separate waterfalls (email only / phone only / both). For each step, state:
- Which tool, and why it sits at that position (cost, hit rate, India coverage, charged-on-miss).
- The stop condition: when a verified result is found, skip the remaining steps.
- The fallback to the next step.

Logic to follow: zero-cost DIY → free credits (highest hit rate first, and tools that don't charge on misses first) → cheapest paid → next cheapest paid → premium.

### Task 3: Paid Ladder
- Rank all paid tools by **cost per verified email** and separately by **cost per verified phone** (ascending).
- Identify the single best "first paid tool" for each mode, with justification.
- Show break-even: the monthly volume at which buying a paid plan beats stacking free tiers.
- Compare aggregators (Clay, FullEnrich, BetterContact) with building our own waterfall.

### Task 4: Pipeline Architecture
Design an end-to-end pipeline with these stages:
1. **Target sourcing:** how to find the right people (titles, companies, hiring signals like open job posts).
2. **Enrichment waterfall:** from Task 2.
3. **Verification:** email verification + phone validity check, and how to handle catch-all domains.
4. **Storage / dedup:** shared Google Sheet or lightweight CRM; a schema with columns; how to avoid two job seekers spending credits on the same contact.
5. **Credit tracker:** how to track remaining free credits per tool per person.
6. **Automation options:** manual (Chrome extensions), semi-automated (Google Sheets + APIs) and fully automated (n8n / Make / Clay). Note which tools have free-tier API access.

### Task 5: Compliance and Deliverability
- India **DPDP Act 2023** and its Rules, GDPR (for EU contacts), CAN-SPAM (US): what is allowed for one-to-one job-seeking outreach.
- TRAI / DND rules and WhatsApp Business policy for calling or messaging Indian phone numbers.
- LinkedIn User Agreement risk for Chrome extensions that scrape profiles, and which tools are lower-risk.
- Deliverability rules: daily send limits per Gmail/Outlook inbox, bounce-rate threshold, warm-up, and whether to use a separate domain.

## OUTPUT FORMAT

1. **Executive summary** (max 10 bullets).
2. **Master comparison table:** all tools, all fields from "Data to Collect".
3. **Free pool table:** per person per month, by data type.
4. **Three waterfalls** (email only / phone only / both) as numbered step lists.
5. **Paid ladder table:** sorted ascending by cost per verified contact, separate for email and phone.
6. **Capacity model:** a table for 1 / 5 / 20 / 100 users at $0, ~$25, ~$50 and ~$100 per month budget.
7. **Pipeline architecture:** stage by stage, plus a Google Sheet schema.
8. **Compliance checklist:** a do / don't list.
9. **Sources:** every claim linked, with date checked.
10. **Open questions / gaps:** what could not be verified.
11. **Machine-readable appendix:** the master comparison table also as a JSON array (one object per tool, using the "Data to Collect" fields as keys), so Part 2 can ingest it directly.

## CONSTRAINTS

- No fabricated numbers. "Unknown" is better than a guess.
- Separate vendor claims from independent evidence.
- Prioritise accuracy and India relevance over breadth.
- All recommendations must be legal and within each tool's Terms of Service.

---

# PART 2: CLAUDE CODE BUILD PROMPT (AUDIT → DESIGN → BUILD → SHIP IN n8n)

> Paste this into Claude Code. Put the Part 1 research report (and its JSON appendix) in the working directory as `research/`.

## ROLE

Act as a senior automation engineer and n8n architect. You build production-grade, cost-aware data-enrichment systems **on top of systems that already exist**. You treat every API credit as money, every rate limit as a hard wall, every API key as a secret, and every existing workflow as production that must not break. The operator (me) is semi-technical: explain decisions in plain language and keep me in control at every gate.

If n8n-related skills are available in this environment (for example `n8n-operator` or `n8n-house-rules`), load them before any n8n work and follow them; they override general defaults.

## MISSION AND DEFINITION OF DONE

Build a lead-enrichment pipeline in n8n that **plugs into my existing workflows and my existing lead ingestion pipeline**, and enriches every ingested lead in the mode chosen by the user:

| Mode | What gets found | What must NOT happen |
|---|---|---|
| `email` | Verified work email (personal email as fallback) | No phone credits spent |
| `phone` | Validated mobile / direct dial | No email credits spent, unless an email unlocks a cheaper phone lookup |
| `both` | Verified email + validated phone | Never pay twice for the same field |

**Done means all of these are true:**

1. A lead entering through the **existing** ingestion pipeline is enriched automatically, with no manual copy-paste between systems.
2. The user's chosen mode is read from the lead (or the user's default) and respected exactly.
3. Results are written **back into the existing lead record / store** (not into a new silo), with status, source, confidence and timestamp.
4. Free-tier credits are used first and to the maximum, in cost order, without exceeding any quota or rate limit; paid tools are used only in ascending cost order and within budget.
5. Existing workflows keep working exactly as before. Enrichment can be switched off with one flag, and the old flow still runs.
6. It has run successfully on **real leads from the real ingestion pipeline** in all three modes, with a test report showing hit rate, credits used and ₹ cost.

## GUIDING PRINCIPLES

- **Discover before you ask.** Inspect what exists first; ask me only what you cannot find out yourself.
- **Integrate, don't rebuild.** Reuse the existing ingestion, storage, credentials and naming conventions. Add the enrichment layer beside them.
- **Non-destructive changes.** Before editing any existing workflow, export a backup JSON and get my approval for the exact change. Prefer adding one hook node (e.g. an Execute Workflow call or a status-change trigger) over rewriting existing logic.
- **Ship a thin working slice early.** Get `email` mode working end to end on real leads first, then add `phone`, then `both`. Never sit on a big unfinished build.
- **Safety rails before features.** Credit ledger, rate limiter, dry-run flag and error handling exist before the first provider is wired in.

---

## PHASE 0: DISCOVERY AUDIT (read-only, no changes)

### 0.1 Connect and inventory
1. Check how you can reach n8n: n8n public API, n8n MCP server, or CLI. If none work, ask me to export the relevant workflow JSONs into `existing/`.
2. List **all** existing workflows: name, ID, active state, trigger type, schedule, tags, last executions and error rate.
3. Export every relevant workflow JSON into `existing/` (read-only snapshot, committed to git) as the baseline backup.
4. List existing **credentials** by name and type only (never print secret values), so you can reuse them.

### 0.2 Map the existing lead ingestion pipeline
Produce `AUDIT.md` with:
- **Flow map** (Mermaid): sources → ingestion workflow(s) → where leads are stored → any downstream workflows (outreach, CRM sync, notifications).
- **Lead store:** type (Google Sheet / Airtable / Postgres / Notion / other), location, tab/table names, and the **exact current schema** (column names, types, sample rows with personal data masked).
- **Lead identity:** what uniquely identifies a lead today (row ID, LinkedIn URL, email, or nothing). Flag duplicates if any.
- **Fields available for enrichment:** which of first name, last name, full name, company, domain, LinkedIn URL, title and location exist, and how clean they are (fill rate %).
- **Ownership:** how a lead is tied to a job seeker (user) today, if at all.
- **Mode field:** whether any field already says email / phone / both. If not, propose where the choice should live.
- **Downstream dependencies:** which workflows read the lead store, and which columns they depend on, so enrichment never breaks them.
- **Execution budget:** n8n hosting (Cloud plan with executions/month, or self-hosted), version, queue mode, and current monthly execution usage.
- **Risks and unknowns.**

### 0.3 Ask me only what's still unknown
After the audit, ask in one batch only what you could not discover, for example:
1. Which tools are signed up per user, and which API keys exist?
2. Monthly paid budget per user (₹ / $), and whether paid escalation is automatic or needs my approval?
3. How should a user choose the mode: a column in the lead sheet, a dropdown in the intake form, a webhook parameter, or a per-user default with per-lead override?
4. Should enrichment run instantly per lead, in scheduled batches, or both?
5. Any approval needed before writing to the production lead store?

**Gate 1:** wait for my answers and OK on `AUDIT.md`.

---

## PHASE 1: INGEST AND VALIDATE THE RESEARCH

1. Parse the research report into `TOOL_REGISTRY.json`, one record per tool:
   - `tool_id`, `data_types` (work_email / personal_email / mobile / direct_dial), `input_types` (linkedin_url / name_domain / email)
   - `lane` (api / manual / excluded), `n8n_node` (native / community / http_request)
   - `base_url`, `auth_type`, endpoints for find / verify / credits-balance, sync or async
   - `free_credits_per_period`, `period`, `reset_rule` (calendar month / signup anniversary / daily)
   - `credits_per_email`, `credits_per_phone`, `charged_on_miss`
   - `rate_limits` (per second / minute / hour / day), `max_concurrency`
   - `paid_cost_per_verified_email`, `paid_cost_per_verified_phone`
   - `india_coverage_score`, `expected_hit_rate`, `observed_hit_rate` (starts null)
   - `tos_notes`, `confidence`, `last_verified_date`
2. Re-check the **current official API docs** of every API-lane tool. Where the docs disagree with the research, trust the docs and log the difference in `DECISIONS.md`.
3. Produce three waterfall configs (`waterfall_email.json`, `waterfall_phone.json`, `waterfall_both.json`), each an ordered list of steps with its cost reasoning.
4. Short **Gap Report:** missing data, low-confidence numbers, and the assumptions you will use.

**Gate 2:** wait for my OK.

---

## PHASE 2: DESIGN (`DESIGN.md`, no building until approved)

Design for failure modes, not just the happy path. Cover every section below.

### 2.1 Integration design (most important section)
- **Hook point:** exactly how enrichment is triggered from the existing pipeline. Options to evaluate: (a) one Execute Workflow node added at the end of the existing ingestion workflow; (b) a separate trigger watching the lead store for new rows / `enrichment_status = pending`; (c) a webhook called by the ingestion flow. Recommend one, justify it, and show the exact change to the existing workflow as a before/after diff.
- **Field mapping:** a table that maps existing lead fields → enrichment input contract, plus the transformations needed (split full name, derive domain from company or website, canonicalise LinkedIn URL).
- **Write-back:** the new columns/fields to add to the existing lead store, all prefixed (e.g. `enr_`) so nothing existing is overwritten:
  `enr_mode, enr_status, enr_email, enr_email_status, enr_email_source, enr_phone, enr_phone_type, enr_phone_source, enr_confidence, enr_credits_used, enr_cost_inr, enr_updated_at, enr_error`
- **Downstream safety:** show that no column used by downstream workflows changes. If a downstream workflow should consume the enriched data (e.g. outreach), propose the change separately, and do not make it without approval.
- **Kill switch:** a single flag (env variable or config row) that turns enrichment off and lets ingestion run exactly as before.
- **Backfill:** how to enrich leads that already exist in the store, in throttled batches that respect free quotas.

### 2.2 Mode selection logic
- Where the mode is read from (per Step 0.3), with precedence: per-lead value → per-user default → global default.
- Validation: unknown or empty values fall back to the default and are logged.
- **Upgrade path:** if a lead was enriched in `email` mode and later switched to `both`, only the missing phone is fetched; the existing email is reused.

### 2.3 Architecture
A Mermaid diagram plus a modular n8n structure: one orchestrator plus sub-workflows (Execute Workflow). Suggested modules (adjust with justification): `enr_intake`, `enr_normalise`, `enr_cache_lookup`, `enr_waterfall_orchestrator`, `enr_provider_<tool>` (one per tool), `enr_verify_email`, `enr_validate_phone`, `enr_credit_ledger`, `enr_rate_limiter`, `enr_writeback`, `enr_credit_reset_scheduler`, `enr_reporting`, `enr_error_handler`, `enr_manual_queue`. Use the `enr_` prefix to separate the new workflows from the existing ones.

### 2.4 Standard provider contract
Every adapter accepts and returns the **same JSON schema**, so a new tool = one adapter + one registry row:
- Input: `lead_id, user_id, mode, first_name, last_name, full_name, company, domain, linkedin_url, fields_needed[], dry_run`
- Output: `status (found / not_found / error / rate_limited / quota_exhausted), email, email_type, phone, phone_type, provider_confidence, credits_spent, latency_ms, error_code`

### 2.5 Supporting data stores
Decide whether these live in the existing store or in a separate database (justify the choice against real limits, e.g. Google Sheets API per-minute quotas and cell limits; high-write logs should not live in Sheets):
- `enr_users`: user_id, name, budget, default mode, active tools
- `enr_contacts_cache`: global, keyed by canonical LinkedIn URL and by `name + domain`, with a TTL (e.g. 90 days)
- `enr_domain_patterns`: learned email pattern per domain, with confidence
- `enr_credit_ledger`: user × tool × period: allowance, reserved, used, remaining, reset_at
- `enr_provider_runs`: one row per API call (audit + hit-rate stats)
- `enr_suppression_list`: never look up or contact these people
- `enr_dead_letter`: failed items with error context

### 2.6 Lead state machine
`pending → normalised → cache_hit | enriching → found_unverified → verified | catch_all | invalid → done | needs_manual | failed | skipped_suppressed | skipped_disabled`. Every transition is persisted, so a crash resumes without re-spending.

### 2.7 Waterfall engine
- The order is **config-driven** (the Phase 1 waterfall files), never hard-coded in nodes.
- Effective cost per verified result = `cost_per_credit × credits_per_lookup ÷ observed_hit_rate`. Free credits cost ₹0 but carry a scarcity weight, so the best free tools are not burned on leads a zero-cost method could solve.
- **Tier 0 (₹0):** cache → learned domain pattern + free verification → other DIY sources.
- **Tier 1 (free credits):** prefer tools that don't charge on misses, and tools whose credits reset soonest ("use it or lose it").
- **Tier 2+ (paid):** ascending cost, capped per lead and per user per month; requires approval if I chose that.
- Request only the `fields_needed` for the mode; never reveal paid fields you don't need.
- Stop at the first result that passes verification for all needed fields.
- **Learning loop:** every verified email updates `enr_domain_patterns`; observed hit rates update the waterfall order monthly.

### 2.8 Credit ledger
- **Reserve** credits before a call, **commit** actual credits after it, and **release** them on a miss for tools that don't charge on misses.
- Reconcile daily with each tool's credits-balance endpoint, where one exists; the provider's number wins.
- Stop at a safety buffer (e.g. 95% of quota).
- Reset on each tool's real reset rule.
- Concurrency-safe: two parallel executions must never spend the last credit (atomic DB update or row lock, not n8n static data).

### 2.9 Rate limiting and resilience
- A per-tool limiter for per-second, per-minute and per-day limits.
- 429 → respect `Retry-After`, then exponential backoff with jitter; skip to the next provider if the wait is too long.
- 401/403 → mark that user's key as broken, alert me, skip the tool for that user.
- Timeouts / 5xx → limited retries, then dead-letter.
- **Idempotency:** check `enr_provider_runs` before every paid call.
- Fit within n8n limits (execution timeout, memory, payload size, Cloud executions/month). Show the maths for expected volume.

### 2.10 Verification
- Email → `valid / invalid / catch_all / unknown`. Only `valid` is send-ready; `catch_all` gets a confidence score.
- Phone → normalise to E.164, validate the country and line type, and flag Indian numbers for DND / WhatsApp-policy care.
- Avoid raw SMTP checks from cloud or home IPs unless justified (blacklisting risk).

### 2.11 Multi-user
- Credentials named `<tool>_<user_id>` in n8n Credentials only.
- Per-user ledgers and budgets; a shared global cache (state the privacy implications).
- A new job seeker = config only (a user row + credentials). Write that checklist.

### 2.12 Manual lane
For extension-only tools: a daily task list per user, plus a simple paste-back path into the same verification + write-back flow.

### 2.13 Compliance
Check the suppression list before every lookup; store the source and timestamp per field; support deletion requests; keep data minimal; dry-run mode is ON by default.

### 2.14 Observability
A daily summary to me: leads enriched per mode, found rate, credits used vs remaining per tool per user, ₹ spent, errors, dead-letter count.

### 2.15 Rollout and rollback plan
Shadow mode (enrich, but write to a test copy of the store) → limited live (one user, 20 leads) → full live. Plus a rollback procedure: kill switch + restore the backup JSON of the existing workflow.

**Gate 3:** wait for my approval of `DESIGN.md`.

---

## PHASE 3: BUILD (thin vertical slices)

**Slice 0: Safety rails.** Supporting stores + seed config, `enr_credit_ledger`, `enr_rate_limiter`, `enr_error_handler`, the dry-run flag and the kill switch.

**Slice 1: Email mode, end to end.**
1. `enr_intake` + `enr_normalise` + `enr_cache_lookup`, reading from the **existing** lead store using the field mapping.
2. Tier 0 email (domain patterns + free verifier).
3. Email provider adapters **one at a time**, best free tool first. Each one: build → test with mocked/pinned responses → one live test on a known contact (with my approval; it spends a credit) → log actual vs expected credits.
4. `enr_waterfall_orchestrator` (email), `enr_verify_email`, `enr_writeback`.
5. Hook into the existing ingestion pipeline (the approved change only, after backing it up).
6. Run in shadow mode on 10 real ingested leads → show me the results → go live.

**Slice 2: Phone mode.** Phone adapters, `enr_validate_phone`, and the phone waterfall, through the same steps.

**Slice 3: Both mode.** Combined orchestration, the reuse/upgrade path, and the no-double-pay check.

**Slice 4: Operations.** `enr_reporting`, `enr_credit_reset_scheduler`, `enr_manual_queue`, and the backfill of existing leads.

Build rules:
- Prefer native n8n nodes and the HTTP Request node; keep Code nodes small and commented.
- No secrets anywhere except n8n Credentials.
- Match the existing naming conventions, and add sticky notes explaining each section in plain English.
- Export every new or changed workflow JSON into `workflows/` in git, with one commit per slice.
- Create workflows via the n8n API / MCP if available; otherwise give me importable JSON with exact import steps.
- **Never spend a real credit, edit an existing workflow, or write to the production lead store without telling me first.**

---

## PHASE 4: TEST AND PROVE IT WORKS

- **Unit:** each adapter against mocked found / not_found / 429 / 401 / 500 / timeout / malformed JSON.
- **Ledger:** 2 parallel executions on the last credit → no overspend.
- **Idempotency:** kill mid-run, resume → no double spend.
- **Integration:** a lead pushed through the real existing ingestion pipeline triggers enrichment and lands back in the lead store with the correct `enr_` fields.
- **Regression:** all existing workflows still run successfully, and downstream columns are unchanged.
- **Mode tests:** the same lead in `email`, `phone` and `both` → only the needed credits are spent; switching `email` → `both` fetches only the phone.
- **Kill switch:** enrichment off → ingestion behaves exactly as before.
- **Live run:** 20 real leads (mix of Indian startups, MNCs and catch-all domains) per mode, after a dry run first.
- `TEST_REPORT.md`: hit rate, credits used, ₹ cost, time per lead, and failures with their causes.

**Gate 4:** go-live approval.

---

## DELIVERABLES

1. `AUDIT.md`: the existing system map and schema.
2. `TOOL_REGISTRY.json` + `waterfall_email.json`, `waterfall_phone.json`, `waterfall_both.json`.
3. `DESIGN.md` (the approved version), including the integration diff.
4. `existing/`: backups of all existing workflows before changes.
5. `workflows/`: all new and changed workflow JSON, version-controlled.
6. Schema + seed scripts for the supporting stores.
7. `RUNBOOK.md` (for a non-technical operator): how to pick a mode, run a backfill, pause enrichment, add a user, add a tool, rotate a key, read the daily report, and roll back.
8. `TEST_REPORT.md` with real numbers.
9. `CAPACITY.md`: verified contacts per month at ₹0 and the cost to reach the target volume, per mode, for 1 / 5 / 20 users, updated with observed hit rates.
10. `DECISIONS.md`: every trade-off and why.

## ACCEPTANCE CRITERIA

- Leads from the existing ingestion pipeline are enriched automatically in the chosen mode and written back to the existing store.
- Existing workflows and downstream columns are unaffected; the kill switch restores the old behaviour.
- Zero quota overruns and zero duplicate paid lookups across users and retries.
- Each mode spends credits only on the fields it needs.
- All rate limits are respected; 429s are handled without data loss.
- New tool = 1 adapter + 1 registry row; new user = config only.
- Every enriched field has a source, timestamp and verification status.
- The full pipeline runs in dry-run mode end to end with ₹0 spent.

## WORKING STYLE

- Phases with explicit gates: after the audit, after the research ingest, after the design, before any live credit spend or production write, and before go-live.
- Discover first, then ask; never assume a field name or schema.
- Explain the "why" behind each design choice in one or two plain sentences.
- Report progress at the end of each slice: what works, what was tested, and what's next.
