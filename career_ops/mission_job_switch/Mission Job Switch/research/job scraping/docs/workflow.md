# Job Discovery Pipeline — Master Reference

---

## Product Vision

Build a one-time comprehensive scrape + ongoing daily feed of PM-adjacent job openings across 598+ target companies, filtered to roles matching Satvik's transferable skillset, scored by semantic relevance to his profile, and exported to Excel for daily review.

**Success criteria:**
- 500–1000 relevant jobs captured in first run
- Each job has: title, company, location, JD, compensation, YoE, posted_at, URL
- Each job tagged with: `role_category` (PM/Growth/CSM/etc.) + `sector` (B2C vertical)
- Jobs ranked by `relevance_score` (semantic match to profile, not keyword count)
- Ghost jobs detected and suppressed
- Daily refresh runnable in < 10 minutes

**Target job seeker profile:** IIT Delhi → Sprinklr (GenAI analytics PM, 2 yrs) → Amex (AML platform PM, present) → LinkRight (AI career OS, solo founder). Strong in: AI/LLM products, fintech/compliance, B2C consumer, enterprise SaaS, social media analytics.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      COLLECTION LAYER                       │
├──────────────────┬──────────────────┬───────────────────────┤
│  Track A         │  Track B         │  Track C              │
│  JobSpy          │  ATS APIs        │  Passive Browser      │
│                  │                  │                       │
│  LinkedIn        │  20 ATS types:   │  Tampermonkey         │
│  Indeed India    │  Greenhouse      │  passive_job_capture  │
│  Google Jobs     │  Lever           │  .js                  │
│  Naukri          │  Ashby           │                       │
│                  │  Workday         │  Manual browsing       │
│  Keyword search  │  Workable        │  = backup / gap fill  │
│  across all      │  SmartRecruiters │                       │
│  boards at once  │  + 14 more       │                       │
│                  │  (iCIMS, JazzHR, │                       │
│                  │  Personio, etc.) │                       │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         └──────────────────┴────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    FILTER LAYER                             │
│                                                             │
│  classify_title()  → role_category (PM/Growth/CSM/etc.)    │
│  is_excluded()     → DELETE (engineers/HR/sales/etc.)      │
│  detect_sector()   → B2C sector tag                        │
│                       CAREER_NAV_B2C                       │
│                       CONSUMER_AI                          │
│                       SOCIAL_COMMERCE                      │
│                       GAMING                               │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    SCORING LAYER                            │
│                                                             │
│  sentence-transformers (all-MiniLM-L6-v2)                  │
│  Free. Local. ~14ms/job on CPU. No API cost.               │
│                                                             │
│  1. Embed Satvik's career profile ONCE → profile.npy       │
│  2. Per job: embed (title + description snippet)           │
│  3. cosine_similarity(job_vec, profile_vec) → 0.0–1.0      │
│  4. relevance_score = round(similarity × 100)              │
│  5. Ghost dedup: if sim > 0.95 vs existing job → skip      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      jobs.db (SQLite)                       │
│                                                             │
│  All metadata: role_category, sector, relevance_score,     │
│  compensation, years_experience, is_remote, is_ghost        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              Job Database.xlsx  (update_excel.py)           │
│  Filter: sector=CAREER_NAV_B2C, role_category=PM           │
│  Sort: relevance_score DESC, posted_at DESC                │
└─────────────────────────────────────────────────────────────┘
```

---

## Target Roles (INCLUDE rules)

Reverse-filter strategy: keep uncertain titles, only delete clear exclusions.

| Category | Example titles |
|---|---|
| `PM` | product manager, product owner, head of product, vp product, director of product |
| `AI_PM` | ai product manager, ai builder, llm product, generative ai product, ai solutions |
| `GROWTH` | growth manager, growth product manager, growth lead, head of growth, growth pm |
| `PMM` | product marketing manager, pmm, go-to-market manager, gtm manager |
| `ANALYTICS_PM` | product analyst, data product manager, analytics product manager |
| `CSM` | customer success manager, customer success lead, director customer success |
| `IMPLEMENTATION` | implementation manager, solutions architect, technical account manager, onboarding manager |
| `FINTECH_PM` | compliance product, risk product, payments product, aml product, fraud product |
| `FOUNDING` | founding pm, founding product, chief of staff |
| `TPM` | technical program manager, program manager, delivery manager |
| `GENERAL_PM` | product specialist, product strategist, product operations, product consultant |

**EXCLUDE (delete if title matches + no INCLUDE signal):** software engineer, data scientist, ml engineer, ux designer, account executive, recruiter, accountant, copywriter, devops engineer, qa engineer, intern, warehouse, etc. Full list in `scripts/filter_pm_jobs.py:EXCLUDE_KEYWORDS`.

---

## Target Sectors (B2C filter)

Hard requirement: **B2C only** — consumer-facing products, not B2B SaaS tools.

```python
SECTOR_COMPANIES = {
    "CAREER_NAV_B2C": [
        # Job seeker-facing: user IS the product consumer
        "linkedin", "glassdoor", "handshake", "unstop", "internshala",
        "apna", "foundit", "topmate", "superpeer", "cutshort", "hirist",
        "rezi", "kickresume", "enhancv", "pramp", "exponent",
    ],
    "CONSUMER_AI": [
        # Direct-to-consumer AI products
        "perplexity", "character.ai", "character ai", "notion",
        "superhuman", "motion", "reclaim", "otter",
        "sarvam", "krutrim", "setu", "frammer", "leher",
        "sharechat", "moj", "josh", "locket",
        "openai", "anthropic", "cohere", "mistral",
    ],
    "SOCIAL_COMMERCE": [
        # Consumer shopping / social selling
        "meesho", "glowroad", "shop101", "whatnot", "temu",
        "tiktok", "pinterest",
    ],
    "GAMING": [
        # Consumer gaming — all B2C
        "dream11", "mpl", "mobile premier league", "nazara", "winzo",
        "games24x7", "gameskraft", "krafton", "ncore", "supergaming",
        "junglee games", "playtika", "zynga", "electronic arts",
        "riot", "scopely", "unity", "epic games",
    ],
}
```

Note: Dropshipping tools (Shopify, DSers, AutoDS), cold email tools (Instantly, Lemlist, Apollo), and N8N/Zapier are **B2B** — excluded from sector targeting.

---

## DB Schema

```sql
CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT UNIQUE,
    segment TEXT,
    career_url TEXT,
    portal_type TEXT,
    verified INTEGER DEFAULT 0,
    verified_url TEXT,
    jobs_found INTEGER DEFAULT 0,
    error TEXT,
    checked_at TEXT
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    company_id INTEGER,
    segment TEXT,
    portal_type TEXT,
    title TEXT,
    department TEXT,
    location TEXT,
    job_url TEXT,
    posted_at TEXT,
    scraped_at TEXT,
    source_portal TEXT,        -- 'jobspy_linkedin' | 'jobspy_indeed' | 'ats_greenhouse' | 'browser_csv' etc.
    scraped_url TEXT,
    -- enrichment columns (added by filter_pm_jobs.py ensure_columns)
    job_description TEXT,
    compensation TEXT,
    years_experience TEXT,
    employment_type TEXT,
    is_remote INTEGER DEFAULT 0,
    -- classification columns
    role_category TEXT,        -- PM | AI_PM | GROWTH | PMM | CSM | IMPLEMENTATION | FINTECH_PM | FOUNDING | TPM | GENERAL_PM | UNCERTAIN
    sector TEXT,               -- CAREER_NAV_B2C | CONSUMER_AI | SOCIAL_COMMERCE | GAMING | NULL
    -- scoring column
    relevance_score REAL,      -- 0.0–100.0, cosine similarity × 100 vs Satvik's profile
    is_ghost INTEGER DEFAULT 0 -- 1 if duplicate/reposted detected via semantic similarity
);
```

---

## Scripts Reference

| Script | Purpose | Status |
|--------|---------|--------|
| `find_career_urls.py` | Step 1: discover career URLs for new companies | EXISTS |
| `classify_career_urls.py` | Step 2: classify ATS portal type | EXISTS |
| `verify_urls.py` | Step 3: HTTP verification | EXISTS |
| `validate_pipeline.py` | Step 3b: 3-gate validation (HTTP + ATS API + Workday) | EXISTS |
| `scrape_jobs.py` | Step 4B: ATS API scraping (20 types, 598 companies) | EXISTS — needs limit 3→50 + description field |
| `filter_pm_jobs.py` | Step 4 post: clean DB, assign role_category | EXISTS — DONE |
| `import_browser_csv.py` | Step 4C: import Tampermonkey CSV | EXISTS |
| `jobspy_scrape.py` | Step 4A: job board scraping via JobSpy | **TO BUILD** |
| `score_jobs.py` | Step 4.5: semantic scoring + ghost dedup | **TO BUILD** |
| `update_excel.py` | Step 5: refresh Job Database.xlsx | EXISTS |
| `analyze_html.py` | Utility: find CSS selectors in saved HTML | EXISTS |
| `process_next300.py` | Utility: batch-process new companies into DB | EXISTS |

### Browser snippets

| File | Purpose |
|------|---------|
| `browser_snippets/passive_job_capture.js` | v1.5 — Tampermonkey script, captures job pages during normal browsing, exports CSV |
| `browser_snippets/README.md` | Install + usage instructions for passive capture |

---

## Execution Order

### One-time full scrape (first run)

```bash
# 0. Clean existing 224 jobs — assign role_category, delete irrelevant
python3 scripts/filter_pm_jobs.py

# 1. ATS companies (111 companies, ~10 min)
#    Requires: scrape_jobs.py updated with limit=50 + description capture
python3 scripts/scrape_jobs.py

# 2. Job boards — LinkedIn/Indeed/Google/Naukri simultaneously (~5 min)
#    Install first: pip install python-jobspy
python3 scripts/jobspy_scrape.py

# 3. Semantic scoring — score all jobs, detect ghost reposts (~2 min for 1000 jobs)
#    Install first: pip install sentence-transformers
python3 scripts/score_jobs.py

# 4. Export to Excel
python3 scripts/update_excel.py
```

### Daily refresh (ongoing)

```bash
# jobspy_scrape.py uses hours_old=24 for first-run freshness
# scrape_jobs.py re-runs ATS (always returns current open jobs, no staleness)
python3 scripts/jobspy_scrape.py && python3 scripts/scrape_jobs.py
python3 scripts/score_jobs.py
python3 scripts/update_excel.py
```

---

## Stage 1 — Company Discovery

### What this stage does

Find company names not yet tracked. Goal: get name into list so Stages 2–5 run automatically. No URLs needed — pipeline finds those.

### Sources to use

**India MNCs & High-Growth Tech**
- [Inc42](https://inc42.com) — India startup news, funding tracker, unicorn list
- [YourStory](https://yourstory.com/companies) — India startup stories
- [Tracxn](https://tracxn.com/explore/startups/india) — India company explorer
- VC portfolio pages: Sequoia India, Accel India, Matrix Partners India, Elevation Capital, Lightspeed India, Kalaari Capital
- Nasscom top product companies list

**Consumer AI Startups — Global**
- [YC Companies](https://ycombinator.com/companies) — filter by AI/ML, 2022–2025 batches
- [Product Hunt](https://producthunt.com) — trending AI products, Product of the Day
- [a16z Portfolio](https://a16z.com/portfolio) — filter by AI
- CB Insights AI 100 / Top AI Startups reports
- TechCrunch AI coverage, Crunchbase AI trending
- [Wellfound (AngelList)](https://wellfound.com/startups) — filter by AI

**Dubai Visa Sponsors**
- [Magnitt](https://magnitt.com) — MENA startup ecosystem, funding rounds
- [Wamda](https://wamda.com) — Arab world startup news
- [ArabNet](https://arabnet.me) — Arab digital economy
- VC portfolio pages: BECO Capital, Wamda Capital, STV (Saudi), Mubadala Ventures, Global Ventures
- GITEX Tech Week and STEP Conference exhibitor lists

### How to run Discovery in Gemini

1. Open Gemini Deep Research (`gemini.google.com` → Deep Research mode)
2. Upload `Job Database.xlsx` as attachment
3. Paste prompt below, fill in `{SEGMENT}`
4. Collect output → give to Claude: *"New companies from discovery batch [N]. Run pipeline on these."*

### Discovery Prompt

```
You are a startup ecosystem researcher.

I have uploaded my company tracking file (Job Database.xlsx).
It has 3 sheets: "Big Tech & MNCs - India", "Consumer AI Startups - Global", "Dubai - Visa Sponsors".

TASK: Find 20–30 companies for this segment that are NOT already in the Excel.

SEGMENT: {SEGMENT}
Use one of: "India MNCs & High-Growth Tech" | "Consumer AI Startups - Global" | "Dubai Visa Sponsors"

WHERE TO LOOK (search these sources first):
{SOURCES_FOR_SEGMENT}

FILTERS:
- Company must be active (not shut down in last 12 months)
- Must have real product-building (not pure IT services, BPO, or staffing)
- For Dubai segment: must be known to hire international talent (not UAE-nationals-only)
- For India: must have real product ownership in India, not just delivery center
- For AI segment: must have a consumer-facing product (not pure API/infra)

OUTPUT FORMAT — simple markdown table, exactly these 4 columns:
| Company Name | Segment | What They Do (1 line) | Source |

No career URLs needed. No funding details needed. Just the company name, segment, one-line description, and where you found it.

Read all company names from the Excel first and exclude any that already appear there.
Provide exactly 20–30 companies. Do not pad with well-known companies I definitely already have.
```

---

### Segment Sources (fill into prompt above)

**India MNCs & High-Growth Tech:**
```
NEWS & TRACKERS
- Inc42 unicorn/soonicorn tracker, funding rounds, startup news (inc42.com)
- YourStory company directory and funding coverage (yourstory.com/companies)
- Entrackr — India funding news and startup intelligence (entrackr.com)
- Economic Times Startup (economictimes.com/tech/startups)
- Mint Startup pages (livemint.com)
- Moneycontrol startup/tech coverage

DIRECTORIES & RANKINGS
- NASSCOM Top 100 Product Companies list (nasscom.in)
- LinkedIn Top Startups India (annual list, search on LinkedIn)
- Forbes India 30 Under 30 / Forbes India startup coverage
- Hurun India Unicorn Index
- Crunchbase India companies filter (crunchbase.com, filter: India, Series A–D)
- Tracxn India startup explorer (tracxn.com/explore/startups/india)
- Startup India government portal (startupindia.gov.in)

VC PORTFOLIO PAGES (search "[VC name] portfolio" on Google)
- Peak XV Partners (formerly Sequoia India) — peakxv.com/portfolio
- Accel India — accel.com/companies (filter India)
- Elevation Capital — elevationcapital.com/portfolio
- Matrix Partners India (now Z47) — z47.com/portfolio
- Lightspeed India — lsvp.com/portfolio (filter India)
- Kalaari Capital — kalaari.com/portfolio
- Blume Ventures — blume.vc/portfolio
- 3one4 Capital — 3one4capital.com/portfolio
- Nexus Venture Partners — nexusvp.com/portfolio
- Chiratae Ventures — chiratae.com/portfolio
- Info Edge Ventures — infoedgeventures.com/portfolio
- BEENEXT — beenext.com/portfolio
- Stellaris Venture Partners — stellarisvp.com/portfolio
- IndiaQuotient — indiaquotient.in/portfolio
- Fundamentum Partnership — fundamentum.vc/portfolio
```

**Consumer AI Startups — Global:**
```
YC & ACCELERATORS
- YC W23/S23/W24/S24/W25 batches filtered by AI/ML (ycombinator.com/companies — filter tag: AI)
- AI Grant portfolio (aigrant.com)
- OpenAI Converge cohort companies
- Google for Startups AI cohort
- Microsoft for Startups AI companies

MAJOR VC PORTFOLIO PAGES
- a16z (Andreessen Horowitz) — a16z.com/portfolio (filter AI)
- Sequoia US — sequoiacap.com/companies (filter AI)
- Khosla Ventures — khoslaventures.com/portfolio
- Lightspeed Venture Partners — lsvp.com/portfolio
- General Catalyst — generalcatalyst.com/companies
- Greylock — greylock.com/portfolio
- Benchmark — benchmark.com/companies
- Index Ventures — indexventures.com/portfolio
- Founders Fund — foundersfund.com/portfolio
- Coatue Management — coatue.com/portfolio
- Accel US — accel.com/companies (filter US/global)
- Bessemer Venture Partners — bvp.com/portfolio
- NEA — nea.com/companies
- GV (Google Ventures) — gv.com/portfolio
- First Round Capital — firstround.com/companies

MEDIA & RANKINGS
- Forbes AI 50 list (annual, search "Forbes AI 50 2025")
- TIME 100 AI Companies (time.com/collection/time100-ai)
- Fast Company Most Innovative Companies — AI category
- CB Insights AI 100 report
- MIT Technology Review 50 Smartest Companies — AI picks

DISCOVERY PORTALS
- Product Hunt — top AI products last 90 days (producthunt.com, filter AI)
- There's An AI For That directory (theresanaiforthat.com)
- Futurepedia (futurepedia.io) — AI tools directory
- Wellfound (AngelList) AI startups 10–500 employees (wellfound.com/startups)
- Crunchbase AI companies, funded in last 18 months

NEWSLETTERS
- Ben's Bites (bensbites.co)
- The Rundown AI (therundown.ai)
- TLDR AI (tldr.tech/ai)
- Lenny's Newsletter startup coverage
```

**Dubai Visa Sponsors:**
```
NEWS & TRACKERS
- Magnitt MENA startup radar, funding rounds (magnitt.com)
- Wamda — Arab world startup news (wamda.com)
- ArabNet Digital Summit coverage (arabnet.me)
- Entrepreneur Middle East (entrepreneurshiphq.com/middle-east)
- Arabian Business tech coverage (arabianbusiness.com)
- Gulf Business technology news (gulfbusiness.com)
- Forbes Middle East startup lists (forbesmiddleeast.com)
- Zawya tech coverage (zawya.com)
- Fintech Galaxy — MENA fintech directory (fintechgalaxy.com)

VC PORTFOLIO PAGES
- BECO Capital — becocapital.com/portfolio
- Wamda Capital — wamdacapital.com/portfolio
- Global Ventures — globalventures.vc/portfolio
- STV (Saudi Telecom Ventures) — stv.vc/portfolio
- Mubadala Ventures — mubadalaventures.com/portfolio
- DisruptAD (Abu Dhabi) — disruptad.com/portfolio
- 500 Global MENA — 500.co/portfolio (filter MENA)
- Nuwa Capital — nuwacapital.com/portfolio
- Shorooq Partners — shorooq.com/portfolio
- Algebra Ventures — algebraventures.com/portfolio
- Flat6Labs MENA — flat6labs.com/portfolio

GOVERNMENT & ECOSYSTEM HUBS
- Hub71 portfolio companies (Abu Dhabi AI hub) — hub71.com/portfolio
- Dubai Future Accelerators cohort companies — dubaifuture.ae
- DIFC Fintech Hive companies — difcfintechhive.ae
- Dubai Internet City tenant companies — dubaiinternetcity.com
- In5 Tech (in5.ae) — Dubai startup incubator portfolio
- ADGM (Abu Dhabi Global Market) fintech companies

EVENTS
- GITEX Tech Week exhibitors (gitex.com)
- STEP Conference Dubai speakers/exhibitors (stepconference.com)
- AIM Congress Abu Dhabi exhibitors (aimcongress.com)
```

---

## Stage 2 — Career URL Discovery

**Input:** Company names from Stage 1
**Output:** `db/career_urls_result.json` — each company with `career_url` + `portal_type`

```bash
python3 scripts/process_next_batch.py
```

The script:
1. Builds URL candidates (careers.X / jobs.X / X/careers etc.)
2. Checks HTTP reachability with curl_cffi (chrome136 TLS)
3. For ATS patterns (Greenhouse/Lever/Ashby) → verifies via public API, not HTML
4. Falls back to Tavily search only if all pattern guesses fail (last resort — free tier limited)

---

## Stage 3 — Validation

**Input:** `db/career_urls_result.json`
**Output:** `db/jobs.db` — `validation_status` + `validation_reason` per company

```bash
python3 scripts/validate_pipeline.py
```

3-gate system:
1. **Gate HTTP** — reachability + homepage redirect detection
2. **Gate ATS Board** — Greenhouse/Lever/Ashby API confirms board exists
3. **Gate Workday** — override map + geo-block classification

Status values:
- `PASS` — URL verified, career page confirmed real
- `GEO_BLOCKED` — Workday URL correct, blocked from India IP
- `ANTI_BOT_INDIA` — bot detection from India IP
- `FAIL_HTTP` — URL wrong, dead, or redirects to homepage

---

## Stage 4 — Job Scraping

Three parallel tracks. Run all three for maximum coverage.

### Track A — JobSpy (job boards)

Scrapes LinkedIn, Indeed India, Google Jobs, Naukri simultaneously via keyword search.

```bash
pip install python-jobspy  # one-time install
python3 scripts/jobspy_scrape.py
```

**How it works:**
- Loops through 15 PM search terms
- Each term hits all 4 job boards concurrently
- `hours_old=168` first run (7 days backfill), `hours_old=24` daily
- `results_wanted=50` per term per site = up to 3000 raw jobs
- Filters via `classify_title()` → drops irrelevant → tags `sector`
- Deduplicates against existing DB by `job_url`
- Inserts with `source_portal='jobspy_{site}'`

**Search terms used:**
```python
SEARCH_TERMS = [
    "product manager", "senior product manager", "AI product manager",
    "growth manager", "growth product manager",
    "product marketing manager",
    "customer success manager",
    "implementation manager", "solutions architect",
    "technical program manager",
    "founding product manager",
    "product analyst", "data product manager",
    "chief of staff",
    "product owner",
]
```

### Track B — ATS APIs

Direct API scraping of all 598 companies via their ATS platforms. Zero rate limits (ATS APIs are designed to syndicate jobs outward). Cleanest data — straight from source.

```bash
python3 scripts/scrape_jobs.py
```

Supported ATS types (20):
Greenhouse, Lever, Ashby, Workday, Workable, SmartRecruiters, Eightfold, BambooHR, Teamtailor, Rippling, Personio, iCIMS, JazzHR, Breezy, Pinpoint, Cornerstone, Recruitee, Oracle, SuccessFactors, Taleo

Note: `scrape_browser_jobs.py` and `scrape_static_jobs.py` are **no longer needed**. JobSpy covers what they would have done for job board companies. The agent-browser pipeline (6 hours planned) is replaced by Track A (5 minutes).

### Track C — Passive Browser Capture

Manual backup. Use when job is found on an authenticated/login-gated page that JobSpy or ATS APIs can't reach.

1. Install Tampermonkey → paste `browser_snippets/passive_job_capture.js`
2. Browse job pages normally
3. Badge counts captures; click → Download CSV
4. Import: `python3 scripts/import_browser_csv.py ~/Downloads/jobs_passive_*.csv`

---

## Stage 4.5 — Filtering & Classification

Runs automatically inside Track A and Track B. Also runs standalone to clean existing DB.

```bash
python3 scripts/filter_pm_jobs.py  # standalone clean + categorize
```

What it does:
- `classify_title(title)` → assigns `role_category` (PM / AI_PM / GROWTH / etc.)
- `is_excluded(title)` → marks for deletion (engineers, HR, sales, interns, etc.)
- `detect_sector(company)` → assigns `sector` (CAREER_NAV_B2C / CONSUMER_AI / GAMING / etc.)
- `--dry-run` flag: print without writing

---

## Stage 4.6 — Semantic Scoring

Scores all jobs by cosine similarity to Satvik's career profile. Detects ghost reposts.

```bash
pip install sentence-transformers  # one-time install
python3 scripts/score_jobs.py
```

What it does:
1. Loads profile text from `db/profile_embedding.npy` (generated on first run from career profile)
2. For each unscored job: embeds `title + " " + description[:500]` via `all-MiniLM-L6-v2`
3. Computes cosine similarity vs profile vector
4. Sets `relevance_score = similarity × 100` (0–100)
5. Ghost detection: if similarity > 0.95 vs any existing job → sets `is_ghost=1`, skips
6. Runs incrementally — only scores jobs where `relevance_score IS NULL`

**Why better than keyword scoring:**
- Saiyam's script: counts keyword occurrences → `score = 4` if "aws" appears 4x
- This: semantic intent match → "LLM-powered analytics PM" matches "GenAI root-cause engine" even with zero keyword overlap

---

## Stage 5 — Excel Sync

```bash
python3 scripts/update_excel.py
```

Refreshes `Job Database.xlsx`. Includes all new jobs with `role_category`, `sector`, `relevance_score` columns. Sort in Excel by `relevance_score DESC` to see best matches first.

---

## URL Correction (for failed companies)

When Stage 3 marks companies `FAIL_HTTP`, use Gemini to find correct URLs. Broken list at `db/failed_companies_for_gemini.md`.

### Correction Prompt for Gemini

```
I have a list of companies whose career portal URLs are broken.
For each company, find the correct current career URL using web search.

Some companies may have:
- Moved careers page to a new path or ATS
- Shut down (mark as "Company_Shut_Down")
- Rebranded (note the new name)

Return a markdown table:
| Company | Correct Career URL | Portal Type | Notes |

Portal Type: ATS_Greenhouse / ATS_Lever / ATS_Ashby / ATS_Workday /
ATS_Workable / ATS_SmartRecruiters / Tier2_CSR_SPA / Tier1_StaticHTML / Company_Shut_Down

[PASTE db/failed_companies_for_gemini.md content here]
```

After Gemini returns, tell Claude:
> "Here are the corrected URLs from Gemini. Update the database and re-run validation."

---

## Files Reference

| File | Purpose |
|------|---------|
| `Job Database.xlsx` | Authoritative input — 598+ companies, 3 sheets. Also final output. |
| `db/career_urls_result.json` | Career URLs (598 entries, growing) with portal_type |
| `db/jobs.db` | SQLite — companies + jobs tables with all metadata |
| `db/profile_embedding.npy` | Satvik's profile encoded as numpy vector (generated by score_jobs.py) |
| `db/failed_companies_for_gemini.md` | Companies needing URL correction |
| `db/quarantine.json` | FAIL entries with reasons |
| `docs/workflow.md` | This file — master reference |
| `docs/bug_log.md` | Pipeline bugs found + fixes applied |
| `research/` | LLM deep research outputs — read-only reference |

---

## Open-Source Reference (what we borrowed)

| Project | What we took |
|---|---|
| `speedyapply/JobSpy` | Track A — job board scraping. `pip install python-jobspy`. |
| `kalil0321/ats-scrapers` (jobhive) | ATS type patterns for iCIMS, Personio, JazzHR, Breezy, Rippling, Cornerstone, Recruitee, Pinpoint, Oracle, SuccessFactors, Taleo |
| `saiyam-gupta/job-spy-enhanced-script` | Search term loop pattern, senior title exclusion pattern, export structure |
| `vasu-devs/JustHireMe` | Ghost job detection concept (cosine similarity > threshold → repost) |
| `santifer/career-ops` | A-F semantic scoring concept (implemented locally via sentence-transformers, no API cost) |

**Deliberately NOT used:**
- Career-ops Playwright + Claude API per job: too expensive per-run
- Serai Notion + Brave Search: overkill integration overhead
- JustHireMe Tauri desktop app: wrong form factor
- agent-browser loop for 478 companies: replaced by JobSpy (5 min vs 6 hours)

---

## Improvement Backlog

### Resolved by new architecture ✅

| Item | Resolution |
|---|---|
| Tier1_StaticHTML + Tier2_CSR_SPA browser scraping (448 cos, 0 jobs) | JobSpy covers these companies via job board search |
| Naukri.com scraping | JobSpy supports Naukri natively |
| Google Jobs scraping | JobSpy supports Google Jobs natively |
| BambooHR support | Added to scrape_jobs.py ATS types |
| Missing ATS types (iCIMS, Recruitee, JazzHR, etc.) | Added via jobhive patterns |
| chrome124 → chrome136 upgrade | scrape_jobs.py uses chrome136 |

### Pending ⏳

**High priority:**
- `scrape_jobs.py` — increase limit 3→50 per company
- `scrape_jobs.py` — capture `job_description` from all ATS scrapers (Greenhouse `content` field, Lever `descriptionPlain`, Ashby `descriptionHtml`, Workday description endpoint)
- Build `scripts/jobspy_scrape.py`
- Build `scripts/score_jobs.py`

**Medium priority:**
- Y Combinator Work at a Startup API — `workatastartup.com/jobs?role=product` (free, no auth)
- Wellfound jobs API — startup-focused, filterable by role/stage
- Remotive API — `remotive.com/api/remote-jobs?category=product` (free, no auth, remote-only)
- RemoteOK API — `remoteok.com/api?tags=product-manager` (free, no auth)
- HackerNews "Who's Hiring" monthly thread — via Algolia HN API

**Low priority:**
- Recruiterflow API reverse-engineering (CoinSwitch)
- JazzHR partner API (requires API key per account — low feasibility)
- Periodic re-scrape daemon (cron or n8n — design when needed)
- HTML dashboard for viewing jobs.db in browser
