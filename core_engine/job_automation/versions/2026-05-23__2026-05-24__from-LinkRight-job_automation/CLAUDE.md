# Job Discovery Agent — Project Rules

## Core Task
Scrape career portals for "Product Manager" jobs across 200 companies in `Job Database - Dubai - Visa Sponsors.csv`. Save all raw data to `discovered_jobs.json`.

## MANDATORY: Tool Usage
- **ONLY use `agent-browser` CLI for ALL web access** — no scripts, no WebFetch, no WebSearch, no gstack browse
- agent-browser commands: `open <url>`, `snapshot`, `click <ref>`, `fill <ref> <value>`, `close`
- Never create or run background Python scripts for scraping

## Output Format
`discovered_jobs.json` — JSON array, one entry per company:
```json
{"company": "Name", "status": "success|failed|skipped", "data": [...] or null}
```
- Save after EVERY company (overwrite file)
- No filtering — collect ALL raw data
- Max 30 jobs per company

## Scraping Rules
- Max 3 attempts per action; fail and move on
- Scroll max 3 times on listing pages
- 8-second timeout for page loads
- Max 30 jobs per company
- Never click Apply buttons
- Search for "Product Manager" on each portal
- Login with `PORTAL_EMAIL` / `PORTAL_PASSWORD` from `~/Desktop/Secrets/linkright/job_automation.env` if portal requires sign-in

## Session Recovery
- Check current JSON state: `python3 -c "import json; d=json.load(open('discovered_jobs.json')); print(len(d), 'done')`
- List remaining: compare CSV company names against JSON entries
- Resume from first company NOT in JSON

## Progress Logging (MANDATORY)
- After EVERY company processed, print one line: `[N/total] CompanyName — X PM jobs` (or `0 PM jobs` / `skipped`)
- Whenever PM jobs ARE found (data array non-empty), immediately print each job title + URL before moving to next company
- At session start, print all previously discovered jobs (company → job titles) so the user sees full progress at a glance
- Never silently skip a company — always log the outcome

## Do NOT
- Run scrape_all.py or any other background script
- Spawn subagents
- Use gstack browse
- Skip PASS companies without attempting agent-browser
- Batch-fail companies without trying
