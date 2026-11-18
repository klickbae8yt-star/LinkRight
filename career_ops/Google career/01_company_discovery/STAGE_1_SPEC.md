# Stage 1 Specification: Company Discovery & Curated Watchlist

**Status:** APPROVED DESIGN (Awaiting Claude Implementation)  
**Target Platform:** Oracle n8n (Plain HTTP Nodes) & Data Tables  
**Methodology:** Zero-Python, Direct API Reverse-Engineering (`api-anything` & `agent-reach` principles)

---

## 1. Architectural Principles & Constraints

1. **Direct Plain-HTTP APIs inside n8n:**
   * No heavy Python dependencies or virtual environments on the Oracle host for routine ingestion.
   * Every source is accessed via standard n8n **HTTP Request nodes** (GET/POST) returning structured JSON.
   * Where a platform lacks an official API, we apply `api-anything` / HAR capture to isolate the site's own internal REST endpoint (clean, cookie-free or long-lived header).
   * Social and founder funding signals leverage `agent-reach` HTTP extraction patterns.

2. **Fault Isolation:**
   * Each discovery source runs in an independent n8n sub-workflow or branch. If one source endpoint changes or is rate-limited, all other sources continue uninterrupted.

3. **Human-in-the-Loop Approval:**
   * Raw discoveries do not enter the active Job Search Watchlist automatically.
   * New candidates are placed in a **Candidate Staging Queue**. An interactive weekly digest (Telegram / n8n Review Form) lets you approve 10–20 high-conviction companies per week into the permanent Watchlist.

---

## 2. Company Qualification & Scoring Model

Every discovered company receives a composite Score (0 to 100) based on three explicit dimensions: **Stage Tier**, **Geographic Flexibility**, and **Domain Focus**, supplemented by a **Native AI Gate**.

### Dimension A: Company Stage Tier (Weight: 35%)
* **Tier 1 (Highest Priority - Score 100):** Early-stage funded startups (**Seed, Series A, Series B**). Fast-moving teams with high equity upside and direct founder ownership.
* **Tier 2 (Priority 2 - Score 75):** High-growth tech unicorns (e.g., Deel, Scale AI, Stripe, Supabase, ElevenLabs).
* **Tier 3 (Priority 3 - Score 50):** Big Tech / FAANG tier (Google, Amazon, Meta, Apple).

### Dimension B: Geographic Work Mode (Weight: 35%)
* **Geo P1 (Score 100):** Fully remote global companies that hire in India / anywhere.
* **Geo P2 (Score 80):** Overseas hubs in **Dubai, UK, or Europe** (viable for relocation or international remote contracting).
* **Geo P3 (Score 65):** Active India presence with Hybrid/On-site requirements in primary hubs:
  * Bengaluru, Gurgaon / Delhi NCR, Hyderabad, Mumbai, Pune.
* **Hard Knockout (Score 0 / Auto-Reject):** Strict domestic US/Canada-only hiring with zero international or remote flexibility.

### Dimension C: Domain & Sector Priority (Weight: 30%)
* **Domain 1 (Top Fit - Score 100):** **AI & Automation / Generative Media Products**
  * Practical, tangible tools used by real end-users (AI video editing, image generation, audio/voice synthesis, consumer/prosumer creative AI). B2C or B2B.
* **Domain 2 (Score 85):** **AI Sales, Marketing & GTM Tech**
  * Automated outreach, prospecting, intelligence, conversion optimization (B2B & B2C).
* **Domain 3 (Score 75):** **Hiring, HR & Recruitment Tech**
  * Modern talent platforms, sourcing automation, ATS innovations.
* **Domain 4 (Score 60):** **Any B2B Industry** (provided it has an active AI-native focus).
* **Domain Exclusions:** None. All sectors are eligible if they fit the AI and stage criteria.

---

## 3. The "Native AI Involvement" Filter

A dedicated boolean classifier that distinguishes genuine AI opportunities from legacy roles using AI as marketing buzzwords:

| Flag | Definition | Criteria |
|---|---|---|
| `is_ai_native: true` | The core product *is* AI, or the role directly drives AI model integration, prompt evaluation, agentic workflows, or synthetic media. | Company's primary value proposition is AI-driven, or JD specifies direct AI tooling/model ownership. |
| `is_ai_native: false` | Traditional software/e-commerce/ops company that only mentions AI in passing as a generic buzzword. | Traditional workflow with zero generative or agentic product ownership. |

*In Stage 2/3, jobs flagged with `is_ai_native: true` receive a significant ranking boost.*

---

## 4. Discovery Sources & Direct API Mappings

All sources use direct HTTP calls inside n8n:

1. **Y Combinator (YC API):**
   * *Method:* Direct Algolia search JSON endpoint (`https://hn.algolia.com/api/v1/` and YC directory public endpoints).
   * *Payload:* Filters by recent batches (`W24`, `S24`, `W25`, `S25`), funded status, and remote-friendly tags.
2. **Hacker News "Who is Hiring" (Firebase REST API):**
   * *Method:* Plain GET to `https://hacker-news.firebaseio.com/v0/item/{id}.json`. Zero authentication, pure JSON.
   * *Signal:* Founder and team lead direct hiring posts on the 1st of every month.
3. **Early-Stage Venture Announcements (TechCrunch & Inc42 Feeds):**
   * *Method:* Direct RSS-to-JSON HTTP endpoints parsing recent Seed/Series A funding announcements in India, UK, Dubai, and Global Remote.
4. **Peak XV Surge & Antler Portfolios:**
   * *Method:* Clean REST endpoint extracted via `api-anything` capturing portfolio listings with stage, founders, and career URLs.
5. **Founder / Signal Tracking via `agent-reach`:**
   * *Method:* Twitter/X & social tracking patterns to catch unannounced stealth rounds and founder hiring announcements.

---

## 5. End-to-End Workflow & Data Model

```
[Cron: Weekly Sunday 18:00 UTC]
           │
           ▼
[Fetch Sources via HTTP Request Nodes (YC, HN, Feeds, Surge)]
           │
           ▼
[Deduplicate against master_list.json / Data Table]
           │
           ▼
[Calculate Company Score (0-100) + Detect ATS (Ashby/Greenhouse/Lever)]
           │
           ▼
[Filter: Score >= 60 & Not Knocked Out]
           │
           ▼
[Staging Table: `stage1_candidates`]
           │
           ▼
[Send Weekly Review Card to Telegram with Approve / Reject Buttons]
           │
     ┌─────┴─────┐
     ▼           ▼
 [Approved]   [Rejected]
     │           │
     ▼           ▼
[Active Watchlist] [Archived]
(Feeds Stage 2 Job Search)
```

### Staged Candidate Record Schema
```json
{
  "company_id": "elevenlabs",
  "name": "ElevenLabs",
  "website": "https://elevenlabs.io",
  "careers_url": "https://jobs.ashbyhq.com/elevenlabs",
  "ats_provider": "ashby",
  "stage": "Series B",
  "tier": 1,
  "headquarters": "London / New York",
  "work_mode": "remote_global",
  "sectors": ["ai_automation", "voice_synthetic_media"],
  "is_ai_native": true,
  "composite_score": 96,
  "source": "techcrunch_funding",
  "discovered_date": "2026-11-12",
  "status": "pending_approval"
}
```

---

## 6. Acceptance Criteria for Claude Build

1. **Zero Python on Host:** Ingestion workflow runs 100% inside n8n using native HTTP Request and Code nodes.
2. **Exact Scoring Fidelity:** Accurately calculates weights across Stage, Work Mode, and Sector.
3. **No US-Only Leaks:** Companies with zero remote or international flexibility are dropped at ingestion.
4. **Interactive Approval:** 10–20 high-scoring candidates presented weekly with one-tap approval into `watchlist`.

