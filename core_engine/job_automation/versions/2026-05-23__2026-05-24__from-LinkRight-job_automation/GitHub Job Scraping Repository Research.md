# **Technical Architecture and Design Patterns of GitHub Repositories for Talent Acquisition, LinkedIn Extraction, and Applicant Tracking Systems**

## **Evolution of Automated Recruitment Data Pipelines**

The landscape of automated talent acquisition has transitioned from simple, static document parsing to highly distributed, asynchronous scraping networks. Early job board aggregators, exemplified by archived tools like JobFunnel 1, relied on standard HTTP requests to fetch static HTML and parse it using simple libraries. While JobFunnel amassed over 2.1k stars and 261 forks on GitHub, it ultimately became obsolete as major platforms deployed aggressive anti-automation defenses, client-side rendering engines, and CAPTCHA gateways.1  
To bypass these barriers, modern scraping pipelines have evolved in two distinct directions. Some leverage advanced browser automation frameworks, such as Playwright and Puppeteer, combined with stealth libraries to simulate real human behavior.2 Others bypass user interfaces entirely by reverse-engineering the internal API endpoints of Applicant Tracking Systems (ATS).4  
The scale of this ecosystem is highlighted by curated aggregators like scraping-apis-for-devs, which contains over 2,622 ready-to-use APIs for developers, including a massive catalog dedicated to job market harvesting and real-time lead generation.7 Enterprise pipelines commonly leverage high-performance web-scraping frameworks like Crawlee 3 and declarative parsers like scrape-it 9 to build robust, scalable architectures capable of navigating the complex anti-bot systems of modern career portals.3

## **Architectural Framework of High-Performance LinkedIn Job Scrapers**

LinkedIn is one of the most heavily fortified data sources in the recruiting domain, deploying IP reputation scoring, behavior-based rate limiting, and mandatory login barriers to block automation.10 Developers have built diverse tools to systematically bypass these defenses.  
The spinlud codebase serves as a standard reference in this space, with the Python library py-linkedin-jobs-scraper earning 476 stars and 119 forks 11, and its TypeScript counterpart linkedin-jobs-scraper securing 179 stars and 46 forks.12 Both tools utilize headless browsers—such as Chromium managed via Puppeteer or Selenium—to extract critical data fields, including job IDs, apply links, titles, corporate metadata, location strings, full-text descriptions, and structural insights.11

                         
                                   |  
                (Is browser running in Cloud/Virtual Env?)  
                 /                                      \\  
                                                  \[No\]  
               /                                          \\  
    {Blocks & 403 Forbidden}                      {Proceeds with Crawl}  
                                 |  
               |                                           |  
    (Inject "li\_at" cookie)                                |  
               |                                           |  
    {Concurrence capped at 1}                     {Parallel Concurrence ok}  
    {Inject Custom "slow\_mo" delay}               {Standard request delays}  
               \\                                          /  
                \\--\[Normalized Extraction of Job Nodes\]--/

To maintain access, spinlud's scrapers support both anonymous and authenticated sessions.11 Anonymous scrapers operate without credentials but are frequently blocked in cloud environments like AWS or Heroku.11 To bypass these blocks, the scraper must pivot to authenticated sessions by injecting an active browser session's li\_at cookie.11  
Because authenticated sessions run on personalized rate limits, concurrent executions on a single account must be throttled.11 This is managed by configuring the slow\_mo parameter to slow down browser operations.11 The delay required to prevent account flags is modeled as:  
![][image1]  
where ![][image2] is the total step delay in milliseconds, ![][image3] is the base delay (recommended at ![][image4] for anonymous sessions and ![][image5] for authenticated sessions), and ![][image6] is the number of concurrent queries.11  
For larger operations, the decoupled multi-account model implemented in LinkedIn-Job-Scraper by arshka (185 stars, 51 forks) is highly effective.13 This architecture splits the ingestion pipeline into two parallel, asynchronously running scripts.13 The first script, search\_retriever.py, searches the index using basic filters to discover new postings.13 It extracts minimal attributes (such as job IDs) and writes them to a database.13  
The second script, details\_retriever.py, systematically pops these IDs from the queue and fetches their full descriptions, requirements, and salaries.13 This multi-account architecture rotates a pool of credentials defined in a local logins.csv file.13 This allows details retrieval—which requires fetching individual pages sequentially—to run during off-peak hours without triggering rate limits on the primary search account.13  
Other developers have built complete self-hosted automation suites. The linkedIn-scraper by ManiMozaffar combines Playwright, FastAPI, and PostgreSQL to extract job data, analyze postings using ChatGPT services to extract required hard skills, and distribute the processed roles directly to Telegram channels.2  
For personal workflows, linkedin-scraper-ext by anton-ds operates as a local Chrome Extension.14 By running directly inside the user's browser, it inherits their active session and bypasses remote bot-detection systems entirely.14 It extracts job descriptions from the DOM on-click and sends them with custom prompts to ChatGPT for instant, structured summaries.14  
At the enterprise tier, tools like linkedin-jobs-scraper-incredibly-fast by pun-4 (Bitbash) claim speeds of up to 1,000 listings per minute by using pre-configured residential and datacenter proxy networks to bypass IP bans.15

| Repository | GitHub Stars | Core Language / Tech Stack | Primary Extraction Mechanism | Session Management |
| :---- | :---- | :---- | :---- | :---- |
| spinlud/py-linkedin-jobs-scraper | 476 11 | Python / Selenium 11 | Headless Browser Page Scraping 11 | Anonymous & Authenticated (li\_at cookie injection) 11 |
| spinlud/linkedin-jobs-scraper | 179 12 | TypeScript / Puppeteer 12 | Headless Browser Page Scraping 12 | Anonymous & Authenticated (li\_at cookie injection) 12 |
| arshka/LinkedIn-Job-Scraper | 185 13 | Python / Requests / sqlite 13 | Decoupled Search & Detail Parsing 13 | Multi-Login rotation via logins.csv configuration 13 |
| ManiMozaffar/linkedIn-scraper | Undefined 2 | Python / Playwright / FastAPI 2 | Browser Automation & AI Parsing 2 | Database-driven proxy and keyword integration 2 |
| anton-ds/linkedin-scraper-ext | Undefined 14 | JavaScript / Chrome Extension 14 | Client-side DOM parsing on-click 14 | Leverages the user's active browser session 14 |
| pun-4/linkedin-jobs-scraper-incredibly-fast | Undefined 15 | JavaScript / Apify Integration 15 | Automated high-speed extraction 15 | Managed residential/datacenter proxy rotation 15 |

## **Multi-Board Aggregation and Unified Job Search Interfaces**

For applications that require data from multiple platforms, developers use unified scraping libraries and monorepos to fetch, normalize, and de-duplicate listings across different job boards.17  
The standard tool in this domain is JobSpy (distributed as python-jobspy on PyPI), which has 3.4k stars and 694 forks.17 JobSpy queries LinkedIn, Indeed, Glassdoor, Google Jobs, ZipRecruiter, and other international boards concurrently, compiling the results into a single Pandas DataFrame.17 It supports query offsets, age-based filtering via hours\_old, and proxy configurations.17  
Indeed searches are highly stable but frequently return false positives because Indeed queries both titles and descriptions.17 To prevent unrelated roles, developers must write refined search terms using boolean logic:  
'"engineering intern" software summer (java OR python OR c++) 2025 \-tax \-marketing'  
This ensures the results contain specific keywords and excludes irrelevant categories.17 The ts-jobspy repository by alpharomercoma provides a complete TypeScript port of JobSpy designed for JavaScript runtimes.19

                    \+-----------------------------+  
                    |    Multi-Board Aggregator   |  
                    \+--------------+--------------+  
                                   |  
         \+-------------------------+-------------------------+  
         |                         |                         |  
         v                         v                         v  
\+------------------+      \+------------------+      \+------------------+  
|     Indeed       |      |     LinkedIn     |      |   Google Jobs    |  
\+--------+---------+      \+--------+---------+      \+--------+---------+  
         |                         |                         |  
(Stable Endpoint)          (High Rate Limits)       (Specific Syntax Req)  
(GraphQL or JSON)          (Requires Proxies)       (Mocks Search Query)  
         \\                         |                         /  
          \\                        |                        /  
           \\-----------------------+-----------------------/  
                                   |  
                                   v  
                    \+-----------------------------+  
                    |      Unified DataFrame      |  
                    |   (Normalized Schema)       |  
                    \+-----------------------------+

Building on these aggregators, jobsparser by FranciscoMoretti (62 stars, 13 forks) is a CLI tool that extends jobspy2.20 It automates search execution across multiple boards and outputs the results as CSV files with unique timestamps.20 This can be contrasted with single-board scrapers like indeed-scraper by rynobax (56 stars, 39 forks) 21 and how-to-scrape-indeed by oxylabs (148 stars) 22, which focus on single-board extraction using xpath parsing.21  
For enterprise-scale applications, the ever-jobs repository by ever-co (34 stars) is built as a modular NestJS monorepo.18 It aggregates postings from over 160 independent portals and exposes them through REST, GraphQL, CLIs, and Model Context Protocol (MCP) servers for autonomous AI agents.18  
Additionally, self-hosted processing pipelines, such as job-board-scraper by matthewincardona, use JobSpy to feed unstructured data to a local Cloudflare AI Worker running Llama-3.2-3B.24 The worker cleans the job descriptions, extracts roles, seniorities, and skills, and writes the structured results directly to a Supabase database.24

| Repository | GitHub Stars | Primary Language | Target Platforms | Core Feature |
| :---- | :---- | :---- | :---- | :---- |
| speedyapply/JobSpy | 3,461 25 | Python 25 | LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs, Bayt 17 | Compiles aggregated results directly into Pandas DataFrames 17 |
| alpharomercoma/ts-jobspy | 10 19 | TypeScript 19 | LinkedIn, Indeed 19 | Type-safe JavaScript port of the original python-jobspy library 19 |
| FranciscoMoretti/jobsparser | 62 20 | Python 20 | LinkedIn, Indeed, Glassdoor, Google Jobs 20 | CLI tool extending jobspy2 with custom outputs and auto-retries 20 |
| ever-jobs/ever-jobs | 34 23 | TypeScript 23 | 160+ sources including job boards and direct ATS APIs 18 | NestJS monorepo with GraphQL APIs and AI MCP server layers 18 |
| matthewincardona/job-board-scraper | Undefined 24 | Python / TypeScript 24 | Multi-source job board extraction via JobSpy 24 | Cloudflare AI worker pipeline running Llama-3.2-3B 24 |

## **Direct Applicant Tracking System (ATS) Harvesting and Reverse API Engineering**

Because public job boards are riddled with duplicate posts and ghost jobs, modern data pipelines have shifted to targeting Applicant Tracking Systems (ATS) directly.4 This API-first approach treats company-hosted careers portals as a single source of truth, bypassing the need to parse volatile consumer-facing layouts.4  
The standard tool for this is ats-scrapers (distributed as jobhive-py), which has 40 stars and 5 forks.4 This repository manages an open-source global dataset containing over 3.3 million live jobs from 406,000 distinct ATS environments.4  
The package bypasses browser rendering for most systems, querying public endpoints directly to extract structured data containing locations, commitment levels, and raw metadata.4 For highly secured sites like Meta or Tesla, the library integrates Browserbase remote sessions to run automated scripts that bypass web-security systems like Akamai.4

                 \+--------------------------------------+  
                 |          Target Careers Page         |  
                 \+------------------+-------------------+  
                                    |  
                 (Detect Platform Host via URL Pattern)  
                 /                  |                   \\  
                /                   |                    \\  
               v                    v                     v  
    \+--------------------+ \+--------------------+ \+--------------------+  
    |   Greenhouse Host  | |     Lever Host     | |     Ashby Host     |  
    \+---------+----------+ \+---------+----------+ \+---------+----------+  
              |                     |                     |  
     (Get Dept Tree V1)     (Query Postings V0)    (ApiJobBoard GQL Query)  
              |                     |                     |  
     (Fetch Target Jobs)            |                     |  
               \\                    |                    /  
                \\                   |                   /  
                 \\------------------+------------------/  
                                    |  
                                    v  
                     \+------------------------------+  
                     |    Canonical Data Schema     |  
                     | \- Title, Company, URL, ID    |  
                     | \- Normalized Salary Range    |  
                     | \- Location Array             |  
                     \+------------------------------+

Each major ATS platform utilizes its own unique API endpoints and data schemas:

* **Greenhouse:** Scrapers target the public Boards API (https://boards-api.greenhouse.io/v1/boards/{token}/jobs).26 To reduce overhead, crawlers first fetch the corporate department tree via the department endpoint.6 This allows the scraper to filter jobs server-side and request only the exact department IDs needed, bypassing the rest of the job catalog.5  
* **Lever:** Crawlers query the Lever Postings API (https://api.lever.co/v0/postings/{company\_slug}).26 This API returns structured JSON objects containing job titles, departments, work commitments, and internal data like salary ranges.4 Because the endpoints are stable and public, they do not require headless browsers.4  
* **Ashby:** Operating via a public GraphQL gateway, Ashby processes listings through structured payloads sent to https://jobs.ashbyhq.com/api/non-auth/graphql-query.4 Crawlers invoke the ApiJobBoardWithTeams query to fetch listing stubs and teams.5 They then retrieve detailed job pages with a 100ms delay to prevent rate-limiting triggers.5  
* **Workday:** Workday does not provide a single, unified public API gateway, as each client operates on its own subdomain.28 Workday crawlers must identify the JSON feed backing the specific tenant UI to extract job descriptions, work models, and metadata.29

For unified workflows, job-board-scraper (Levergreen) by adgramigna (42 stars, 5 forks) orchestrates Scrapy spiders to pull Greenhouse and Lever listings on a daily schedule.31 To prevent IP bans, the system caches raw HTML in an Amazon S3 bucket, using the cached files to run duplicate daily crawls.31 Once fetched, dbt Core cleans and normalizes the data on Neon Serverless Postgres, and Hightouch syncs the results to Airtable for live rendering on Softr web interfaces.31  
For local automation, workday by raghuboosetty uses Selenium to automate Workday applications.32 It pulls candidate details from a local YAML file and injects them directly into standard Workday form fields, pausing for 60 seconds to let users manually handle non-standard mandatory questions.32  
Similarly, the workday-scraper-api by jharemza provides a Flask REST API that crawls Workday portals, normalizes listings, and writes them directly to local SQLite databases or Notion workspaces.33  
At the system level, Go-based engines like JobsScraper by MabudAlam implement concurrent syncing with rate limiters to aggregate listings from Ashby, Lever, Amazon, and Atlassian, storing the normalized records in local SQLite databases.35

| Repository / Project | Target ATS / Sources | Primary Language | Sync Architecture | Data Persistence |
| :---- | :---- | :---- | :---- | :---- |
| stapply-ai/ats-scrapers | Greenhouse, Lever, Ashby, Workday, BambooHR 4 | Python 4 | Asynchronous API Fetching & Browserbase remote sessions 4 | Raw JSON to Canonical Pandas DataFrames 4 |
| d-alleyne/ashby-job-scraper | Ashby Job Boards 5 | JavaScript 5 | Public GraphQL API Integration (ApiJobBoardWithTeams) 5 | Structured JSON array outputs 5 |
| d-alleyne/greenhouse-job-scraper | Greenhouse Job Boards 6 | JavaScript 6 | Public V1 Boards API & Department tree filtering 6 | Structured JSON with salary & location mapping 6 |
| adgramigna/job-board-scraper | Greenhouse, Lever 31 | Python 31 | Scrapy Spiders, AWS S3 HTML caching, dbt Core 31 | Neon Serverless Postgres & Airtable 31 |
| jharemza/workday-scraper-api | Workday Portals 33 | Python 34 | Headless browser parsing of Workday subdomains 33 | SQLite database & Notion workspace sync 33 |
| MabudAlam/JobsScraper | Ashby, Lever, Amazon, Atlassian 35 | Go / TypeScript 35 | Concurrent syncing with rate limiters 35 | SQLite database with REST API endpoint query 35 |

## **Career Page Crawling, AI Enrichment, and Local Job Search Systems**

When a company does not use a standardized ATS, automated pipelines must crawl career pages directly and use Large Language Models (LLMs) to structure the unstructured text.36  
The Gist repository by thoroc (HiringCafe, 17 stars) illustrates this NLP crawler pattern.36 The system uses a Node.js crawler built on Cheerio and Puppeteer to locate corporate career pages.36 It then dumps the raw HTML into ChatGPT (o1-mini) to perform a binary classification on whether the page contains a job description.36  
Once verified, the raw text is sent to GPT-4o-mini to extract key attributes—such as salaries, required years of experience, remote work status, and visa sponsorship—and return a structured JSON object.36 To weed out "ghost jobs" that are repeatedly reposted, the system calculates the Cosine Similarity between the text embeddings of new posts and historical listings from the same company:  
![][image7]  
where ![][image8] and ![][image9] represent the vector embeddings of the job descriptions. If the score exceeds a threshold (typically ![][image10]), the listing is flagged as a duplicate and hidden, keeping the search index fresh.36  
For personal job hunting, JobNavigator by vesaias (5 stars, 1 fork) is a complete self-hosted platform.37 It combines 6 scraping tiers—including direct Playwright crawlers for 11 ATS systems, board queries via JobSpy, levels.fyi extraction, and a Chrome extension—to aggregate listings in one dashboard.37  
The system queries MyVisaJobs for corporate H-1B LCA data and uses Claude or OpenAI to score roles against a candidate's resume.37 High-scoring matches trigger a local LLM to rewrite LaTeX templates (employment.tex, skills.tex) into custom PDFs.37

\+-------------------------------------------------------------+  
|               Job-Tracker Clipboard Monitoring              |  
\+------------------------------+------------------------------+  
                               |  
                   (User copies a job post URL)  
                               |  
                               v  
\+-------------------------------------------------------------+  
|                  Pattern Recognition Engine                 |  
| \- Extracts Company Name from URL domains                    |  
| \- Identifies Hosting Platform (LinkedIn, Greenhouse, Lever) |  
\+------------------------------+------------------------------+  
                               |  
                               v  
\+-------------------------------------------------------------+  
|                 Asynchronous Ingestion Task                 |  
| \- Requests raw page HTML in the background                  |  
| \- Extracts Job ID, Location, and Salary data                |  
\+------------------------------+------------------------------+  
                               |  
                               v  
\+-------------------------------------------------------------+  
|                    Local Storage Engine                     |  
| \- Populates draft details in SQLite database                |  
| \- Displays edit modal to the user                           |  
\+-------------------------------------------------------------+

Other developers have built lightweight local automation tools:

* **Job-Tracker-Smart-Application-Management-System (sruthi7sri):** A Flask-based local tool that uses pyperclip to monitor the system clipboard.26 When a user copies a job URL from LinkedIn, Greenhouse, Lever, or Workday, the system automatically parses the URL patterns to extract the company name, job ID, and platform.26 It then scrapes the page in the background to fetch the title and location, presenting a pre-filled draft to the user.26  
* **job-scraping-app (billyweinberger):** A Python application that scrapes Greenhouse, Lever, and Ashby APIs, rank-scores positions based on custom keywords, and uses ChatGPT to generate tailored cover letters.27 The pipeline runs automatically via daily GitHub Actions and posts a digest of the top roles to the repository's GitHub Issues.27  
* **job-finder (ejirocodes):** A TypeScript application that monitors career sites using Firecrawl's /extract endpoint.38 It processes qualifications using Together AI and sends real-time notifications to Slack webhooks.38  
* **SeekSpider (qinscode):** A Python crawler built on Scrapy and Plombery scheduling that stores listings in PostgreSQL and post-processes descriptions using DeepSeek AI APIs.39  
* **yubhub (houtini-ai):** A Model Context Protocol (MCP) server that monitors corporate careers pages, enriches job postings with AI, and outputs structured XML feeds.40

| System / Repository | GitHub Stars | Parsing & Scraping Stack | AI / Processing Integration | Delivery Channel |
| :---- | :---- | :---- | :---- | :---- |
| thoroc/HiringCafe (Gist) | 17 36 | Node.js / Cheerio / Puppeteer 36 | GPT-4o-mini parsing & embedding-based deduplication 36 | Hosted UI powered by Elasticsearch 36 |
| vesaias/JobNavigator | 5 37 | Python / Playwright 37 | Claude & OpenAI resume scoring & LaTeX custom PDF generation 37 | Self-hosted React Dashboard & Telegram 37 |
| sruthi7sri/Job-Tracker | 1 26 | Python / Flask / pyperclip 26 | Clipboard-triggered metadata parser 26 | Local Flask Dashboard & Excel exporter 26 |
| billyweinberger/job-scraping-app | 3 27 | Python / Greenhouse / Lever / Ashby APIs 27 | ChatGPT keyword matching & resume tailoring 27 | GitHub Issues Daily Digest via GitHub Actions 27 |
| ejirocodes/job-finder | 11 38 | TypeScript / Express / Firecrawl 38 | Together AI requirement analysis 38 | Real-time notifications via Slack Webhooks 38 |
| qinscode/SeekSpider | Undefined 39 | Python / Scrapy / Plombery 39 | DeepSeek API integration 39 | React \+ Vite UI and PostgreSQL 39 |
| houtini-ai/yubhub | 1 40 | JavaScript / TypeScript 40 | AI enrichment & categorization 40 | Model Context Protocol (MCP) & XML feeds 40 |

## **Architectural Selection and Performance Benchmarks**

When designing a job collection pipeline, developers must choose a scraping framework that balances execution speed against the engineering cost of bypassing bot detection.3  
The jobscz-scraper repository benchmarked Puppeteer, Playwright, and Selenium on Linux environments.41 In specific tests on Jobs.cz, Puppeteer and Selenium performed identically, running approximately 3.7 times faster than Playwright.41  
However, Playwright remains highly popular because of its clean API, browser context isolation, and multi-browser support (Chromium, Firefox, and WebKit).8 For applications that require Javascript execution, Puppeteer and Playwright are much more effective than request-based libraries like Cheerio, which fail on dynamic Single Page Applications (SPAs).3

                            \[Cloudflare / Akamai Gate\]  
                                        |  
                      (What is the scraper's TLS Signature?)  
                      /                                    \\  
                        \[Impersonated Fingerprint\]  
                   /                                          \\  
         {403 Forbidden Block}                         {200 Successful Request}  
    \[Fix: rebrowser or curl-impersonate\]                        |  
                   |                                            |  
         {Bypass TLS Fingerprinting}                            |  
                   |                                            |  
                   \\------/

To prevent blocks on highly fortified job boards, modern scraping pipelines integrate advanced anti-detection tools 3:

* **TLS Impersonation:** Tools like curl-impersonate (integrated via python bindings like curl\_cffi) modify the TLS handshake signature to mimic real web browsers (Chrome or Firefox), allowing HTTP requests to bypass Cloudflare without rendering web pages.3  
* **Automation Leak Patches:** Frameworks like rebrowser patch internal variables in Puppeteer and Playwright to hide browser-automation flags (such as navigator.webdriver), bypassing behavior-based checks.3  
* **Anti-Detect Browsers:** Camoufox provides a customized, headless Firefox engine that automatically spoofs WebGL configurations, handles proxy routing, and masks hardware signatures.3  
* **Next-Generation Drivers:** Libraries like nodriver (the successor to undetected-chromedriver) interact directly with the Chrome DevTools Protocol, completely avoiding the Selenium webdriver signatures that trigger security blocks.3

By combining direct API-first connections with browser automation fallbacks, engineers can build resilient, high-performance scraping pipelines that systematically collect clean, real-time job market data.4

#### **Works cited**

1. PaulMcInnis/JobFunnel: Scrape job websites into a single spreadsheet with no duplicates. \- GitHub, accessed on May 24, 2026, [https://github.com/PaulMcInnis/JobFunnel](https://github.com/PaulMcInnis/JobFunnel)  
2. ManiMozaffar/linkedIn-scraper: A playwright bot which is implemented to scrape linkedin and store advertisement data in a database and telegram channel \- GitHub, accessed on May 24, 2026, [https://github.com/ManiMozaffar/linkedIn-scraper](https://github.com/ManiMozaffar/linkedIn-scraper)  
3. spinov001-art/awesome-web-scraping-2026 \- GitHub, accessed on May 24, 2026, [https://github.com/spinov001-art/awesome-web-scraping-2026](https://github.com/spinov001-art/awesome-web-scraping-2026)  
4. GitHub \- kalil0321/ats-scrapers: Building the largest open-source ATS job dataset, accessed on May 24, 2026, [https://github.com/stapply-ai/ats-scrapers](https://github.com/stapply-ai/ats-scrapers)  
5. Fast and reliable Ashby job board scraper for Apify \- GitHub, accessed on May 24, 2026, [https://github.com/d-alleyne/ashby-job-scraper](https://github.com/d-alleyne/ashby-job-scraper)  
6. d-alleyne/greenhouse-job-scraper: Open source Apify Actor for scraping Greenhouse job boards with department filtering \- GitHub, accessed on May 24, 2026, [https://github.com/d-alleyne/greenhouse-job-scraper](https://github.com/d-alleyne/greenhouse-job-scraper)  
7. cporter202/scraping-apis-for-devs: This GitHub repo is a powerhouse collection of scraping APIs for developers that you can start using immediately to build everything from simple automations to full-scale applications., accessed on May 24, 2026, [https://github.com/cporter202/scraping-apis-for-devs](https://github.com/cporter202/scraping-apis-for-devs)  
8. Crawlee Tutorial: Easy Web Scraping and Browser Automation \- GitHub, accessed on May 24, 2026, [https://github.com/oxylabs/crawlee-web-scraping-tutorial](https://github.com/oxylabs/crawlee-web-scraping-tutorial)  
9. IonicaBizau/scrape-it: A Node.js scraper for humans. \- GitHub, accessed on May 24, 2026, [https://github.com/IonicaBizau/scrape-it](https://github.com/IonicaBizau/scrape-it)  
10. luminati-io/LinkedIn-Scraper: Extract LinkedIn data with the \#1 LinkedIn Scraper API, including profiles, job postings, company details, connections, and posts. Start your free trial now\! \- GitHub, accessed on May 24, 2026, [https://github.com/luminati-io/LinkedIn-Scraper](https://github.com/luminati-io/LinkedIn-Scraper)  
11. spinlud/py-linkedin-jobs-scraper \- GitHub, accessed on May 24, 2026, [https://github.com/spinlud/py-linkedin-jobs-scraper](https://github.com/spinlud/py-linkedin-jobs-scraper)  
12. spinlud/linkedin-jobs-scraper \- GitHub, accessed on May 24, 2026, [https://github.com/spinlud/linkedin-jobs-scraper](https://github.com/spinlud/linkedin-jobs-scraper)  
13. arshka/LinkedIn-Job-Scraper \- GitHub, accessed on May 24, 2026, [https://github.com/arshka/LinkedIn-Job-Scraper](https://github.com/arshka/LinkedIn-Job-Scraper)  
14. LinkedIn Job Scraper & Summarizer (Chrome Extension) \- GitHub, accessed on May 24, 2026, [https://github.com/anton-ds/linkedin-scraper-ext](https://github.com/anton-ds/linkedin-scraper-ext)  
15. pun-4/linkedin-jobs-scraper-incredibly-fast \- GitHub, accessed on May 24, 2026, [https://github.com/pun-4/linkedin-jobs-scraper-incredibly-fast](https://github.com/pun-4/linkedin-jobs-scraper-incredibly-fast)  
16. spinlud \- GitHub, accessed on May 24, 2026, [https://github.com/spinlud](https://github.com/spinlud)  
17. GitHub \- speedyapply/JobSpy: Jobs scraper library for LinkedIn, Indeed, Glassdoor, Google, ZipRecruiter & more, accessed on May 24, 2026, [https://github.com/speedyapply/JobSpy](https://github.com/speedyapply/JobSpy)  
18. Ever® Jobs™ \- aggregating jobs/gigs postings from multiple sources \- GitHub, accessed on May 24, 2026, [https://github.com/ever-jobs/ever-jobs](https://github.com/ever-jobs/ever-jobs)  
19. alpharomercoma/ts-jobspy: TypeScript job scraper for LinkedIn, Indeed, Glassdoor, ZipRecruiter & more \- GitHub, accessed on May 24, 2026, [https://github.com/alpharomercoma/ts-jobspy](https://github.com/alpharomercoma/ts-jobspy)  
20. GitHub \- FranciscoMoretti/jobsparser: CLI tool to scrape jobs from multiple job sites, accessed on May 24, 2026, [https://github.com/FranciscoMoretti/jobsparser](https://github.com/FranciscoMoretti/jobsparser)  
21. rynobax/indeed-scraper: A Node.js package for getting job listings from Indeed.com., accessed on May 24, 2026, [https://github.com/rynobax/indeed-scraper](https://github.com/rynobax/indeed-scraper)  
22. oxylabs/how-to-scrape-indeed: A tutorial for collecting job postings from Indeed using Python and Oxylabs Web Scraper API. \- GitHub, accessed on May 24, 2026, [https://github.com/oxylabs/how-to-scrape-indeed](https://github.com/oxylabs/how-to-scrape-indeed)  
23. job-scraper · GitHub Topics, accessed on May 24, 2026, [https://github.com/topics/job-scraper?l=typescript](https://github.com/topics/job-scraper?l=typescript)  
24. GitHub \- matthewincardona/job-board-scraper: A robust job scraper and AI-powered classifier. Uses JobSpy and Cloudflare AI workers., accessed on May 24, 2026, [https://github.com/matthewincardona/job-board-scraper](https://github.com/matthewincardona/job-board-scraper)  
25. SpeedyApply \- GitHub, accessed on May 24, 2026, [https://github.com/speedyapply](https://github.com/speedyapply)  
26. sruthi7sri/Job-Tracker-Smart-Application-Management-System \- GitHub, accessed on May 24, 2026, [https://github.com/sruthi7sri/Job-Tracker-Smart-Application-Management-System](https://github.com/sruthi7sri/Job-Tracker-Smart-Application-Management-System)  
27. GitHub \- billyweinberger/job-scraping-app, accessed on May 24, 2026, [https://github.com/billyweinberger/job-scraping-app](https://github.com/billyweinberger/job-scraping-app)  
28. Add additional sources (comment here to suggest another source) · Issue \#23 · nicobrenner/commandjobs \- GitHub, accessed on May 24, 2026, [https://github.com/nicobrenner/commandjobs/issues/23](https://github.com/nicobrenner/commandjobs/issues/23)  
29. erona-enner/workday-jobs-crawler \- GitHub, accessed on May 24, 2026, [https://github.com/erona-enner/workday-jobs-crawler](https://github.com/erona-enner/workday-jobs-crawler)  
30. viktor-shcherb/job-seek: Streamlit-based app for job portal scraping \- GitHub, accessed on May 24, 2026, [https://github.com/viktor-shcherb/job-seek](https://github.com/viktor-shcherb/job-seek)  
31. adgramigna/job-board-scraper: Scrapes job listings from popular job boards Greenhouse, Lever, Ashby, and Rippling \- GitHub, accessed on May 24, 2026, [https://github.com/adgramigna/job-board-scraper](https://github.com/adgramigna/job-board-scraper)  
32. Python script to apply for jobs on Workday \- GitHub, accessed on May 24, 2026, [https://github.com/raghuboosetty/workday](https://github.com/raghuboosetty/workday)  
33. jharemza \- GitHub, accessed on May 24, 2026, [https://github.com/jharemza](https://github.com/jharemza)  
34. jharemza/workday-scraper-api: Flask API service for ... \- GitHub, accessed on May 24, 2026, [https://github.com/jharemza/workday-scraper-api](https://github.com/jharemza/workday-scraper-api)  
35. GitHub \- MabudAlam/JobsScraper: Jobs Scraper: Streamline job searching by scraping and storing job postings from various websites ina SQLite3 database using this Go application., accessed on May 24, 2026, [https://github.com/Pavel401/JobsScraper](https://github.com/Pavel401/JobsScraper)  
36. How I scraped 2.1 million jobs (including 5335 data science jobs) \- GitHub Gist, accessed on May 24, 2026, [https://gist.github.com/thoroc/21601e286d9d4fec8505a88d71145ad9](https://gist.github.com/thoroc/21601e286d9d4fec8505a88d71145ad9)  
37. vesaias/JobNavigator: Self-hosted job search automation: AI scoring, multi-source scraping, resume builder, Chrome extension, React dashboard \- GitHub, accessed on May 24, 2026, [https://github.com/vesaias/JobNavigator](https://github.com/vesaias/JobNavigator)  
38. ejirocodes/job-finder: Supercharged job search with AI \- GitHub, accessed on May 24, 2026, [https://github.com/ejirocodes/job-finder](https://github.com/ejirocodes/job-finder)  
39. Seekspider: A Scrapy Project for Job Scraping \- GitHub, accessed on May 24, 2026, [https://github.com/qinscode/SeekSpider](https://github.com/qinscode/SeekSpider)  
40. MCP server for YubHub \- Scrape \*any\* careers page. Get a structured job feed. \- GitHub, accessed on May 24, 2026, [https://github.com/houtini-ai/yubhub](https://github.com/houtini-ai/yubhub)  
41. zahradnik-ondrej/jobscz-scraper: A simple data scraper of Jobs.cz written in multiple JS/TS libraries. \- GitHub, accessed on May 24, 2026, [https://github.com/zahradnik-ondrej/jobscz-scraper](https://github.com/zahradnik-ondrej/jobscz-scraper)  
42. calebmwelsh/Upwork-Job-Scraper \- GitHub, accessed on May 24, 2026, [https://github.com/calebmwelsh/Upwork-Job-Scraper](https://github.com/calebmwelsh/Upwork-Job-Scraper)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABGCAYAAABxPchcAAAG8ElEQVR4Xu3dV4glWxUG4G3OiooBRRlFMCGIiogIY8KEggkVDFxUDKAgCCrqgyiomMEXEcODqIhiRBEfvNeAWcGA6cF7Meecc/1WFbN7dZ0+1TNzpsee74NNz1pV+1Sd09PU6r13VbcGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAXmIcN7Tk1ucG/a4Jj5x81cUzdpyYAYNd+PrT/TO1PQ/vV0H7f5e56atc9rjS0kzW5xW+GdtuaPEJ5r/P75PTdbGg/rsnO22qi86Y2fv7frxsm9xrat9u4z9vLtqOSX1S+XJMAsGu5GP69JgdvbOO2u9cNg3/VxArXbedfcXTzdv6d0/+bfH5XLblPt3FU9aCCONvv18VL+/Ujs08b2gO6+CjlXG9UkwCwS7n4vLgmJ0sX3Gss5NY636ZGb9hO/70cJ2fyGfytJjp3aptfu+YTv7yLX9L2j8jWPkflSUP7S00CwC7lIni1mpx8oe2/SH5jaB8tubVeNbSr1+QRul7b//4uRKf7GdxkaM+ryc6mgu2hQ/tmyaXw6/dd6pdcpmAP8sya6NylJs7A0vkBwE48qh184cnaoro98bVKbpZ8Fp9nHdwv2vIauK/UxI59aWjvHdoTh/b1of2s27ZpmjZTxK9v41qlfv+vtnH/uV1c4ujjFITbPLjt7Z/p5hw38eXaWGSkmMl6w6wDrN46tD+0cXTq0qHdfu/mVZY+gzVq0VVtKtguG9qHS25eqzZb6pfcmrVs766JNn5PMzq81i3beLzPT19vvHfz/3KvKTkA2IlccC+pyU5fSPS5TbLt2tO/XzDF1VKulxsaUnisae+b+hzknyXeVrAlvncXP3bKza48xY+c4lzI++2XL/Ear2xjn991ucQpMvppwuSe1cVfbGMh18s+tyq5bQ57vrNt/TYVbClA6/cuxXS/71K/5FJAbfP8ob2/i/NLxDW7eJuXtf3nUn/RyP8jNx8AcE7kQnTPmuxke3/hWipwZj8c2pO7OHcAPrCLZ5v670qOd+su7gue+n4uLvGs5hLnrtrIFG/iV0xxpuxeNP17rayJymv0C9l/OeV6iT9e4vqYiTpStcZh959t67epYEshWgu2r7W9+y71S+5bNbnBXLQ9vG0eEV5yxzYe53ZTPBfgGXHrfXZofyw5ANiJpYvi7Llt3P70LneHKVddpS3nl6zd72zJ8frWqwXb0j6RXD9C8+opF5luzRTcHH9u+noYT2j7j/uThVziT5Q4I369j0z5JfPo4Jr2nanPQTYdZ7apYEtx9qGSy2hvv+9Sv+RqoXeQfG/mwnqt+f1v8662bj8AOCPzM7CW3KaN215YN7TlPm9uy/kla/bLaNWa1o+WrZG7YfvjH6Zgq4vd5/3mdVxzfMn09TDqtGv8YCGX+JMlvkUXx2em/GEcdv/Ztn6bCrZMl9f1b2tvOnh0TW6QO5LnIvuD/YYtcoy31OSCjPT9uiYB4GzLhWnpohjJZ6RmyVKfx7fl/ONqYvDnmtixehdjf56Zguzj15Z4tpTL+qXchHBiirOmKWvRrj/vcAgXtf3HyBRzzSX+VImf3cWR9Vq13zaH3X+2rd+mgi1qPnE/6paCrt60Ufts0hdrkWe49WvaDpJjXFSTbf/U81+H9rGSA4Cz6gptvDDVPyeUNWi5S7F/oGmVfidrsu2/mGb92v1LLsXM60pu1+p59XGe81W350KcxfyzjFgtPXPrpm1v37uV+DBSdKVvP7352ynXS5zHqszq4vhIfJ2S26a+xlrvaPunZHsPaptfO/n+gbuJc8PJLMXapV2cmzvWLPLPaGXWFVZPGdp7anLBT4f2vS7Oz0p+Jk50ucj55vEkALATKUhysZlb7qLMdFSKkjWPKbis7V9/FHkm1/yamSpaupi9tI3TkOfSI9reP8F1xSmf95w/qZSpxzq1lfOc99/0UOHo15PFO0u8xkOG9qM2nkfWreU1M3KXEbbkcu73aOOjOxIn35/vndup6cT+/R3GpqJqmxNt/whf5Jwz4ji/h3zOKUB7923jcT/QxseV1EX9kRsv8joHrcur8r3bZOkmmCXzY1XS3lC2zdaeDwAciTxb7XQvVnVE77g72U5d+De188GZnMeFeKfkY9pYXAPAeW3N1FL1jLZ3qpHjIaNoKWAuJGdS4ALAOfXdmjhAnmW19AfmOR4upAImI2s3qEkAOF89tY0PfF0ji7Y5vvIntM713b9HJWsiAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOAf+Czht03zDFoWsAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAaCAYAAAAue6XIAAABzklEQVR4Xu2WPS8EURSGX98FCZVEKSIarWhJfESn4x/oVUKBRCU0hHoLf0BLIwqFSiLxEaJCKSQSxOc5uXvtePfc3TvLRsg+ySnmOefOnJncOTNAhb9Fm0Q1ywBpan+cZolLlkV4ZxHDosQd3GKNB4kbcsef1TalXLhe4o1lLL4xiyeEc+cSkywj2ZNYZhmDNrPLMksTXH6OvBK6iRhqUML6cbhF/ZxIYD35NYl7cmnRcw6wLMQR8hthrGb1eIEcoy/fqsSSRAvllBOJfZaFsBphrBo97iSX5EriArkxxeuVadg+iBbvsEwwBFfDU0FdLTnPI9xE8ZzCbspvwSh8cR/5JGdwNa3kQxeZgX0jVXSs9CJ8njxCd5xE868sEV6nPpRjehBfW/TE/uWzPo/qdfww6nWvxjCGwtf/ghaG5us8XL6bE1k018ESzmdYws1rZgqRzfq9NUh+FO7leCbP6NpZlsIW8hsYkbglpxxKHLBMsg63B/0W0HiB+6zqv8EG3Le7GBnYDSibyJ1b/zX0AVhofphlOWhE/hNMg06H76xPzbXEBMtItiVWWJaTOpT2dHS6WOOw7LTDzes0/Eqjni7YXygLHXcNLCtU+A98AC1sfAGfm3SdAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE0AAAAZCAYAAAB0FqNRAAACkElEQVR4Xu2WS6jNURTGl0dhIAkDYaiUkFAiUZKJMCCPgakYSJGB8iiFSFIy8hooeQw8RqQcGTJTRpiglLyKPMrj+9prdfb5zr733POfXe1ffd27vv1ae//PfphVKpVhzgRooZqVMqOgP9Bf/1vpg7poDaiL1oC6aAXGQ9egV9A+6Epn8YCLNgm6Az2DdknZSmg+NA9a7B4vk7nQAi8bAS1yr5+LZpal8c5Cy9zbCF2EpkUlsA26Dm3NvByOfwJ6Cx2TskGZDn3P4omWFimntGjnoW9ZvNk62+2BXrp31b3jHr+D1kIjLX0oene9zlBYbuljsd126LH7M91bAn21tCjj3HvqdYKl7rOcxLz5AXtyA3oh3heJddHmuKfwi30Qj/V2ZvFv6GMW8zlzOYv7gX1rHiXvXsFjvEm8He73ZLWlij+hI5ZWXNFF48RLnR+0bl/b6qRuW/rFNYH9XCp4mgPHyD1uRa1D+Mukv0ULSpy09mDU887irkQ0DnZb8rk9Am7TqLsKWu/xBvdK/QwVtj1X8LTPm+LFkVCC/n01FW6PgF+cBycbrsh8TUTj4Kglf4b49A5Ye1sy6R/QZOiwe01gv2cKnuYWcwpuSRyMseRf0ALlobVvt+AXtD+LNZHTEgc8bEs++6PPxSJxJraiQkPYB29Q9TQHntu5N9Vj3uI5a9wfK34XLeu8PQkbTpFYE+Ev5UkW8/nBOnxCKDwjWDY78xjrjdwv7INPJfU010cF74F1j8863Mo9aVmaKC+CGJBvLDIaeg+9sXQz5rceie1IsZwLNxCaNCfC50ITTll6try2lNtnSx+ZuYbH/8knj+mzzV73yTpr58/LjZfisOOQtScxmCqVSqVSqVT+d/4BworVGhZzxNcAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAF0AAAAZCAYAAABTuCK5AAADIUlEQVR4Xu2YW6iNQRTH/26RFEkuoXNyCSmKB8qlhCclUYq8SW55IKQUHuQaL8SbUohnEgqlJMoDIYXIndzvl8L6t2a09tqzz/722Sf2w/zq3/nWf61vvpn59pmZvYFMJpPJZIrTUfTDm4Y5om+i36IToval6b/sgrbzWjTR5SJTRLehbR12uYZjOrSjy3yiDuLgo1IcFS008S1obVfjkfeizSb+KtpmYrJK9MvES1D5uQ3FBGhHd/pEHXxA5cH7FzI6xM+MNzV4lp4Jj/GIhOdfTsMyVPRddMQnWkFLk/4TpZ/OcdDaq8bjkpK6n96CcD0rxB6OIeU3NL1Eb0UXfKIGWpp0zxlobR/jMebL8dC/Hq7PhdhzH2k/Mlu0TnQgxJ1FK0UbRZ1ikbAWWjPEeJFJoouiy6K5ojul6dbTBToArrkdXK4aRSd9KbRuvvPpsQ0Pfa7t5F2IPTeR9iOrRU+gNXwBK4K/NXhNovPBGx68mSEmXIYPmZh9b+l5NdMbOrhTPlGFIpO+G3py+QQdnIX3vnEeoR/btdeWa0j7Fn56WXPM+fTs0hc92xfGi00cvboZBl1XD/pEQYpMemQatHaN8RjzZXvspDwNsecG0r6lGVrT5Hx6+xKebe9SiB+gfPJbxWRog1t8okZqmXTiB8Zrboge+nH9rLSm30PatwyA1vA/2UJvR8Lz7d01PrWxNF2MedCb2+rMXmnSu0P9Rc6PnW/nYg+9/eF6fYg9RU4v/aE1PIZa6G1PeLa9fuaa979E9eeVwE2EN9iNoi2oNOl7oP4X5/uB8V/c388XQs+eMCpN3HHneZqhdTypWehV+6T7fhF6hQ4bm0RjvNlGcFJTneuGcp/fTultcD69kSa+gvITzXPoCSvSF+UvJsVYaF3qi5Xfx1KTftrE0ftvfIR+s3wUxKMZd/7BpmYUtJM8h/P4x+vlJh9pgubOih5C20rxSvRCdBJaP6g0XQZ/8+EmzP7xL5ejvdAXSO8x9CeIgdClI3p8DuEz4k8o1GdRj5DLNCLcTGYU1PhwT6ZOuInwd48i8mtfJpPJZDKZzL/jD+83Agk1dw3gAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFMAAAAZCAYAAABNcRIKAAADAElEQVR4Xu2XS6iNURTHl7ciIjFA14A8k8cAedybR5EykAkhAxPKwBwpQonyHknyKGVACYmSEGYU8kp5peQZeT/W31qL/a2zv3u/c87t9g32r/6db/3X3vvsvc/+9t6HKJFIJBJl4B1rCasXqydrAettpoQwmHWd9Zt13uVCtrG+sV6zprhcqZhFMpiVPlEHaM9rQKYEUaP6xhgXG+9ZG4P4M2tLEJeSySSD2eoTNYB2NrP2sma4nIEyK5yH1XctiFHXT3DviFdahrC+so76RBW0NNi+JGXwGXJOfQOTG2sL3mJvlpk+JPvcJZ8oQGwCQtZRvMwByvp4/h7EBvxb3lTasZaTvGG71JvEOkzZ/XYq6whrTeCFbGc9Z+1kzWE1ZNO10ZX1mHWH1cHl8sBg77Nus66yfrA6BvkTWsazhyon80MQG/Cxd8boTDIRKHOP5NBqTzIOeKdYL+n/5LxRPyQWD3dezeB1xAl91idywJd3CeLT6hlY7b7DYAeJ319jPGOwHvix+iGxMifVwy3CwKoNy410MVhNrTCZQ0n2rYM+USXDSDq4VmPsx77DYDeJb6sYz/gRPfB/edMRm8xjEW9sxLO6GPdol6uaaSSNbfKJgvjtAK8Z2rurcd6euZ+yPp5xGHrgP/CmIzaZ2De9N0o99NEYr57pZ5ArzEKSyvXcOR+StIE9yuiu3mWN7RrW0mkemxAAb583HbG6hyLeCPVsMnGAQcYykvzFwGuWVSQV5vlEDTxhfXLebJL2FwUe4vlBDD5Sdo/EPdUPHgOF18n5nthkxlam7ZH2NjVS5dmAvTzvwMuwnjXOm3UwkPXIeV+osjNYhTjlDZukQYEH4GHAxg2Kn/Ce2GT6lQ+mq9dP4yaNu1kB5gxrQxC3KUtJOoR7Gj6vZNP/uEmyio+TlJuZTf+lgSR3gWTVo83m6MF6xXqqwjMONBxkz9TD1Qj3S/zAaA/eC5J7dRPJvzf0zX4QxIm2Bne6uQU1UeskcsDfxgkFVffFNZFIJBKJRCvyB4yd3mxlImnYAAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAkAAAAaCAYAAABl03YlAAAAbElEQVR4XmNgGAXkAn8gXgfEiegSIOAJxP+B2BHKnwrEZxHSDAyuDBAFckhiIP5pJD5Y4BWyABAoInPMGCCKfJEF0cFcBogivCCWAbeiGGQOSJEGsgAQvANid2QBKSD+wwBRDMKrkCVHARUBAGBkFHDwro5zAAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,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>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAZCAYAAAA8CX6UAAAAzUlEQVR4XmNgGAWUAjcglkUXJAf8h2KKQBMDwqAgNDmSAMwQEP6HJkc0UGZANQiE2VBUEAleAvF1IC5mQBi0H0UFkQCkURiJTVagdzGgaroK5YNwJJI4QQDSUILE54eKkeQqFQaI4q9Q/B2I/0DFYJgdrhoPAAXyXSBOQsPTGRAG7YerxgNACkXRBaGAoPe0gDgCiFcxIALUEEmeFyr/ESoPwt1QMSkkdQw1DBAvPQbiJ1D2BCR5DSB+D8TPoGpA+CkQvwViHyR1o2DkAgCArEPKtJWJpwAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAZCAYAAADXPsWXAAAAvElEQVR4XmNgGAU0A21A/J9IvAGqBycoZEAoFkaT40aS+4EmhwLwGQICPxkQ8mJocnBAyJArDAh5NTQ5OCBkCEzuL7oEMkA2pBqIC4C4HIj7kcTXwlXjAMiGgGKsBojrgLgJiPdCxb8DsQJUPVZAyDv5DAh5DTQ5OCBkCAjA5EEYK6CLIVEMCPmbaHIMekAcDsSLGBCKUqBiII3JQLwVSe4fRBsqwJV3/gDxLwZIjHwC4oNA7A7VMwpGFgAAJuhYA9E6V50AAAAASUVORK5CYII=>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADoAAAAZCAYAAABggz2wAAACJklEQVR4Xu2Wz0sVURTHT1Zgi6KF2cKgDCRyWYqBIAi5EmxntNaFGEGraBO8lRv/g9CFLsS1C5HChUKbAjERIwmeEC7c+CuoNKK+33dn9MyZufPGNyCI84Evb873nHtn7ry5P0QKCgrOM2+gfegnNGByaVyCVqB/0BZ0N5qucAi9hG5CV6DH0IYuSKJHXKfDNpGDNei9ilehDypO4w90QcV70KCKCZ/XqjtSkUKnuAajNnFCronrx0LvujUNM9B9a0q8P8YlaAx6Gk1lpwU6gKZsIiPLEn8wQo8PlgZrpo3Hf9f2Z+NcNEA70KJNVCH8lCw+X/NOXM035S2Jm++aav3URD1UFjfvLppcEr4B+XxLWEd9FfeJWpjjGrAJzQYxF6bcNEK70JxNJOAbkM+38MXqwW5H0xXo31bxq8CrmXvilvIJm0jBNyCfr2kWV8N5eSe4prhNVYN189asRpe4hiM2kQHfgHy+hnmuDZqFwL+hvMvqOiRL/0c8E1ecZ0/9Ick3pPfFmgoOJKkdof86uB4P4vbjdAV63INTeSGusM8maqBfkh+Y3kMVcy4+VzFJakfo3wquJ6G/Ej1UXBVX81Z5MUrQA2vmhDcdUjEPIXYQjKlW5XEucovR8OXzKwmpg36pmJQl3v+pwPMnb/wR+gz9lug/QJ5An4xH1sW15dYS9mFpE5fjWZi/36Ppc04T1JtRj4I2ZxIu5x0ZlXTgLigoKCjIwn/eF5XFjoFO3gAAAABJRU5ErkJggg==>