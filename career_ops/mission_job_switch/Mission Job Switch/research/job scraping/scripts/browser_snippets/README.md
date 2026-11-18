# Browser Snippets

## passive_job_capture.js — Install once, captures everything

**Zero bot risk.** You navigate normally. Script just reads DOM of pages already loaded.

### Install (one time)

1. Install **Tampermonkey** extension in Chrome: `chrome.google.com/webstore/detail/tampermonkey`
2. Click Tampermonkey icon → Dashboard → New Script (+ button)
3. Delete all default code, paste entire `passive_job_capture.js`
4. Ctrl+S to save

### How to use

- Browse job portals normally — LinkedIn, Naukri, Wellfound, company career pages, anywhere
- Open individual job description pages (click into each job you're interested in)
- Green badge `📋 5 jobs` appears in bottom-right corner as jobs are captured
- When done browsing, click the badge → Download CSV
- Import: `python3 scripts/import_browser_csv.py ~/Downloads/jobs_passive_2026-05-21.csv`

### What gets captured (auto-detected)

Script scores each page for job-description signals:
- URL patterns: `/jobs/view/`, `/careers/slug`, `?jobId=`, greenhouse/lever/ashby URLs etc.
- Content keywords: "responsibilities", "requirements", "qualifications", "about the role" etc.
- Score ≥ 25 → captured. Search results pages (score too low) → ignored.

### Data stored

Tampermonkey's own storage (not per-domain localStorage). Works across all portals in same session.
Each capture: URL, page title, portal hostname, score, timestamp, raw visible text (up to 15k chars).

CSV columns: `url, title, company, location, portal, captured_at, score, raw_text`
`title/company/location` are best-effort extracted from URL + page title + text patterns.

### Clear session

Click badge → red "✕ Clear" button.

---

## For portal-specific scripts (to be added)

When you want to scrape a full job listing (search results, not just individual pages):

1. Log into the portal
2. Navigate to the jobs search results page
3. Run: `playwright codegen --browser chromium --channel chrome <url>`
   - Records every click as a Python script
   - Give Claude that output → Claude writes the portal scraper

OR:

1. Save the jobs listing page as HTML (Ctrl+S → HTML Only)
2. `python3 scripts/analyze_html.py saved_page.html`
3. Give Claude the output → Claude writes the portal-specific JS snippet

Portal-specific scripts will be added here as separate files: `linkedin.js`, `naukri.js`, etc.
