"""
Career URL Finder & Portal Type Classifier v2
- Async httpx: parallel checks, fast timeouts
- Incremental JSON saves after every company
- Tier 1/2/3 detection from page source signals
"""

import asyncio
import json
import re
import time
from pathlib import Path
from collections import Counter
from urllib.parse import urlparse
import httpx

OUTPUT_FILE = Path(__file__).parent.parent / "db" / "career_urls_result.json"

# ATS URL pattern → portal type
ATS_PATTERNS = [
    (r"myworkdayjobs\.com", "ATS_Workday"),
    (r"greenhouse\.io", "ATS_Greenhouse"),
    (r"jobs\.lever\.co", "ATS_Lever"),
    (r"ashbyhq\.com", "ATS_Ashby"),
    (r"teamtailor\.com", "ATS_Teamtailor"),
    (r"smartrecruiters\.com", "ATS_SmartRecruiters"),
    (r"apply\.workable\.com", "ATS_Workable"),
    (r"bamboohr\.com", "ATS_BambooHR"),
    (r"taleo\.net", "ATS_Taleo"),
    (r"icims\.com", "ATS_iCIMS"),
    (r"eightfold\.ai", "ATS_Eightfold"),
    (r"successfactors\.com", "ATS_SAP_SuccessFactors"),
    (r"jobs\.sap\.com", "ATS_SAP_SuccessFactors"),
    (r"jobvite\.com", "ATS_Jobvite"),
    (r"phenom\.com", "ATS_Phenom"),
    (r"breezy\.hr", "ATS_Breezy"),
    (r"recruitee\.com", "ATS_Recruitee"),
    (r"dover\.com/careers", "ATS_Dover"),
    (r"oraclecloud\.com/hcmUI", "ATS_Oracle_HCM"),
    (r"rippling\.com/jobs", "ATS_Rippling"),
    (r"pinpoint\.co", "ATS_Pinpoint"),
]

# Tier detection signals in page HTML source
TIER2_SIGNALS = [
    r'<script id="__NEXT_DATA__"',       # Next.js
    r'data-nuxt',                         # Nuxt.js
    r'window\.__INITIAL_STATE__',         # generic SPA
    r'window\.__APOLLO_STATE__',          # Apollo/GraphQL SPA
    r'<div id="root">',                  # React CRA
    r'<div id="app">',                   # Vue
    r'"__NEXT_DATA__"',
    r'/_next/static',
    r'/static/js/main\.',
    r'react-dom',
    r'vue\.js',
    r'angular\.js',
    r'ember\.js',
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def classify_by_url(url: str) -> str | None:
    if not url:
        return None
    for pattern, ats_type in ATS_PATTERNS:
        if re.search(pattern, url.lower()):
            return ats_type
    return None

def classify_by_body(body: str) -> str:
    # Check iframe src for embedded ATS before checking body text
    for src in re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', body, re.IGNORECASE):
        ats = classify_by_url(src)
        if ats:
            return ats

    for signal in TIER2_SIGNALS:
        if re.search(signal, body, re.IGNORECASE):
            return "Tier2_CSR_SPA"
    # Minimal HTML = Tier 1
    if len(body) < 5000 and "<script" not in body.lower():
        return "Tier1_StaticHTML"
    if "<table" in body.lower() and "job" in body.lower():
        return "Tier1_StaticHTML"
    return "Tier1_StaticHTML"  # default for non-SPA custom sites

_CAREER_KWS = ["career", "job", "hire", "work", "talent", "vacancy", "recruit"]

async def check_sitemap_rss(client: httpx.AsyncClient, first_candidate: str) -> str | None:
    """Check sitemap.xml and RSS feeds for a career URL before trying candidates."""
    parsed = urlparse(first_candidate)
    if not parsed.netloc:
        return None
    root = f"{parsed.scheme}://{parsed.netloc}"

    # Try sitemap.xml — find career-related <loc> entries
    for sitemap_path in ["/sitemap.xml", "/sitemap_index.xml"]:
        try:
            r = await client.get(root + sitemap_path, headers=HEADERS,
                                 follow_redirects=True, timeout=8)
            if r.status_code == 200 and "xml" in r.headers.get("content-type", ""):
                for loc in re.findall(r'<loc>([^<]+)</loc>', r.text):
                    if any(kw in loc.lower() for kw in _CAREER_KWS):
                        ats = classify_by_url(loc)
                        if ats or parsed.netloc in loc:
                            return loc.strip()
        except Exception:
            pass

    # Try RSS/XML job feeds
    for feed_path in ["/jobs.rss", "/feed.xml", "/jobs.xml", "/careers.rss"]:
        try:
            r = await client.get(root + feed_path, headers=HEADERS,
                                 follow_redirects=True, timeout=8)
            if r.status_code == 200:
                links = re.findall(r'<link>([^<]+)</link>', r.text)
                for link in links:
                    if any(kw in link.lower() for kw in _CAREER_KWS):
                        return link.strip()
        except Exception:
            pass

    return None


async def check_url_async(client: httpx.AsyncClient, url: str) -> tuple[str, int, str]:
    """Returns (final_url, status_code, body_snippet)"""
    try:
        r = await client.get(url, headers=HEADERS, follow_redirects=True, timeout=8)
        body = r.text[:8000] if r.text else ""
        return str(r.url), r.status_code, body
    except Exception:
        return url, 0, ""


async def verify_ats_via_api(client: httpx.AsyncClient, url: str) -> bool:
    """For a guessed ATS URL, verify board exists via the public API.
    Returns True if API returns 200 (board exists), False otherwise.
    Critical: prevents 403 bot-blocks from being mis-accepted as 'valid ATS board'.
    """
    m = re.search(r"boards\.greenhouse\.io/([^/?#]+)", url)
    if m:
        try:
            r = await client.get(f"https://boards-api.greenhouse.io/v1/boards/{m.group(1)}/jobs",
                                  timeout=8)
            return r.status_code == 200
        except Exception:
            return False

    m = re.search(r"jobs\.lever\.co/([^/?#]+)", url)
    if m:
        try:
            r = await client.get(f"https://api.lever.co/v0/postings/{m.group(1)}?limit=1",
                                  timeout=8)
            return r.status_code == 200
        except Exception:
            return False

    m = re.search(r"jobs\.ashbyhq\.com/([^/?#]+)", url)
    if m:
        try:
            r = await client.get(f"https://api.ashbyhq.com/posting-api/job-board/{m.group(1)}",
                                  timeout=8)
            return r.status_code == 200
        except Exception:
            return False

    return True  # Not a known ATS URL → can't verify, let caller decide

async def process_company(client: httpx.AsyncClient, entry: dict) -> dict:
    company = entry["company"]
    segment = entry["segment"]
    candidates = list(entry["candidates"])

    # Step 0: sitemap/RSS check — may surface a better career URL before trying candidates
    if candidates:
        sitemap_url = await check_sitemap_rss(client, candidates[0])
        if sitemap_url and sitemap_url not in candidates:
            candidates.insert(0, sitemap_url)

    for candidate in candidates:
        final_url, code, body = await check_url_async(client, candidate)
        if code in (200, 301, 302, 403):
            # Classify
            ats_type = classify_by_url(final_url) or classify_by_url(candidate)

            # CRITICAL: HTML pages of ATS boards return misleading status codes:
            #   - Greenhouse/Lever: 403 for any slug (real or fake)
            #   - Ashby: 200 for any slug (SPA shell always loads)
            # ALWAYS verify via ATS API when an ATS pattern matches.
            # verify_ats_via_api() returns True for non-ATS or unverified types.
            if ats_type and not await verify_ats_via_api(client, candidate):
                continue  # board doesn't exist — try next candidate

            if ats_type:
                portal_type = ats_type
            elif code == 200 and body:
                portal_type = classify_by_body(body)
            else:
                portal_type = "Tier3_ProtectedAPI" if code == 403 else "Custom_Career_Site"

            return {
                "company": company,
                "segment": segment,
                "career_url": final_url,
                "http_status": code,
                "portal_type": portal_type,
                "source_candidate": candidate,
            }

    return {
        "company": company,
        "segment": segment,
        "career_url": candidates[0],
        "http_status": 0,
        "portal_type": "URL_Not_Verified",
        "source_candidate": candidates[0],
    }

COMPANIES = [
  # SEGMENT 1: Big Tech & Tier-1 MNCs (India)
  {"company": "Google", "segment": "india_mnc", "candidates": ["https://careers.google.com"]},
  {"company": "Microsoft", "segment": "india_mnc", "candidates": ["https://careers.microsoft.com"]},
  {"company": "Amazon", "segment": "india_mnc", "candidates": ["https://amazon.jobs"]},
  {"company": "Uber", "segment": "india_mnc", "candidates": ["https://www.uber.com/us/en/careers/","https://boards.greenhouse.io/uber"]},
  {"company": "Flipkart", "segment": "india_mnc", "candidates": ["https://www.flipkartcareers.com","https://jobs.lever.co/flipkart"]},
  {"company": "Swiggy", "segment": "india_mnc", "candidates": ["https://careers.swiggy.com","https://jobs.lever.co/swiggy"]},
  {"company": "Atlassian", "segment": "india_mnc", "candidates": ["https://www.atlassian.com/company/careers","https://boards.greenhouse.io/atlassian"]},
  {"company": "Adobe", "segment": "india_mnc", "candidates": ["https://adobe.wd5.myworkdayjobs.com/external_experienced","https://www.adobe.com/careers.html"]},
  {"company": "Salesforce", "segment": "india_mnc", "candidates": ["https://careers.salesforce.com","https://salesforce.wd12.myworkdayjobs.com/External_Career_Site"]},
  {"company": "Walmart Global Tech", "segment": "india_mnc", "candidates": ["https://careers.walmart.com","https://walmart.wd5.myworkdayjobs.com/WalmartExternal"]},
  {"company": "NVIDIA", "segment": "india_mnc", "candidates": ["https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite","https://www.nvidia.com/en-us/about-nvidia/careers/"]},
  {"company": "LinkedIn", "segment": "india_mnc", "candidates": ["https://careers.linkedin.com"]},
  {"company": "PayPal", "segment": "india_mnc", "candidates": ["https://careers.pypl.com","https://paypal.eightfold.ai/careers"]},
  {"company": "PhonePe", "segment": "india_mnc", "candidates": ["https://careers.phonepe.com","https://jobs.lever.co/phonepe"]},
  {"company": "Zepto", "segment": "india_mnc", "candidates": ["https://jobs.lever.co/zepto","https://www.zeptonow.com/careers"]},
  {"company": "Zomato / Blinkit", "segment": "india_mnc", "candidates": ["https://www.zomato.com/careers","https://careers.zomato.com"]},
  {"company": "Razorpay", "segment": "india_mnc", "candidates": ["https://razorpay.com/jobs","https://jobs.lever.co/razorpay"]},
  {"company": "Booking.com", "segment": "india_mnc", "candidates": ["https://careers.booking.com"]},
  {"company": "Oracle", "segment": "india_mnc", "candidates": ["https://www.oracle.com/careers","https://oracle.taleo.net/careersection/2/jobsearch.ftl"]},
  {"company": "Cisco", "segment": "india_mnc", "candidates": ["https://jobs.cisco.com","https://cisco.wd5.myworkdayjobs.com/External"]},
  {"company": "Intuit", "segment": "india_mnc", "candidates": ["https://jobs.intuit.com","https://intuit.wd1.myworkdayjobs.com/Intuit_Careers"]},
  {"company": "ServiceNow", "segment": "india_mnc", "candidates": ["https://careers.servicenow.com","https://servicenow.wd1.myworkdayjobs.com/External"]},
  {"company": "Twilio", "segment": "india_mnc", "candidates": ["https://www.twilio.com/en-us/company/jobs","https://boards.greenhouse.io/twilio"]},
  {"company": "Grab", "segment": "india_mnc", "candidates": ["https://grab.careers","https://jobs.lever.co/grab"]},
  {"company": "Stripe", "segment": "india_mnc", "candidates": ["https://stripe.com/jobs","https://jobs.lever.co/stripe"]},
  {"company": "Intel", "segment": "india_mnc", "candidates": ["https://www.intel.com/content/www/us/en/jobs/jobs-at-intel.html","https://intel.wd1.myworkdayjobs.com/External"]},
  {"company": "SAP", "segment": "india_mnc", "candidates": ["https://jobs.sap.com","https://www.sap.com/about/careers.html"]},
  {"company": "Myntra", "segment": "india_mnc", "candidates": ["https://myntra.com/careers","https://jobs.lever.co/myntra"]},
  {"company": "Qualcomm", "segment": "india_mnc", "candidates": ["https://www.qualcomm.com/company/careers","https://qualcomm.wd5.myworkdayjobs.com/External"]},
  {"company": "JPMorgan Chase (Tech)", "segment": "india_mnc", "candidates": ["https://careers.jpmorgan.com"]},
  {"company": "Meta", "segment": "india_mnc", "candidates": ["https://www.metacareers.com"]},
  {"company": "Apple", "segment": "india_mnc", "candidates": ["https://jobs.apple.com"]},
  {"company": "Netflix", "segment": "india_mnc", "candidates": ["https://jobs.netflix.com","https://jobs.lever.co/netflix"]},
  {"company": "Snap Inc.", "segment": "india_mnc", "candidates": ["https://careers.snap.com","https://snap.wd1.myworkdayjobs.com/en-US/roles"]},
  {"company": "Disney+ Hotstar", "segment": "india_mnc", "candidates": ["https://careers.hotstar.com","https://hotstar.wd1.myworkdayjobs.com/Careers"]},
  {"company": "Meesho", "segment": "india_mnc", "candidates": ["https://meesho.io/careers","https://jobs.lever.co/meesho"]},
  {"company": "InMobi / Glance", "segment": "india_mnc", "candidates": ["https://www.inmobi.com/company/careers","https://boards.greenhouse.io/inmobi"]},
  {"company": "Ola / Ola Electric", "segment": "india_mnc", "candidates": ["https://olaelectric.com/careers","https://jobs.lever.co/olacabs"]},
  {"company": "MakeMyTrip", "segment": "india_mnc", "candidates": ["https://careers.makemytrip.com","https://jobs.lever.co/makemytrip"]},
  {"company": "Coinbase", "segment": "india_mnc", "candidates": ["https://www.coinbase.com/careers","https://jobs.lever.co/coinbase"]},
  {"company": "Expedia Group", "segment": "india_mnc", "candidates": ["https://lifeatexpedia.com","https://expedia.wd5.myworkdayjobs.com/search"]},
  {"company": "Zoom Video Communications", "segment": "india_mnc", "candidates": ["https://careers.zoom.us","https://zoom.wd5.myworkdayjobs.com/Zoom"]},
  {"company": "Mastercard", "segment": "india_mnc", "candidates": ["https://careers.mastercard.com","https://mastercard.wd1.myworkdayjobs.com/CorporateCareers"]},
  {"company": "Visa", "segment": "india_mnc", "candidates": ["https://careers.visa.com","https://visainc.wd1.myworkdayjobs.com/Visa_Careers"]},
  {"company": "Rakuten India", "segment": "india_mnc", "candidates": ["https://rakuten.careers","https://rakuten.wd1.myworkdayjobs.com/RakutenCareers"]},
  {"company": "Sony India Software Centre", "segment": "india_mnc", "candidates": ["https://www.sonyindiasoftware.com/careers","https://sony.wd1.myworkdayjobs.com/SonyGlobal"]},
  {"company": "Goldman Sachs (Tech)", "segment": "india_mnc", "candidates": ["https://www.goldmansachs.com/careers","https://goldmansachs.wd1.myworkdayjobs.com/External_Career_Site"]},
  {"company": "Dell Technologies", "segment": "india_mnc", "candidates": ["https://jobs.dell.com","https://dell.wd1.myworkdayjobs.com/External"]},
  {"company": "Samsung R&D Institute", "segment": "india_mnc", "candidates": ["https://research.samsung.com/careers","https://samsung.wd3.myworkdayjobs.com/Samsung_Careers"]},
  {"company": "Morgan Stanley (Tech)", "segment": "india_mnc", "candidates": ["https://www.morganstanley.com/people-opportunities","https://morganstanley.wd1.myworkdayjobs.com/MS_External_Career_Site"]},
  {"company": "IBM India", "segment": "india_mnc", "candidates": ["https://www.ibm.com/employment","https://ibm.wd12.myworkdayjobs.com/External_Career_Site_IBM"]},
  {"company": "Broadcom (VMware)", "segment": "india_mnc", "candidates": ["https://careers.broadcom.com","https://broadcom.wd1.myworkdayjobs.com/External_Career_Site"]},
  {"company": "Target India", "segment": "india_mnc", "candidates": ["https://corporate.target.com/careers","https://target.wd5.myworkdayjobs.com/TargetCareers"]},
  {"company": "Tesco Technology", "segment": "india_mnc", "candidates": ["https://www.tesco-careers.com"]},
  {"company": "Hewlett Packard Enterprise", "segment": "india_mnc", "candidates": ["https://careers.hpe.com","https://hpe.wd5.myworkdayjobs.com/Jobsathpe"]},
  {"company": "Philips HealthTech", "segment": "india_mnc", "candidates": ["https://www.philips.com/a-w/about/careers.html","https://philips.wd3.myworkdayjobs.com/jobs"]},
  {"company": "Yahoo! India", "segment": "india_mnc", "candidates": ["https://yahooinc.com/careers","https://careers.yahooinc.com"]},
  {"company": "Coupang India", "segment": "india_mnc", "candidates": ["https://boards.greenhouse.io/coupang","https://www.coupang.com/np/careers"]},
  {"company": "Siemens Technology", "segment": "india_mnc", "candidates": ["https://jobs.siemens.com","https://www.siemens.com/global/en/home/company/jobs.html"]},
  {"company": "Citrix (Cloud Software Group)", "segment": "india_mnc", "candidates": ["https://www.citrix.com/about/careers","https://cloud-software-group.wd5.myworkdayjobs.com/External"]},
  {"company": "Trellix", "segment": "india_mnc", "candidates": ["https://www.trellix.com/en-us/about/careers.html","https://boards.greenhouse.io/trellix"]},
  {"company": "Juniper Networks", "segment": "india_mnc", "candidates": ["https://careers.juniper.net","https://juniper.wd1.myworkdayjobs.com/External"]},
  {"company": "Akamai Technologies", "segment": "india_mnc", "candidates": ["https://www.akamai.com/careers","https://akamai.wd1.myworkdayjobs.com/akamai-jobs"]},
  {"company": "Thomson Reuters", "segment": "india_mnc", "candidates": ["https://jobs.thomsonreuters.com","https://thomsonreuters.wd5.myworkdayjobs.com/External_Career_Site"]},
  {"company": "Electronic Arts (EA)", "segment": "india_mnc", "candidates": ["https://jobs.ea.com","https://ea.wd3.myworkdayjobs.com/EA_Careers"]},
  {"company": "Autodesk", "segment": "india_mnc", "candidates": ["https://www.autodesk.com/careers","https://autodesk.wd1.myworkdayjobs.com/Ext"]},
  {"company": "Honeywell Technology", "segment": "india_mnc", "candidates": ["https://careers.honeywell.com","https://honeywell.wd5.myworkdayjobs.com/Honeywell"]},
  {"company": "Gartner", "segment": "india_mnc", "candidates": ["https://jobs.gartner.com","https://gartner.wd5.myworkdayjobs.com/Gartner_Careers"]},
  {"company": "GE HealthCare", "segment": "india_mnc", "candidates": ["https://jobs.gehealthcare.com","https://gehealthcare.wd5.myworkdayjobs.com/GEHC_Careers"]},
  {"company": "Barclays", "segment": "india_mnc", "candidates": ["https://search.jobs.barclays","https://home.barclays/careers"]},
  {"company": "HP Inc.", "segment": "india_mnc", "candidates": ["https://jobs.hp.com","https://hp.wd5.myworkdayjobs.com/ExternalCareerSite"]},
  {"company": "Red Hat", "segment": "india_mnc", "candidates": ["https://www.redhat.com/en/jobs","https://boards.greenhouse.io/redhat"]},
  {"company": "Deloitte USI", "segment": "india_mnc", "candidates": ["https://careers.deloitte.com"]},
  {"company": "Societe Generale (GSC)", "segment": "india_mnc", "candidates": ["https://careers.societegenerale.com","https://careers.smartrecruiters.com/SocieteGenerale"]},
  {"company": "Amadeus", "segment": "india_mnc", "candidates": ["https://jobs.amadeus.com","https://amadeus.wd3.myworkdayjobs.com/Amadeus"]},
  {"company": "Veritas Technologies", "segment": "india_mnc", "candidates": ["https://www.veritas.com/company/careers","https://boards.greenhouse.io/veritas"]},
  {"company": "MathWorks", "segment": "india_mnc", "candidates": ["https://www.mathworks.com/company/jobs","https://mathworks.wd1.myworkdayjobs.com/Main"]},
  {"company": "NetApp", "segment": "india_mnc", "candidates": ["https://careers.netapp.com","https://netapp.wd1.myworkdayjobs.com/NetApp"]},
  {"company": "Bosch Global Tech (BGSW)", "segment": "india_mnc", "candidates": ["https://www.bosch.in/careers","https://bosch.wd3.myworkdayjobs.com/Bosch_Ext_Prtl"]},
  {"company": "Citi (Citibank Tech)", "segment": "india_mnc", "candidates": ["https://jobs.citi.com","https://citi.wd5.myworkdayjobs.com/2"]},
  {"company": "Freshworks", "segment": "india_mnc", "candidates": ["https://careers.freshworks.com","https://boards.greenhouse.io/freshworks"]},
  {"company": "Palo Alto Networks", "segment": "india_mnc", "candidates": ["https://jobs.paloaltonetworks.com","https://paloaltonetworks.wd1.myworkdayjobs.com/External"]},
  {"company": "Nutanix", "segment": "india_mnc", "candidates": ["https://www.nutanix.com/company/careers","https://nutanix.wd5.myworkdayjobs.com/Nutanix"]},
  {"company": "Acko", "segment": "india_mnc", "candidates": ["https://www.acko.com/careers","https://jobs.lever.co/acko"]},
  {"company": "Jio Platforms", "segment": "india_mnc", "candidates": ["https://careers.jio.com"]},
  {"company": "Nykaa", "segment": "india_mnc", "candidates": ["https://careers.nykaa.com","https://jobs.lever.co/nykaa"]},
  {"company": "Sprinklr", "segment": "india_mnc", "candidates": ["https://www.sprinklr.com/life/careers","https://jobs.lever.co/sprinklr"]},
  {"company": "Gupshup", "segment": "india_mnc", "candidates": ["https://www.gupshup.io/careers","https://boards.greenhouse.io/gupshup"]},
  {"company": "Splunk (Cisco)", "segment": "india_mnc", "candidates": ["https://www.splunk.com/en_us/careers.html","https://splunk.wd5.myworkdayjobs.com/SplunkCareers"]},
  {"company": "HSBC Technology", "segment": "india_mnc", "candidates": ["https://www.hsbc.com/careers","https://hsbc.wd3.myworkdayjobs.com/HSBCexternalcareers"]},
  {"company": "CRED", "segment": "india_mnc", "candidates": ["https://cred.club/careers","https://jobs.lever.co/cred"]},
  {"company": "Paytm", "segment": "india_mnc", "candidates": ["https://jobs.paytm.com","https://paytm.com/about-us/careers"]},
  {"company": "Urban Company", "segment": "india_mnc", "candidates": ["https://www.urbancompany.com/careers","https://jobs.lever.co/urbancompany"]},
  {"company": "Tata Neu (Tata Digital)", "segment": "india_mnc", "candidates": ["https://careers.tata.com","https://tatadigital.wd1.myworkdayjobs.com/TD_External"]},
  {"company": "Cars24", "segment": "india_mnc", "candidates": ["https://www.cars24.com/careers","https://jobs.lever.co/cars24"]},
  {"company": "Info Edge (Naukri)", "segment": "india_mnc", "candidates": ["https://infoedge.in/careers","https://boards.greenhouse.io/infoedge"]},
  {"company": "Dream11", "segment": "india_mnc", "candidates": ["https://dream11.com/careers","https://jobs.lever.co/dream11"]},
  {"company": "Groww", "segment": "india_mnc", "candidates": ["https://groww.in/careers","https://jobs.lever.co/groww"]},
  {"company": "Upstox", "segment": "india_mnc", "candidates": ["https://upstox.com/careers","https://jobs.lever.co/upstox"]},
  {"company": "Games24x7", "segment": "india_mnc", "candidates": ["https://www.games24x7.com/careers","https://jobs.lever.co/games24x7"]},

  # SEGMENT 2: Consumer AI Startups
  {"company": "Perplexity AI", "segment": "global_ai_startup", "candidates": ["https://jobs.ashbyhq.com/perplexity","https://www.perplexity.ai/hub/jobs"]},
  {"company": "Character.ai", "segment": "global_ai_startup", "candidates": ["https://jobs.ashbyhq.com/character","https://character.ai/careers"]},
  {"company": "Midjourney", "segment": "global_ai_startup", "candidates": ["https://www.midjourney.com/jobs","https://boards.greenhouse.io/midjourney"]},
  {"company": "ElevenLabs", "segment": "global_ai_startup", "candidates": ["https://jobs.ashbyhq.com/elevenlabs","https://elevenlabs.io/careers"]},
  {"company": "Cursor (Anysphere)", "segment": "global_ai_startup", "candidates": ["https://boards.greenhouse.io/anysphere","https://cursor.com/careers"]},
  {"company": "Suno AI", "segment": "global_ai_startup", "candidates": ["https://suno.com/careers","https://jobs.ashbyhq.com/suno"]},
  {"company": "Phind", "segment": "global_ai_startup", "candidates": ["https://www.phind.com/careers","https://jobs.lever.co/phind"]},
  {"company": "Limitless AI", "segment": "global_ai_startup", "candidates": ["https://limitless.ai/careers","https://jobs.ashbyhq.com/limitless"]},
  {"company": "Krea AI", "segment": "global_ai_startup", "candidates": ["https://www.krea.ai/careers","https://jobs.ashbyhq.com/krea"]},
  {"company": "Heptabase", "segment": "global_ai_startup", "candidates": ["https://heptabase.com/careers","https://jobs.ashbyhq.com/heptabase"]},
  {"company": "InVideo", "segment": "global_ai_startup", "candidates": ["https://careers.invideo.io","https://jobs.lever.co/invideo"]},
  {"company": "Gamma App", "segment": "global_ai_startup", "candidates": ["https://gamma.app/jobs","https://jobs.ashbyhq.com/gamma"]},
  {"company": "Captions", "segment": "global_ai_startup", "candidates": ["https://www.captions.ai/careers","https://jobs.ashbyhq.com/captions"]},
  {"company": "HeyGen", "segment": "global_ai_startup", "candidates": ["https://jobs.ashbyhq.com/heygen","https://www.heygen.com/careers"]},
  {"company": "The Browser Company", "segment": "global_ai_startup", "candidates": ["https://thebrowser.company/careers","https://jobs.ashbyhq.com/the-browser-company"]},
  {"company": "Luma AI", "segment": "global_ai_startup", "candidates": ["https://lumalabs.ai/careers","https://jobs.ashbyhq.com/luma-ai"]},
  {"company": "Jenni AI", "segment": "global_ai_startup", "candidates": ["https://jenni.ai/careers","https://jobs.lever.co/jenni"]},
  {"company": "Consensus", "segment": "global_ai_startup", "candidates": ["https://consensus.app/home/blog/careers","https://jobs.lever.co/consensus"]},
  {"company": "Glif", "segment": "global_ai_startup", "candidates": ["https://glif.app/careers","https://jobs.lever.co/glif"]},
  {"company": "Decart AI (Oasis)", "segment": "global_ai_startup", "candidates": ["https://decart.ai/careers","https://jobs.ashbyhq.com/decart"]},
  {"company": "Ideogram", "segment": "global_ai_startup", "candidates": ["https://ideogram.ai/about/careers","https://jobs.ashbyhq.com/ideogram"]},
  {"company": "Pika Labs", "segment": "global_ai_startup", "candidates": ["https://pika.art/careers","https://jobs.ashbyhq.com/pika"]},
  {"company": "Viggle AI", "segment": "global_ai_startup", "candidates": ["https://www.viggle.ai/careers","https://jobs.lever.co/viggle"]},
  {"company": "Granola", "segment": "global_ai_startup", "candidates": ["https://www.granola.so/jobs","https://jobs.ashbyhq.com/granola"]},
  {"company": "Opal", "segment": "global_ai_startup", "candidates": ["https://www.opal.so/jobs","https://jobs.lever.co/opal"]},
  {"company": "AudioPen", "segment": "global_ai_startup", "candidates": ["https://audiopen.ai"]},
  {"company": "Poised", "segment": "global_ai_startup", "candidates": ["https://www.poised.com/careers","https://jobs.lever.co/poised"]},
  {"company": "Tavus", "segment": "global_ai_startup", "candidates": ["https://jobs.ashbyhq.com/tavus","https://www.tavus.io/careers"]},
  {"company": "Rosebud AI", "segment": "global_ai_startup", "candidates": ["https://www.rosebud.ai/careers","https://jobs.lever.co/rosebud"]},
  {"company": "Morph Studio", "segment": "global_ai_startup", "candidates": ["https://morphstudio.com/careers","https://jobs.ashbyhq.com/morph-studio"]},
  {"company": "Hume AI", "segment": "global_ai_startup", "candidates": ["https://www.hume.ai/careers","https://jobs.ashbyhq.com/hume-ai"]},
  {"company": "Bland AI", "segment": "global_ai_startup", "candidates": ["https://www.bland.ai/careers","https://jobs.ashbyhq.com/bland-ai"]},
  {"company": "Photoroom", "segment": "global_ai_startup", "candidates": ["https://jobs.lever.co/photoroom","https://www.photoroom.com/careers"]},
  {"company": "Opus Clip", "segment": "global_ai_startup", "candidates": ["https://www.opus.pro/careers","https://jobs.ashbyhq.com/opus-clip"]},
  {"company": "Podcastle", "segment": "global_ai_startup", "candidates": ["https://podcastle.ai/careers","https://jobs.lever.co/podcastle"]},
  {"company": "Copilot Money", "segment": "global_ai_startup", "candidates": ["https://copilot.money/careers","https://jobs.lever.co/copilot"]},
  {"company": "Reka AI", "segment": "global_ai_startup", "candidates": ["https://reka.ai/careers","https://jobs.ashbyhq.com/reka-ai"]},
  {"company": "Play.ht", "segment": "global_ai_startup", "candidates": ["https://play.ht/jobs","https://jobs.lever.co/playht"]},
  {"company": "Lex (Every)", "segment": "global_ai_startup", "candidates": ["https://every.to/jobs","https://jobs.lever.co/every"]},
  {"company": "Cognition AI", "segment": "global_ai_startup", "candidates": ["https://www.cognition.ai/careers","https://jobs.ashbyhq.com/cognition"]},
  {"company": "Speak", "segment": "global_ai_startup", "candidates": ["https://www.speak.com/careers","https://boards.greenhouse.io/speak"]},
  {"company": "Julius AI", "segment": "global_ai_startup", "candidates": ["https://julius.ai/careers","https://jobs.lever.co/julius"]},
  {"company": "Jan AI", "segment": "global_ai_startup", "candidates": ["https://jan.ai/careers","https://jobs.lever.co/janhq"]},
  {"company": "Type", "segment": "global_ai_startup", "candidates": ["https://type.ai/careers","https://jobs.lever.co/type-ai"]},
  {"company": "You.com", "segment": "global_ai_startup", "candidates": ["https://you.com/careers","https://boards.greenhouse.io/youcom"]},
  {"company": "Fathom", "segment": "global_ai_startup", "candidates": ["https://fathom.video/careers","https://jobs.ashbyhq.com/fathom"]},
  {"company": "Poe (Quora)", "segment": "global_ai_startup", "candidates": ["https://www.quora.com/about/careers","https://jobs.lever.co/quora"]},
  {"company": "Otter.ai", "segment": "global_ai_startup", "candidates": ["https://otter.ai/careers","https://jobs.lever.co/otterai"]},
  {"company": "QuillBot", "segment": "global_ai_startup", "candidates": ["https://quillbot.com/jobs","https://boards.greenhouse.io/quillbot"]},
  {"company": "Minion AI", "segment": "global_ai_startup", "candidates": ["https://minion.ai/careers","https://jobs.lever.co/minionai"]},
  {"company": "Leonardo.AI", "segment": "global_ai_startup", "candidates": ["https://leonardo.ai/careers","https://jobs.ashbyhq.com/leonardo-ai"]},
  {"company": "Sizzle AI", "segment": "global_ai_startup", "candidates": ["https://sizzle.ai/careers","https://jobs.lever.co/sizzle"]},
  {"company": "Talkie AI", "segment": "global_ai_startup", "candidates": ["https://www.talkie-ai.com/careers","https://jobs.lever.co/talkie-ai"]},
  {"company": "Superwhisper", "segment": "global_ai_startup", "candidates": ["https://superwhisper.com/careers","https://jobs.lever.co/superwhisper"]},
  {"company": "MyShell", "segment": "global_ai_startup", "candidates": ["https://myshell.ai/careers","https://jobs.ashbyhq.com/myshell"]},
  {"company": "Andi Search", "segment": "global_ai_startup", "candidates": ["https://andisearch.com/careers","https://jobs.lever.co/andi-search"]},
  {"company": "Magical", "segment": "global_ai_startup", "candidates": ["https://www.getmagical.com/careers","https://jobs.lever.co/magical"]},
  {"company": "Voicify AI (Jammable)", "segment": "global_ai_startup", "candidates": ["https://jammable.com/careers","https://jobs.lever.co/jammable"]},
  {"company": "Reface", "segment": "global_ai_startup", "candidates": ["https://reface.ai/careers","https://jobs.lever.co/reface"]},
  {"company": "Lovo.ai", "segment": "global_ai_startup", "candidates": ["https://lovo.ai/careers","https://jobs.lever.co/lovo"]},
  {"company": "Genspark", "segment": "global_ai_startup", "candidates": ["https://www.genspark.ai/careers","https://jobs.ashbyhq.com/genspark"]},
  {"company": "Tome", "segment": "global_ai_startup", "candidates": ["https://tome.app/careers","https://jobs.lever.co/tome"]},
  {"company": "Confido Health", "segment": "global_ai_startup", "candidates": ["https://confidohealth.com/careers","https://jobs.ashbyhq.com/confido-health"]},
  {"company": "Dot (New Computer)", "segment": "global_ai_startup", "candidates": ["https://new.computer/careers","https://jobs.ashbyhq.com/new-computer"]},
  {"company": "Gushwork AI", "segment": "global_ai_startup", "candidates": ["https://www.gushwork.ai/careers","https://jobs.lever.co/gushwork"]},
  {"company": "Rive", "segment": "global_ai_startup", "candidates": ["https://rive.app/careers","https://jobs.lever.co/rive"]},
  {"company": "CodiumAI (Qodo)", "segment": "global_ai_startup", "candidates": ["https://www.qodo.ai/careers","https://boards.greenhouse.io/qodo"]},
  {"company": "Linum AI", "segment": "global_ai_startup", "candidates": ["https://linum.ai/careers","https://jobs.ashbyhq.com/linum"]},
  {"company": "Nekton AI", "segment": "global_ai_startup", "candidates": ["https://nekton.ai/careers","https://jobs.lever.co/nekton"]},
  {"company": "Jivi", "segment": "global_ai_startup", "candidates": ["https://www.jivi.ai/careers","https://jobs.lever.co/jivi"]},
  {"company": "Descript", "segment": "global_ai_startup", "candidates": ["https://www.descript.com/careers","https://boards.greenhouse.io/descript"]},
  {"company": "Chai AI", "segment": "global_ai_startup", "candidates": ["https://www.chai-research.com/careers","https://jobs.lever.co/chai"]},
  {"company": "Voicenotes", "segment": "global_ai_startup", "candidates": ["https://voicenotes.com/careers","https://jobs.lever.co/voicenotes"]},
  {"company": "Monica AI", "segment": "global_ai_startup", "candidates": ["https://monica.im/careers","https://jobs.lever.co/monica-ai"]},
  {"company": "HyperWrite", "segment": "global_ai_startup", "candidates": ["https://hyperwriteai.com/careers","https://jobs.lever.co/hyperwrite"]},
  {"company": "Mindy AI", "segment": "global_ai_startup", "candidates": ["https://mindy.ai/careers","https://jobs.lever.co/mindy"]},
  {"company": "Veed.io", "segment": "global_ai_startup", "candidates": ["https://www.veed.io/careers","https://jobs.lever.co/veed"]},
  {"company": "Sana Labs", "segment": "global_ai_startup", "candidates": ["https://www.sanalabs.com/careers","https://boards.greenhouse.io/sanalabs"]},
  {"company": "NovelAI", "segment": "global_ai_startup", "candidates": ["https://novelai.net/careers","https://jobs.lever.co/novelai"]},
  {"company": "Kaiber.ai", "segment": "global_ai_startup", "candidates": ["https://kaiber.ai/careers","https://jobs.ashbyhq.com/kaiber"]},
  {"company": "Hedra AI", "segment": "global_ai_startup", "candidates": ["https://www.hedra.com/careers","https://jobs.ashbyhq.com/hedra"]},
  {"company": "Kling AI (Kuaishou)", "segment": "global_ai_startup", "candidates": ["https://klingai.com/careers","https://jobs.lever.co/kuaishou"]},
  {"company": "Hailuo AI (MiniMax)", "segment": "global_ai_startup", "candidates": ["https://www.minimax.io/careers","https://jobs.ashbyhq.com/minimax"]},
  {"company": "Harmonic", "segment": "global_ai_startup", "candidates": ["https://harmonic.ai/careers","https://jobs.ashbyhq.com/harmonic"]},
  {"company": "LM Arena (LMSYS)", "segment": "global_ai_startup", "candidates": ["https://lmarena.ai/careers","https://jobs.ashbyhq.com/lmsys"]},
  {"company": "Sider AI", "segment": "global_ai_startup", "candidates": ["https://sider.ai/careers","https://jobs.lever.co/sider"]},
  {"company": "Epicenter", "segment": "global_ai_startup", "candidates": ["https://epicenter.so/careers","https://jobs.ashbyhq.com/epicenter"]},
  {"company": "Rask AI", "segment": "global_ai_startup", "candidates": ["https://www.rask.ai/careers","https://jobs.lever.co/rask-ai"]},
  {"company": "D-ID", "segment": "global_ai_startup", "candidates": ["https://www.d-id.com/careers","https://boards.greenhouse.io/did"]},
  {"company": "Klap", "segment": "global_ai_startup", "candidates": ["https://klap.app/careers","https://jobs.lever.co/klap"]},
  {"company": "Thinking Machines Lab", "segment": "global_ai_startup", "candidates": ["https://thinkingmachines.ai/careers","https://jobs.ashbyhq.com/thinking-machines"]},
  {"company": "Blue AI", "segment": "global_ai_startup", "candidates": ["https://blue.ai/careers","https://jobs.lever.co/blue-ai"]},
  {"company": "Meteor AI", "segment": "global_ai_startup", "candidates": ["https://meteor.ai/careers","https://jobs.lever.co/meteor"]},
  {"company": "Cocreate AI", "segment": "global_ai_startup", "candidates": ["https://cocreate.ai/careers","https://jobs.ashbyhq.com/cocreate"]},
  {"company": "Interface AI", "segment": "global_ai_startup", "candidates": ["https://interface.ai/careers","https://boards.greenhouse.io/interfaceai"]},
  {"company": "Udio", "segment": "global_ai_startup", "candidates": ["https://www.udio.com/careers","https://jobs.ashbyhq.com/udio"]},
  {"company": "OpenRouter", "segment": "global_ai_startup", "candidates": ["https://openrouter.ai/careers","https://jobs.ashbyhq.com/openrouter"]},
  {"company": "Clay (CRM)", "segment": "global_ai_startup", "candidates": ["https://www.clay.com/careers","https://jobs.ashbyhq.com/clay"]},
  {"company": "Listen Labs", "segment": "global_ai_startup", "candidates": ["https://listenlabs.ai/careers","https://jobs.lever.co/listen-labs"]},
  {"company": "Vanna AI", "segment": "global_ai_startup", "candidates": ["https://vanna.ai/careers","https://jobs.lever.co/vanna"]},

  # SEGMENT 3: Dubai Companies
  {"company": "Careem", "segment": "dubai_visa", "candidates": ["https://careers.careem.com","https://boards.greenhouse.io/careem"]},
  {"company": "Noon", "segment": "dubai_visa", "candidates": ["https://careers.noon.com","https://boards.greenhouse.io/noon"]},
  {"company": "Talabat", "segment": "dubai_visa", "candidates": ["https://jobs.talabat.com","https://talabat.wd3.myworkdayjobs.com/Talabat_Careers"]},
  {"company": "Majid Al Futtaim (MAF)", "segment": "dubai_visa", "candidates": ["https://careers.majidalfuttaim.com","https://maf.wd3.myworkdayjobs.com/MAF_External"]},
  {"company": "Binance", "segment": "dubai_visa", "candidates": ["https://www.binance.com/en/careers","https://jobs.lever.co/binance"]},
  {"company": "Crypto.com", "segment": "dubai_visa", "candidates": ["https://crypto.com/en/careers.html","https://boards.greenhouse.io/cryptocom"]},
  {"company": "Kitopi", "segment": "dubai_visa", "candidates": ["https://www.kitopi.com/careers","https://jobs.lever.co/kitopi"]},
  {"company": "Yassir", "segment": "dubai_visa", "candidates": ["https://yassir.com/careers","https://jobs.lever.co/yassir"]},
  {"company": "Astra Tech (Botim)", "segment": "dubai_visa", "candidates": ["https://www.astratech.com/careers","https://boards.greenhouse.io/astratech"]},
  {"company": "Tether", "segment": "dubai_visa", "candidates": ["https://tether.to/en/careers","https://jobs.lever.co/tether"]},
  {"company": "Property Finder", "segment": "dubai_visa", "candidates": ["https://www.propertyfinder.ae/en/careers","https://boards.greenhouse.io/propertyfinder"]},
  {"company": "Dubizzle (EMPG)", "segment": "dubai_visa", "candidates": ["https://careers.dubizzle.com","https://dubizzle.wd3.myworkdayjobs.com/Dubizzle_Careers"]},
  {"company": "Wio Bank", "segment": "dubai_visa", "candidates": ["https://www.wio.io/careers","https://jobs.lever.co/wio-bank"]},
  {"company": "Deliveroo UAE", "segment": "dubai_visa", "candidates": ["https://careers.deliveroo.co.uk","https://boards.greenhouse.io/deliveroo"]},
  {"company": "Mashreq Neo (Mashreq)", "segment": "dubai_visa", "candidates": ["https://www.mashreqbank.com/uae/en/about-us/careers","https://mashreq.wd1.myworkdayjobs.com/mashreqext"]},
  {"company": "Baraka", "segment": "dubai_visa", "candidates": ["https://getbaraka.com/careers","https://jobs.lever.co/baraka"]},
  {"company": "Chalhoub Group", "segment": "dubai_visa", "candidates": ["https://careers.chalhoubgroup.com","https://chalhoubgroup.wd3.myworkdayjobs.com/ChalhoubCareers"]},
  {"company": "Al Tayer Digital (Ounass)", "segment": "dubai_visa", "candidates": ["https://www.altayergroup.com/careers","https://boards.greenhouse.io/altayer"]},
  {"company": "Landmark Group", "segment": "dubai_visa", "candidates": ["https://landmarkgroup.com/careers","https://landmark.wd3.myworkdayjobs.com/LandmarkExternal"]},
  {"company": "Postpay", "segment": "dubai_visa", "candidates": ["https://postpay.io/careers","https://jobs.lever.co/postpay"]},
  {"company": "Revolut", "segment": "dubai_visa", "candidates": ["https://www.revolut.com/careers","https://boards.greenhouse.io/revolut"]},
  {"company": "Almosafer", "segment": "dubai_visa", "candidates": ["https://www.almosafer.com/en/careers","https://jobs.lever.co/almosafer"]},
  {"company": "webook.com", "segment": "dubai_visa", "candidates": ["https://webook.com/en/careers","https://jobs.lever.co/webook"]},
  {"company": "Qlub", "segment": "dubai_visa", "candidates": ["https://qlub.io/careers","https://jobs.lever.co/qlub"]},
  {"company": "Sarwa", "segment": "dubai_visa", "candidates": ["https://www.sarwa.co/careers","https://jobs.lever.co/sarwa"]},
  {"company": "SmartCrowd", "segment": "dubai_visa", "candidates": ["https://www.smartcrowd.ae/careers","https://jobs.lever.co/smartcrowd"]},
  {"company": "Emirates Group", "segment": "dubai_visa", "candidates": ["https://www.emiratesgroupcareers.com","https://ekc.wd3.myworkdayjobs.com/en-US/Emirates_External"]},
  {"company": "Flydubai", "segment": "dubai_visa", "candidates": ["https://www.flydubai.com/en/flying-with-us/careers","https://flydubai.taleo.net/careersection/2/jobsearch.ftl"]},
  {"company": "Emaar Properties (Digital)", "segment": "dubai_visa", "candidates": ["https://careers.emaar.com","https://emaar.wd3.myworkdayjobs.com/EmaarCareers"]},
  {"company": "Lean Technologies", "segment": "dubai_visa", "candidates": ["https://www.leantech.me/careers","https://jobs.lever.co/lean-technologies"]},
  {"company": "Tabby", "segment": "dubai_visa", "candidates": ["https://tabby.ai/careers","https://jobs.lever.co/tabby"]},
  {"company": "Tamara", "segment": "dubai_visa", "candidates": ["https://tamara.co/en/careers","https://boards.greenhouse.io/tamara"]},
  {"company": "Anghami", "segment": "dubai_visa", "candidates": ["https://www.anghami.com/careers","https://jobs.lever.co/anghami"]},
  {"company": "Trukker", "segment": "dubai_visa", "candidates": ["https://trukker.com/careers","https://jobs.lever.co/trukker"]},
  {"company": "Alshaya Group (Digital)", "segment": "dubai_visa", "candidates": ["https://careers.alshaya.com","https://alshaya.wd3.myworkdayjobs.com/alshaya"]},
  {"company": "GrubTech", "segment": "dubai_visa", "candidates": ["https://www.grubtech.com/careers","https://jobs.lever.co/grubtech"]},
  {"company": "Tarabut Gateway", "segment": "dubai_visa", "candidates": ["https://tarabut.com/careers","https://jobs.lever.co/tarabut"]},
  {"company": "BitOasis", "segment": "dubai_visa", "candidates": ["https://bitoasis.net/en/careers","https://boards.greenhouse.io/bitoasis"]},
  {"company": "Eyewa", "segment": "dubai_visa", "candidates": ["https://www.eyewa.com/careers","https://jobs.lever.co/eyewa"]},
  {"company": "Mumzworld", "segment": "dubai_visa", "candidates": ["https://www.mumzworld.com/en/careers","https://boards.greenhouse.io/mumzworld"]},
  {"company": "Bayut", "segment": "dubai_visa", "candidates": ["https://www.bayut.com/careers","https://boards.greenhouse.io/bayut"]},
  {"company": "Fetchr", "segment": "dubai_visa", "candidates": ["https://www.fetchr.us/careers","https://jobs.lever.co/fetchr"]},
  {"company": "Desert Control", "segment": "dubai_visa", "candidates": ["https://desertcontrol.com/careers","https://jobs.lever.co/desert-control"]},
  {"company": "Cari", "segment": "dubai_visa", "candidates": ["https://www.cari.ae/careers","https://jobs.lever.co/cari"]},
  {"company": "Swvl", "segment": "dubai_visa", "candidates": ["https://www.swvl.com/careers","https://boards.greenhouse.io/swvl"]},
  {"company": "Denarii Cash", "segment": "dubai_visa", "candidates": ["https://denariicash.com/careers","https://jobs.lever.co/denarii"]},
  {"company": "Netaq", "segment": "dubai_visa", "candidates": ["https://netaq.ae/careers","https://jobs.lever.co/netaq"]},
  {"company": "Sprii", "segment": "dubai_visa", "candidates": ["https://www.sprii.com/careers","https://jobs.lever.co/sprii"]},
  {"company": "Eureeca", "segment": "dubai_visa", "candidates": ["https://eureeca.com/careers","https://jobs.lever.co/eureeca"]},
  {"company": "Beehive", "segment": "dubai_visa", "candidates": ["https://www.beehive.ae/careers","https://jobs.lever.co/beehive-ae"]},
  {"company": "Network International", "segment": "dubai_visa", "candidates": ["https://www.networkinternational.ae/en/careers","https://ni.wd3.myworkdayjobs.com/NI_External"]},
  {"company": "Commercial Bank of Dubai (CBD)", "segment": "dubai_visa", "candidates": ["https://www.cbd.ae/careers","https://cbd.wd3.myworkdayjobs.com/CBD_External"]},
  {"company": "Invygo", "segment": "dubai_visa", "candidates": ["https://www.invygo.com/careers","https://jobs.lever.co/invygo"]},
  {"company": "Zand Bank", "segment": "dubai_visa", "candidates": ["https://www.zand.ae/careers","https://jobs.lever.co/zand"]},
  {"company": "ServiceMarket", "segment": "dubai_visa", "candidates": ["https://www.servicemarket.com/careers","https://jobs.lever.co/servicemarket"]},
  {"company": "Huspy", "segment": "dubai_visa", "candidates": ["https://www.huspy.com/careers","https://jobs.lever.co/huspy"]},
  {"company": "Hala", "segment": "dubai_visa", "candidates": ["https://hala.com/careers","https://jobs.lever.co/hala"]},
  {"company": "Rain", "segment": "dubai_visa", "candidates": ["https://rain.bh/careers","https://boards.greenhouse.io/rain"]},
  {"company": "Salla", "segment": "dubai_visa", "candidates": ["https://salla.sa/careers","https://jobs.lever.co/salla"]},
  {"company": "Liv. Bank", "segment": "dubai_visa", "candidates": ["https://www.liv.me/careers","https://jobs.lever.co/liv-bank"]},
  {"company": "Hoxton Wealth", "segment": "dubai_visa", "candidates": ["https://hoxtonwealth.com/careers","https://jobs.lever.co/hoxton-wealth"]},
  {"company": "Life Pharmacy", "segment": "dubai_visa", "candidates": ["https://www.lifepharmacy.com/en/careers","https://jobs.lever.co/life-pharmacy"]},
  {"company": "Yalla Group", "segment": "dubai_visa", "candidates": ["https://www.yallagroup.com/careers","https://boards.greenhouse.io/yallagroup"]},
  {"company": "The Open Platform (TOP)", "segment": "dubai_visa", "candidates": ["https://toplatform.com/careers","https://jobs.lever.co/top-platform"]},
  {"company": "Erad", "segment": "dubai_visa", "candidates": ["https://erad.co/careers","https://jobs.lever.co/erad"]},
  {"company": "Bamboo Card", "segment": "dubai_visa", "candidates": ["https://bamboocard.com/careers","https://jobs.lever.co/bamboo-card"]},
  {"company": "ZainTECH", "segment": "dubai_visa", "candidates": ["https://zaintech.com/careers","https://jobs.lever.co/zaintech"]},
  {"company": "Midis Group", "segment": "dubai_visa", "candidates": ["https://www.midisgroup.com/careers","https://jobs.lever.co/midis"]},
  {"company": "Future Group", "segment": "dubai_visa", "candidates": ["https://futuregroup.ae/careers","https://jobs.lever.co/future-group"]},
  {"company": "KreupAI Technologies", "segment": "dubai_visa", "candidates": ["https://kreupai.com/careers","https://jobs.lever.co/kreupai"]},
  {"company": "Lenskart (Middle East)", "segment": "dubai_visa", "candidates": ["https://careers.lenskart.com","https://lenskart.wd1.myworkdayjobs.com/Lenskart_Careers"]},
  {"company": "Paymentology", "segment": "dubai_visa", "candidates": ["https://www.paymentology.com/careers","https://boards.greenhouse.io/paymentology"]},
  {"company": "Amana Capital", "segment": "dubai_visa", "candidates": ["https://www.amana.inc/careers","https://jobs.lever.co/amana"]},
  {"company": "Edfundo", "segment": "dubai_visa", "candidates": ["https://edfundo.com/careers","https://jobs.lever.co/edfundo"]},
  {"company": "Opontia", "segment": "dubai_visa", "candidates": ["https://opontia.com/careers","https://boards.greenhouse.io/opontia"]},
  {"company": "Seva Stories", "segment": "dubai_visa", "candidates": ["https://seva.ae/careers","https://jobs.lever.co/seva"]},
  {"company": "Telr", "segment": "dubai_visa", "candidates": ["https://telr.com/careers","https://jobs.lever.co/telr"]},
  {"company": "Nomod", "segment": "dubai_visa", "candidates": ["https://nomod.com/careers","https://jobs.lever.co/nomod"]},
  {"company": "Wakecap", "segment": "dubai_visa", "candidates": ["https://wakecap.com/careers","https://boards.greenhouse.io/wakecap"]},
  {"company": "Klaim", "segment": "dubai_visa", "candidates": ["https://klaim.ai/careers","https://jobs.lever.co/klaim"]},
  {"company": "Bybit", "segment": "dubai_visa", "candidates": ["https://careers.bybit.com","https://jobs.lever.co/bybit"]},
  {"company": "Mamo Pay", "segment": "dubai_visa", "candidates": ["https://mamo.io/careers","https://jobs.lever.co/mamo"]},
  {"company": "OKX Middle East", "segment": "dubai_visa", "candidates": ["https://www.okx.com/careers","https://jobs.lever.co/okx"]},
  {"company": "PureHealth", "segment": "dubai_visa", "candidates": ["https://purehealth.ae/careers","https://purehealth.wd3.myworkdayjobs.com/PureHealth_Careers"]},
  {"company": "The Luxury Closet", "segment": "dubai_visa", "candidates": ["https://www.theluxurycloset.com/careers","https://jobs.lever.co/luxury-closet"]},
  {"company": "Justlife (Justmop)", "segment": "dubai_visa", "candidates": ["https://justlife.com/careers","https://jobs.lever.co/justlife"]},
  {"company": "Zywa", "segment": "dubai_visa", "candidates": ["https://zywa.app/careers","https://jobs.lever.co/zywa"]},
  {"company": "StashAway", "segment": "dubai_visa", "candidates": ["https://www.stashaway.com/careers","https://boards.greenhouse.io/stashaway"]},
  {"company": "Deriv", "segment": "dubai_visa", "candidates": ["https://deriv.com/careers","https://boards.greenhouse.io/deriv"]},
  {"company": "Daman Insurance", "segment": "dubai_visa", "candidates": ["https://www.damanhealth.ae/careers","https://daman.wd3.myworkdayjobs.com/Daman_External"]},
  {"company": "Starzplay", "segment": "dubai_visa", "candidates": ["https://starzplay.com/careers","https://boards.greenhouse.io/starzplay"]},
  {"company": "InstaShop", "segment": "dubai_visa", "candidates": ["https://www.instashop.com/careers","https://boards.greenhouse.io/instashop"]},
  {"company": "Emirates NBD (Digital Hub)", "segment": "dubai_visa", "candidates": ["https://www.emiratesnbd.com/en/careers","https://emiratesnbd.wd3.myworkdayjobs.com/ENBD_External"]},
  {"company": "First Abu Dhabi Bank (FAB Tech)", "segment": "dubai_visa", "candidates": ["https://www.bankfab.com/en-ae/about-fab/careers","https://fab.wd3.myworkdayjobs.com/External_Careers"]},
  {"company": "Al Futtaim Group (Digital)", "segment": "dubai_visa", "candidates": ["https://careers.alfuttaim.com","https://alfuttaim.wd3.myworkdayjobs.com/AlFuttaim"]},
  {"company": "GEMS EdTech", "segment": "dubai_visa", "candidates": ["https://gemsworld.com/careers","https://jobs.lever.co/gems-education"]},
  {"company": "Seera Group", "segment": "dubai_visa", "candidates": ["https://www.seeragroup.com/en/careers","https://jobs.lever.co/seera"]},
  {"company": "Omnix International", "segment": "dubai_visa", "candidates": ["https://omnix.com/careers","https://jobs.lever.co/omnix"]},
  {"company": "Cigna Middle East", "segment": "dubai_visa", "candidates": ["https://www.cigna.ae/about-us/careers","https://cigna.wd1.myworkdayjobs.com/Cigna_Careers"]},
  {"company": "YallaHub", "segment": "dubai_visa", "candidates": ["https://yallahub.com/careers","https://jobs.lever.co/yallahub"]},
]


async def run_all():
    results = []
    # Load existing results to resume if interrupted
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE) as f:
            results = json.load(f)
        done_companies = {r["company"] for r in results}
        remaining = [c for c in COMPANIES if c["company"] not in done_companies]
        print(f"Resuming: {len(results)} done, {len(remaining)} remaining")
    else:
        remaining = COMPANIES

    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)
    async with httpx.AsyncClient(limits=limits, timeout=8) as client:
        # Process in batches of 20 (parallel)
        BATCH = 20
        for batch_start in range(0, len(remaining), BATCH):
            batch = remaining[batch_start:batch_start + BATCH]
            tasks = [process_company(client, entry) for entry in batch]
            batch_results = await asyncio.gather(*tasks)

            for res in batch_results:
                results.append(res)
                status = res["http_status"]
                status_str = "✓" if status == 200 else f"~{status}" if status else "✗"
                print(f"[{len(results):3d}] {status_str} {res['company'][:35]:35s} → {res['portal_type']}")

            # Save after every batch
            with open(OUTPUT_FILE, "w") as f:
                json.dump(results, f, indent=2)

    print(f"\n✓ Saved {len(results)} results → {OUTPUT_FILE}")

    types = Counter(r["portal_type"] for r in results)
    print("\n=== Portal Type Distribution ===")
    for t, c in types.most_common():
        print(f"  {c:3d}  {t}")


if __name__ == "__main__":
    asyncio.run(run_all())
