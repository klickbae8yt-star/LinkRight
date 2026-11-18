# linkright-hunt — Skill Plan

**Skill:** `/linkright-hunt`
**Version:** 1.1.0 (in progress)
**Build Phase:** Phase 2
**Status:** Data layer built. Skill orchestration pending.

---

## 1. What This Skill Does

`linkright-hunt` is the job discovery and adaptive intelligence layer of Linkright.

It solves three distinct problems:

**Problem 1 — Discovery:** Find relevant job openings across multiple sources without manual browsing.

**Problem 2 — Understanding:** Given a JD, deeply analyze what the role actually requires — beyond keywords, into the real signal demands. Use the KB signal taxonomy so the analysis is rich and consistent.

**Problem 3 — Prioritization:** Which opportunities are actually worth your time? Combine profile fit (how well your signals match) with shortlist probability (what your actual application history says about which job types you convert on).

The system gets smarter every time you record an outcome. After 15-20 applications, its prioritization recommendations are meaningfully better than day one.

---

## 2. Two Modes of Operation

### Mode A — Batch Discovery (Automated, Runs Offline)

Pre-builds a curated job database (`jobs.db`) by sweeping all known target companies and job boards. User does not need to be present.

```
scrape_jobs.py       → 598 target companies via ATS APIs (20 ATS types)
jobspy_scrape.py     → LinkedIn guest API + Indeed India + Google Jobs (keyword sweep)
filter_pm_jobs.py    → classify titles, tag sectors, delete irrelevant
score_jobs.py        → semantic profile fit (sentence-transformers)
update_excel.py      → export to Job Database.xlsx
```

Triggered via skill with natural language description:
```
/linkright-hunt search founding PM roles at consumer AI startups, Series A/B, remote preferred
```

Claude interprets the description → derives params → runs scripts → presents ranked results.

### Mode B — Single JD Intelligence (Interactive, On-Demand)

User pastes a JD or URL. Skill runs full signal extraction pipeline, computes fit score, checks shortlist probability, flags red flags, mirrors vocabulary.

```
/linkright-hunt analyze [paste JD or URL]
/linkright-hunt score [paste JD]
/linkright-hunt enrich [opportunity ID] — add context from blog/interview reports
```

---

## 3. Natural Language Search Interface

The skill accepts a free-form description. Claude interprets it into structured params. This is the primary UX — no flag memorization required.

### Interpretation Rules

| User says | Extracted param |
|---|---|
| role type / title | `--search-terms` (mapped to canonical keyword list) |
| industry / domain | `--sectors` (CONSUMER_AI / CAREER_NAV_B2C / GAMING / SOCIAL_COMMERCE / ALL) |
| location ("India", "remote", "US open") | `--location` + `--remote` flag |
| freshness ("recent", "last week", "today") | `--hours-old` (24 / 72 / 168) |
| company stage ("Series A/B", "startup", "big tech") | used in output filter + display label |
| seniority ("entry", "mid", "senior") | adjusts search_terms (drop senior titles if entry; add senior if preferred) |

### Search Term Mapping

Claude maps the description to SEARCH_TERMS pulled from `jobspy_scrape.py:DEFAULT_SEARCH_TERMS` and `scrape_jobs.py:WORKDAY_SEARCH`. Examples:

| Description | Mapped search_terms | workday_search |
|---|---|---|
| "founding PM at AI startup" | founding product manager, chief of staff, ai product manager | product manager |
| "growth at B2C consumer app" | growth manager, growth product manager, product growth | growth |
| "AI PM roles" | ai product manager, ai builder, llm product, generative ai product | ai product |
| "customer success implementation" | customer success manager, implementation manager, solutions architect | customer success |

### Interpretation Output (shown to user before running)

```
Interpreted as:
  Search terms   : ["founding product manager", "chief of staff", "ai product manager"]
  Sectors        : CONSUMER_AI
  Location       : India
  Remote         : yes (preferred)
  Hours old      : 168 (7 days — wider window for founding roles)
  Workday filter : "product manager"

Run with these params? (y to confirm, or adjust)
```

---

## 4. The Two-Score System

Every opportunity gets exactly two independent scores. Never just one.

### Score A — Semantic Fit Score (v1: sentence-transformers)

**Phase 1 implementation** (built): `score_jobs.py`

Uses `all-MiniLM-L6-v2` (free, local, ~80MB, ~14ms/job on CPU):
1. Embed Satvik's career profile ONCE → `db/profile_embedding.npy`
2. Per job: embed `(title + description[:2000])`
3. `cosine_similarity(job_vec, profile_vec)` × 100 → `relevance_score`
4. Ghost detection: `similarity > 0.95` vs existing same-company job → `is_ghost=1`

**Phase 2 implementation** (to build): `fit_scorer.py`

Signal-based fit score using KB taxonomy:
```
fit_score = Σ (signal_i_required × user_strength_i × kb_weight_i) / Σ signal_i_required

Where:
  signal_i_required = 1 if job requires this signal (primary=1.0, secondary=0.6, mentioned=0.3)
  user_strength_i   = user's confirmed strength (high=1.0, medium=0.6, low=0.2, absent=0)
  kb_weight_i       = base importance from KB taxonomy for this archetype
```

Phase 2 fit score replaces Phase 1 `relevance_score` column once `jd_analyzer.py` is operational.

**This score does NOT change based on outcomes.** Factual snapshot: "given your profile today, this is the match quality."

---

### Score B — Shortlist Probability Score

**What it answers:** "Based on your application history — what's the realistic chance they'll actually call you?"

**Why this matters:**
High fit + high shortlist probability = clear priority.
High fit + low shortlist probability = archetype mismatch worth investigating.
Low fit + high shortlist probability = check what they actually value.

**How it's learned:**

```
OUTCOME TYPES (record one for each application after 14 days):
  SHORTLISTED    → got a call/screen (strong positive)
  CLEARED_STAGE  → advanced past initial screen (stronger positive)
  OFFER          → received offer (strongest)
  EARLY_REJECT   → rejected before screen (moderate negative)
  GHOSTED        → no response after 14 days (mild negative)

FEATURE VECTOR per job:
  - archetype: [ai_pm, enterprise_pm, growth_pm, platform_pm, ...]
  - domain: [ai, fintech, saas, consumer, b2b, ...]
  - company_stage: [startup, scaleup, enterprise, faang]
  - seniority: [ic4, ic5, ic6, director]
  - primary_signals: [systems_thinking, ambiguity_handling, ...] (top 3)
  - ats: [greenhouse, lever, ashby, ...]
```

**Confidence thresholds:**

| Outcomes recorded | Model confidence | Display |
|---|---|---|
| 0-4 | No model | "Record outcomes to start building your shortlist model" |
| 5-9 | Low | Score B shown with "early signal, limited data" note |
| 10-14 | Medium | Score B shown with confidence label |
| 15+ | High | Score B shown prominently |
| 25+ | Strong | Model report available |

---

### Combined Opportunity Score

```
opportunity_score = (fit_score × w_fit) + (shortlist_prob × w_shortlist)
Default: w_fit=0.5, w_shortlist=0.5
Tune: "prioritize fit" → 0.7/0.3 or "prioritize realism" → 0.3/0.7
```

---

## 5. Sector Targeting (B2C Filter)

Hard requirement: **B2C only** — consumer-facing products, not B2B SaaS.

Priority sectors:

| Sector tag | Focus | Companies |
|---|---|---|
| `CONSUMER_AI` | Direct-to-consumer AI products | Perplexity, Character.ai, Notion, Superhuman, Sarvam, Krutrim, ShareChat, OpenAI, Anthropic, Cohere |
| `CAREER_NAV_B2C` | Job seeker-facing career tools | LinkedIn, Glassdoor, Handshake, Unstop, Internshala, Apna, Cutshort, Rezi, TopMate |
| `GAMING` | Consumer gaming (all B2C) | Dream11, MPL, Nazara, WinZO, Games24x7, Krafton, SuperGaming, Riot, Epic Games |
| `SOCIAL_COMMERCE` | Consumer shopping / social selling | Meesho, GlowRoad, Shop101, Whatnot, TikTok |

**Explicitly excluded from sector targeting** (B2B tools, not B2C):
- Dropshipping tools: Shopify, DSers, AutoDS, Spocket
- Cold email tools: Instantly, Lemlist, Apollo, Brevo
- Automation tools: N8N, Zapier, Make

`detect_sector()` is implemented in `filter_pm_jobs.py` and `jobspy_scrape.py`. Column `sector` in `jobs.db`.

---

## 6. Signal Intelligence — JD Deep Analysis

This separates Linkright hunt from any job board filter. Every JD is analyzed through the full PM signal taxonomy.

### Signal Extraction Pipeline

```
RAW JD TEXT
    │
    ▼
Step 1: ARCHETYPE DETECTION
  → Which PM archetype does this role target?
  → Load archetype profile from KB: ref_04_archetype_requirements.md
  → Output: primary_archetype, secondary_archetype (if mixed role)

    │
    ▼
Step 2: SIGNAL REQUIREMENT EXTRACTION
  → Against KB signal taxonomy, extract:
    - Primary signals (emphasized repeatedly or in JD headline)
    - Secondary signals (mentioned once, important but not primary)
    - Mentioned signals (exists in JD but not core requirement)
    - Negative signals (things the role specifically de-emphasizes)
  → Output: signal_requirements map with emphasis levels

    │
    ▼
Step 3: DOMAIN + CONTEXT SIGNALS
  → Industry domain: AI, fintech, SaaS, consumer, etc.
  → Company stage signal: what stage behaviors does this require?
  → Seniority signal: strategic leadership vs IC execution vs hybrid
  → Team context: cross-functional, platform, growth, etc.

    │
    ▼
Step 4: RECRUITER LANGUAGE ANALYSIS
  → Extract verbatim phrases that reveal true priorities
  → Flag weasel language (e.g. "wear many hats" = unclear ownership)
  → Flag red flags (e.g. "manage support escalations" in a PM role)
  → Mirror vocabulary: these are the words to use in your resume/cover letter

    │
    ▼
Step 5: MANUAL ENRICHMENT (if user has context)
  → Company blog/podcast signals
  → Interview reports (Glassdoor/Blind)
  → Hiring manager profile: what do they post about on LinkedIn?
  → Recruiter call intel: what did they emphasize?
  → Output: enriched_signals (overrides or supplements JD-derived signals)
```

### Signal Taxonomy (from KB)

**Tier 1 — PM Core Competencies (universal)**
- `systems_thinking` — sees interconnections, not just features
- `ambiguity_handling` — defines scope without full information
- `stakeholder_leadership` — aligns without authority
- `execution_rigor` — ships on time, manages tradeoffs
- `user_empathy` — builds from real user understanding
- `data_fluency` — reasons from data, not assumptions
- `communication_clarity` — simplifies complex things

**Tier 2 — Archetype Signals (role-type specific)**
- AI PM: `ai_workflow_design`, `model_evaluation`, `ai_trust_ux`, `prompt_systems`
- Enterprise PM: `enterprise_workflow_ownership`, `implementation_management`, `b2b_buyer_psychology`
- Growth PM: `growth_experimentation`, `funnel_optimization`, `retention_mechanics`
- Platform PM: `api_design_thinking`, `developer_experience`, `platform_governance`
- Consumer PM: `engagement_loops`, `viral_mechanics`, `personalization_systems`
- Founding PM: `zero_to_one_execution`, `market_hypothesis_testing`, `resource_constraint_navigation`

**Tier 3 — Domain Signals (industry-specific)**
- Fintech: `regulatory_awareness`, `trust_and_compliance_ux`, `financial_product_design`
- AI/ML: `ml_systems_literacy`, `ai_safety_awareness`, `responsible_ai_ux`
- SaaS: `onboarding_optimization`, `churn_reduction`, `enterprise_sales_alignment`
- Consumer: `content_ecosystem_understanding`, `social_dynamics`, `habit_formation`

**Tier 4 — Contextual Signals (stage/seniority)**
- Startup: `first_principles_thinking`, `scrappy_execution`, `founder_alignment`
- Enterprise: `change_management`, `organizational_navigation`, `governance_design`
- Senior IC: `technical_depth_pm`, `roadmap_ownership`, `cross_team_influence`
- Manager: `team_building`, `coaching_ability`, `vision_communication`

Full taxonomy: `references/ref_02_signal_taxonomy.md`

---

## 7. Manual Signal Enrichment

The JD alone is incomplete. Companies often have unstated requirements.

| Source | How to Add | Impact |
|---|---|---|
| Company PM blog / podcast | Paste 2-3 URLs or key quotes | High |
| Glassdoor/Blind interview reports | Paste reported questions | High |
| Hiring manager LinkedIn | Paste URL or recent posts | Medium |
| Recruiter call notes | Free-text summary | High |
| Ex-employee insights | Free-text | Medium |
| Your read of the company | Free-text opinion | Medium |

Enrichment stored in opportunity record as `manual_signals`. Persists across sessions.

---

## 8. The Adaptive Shortlist Model — Full Design

### Data Structure (outcomes.json)

```json
{
  "outcomes": [
    {
      "opp_id": "OPP_001",
      "company": "Company A",
      "role": "Senior PM - Enterprise AI",
      "applied_date": "2026-05-10",
      "outcome": "shortlisted",
      "outcome_date": "2026-05-14",
      "stage_reached": "phone_screen",
      "features": {
        "archetype": "ai_enterprise_pm",
        "domain": "ai",
        "company_stage": "scaleup",
        "seniority": "ic5",
        "primary_signals": ["systems_thinking", "ai_workflow_design", "enterprise_workflow_ownership"],
        "ats": "greenhouse",
        "fit_score_at_application": 78
      },
      "notes": "HR said they liked the onboarding redesign story"
    }
  ],
  "model_version": "1.0",
  "last_updated": "2026-05-21",
  "total_outcomes_recorded": 0,
  "model_confidence": "none"
}
```

### Feedback Loop Rules

- Record outcomes within 14 days of applying — data gets stale quickly
- Ghosting threshold: 14 calendar days with no response = record as "ghosted"
- Model doesn't tell you to stop applying to low-probability roles — informs prioritization, not eliminates
- Model weights reset partially if user makes major profile changes

### Model Report (after sufficient data)

```
YOUR SHORTLIST PATTERNS (based on 18 applications):

CONSISTENTLY SHORTLISTED FOR:
  ✓ Enterprise PM roles at scaleup/Series B-D companies (7/9 = 78%)
  ✓ Roles where systems_thinking is a primary signal (8/10 = 80%)
  ✓ AI workflow / AI-native products (5/6 = 83%)

RARELY SHORTLISTED FOR:
  ✗ Pure growth PM roles (1/5 = 20%)
  ✗ Consumer apps with viral_mechanics as primary signal (0/3 = 0%)

RECOMMENDATION:
  Prioritize: AI-native enterprise PM roles at Series B-D
  Deprioritize (for now): consumer/growth PM roles
```

---

## 9. Portal Tier Architecture

### Tier 1 — Direct ATS APIs (Zero Risk, Built ✅)

Fully sanctioned, free, returns structured JSON. No login required. ATS APIs are designed to syndicate jobs outward.

| ATS | Endpoint Pattern | Limit | Status |
|---|---|---|---|
| Greenhouse | `boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true` | 20 (HTML heavy) | ✅ scrape_jobs.py |
| Lever | `api.lever.co/v0/postings/{slug}?limit=50` | 50 | ✅ scrape_jobs.py |
| Ashby | `api.ashbyhq.com/posting-api/job-board/{slug}` | 50 | ✅ scrape_jobs.py |
| Workday | CXS POST `{tenant}.wd{N}.myworkdayjobs.com/wday/cxs/.../jobs` | 50 + searchText filter | ✅ scrape_jobs.py |
| Workable | `apply.workable.com/api/v3/accounts/{slug}/jobs` | 50 | ✅ scrape_jobs.py |
| SmartRecruiters | `api.smartrecruiters.com/v1/companies/{slug}/postings?limit=50` | 50 | ✅ scrape_jobs.py |
| Eightfold | `{company}.eightfold.ai/api/apply/v2/jobs?num=50` | 50 | ✅ scrape_jobs.py |
| BambooHR | `{subdomain}.bamboohr.com/careers/list` | 50 | ✅ scrape_jobs.py |
| Teamtailor | `{subdomain}.teamtailor.com/jobs.json` | 50 | ✅ scrape_jobs.py |

**Additional ATS types to integrate (jobhive patterns):**
Rippling, Personio, iCIMS, JazzHR, Breezy, Pinpoint, Cornerstone, Recruitee, Oracle SuccessFactors, Taleo — `scripts/scrape_jobs.py` to expand.

**Combined coverage:** ~60-70% of tech PM roles globally. Start here always.

### Tier 2 — JobSpy Multi-Board (Guest API, Low Risk, Built ✅)

`python-jobspy` library. Scrapes job board guest APIs concurrently. No user account required.

| Board | Coverage | Risk |
|---|---|---|
| Indeed India | Strong India coverage | Very low (no auth) |
| Google Jobs | Aggregates from company pages | Very low (public) |
| Naukri | India's largest job portal | Low (guest endpoint) |
| LinkedIn (guest) | Uses `linkedin.com/jobs-guest/` — **no account login** | Low-medium (guest only) |

**LinkedIn safety note:** JobSpy uses LinkedIn's guest jobs API, NOT the authenticated account API. This is lower risk than account-level automation. However, it can be rate-limited per IP. **No LinkedIn account automation, ever.** If LinkedIn scraping fails, skip and use manual passive capture instead.

Script: `scripts/jobspy_scrape.py`. Accepts `--search-terms`, `--sectors`, `--location`, `--remote`, `--hours-old`, `--results`.

### Tier 3 — Free Niche APIs (No Auth, Pending ⏳)

| Source | Focus | API |
|---|---|---|
| Remotive | Remote-only | `remotive.com/api/remote-jobs?category=product` |
| RemoteOK | Remote-only | `remoteok.com/api?tags=product-manager` |
| Adzuna | India + global | 250 req/day free, API key required |
| Himalayas | Remote + global | No auth |
| Jobicy | Remote-only | No auth |
| WFH.io | Remote + startup | No auth |
| YC Work at a Startup | YC companies only | `workatastartup.com/jobs?role=product` (free, no auth) |

Add to `scripts/tier3_search.py` (to build).

### Tier 4 — Browser Extension Passive Capture (Built ✅)

`browser_snippets/passive_job_capture.js` v1.5 — Tampermonkey. Captures job pages during normal user browsing. Zero bot risk.

DOM Signal Matrix:
- Priority 1: `<script type="application/ld+json">` with `@type: "JobPosting"` → Very High confidence
- Priority 2: ATS URL pattern match → High confidence
- Priority 3: DOM heuristics (Apply button + H1 + 200+ word description) → Medium confidence

Import: `python3 scripts/import_browser_csv.py ~/Downloads/jobs_passive_*.csv`

### Tier 5 — Semi-Automated Indian Portals (Pending ⏳)

| Portal | Approach | Risk |
|---|---|---|
| Internshala | Playwright, human-like delays (2-4s), max 3 pages/session, no login | Low |
| Hirist | Same pattern | Low |

Script: `scripts/internshala.py` (to build, Phase 2+).

### Tier 6 — Medium Risk (Phase 3 only)

| Portal | Risk | Notes |
|---|---|---|
| Naukri (authenticated) | Medium | Residential proxy needed for bulk |
| Foundit | Medium | Same |

### LinkedIn — Safety Rules (Non-Negotiable)

| Rule | Detail |
|---|---|
| NO account automation | Never use authenticated LinkedIn API or headless browser with account session |
| NO connection request automation | Ban risk |
| NO DM automation | Ban risk |
| Guest endpoint | `linkedin.com/jobs-guest/` — JobSpy uses this. OK for job listing search. Stop if rate limited. |
| LinkedIn for passive reading | Browse as normal user; passive_job_capture.js handles capture |
| Email-first for networking | Find email addresses; do NOT use LinkedIn DMs for cold outreach |

---

## 10. Data Infrastructure

### Two Stores

| Store | Format | Purpose |
|---|---|---|
| `db/jobs.db` | SQLite | Batch discovery output. Raw job feed. Used for bulk scraping, filtering, scoring. |
| `memory/pipeline.json` | JSON | Active opportunity pipeline. Curated subset you're tracking. Full JD analysis + signals + outcome history. |

### Flow: jobs.db → pipeline.json

```
Batch scrape → jobs.db (thousands of jobs, rough filter)
    │
    ▼
User reviews top-scored jobs from Excel / skill output
    │
    ▼
"Save to pipeline" → pipeline_update.py → pipeline.json
    │
    ▼
Full JD analysis + signal extraction for saved opportunities
    │
    ▼
linkright-sync picks up from pipeline.json → tailored resume
linkright-interview picks up from pipeline.json → question bank
linkright-companion reads pipeline.json → daily briefing
```

### jobs.db Schema

```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT, company_id INTEGER, segment TEXT, portal_type TEXT,
    title TEXT, department TEXT, location TEXT,
    job_url TEXT, posted_at TEXT, scraped_at TEXT,
    job_description TEXT,        -- raw JD text (capped 8000 chars)
    compensation TEXT,           -- extracted compensation range
    years_experience TEXT,       -- extracted YoE requirement
    employment_type TEXT,        -- Full-time / Contract / Part-time
    is_remote INTEGER DEFAULT 0,
    role_category TEXT,          -- PM | AI_PM | GROWTH | PMM | CSM | IMPLEMENTATION | FINTECH_PM | FOUNDING | TPM | GENERAL_PM | UNCERTAIN
    sector TEXT,                 -- CONSUMER_AI | CAREER_NAV_B2C | GAMING | SOCIAL_COMMERCE | NULL
    relevance_score REAL,        -- 0-100, cosine similarity vs profile (Phase 1 fit score)
    is_ghost INTEGER DEFAULT 0,  -- 1 = repost detected via semantic similarity
    source_portal TEXT,          -- jobspy_linkedin | jobspy_indeed | ats_greenhouse | browser_csv | etc.
    scraped_url TEXT
);
```

### pipeline.json Schema (per opportunity)

```yaml
id: "OPP_001"
title: "Senior Product Manager — Enterprise AI"
company: "Company Name"
ats: "greenhouse"
source: "tier1_ats"          # tier1_ats | tier2_jobspy | tier3_api | browser_capture | manual
source_url: "https://..."
date_seen: "2026-05-21"
stage: "saved"               # saved|applied|screening|phone_screen|interview|final|offer|rejected|archived

# Fit Analysis
fit_score: null              # computed by fit_scorer.py (Phase 2) or relevance_score (Phase 1)
shortlist_probability: null  # computed from outcome history
opportunity_score: null      # combined score

# JD Analysis (filled by jd_analyzer.py)
jd_raw: ""
jd_analyzed:
  archetype: null
  primary_signals: []
  secondary_signals: []
  negative_signals: []
  seniority: null
  domain: null
  company_stage: null
  red_flags: []
  recruiter_language: []

# Manual Enrichment
manual_signals: []
enrichment_notes: ""

# Application Tracking
applied_date: null
resume_version_id: null
cover_letter_version_id: null

# Outcome
outcome: null
outcome_date: null
stage_history:
  - stage: "saved"
    date: "2026-05-21"
```

---

## 11. ATS Detection Probe

Discovers ATS for any company when you only have their name.

```python
def probe_ats(company_slug):
    endpoints = [
        ("greenhouse",      f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"),
        ("lever",           f"https://api.lever.co/v0/postings/{company_slug}"),
        ("ashby",           f"https://api.ashbyhq.com/posting-api/job-board/{company_slug}"),
        ("smartrecruiters", f"https://api.smartrecruiters.com/v1/companies/{company_slug}/postings"),
        ("rippling",        f"https://api.rippling.com/platform/api/ats/v1/board/{company_slug}/jobs"),
    ]
    for ats_name, url in endpoints:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return {"ats": ats_name, "slug": company_slug, "jobs": normalize_jobs(ats_name, r.json())}
    return {"ats": "unknown", "jobs": []}
```

ATS detection logic also exists in `scripts/find_career_urls.py` (broader, with Tavily fallback). `ats_probe.py` is the lightweight interactive version for single-company lookups.

---

## 12. Skill Gates

### Gate 1 — Mode Detection

```
What do you want to do?
a) Search for new jobs  (describe in plain language what you're looking for)
b) Analyze a specific JD  (paste URL or text)
c) Add context to an existing opportunity  (manual enrichment)
d) Record an outcome  (shortlisted / rejected / ghosted)
e) View / update pipeline
f) Probe ATS for a specific company
g) View your shortlist model report
```

### Gate 2 — Search Execution (mode=a)

1. Read user's natural language description
2. Interpret → derive params: search_terms, sectors, location, remote, hours_old, workday_search
3. Show interpretation to user: "Interpreted as: [params]. Run? (y/adjust)"
4. On confirm: run `jobspy_scrape.py` + `scrape_jobs.py` (Workday with derived searchText)
5. Run `score_jobs.py` on new results
6. Rank by `relevance_score`, filter by sector if specified
7. Present top 15 with: company, title, sector, score, location, URL

### Gate 3 — JD Analysis (mode=b)

1. Accept URL or pasted text
2. Fetch JD if URL provided
3. Run full signal extraction pipeline (Steps 1-4 from Section 6)
4. Compute Phase 1 score (sentence-transformers) immediately
5. Compute Phase 2 fit score if `jd_analyzer.py` available
6. Ask: "Any additional context about this company?" → manual enrichment if yes
7. Show: archetype, signals, scores, gap signals, red flags, recruiter language
8. Ask: save to pipeline?

### Gate 4 — Record Outcome (mode=d)

1. Show applications without outcomes (stage=applied/screening/etc., >14 days)
2. For each: "What happened?" → select outcome
3. Add brief notes (optional)
4. Update `memory/outcomes.json`
5. Show: "Model updated. [N] outcomes recorded. Confidence: [level]."

### Gate 5 — Pipeline View (mode=e)

1. Load `memory/pipeline.json`
2. Render by stage with days-in-stage
3. Flag: any application >14 days without outcome → "Record outcome?"
4. Show: opportunity scores + recommended next action per opportunity

---

## 13. Hard Rules

- **NEVER automate any LinkedIn account interaction** — account ban risk is severe
- **LinkedIn guest endpoint OK** — `linkedin.com/jobs-guest/` for job search only, no auth
- **NEVER apply on behalf of the user** — surface and score only; user applies manually
- **NEVER write to pipeline.json without showing user summary first**
- **ALWAYS preserve full JD text** — needed for resume tailoring downstream (linkright-sync)
- **ALWAYS show both scores separately** — never merge into one opaque score
- **ALWAYS explain score components** — "fit 82% because 4/5 primary signals matched"
- **NEVER claim the shortlist model is definitive** — probability signal, not a judgment
- **B2C hard requirement** — sector targeting excludes B2B tools (Shopify, Salesforce, HubSpot, N8N, etc.)

---

## 14. Scripts Reference

### Built ✅

| Script | Purpose | Location |
|---|---|---|
| `scrape_jobs.py` | Tier 1 ATS scraping (9 ATS types, 598 companies, limit 50) | `job scraping/scripts/` |
| `jobspy_scrape.py` | Tier 2 job board (LinkedIn guest + Indeed + Google + Naukri) | `job scraping/scripts/` |
| `filter_pm_jobs.py` | Title filtering, role_category, sector tagging, exclude irrelevant | `job scraping/scripts/` |
| `score_jobs.py` | Phase 1 semantic fit (sentence-transformers), ghost dedup | `job scraping/scripts/` |
| `import_browser_csv.py` | Import Tier 4 passive capture CSV | `job scraping/scripts/` |
| `update_excel.py` | Export jobs.db → Job Database.xlsx | `job scraping/scripts/` |
| `find_career_urls.py` | ATS detection for new companies | `job scraping/scripts/` |
| `validate_pipeline.py` | 3-gate URL validation | `job scraping/scripts/` |

### To Build ⏳

| Script | Purpose | Priority |
|---|---|---|
| `ats_probe.py` | Interactive: company name → ATS probe → live jobs | High |
| `jd_analyzer.py` | JD text → archetype + signal requirements + red flags + recruiter language | High |
| `fit_scorer.py` | JD signals + profile signals → Phase 2 fit score with breakdown | High |
| `pipeline_update.py` | CRUD on memory/pipeline.json (add, update stage, archive) | High |
| `shortlist_model.py` | outcomes.json + job features → shortlist probability | Medium |
| `tier3_search.py` | Remotive + RemoteOK + Adzuna + YC WaaS → normalized job list | Medium |
| `model_report.py` | outcomes.json → shortlist pattern analysis report | Medium |
| `internshala.py` | Playwright scraper for Internshala (Tier 5) | Low |
| `dedup.py` | Standalone dedup: URL match + fuzzy (company, title, date) | Low (inline dedup exists) |

---

## 15. References to Write

| File | Contents | Priority |
|---|---|---|
| `references/ref_01_portal_tiers.md` | Full portal tier guide: endpoints, auth, risk ratings, rate limits | High |
| `references/ref_02_signal_taxonomy.md` | Full signal taxonomy: all 4 tiers, definitions, archetype signal maps | High |
| `references/ref_03_jd_analysis.md` | JD parsing guide: signal extraction steps, recruiter language patterns, red flags | High |
| `references/ref_04_archetype_requirements.md` | 8 PM archetypes: required signals, seniority expectations, company stage fit | High |
| `references/ref_05_india_portals.md` | Internshala, Hirist, Naukri: Playwright configs, selectors, rate limits | Low |
| `references/ref_06_adaptive_model.md` | Full model design: feature vectors, weight update rules, confidence thresholds | Medium |

---

## 16. Build Checklist

### Data Layer (job scraping infrastructure)

- [x] `scrape_jobs.py` — limit 3→50, job_description field, 9 ATS types
- [x] `filter_pm_jobs.py` — role_category + sector + exclude irrelevant
- [x] `jobspy_scrape.py` — JobSpy multi-board with NL param args
- [x] `score_jobs.py` — sentence-transformers Phase 1 fit + ghost dedup
- [x] `docs/workflow.md` — updated with full architecture
- [x] `CLAUDE.md` — updated with all new scripts
- [ ] `scrape_jobs.py` — expand ATS types (add Rippling, Personio, iCIMS, JazzHR, Breezy via jobhive patterns)
- [ ] `tier3_search.py` — Remotive + RemoteOK + YC WaaS

### Skill Orchestration (linkright-hunt SKILL.md)

- [ ] Write SKILL.md (lean <400 lines, gate-based)
- [ ] Write `references/ref_01_portal_tiers.md`
- [ ] Write `references/ref_02_signal_taxonomy.md`
- [ ] Write `references/ref_03_jd_analysis.md`
- [ ] Write `references/ref_04_archetype_requirements.md`
- [ ] Build `ats_probe.py` — test against 10 known companies
- [ ] Build `jd_analyzer.py` — test against 5 diverse JDs
- [ ] Build `fit_scorer.py` — validate against manual scoring
- [ ] Build `pipeline_update.py`

### Adaptive Model (Phase 2+)

- [ ] Build `shortlist_model.py` — test with synthetic outcome data
- [ ] Build `model_report.py`
- [ ] Write `references/ref_06_adaptive_model.md`
- [ ] End-to-end outcome recording test

### Integration Tests

- [ ] Full run: `scrape_jobs.py` + `jobspy_scrape.py` → filter → score → top 20 output
- [ ] Single JD: paste JD → archetype detection → fit score → pipeline save
- [ ] Outcome recording: 3 outcomes → model confidence updates
- [ ] Cross-skill: save to pipeline.json → `linkright-sync` picks up JD → tailored resume

---

## 17. Success Criteria

- Batch discovery returns ≥50 relevant PM jobs per run across all sources
- Top 20 by relevance_score contain ≥15 genuinely relevant roles (manual check)
- ATS probe correctly identifies ATS for 8/10 known tech companies
- JD analysis extracts correct archetype for 9/10 test JDs
- Fit score correlates with manual assessment: ≥75%
- After 15 outcomes recorded: model report shows meaningful pattern
- Pipeline.json maintains full history with zero data loss
- Zero LinkedIn account automation — not even one authenticated request
- B2C sector filter working: gaming/career-nav/consumer-AI jobs tagged correctly
