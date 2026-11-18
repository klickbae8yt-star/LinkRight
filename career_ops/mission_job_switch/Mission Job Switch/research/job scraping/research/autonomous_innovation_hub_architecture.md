# Autonomous Innovation Hub — Job Aggregation Engine
## Production Architecture Blueprint v1.0
**Last updated:** 2026-05-21  
**Context:** Personal job-switch intelligence layer. Aggregates 100-company target list across 3 tracks (India MNCs, Global AI Startups, Dubai Visa Sponsors).

---

## ROLE CONTEXT
Principal Data Acquisition Architect — designing a distributed, infinite-scale, centralized job aggregation engine.  
**Philosophy:** Efficiency-First, Low-Overhead. Prefer n8n orchestration + free-tier cloud over custom infrastructure. Zero brute-force headless rendering unless unavoidable.

---

## ARCHITECTURE DECISION LOG

| Decision | Choice | Reason |
|---|---|---|
| Orchestration | n8n (self-hosted or cloud) | Event-driven, visual, free-tier viable |
| State store | Redis + Bloom Filter | O(1) dedup check, ~10KB per 10K URLs |
| Headless engine | rebrowser-playwright (only when needed) | Memory-isolated context recycling; fixes CDP leak |
| HTTP client (Tier 3) | curl_cffi (Chrome 124-146) | Replaces tls-client (dead); BoringSSL TLS spoofing |
| Dedup layer | SHA-256 hash + cosine similarity | Exact + semantic collision coverage |
| LLM parsing | GPT-4o-mini / Gemini Flash via structured output | Cost-efficient entity extraction |
| Schema store | PostgreSQL (Supabase free tier) | Relational + JSON + pgvector (HNSW, ~50k 384-dim free) |
| Embeddings | External FastAPI microservice (all-MiniLM-L6-v2) | n8n Code Node can't run sentence-transformers on Cloud |

---

## 1. DATA DELIVERY TAXONOMY

### 1.1 Static HTML Portals (SSR/SSG/Legacy Tables)

**Detection signal:** Full job content present in `curl` response body with no JS execution.

**Stack:**
- `httpx` (Python async) or `axios` (Node) for raw HTTP
- `lxml` (Python) or `cheerio` (Node) for DOM traversal
- RSS/sitemap-first: always check `/sitemap.xml`, `/feed.xml`, `/jobs.rss` before crawling HTML pages

**Stealth config:**
```python
HEADERS_POOL = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
    },
    # ... rotate through 5-8 UA profiles
]

# Jitter: random.uniform(1.5, 4.5) seconds between requests per domain
# Max concurrency per domain: 2 simultaneous requests
```

**Heuristic fallback regex (unstructured semantic blocks):**
```python
FALLBACK_PATTERNS = {
    "title": [
        r'<h[1-3][^>]*>\s*(.{10,120}?)\s*</h[1-3]>',
        r'class="[^"]*(?:job[-_]?title|position[-_]?name)[^"]*"[^>]*>\s*(.+?)\s*<',
    ],
    "location": [
        r'(?:location|city|office)["\s:]+([A-Z][a-zA-Z\s,]+(?:India|UAE|Dubai|Remote))',
    ],
    "company": [
        r'<(?:meta|span)[^>]*(?:company|employer|organization)[^>]*content="([^"]+)"',
    ],
}
```

**Drift mitigation:** If extracted field count drops below 60% of baseline → flag domain, reroute to headless fallback, send Slack/webhook alert.

---

### 1.2 CSR/SPA (React/Next.js/Vue) Portals

**Detection signal:** Raw `curl` returns empty `<div id="root">` or minimal shell HTML.

**Strategy priority order:**
1. **JSON hydration extraction (zero-browser):** Check `<script id="__NEXT_DATA__">`, `window.__INITIAL_STATE__`, `window.__PRELOADED_STATE__` in raw source. Parse directly.
2. **Network API interception (Playwright):** If hydration absent, run browser but intercept XHR/fetch calls.
3. **Full DOM scrape (last resort):** Only if API response is encrypted/obfuscated.

**⚠️ Use `rebrowser-playwright` not vanilla Playwright:**
```bash
pip install rebrowser-playwright
playwright install chromium
# Set env: REBROWSER_PATCHES_RUNTIME_FIX_MODE=addBinding
# Fixes Runtime.Enable CDP leak — primary Cloudflare/DataDome detection vector
```

**Playwright memory-safe cluster config:**
```python
# Use: from rebrowser_playwright.async_api import async_playwright
# Drop-in replacement for playwright
N_PAGES_PER_CONTEXT = 15  # tunable

async def create_isolated_context(browser):
    context = await browser.new_context(
        user_agent=random.choice(UA_POOL),
        viewport={"width": 1366, "height": 768},
        java_script_enabled=True,
        ignore_https_errors=False,
    )
    # Block all non-essential resources
    await context.route(
        "**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2,ttf,mp4,webm,ico}",
        lambda route: route.abort()
    )
    await context.route("**/*analytics*", lambda route: route.abort())
    await context.route("**/*tracker*", lambda route: route.abort())
    await context.route("**/*ads*", lambda route: route.abort())
    return context

# Usage pattern:
page_count = 0
context = await create_isolated_context(browser)
for url in url_batch:
    if page_count >= N_PAGES_PER_CONTEXT:
        await context.close()  # explicit memory release
        context = await create_isolated_context(browser)
        page_count = 0
    page = await context.new_page()
    # ... scrape
    await page.close()
    page_count += 1
```

**API interception harvest:**
```python
captured_api_responses = []

async def handle_response(response):
    if response.request.resource_type == "fetch" and "job" in response.url:
        try:
            body = await response.json()
            captured_api_responses.append({"url": response.url, "body": body})
        except:
            pass

page.on("response", handle_response)
await page.goto(target_url, wait_until="networkidle", timeout=30000)
```

---

### 1.3 Internal REST APIs + TLS Fingerprint Evasion

**Detection signal:** Browser DevTools Network tab shows `/api/jobs`, `/graphql`, or `/v*/positions` XHR calls returning clean JSON.

**TLS fingerprinting stack:**
- **Tool:** `curl_cffi` v0.15+ (Chrome 124/146 profiles) — **NOT** `tls-client` (max Chrome 120, unmaintained since 2023)
- **Install:** `pip install curl_cffi`
- **What it spoofs:** JA3/JA4 TLS signature, HTTP/2 SETTINGS frame, ALPN extension order, cipher suite sequence
- **When needed:** Cloudflare, Akamai, DataDome sites that fingerprint TLS at handshake before sending any HTTP response
- **Supported Chrome profiles (2026):** chrome116, chrome119, chrome120, chrome123, chrome124, chrome131, chrome133a, chrome136, chrome142, chrome145, **chrome146** (default)

```python
from curl_cffi.requests import AsyncSession

async with AsyncSession(impersonate="chrome124") as session:
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    })

# Token harvest flow:
# 1. GET homepage → extract CSRF token from meta tag or cookie
# 2. POST /api/auth or /login with credentials
# 3. Store session cookies
# 4. Fire high-velocity paginated API calls with session

def harvest_token(session, base_url):
    resp = session.get(f"{base_url}/")
    # Try meta tag
    import re
    match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
    if match:
        session.headers["X-CSRF-Token"] = match.group(1)
    # Try cookie
    if "csrftoken" in session.cookies:
        session.headers["X-CSRFToken"] = session.cookies["csrftoken"]
    return session
```

---

## 2. ENTERPRISE ATS INGESTION VECTORS

### 2.1 ATS Endpoint Reference

| ATS | Public Feed URL Pattern | Format | Notes |
|---|---|---|---|
| **Greenhouse** | `https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs?content=true` | JSON | `content=true` includes full description |
| **Lever** | `https://api.lever.co/v0/postings/{company_slug}?mode=json` | JSON | `?mode=json&limit=500` for bulk |
| **Workday** | `https://{company}.myworkdayjobs.com/wday/cxs/{company}/{board}/jobs` | JSON POST | POST body: `{"limit":20,"offset":0,"searchText":"","locations":[]}` |
| **Ashby** | `https://jobs.ashbyhq.com/api/non-user-graphql` | GraphQL | POST with `operationName: "ApiJobBoardWithTeams"` |
| **Teamtailor** | `https://api.teamtailor.com/v1/jobs` | JSON (API key) | Public listings: `https://{company}.teamtailor.com/jobs.json` |
| **SmartRecruiters** | `https://api.smartrecruiters.com/v1/companies/{company_id}/postings` | JSON | No auth for public listings |
| **Workable** | `https://apply.workable.com/api/v3/accounts/{slug}/jobs` | JSON POST | `{"query":"","location":[],"department":[],"worktype":[],"remote":[]}` |
| **BambooHR** | `https://{company}.bamboohr.com/careers/list` | JSON | `Accept: application/json` header required |
| **Jobvite** | `https://jobs.jobvite.com/api/jobs?c={company_id}` | JSON | |
| **iCIMS** | `https://{company}.icims.com/jobs/search` | Custom XML/JSON | Check `?schemaVersion=2` param |
| **Taleo** | `https://{company}.taleo.net/careersection/{section_id}/jobsearch.ftl` | HTML (legacy) | Use `?lang=en_US&src=CWS-10020` |

**Workday full implementation:**
```python
# VERIFIED 2026-05-21: No CSRF token required on CXS public endpoints
# Primary blocker is Cloudflare (__cf_bm cookie) — use curl_cffi
from curl_cffi.requests import AsyncSession

async def fetch_workday_jobs(company_subdomain: str, board_id: str, wday_num: int = 3) -> list:
    """
    company_subdomain: tenant slug (e.g., 'sysco' for sysco.wd5.myworkdayjobs.com)
    board_id: board slug visible in URL (e.g., 'External_Career_Site')
    wday_num: the WD instance number (wd1, wd3, wd5 — check company URL)
    Response shape: {"total": N, "jobPostings": [{"title", "externalPath", "locationsText", "postedOn"}]}
    """
    base = f"https://{company_subdomain}.wd{wday_num}.myworkdayjobs.com"
    endpoint = f"{base}/wday/cxs/{company_subdomain}/{board_id}/jobs"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # No CSRF header needed — confirmed via live testing May 2026
    # HTTP 422 = wrong tenant/board slug, NOT auth failure

    payload = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": ""}

    all_jobs = []
    async with AsyncSession(impersonate="chrome124") as client:
        while True:
            resp = await client.post(endpoint, headers=headers, json=payload)
            if resp.status_code == 422:
                raise ValueError(f"Wrong tenant/board slug for {company_subdomain}/{board_id}")
            data = resp.json()
            jobs = data.get("jobPostings", [])
            all_jobs.extend(jobs)
            total = data.get("total", 0)
            payload["offset"] += len(jobs)
            if payload["offset"] >= total or not jobs:
                break

    return all_jobs
```

**Greenhouse implementation:**
```python
async def fetch_greenhouse_jobs(company_slug: str) -> list:
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
    params = {"content": "true"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
    return resp.json().get("jobs", [])
```

**Ashby implementation (use REST, not GraphQL):**
```python
# VERIFIED 2026-05-21: GraphQL fields isRemote/isListed/status REMOVED from type
# Use the official REST API instead — returns ALL fields including isListed, descriptionHtml
import httpx

async def fetch_ashby_jobs(job_board_name: str) -> list:
    """
    job_board_name: the slug after jobs.ashbyhq.com/ (e.g., 'perplexity-ai')
    REST API is the officially documented public API and has not changed.
    """
    url = f"https://api.ashbyhq.com/posting-api/job-board/{job_board_name}"
    params = {"includeCompensation": "true"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
    return resp.json().get("jobPostings", [])

# If you must use GraphQL, the WORKING query (2026) is:
ASHBY_GRAPHQL_QUERY = """
query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) {
  jobBoard: jobBoardWithTeams(organizationHostedJobsPageName: $organizationHostedJobsPageName) {
    teams { id name parentTeamId }
    jobPostings {
      id title teamId locationId locationName employmentType workplaceType
      secondaryLocations compensationTierSummary
    }
  }
}
"""
# NOTE: DO NOT include isRemote, isListed, status — removed from type, causes GRAPHQL_VALIDATION_FAILED
```

---

### 2.2 Authenticated Intranet Console Snippet

Self-contained async browser console script for internal job boards requiring manual login:

```javascript
// AUTONOMOUS INNOVATION HUB — Intranet Harvester v1.0
// Run in browser DevTools Console on any internal job board page
// Config: set WEBHOOK_URL before running
(async () => {
  const WEBHOOK_URL = "https://hooks.n8n.example.com/webhook/job-intake";
  const JITTER_MIN_MS = 800;
  const JITTER_MAX_MS = 2500;
  const BATCH_SIZE = 20;
  const MAX_PAGES = 50;

  const jitter = () => new Promise(r =>
    setTimeout(r, JITTER_MIN_MS + Math.random() * (JITTER_MAX_MS - JITTER_MIN_MS))
  );

  const extractJobsFromDOM = () => {
    const jobs = [];
    // Generic selectors — tune per portal
    const selectors = [
      '[data-testid*="job"]', '.job-card', '.job-listing',
      '[class*="JobCard"]', '[class*="job-row"]', 'li[class*="position"]'
    ];
    for (const sel of selectors) {
      const nodes = document.querySelectorAll(sel);
      if (nodes.length > 0) {
        nodes.forEach(node => {
          jobs.push({
            title: node.querySelector('h2,h3,[class*="title"],[class*="role"]')?.innerText?.trim(),
            location: node.querySelector('[class*="location"],[data-testid*="location"]')?.innerText?.trim(),
            department: node.querySelector('[class*="dept"],[class*="team"],[class*="function"]')?.innerText?.trim(),
            url: node.querySelector('a')?.href,
            raw_html: node.outerHTML.substring(0, 2000),
            harvested_at: new Date().toISOString(),
            source_url: window.location.href,
          });
        });
        break; // first matching selector wins
      }
    }
    return jobs;
  };

  const findNextPageButton = () => {
    const candidates = [
      document.querySelector('[aria-label="Next page"]'),
      document.querySelector('[data-testid="pagination-next"]'),
      document.querySelector('.pagination-next:not([disabled])'),
      [...document.querySelectorAll('button,a')].find(el =>
        /next/i.test(el.innerText) && !el.disabled && el.offsetParent !== null
      ),
    ];
    return candidates.find(Boolean) || null;
  };

  const postBatch = async (batch) => {
    try {
      await fetch(WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jobs: batch, batch_size: batch.length, ts: Date.now() }),
      });
      console.log(`✓ Posted batch of ${batch.length} jobs`);
    } catch (e) {
      console.error("Webhook POST failed:", e.message);
    }
  };

  let allJobs = [];
  let page = 1;

  while (page <= MAX_PAGES) {
    console.log(`Scraping page ${page}...`);
    const pageJobs = extractJobsFromDOM();
    allJobs.push(...pageJobs);
    console.log(`  Found ${pageJobs.length} jobs (total: ${allJobs.length})`);

    if (allJobs.length >= BATCH_SIZE) {
      await postBatch(allJobs.splice(0, BATCH_SIZE));
      await jitter();
    }

    const nextBtn = findNextPageButton();
    if (!nextBtn) { console.log("No next page found. Done."); break; }

    nextBtn.click();
    await jitter();
    await new Promise(r => setTimeout(r, 1500)); // wait for DOM update
    page++;
  }

  if (allJobs.length > 0) await postBatch(allJobs);
  console.log("Harvest complete.");
})();
```

---

### 2.3 Passive Browser Extension (Manifest V3)

**Directory structure:**
```
extension/
├── manifest.json
├── background.js          (Service Worker)
├── content_scripts/
│   └── job_detector.js
└── utils/
    └── heuristics.js
```

**manifest.json:**
```json
{
  "manifest_version": 3,
  "name": "Job Harvester",
  "version": "1.0",
  "permissions": ["storage", "alarms"],
  "host_permissions": ["<all_urls>"],
  "background": { "service_worker": "background.js" },
  "content_scripts": [{
    "matches": ["<all_urls>"],
    "js": ["content_scripts/job_detector.js"],
    "run_at": "document_idle"
  }]
}
```

**content_scripts/job_detector.js:**
```javascript
const JOB_PAGE_SIGNALS = [
  "responsibilities", "requirements", "qualifications",
  "what you'll do", "about the role", "job description",
  "years of experience", "we are looking for"
];

const isJobPage = () => {
  const body = document.body.innerText.toLowerCase();
  const matches = JOB_PAGE_SIGNALS.filter(s => body.includes(s));
  return matches.length >= 3; // at least 3 signals = job page
};

const extractJobData = () => ({
  url: window.location.href,
  title: document.querySelector('h1')?.innerText?.trim(),
  company: document.querySelector('[class*="company"],[itemtype*="Organization"]')?.innerText?.trim()
    || document.title.split(' - ').slice(-1)[0]?.trim(),
  description: document.body.innerText.substring(0, 3000),
  captured_at: new Date().toISOString(),
  domain: window.location.hostname,
});

if (isJobPage()) {
  const data = extractJobData();
  chrome.runtime.sendMessage({ type: "JOB_DETECTED", payload: data });
}
```

**background.js (Service Worker):**
```javascript
const WEBHOOK = "https://hooks.n8n.example.com/webhook/job-intake";
const QUEUE_KEY = "job_queue";
const FLUSH_INTERVAL_MINUTES = 5;

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "JOB_DETECTED") {
    chrome.storage.local.get([QUEUE_KEY], (result) => {
      const queue = result[QUEUE_KEY] || [];
      queue.push(msg.payload);
      chrome.storage.local.set({ [QUEUE_KEY]: queue });
    });
  }
});

// Flush queue every 5 minutes
chrome.alarms.create("flush_queue", { periodInMinutes: FLUSH_INTERVAL_MINUTES });
chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name !== "flush_queue") return;
  chrome.storage.local.get([QUEUE_KEY], async (result) => {
    const queue = result[QUEUE_KEY] || [];
    if (queue.length === 0) return;
    try {
      await fetch(WEBHOOK, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jobs: queue }),
      });
      chrome.storage.local.set({ [QUEUE_KEY]: [] });
    } catch (e) { /* retain queue on failure */ }
  });
});
```

---

### 2.4 Unstructured Social/Community Stream Parser (LLM-Native)

**Pipeline:** Raw message → token-pinned LLM extraction → structured JSON → dedup layer

**Optimized system prompt:**
```
You are a job posting parser. Extract structured data from raw text.
Return ONLY valid JSON matching this exact schema. No markdown, no explanation.
If a field cannot be determined, use null.

Schema:
{
  "job_title": string | null,
  "company": string | null,
  "location": string | null,        // "Remote" if remote, city/country if specified
  "salary_min": number | null,      // numeric, USD equivalent if possible
  "salary_max": number | null,
  "currency": string | null,        // ISO 4217 code
  "employment_type": "full_time" | "part_time" | "contract" | "freelance" | null,
  "skills_required": string[],      // top 5 max
  "experience_years_min": number | null,
  "apply_url": string | null,
  "is_job_posting": boolean         // false if message is not a hiring post
}
```

**Python extraction pipeline:**
```python
from openai import AsyncOpenAI
from instructor import from_openai, Mode
from pydantic import BaseModel
from typing import Optional

client = from_openai(AsyncOpenAI(), mode=Mode.JSON)

class JobPosting(BaseModel):
    job_title: Optional[str]
    company: Optional[str]
    location: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    currency: Optional[str]
    employment_type: Optional[str]
    skills_required: list[str]
    experience_years_min: Optional[int]
    apply_url: Optional[str]
    is_job_posting: bool

async def parse_social_post(raw_text: str) -> JobPosting:
    return await client.chat.completions.create(
        model="gpt-4o-mini",  # cheapest capable model
        response_model=JobPosting,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text[:4000]},  # token cap
        ],
        max_tokens=400,
    )
```

---

## 3. UNIFIED FRAMEWORK, SCHEMAS & DEDUPLICATION

### 3.1 n8n Orchestration Architecture

```
[Trigger Layer]
  ├── Cron: ATS API batch (every 6h) → HTTP Request Node → Parse JSON → Normalize Node
  ├── Webhook: Console snippet / Extension POST → Parse Body → Normalize Node
  └── RSS Watcher: Monitor /jobs.rss feeds (every 1h) → Parse XML → Normalize Node

[Normalization Node] (Code Node in n8n)
  → strip markdown, lowercase, trim whitespace
  → extract salary from free text
  → map to unified schema

[Dedup Gate] (Redis lookup via HTTP Request to Redis REST API)
  → check bloom filter → if exists: DROP → if new: PASS

[Storage Node]
  → Supabase (PostgreSQL) upsert via HTTP Request node

[Alert Node]
  → drift detection: if null_field_rate > 40% → Slack webhook
  → new job alert: if match_score(job, target_list) > 0.8 → email/Slack
```

### 3.2 Production JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "source_url", "job_title", "company", "ingested_at"],
  "properties": {
    "id": {
      "type": "string",
      "description": "sha256(normalize(company)+normalize(job_title)+normalize(location)+description[:500])"
    },
    "source_url": { "type": "string", "format": "uri" },
    "canonical_url": { "type": ["string", "null"], "format": "uri" },
    "ats_source": {
      "type": ["string", "null"],
      "enum": ["greenhouse", "lever", "workday", "ashby", "teamtailor", "smartrecruiters",
               "workable", "bamboohr", "jobvite", "icims", "manual", "extension", "social", null]
    },
    "job_title": { "type": "string" },
    "job_title_normalized": { "type": "string" },
    "company": { "type": "string" },
    "company_normalized": { "type": "string" },
    "location": { "type": ["string", "null"] },
    "location_normalized": { "type": ["string", "null"] },
    "is_remote": { "type": "boolean", "default": false },
    "employment_type": {
      "type": ["string", "null"],
      "enum": ["full_time", "part_time", "contract", "freelance", "internship", null]
    },
    "seniority_level": {
      "type": ["string", "null"],
      "enum": ["intern", "junior", "mid", "senior", "lead", "principal", "director", "vp", "c_level", null]
    },
    "department": { "type": ["string", "null"] },
    "clean_description": { "type": ["string", "null"] },
    "description_embedding": {
      "type": ["array", "null"],
      "items": { "type": "number" },
      "description": "384-dim vector from all-MiniLM-L6-v2"
    },
    "skills_required": { "type": "array", "items": { "type": "string" } },
    "experience_years_min": { "type": ["integer", "null"] },
    "experience_years_max": { "type": ["integer", "null"] },
    "salary_min": { "type": ["number", "null"] },
    "salary_max": { "type": ["number", "null"] },
    "currency": { "type": ["string", "null"] },
    "raw_salary_text": { "type": ["string", "null"] },
    "apply_url": { "type": ["string", "null"], "format": "uri" },
    "ingested_at": { "type": "string", "format": "date-time" },
    "first_seen_at": { "type": "string", "format": "date-time" },
    "last_seen_at": { "type": "string", "format": "date-time" },
    "is_active": { "type": "boolean", "default": true },
    "deactivated_at": { "type": ["string", "null"], "format": "date-time" },
    "content_hash": {
      "type": "string",
      "description": "sha256 of clean_description — for change detection"
    },
    "snapshot_b64": {
      "type": ["string", "null"],
      "description": "gzip+base64 of raw HTML snapshot, max 50KB"
    },
    "target_company_match": { "type": "boolean", "default": false },
    "target_segment": {
      "type": ["string", "null"],
      "enum": ["india_mnc", "global_ai_startup", "dubai_visa", null]
    },
    "relevance_score": {
      "type": ["number", "null"],
      "minimum": 0, "maximum": 1,
      "description": "Cosine similarity to ideal PM role embedding"
    },
    "application_status": {
      "type": ["string", "null"],
      "enum": ["not_applied", "applied", "screening", "interviewing", "offer", "rejected", "closed", null],
      "default": "not_applied"
    },
    "notes": { "type": ["string", "null"] }
  }
}
```

---

### 3.3 Hybrid Deduplication Engine (4-Layer)

```python
import hashlib
import re
import unicodedata
from typing import Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from redis import Redis

# Load once at startup — ~90MB RAM
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
redis_client = Redis(host="localhost", port=6379, db=0)

COSINE_SIM_THRESHOLD = 0.92
BLOOM_FILTER_KEY = "job_bloom"

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    # Remove common noise words
    NOISE = {"the", "a", "an", "and", "or", "of", "in", "at", "for", "to", "is", "are", "we", "you"}
    return " ".join(w for w in text.split() if w not in NOISE)

def compute_canonical_hash(company: str, title: str, location: str, description: str) -> str:
    """Layer 2: Deterministic content hash"""
    fingerprint = (
        normalize_text(company)
        + normalize_text(title)
        + normalize_text(location)
        + normalize_text(description[:500])
    )
    return hashlib.sha256(fingerprint.encode()).hexdigest()

def expand_short_url(url: str) -> str:
    """Layer 1: Short URL expansion"""
    SHORT_URL_DOMAINS = {"bit.ly", "tinyurl.com", "t.co", "ow.ly", "buff.ly"}
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.lstrip("www.")
    if domain in SHORT_URL_DOMAINS:
        import httpx
        try:
            r = httpx.head(url, follow_redirects=True, timeout=5)
            return str(r.url)
        except:
            pass
    return url

def get_canonical_url(url: str) -> str:
    """Layer 1: URL normalization"""
    url = expand_short_url(url)
    # Strip tracking params
    TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "ref", "src", "gh_src"}
    from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
    parsed = urlparse(url)
    clean_params = {k: v for k, v in parse_qs(parsed.query).items() if k not in TRACKING_PARAMS}
    canonical = urlunparse(parsed._replace(query=urlencode(clean_params, doseq=True), fragment=""))
    return canonical.rstrip("/").lower()

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

class DeduplicationEngine:
    def __init__(self):
        self.seen_hashes: set = set()  # in-memory fast set
        self.seen_urls: set = set()

    def is_duplicate(self, job: dict) -> tuple[bool, str]:
        """
        Returns (is_duplicate, reason)
        reason: "url_match" | "hash_match" | "semantic_match" | "new"
        """
        # Layer 1: URL dedup
        canonical_url = get_canonical_url(job.get("source_url", ""))
        if canonical_url in self.seen_urls:
            return True, "url_match"
        
        # Layer 2: Hash dedup
        content_hash = compute_canonical_hash(
            job.get("company", ""),
            job.get("job_title", ""),
            job.get("location", ""),
            job.get("clean_description", ""),
        )
        if content_hash in self.seen_hashes:
            return True, "hash_match"
        
        # Also check Redis bloom filter (cross-session persistence)
        if redis_client.getbit(BLOOM_FILTER_KEY, int(content_hash[:8], 16) % (10**7)):
            return True, "hash_match_redis"

        # Layer 3: Semantic dedup (only if description present and >100 chars)
        description = job.get("clean_description", "")
        if len(description) > 100:
            new_embedding = EMBED_MODEL.encode(description[:1000])
            # Check against recent embeddings stored in Redis
            recent_keys = redis_client.lrange("recent_embeddings", 0, 199)  # last 200
            for key in recent_keys:
                stored = np.frombuffer(redis_client.get(key), dtype=np.float32)
                if cosine_similarity(new_embedding, stored) > COSINE_SIM_THRESHOLD:
                    return True, "semantic_match"
            # Store new embedding
            embed_key = f"embed:{content_hash}"
            redis_client.set(embed_key, new_embedding.astype(np.float32).tobytes(), ex=86400 * 30)
            redis_client.lpush("recent_embeddings", embed_key)
            redis_client.ltrim("recent_embeddings", 0, 199)

        # Not a duplicate — register
        self.seen_urls.add(canonical_url)
        self.seen_hashes.add(content_hash)
        redis_client.setbit(BLOOM_FILTER_KEY, int(content_hash[:8], 16) % (10**7), 1)

        return False, "new"
```

---

### 3.4 Self-Healing & Drift Detection

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ScraperHealth:
    domain: str
    expected_fields: list[str]
    null_threshold: float = 0.4  # >40% nulls = drift alert

def check_drift(jobs: list[dict], health: ScraperHealth) -> dict:
    if not jobs:
        return {"status": "empty", "action": "alert", "domain": health.domain}
    
    null_rates = {}
    for field in health.expected_fields:
        null_count = sum(1 for j in jobs if not j.get(field))
        null_rates[field] = null_count / len(jobs)
    
    critical_nulls = {f: r for f, r in null_rates.items() if r > health.null_threshold}
    
    if critical_nulls:
        return {
            "status": "drift_detected",
            "domain": health.domain,
            "critical_fields": critical_nulls,
            "action": "alert_and_fallback",
            "timestamp": datetime.utcnow().isoformat(),
        }
    return {"status": "healthy"}

# Exponential backoff with jitter
import asyncio
import random

async def fetch_with_backoff(fetch_fn, max_retries=4, base_delay=2.0):
    for attempt in range(max_retries):
        try:
            return await fetch_fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
```

---

## 5. INFRASTRUCTURE COST ESTIMATE

| Component | Tool | Cost |
|---|---|---|
| Orchestration | n8n Cloud (Starter) | $20/mo or self-host free |
| Database | Supabase (free tier) | Free (500MB) |
| Redis | Upstash (free tier) | Free (10K req/day) |
| LLM parsing | GPT-4o-mini | ~$0.001/post → $1-5/mo |
| Proxy rotation | Webshare (free tier) | Free (1GB/mo) |
| Embeddings | local all-MiniLM-L6-v2 | Free (CPU) |
| TLS client | tls-client (Python lib) | Free |
| **Total** | | **~$20-30/mo** |

---

## 6. RESEARCH GAPS — RESOLVED (2026-05-21)

| Gap | Finding | Status |
|---|---|---|
| Workday CSRF token | NOT required for CXS POST endpoints. Cloudflare is the blocker. | ✅ RESOLVED |
| `tls-client` Chrome 124 | `tls-client` max Chrome 120, unmaintained → use `curl_cffi` | ✅ RESOLVED |
| n8n embedding compute | Code Node can't run sentence-transformers on Cloud → external FastAPI microservice | ✅ RESOLVED |
| Supabase pgvector free | Supported; ~50k 384-dim vector limit on free Micro; HNSW recommended | ✅ RESOLVED |
| Playwright stealth 2025 | `playwright-extra` dead since 2023 → use `rebrowser-playwright` | ✅ RESOLVED |
| Greenhouse/Lever rate limits | No documented limits on public read APIs in 2025-2026 | ✅ RESOLVED |
| Ashby GraphQL schema | `isRemote`/`isListed`/`status` removed → use REST API instead | ✅ RESOLVED |
| curl-impersonate latest | v0.6.1 (Mar 2024), max Chrome 116 → use `curl_cffi` lexiforest fork | ✅ RESOLVED |

**Still open:**
- [ ] LinkedIn unofficial API / li-scraper current state (2026) — blocked by AMEX wifi TLS
- [ ] Reddit API current rate limits and OAuth2 flow (2026)

---

## 7. NEXT STEPS

1. **Immediate:** Research all gaps in Section 6 using agent-browser
2. **Week 1:** Deploy n8n + Supabase + implement Greenhouse/Lever/Ashby fetchers
3. **Week 2:** Add Workday fetcher for top 20 target companies from Job Database.xlsx
4. **Week 3:** Dedup engine + drift detection
5. **Week 4:** Console snippet testing on 5 internal boards, Extension v1
