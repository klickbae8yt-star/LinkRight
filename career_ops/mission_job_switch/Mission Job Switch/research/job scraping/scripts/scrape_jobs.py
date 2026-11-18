"""
Career portal verifier + job scraper
- Hits actual ATS APIs for definitive verification
- Gets up to 50 jobs per company
- Saves to jobs.db (SQLite)
"""

import asyncio
import json
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import httpx
from curl_cffi.requests import AsyncSession as CurlSession

BASE = Path(__file__).parent.parent
JSON_PATH = BASE / "db" / "career_urls_result.json"
DB_PATH = BASE / "db" / "jobs.db"

# CLI: --workday-search overrides the Workday CXS searchText at runtime
# Set via skill based on user's natural language description
import argparse as _ap
_p = _ap.ArgumentParser(add_help=False)
_p.add_argument("--workday-search", default="product")
_ARGS, _ = _p.parse_known_args()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# ─── ATS OVERRIDES (company → explicit API params) ────────────────────────────
# For companies where career_url is generic (not the ATS URL itself).
# Format: company_name_lower → {"type": ..., "slug/tenant/board/wdN": ...}

ATS_OVERRIDES = {
    # Greenhouse slugs
    "phonepe":              {"type": "greenhouse", "slug": "phonepe"},
    "twilio":               {"type": "greenhouse", "slug": "twilio"},
    "stripe":               {"type": "greenhouse", "slug": "stripe"},
    "inmobi / glance":      {"type": "greenhouse", "slug": "inmobi"},
    "coupang india":        {"type": "greenhouse", "slug": "coupang"},
    "careem":               {"type": "greenhouse", "slug": "careem"},
    "groww":                {"type": "greenhouse", "slug": "groww"},

    # Lever slugs
    "zomato / blinkit":     {"type": "lever", "slug": "eternal"},   # Zomato parent rebranded to Eternal
    "meesho":               {"type": "lever", "slug": "meesho"},
    "cred":                 {"type": "lever", "slug": "cred"},
    "binance":              {"type": "lever", "slug": "binance"},
    "gushwork ai":          {"type": "lever", "slug": "gushwork"},

    # SmartRecruiters slugs (case-sensitive company ID)
    "razorpay":             {"type": "smartrecruiters", "slug": "Razorpay"},
    "coinbase":             {"type": "smartrecruiters", "slug": "Coinbase"},
    "bayut":                {"type": "smartrecruiters", "slug": "Bayut1"},

    # Workable slugs
    "talabat":              {"type": "workable", "slug": "talabat"},
    "monica ai":            {"type": "workable", "slug": "monica"},
    "d-id":                 {"type": "workable", "slug": "d-id"},
    "veed.io":              {"type": "workable", "slug": "veed"},

    # Ashby board IDs
    "pika labs":            {"type": "ashby", "board": "pika"},

    # Workday: tenant, wdN, board
    "uber":                 {"type": "workday", "tenant": "uber",           "wdN": 5,  "board": "Uber_Career"},
    "atlassian":            {"type": "workday", "tenant": "atlassian",      "wdN": 5,  "board": "atlassian"},
    "salesforce":           {"type": "workday", "tenant": "salesforce",     "wdN": 12, "board": "External_Career_Site"},
    "walmart global tech":  {"type": "workday", "tenant": "walmart",        "wdN": 5,  "board": "WalmartExternal"},
    "linkedin":             {"type": "workday", "tenant": "linkedin",       "wdN": 5,  "board": "LinkedIn"},
    "booking.com":          {"type": "workday", "tenant": "booking",        "wdN": 3,  "board": "ExternalCareerSite"},
    "cisco":                {"type": "workday", "tenant": "cisco",          "wdN": 5,  "board": "External"},
    "intuit":               {"type": "workday", "tenant": "intuit",         "wdN": 5,  "board": "Intuit_Careers"},
    "grab":                 {"type": "workday", "tenant": "grab",           "wdN": 5,  "board": "careers"},
    "apple":                {"type": "workday", "tenant": "apple",          "wdN": 5,  "board": "External"},
    "netflix":              {"type": "workday", "tenant": "netflix",        "wdN": 5,  "board": "NetflixJobs"},
    "servicenow":           {"type": "workday", "tenant": "servicenow",     "wdN": 5,  "board": "External"},
    "expedia group":        {"type": "workday", "tenant": "expedia",        "wdN": 5,  "board": "expedia_group"},
    "visa":                 {"type": "workday", "tenant": "visa",           "wdN": 5,  "board": "External"},
    "rakuten india":        {"type": "workday", "tenant": "rakuten",        "wdN": 3,  "board": "rakuten"},
    "broadcom (vmware)":    {"type": "workday", "tenant": "broadcom",       "wdN": 1,  "board": "ExternalJobBoard"},
    "tesco technology":     {"type": "workday", "tenant": "tesco",          "wdN": 3,  "board": "External"},
    "philips healthtech":   {"type": "workday", "tenant": "philips",        "wdN": 3,  "board": "External"},
    "yahoo! india":         {"type": "workday", "tenant": "yahooinc",       "wdN": 5,  "board": "Yahoo"},
    "citrix (cloud software group)": {"type": "workday", "tenant": "cloudsoftwaregroup", "wdN": 5, "board": "External"},
    "trellix":              {"type": "workday", "tenant": "trellix",        "wdN": 1,  "board": "External"},
    "akamai technologies":  {"type": "workday", "tenant": "akamai",        "wdN": 1,  "board": "akamai"},
    "gartner":              {"type": "workday", "tenant": "gartner",        "wdN": 5,  "board": "External"},
    "ge healthcare":        {"type": "workday", "tenant": "gehealthcare",   "wdN": 5,  "board": "External"},
    "nutanix":              {"type": "workday", "tenant": "nutanix",        "wdN": 5,  "board": "External"},
    "zoom video communications": {"type": "workday", "tenant": "zoom",     "wdN": 5,  "board": "External"},
    "mastercard":           {"type": "workday", "tenant": "mastercard",     "wdN": 1,  "board": "CorporateCareers"},
    "myntra":               {"type": "workday", "tenant": "myntra",         "wdN": 5,  "board": "myntra"},
    "qualcomm":             {"type": "workday", "tenant": "qualcomm",       "wdN": 5,  "board": "External"},
    "goldman sachs (tech)": {"type": "workday", "tenant": "gs",            "wdN": 5,  "board": "GSExternal"},
    "makemytrip":           {"type": "workday", "tenant": "makemytrip",     "wdN": 5,  "board": "makemytrip"},
    "sony india software centre": {"type": "workday", "tenant": "sony",    "wdN": 5,  "board": "sony_global_ext"},
    "cigna middle east":    {"type": "workday", "tenant": "cigna",          "wdN": 5,  "board": "External"},
    "seera group":          {"type": "workday", "tenant": "seera",          "wdN": 3,  "board": "External"},
}

# ─── DB ────────────────────────────────────────────────────────────────────────

def init_db(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS companies (
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
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            segment TEXT,
            portal_type TEXT,
            title TEXT,
            department TEXT,
            location TEXT,
            job_url TEXT,
            posted_at TEXT,
            scraped_at TEXT,
            job_description TEXT,
            compensation TEXT,
            years_experience TEXT,
            employment_type TEXT,
            is_remote INTEGER DEFAULT 0,
            role_category TEXT,
            sector TEXT,
            relevance_score REAL,
            is_ghost INTEGER DEFAULT 0,
            source_portal TEXT,
            company_id INTEGER
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company)")
    conn.commit()
    return conn


def upsert_company(conn, company, segment, career_url, portal_type,
                   verified, verified_url, jobs_found, error):
    conn.execute("""
        INSERT INTO companies (company, segment, career_url, portal_type,
            verified, verified_url, jobs_found, error, checked_at)
        VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(company) DO UPDATE SET
            portal_type=excluded.portal_type,
            verified=excluded.verified,
            verified_url=excluded.verified_url,
            jobs_found=excluded.jobs_found,
            error=excluded.error,
            checked_at=excluded.checked_at
    """, (company, segment, career_url, portal_type,
          1 if verified else 0, verified_url, jobs_found,
          error, datetime.now().isoformat()))
    conn.commit()


MAX_DESC_CHARS = 8000

def _str(v) -> str:
    if isinstance(v, (list, dict)):
        return json.dumps(v)
    return str(v) if v else ""

def _desc(v) -> str:
    """Stringify + truncate description to avoid DB bloat and timeout issues."""
    s = _str(v)
    return s[:MAX_DESC_CHARS] if len(s) > MAX_DESC_CHARS else s


def insert_jobs(conn, company, segment, portal_type, jobs):
    conn.execute("DELETE FROM jobs WHERE company=?", (company,))
    now = datetime.now().isoformat()
    conn.executemany("""
        INSERT INTO jobs (company, segment, portal_type, title, department,
            location, job_url, posted_at, scraped_at, job_description)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, [
        (company, segment, portal_type,
         _str(j.get("title")), _str(j.get("department")),
         _str(j.get("location")), _str(j.get("url")),
         _str(j.get("posted_at")), now,
         _desc(j.get("job_description")))
        for j in jobs
    ])
    conn.commit()


# ─── SLUG EXTRACTORS ──────────────────────────────────────────────────────────

def greenhouse_slug(entry) -> str | None:
    url = entry.get("career_url","")
    m = re.search(r'greenhouse\.io/([^/?#]+)', url)
    if m:
        return m.group(1)
    # try classification_source
    src = entry.get("classification_source","")
    m = re.search(r'greenhouse\.io/([^/?#\s]+)', src)
    if m:
        return m.group(1)
    return None


def lever_slug(entry) -> str | None:
    combined = entry.get("career_url","") + " " + entry.get("classification_source","")
    m = re.search(r'lever\.co/([^/?#\s]+)', combined)
    return m.group(1) if m else None


def ashby_board(entry) -> str | None:
    url = entry.get("career_url","")
    m = re.search(r'ashbyhq\.com/([^/?#]+)', url)
    if m:
        return m.group(1).rstrip("/")
    src = entry.get("classification_source","")
    m = re.search(r'ashbyhq\.com/([^/?#\s]+)', src)
    if m:
        return m.group(1).rstrip("/")
    return None


def workday_parts(entry) -> tuple[str,int,str] | None:
    """Returns (tenant, wdN, board) or None."""
    url = entry.get("career_url","")
    m = re.search(r'([\w-]+)\.(wd\d+)\.myworkdayjobs\.com/(?:[^/]+/)?([^/?#]+)', url)
    if m:
        tenant, wdstr, board = m.group(1), m.group(2), m.group(3)
        wdN = int(re.search(r'\d+', wdstr).group())
        return tenant, wdN, board
    src = entry.get("classification_source","")
    m = re.search(r'([\w-]+)\.(wd\d+)\.myworkdayjobs\.com', src)
    if m:
        tenant = m.group(1)
        wdN = int(re.search(r'\d+', m.group(2)).group())
        return tenant, wdN, None  # board unknown → needs discovery
    return None


def workable_slug(entry) -> str | None:
    url = entry.get("career_url","")
    m = re.search(r'workable\.com/([^/?#]+)', url)
    return m.group(1).rstrip("/") if m else None


def smartrecruiters_slug(entry) -> str | None:
    combined = entry.get("career_url","") + " " + entry.get("classification_source","")
    m = re.search(r'smartrecruiters\.com/([^/?#\s]+)', combined)
    return m.group(1) if m else None


# ─── SCRAPERS ─────────────────────────────────────────────────────────────────

async def scrape_greenhouse(client: httpx.AsyncClient, slug: str) -> tuple[bool, str, list]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
    try:
        r = await client.get(url, timeout=25)
        if r.status_code == 200:
            data = r.json()
            if "jobs" not in data:
                print(f"  ⚠ SCHEMA_CHANGE Greenhouse/{slug}: keys={list(data.keys())[:5]}")
                return False, url, []
            jobs_raw = data["jobs"][:20]  # content=true returns full HTML; keep low to avoid timeout
            jobs = [{
                "title": j.get("title",""),
                "department": (j.get("departments") or [{}])[0].get("name","") if j.get("departments") else "",
                "location": (j.get("offices") or [{}])[0].get("name","") if j.get("offices") else j.get("location",{}).get("name",""),
                "url": j.get("absolute_url",""),
                "posted_at": j.get("updated_at",""),
                "job_description": j.get("content",""),
            } for j in jobs_raw]
            return True, url, jobs
        return False, url, []
    except Exception as e:
        return False, url, []


async def scrape_lever(client: httpx.AsyncClient, slug: str) -> tuple[bool, str, list]:
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json&limit=50"
    try:
        r = await client.get(url, timeout=20)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, dict):
                data = data.get("data", [])
            if not isinstance(data, list):
                print(f"  ⚠ SCHEMA_CHANGE Lever/{slug}: expected list, got {type(data).__name__}")
                return False, url, []
            jobs = [{
                "title": j.get("text",""),
                "department": (j.get("categories") or {}).get("department",""),
                "location": (j.get("categories") or {}).get("location",""),
                "url": j.get("hostedUrl",""),
                "posted_at": datetime.fromtimestamp(j["createdAt"]/1000).isoformat() if j.get("createdAt") else "",
                "job_description": j.get("descriptionPlain","") or j.get("description",""),
            } for j in data[:50]]
            return True, url, jobs
        return False, url, []
    except Exception as e:
        return False, url, []


async def scrape_ashby(client: httpx.AsyncClient, board_id: str) -> tuple[bool, str, list]:
    url = f"https://api.ashbyhq.com/posting-api/job-board/{board_id}"
    try:
        r = await client.get(url, timeout=20)
        if r.status_code == 200:
            data = r.json()
            postings_raw = data.get("jobs") or data.get("jobPostings")
            if postings_raw is None:
                print(f"  ⚠ SCHEMA_CHANGE Ashby/{board_id}: neither 'jobs' nor 'jobPostings' found. keys={list(data.keys())[:5]}")
                return False, url, []
            postings = postings_raw[:50]
            jobs = [{
                "title": j.get("title",""),
                "department": j.get("department","") or j.get("departmentName",""),
                "location": j.get("location","") or j.get("locationName","") or ("Remote" if j.get("isRemote") else ""),
                "url": j.get("jobUrl","") or f"https://jobs.ashbyhq.com/{board_id}/{j.get('id','')}",
                "posted_at": j.get("publishedAt","") or j.get("publishedDate",""),
                "job_description": j.get("descriptionHtml","") or j.get("descriptionPlain",""),
            } for j in postings]
            return True, url, jobs
        return False, url, []
    except Exception as e:
        return False, url, []


async def discover_workday_board(curl_session: CurlSession, tenant: str, wdN: int) -> str | None:
    """Follow redirect from tenant homepage to discover board slug."""
    base = f"https://{tenant}.wd{wdN}.myworkdayjobs.com/"
    try:
        r = await curl_session.get(base, timeout=20, impersonate="chrome136", allow_redirects=True)
        final = str(r.url)
        m = re.search(r'myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/?#]+)', final)
        if m and m.group(1) not in ("", tenant):
            return m.group(1)
        # Try to find board in page links
        m2 = re.search(r'/([A-Za-z0-9_-]{4,50})/jobDetails', r.text)
        if m2:
            return m2.group(1)
    except:
        pass
    return None


async def scrape_workday(curl_session: CurlSession, tenant: str, wdN: int, board: str) -> tuple[bool, str, list]:
    endpoint = f"https://{tenant}.wd{wdN}.myworkdayjobs.com/wday/cxs/{tenant}/{board}/jobs"
    payload = {"appliedFacets": {}, "limit": 50, "offset": 0, "searchText": _ARGS.workday_search}
    headers = {**HEADERS, "Content-Type": "application/json"}
    try:
        r = await curl_session.post(endpoint, json=payload, headers=headers, timeout=25, impersonate="chrome136")
        if r.status_code == 200:
            data = r.json()
            if "jobPostings" not in data:
                print(f"  ⚠ SCHEMA_CHANGE Workday/{tenant}/{board}: keys={list(data.keys())[:5]}")
                return False, endpoint, []
            postings = data["jobPostings"][:50]
            jobs = [{
                "title": j.get("title",""),
                "department": "",
                "location": j.get("locationsText",""),
                "url": f"https://{tenant}.wd{wdN}.myworkdayjobs.com{j.get('externalPath','')}",
                "posted_at": j.get("postedOn",""),
                "job_description": "",
            } for j in postings]
            return True, endpoint, jobs
        return False, endpoint, []
    except Exception as e:
        return False, endpoint, []


async def scrape_workable(client: httpx.AsyncClient, slug: str) -> tuple[bool, str, list]:
    url = f"https://apply.workable.com/api/v3/accounts/{slug}/jobs"
    try:
        r = await client.post(url, json={"query":"","location":[],"department":[],"worktype":[],"remote":[]}, timeout=20)
        if r.status_code == 200:
            data = r.json()
            if "results" not in data:
                print(f"  ⚠ SCHEMA_CHANGE Workable/{slug}: keys={list(data.keys())[:5]}")
                return False, url, []
            results = data["results"][:50]
            jobs = [{
                "title": j.get("title",""),
                "department": j.get("department",""),
                "location": j.get("location",{}).get("city","") if j.get("location") else "",
                "url": f"https://apply.workable.com/{slug}/j/{j.get('shortcode','')}",
                "posted_at": j.get("published",""),
                "job_description": j.get("description",""),
            } for j in results]
            return True, url, jobs
        return False, url, []
    except:
        return False, url, []


async def scrape_smartrecruiters(client: httpx.AsyncClient, slug: str) -> tuple[bool, str, list]:
    url = f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=50"
    try:
        r = await client.get(url, timeout=20)
        if r.status_code == 200:
            data = r.json()
            if "content" not in data:
                print(f"  ⚠ SCHEMA_CHANGE SmartRecruiters/{slug}: keys={list(data.keys())[:5]}")
                return False, url, []
            postings = data["content"][:50]
            jobs = [{
                "title": j.get("name",""),
                "department": (j.get("department") or {}).get("label",""),
                "location": (j.get("location") or {}).get("city",""),
                "url": f"https://jobs.smartrecruiters.com/{slug}/{j.get('id','')}",
                "posted_at": j.get("releasedDate",""),
                "job_description": (j.get("jobAd") or {}).get("sections",{}).get("jobDescription",{}).get("text",""),
            } for j in postings]
            return True, url, jobs
        return False, url, []
    except:
        return False, url, []


async def scrape_eightfold(client: httpx.AsyncClient, career_url: str) -> tuple[bool, str, list]:
    m = re.search(r'([\w-]+)\.eightfold\.ai', career_url)
    if not m:
        return False, career_url, []
    company = m.group(1)
    url = f"https://{company}.eightfold.ai/api/apply/v2/jobs?domain={company}.eightfold.ai&start=0&num=50"
    try:
        r = await client.get(url, timeout=20)
        if r.status_code == 200:
            postings = r.json().get("positions", [])[:50]
            jobs = [{
                "title": j.get("name",""),
                "department": j.get("department",""),
                "location": j.get("location",""),
                "url": f"https://{company}.eightfold.ai/careers?pid={j.get('id','')}",
                "posted_at": j.get("t_update",""),
                "job_description": j.get("description",""),
            } for j in postings]
            return True, url, jobs
        return False, url, []
    except:
        return False, url, []


async def scrape_next_js(client: httpx.AsyncClient, career_url: str) -> tuple[bool, str, list]:
    """Try to extract jobs from __NEXT_DATA__ embedded JSON."""
    try:
        r = await client.get(career_url, timeout=15, follow_redirects=True)
        if r.status_code != 200:
            return False, career_url, []
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', r.text, re.DOTALL)
        if not m:
            return False, career_url, []
        nd = json.loads(m.group(1))
        # Flatten and search for job-like objects
        text = json.dumps(nd)
        # Look for arrays of objects with title/location keys
        job_arrays = re.findall(r'\[(\{[^]]{50,}\}(?:,\{[^]]{50,}\})*)\]', text)
        for arr_str in job_arrays:
            try:
                arr = json.loads(f"[{arr_str}]")
                if arr and isinstance(arr[0], dict):
                    keys = set(arr[0].keys())
                    if {"title","location"} & keys or {"name","location"} & keys:
                        jobs = [{
                            "title": j.get("title") or j.get("name",""),
                            "department": j.get("department","") or j.get("team",""),
                            "location": j.get("location","") or j.get("city",""),
                            "url": j.get("url","") or j.get("link","") or j.get("applyUrl",""),
                            "posted_at": j.get("date","") or j.get("updatedAt",""),
                            "job_description": j.get("description","") or j.get("content",""),
                        } for j in arr[:50] if j.get("title") or j.get("name")]
                        if jobs:
                            return True, career_url, jobs
            except:
                pass
        return False, career_url, []
    except Exception as e:
        return False, career_url, []


async def scrape_bamboohr(client: httpx.AsyncClient, career_url: str) -> tuple[bool, str, list]:
    m = re.search(r'([\w-]+)\.bamboohr\.com', career_url)
    if not m:
        return False, career_url, []
    subdomain = m.group(1)
    url = f"https://{subdomain}.bamboohr.com/careers/list"
    try:
        r = await client.get(url, headers={**HEADERS, "Accept": "application/json"}, timeout=20)
        if r.status_code == 200:
            results = r.json().get("result", [])[:50]
            jobs = [{
                "title": j.get("jobOpeningName", ""),
                "department": j.get("departmentLabel", ""),
                "location": j.get("locationLabel", ""),
                "url": f"https://{subdomain}.bamboohr.com/careers/{j.get('id', '')}",
                "posted_at": j.get("datePosted", ""),
                "job_description": j.get("description", ""),
            } for j in results]
            return True, url, jobs
        return False, url, []
    except Exception:
        return False, url, []


async def scrape_teamtailor(client: httpx.AsyncClient, career_url: str) -> tuple[bool, str, list]:
    m = re.search(r'([\w-]+)\.teamtailor\.com', career_url)
    if not m:
        return False, career_url, []
    subdomain = m.group(1)
    url = f"https://{subdomain}.teamtailor.com/jobs.json"
    try:
        r = await client.get(url, headers={**HEADERS, "Accept": "application/json"}, timeout=20)
        if r.status_code == 200:
            raw = r.json()
            jobs_raw = raw.get("data", raw if isinstance(raw, list) else [])[:50]
            jobs = []
            for j in jobs_raw:
                attrs = j.get("attributes", j) if isinstance(j, dict) else {}
                jobs.append({
                    "title": attrs.get("title", ""),
                    "department": "",
                    "location": attrs.get("location", ""),
                    "url": attrs.get("career-page-url", career_url),
                    "posted_at": attrs.get("created-at", ""),
                    "job_description": attrs.get("body", "") or attrs.get("pitch", ""),
                })
            return True, url, jobs
        return False, url, []
    except Exception:
        return False, url, []


async def scrape_tier1(client: httpx.AsyncClient, career_url: str) -> tuple[bool, str, list]:
    """Best-effort HTML parse for static job pages."""
    try:
        r = await client.get(career_url, timeout=15, follow_redirects=True)
        if r.status_code != 200:
            return False, career_url, []
        # Look for embedded JSON-LD job postings
        ld_blocks = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', r.text, re.DOTALL)
        for block in ld_blocks:
            try:
                data = json.loads(block)
                if isinstance(data, list):
                    data = data[0]
                if data.get("@type") == "JobPosting":
                    return True, career_url, [{
                        "title": data.get("title",""),
                        "department": "",
                        "location": (data.get("jobLocation") or {}).get("address",{}).get("addressLocality",""),
                        "url": data.get("url","") or career_url,
                        "posted_at": data.get("datePosted",""),
                        "job_description": data.get("description",""),
                    }]
            except:
                pass
        # Look for common job listing patterns
        jobs = []
        # Pattern: <h2/h3 class="job-title">...</h2>
        titles = re.findall(r'<(?:h[23]|a)[^>]+(?:job-title|position-title|role-title)[^>]*>([^<]{5,80})</', r.text)
        if titles:
            jobs = [{"title": t.strip(), "department":"", "location":"", "url":career_url, "posted_at":"", "job_description":""} for t in titles[:50]]
            return True, career_url, jobs
        return False, career_url, []
    except:
        return False, career_url, []


# ─── DISPATCH ─────────────────────────────────────────────────────────────────

async def process_entry(entry, httpx_client, curl_session, semaphore, conn) -> dict:
    async with semaphore:
        company = entry["company"]
        portal_type = entry["portal_type"]
        career_url = entry.get("career_url","")
        segment = entry.get("segment","")

        verified = False
        verified_url = career_url
        jobs = []
        error = ""

        ov = ATS_OVERRIDES.get(company.lower().strip())

        try:
            # Apply override if present — replaces portal_type for dispatch
            _TYPE_MAP = {
                "greenhouse": "ATS_Greenhouse", "lever": "ATS_Lever",
                "ashby": "ATS_Ashby", "workday": "ATS_Workday",
                "workable": "ATS_Workable", "smartrecruiters": "ATS_SmartRecruiters",
                "eightfold": "ATS_Eightfold", "bamboohr": "ATS_BambooHR",
                "teamtailor": "ATS_Teamtailor",
            }
            eff_type = portal_type
            if ov:
                eff_type = _TYPE_MAP.get(ov["type"].lower(), portal_type)

            if eff_type == "ATS_Greenhouse":
                slug = ov["slug"] if ov and ov.get("slug") else greenhouse_slug(entry)
                if slug:
                    verified, verified_url, jobs = await scrape_greenhouse(httpx_client, slug)
                else:
                    error = "no_slug"

            elif eff_type == "ATS_Lever":
                slug = ov["slug"] if ov and ov.get("slug") else lever_slug(entry)
                if slug:
                    verified, verified_url, jobs = await scrape_lever(httpx_client, slug)
                else:
                    error = "no_slug"

            elif eff_type == "ATS_Ashby":
                board = ov["board"] if ov and ov.get("board") else ashby_board(entry)
                if board:
                    verified, verified_url, jobs = await scrape_ashby(httpx_client, board)
                else:
                    error = "no_board"

            elif eff_type == "ATS_Workday":
                if ov and ov.get("tenant"):
                    tenant, wdN, board = ov["tenant"], ov["wdN"], ov.get("board")
                else:
                    parts = workday_parts(entry)
                    if parts:
                        tenant, wdN, board = parts
                    else:
                        error = "no_workday_url"
                        tenant = None
                if not error:
                    if board is None:
                        board = await discover_workday_board(curl_session, tenant, wdN)
                    if board:
                        verified, verified_url, jobs = await scrape_workday(curl_session, tenant, wdN, board)
                        if not verified:
                            verified, verified_url, jobs = await scrape_workday(curl_session, tenant, wdN, tenant)
                    else:
                        error = "board_not_found"

            elif eff_type == "ATS_Workable":
                slug = workable_slug(entry)
                if slug:
                    verified, verified_url, jobs = await scrape_workable(httpx_client, slug)
                else:
                    error = "no_slug"

            elif eff_type == "ATS_SmartRecruiters":
                slug = smartrecruiters_slug(entry)
                if slug:
                    verified, verified_url, jobs = await scrape_smartrecruiters(httpx_client, slug)
                else:
                    error = "no_slug"

            elif eff_type == "ATS_Eightfold":
                verified, verified_url, jobs = await scrape_eightfold(httpx_client, career_url)

            elif eff_type == "ATS_BambooHR":
                verified, verified_url, jobs = await scrape_bamboohr(httpx_client, career_url)

            elif eff_type == "ATS_Teamtailor":
                verified, verified_url, jobs = await scrape_teamtailor(httpx_client, career_url)

            elif eff_type == "Tier2_CSR_SPA":
                verified, verified_url, jobs = await scrape_next_js(httpx_client, career_url)
                if not verified:
                    # Fallback: just verify URL is live
                    try:
                        r = await httpx_client.head(career_url, timeout=10, follow_redirects=True)
                        verified = r.status_code < 400
                        verified_url = str(r.url)
                    except:
                        pass

            elif eff_type == "Tier1_StaticHTML":
                verified, verified_url, jobs = await scrape_tier1(httpx_client, career_url)
                if not verified:
                    try:
                        r = await httpx_client.head(career_url, timeout=10, follow_redirects=True)
                        verified = r.status_code < 400
                        verified_url = str(r.url)
                    except:
                        pass

            else:
                # ATS_Taleo, ATS_SAP_SuccessFactors, etc. - just verify URL live
                try:
                    r = await httpx_client.head(career_url, timeout=10, follow_redirects=True)
                    verified = r.status_code < 400
                    verified_url = str(r.url)
                except:
                    pass

        except Exception as e:
            error = str(e)[:120]

        # Zero-job anomaly: verified but 0 jobs — API change or truly no openings
        if verified and len(jobs) == 0 and eff_type not in ("Tier2_CSR_SPA", "Tier1_StaticHTML"):
            print(f"  ⚠ ZERO_JOBS {company} [{eff_type}] — check API or no openings")

        upsert_company(conn, company, segment, career_url, portal_type,
                       verified, verified_url, len(jobs), error or None)
        if jobs:
            insert_jobs(conn, company, segment, portal_type, jobs)

        status = "✓" if verified else "✗"
        jobs_str = f"{len(jobs)} jobs" if jobs else "no jobs"
        print(f"  {status} {company:40s} [{portal_type:20s}] {jobs_str} {error}")
        sys.stdout.flush()
        return {"company": company, "verified": verified, "jobs": len(jobs)}


async def main():
    with open(JSON_PATH) as f:
        entries = json.load(f)

    conn = init_db(DB_PATH)
    print(f"DB: {DB_PATH}")
    print(f"Companies: {len(entries)}\n")

    semaphore = asyncio.Semaphore(5)  # conservative: 5 concurrent to avoid rate limits

    limits = httpx.Limits(max_keepalive_connections=20, max_connections=30)
    async with httpx.AsyncClient(headers=HEADERS, timeout=25, limits=limits,
                                  follow_redirects=True) as httpx_client:
        async with CurlSession(impersonate="chrome136") as curl_session:
            tasks = [
                process_entry(e, httpx_client, curl_session, semaphore, conn)
                for e in entries
            ]
            results = await asyncio.gather(*tasks)

    # Summary
    verified = sum(1 for r in results if r["verified"])
    with_jobs = sum(1 for r in results if r["jobs"] > 0)
    total_jobs = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]

    print(f"\n{'='*60}")
    print(f"Verified URLs:   {verified}/{len(entries)}")
    print(f"Companies w/ jobs: {with_jobs}/{len(entries)}")
    print(f"Total jobs in DB:  {total_jobs}")

    # Per-type summary
    print("\nPer portal type:")
    rows = conn.execute("""
        SELECT portal_type,
               COUNT(*) as total,
               SUM(verified) as verified,
               SUM(jobs_found) as jobs
        FROM companies
        GROUP BY portal_type
        ORDER BY total DESC
    """).fetchall()
    for r in rows:
        print(f"  {r[0]:25s} total={r[1]:3d} verified={r[2]:3d} jobs={r[3]}")

    # Sample jobs
    print("\nSample jobs (first 10):")
    for row in conn.execute("SELECT company, portal_type, title, location FROM jobs LIMIT 10"):
        print(f"  {row[0]:30s} {row[2][:50]:50s} {row[3]}")

    conn.close()


if __name__ == "__main__":
    asyncio.run(main())
