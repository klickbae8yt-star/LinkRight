"""
Validation Pipeline — runs between classify_career_urls.py and scrape_jobs.py.

Every URL must pass 3 gates before being written/kept in DB:
  Gate 1: HTTP reachability  (curl_cffi chrome136)
  Gate 2: ATS board existence (Greenhouse/Lever/Ashby API calls)
  Gate 3: Workday error type  (geo-block vs wrong-board vs anti-bot)

Outputs:
  - DB: companies.validation_status column updated
  - db/quarantine.json: entries that failed (with reason)
  - Console: per-company pass/fail report
"""

import asyncio
import json
import re
import sqlite3
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import httpx
from curl_cffi.requests import AsyncSession

BASE = Path(__file__).parent.parent
JSON_PATH = BASE / "db" / "career_urls_result.json"
DB_PATH   = BASE / "db" / "jobs.db"
QUARANTINE_PATH = BASE / "db" / "quarantine.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

CAREER_KWS = {"career", "job", "hire", "work", "talent", "vacancy", "recruit",
               "greenhouse", "lever", "ashby", "workday", "smartrecruiters",
               "workable", "eightfold", "bamboohr", "teamtailor"}

ATS_DOMAINS = {"greenhouse.io", "lever.co", "ashbyhq.com", "myworkdayjobs.com",
               "smartrecruiters.com", "workable.com", "eightfold.ai",
               "bamboohr.com", "teamtailor.com", "taleo.net", "successfactors.com"}

# ─── SLUG EXTRACTORS ──────────────────────────────────────────────────────────
# Slug can be in career_url OR in classification_source (e.g. "known_ats: boards.greenhouse.io/careem")

def _slug(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text or "", re.I)
    return m.group(1).rstrip("/") if m else None

def greenhouse_slug(entry: dict) -> str | None:
    combined = (entry.get("career_url","") + " " + entry.get("classification_source",""))
    return _slug(combined, r"greenhouse\.io/([^/?#\s\"\']+)")

def lever_slug(entry: dict) -> str | None:
    combined = (entry.get("career_url","") + " " + entry.get("classification_source",""))
    return _slug(combined, r"lever\.co/([^/?#\s\"\']+)")

def ashby_board(entry: dict) -> str | None:
    combined = (entry.get("career_url","") + " " + entry.get("classification_source",""))
    return _slug(combined, r"ashbyhq\.com/([^/?#\s\"\']+)")

def workday_parts(entry: dict) -> tuple[str, int, str] | None:
    combined = (entry.get("career_url","") + " " + entry.get("classification_source",""))
    m = re.search(
        r"([\w-]+)\.(wd\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/?#\s\"\']+)",
        combined, re.I)
    if m:
        tenant = m.group(1)
        wdN = int(re.search(r"\d+", m.group(2)).group())
        board = m.group(3)
        return tenant, wdN, board
    return None

# Workday overrides for companies where career_url is company site, not Workday URL
# (copied from scrape_jobs.py ATS_OVERRIDES — keep in sync)
WORKDAY_OVERRIDES: dict[str, tuple[str, int, str]] = {
    "uber":                   ("uber",              5,  "Uber_Career"),
    "atlassian":              ("atlassian",          5,  "atlassian"),
    "salesforce":             ("salesforce",         12, "External_Career_Site"),
    "walmart global tech":    ("walmart",            5,  "WalmartExternal"),
    "linkedin":               ("linkedin",           5,  "LinkedIn"),
    "booking.com":            ("booking",            3,  "ExternalCareerSite"),
    "cisco":                  ("cisco",              5,  "External"),
    "intuit":                 ("intuit",             5,  "Intuit_Careers"),
    "grab":                   ("grab",               5,  "careers"),
    "apple":                  ("apple",              5,  "External"),
    "netflix":                ("netflix",            5,  "NetflixJobs"),
    "servicenow":             ("servicenow",         5,  "External"),
    "expedia group":          ("expedia",            5,  "expedia_group"),
    "visa":                   ("visa",               5,  "External"),
    "rakuten india":          ("rakuten",            3,  "rakuten"),
    "broadcom (vmware)":      ("broadcom",           1,  "ExternalJobBoard"),
    "tesco technology":       ("tesco",              3,  "External"),
    "philips healthtech":     ("philips",            3,  "External"),
    "yahoo! india":           ("yahooinc",           5,  "Yahoo"),
    "citrix (cloud software group)": ("cloudsoftwaregroup", 5, "External"),
    "trellix":                ("trellix",            1,  "External"),
    "akamai technologies":    ("akamai",             1,  "akamai"),
    "gartner":                ("gartner",            5,  "External"),
    "ge healthcare":          ("gehealthcare",       5,  "External"),
    "nutanix":                ("nutanix",            5,  "External"),
    "disney+ hotstar":        ("disney",             5,  "DisneyExperiencesJobs"),
    "zoom video communications": ("zoom",            5,  "External"),
    "mastercard":             ("mastercard",         1,  "CorporateCareers"),
    "myntra":                 ("myntra",             5,  "myntra"),
    "qualcomm":               ("qualcomm",           5,  "External"),
    "goldman sachs (tech)":   ("gs",                 5,  "GSExternal"),
    "makemytrip":             ("makemytrip",         5,  "makemytrip"),
    "sony india software centre": ("sony",           5,  "sony_global_ext"),
    "cigna middle east":      ("cigna",              5,  "External"),
    "seera group":            ("seera",              3,  "External"),
    "adcb (digital hub)":     ("adcb",               3,  "ADCB"),
}


# ─── CROSS-FIELD CONSISTENCY ─────────────────────────────────────────────────
# For ATS types where the ATS domain MUST appear in career_url or classification_source.
# Catches data errors like portal_type=ATS_Greenhouse but career_url pointing to Workable.

_ATS_DOMAIN_REQUIRED = {
    "ATS_Greenhouse":      "greenhouse.io",
    "ATS_Lever":           "lever.co",
    "ATS_Ashby":           "ashbyhq.com",
    "ATS_Workable":        "workable.com",
    "ATS_SmartRecruiters": "smartrecruiters.com",
    "ATS_Teamtailor":      "teamtailor.com",
    "ATS_BambooHR":        "bamboohr.com",
}

_TRUSTED_SOURCES = ("agent_verified", "corrected:", "manual:", "known_ats:")

def cross_validate_entry(entry: dict) -> str | None:
    pt = entry.get("portal_type", "")
    if pt not in _ATS_DOMAIN_REQUIRED:
        return None
    src = (entry.get("classification_source","") or "").lower()
    # Skip cross-validation when classification was manually/agent-verified.
    # Those override URL-pattern heuristics.
    if any(t in src for t in _TRUSTED_SOURCES):
        return None
    required = _ATS_DOMAIN_REQUIRED[pt]
    combined = (entry.get("career_url","") + " " + src).lower()
    if required not in combined:
        return f"CROSS_VALIDATE: {pt} but no {required} in url/source"
    return None


# ─── GATE 1: HTTP REACHABILITY ────────────────────────────────────────────────

async def gate_http(session: AsyncSession, url: str) -> tuple[bool, str, str]:
    """
    Returns (passed, final_url, rejection_reason).
    rejection_reason is "" on pass.
    """
    if not url:
        return False, url, "NO_URL"

    # LinkedIn always returns 999 to bots — treat as pass
    if "linkedin.com" in url:
        return True, url, ""

    try:
        r = await session.get(url, headers=HEADERS, timeout=15,
                               allow_redirects=True, impersonate="chrome136")
        final = str(r.url)
        status = r.status_code

        # Definitive failures
        if status == 0:
            return False, url, "TIMEOUT_OR_DNS_FAIL"

        # Domain squatting
        if "sedo.com" in final or "sedoparking.com" in final:
            return False, url, "DOMAIN_SQUATTED"

        orig_domain = urlparse(url).netloc.lstrip("www.")
        final_domain = urlparse(final).netloc.lstrip("www.")

        # For known ATS domains: 404/500 = SPA or geo-block, not dead URL.
        # Gate 2 (ATS board API) does the real verification.
        if any(d in orig_domain for d in ATS_DOMAINS):
            if status in (404, 500):
                return True, url, ""

        if status == 404:
            return False, url, "HTTP_404"

        # 403/418 on correct domain = bot block, but URL is real
        if status in (403, 418):
            if orig_domain in final_domain or any(d in final_domain for d in ATS_DOMAINS):
                return True, final, ""
            return False, final, f"HTTP_{status}_WRONG_DOMAIN:{final_domain}"

        # 200/301/302 — check if redirected to homepage (no career keyword)
        if status < 400:
            orig_has_kw   = any(kw in url.lower() for kw in CAREER_KWS)
            final_has_kw  = any(kw in final.lower() for kw in CAREER_KWS)
            # If both original and final have no career keyword → likely homepage
            if not orig_has_kw and not final_has_kw:
                # Allow if redirected to ATS domain
                if not any(d in final_domain for d in ATS_DOMAINS):
                    return False, final, f"HOMEPAGE_REDIRECT:{final[:80]}"
            return True, final, ""

        return False, url, f"HTTP_{status}"

    except Exception as e:
        err = str(e)
        if "Could not resolve host" in err or "nodename nor servname" in err:
            return False, url, "DNS_FAIL"
        if "timed out" in err.lower() or "ConnectTimeout" in err:
            return False, url, "TIMEOUT"
        return False, url, f"EXCEPTION:{err[:80]}"


# ─── GATE 2: ATS BOARD EXISTENCE ──────────────────────────────────────────────

async def gate_ats_board(client: httpx.AsyncClient,
                          portal_type: str, entry: dict) -> tuple[bool, str]:
    """
    Returns (passed, rejection_reason).
    Only runs for Greenhouse / Lever / Ashby — verifies board exists via API.
    """

    if portal_type == "ATS_Greenhouse":
        slug = greenhouse_slug(entry)
        if not slug:
            return False, "GREENHOUSE_NO_SLUG"
        try:
            r = await client.get(
                f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs",
                timeout=10)
            if r.status_code == 404:
                return False, f"GREENHOUSE_BOARD_404:{slug}"
            if r.status_code == 200:
                data = r.json()
                if "jobs" not in data and "errorCode" in data:
                    return False, "GREENHOUSE_SCHEMA_ERROR"
                return True, ""
            return True, ""  # 403 etc — board likely exists, bot-blocked
        except Exception:
            return True, ""  # Network error → don't reject

    if portal_type == "ATS_Lever":
        slug = lever_slug(entry)
        if not slug:
            return False, "LEVER_NO_SLUG"
        try:
            r = await client.get(
                f"https://api.lever.co/v0/postings/{slug}?mode=json&limit=1",
                timeout=10)
            if r.status_code == 404:
                return False, f"LEVER_404:{slug}"
            return True, ""
        except Exception:
            return True, ""

    if portal_type == "ATS_Ashby":
        board = ashby_board(entry)
        if not board:
            return False, "ASHBY_NO_BOARD_ID"
        try:
            r = await client.get(
                f"https://api.ashbyhq.com/posting-api/job-board/{board}",
                timeout=10)
            if r.status_code == 404:
                return False, f"ASHBY_BOARD_404:{board}"
            if r.status_code == 200:
                data = r.json()
                if "jobs" not in data and "jobPostings" not in data:
                    return False, f"ASHBY_SCHEMA_CHANGED:keys={list(data.keys())[:5]}"
                return True, ""
            return True, ""
        except Exception:
            return True, ""

    return True, ""


# ─── GATE 3: WORKDAY ERROR TYPE ───────────────────────────────────────────────

async def gate_workday(curl_session: AsyncSession,
                        entry: dict) -> tuple[bool, str, str]:
    """
    Returns (passed, status_label, rejection_reason).
    Distinguishes: WORKING | GEO_BLOCKED | WRONG_BOARD | ANTI_BOT_INDIA
    Triggers for ATS_Workday regardless of whether career_url is a Workday URL.
    Uses WORKDAY_OVERRIDES for companies whose career_url is the company site.
    """
    company_key = entry.get("company", "").lower().strip()
    url = entry.get("career_url", "")

    # Resolve tenant/wdN/board: URL first, then overrides
    parts = workday_parts(entry)
    override_used = company_key in WORKDAY_OVERRIDES  # trust manual curation always
    if not parts:
        override = WORKDAY_OVERRIDES.get(company_key)
        if override:
            tenant, wdN, board = override
        else:
            return True, "NO_WORKDAY_PARAMS", ""  # can't verify, don't block
    else:
        tenant, wdN, board = parts
    endpoint = (f"https://{tenant}.wd{wdN}.myworkdayjobs.com"
                f"/wday/cxs/{tenant}/{board}/jobs")

    try:
        # First, GET the board page — reveals if tenant exists at all
        get_r = await curl_session.get(
            f"https://{tenant}.wd{wdN}.myworkdayjobs.com/{board}",
            timeout=12, allow_redirects=True, impersonate="chrome136")
        get_status = get_r.status_code

        if get_status == 404:
            # India often returns 404 (not 500) for geo-blocked Workday tenants
            if override_used:
                return True, "GEO_BLOCKED", ""
            return False, "WRONG_BOARD", f"WORKDAY_BOARD_404:{board}"

        # Now POST the jobs API
        post_r = await curl_session.post(
            endpoint,
            json={"appliedFacets": {}, "limit": 1, "offset": 0, "searchText": ""},
            headers={**HEADERS, "Content-Type": "application/json"},
            timeout=15, impersonate="chrome136")
        post_status = post_r.status_code

        if post_status == 200:
            return True, "WORKING", ""

        if post_status in (403, 422):
            if get_status < 400:
                return True, "ANTI_BOT_INDIA", ""
            if override_used:
                return True, "GEO_BLOCKED", ""
            return False, "ANTI_BOT_UNREACHABLE", f"WORKDAY_{post_status}_GET_{get_status}"

        if post_status == 500 or get_status == 500:
            return True, "GEO_BLOCKED", ""

        if override_used:
            return True, "GEO_BLOCKED", ""
        return False, f"UNKNOWN_{post_status}", f"WORKDAY_POST_{post_status}"

    except Exception as e:
        err = str(e)
        if "timed out" in err.lower():
            # Timeout on Workday = almost always geo-block (India)
            return True, "GEO_BLOCKED", ""
        return False, "EXCEPTION", f"WORKDAY_ERR:{err[:60]}"


# ─── DB ───────────────────────────────────────────────────────────────────────

def _add_validation_column(conn: sqlite3.Connection):
    cols = {r[1] for r in conn.execute("PRAGMA table_info(companies)")}
    if "validation_status" not in cols:
        conn.execute("ALTER TABLE companies ADD COLUMN validation_status TEXT")
    if "validation_reason" not in cols:
        conn.execute("ALTER TABLE companies ADD COLUMN validation_reason TEXT")
    if "validated_at" not in cols:
        conn.execute("ALTER TABLE companies ADD COLUMN validated_at TEXT")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quarantine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            segment TEXT,
            career_url TEXT,
            portal_type TEXT,
            rejection_reason TEXT,
            quarantined_at TEXT
        )
    """)
    conn.commit()


def _write_result(conn: sqlite3.Connection, entry: dict,
                   status: str, reason: str):
    # UPDATE-only used to fail silently for companies appended to JSON
    # but not yet in companies table. Now ensure row exists first.
    conn.execute("""
        INSERT INTO companies (company, segment, career_url, portal_type, classification_source,
                                validation_status, validation_reason, validated_at)
        VALUES (?,?,?,?,?,?,?,?)
        ON CONFLICT(company) DO UPDATE SET
            segment=COALESCE(excluded.segment, companies.segment),
            career_url=COALESCE(excluded.career_url, companies.career_url),
            portal_type=COALESCE(excluded.portal_type, companies.portal_type),
            classification_source=COALESCE(excluded.classification_source, companies.classification_source),
            validation_status=excluded.validation_status,
            validation_reason=excluded.validation_reason,
            validated_at=excluded.validated_at
    """, (entry["company"], entry.get("segment",""), entry.get("career_url",""),
          entry.get("portal_type",""), entry.get("classification_source",""),
          status, reason or None, datetime.now().isoformat()))


def _quarantine(conn: sqlite3.Connection, entry: dict, reason: str):
    conn.execute("""
        INSERT INTO quarantine (company, segment, career_url, portal_type,
                                rejection_reason, quarantined_at)
        VALUES (?,?,?,?,?,?)
        ON CONFLICT DO NOTHING
    """, (entry["company"], entry.get("segment", ""),
          entry.get("career_url", ""), entry.get("portal_type", ""),
          reason, datetime.now().isoformat()))


# ─── MAIN ─────────────────────────────────────────────────────────────────────

async def validate_entry(entry: dict,
                          curl_session: AsyncSession,
                          http_client: httpx.AsyncClient,
                          sem: asyncio.Semaphore,
                          conn: sqlite3.Connection) -> dict:
    async with sem:
        company     = entry["company"]
        url         = entry.get("career_url", "")
        portal_type = entry.get("portal_type", "")

        label = "PASS"
        reason = ""
        workday_label = ""

        # ── Pre-gate: cross-field consistency ─────────────────────────────────
        cross_err = cross_validate_entry(entry)
        if cross_err:
            label = "FAIL_CROSS_VALIDATE"
            reason = cross_err
            _write_result(conn, entry, label, reason)
            _quarantine(conn, entry, reason)
            conn.commit()
            print(f"  ✗ [{'FAIL_CROSS_VALIDATE':22s}] {company:40s} ← {reason}")
            return {"company": company, "label": label, "reason": reason}

        # ── Gate 1: HTTP ──────────────────────────────────────────────────────
        g1_pass, final_url, g1_reason = await gate_http(curl_session, url)
        if not g1_pass:
            label = "FAIL_HTTP"
            reason = g1_reason
        else:
            url = final_url  # use redirected URL going forward

            # ── Gate 2: ATS board (Greenhouse / Lever / Ashby only) ───────────
            g2_pass, g2_reason = await gate_ats_board(http_client, portal_type, entry)
            if not g2_pass:
                label = "FAIL_ATS_BOARD"
                reason = g2_reason
            else:
                # ── Gate 3: Workday error classification ─────────────────────
                if portal_type == "ATS_Workday":
                    g3_pass, workday_label, g3_reason = await gate_workday(
                        curl_session, entry)
                    if not g3_pass:
                        label = "FAIL_WORKDAY"
                        reason = g3_reason
                    elif workday_label in ("GEO_BLOCKED", "ANTI_BOT_INDIA"):
                        label = workday_label  # pass but flagged
                        reason = g3_reason
                    else:
                        label = "PASS"

        # ── Write result ──────────────────────────────────────────────────────
        _write_result(conn, entry, label, reason)
        if label.startswith("FAIL"):
            _quarantine(conn, entry, reason)
        conn.commit()

        # ── Console output ────────────────────────────────────────────────────
        icon = "✓" if label == "PASS" else ("⚠" if "GEO" in label or "ANTI_BOT" in label else "✗")
        extra = f" [{workday_label}]" if workday_label else ""
        extra += f" ← {reason}" if reason else ""
        print(f"  {icon} [{label:22s}] {company:40s}{extra}")

        return {"company": company, "label": label, "reason": reason}


async def main():
    with open(JSON_PATH) as f:
        entries = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    _add_validation_column(conn)

    print(f"Validating {len(entries)} companies through 3 gates...\n")

    sem = asyncio.Semaphore(8)
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)

    async with AsyncSession(impersonate="chrome136") as curl_session:
        async with httpx.AsyncClient(timeout=12, limits=limits,
                                      follow_redirects=True) as http_client:
            tasks = [
                validate_entry(e, curl_session, http_client, sem, conn)
                for e in entries
            ]
            results = await asyncio.gather(*tasks)

    # ── Summary ───────────────────────────────────────────────────────────────
    counts: defaultdict[str, int] = defaultdict(int)
    for r in results:
        counts[r["label"]] += 1

    print(f"\n{'='*65}")
    print(f"VALIDATION SUMMARY — {len(entries)} companies")
    print(f"{'='*65}")
    for label, count in sorted(counts.items(), key=lambda x: -x[1]):
        icon = "✓" if label == "PASS" else ("⚠" if "GEO" in label or "ANTI_BOT" in label else "✗")
        print(f"  {icon} {label:30s}: {count:3d}")

    fail_count = sum(v for k, v in counts.items() if k.startswith("FAIL"))
    warn_count = sum(v for k, v in counts.items()
                     if "GEO" in k or "ANTI_BOT" in k)
    pass_count = counts.get("PASS", 0)

    print(f"\n  PASS (clean):        {pass_count}")
    print(f"  WARN (geo/anti-bot): {warn_count}  ← URL correct, scraping blocked")
    print(f"  FAIL (bad URL/ATS):  {fail_count}  ← investigate + fix before scraping")

    # ── Save quarantine to JSON ───────────────────────────────────────────────
    quarantine_rows = conn.execute(
        "SELECT company, segment, career_url, portal_type, rejection_reason "
        "FROM quarantine ORDER BY quarantined_at DESC"
    ).fetchall()
    if quarantine_rows:
        quarantine_data = [
            {"company": r[0], "segment": r[1], "career_url": r[2],
             "portal_type": r[3], "rejection_reason": r[4]}
            for r in quarantine_rows
        ]
        with open(QUARANTINE_PATH, "w") as f:
            json.dump(quarantine_data, f, indent=2)
        print(f"\n  Quarantine saved → {QUARANTINE_PATH} ({len(quarantine_rows)} entries)")

    conn.close()
    return results


if __name__ == "__main__":
    asyncio.run(main())
