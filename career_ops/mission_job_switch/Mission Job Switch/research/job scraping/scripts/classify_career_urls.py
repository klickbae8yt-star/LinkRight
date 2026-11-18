"""
Career URL Classifier - Pass 2
Reclassify Unknown and Custom_Career_Site entries using:
1. Known ATS mappings for major companies
2. curl_cffi requests (better TLS) to retry Unknown entries
3. Body-based Tier1/Tier2 detection
"""

import asyncio
import json
import re
import sys
from pathlib import Path
from curl_cffi.requests import AsyncSession

INPUT_FILE = Path(__file__).parent.parent / "db" / "career_urls_result.json"
OUTPUT_FILE = Path(__file__).parent.parent / "db" / "career_urls_result.json"

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
    (r"oraclecloud\.com/hcmUI", "ATS_Oracle_HCM"),
    (r"rippling\.com/jobs", "ATS_Rippling"),
    (r"pinpoint\.co", "ATS_Pinpoint"),
    (r"workable\.com", "ATS_Workable"),
    (r"dover\.com/careers", "ATS_Dover"),
]

TIER2_SIGNALS = [
    r'<script id="__NEXT_DATA__"', r'data-nuxt', r'window\.__INITIAL_STATE__',
    r'window\.__APOLLO_STATE__', r'<div id="root">', r'<div id="app">',
    r'"__NEXT_DATA__"', r'/_next/static', r'/static/js/main\.', r'react-dom',
    r'vue\.js', r'angular\.js', r'ember\.js', r'nuxt\.js',
    r'__webpack_require__', r'ReactDOM\.render', r'createApp\(',
]

TIER3_SIGNALS = [
    r'cf-ray', r'__cf_bm', r'cf-clearance',  # Cloudflare
    r'x-amz-cf-id', r'x-amz-request-id',      # AWS CloudFront
    r'security verification', r'please enable javascript',
    r'access denied', r'bot detection',
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# Known ATS overrides for companies where URL didn't reveal ATS
# Format: company_name_lower → (portal_type, notes)
KNOWN_ATS = {
    # India MNCs
    "uber": ("ATS_Workday", "uber.wd5.myworkdayjobs.com"),
    "servicenow": ("ATS_Workday", "servicenow.wd5.myworkdayjobs.com"),
    "meta": ("Tier2_CSR_SPA", "metacareers.com - React SPA"),
    "coinbase": ("ATS_Greenhouse", "boards.greenhouse.io/coinbase"),
    "expedia group": ("ATS_Workday", "expedia.wd5.myworkdayjobs.com"),
    "visa": ("ATS_Workday", "visa.wd5.myworkdayjobs.com"),
    "rakuten india": ("ATS_Workday", "rakuten via Workday"),
    "broadcom (vmware)": ("ATS_Workday", "broadcom.wd1.myworkdayjobs.com"),
    "tesco technology": ("ATS_Workday", "tesco.wd3.myworkdayjobs.com"),
    "philips healthtech": ("ATS_Workday", "philips.wd3.myworkdayjobs.com"),
    "yahoo! india": ("ATS_Workday", "yahooinc.wd5.myworkdayjobs.com"),
    "coupang india": ("ATS_Greenhouse", "boards.greenhouse.io/coupang"),
    "citrix (cloud software group)": ("ATS_Workday", "cloudsoftwaregroup.wd5.myworkdayjobs.com"),
    "trellix": ("ATS_Workday", "trellix.wd1.myworkdayjobs.com"),
    "akamai technologies": ("ATS_Workday", "akamai.wd1.myworkdayjobs.com"),
    "gartner": ("ATS_Workday", "gartner.wd5.myworkdayjobs.com"),
    "ge healthcare": ("ATS_Workday", "gehealthcare.wd5.myworkdayjobs.com"),
    "mathworks": ("Tier2_CSR_SPA", "MathWorks custom React portal"),
    "nutanix": ("ATS_Workday", "nutanix.wd5.myworkdayjobs.com"),
    "sony india software centre": ("ATS_Workday", "Sony via Workday"),
    "snap inc.": ("Tier2_CSR_SPA", "snap.com/careers - React SPA"),
    "disney+ hotstar": ("ATS_Workday", "disney.wd5.myworkdayjobs.com"),
    # AI Startups
    "openai": ("ATS_Greenhouse", "boards.greenhouse.io/openai"),
    "anthropic": ("ATS_Ashby", "jobs.ashbyhq.com/anthropic"),
    "perplexity ai": ("ATS_Ashby", "jobs.ashbyhq.com/perplexity"),
    "mistral ai": ("ATS_Ashby", "jobs.ashbyhq.com/mistralai"),
    "cohere": ("ATS_Greenhouse", "boards.greenhouse.io/cohere"),
    "databricks": ("ATS_Workday", "databricks.wd5.myworkdayjobs.com"),
    "scale ai": ("ATS_Greenhouse", "boards.greenhouse.io/scaleai"),
    "hugging face": ("ATS_Greenhouse", "boards.greenhouse.io/huggingface"),
    "stability ai": ("ATS_Lever", "jobs.lever.co/stability-ai"),
    "runway": ("ATS_Lever", "jobs.lever.co/runwayml"),
    "midjourney": ("Tier2_CSR_SPA", "midjourney.com/jobs - custom portal"),
    "pika labs": ("ATS_Ashby", "jobs.ashbyhq.com/pika"),
    "adept": ("ATS_Greenhouse", "boards.greenhouse.io/adept"),
    "together ai": ("ATS_Ashby", "jobs.ashbyhq.com/together"),
    "replicate": ("ATS_Ashby", "jobs.ashbyhq.com/replicate"),
    "weights & biases": ("ATS_Greenhouse", "boards.greenhouse.io/wandb"),
    "modal": ("ATS_Ashby", "jobs.ashbyhq.com/modal"),
    "vapi": ("ATS_Ashby", "jobs.ashbyhq.com/vapi"),
    "fireworks ai": ("ATS_Ashby", "jobs.ashbyhq.com/fireworks"),
    "anyscale": ("ATS_Greenhouse", "boards.greenhouse.io/anyscale"),
    "coreweave": ("ATS_Greenhouse", "boards.greenhouse.io/coreweave"),
    "lambda labs": ("ATS_Greenhouse", "boards.greenhouse.io/lambdalabs"),
    "vast.ai": ("ATS_Ashby", "jobs.ashbyhq.com/vast"),
    "cerebras systems": ("ATS_Greenhouse", "boards.greenhouse.io/cerebras"),
    "groq": ("ATS_Greenhouse", "boards.greenhouse.io/groq"),
    "samba nova systems": ("ATS_Greenhouse", "boards.greenhouse.io/sambanova"),
    "inflection ai": ("ATS_Ashby", "jobs.ashbyhq.com/inflection"),
    "xai (x.ai)": ("ATS_Ashby", "jobs.ashbyhq.com/xai"),
    "character.ai": ("ATS_Greenhouse", "boards.greenhouse.io/characterai"),
    "luma ai": ("ATS_Ashby", "jobs.ashbyhq.com/luma"),
    "eleven labs": ("ATS_Ashby", "jobs.ashbyhq.com/elevenlabs"),
    "elevenlabs": ("ATS_Ashby", "jobs.ashbyhq.com/elevenlabs"),
    "deepmind": ("ATS_Workday", "Google/DeepMind via Workday"),
    "google deepmind": ("ATS_Workday", "google.wd1.myworkdayjobs.com"),
    "krutrim": ("Tier2_CSR_SPA", "krutrim.com/careers - custom"),
    "sarvam ai": ("ATS_Ashby", "jobs.ashbyhq.com/sarvamai"),
    "cognitiveview": ("Tier2_CSR_SPA", "Custom startup portal"),
    "ola electric": ("Tier2_CSR_SPA", "olaelectric.com/careers - custom SPA"),
    # Dubai
    "amazon (uae)": ("Custom_Career_Site", "amazon.jobs - custom"),
    "google (dubai)": ("ATS_Workday", "google.wd1.myworkdayjobs.com"),
    "microsoft (uae)": ("ATS_Workday", "microsoft.wd5.myworkdayjobs.com"),
    "talabat": ("ATS_Greenhouse", "boards.greenhouse.io/talabat"),
    "careem": ("ATS_Greenhouse", "boards.greenhouse.io/careem"),
    "noon": ("Tier2_CSR_SPA", "noon.com/careers - custom SPA"),
    "deliveroo (uae)": ("ATS_Greenhouse", "boards.greenhouse.io/deliveroo"),
    "uber (dubai)": ("ATS_Workday", "uber.wd5.myworkdayjobs.com"),
    "booking.com (dubai)": ("ATS_Workday", "booking.wd3.myworkdayjobs.com"),
    "airbnb (dubai)": ("ATS_Greenhouse", "boards.greenhouse.io/airbnb"),
    "bybit": ("Tier2_CSR_SPA", "bybit.com/en/careers - custom SPA"),
    "okx": ("Tier2_CSR_SPA", "okx.com/careers - custom SPA"),
    "binance": ("Tier2_CSR_SPA", "binance.com/careers - custom SPA"),
    "kraken": ("ATS_Lever", "jobs.lever.co/kraken"),
    "coinbase (dubai)": ("ATS_Greenhouse", "boards.greenhouse.io/coinbase"),
    "dewa (digital)": ("Tier2_CSR_SPA", "dewa.gov.ae/careers - custom SPA"),
    "du telecom": ("ATS_Workday", "du.wd3.myworkdayjobs.com"),
    "etisalat / e&": ("ATS_SAP_SuccessFactors", "etisalat via SuccessFactors"),
    "farah experiences": ("Tier2_CSR_SPA", "farahexperiences.com/careers"),
    "majid al futtaim": ("ATS_Workday", "majidalfuttaim.wd3.myworkdayjobs.com"),
    "emaar": ("ATS_Workday", "emaar.wd3.myworkdayjobs.com"),
    "damac group": ("Tier2_CSR_SPA", "damacproperties.com/careers"),
    "property finder": ("ATS_Greenhouse", "boards.greenhouse.io/propertyfinder"),
    "bayut": ("ATS_Greenhouse", "boards.greenhouse.io/bayut"),
    "dubizzle": ("ATS_Lever", "jobs.lever.co/dubizzle"),
    "bayt.com": ("Tier2_CSR_SPA", "bayt.com - custom job portal"),
    "presight": ("ATS_Workday", "presight.ai/careers - Workday"),
    "inception (g42)": ("ATS_Workday", "g42.wd5.myworkdayjobs.com"),
    "g42": ("ATS_Workday", "g42.wd5.myworkdayjobs.com"),
    "core42": ("ATS_Workday", "core42.wd5.myworkdayjobs.com"),
    "abudhabi commercial bank": ("ATS_Workday", "adcb via Workday"),
    "first abu dhabi bank": ("ATS_Workday", "fab via Workday"),
    "mashreq bank": ("ATS_Workday", "mashreq.wd3.myworkdayjobs.com"),
    "rakbank": ("Tier2_CSR_SPA", "rakbank.ae/careers - custom"),
    "enbd": ("Tier2_CSR_SPA", "emiratesnbd.com/careers - custom SPA"),
    "emirates airline": ("ATS_Workday", "emirates.wd3.myworkdayjobs.com"),
    "flydubai": ("Tier2_CSR_SPA", "flydubai.com/en/careers - custom"),
    "air arabia": ("Tier2_CSR_SPA", "airarabia.com/en/about/careers"),
    "dp world": ("ATS_Workday", "dpworld.wd5.myworkdayjobs.com"),
    "ad ports group": ("Tier2_CSR_SPA", "adportsgroup.com/careers"),
    "serco middle east": ("ATS_Workday", "serco via Workday"),
    "gems world academy": ("Tier2_CSR_SPA", "gemsworld.com/careers"),
    "gems edtech": ("Tier2_CSR_SPA", "gemsworld.com/careers"),
    "seera group": ("ATS_Workday", "seera via Workday"),
    "omnix international": ("Tier2_CSR_SPA", "omnix.com/careers"),
    "cigna middle east": ("ATS_Workday", "cigna.wd5.myworkdayjobs.com"),
    "yallahub": ("ATS_Ashby", "jobs.ashbyhq.com/yallahub"),
}

# Companies where Custom_Career_Site should be Tier1 or Tier2
# (sites with HTTP 200 but no ATS URL match)
CUSTOM_TIER_OVERRIDES = {
    # Tier1: static HTML / SSR
    "google": "Tier2_CSR_SPA",  # React SPA
    "microsoft": "Tier2_CSR_SPA",  # React SPA
    "amazon": "Tier2_CSR_SPA",  # amazon.jobs React SPA
    "flipkart": "Tier2_CSR_SPA",  # Next.js
    "swiggy": "Tier2_CSR_SPA",  # React SPA
    "atlassian": "ATS_Workday",  # redirects to Workday
    "adobe": "ATS_Workday",  # adobe.wd5.myworkdayjobs.com
    "salesforce": "ATS_Workday",  # salesforce.wd5.myworkdayjobs.com
    "walmart global tech": "ATS_Workday",  # walmart.wd5.myworkdayjobs.com
    "nvidia": "ATS_Workday",  # nvidia.wd5.myworkdayjobs.com
    "linkedin": "ATS_Workday",  # linkedin via Microsoft Workday
    "paypal": "ATS_Workday",  # paypal.wd5.myworkdayjobs.com
    "phonepe": "ATS_Greenhouse",  # boards.greenhouse.io/phonepe
    "zepto": "ATS_Ashby",  # jobs.ashbyhq.com/zepto
    "zomato / blinkit": "ATS_Lever",  # jobs.lever.co/zomato
    "razorpay": "ATS_Lever",  # jobs.lever.co/razorpay
    "booking.com": "ATS_Workday",  # booking.wd3.myworkdayjobs.com
    "oracle": "ATS_Taleo",  # Oracle uses Taleo (their own product)
    "cisco": "ATS_Workday",  # cisco.wd5.myworkdayjobs.com
    "intuit": "ATS_Workday",  # intuit.wd5.myworkdayjobs.com
    "twilio": "ATS_Greenhouse",  # boards.greenhouse.io/twilio
    "grab": "ATS_Workday",  # grab.wd5.myworkdayjobs.com
    "stripe": "ATS_Greenhouse",  # stripe.com/jobs uses Greenhouse
    "intel": "ATS_Workday",  # intel.wd5.myworkdayjobs.com
    "sap": "ATS_SAP_SuccessFactors",  # SAP uses own product
    "myntra": "ATS_Workday",  # flipkart/myntra via Workday
    "qualcomm": "ATS_Workday",  # qualcomm.wd5.myworkdayjobs.com
    "jpmorgan chase (tech india)": "ATS_Workday",  # jpmc.wd5.myworkdayjobs.com
    "goldman sachs (tech)": "ATS_Workday",  # goldmansachs.wd5.myworkdayjobs.com
    "dell technologies": "ATS_Workday",  # dell.wd5.myworkdayjobs.com
    "samsung r&d institute india (samsung)": "ATS_Workday",  # samsung via Workday
    "morgan stanley (tech india)": "ATS_Workday",  # morganstanley.wd5.myworkdayjobs.com
    "meesho": "ATS_Lever",  # jobs.lever.co/meesho
    "inmobi / glance": "ATS_Greenhouse",  # boards.greenhouse.io/inmobi
    "ola / ola electric": "Tier2_CSR_SPA",  # custom SPA
    "makemytrip": "ATS_Workday",  # makemytrip via Workday
    "zoom video communications": "ATS_Workday",  # zoom.wd5.myworkdayjobs.com
    "mastercard": "ATS_Workday",  # mastercard.wd1.myworkdayjobs.com
    "apple": "ATS_Workday",  # apple.wd5.myworkdayjobs.com
    "netflix": "ATS_Workday",  # netflix.wd5.myworkdayjobs.com
}


def classify_by_url(url: str) -> str | None:
    if not url:
        return None
    for pattern, ats_type in [
        (r"myworkdayjobs\.com", "ATS_Workday"),
        (r"greenhouse\.io", "ATS_Greenhouse"),
        (r"jobs\.lever\.co", "ATS_Lever"),
        (r"ashbyhq\.com", "ATS_Ashby"),
        (r"teamtailor\.com", "ATS_Teamtailor"),
        (r"smartrecruiters\.com", "ATS_SmartRecruiters"),
        (r"apply\.workable\.com", "ATS_Workable"),
        (r"workable\.com", "ATS_Workable"),
        (r"bamboohr\.com", "ATS_BambooHR"),
        (r"taleo\.net", "ATS_Taleo"),
        (r"icims\.com", "ATS_iCIMS"),
        (r"eightfold\.ai", "ATS_Eightfold"),
        (r"successfactors\.com", "ATS_SAP_SuccessFactors"),
        (r"jobs\.sap\.com", "ATS_SAP_SuccessFactors"),
        (r"jobvite\.com", "ATS_Jobvite"),
        (r"oraclecloud\.com/hcmUI", "ATS_Oracle_HCM"),
        (r"phenom\.com", "ATS_Phenom"),
        (r"rippling\.com/jobs", "ATS_Rippling"),
        (r"lever\.co", "ATS_Lever"),
        (r"boards\.greenhouse", "ATS_Greenhouse"),
    ]:
        if re.search(pattern, url, re.I):
            return ats_type
    return None


def classify_by_body(body: str) -> str:
    # Scan iframe src attributes for embedded ATS before checking body text
    for src in re.findall(r'<iframe[^>]+src=["\']([^"\']+)["\']', body, re.IGNORECASE):
        ats = classify_by_url(src)
        if ats:
            return ats

    body_lower = body.lower()
    if any(re.search(p, body, re.I) for p in [
        r"myworkdayjobs\.com", r"workday\.com"
    ]):
        return "ATS_Workday"
    if re.search(r"greenhouse\.io", body, re.I):
        return "ATS_Greenhouse"
    if re.search(r"lever\.co", body, re.I):
        return "ATS_Lever"
    if re.search(r"ashbyhq\.com", body, re.I):
        return "ATS_Ashby"
    if re.search(r"successfactors\.com", body, re.I):
        return "ATS_SAP_SuccessFactors"
    if re.search(r"taleo\.net", body, re.I):
        return "ATS_Taleo"
    if re.search(r"icims\.com", body, re.I):
        return "ATS_iCIMS"
    if re.search(r"eightfold\.ai", body, re.I):
        return "ATS_Eightfold"
    if any(re.search(p, body) for p in TIER2_SIGNALS):
        return "Tier2_CSR_SPA"
    return "Tier1_StaticHTML"


async def fetch_and_classify(session, entry: dict) -> dict:
    url = entry.get("career_url")
    if not url:
        return entry

    # Already well-classified
    current = entry.get("portal_type", "Unknown")
    if current not in ("Unknown", "Custom_Career_Site"):
        return entry

    company_lower = entry["company"].lower()

    # 1. Check known ATS lookup
    if company_lower in KNOWN_ATS:
        pt, notes = KNOWN_ATS[company_lower]
        entry["portal_type"] = pt
        entry["classification_source"] = f"known_ats: {notes}"
        return entry

    # 2. Check custom tier overrides for Custom_Career_Site
    if current == "Custom_Career_Site" and company_lower in CUSTOM_TIER_OVERRIDES:
        entry["portal_type"] = CUSTOM_TIER_OVERRIDES[company_lower]
        entry["classification_source"] = "custom_tier_override"
        return entry

    # 3. Try HTTP fetch with curl_cffi
    try:
        resp = await session.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                     "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"},
            timeout=12,
            allow_redirects=True,
        )
        final_url = str(resp.url)
        body = resp.text[:30000] if resp.text else ""
        status = resp.status_code

        ats_from_url = classify_by_url(final_url)
        if ats_from_url:
            entry["portal_type"] = ats_from_url
            entry["career_url"] = final_url
            entry["http_status"] = status
            entry["classification_source"] = "curl_cffi_redirect_url"
            return entry

        if status == 403:
            entry["portal_type"] = "Tier3_ProtectedAPI"
            entry["http_status"] = 403
            entry["classification_source"] = "curl_cffi_403"
            return entry

        if status == 200 and body:
            ats_from_body = classify_by_body(body)
            entry["portal_type"] = ats_from_body
            entry["http_status"] = status
            entry["career_url"] = final_url
            entry["classification_source"] = "curl_cffi_body"
            return entry

    except Exception as e:
        entry["fetch_error"] = str(e)[:100]

    # 4. Fallback: for major companies still Unknown, assume Tier2
    if current == "Unknown" and entry.get("http_status") is None:
        entry["portal_type"] = "Tier2_CSR_SPA"
        entry["classification_source"] = "fallback_tier2"

    return entry


async def main():
    with open(INPUT_FILE) as f:
        data = json.load(f)

    needs_work = [e for e in data if e.get("portal_type") in ("Unknown", "Custom_Career_Site")]
    print(f"Total: {len(data)}, needs reclassification: {len(needs_work)}")

    async with AsyncSession(impersonate="chrome136") as session:
        for i in range(0, len(data), 20):
            batch = data[i:i+20]
            tasks = [fetch_and_classify(session, e) for e in batch]
            results = await asyncio.gather(*tasks)
            for j, r in enumerate(results):
                data[i+j] = r
            done = min(i+20, len(data))
            classified = sum(1 for e in data[:done] if e.get("portal_type") not in ("Unknown",))
            print(f"  [{done}/{len(data)}] classified: {classified}")
            with open(OUTPUT_FILE, "w") as f:
                json.dump(data, f, indent=2)

    # Final stats
    from collections import Counter
    types = Counter(e["portal_type"] for e in data)
    print("\nFinal portal type breakdown:")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

    remaining_unknown = [e["company"] for e in data if e["portal_type"] == "Unknown"]
    if remaining_unknown:
        print(f"\nStill Unknown ({len(remaining_unknown)}): {remaining_unknown[:20]}")


if __name__ == "__main__":
    asyncio.run(main())
