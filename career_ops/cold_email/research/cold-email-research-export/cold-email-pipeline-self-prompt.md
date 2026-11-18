# Job-Seeker Cold Email Pipeline: Two-Part Self-Prompt

*Prepared 14 Oct 2026. Sits downstream of the contact-finder pipeline (`claude/contact-finder-pipeline-research-prompt.md`): that one finds and verifies the emails, this one sends and converts them.*

- **Part 1: Deep research prompt.** Paste it into a deep-research tool (Claude Research, Perplexity, ChatGPT or Gemini Deep Research). It produces the research report and the recommended stack.
- **Part 2: Claude Code build prompt.** Paste it into Claude Code with the Part 1 report. It audits what exists, designs the sending layer, guides the infrastructure setup, then builds and ships a **working** cold email pipeline in n8n: domains → inboxes → ramp-up → personalised sequences → reply handling → monitoring → improvement loop.

**Fixed constraints for both parts**

| Constraint | Value |
|---|---|
| Use case | One-to-one job-seeker outreach (hiring managers, team leads, recruiters, startup founders) |
| Users | Me, my brother, later more job seekers; each sends **as themselves** under their own accounts |
| Location | India-based senders; recipients in India, US, UK, EU, Middle East and elsewhere |
| Target volume | ~100 emails/day total (first touches + follow-ups) within 6–8 weeks |
| Budget | **$20/month hard cap (~₹1,700)** for everything: domains, inboxes, tools, AI |
| Existing stack | Self-hosted n8n + the contact-finder enrichment pipeline (verified emails in an existing lead store) |

---

# PART 1: DEEP RESEARCH PROMPT

## ROLE

Act as a senior cold email deliverability engineer, outbound/GTM architect and job-search outreach strategist. You know how the best outbound teams in the world run cold email in 2026 (infrastructure separation, inbox rotation, ramp-up, list hygiene, signal-based targeting, reply handling, testing). You are skeptical of vendor marketing: most cold email "guides" are written by companies selling warm-up, inboxes or sequencers. Verify every claim against primary sources (mailbox provider docs, official pricing pages, RFCs, laws).

## CONTEXT

- I am building a reusable cold email system for **multiple job seekers** (me, my brother, later many more), mostly based in **India**, targeting roles in India and abroad.
- Upstream, a contact-finder pipeline already produces **verified work emails** of the right people (hiring managers, team leads, recruiters, founders), stored in a lead store with fields like `enr_email`, `enr_email_status`, `enr_email_source`.
- Goal: send **highly personalised** one-to-one emails (using the job post, the recipient's LinkedIn profile context and company context), with follow-up sequences, at **~100 emails/day total**, and turn them into replies, referrals and interviews.
- Budget: **$20/month total**. Exhaust every legitimate free tier first, then the cheapest reliable paid option. I already self-host n8n, so "build it in n8n" is a valid option for any stage.
- Each job seeker uses **their own accounts**. Do NOT recommend fake accounts, credit farming, purchased email lists, or anything that breaks a provider's Terms of Service. Flag tools whose ToS restricts cold outreach.

## WHY JOB-SEEKER COLD EMAIL IS DIFFERENT (apply this lens everywhere)

1. The sender is a **real person with a personal brand**, not a company. A burned domain or a spammy email hurts a career, not just a campaign.
2. Volume per person is low; **relevance per email** is everything. One great email beats ten generic ones.
3. Recipients may Google the sender or check the sending domain. A lookalike sales domain (e.g. `get-rahulsharma.com`) may look odd; a personal-brand domain (e.g. `rahulsharma.dev`) may look credible. Evaluate this.
4. The "conversion" is a reply, referral, call or interview, not a sale. Define the funnel accordingly.
5. Legal status may differ from commercial email (CAN-SPAM, CASL, GDPR, DPDP). Research it; don't assume.
6. Multiple job seekers may target the **same company or person**. The system needs collision rules.

## SEED FACTS FROM MY PRELIMINARY RESEARCH (14 Oct 2026, re-verify every one)

These came mostly from secondary sources. Confirm each against the primary source, correct it if wrong, and mark it High / Medium / Low confidence.

**Mailbox provider rules**
1. Gmail: bulk sender = roughly 5,000+ messages/day to personal Gmail accounts. All senders need SPF or DKIM, valid PTR, TLS and RFC-compliant formatting; bulk senders need SPF + DKIM + DMARC (p=none minimum, aligned), RFC 8058 one-click unsubscribe, and a spam rate under 0.3% (target under 0.1%).
2. Gmail: from November 2025 Google said it is "ramping up its enforcement on non-compliant traffic", with temporary and permanent rejections.
3. Microsoft (Outlook.com / Hotmail / Live): from 5 May 2025, senders of 5,000+/day must pass SPF, DKIM and DMARC (p=none minimum, aligned). Non-compliant mail goes to Junk, then is rejected with `550 5.7.515`.
4. Google Postmaster Tools v2 shows a compliance dashboard (Compliant / Needs work / No data) and a spam rate. At under ~100 Gmail recipients/day the data is usually blank, so at my volume it may show nothing.
5. Google Workspace hard cap: 2,000 emails/day per user; free Gmail: 500/day. Commonly cited safe cold volume: 20–30/inbox/day after ramp-up (some say 30–50). New inbox ramp: start at 5–10/day, grow over 3–4 weeks.
6. Hard bounce rate should stay under 2%.

**Warm-up**
7. Google told GMass (Jan 2023) to shut down its warm-up system or lose Gmail API access, and treats automated warm-up as a ToS violation. Several vendors stopped warming Google accounts. Is this still Google's position in 2026, and does it apply to IMAP/SMTP-based warm-up and to Microsoft 365 / Zoho?
8. Free warm-up tiers: TrulyInbox free (1 inbox, 10 emails/day, no expiry); Snov.io free (1 warm-up mailbox, 15 emails/day); Mailflow (5 emails/day); Warmup Inbox reportedly ~$15/inbox (per month or per year? confirm); Mailivery from ~$29/month.

**Inboxes and domains**
9. Google Workspace Business Starter: $7/user/month (annual) or $8.40 (flexible), after the 2025 price rise. Find the **India (INR) price**, which may be lower.
10. Zoho Mail: Forever Free plan is web-only (no IMAP/SMTP), so it cannot connect to a sender. Mail Lite ≈ $1/user/month (annual) with IMAP/SMTP. Check Zoho's acceptable-use policy on cold outreach.
11. Microsoft 365 Business Basic ≈ $6/user/month. Confirm the India price.
12. Cold email inbox resellers: Zapmail $39/month for 10 Google inboxes (~$3–3.90/inbox); Mailforge ~$3/inbox; Inframail $99/month flat (Microsoft). Check minimums, whether reseller accounts get suspended, and whether any fit a $20 budget.
13. A `.com` costs ~$10–11/year at at-cost registrars (Cloudflare, Porkbun). Check `.in`, `.dev`, `.me`, `.co` prices and renewals.

**Sending / sequencing tools**
14. Instantly: Growth $47/month (≈$30/month annual), no free plan, unlimited inboxes + warm-up.
15. Saleshandy Starter ≈ $25/month annual (~$36 monthly), plus a reported $4/month fee per connected Google/Microsoft mailbox.
16. Lemlist Starter ≈ $24/month annual. GMass Standard $29.95/month (Jan 2026). Mailmeteor ~$10/month (free: ~50/day, no sequences).
17. Free sequencer tiers: Hunter free (50 credits/month, 1 connected account, 500 recipients/campaign); Snov.io free (50 credits, 100 recipients/month); Apollo free (2 sequences, ~75–100 credits/month, no warm-up).

**LinkedIn context and AI**
18. LinkedIn sued Proxycurl (Nubela) in Jan 2025; Proxycurl shut down in July 2025. Alternatives: scrapers (Apify, Bright Data, ScrapIn: ~$1.50–$10 per 1,000 profiles), datasets (People Data Labs, Coresignal), account-based APIs (Linked API ~$49/seat/month, Unipile).
19. Apify free plan: $5 platform credit per month, no rollover; LinkedIn profile actors "from $10 per 1,000 profiles".
20. Clay free plan: 100 Data Credits + 500 Actions/month, 200-row table cap; Launch plan from ~$167–185/month. Bring-your-own API keys supported.
21. Gemini API free tier covers some Flash/Flash-Lite models, but free-tier content "is used to improve Google's products", and apps serving EEA/UK/Swiss users must use the paid tier. So prospect personal data may not belong on free LLM tiers.

**Benchmarks (sales cold email; job-seeker numbers may differ)**
22. Instantly 2026 benchmark (2025 data): average reply rate 3.43%; top quartile ≥5.5%; top 10% ≥10.7%; 58% of replies come from the first email, 42% from follow-ups; 4–7 touches optimal; top performers write under 80 words; Tuesday/Wednesday peak.

**Law**
23. India DPDP Rules notified 13 Nov 2025; most obligations (notice, consent) apply after 18 months (~May 2027). The Act exempts personal data processed by an individual for a personal or domestic purpose. Does one job seeker's own outreach fall under that? Does a system run for many job seekers?

## RESEARCH SCOPE: EVERY STAGE OF THE PIPELINE

For each stage, explain **what the best teams do, why it works, the minimum viable version for my volume and budget, and the tools (free → limited free → paid)**.

### Stage 1: Sender identity and domain strategy
- Personal Gmail vs a personal-brand domain vs lookalike secondary domains vs the job seeker's existing domain. Deliverability, credibility to a hiring manager, risk to the person's primary account, cost.
- How many domains and inboxes per job seeker for ~100/day total, and why (reputation isolation, inbox caps).
- Domain naming rules, TLD choice (.com vs .in vs .dev and others; spam-filter perception), domain age, and buying "aged" domains (worth it or not).
- Forwarding the secondary domain to the job seeker's portfolio/LinkedIn so it looks legitimate when checked.

### Stage 2: Inbox provider
- Google Workspace vs Microsoft 365 vs Zoho Mail vs cold email inbox resellers vs cheap private-SMTP hosts (e.g. Purelymail, Migadu, MXroute) vs free Gmail.
- For each: price (USD + INR), minimums, IMAP/SMTP/API access, sending limits, inbox placement at Gmail and Outlook recipients, ToS on cold outreach, suspension risk, and whether one user with aliases is enough (and why not, if not).

### Stage 3: Authentication and DNS
- SPF, DKIM (2048-bit), DMARC (start policy, when to move to quarantine/reject, `rua` reporting), alignment, PTR, TLS, MX, BIMI (worth it or not), custom tracking domain (needed only if tracking).
- Free DNS hosting (e.g. Cloudflare) and free checkers (MXToolbox, mail-tester, DMARC report tools).
- Exact DNS records per provider, as a copy-paste checklist.

### Stage 4: Warm-up and ramp-up
- Does automated warm-up still work in 2026, and is it allowed for each provider? Separate evidence from vendor claims.
- The safest **manual / natural ramp** plan for a brand-new inbox (week-by-week volume), including real engagement (genuine conversations, newsletters, replies from friends).
- Free and cheap warm-up tools with exact limits; whether warm-up must keep running after ramp-up.
- How long before a new domain/inbox can send cold safely, and how to tell it's ready.

### Stage 5: List quality and targeting
- Re-verification before sending (how fresh must a verification be), catch-all handling, role accounts (`hr@`, `careers@`), and the bounce threshold that should pause sending.
- Targeting the right person per job post (hiring manager vs recruiter vs team member for a referral), how many people per company, and spacing between them.
- Signals that lift reply rates for job seekers: an open job post, a recent hiring post on LinkedIn, team growth, funding, product launches.

### Stage 6: Personalisation at scale (with LinkedIn context)
- **What context matters**, ranked by impact: the job post itself, the recipient's role, tenure, recent LinkedIn posts, shared background (school, company, city), company news, and the candidate's own matching proof points.
- **How to get LinkedIn context legally and within budget.** Rank every option by cost, data quality and risk to the job seeker's LinkedIn account: manual capture by the job seeker in their own browser, Sales Navigator, Apify actors, datasets (PDL, Coresignal), account-based APIs, search-engine snippets (Google/SerpAPI/Serper/Brave free tiers), public posts, company sites. Quote LinkedIn's User Agreement on automated access and copying. No fake accounts.
- **Which AI to write with.** Compare Claude, OpenAI, Gemini, Groq/open models and local models on cost per 1,000 personalised emails, quality, and **data-use terms** (training on inputs, EEA restrictions) given that prompts contain third-party personal data.
- **Writing framework:** structure, length, subject lines, the one ask, tone for each recipient type (hiring manager / recruiter / founder / peer for referral), what makes AI-written email feel generic, and guardrails against invented facts.
- Plain text vs HTML; links (how many, which); attachments (resume on first touch or not); signatures; spintax/variation; "creepy" personalisation to avoid.

### Stage 7: Sequences and follow-ups
- Number of touches for job-seeker outreach (vs the sales 4–7), spacing in business days, same-thread replies vs new threads, what each follow-up should add, the final "break-up" email, and switching channel (LinkedIn connect/comment) between emails.
- Send windows in the **recipient's** time zone and day-of-week effects; randomised gaps between sends.
- Stop conditions: reply, bounce, unsubscribe, out-of-office (reschedule), "not now" (snooze), referral (new lead).

### Stage 8: Sending engine
- **Buy vs build.** Compare paid sequencers (Instantly, Smartlead, Saleshandy, Lemlist, Snov.io, Woodpecker, Reply.io, QuickMail, Plusvibe, Salesforge, Emelia, GMass, Mailmeteor, YAMM, Hunter Campaigns, Apollo and any 2026 entrants) with **building it in n8n** (Gmail API / Microsoft Graph / SMTP + IMAP).
- For a build: Gmail API and Graph sending quotas, threading (`threadId`, `In-Reply-To`, `References`), reply detection, bounce parsing, OAuth setup, and n8n's native nodes and limits.
- Which zero-build free tier could run the whole thing on day 1 while the n8n build is in progress.

### Stage 9: Reply handling and conversion
- Reply classification (positive, referral, not now, not the right person, negative, unsubscribe, OOO, auto-reply, bounce) and the best next action for each.
- Speed-to-reply: alerting the job seeker fast (Telegram, WhatsApp, email, push) and AI-drafted responses they approve.
- The job-seeker funnel: sent → delivered → replied → positive → call/referral → interview → offer. What counts as good at each step.

### Stage 10: Monitoring and deliverability health
- Which signals are visible at ~100/day (Postmaster may be blank) and the substitutes: bounce rate, reply rate trends, seed/inbox-placement tests, mail-tester scores, DMARC aggregate reports, blacklist checks, Microsoft SNDS.
- Why open tracking is unreliable (Apple Mail Privacy Protection, bot opens) and whether tracking pixels/links hurt placement. Recommend what to track instead.
- Auto-pause thresholds (bounces, negative replies, placement drops) and recovery steps for a burned inbox/domain.

### Stage 11: Testing and improvement loop
- A/B testing at low volume: minimum sample sizes, what to test first (angle, ask, subject, length, follow-up timing), how to judge results honestly, and a weekly review ritual.
- How the world's best outbound teams iterate (copy libraries, winning-pattern logs, segment-level analysis).

### Stage 12: Compliance and ethics
- CAN-SPAM (is job-seeking email "commercial"?), GDPR legitimate interest for EU/UK recipients, UK PECR, Canada CASL, Australia Spam Act, UAE rules, India DPDP Act 2023 + Rules 2025 (with the personal-purpose exemption question), and the IT Act.
- What every email must contain anyway (real identity, honest subject, easy opt-out), suppression handling, data retention, and deletion requests.

## ANALYSIS TASKS

### Task 1: Hypotheses to test (give a verdict on each, with evidence)
- **H1:** For job seekers, a personal-brand domain per job seeker with 2 inboxes beats personal Gmail on safety, and beats lookalike sales domains on reply rate.
- **H2:** At $20/month, building the sender in n8n beats every paid sequencer, because any paid sequencer alone takes most of the budget.
- **H3:** Automated warm-up is unnecessary (and risky on Google) at ≤30 emails/inbox/day if the domain is authenticated and ramped manually over 3–4 weeks.
- **H4:** Zoho Mail Lite or Microsoft 365 gives acceptable inbox placement at a fraction of Google Workspace's cost.
- **H5:** Job-post context + one specific LinkedIn detail + one matching proof point gets more replies than heavy multi-detail personalisation.
- **H6:** 3 touches (1 email + 2 follow-ups) is the best number for job-seeker outreach.
- **H7:** No open tracking and no links in the first email improves inbox placement measurably.

### Task 2: Stack options at three budgets
Design three complete stacks: **$0/month**, **~$10/month** and **$20/month**. For each: every component by stage, the monthly cost line by line (USD + INR, one-time vs recurring, domains amortised monthly), capacity in emails/day, setup time, and the main risk. Pick **one recommended stack** and justify it.

### Task 3: Capacity and ramp model
- Inboxes and domains needed for 100 emails/day total, given caps per inbox and the follow-up share of daily volume (with 3 touches, about a third of sends are first touches).
- A week-by-week ramp table from day 1 to full volume, per inbox.
- How capacity scales for 1, 2, 5 and 20 job seekers, and the cost per job seeker.

### Task 4: Playbooks
- A copy-paste DNS checklist per inbox provider.
- 3 email templates per recipient type (hiring manager, recruiter, founder, referral ask) with variables marked, each under 100 words, plus 2 follow-ups each.
- The AI personalisation prompt (system + user) with anti-hallucination rules.
- A reply-handling playbook with a response template per reply type.

### Task 5: Funnel benchmarks
Realistic targets for job-seeker cold email (delivery rate, reply rate, positive reply rate, call/interview rate), with sources, clearly separated from sales benchmarks.

## DATA TO COLLECT PER TOOL

Write "Unknown" if a value is not found; never guess.

| Field | Detail |
|---|---|
| Stage | Domain / inbox / DNS / warm-up / verification / LinkedIn context / AI / sequencer / monitoring |
| Free tier | Exact limits, refresh cycle, one-time vs monthly, expiry |
| Entry paid plan | Price USD + INR, monthly vs annual, minimums, per-mailbox fees |
| Fits $20 budget? | Yes / partly / no, with the reason |
| API / n8n | API on free tier? Native n8n node, community node, or HTTP Request |
| Limits | Sending caps, rate limits, recipients, inboxes |
| ToS on cold outreach | Allowed / restricted / banned, with the quote |
| Data-use terms | Trains on inputs? Data location? (AI and data tools) |
| Evidence quality | Vendor claim vs independent evidence (separate columns) |
| Source + date checked | Official URL + date |

## VERIFICATION RULES

1. Official docs and pricing pages first (Google, Microsoft, Yahoo, Zoho, RFCs, laws), then independent sources (deliverability experts, Reddit r/coldemail, r/sales, r/emailmarketing, r/developersIndia, r/jobs), then vendor blogs.
2. Most cold email content is written by vendors. Name the vendor behind each claim and discount accordingly.
3. Treat any figure older than 6 months as **stale** and flag it.
4. When sources conflict, show both values and explain which you trust and why.
5. Mark every key number **High / Medium / Low** confidence.

## OUTPUT FORMAT

1. **Executive summary** (max 10 bullets), including the recommended stack and its monthly cost.
2. **Hypothesis verdicts** (H1–H7): supported / rejected / unclear, with evidence.
3. **Stage-by-stage playbook** (Stages 1–12): best practice, why, the minimum viable version for me, tools.
4. **Master tool table** with all fields from "Data to Collect".
5. **Three stacks** ($0 / ~$10 / $20) with line-item costs, plus the recommendation.
6. **Capacity and ramp model**: inboxes needed, week-by-week ramp, scaling for 1 / 2 / 5 / 20 job seekers.
7. **DNS checklist**, **templates**, **AI personalisation prompt**, **reply playbook** (Task 4).
8. **Monitoring plan**: metrics, thresholds, auto-pause rules, recovery steps.
9. **Funnel benchmarks** for job seekers vs sales.
10. **Compliance checklist**: do / don't, per country.
11. **Corrections to my seed facts** (which were wrong or outdated).
12. **Sources**: every claim linked, with the date checked.
13. **Open questions / gaps.**
14. **Machine-readable appendix:** the master tool table as a JSON array, plus the recommended stack, ramp schedule, thresholds and sequence timings as JSON, so Part 2 can ingest them directly.

## CONSTRAINTS

- No fabricated numbers. "Unknown" beats a guess.
- Separate vendor claims from independent evidence.
- Everything must be legal and within each provider's ToS. No fake accounts, purchased lists, or LinkedIn scraping through fake or rented accounts.
- Optimise for: deliverability safety > relevance per email > cost > volume.

---

# PART 2: CLAUDE CODE BUILD PROMPT (AUDIT → SETUP → DESIGN → BUILD → SHIP → IMPROVE IN n8n)

> Paste this into Claude Code. Put the Part 1 research report (and its JSON appendix) in the working directory as `research/`. If the contact-finder build exists, put its `AUDIT.md`, `DESIGN.md` and `TOOL_REGISTRY.json` in `upstream/`.

## ROLE

Act as a senior deliverability engineer and n8n automation architect. You build production-grade cold email systems **on top of systems that already exist**. You treat every sending inbox as a reputation asset that is slow to build and fast to burn, every email to a real person as irreversible, every API key as a secret, and every existing workflow as production that must not break. The operator (me) is semi-technical: explain each decision in one or two plain sentences and keep me in control at every gate.

If n8n-related skills are available in this environment (for example `n8n-operator` or `n8n-house-rules`), load them before any n8n work and follow them; they override general defaults.

## MISSION AND DEFINITION OF DONE

Build a cold email pipeline in n8n that takes **verified leads from the existing contact-finder pipeline** and turns them into personalised email sequences sent from each job seeker's own inboxes, then handles replies, protects deliverability, and improves itself from results.

**Done means all of these are true:**

1. Each job seeker has authenticated sending domains and inboxes (SPF, DKIM, DMARC passing, confirmed in real message headers) and a ramp-up schedule that the system enforces automatically.
2. A verified lead in the existing lead store flows into a sequence with no manual copy-paste: context gathered → email drafted → approved (by the job seeker, while approval is on) → sent at the right local time from the right inbox → followed up in the same thread → stopped on reply, bounce or opt-out.
3. Every personalised claim in every email traces back to a stored source (job post, LinkedIn context, company page, or the candidate's own profile). No invented facts.
4. Replies are classified, the job seeker is alerted within minutes for positive replies and referrals, and the right next action happens for every reply type.
5. Per-inbox caps, send windows and auto-pause rules can't be bypassed; a single kill switch stops all sending.
6. Total running cost stays within **$20/month** and is tracked in a cost ledger.
7. It has run on **real leads** for at least one job seeker, with a test report showing deliverability checks, reply rate, costs, and zero cap or suppression violations.
8. Existing workflows (including the contact-finder pipeline) keep working exactly as before.

## GUIDING PRINCIPLES

- **Discover before you ask.** Inspect what exists; ask me only what you can't find out yourself.
- **Integrate, don't rebuild.** Read leads from the existing lead store; write sending status back with a `ce_` prefix; reuse existing credentials and naming conventions.
- **Reputation first.** When in doubt, send less, later, or not at all.
- **Ship a thin working slice early.** One inbox, one seed lead, send → follow-up → reply-stop, end to end, before anything fancy.
- **Safety rails before features.** Kill switch, dry-run, caps, suppression and the cost ledger exist before the first real email.
- **Human in the loop at the start.** The job seeker approves every first-touch email until the quality bar is proven; then approval can relax per user, by their choice.

---

## PHASE 0: DISCOVERY AUDIT (read-only, no changes)

1. Check how you can reach n8n (public API, n8n MCP server, or CLI). If none work, ask me to export the relevant workflow JSONs into `existing/`.
2. Inventory all workflows (name, ID, active, trigger, schedule, tags, recent executions and error rate) and export the relevant ones into `existing/` as the baseline backup.
3. List existing credentials by name and type only (never print secrets): Gmail/Google OAuth, Microsoft, SMTP/IMAP, Sheets, databases, LLM keys, Telegram/Slack.
4. Map the contact-finder pipeline: where leads live, the exact schema, the `enr_` fields, how a lead is tied to a job seeker, and what "send-ready" means today (e.g. `enr_email_status = valid`). If that pipeline isn't live yet, define a minimal **input contract** (a Google Sheet or CSV with: `lead_id, user_id, first_name, last_name, title, company, domain, email, email_status, linkedin_url, job_post_url, recipient_type, timezone`) so this build doesn't block on it.
5. Check what already exists for sending: domains owned, DNS host, mailboxes, any sequencer accounts, any warm-up tools.
6. Check n8n hosting limits: version, execution timeout, queue mode, server resources, and whether polling-based triggers across N inboxes fit.

Produce `AUDIT.md` with a Mermaid flow map, the lead-store schema (personal data masked), what exists for sending, risks and unknowns.

Then ask me in **one batch** only what you couldn't discover, for example:
1. Which job seekers go first, and their target roles, countries and recipient types?
2. Their names for the domains (personal-brand preference), and any existing domains?
3. Where should approvals and alerts happen (Google Sheet tab, n8n form, Telegram, email)?
4. Is the candidate profile (master resume / bullet bank, e.g. from the Linkright system) available as a file, and where?
5. Any company or person that must never be emailed?

**Gate 1:** wait for my answers and my OK on `AUDIT.md`.

---

## PHASE 1: INGEST AND VALIDATE THE RESEARCH

1. Turn the Part 1 report into config files:
   - `STACK.json`: the chosen tool per stage, with cost and the reason.
   - `TOOL_REGISTRY.json`: one record per tool (stage, free limits, cost, API/n8n support, ToS notes, data-use terms, confidence, last verified).
   - `ramp_schedule.json`: daily cap per inbox by ramp day.
   - `thresholds.json`: bounce, negative-reply and placement thresholds that trigger a pause.
   - `sequences/*.json`: steps, delays in business days, send windows, stop rules, per recipient type.
2. Re-check the **current official docs** for the chosen inbox provider and sending method (quotas, OAuth scopes, threading behaviour, cold-outreach ToS). Where docs disagree with the research, trust the docs and log the difference in `DECISIONS.md`.
3. Write `BUDGET.md`: every recurring and one-time cost line in USD and INR, domains amortised monthly, LLM cost per 1,000 emails at the expected volume, and the total. It must be ≤ $20/month; if not, propose cuts.
4. Write a short **Gap Report**: missing data, low-confidence numbers, and the assumptions you'll use.

**Gate 2:** wait for my OK.

---

## PHASE 2: INFRASTRUCTURE SETUP (guided; I do every purchase)

You never buy anything or create paid accounts. You give me exact steps, then verify my work.

1. **Domains:** propose 3–5 name options per job seeker following the research rules; I buy them. Set them to forward to the job seeker's portfolio or LinkedIn.
2. **Mailboxes:** step-by-step creation for the chosen provider, with naming (e.g. `firstname@`, `f.lastname@`), profile photo, display name and signature.
3. **DNS:** generate the exact SPF, DKIM, DMARC (start policy + `rua` address), MX and any tracking-domain records per domain. If I give you a DNS API token (e.g. Cloudflare, scoped to these zones only), apply them via the API; otherwise give me a copy-paste table.
4. **Verify:** check every record with `dig`/DNS-over-HTTPS, then send a test to mail-tester and to seed inboxes I own (at least one Gmail, one Outlook, one Yahoo) and read the headers: SPF, DKIM and DMARC must all pass and align.
5. **Ramp start:** record each inbox's start date so the ramp schedule begins, plus the manual/natural warm-up actions the research recommends, as a daily checklist for me.

Output: `INFRA.md` with every domain, inbox, DNS record, verification result and screenshot/header evidence.

**Gate 3:** all checks green, and my OK.

---

## PHASE 3: DESIGN (`DESIGN.md`, no building until approved)

Design for failure modes, not just the happy path.

### 3.1 Integration with the lead store
- **Hook:** how send-ready leads enter (recommend one: a scheduled pull of `enr_email_status = valid AND ce_status IS NULL`, an Execute Workflow call from the contact-finder, or a status-change trigger). Show the before/after diff of any existing workflow you'd touch.
- **Write-back columns** (prefixed so nothing existing is overwritten): `ce_status, ce_campaign_id, ce_sequence_id, ce_step, ce_inbox, ce_thread_id, ce_last_sent_at, ce_next_send_at, ce_reply_type, ce_reply_at, ce_variant, ce_sources, ce_error`.
- **Feedback upstream:** a hard bounce sets the email to invalid in the contact-finder's fields (and updates its domain-pattern learning); a referral reply creates a new lead in the existing ingestion path with `referred_by`.
- **Kill switch:** one flag that stops all sending and drafting; the contact-finder keeps running.

### 3.2 Data model
Decide where each store lives and justify it (Google Sheets for human-facing queues; a real database such as Postgres/Supabase free tier for logs and anything written often or concurrently):
- `ce_users`: user_id, name, timezone, approval_mode, alert channel, signature, candidate profile location
- `ce_domains` and `ce_inboxes`: provider, credential name, ramp start date, today's cap, status (`ramping / active / paused / resting / burned`), health score
- `ce_campaigns`: per job seeker per target role/market
- `ce_messages`: every draft and send (lead, step, variant, subject, body, `facts_used[]` with sources, approved_by, sent_at, message_id, thread_id)
- `ce_events`: sent, bounced, replied, opted_out, paused, error
- `ce_replies`: raw text, classification, confidence, action taken
- `ce_suppression`: global across all job seekers (emails and domains), with reason and date
- `ce_company_locks`: which job seeker is contacting which company/person, and until when
- `ce_experiments` and `ce_daily_metrics`
- `ce_cost_ledger`: month, tool, units, cost

### 3.3 Lead state machine
`queued → context_pending → drafting → awaiting_approval → scheduled → sent_step_n → (replied | bounced | opted_out | ooo_rescheduled | snoozed | completed | failed | skipped_suppressed | skipped_collision | skipped_disabled)`. Every transition is persisted, so a crash resumes without double-sending.

### 3.4 Scheduler and caps
- Per-inbox daily cap from `ramp_schedule.json`, never above the research's safe maximum, enforced atomically (two executions can't both take the last slot).
- Send windows in the **recipient's** local time and preferred weekdays; no weekends; randomised gaps between sends; per-domain hourly cap.
- Inbox rotation across a job seeker's inboxes; a sequence always continues from the inbox that sent step 1 (same thread, same sender).
- Follow-ups have priority over new first touches when capacity is tight.
- Company spacing: at most N people per company per job seeker, at least M business days apart (from research).

### 3.5 Sending adapter
- A standard contract, so the provider can change without touching the rest. Input: `inbox_id, to, subject, body_text, thread_ref, dry_run`. Output: `status, message_id, thread_id, provider_response, error_code`.
- Implement the provider the research chose (Gmail API / Microsoft Graph / SMTP). Plain text only; follow-ups as true replies in the same thread (`threadId`, `In-Reply-To`, `References`); no tracking pixels or tracked links unless the research says otherwise.
- **Idempotency:** a unique key per lead × step; check `ce_messages` before every send.

### 3.6 Personalisation engine
- **Context gathering**, cheapest and safest first: job post text → company page/news → LinkedIn context. For LinkedIn, build the lane the research approved; by default a **manual capture lane** (a daily task list where the job seeker pastes the recipient's headline, About and one recent post into the lead row). Only add an automated provider if the research rated it compliant and it fits the budget.
- **Candidate claims** come only from the candidate profile (master resume / bullet bank). The model may select and rephrase proof points, never invent them.
- **Drafting:** a versioned prompt in `prompts/` per recipient type, using the research's writing framework; output as JSON: `subject, body, followups[], facts_used[{fact, source_field}], confidence`.
- **Validator** (code, not AI): every fact maps to a stored input; word limits; no banned or spam-trigger phrases; link and attachment rules; correct name, company and role; personalisation present. A failed validation means redraft once, then send to manual review.
- **LLM choice** follows the research's data-use findings (no free tier that trains on prospects' personal data); cost is logged per call to `ce_cost_ledger`, with a monthly cap that pauses drafting, not sending of already-approved emails.

### 3.7 Approval queue
- A simple review surface (Sheet tab or n8n form) showing the draft, the sources used and an approve / edit / reject control. Edits are saved as training examples for the copy library.
- `approval_mode` per user: `all` (default), `first_touch_only`, `low_confidence_only`.

### 3.8 Reply handling
- Detect replies per inbox (polling or push; show the execution maths for N inboxes) and match them to `ce_thread_id`.
- Classify with rules first (bounce, auto-reply, OOO), then the LLM: `positive, referral, not_now, wrong_person, negative, opt_out, question`.
- Actions: stop the sequence on any human reply; alert the job seeker on positive/referral/question with an AI-drafted response to approve; OOO → reschedule after the return date; `not_now` → snooze for the research's interval; `wrong_person` / `referral` → new lead with context; `opt_out`/`negative` → global suppression.
- Bounces: parse the DSN, mark the address invalid, feed it back upstream, and count it toward the inbox's health.

### 3.9 Deliverability monitoring and auto-pause
- Rolling per-inbox metrics: sends, hard bounces, replies, negative replies, opt-outs.
- Auto-pause rules from `thresholds.json` (e.g. bounce rate over the threshold in the last 50–100 sends, a cluster of negative replies, a failed DNS check, a blacklist hit, a seed-test spam placement). A paused inbox stops new first touches immediately and alerts me.
- Scheduled checks: daily DNS record check per domain, daily blacklist check, weekly seed-placement test across Gmail/Outlook/Yahoo seeds, DMARC aggregate report parsing if the research recommends a free tool or a simple parser.
- Recovery playbook steps from the research, as runbook entries.

### 3.10 Multi-user and collisions
- A new job seeker = a config row + domains/inboxes + credentials named `<provider>_<user_id>_<inbox>`. Write that checklist.
- Global suppression applies to everyone. `ce_company_locks` prevents two job seekers from emailing the same person, and spaces out different people at the same company.

### 3.11 Experiments and improvement loop
- Random variant assignment per lead, stratified by recipient type; minimum sample sizes from the research before calling a result.
- Weekly report: funnel per user, campaign, recipient type and variant; best and worst emails (anonymised); a recommended next test.
- A `copy_library.md` of winning patterns, updated only from tested results.

### 3.12 Compliance
Real identity and honest subject lines in every email; an easy opt-out line as the research recommends; suppression checked before every draft and every send; source and timestamp stored per personal-data field; deletion requests supported; a data-retention rule (e.g. delete context for leads inactive for N days).

### 3.13 Observability
- Daily digest to each job seeker: sent per inbox, replies (with links), positives, bounces, inbox health, tomorrow's queue, pending approvals, manual capture tasks.
- Daily admin digest to me: all users, costs vs budget, errors, dead-letter count, paused inboxes.

### 3.14 Rollout and rollback
Dry-run (everything redirected to my seed inboxes) → one job seeker, one inbox, 5 real leads with approval → ramp per schedule → second job seeker. Rollback: kill switch + restore backup JSONs.

**Gate 4:** wait for my approval of `DESIGN.md`.

---

## PHASE 4: BUILD (thin vertical slices)

Use the `ce_` prefix for every new workflow.

- **Slice 0: Safety rails.** Data stores + seed config, kill switch, dry-run flag (redirects all mail to seeds), atomic cap counter, suppression check, idempotency check, error handler + dead-letter, cost ledger.
- **Slice 1: One inbox, end to end.** Hand-written email to a seed address → send → follow-up in the same thread after a short test delay → reply from the seed stops the sequence → bounce test to a known-bad address is detected.
- **Slice 2: Scheduler.** Ramp caps, recipient time zones, send windows, rotation across inboxes, follow-up priority, company spacing.
- **Slice 3: Personalisation.** Context gathering, the manual LinkedIn capture lane, drafting prompts, the validator, and the approval queue.
- **Slice 4: Replies.** Detection, classification, alerts with drafted responses, OOO/snooze/referral handling, and bounce feedback to the contact-finder.
- **Slice 5: Health.** Rolling metrics, auto-pause, DNS/blacklist checks, seed tests, daily digests.
- **Slice 6: Improve and scale.** Experiments, the weekly report, the copy library, and onboarding a second job seeker.

Build rules:
- Prefer native n8n nodes and the HTTP Request node; keep Code nodes small and commented.
- No secrets anywhere except n8n Credentials.
- Add sticky notes explaining each section in plain English.
- Export every new or changed workflow JSON into `workflows/` in git, one commit per slice.
- **Never send to a real prospect, edit an existing workflow, write to the production lead store, or spend money without telling me first.**

---

## PHASE 5: TEST AND PROVE IT WORKS

- **Authentication:** SPF, DKIM and DMARC pass and align in the headers of a message received at Gmail, Outlook and Yahoo seeds; mail-tester score at or above the research's target.
- **Placement:** seed tests land in the inbox (not spam/promotions where avoidable) for each inbox.
- **Threading:** follow-ups appear in the same thread in Gmail and Outlook.
- **Stops:** reply, bounce, opt-out and OOO each produce the right state and action.
- **Caps:** trying to exceed an inbox's cap is blocked; two parallel runs can't overspend the last slot.
- **Idempotency:** kill a run mid-send and resume → no duplicate email.
- **Suppression and collisions:** a suppressed address and a locked company are both skipped, for every user.
- **Validator:** a draft with an injected fake fact, a wrong name or a banned phrase is rejected.
- **Time zones:** a US lead and an Indian lead are each sent inside their local window.
- **Kill switch and dry-run:** both behave exactly as designed.
- **Regression:** the contact-finder and all existing workflows still run, and their columns are unchanged.
- **Cost:** the ledger matches real invoices and usage; the LLM cap pauses drafting.
- **Live pilot:** one job seeker, 5 → 20 real leads with approval, over 1–2 weeks, within ramp caps.

Write `TEST_REPORT.md`: deliverability evidence, sends, bounces, replies by type, cost, time per lead, and failures with causes.

**Gate 5:** go-live approval.

---

## PHASE 6: OPERATE AND IMPROVE

- Follow the ramp schedule to ~100 emails/day total across inboxes; never skip ramp steps.
- **Weekly review** (generate the agenda automatically): funnel numbers vs benchmarks, inbox health, what changed, the experiment result, one decision, one next test.
- **Monthly:** cost vs budget, tool and price changes (re-verify the stack), rest or retire unhealthy inboxes, refresh the copy library.
- When a new job seeker joins: run the onboarding checklist (Phase 2 for their domains, then config only).

---

## DELIVERABLES

1. `AUDIT.md`: the existing system map and lead-store schema.
2. `STACK.json`, `TOOL_REGISTRY.json`, `ramp_schedule.json`, `thresholds.json`, `sequences/`.
3. `BUDGET.md` and a live `ce_cost_ledger`.
4. `INFRA.md`: domains, inboxes, DNS records and verification evidence.
5. `DESIGN.md` (the approved version), including any integration diff.
6. `existing/`: backups of existing workflows before any change.
7. `workflows/`: all new and changed workflow JSON, version-controlled.
8. Schema + seed scripts for the data stores.
9. `prompts/`: versioned drafting and reply-classification prompts, plus validator rules.
10. `copy_library.md`: templates and tested winning patterns.
11. `RUNBOOK.md` (for a non-technical operator): approve drafts, do manual LinkedIn capture, read the digest, pause/resume an inbox, handle a burned inbox, add a job seeker, add an inbox, rotate a credential, run the weekly review, roll back.
12. `TEST_REPORT.md` with real numbers.
13. `DECISIONS.md`: every trade-off and why.

## ACCEPTANCE CRITERIA

- Verified leads from the existing pipeline flow into personalised sequences with no manual copy-paste (except the approved manual LinkedIn capture lane).
- Every domain passes SPF, DKIM and DMARC with alignment, confirmed in received headers.
- No inbox ever exceeds its ramp cap; auto-pause fires on threshold breaches.
- Zero duplicate sends, zero emails to suppressed addresses, zero collisions between job seekers.
- Every personalised fact has a stored source; the validator blocks invented facts.
- Replies stop sequences, and positive replies reach the job seeker within minutes.
- Monthly cost ≤ $20, tracked in the ledger.
- Existing workflows and the contact-finder are unaffected; the kill switch stops all sending.
- A new job seeker = Phase 2 for their domains + config only.

## WORKING STYLE

- Phases with explicit gates: after the audit, after the research ingest, after infrastructure, after the design, and before go-live. Also stop before any first real send, any production write and any spend.
- Discover first, then ask; never assume a field name, schema or DNS host.
- Explain the "why" behind each design choice in one or two plain sentences.
- Report progress at the end of each slice: what works, what was tested, and what's next.
