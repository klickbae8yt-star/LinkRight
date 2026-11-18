# Cold Email Pipeline: Raw Research Findings

**Research date:** 14 Oct 2026 (preliminary pass, done to seed the self-prompt)
**Scope:** job-seeker cold email at ~100 emails/day on a $20/month budget
**Method:** web searches plus page reads. Most pages are **secondary sources**, often written by vendors who sell cold email tools. Every number below needs re-checking against the official source before you rely on it. That re-check is exactly what Part 1 of the self-prompt asks the deep-research tool to do.

**Confidence key:** High = official source or several independent sources agree. Medium = one credible secondary source. Low = vendor marketing, inconsistent source, or unclear date.

---

## 1. Mailbox provider rules (Gmail, Yahoo, Microsoft)

### 1.1 Gmail and Yahoo sender requirements
Source: [LeadHaste: Gmail deliverability requirements 2026](https://leadhaste.com/blog/gmail-deliverability-requirements-2026) (published 22 Jul 2026, updated 21 Sep 2026; LeadHaste is a vendor that sells cold email services). Confidence: Medium.

- **Bulk sender:** roughly 5,000+ messages/day to personal Gmail or Yahoo addresses. This is the strictest tier.
- **All senders:** SPF, DKIM, matching reverse DNS (PTR) and TLS. The article recommends meeting the bulk-sender bar even below the threshold.
- **DMARC:** required for bulk senders. `p=none` is fine to start; move toward quarantine/reject after 2–4 weeks of watching reports.
- **Spam complaint rate:** enforcement starts at **0.3%** (about 3 complaints per 1,000 recipients). Real target: **under 0.1%**.
- **One-click unsubscribe (RFC 8058):** required for bulk marketing/subscription mail; honour opt-outs within a couple of days. Transactional mail is exempt.
- **Vendor guidance (not official rules):** hard bounces under 2%; 30–50 sends per inbox per day; about 2–3 weeks of domain warm-up.
- The article claims bulk-level authentication failures are rejected at SMTP level rather than filtered to spam (unverified).
- Official reference linked in the article: Google sender guidelines, support.google.com/mail/answer/81126.

### 1.2 Gmail enforcement ramp-up (November 2025)
Source: [Spam Resource: Google warns sender requirements enforcement ramping up](https://www.spamresource.com/2025/11/google-warns-sender-requirements.html). Confidence: High (it quotes Google's own FAQ text).

- On **3 Nov 2025** Google added this to its Bulk Sender Guidelines FAQ: *"Starting November 2025, Gmail is ramping up its enforcement on non-compliant traffic."*
- Non-compliant messages "will experience disruptions", including **temporary (4xx) and permanent (5xx) rejections**. Before this, enforcement was more sporadic.
- The requirements themselves did not change: authentication, alignment, easy unsubscribe, low complaint rates, RFC compliance.
- Google's DMARC reporting now includes SMTP response details on authentication, RFC and compliance, which helps monitoring.

### 1.3 Microsoft (Outlook.com, Hotmail, Live)
Source: [Mailgun: Microsoft sender requirements](https://www.mailgun.com/blog/deliverability/microsoft-sender-requirements/). Confidence: High (widely reported, matches Microsoft's announcement).

- **Effective date:** 5 May 2025.
- **Threshold:** senders of more than 5,000 messages/day to Outlook.com, Hotmail.com and Live.com addresses.
- **Required:** SPF pass, DKIM signing, DMARC record with at least `p=none`, aligned with SPF or DKIM (ideally both).
- **Non-compliant mail:** first routed to Junk, later blocked. The rejection error is `550; 5.7.515 Access denied, sending domain [SendingDomain] does not meet the required authentication level.`
- **Recommended:** real From/Reply-To that can receive replies; a visible, working unsubscribe link for bulk/marketing; clean lists and bounce monitoring; honest subjects and headers.
- **Not required by Microsoft:** RFC 8058 one-click unsubscribe and the List-Unsubscribe header (unlike Gmail and Yahoo).

### 1.4 Google Postmaster Tools v2
Source: [Suped: Ultimate guide to Google Postmaster Tools v2](https://www.suped.com/blog/ultimate-guide-to-google-postmaster-tools-v2) (article updated 25 Jun 2026). Confidence: Medium.

- **Compliance status dashboard:** each requirement shows Compliant, Needs work, or No data found.
  - All senders: basic SPF or DKIM, DNS records, message formatting, encryption, user-reported spam rate.
  - Bulk senders also: SPF and DKIM together, DMARC policy and alignment, one-click unsubscribe, unsubscribes honoured.
- Status rolls up to the primary domain. A DNS fix can take up to 7 days to clear "Needs work".
- **Spam rate** = user spam reports ÷ eligible DKIM-authenticated inbox deliveries × 100, calculated daily. Target under 0.1%; 0.3%+ is the danger line.
- **Legacy v1:** IP/domain reputation views are being deprecated; availability varies by account during the transition. Treat them as context only.
- **Minimum volume to see data** (planning guidance, not an official figure), per day to personal Gmail accounts:
  - Under 100: usually blank
  - 100–299: patchy
  - 300–999: more days populate, reputation still sparse
  - 1,000+: more reliable
  - ~5,000+: bulk sender rules apply
- **Implication for us:** at ~100/day spread across inboxes, Postmaster Tools will likely show nothing useful. We need other signals (bounces, reply trends, seed tests, DMARC reports).

### 1.5 Google Workspace sending limits
Source: [LeadHaste: Google Workspace cold email limits 2026](https://leadhaste.com/blog/google-workspace-cold-email-limits-2026) (vendor content). Confidence: Medium for official caps, Low for the "safe" numbers.

- **Official caps:** 2,000 emails/day per paid Workspace user; 500/day for free Gmail. Rolling 24-hour window, not a midnight reset.
- The 2,000 figure is a technical cap, not a safe cold email number.
- **Safe cold volume:** the body says 20–30/inbox/day; the FAQ says 30–50 for warmed inboxes (inconsistent).
- **New inbox ramp:** start at 5–10/day, grow over 3–4 weeks to 20–30/day.
- **Scaling:** add inboxes rather than pushing more per inbox. Suggests 2–3 inboxes per dedicated sending domain, kept separate from the primary domain.
- Exceeding the daily limit triggers a sending suspension of up to 24 hours; the bigger risk is lasting reputation damage.

### 1.6 Other general deliverability references found (not read in full)
- [Instantly: How to achieve 90%+ cold email deliverability in 2026](https://instantly.ai/blog/how-to-achieve-90-cold-email-deliverability-in-2025/) (vendor)
- [Courier: Email sender requirements](https://www.courier.com/blog/email-sender-requirements)
- [PowerDMARC: Bulk email sender requirements](https://powerdmarc.com/de/bulk-email-sender-requirements/)
- [Abmatic: Cold email deliverability 2026](https://abmatic.ai/blog/cold-email-deliverability-2026)
- [Suped: How Gmail is enforcing sender requirements](https://suped.com/email-deliverability/answers/how-is-gmail-enforcing-its-new-sender-requirements-and-what-impact-are-senders-seeing)
- [LeadHaste: Email deliverability 2026 changes](https://leadhaste.com/blog/email-deliverability-2026-changes)
- [Prospeo: Spam rate threshold](https://prospeo.io/s/spam-rate-threshold)
- [LeadHaste: Cold email sending limits 2026](https://leadhaste.com/blog/cold-email-sending-limits-2026)
- [Suped: Microsoft sender requirements and observed enforcement bounces](https://www.suped.com/learn/email-deliverability/what-are-the-new-microsoft-email-sender-requirements-and-observed-enforcement-bounces)
- [Ikarus: Microsoft enforces DMARC](https://www.ikarussecurity.com/en/security-news-en/microsoft-enforces-dmarc-new-delivery-rules-for-high-volume-outlook-emails/)
- [Egressif: Microsoft sender requirements](https://egressif.io/resources/sender-requirements/microsoft)
- [Valimail: Why Gmail is rejecting your emails](https://www.valimail.com/?p=11424)
- [Red Sift: Gmail's enforcement ramps up](https://redsift.com/blog/gmails-enforcement-ramps-up-what-bulk-senders-need-to-know)
- [Palisade: Google sender requirements stricter from Nov 2025](https://www.palisade.email/learning/google-is-making-email-sender-requirements-stricter-starting-nov-2025)
- [Folderly: Postmaster Tools v1 retiring](https://folderly.com/blog/google-postmaster-tools-v2-migration-guide-2025)
- [Blueshift: Postmaster Tools v2 compliance dashboard](https://blueshift.com/blog/google-postmaster-tools-v2/)
- [InboxAlly: Postmaster Tools update Sep 2025](https://www.inboxally.com/blog/big-industry-change-with-google-postmater-tools-update)

---

## 2. Warm-up

### 2.1 Google's stance on automated warm-up (key finding)
Sources: [GMass: Warmup shutting down](https://www.gmass.co/blog/warmup-shutting-down/) and [Growbots: Google bans cold email warmup](https://www.growbots.com/blog/google-bans-cold-email-warmup/) (published 15 May 2023, modified 16 Jan 2024). Confidence: High that it happened in 2023; **unknown whether anything changed since**.

- Google told GMass to **shut down its warm-up system or lose Gmail API access**. GMass warm-up stopped on **31 Jan 2023**. Google "made it clear they don't want warmup taking place at all" and treats it as a ToS violation.
- GMass rejected switching to IMAP, saying Google would likely detect it.
- Warmbots stopped warming Google accounts on **31 May 2023**.
- Growbots' reasoning: warm-up emails are sent without prior engagement (anti-spam policy) and third-party tools use Gmail API access in ways Google disallows.
- **Recommended alternatives:**
  - **Manual ramp:** start with your most engaged contacts, increase volume over several weeks, run a deliverability test after a couple of weeks, stay at 30–40/day or less during warm-up.
  - GMass's list: increase volume gradually starting with small targeted groups; write high-quality personalised emails; set up a custom tracking domain; embed images rather than hosting them; fix DKIM/SPF/DMARC; throttle send speed; try plain text; test before sending.
  - Use providers that hadn't banned warm-up at the time (Yahoo, Outlook, Zoho were named in 2023).
  - IMAP/SMTP-based warm-up instead of the Gmail API (risk unclear).
- **Open question:** Many 2026 tools (e.g. Instantly) still sell "unlimited warm-up". Whether Google suspends Workspace accounts for it in 2026 was not confirmed in this pass.

### 2.2 Free and cheap warm-up tools
Source: [HotHawk: Best free email warmup tools](https://hothawk.ai/compare/best-free-email-warmup-tools) (pricing "accurate as of June 2026"; HotHawk is itself a vendor). Confidence: Medium/Low.

| Tool | Free plan | Time limit | Paid entry |
|---|---|---|---|
| TrulyInbox | 1 account, 10 warm-up emails/day | Never expires | From $22/month |
| HotHawk | Not stated | 7-day trial, no card | $97/month |
| Instantly | "Unlimited" warm-up, with a paid platform plan | n/a | From $47/month |
| Warmup Inbox | Not stated | 7-day trial, no card | "$15 per inbox per year" (looks wrong; may be per month; re-check) |
| Mailivery | Not stated | 7-day trial | From $29/month |
| Warmy.io | Not stated | 7-day trial, no card | No public price (pulled in 2026) |

Also from [Prospeo: Free cold emailing software](https://prospeo.io/s/free-cold-emailing-software) (vendor):
- **Mailflow:** 5 warm-up emails/day, up to 100 inboxes, free.
- **EmailWarmup:** 10 emails/day, 1 inbox, unlimited delivery testing, free.
- **Snov.io free:** 1 warm-up mailbox at 15 emails/day (non-renewable quota).

Other warm-up pages found (not read in full): [Mailivery: best warm-up tools](https://mailivery.io/blog/best-email-warm-up-tools), [Mailivery: free warm-up tools](https://mailivery.io/blog/free-email-warmup-tools), [Mailivery: TrulyInbox reviews](https://mailivery.io/blog/trulyinbox-reviews), [Mailivery: does warm-up work](https://mailivery.io/blog/does-email-warmup-work), [Waalaxy: Email warmup 2026 guide](https://blog.waalaxy.com/en/email-warmup/), [Sender: warm-up tools](https://www.sender.net/blog/email-warm-up-tools/), [TrulyInbox: Warmbox alternatives](https://www.trulyinbox.com/blog/warmbox-alternative/), [TrulyInbox: 14 warm-up services](https://www.trulyinbox.com/blog/email-warmup-tools/), [MailReach: user suspended by Google](https://help.mailreach.co/en/article/user-suspended-by-google-the-causes-and-what-to-do-about-it-p31s5p/), [Prospeo: How to warm up your inbox 2026](https://prospeo.io/s/warm-up-inbox), [EmailBison: Google Workspace vs Microsoft 365 for cold email](https://emailbison.com/blogs/google-workspace-vs-microsoft-365).

---

## 3. Inboxes and domains

### 3.1 Google Workspace pricing
Source: [Hostraha: Google Workspace pricing 2026](https://www.hostraha.com/blog/google-workspace-pricing-2026). Confidence: Medium (matches Google's 2025 announcement).

- **Business Starter:** $7.00/user/month (annual) or $8.40/user/month (flexible/monthly). INR price not listed; Indian pricing may differ and should be checked.
- 2025 price rise of about 17–22% across plans, with Gemini AI bundled into Business and Enterprise:
  - 16 Jan 2025: new pricing for new customers
  - 17 Mar 2025: existing monthly plans repriced; annual plans update at next renewal
  - 7 Jul 2025: final pricing updates for very small businesses
- No further increases announced for 2026.

Other India pricing pages found (not read): [Netspace India](https://www.netspaceindia.com/email-solutions/google-workspace-pricing/), [Aarav Infotech](https://www.aaravinfotech.com/google-workspace), [SaaS CRM Review](https://saascrmreview.com/google-workspace-pricing/), [Cloudfy: renewal pricing India](https://cloudfysystems.com/blog/google-workspace-renewal-pricing-india), [Amyntas: pricing 2026](https://www.amyntas.in/google-workspace-pricing-2026/).

### 3.2 Zoho Mail
Source: [AI Productivity: Zoho Mail pricing 2026](https://aiproductivity.ai/pricing/zoho-mail/). Confidence: Medium (page is internally inconsistent).

- **Forever Free:** up to 5 users, 5 GB/user, one domain, **web access only (no IMAP/POP/SMTP)**, so it can't connect to a sender or n8n. (The FAQ also mentions mobile app access, which contradicts the table.)
- **Mail Lite:** about **$1/user/month annual** (≈$1.25 monthly), 5–10 GB/user, IMAP/POP access.
- Daily sending limits: not stated. Zoho's acceptable-use policy on cold outreach was **not** checked.

Other Zoho pages found: [Capterra: Zoho Mail pricing](https://www.capterra.com/p/174694/Zoho-Mail/pricing/), [Neo: Zoho review](https://www.neo.space/blog/review-of-zoho-mail-pricing-features-set-up-process), [StartupOwl: Zoho Mail](https://startupowl.com/reviews/zoho-mail).

### 3.3 Cold email inbox resellers
Sources: [Modern Inbound: Zapmail vs Inframail](https://moderninbound.com/blog/zapmail-vs-inframail) (published 22 Jul 2026, modified 11 Oct 2026) and [SendKit: Zapmail pricing](https://sendkit.ai/zapmail-pricing) (updated Mar 2026; SendKit competes with Zapmail). Confidence: Medium.

| Provider | Price | Backend | Notes |
|---|---|---|---|
| Zapmail | Starter $39/month for 10 mailboxes; Growth $99/30; Pro $299/100; extra mailbox $3.00–3.50 | Google Workspace only | Rough totals: ~$40–50 for 10, $120–150 for 30, $400–500 for 100 |
| Mailforge | ~$3/inbox/month | Google and Microsoft | Minimums not stated |
| Inframail | $99/month flat, unlimited inboxes | Microsoft 365 | Cheaper per inbox only at volume |
| Pipl.ai | From $49/month | Not stated | Bundled sending + warm-up |
| Emailguard | Varies | n/a | Deliverability monitoring, not an inbox provider |

**Implication:** every reseller's entry tier is above a $20/month total budget.

Other reseller comparisons found: [Salesforge: Zapmail alternatives](https://www.salesforge.ai/blog/zapmail-alternatives), [Modern Inbound: Mailforge alternatives](https://moderninbound.com/blog/best-mailforge-alternatives), [SendKit: Maildoso vs Infraforge](https://sendkit.ai/maildoso-vs-infraforge), [SendKit: Zapmail vs Infraforge](https://sendkit.ai/zapmail-vs-infraforge), [SendKit: Maildoso vs Zapmail](https://sendkit.ai/maildoso-vs-zapmail), [SendKit: Zapmail vs Mailforge](https://sendkit.ai/zapmail-vs-mailforge), [Prospeo: Mailreef alternatives](https://prospeo.io/s/mailreef-alternatives), [Salesforge: InboxKit alternatives](https://www.salesforge.ai/blog/inboxkit-alternatives), [GTM Directory: Zapmail vs Premium Inboxes](https://thegtmdirectory.com/compare/zapmail-vs-premium-inboxes).

### 3.4 Microsoft 365 and domains
- Microsoft 365 Business Basic ≈ $6/user/month: from general knowledge, **not verified** in this pass. Check the India price.
- `.com` ≈ $10–11/year at at-cost registrars (Cloudflare, Porkbun): from general knowledge, **not verified**. The search returned only unrelated TLD pages ([domainoffer.net](https://domainoffer.net/tld/company/cloudflare)). Check `.com`, `.in`, `.dev`, `.me`, `.co` and their renewal prices.

---

## 4. Sending and sequencing tools

### 4.1 Instantly vs Saleshandy
Source: [SendKit: Instantly vs Saleshandy](https://sendkit.ai/instantly-vs-saleshandy) (SendKit is a competitor, from $99/month). Confidence: Medium.

**Instantly:**
- Growth $47/month (5,000 emails/month, 1,000 contacts); Hypergrowth $97/month (100,000 emails/month); Light Speed (500,000+); Enterprise custom.
- Unlimited email accounts on all plans; unlimited warm-up on all Outreach plans.
- Growth Leads (separate, credit-based) $47–97/month; verification (separate) ~$30/month at typical volume.
- Prospeo says Instantly is about **$30/month on annual billing** and has **no free plan or trial**.

**Saleshandy:**
- Starter $25/month annual (~$36 monthly), 6,000 emails/month (Prospeo: 2,000 prospects); Pro $69 annual (~$99), 150,000 emails; Scale $139 (~$199), 240,000; Scale Plus $219 (~$315).
- Unlimited email accounts, but a **$4/month fee per connected Google Workspace or Microsoft 365 mailbox** (per SendKit).
- Warm-up via TrulyInbox.
- 7-day trial (per Prospeo).

### 4.2 Free tiers and cheap options
Source: [Prospeo: Free cold emailing software 2026](https://prospeo.io/s/free-cold-emailing-software) (no publish date; mentions a Jan 2026 GMass price change and a Jul 2025 Snov.io update; Prospeo is a vendor). Confidence: Medium/Low.

| Tool | Free limits | Paid entry |
|---|---|---|
| Prospeo | 75 verified emails/month + 100 extension credits/month (page also says 100 free credits) | ~$39/month data tier |
| Snov.io | 50 credits/month; 100 campaign recipients/month; follow-ups don't use extra recipients; 1 warm-up mailbox at 15/day; 1 user | $39/month Starter |
| Mailmeteor | ~50 emails/day, open tracking; no multi-step sequences, warm-up or CRM | ~$10/month |
| Apollo | 100 credits/month; 2 sequences; no warm-up | ~$49–59/user/month |
| Hunter | 1 email account; up to 500 recipients per campaign | $49/month |
| Streak | Free CRM; limits not stated | Not stated |
| GMass | 7-day trial, 50/day | $29.95/month Standard (Jan 2026) |
| Saleshandy | 7-day trial | $25/month Starter |
| Lemlist | 14-day trial | $24/month Starter (annual) |
| Instantly | No free plan or trial | $30/month annual |

### 4.3 Apollo free plan
Source: [CostBench: Apollo free plan 2026](https://www.costbench.com/software/ai-sales-tools/apollo/free-plan/) ("last verified 26 Aug 2026" vs "as of Oct 2026", unclear). Confidence: Medium/Low.
- 900 credits per seat per year, granted monthly (~75/month). (Prospeo says 100/month.)
- 2 sequences; unlimited sequences are paid. Warm-up and the deliverability suite are paid only.
- Daily sending limit and mailbox count not stated.
- Other caps: 5 AI assistant chats, 20 website-visitor identifications/month, 100 CRM enrichments/month, 150 minutes of call recording. Possible Apollo branding, restricted/watermarked exports, limited API.

Other Apollo pages found: [Zeliq](https://www.zeliq.com/blog/apolloio-pricing), [Landbase](https://www.landbase.com/blog/apollo-pricing), [MarketBetter](https://www.marketbetter.ai/blog/apollo-io-pricing-breakdown-2026/), [SendKit](https://sendkit.ai/apollo-pricing), [LeadHaste](https://leadhaste.com/blog/apolloio-pricing-2026), [SyncGTM review](https://syncgtm.com/blog/apollo-io-review), [Lakestar](https://founders.lakestar.com/apollo-io/pricing).

### 4.4 Hunter
Source: [MarketBetter: Hunter.io pricing 2026](https://marketbetter.ai/blog/hunter-io-pricing-breakdown-2026/) (published 23 Feb 2026, pricing verified against hunter.io on 13 Sep 2026, updated 1 Oct 2026). Confidence: Medium.
- **Free:** 50 credits/month shared across searches and verifications (Domain Search costs 1 credit per email returned; Email Finder and Verifier 1 each); 500 recipients per campaign sequence; 1 connected email account; unlimited view-only team members; no auto-verification, enrichment or AI writer. Follow-up limits not stated.
- **Paid (monthly / annual per month):** Starter $49/$34; Growth $149/$104; Scale $299/$209; Enterprise custom. Annual saves 30%.

Other Hunter pages found: [Hunter cold email software](https://hunter.io/cold-email-software?budget=3), [SyncGTM review](https://www.syncgtm.com/blog/hunter-io-review), [Emailchaser review](https://www.emailchaser.com/learn/hunter-io-review), [Software Advice](https://www.softwareadvice.com/email-marketing/hunter-profile).

### 4.5 Snov.io (pages found, not read in full)
[Woodpecker: Snov.io pricing](https://woodpecker.co/blog/snovio-pricing/), [Saleshandy: Snov.io pricing 2026](https://www.saleshandy.com/blog/snovio-pricing/), [Snov.io KB: Trial vs Premium](https://snov.io/knowledgebase/?p=38550), [Snov.io KB: warm-up slots and limits](https://snov.io/knowledgebase/warm-up-slots-and-warm-up-volume-limits/), [Snov.io KB: pricing plans overview](https://snov.io/knowledgebase/pricing-plans-overview/).

### 4.6 Other sequencer comparisons found
[HotHawk: Saleshandy alternatives](https://hothawk.ai/compare/saleshandy-alternatives), [SalesRobot: Smartlead alternatives](https://www.salesrobot.co/blogs/smartlead-alternatives), [Rework: Smartlead alternatives 2026](https://resources.rework.com/tools/sales-engagement/best-smartlead-alternatives), [Instantly: Saleshandy alternatives](https://instantly.ai/blog/saleshandy-alternatives-2025-budget-friendly-cold-email-tools-for-scaling-agencies/), [Cut the SaaS: Instantly alternatives](https://cut-the-saas.com/alternatives/instantly), [TrulyInbox: Smartlead alternatives](https://www.trulyinbox.com/blog/smartlead-alternatives/), [GTM Directory: Instantly vs Saleshandy](https://thegtmdirectory.com/compare/instantly-vs-saleshandy).

---

## 5. LinkedIn context and enrichment

### 5.1 What happened to Proxycurl
Source: [Linked API: Proxycurl alternatives](https://linkedapi.io/guides/proxycurl-alternatives) (Linked API sells an alternative). Confidence: High on the events (widely reported).

- **24 Jan 2025:** LinkedIn sued Nubela, the company behind Proxycurl (*LinkedIn Corp. v. Nubela Pte. Ltd.*, N.D. Cal., No. 3:25-cv-00828), with six claims including breach of contract, CFAA, California UCL, Lanham Act and misappropriation.
- **Core allegation:** fake accounts used to scrape millions of profiles, including non-public data, resold via API.
- **Mid-2025:** settled. Proxycurl announced its wind-down in **July 2025**; customer data was to be deleted.
- The founder said about half of the ~$10M business came from scraping LinkedIn and there was "no winning in fighting this".
- Proxycurl's old pricing: $49/month (2,500 credits) up to $1,899/month (211,000 credits).

### 5.2 LinkedIn data alternatives and their risks

| Provider | Approach | Price (category range) |
|---|---|---|
| ScrapIn, Apify, Bright Data, Scrapingdog | Real-time scraping via proxies | ~$1.50–4 per 1K profiles |
| Coresignal, People Data Labs | Pre-scraped datasets | ~$0.005–0.20 per record |
| Crustdata | Indexes public web pages | Not published |
| Linked API | Uses your own logged-in account | $49/seat/month, annual |
| Unipile | Account-based | Flat per connected account (not stated) |
| Reverse Contact, Prospeo | Consented contact enrichment | Not stated |

Risks noted:
- Scraping public data isn't automatically illegal in the US (*hiQ v. LinkedIn*), but it still falls under LinkedIn's terms, and under GDPR/CCPA for personal data.
- Fake accounts and non-public data are what turned Proxycurl into a lawsuit (CFAA and privacy exposure).
- Dataset providers built on a central scraped index can be ordered to delete data at short notice.
- Account-based tools move the risk onto **your own LinkedIn account**, and throughput is limited by daily limits.
- Advice: get contact details from consented B2B enrichment providers, not by extracting them from LinkedIn.

Other Proxycurl pages found: [Bright Data](https://brightdata.com/blog/web-data/proxycurl-alternatives.md), [Nubela founder post](https://nubela.co/blog/what-is-proxycurl-api-now-in-2026-im-the-founder/), [ZoomInfo: Proxycurl API review](https://pipeline.zoominfo.com/sales/proxycurl-api), [Unipile](https://www.unipile.com/proxycurl-alternative/), [ZoomInfo: alternatives](https://pipeline.zoominfo.com/sales/proxycurl-alternatives), [API Serpent](https://apiserpent.com/blog/proxycurl-alternative-linkedin-api).

### 5.3 Apify free plan
Source: [use-apify.com: Apify free plan](https://use-apify.com/docs/what-is-apify/apify-free-plan). Confidence: Medium.
- **$5 of platform usage per billing cycle**, no card, permanent plan; unused credit doesn't roll over; runs are blocked when it runs out (no overage).
- Limits: up to 16 GB RAM per run; 5 (or 25) concurrent runs, plan for 5; 5 datacenter proxy IPs; residential proxy $8/GB.
- LinkedIn profile actors: "from $10 per 1,000 profiles", so $5 covers about 500 profiles at best. The free tier gets no Store discount, so real cost may be higher.
- Whether LinkedIn actors need cookies/login: not stated. Check each actor.

Other Apify pages found: [SocialCrawl: best LinkedIn data APIs 2026](https://www.socialcrawl.dev/blog/best-linkedin-data-apis-2026.md), [API Serpent: Apify LinkedIn pricing](https://apiserpent.com/blog/apify-linkedin-scraper-pricing-explained), [Modern Inbound: Apify vs PhantomBuster](https://moderninbound.com/blog/apify-vs-phantombuster), [use-apify: best LinkedIn scrapers](https://use-apify.com/docs/best-apify-actors/best-linkedin-scrapers), [SyncGTM: Apify review](https://syncgtm.com/blog/apify-review-2026), [Prospeo: Apify pricing](https://prospeo.io/s/apify-pricing-reviews-pros-and-cons).

### 5.4 Clay
Source: [Valley: Clay pricing and credits 2026](https://www.joinvalley.co/blog/clay-pricing-and-credits-explained-2026) (prices as of 6 Oct 2026; Valley is a competitor). Confidence: Medium.
- **Free:** 100 Data Credits + 500 Actions/month, unlimited seats, 200-row table cap.
- **Launch:** $185/month monthly or $167/month annual, 2,500 Data Credits + 15,000 Actions; price rises with more of either.
- Data Credits buy marketplace data (150+ providers); Actions pay for platform work (enrichments, tables, AI calls, exports). Data Credits roll over up to 2× monthly on Launch/Growth; Actions reset.
- **Bring your own API key:** yes; then you pay only Actions for that provider.
- **Implication:** way above $20/month; only the free tier is relevant.

Other Clay pages found: [Zeliq](https://www.zeliq.com/blog/clay-pricing), [Landbase](https://www.landbase.com/blog/clay-pricing), [Gojiberry](https://blog.gojiberry.ai/blog/clay-pricing), [Docket](https://www.docket.io/resources/research/clay-pricing), [Databar](https://databar.ai/blog/article/clay-pricing-2026), [Clay: new pricing](https://www.clay.com/blog/introducing-clays-new-pricing), [SyncGTM](https://www.syncgtm.com/blog/clay-pricing-change), [Datalane](https://www.datalane.com/post/clay-pricing).

---

## 6. AI for writing personalised emails

### 6.1 Gemini API free tier
Source: [AgentDeals: Gemini API pricing changes](https://agentdeals.dev/gemini-api-pricing-changes) (third-party aggregator with inconsistent dating; covers events up to Oct 2026). Confidence: Low/Medium.
- Free tier covers Gemini 3.x Flash and Flash-Lite models (3.8 Flash, 3.6 Flash, 3.5 Flash-Lite, 3.1 Flash-Lite), plus Gemini Embedding 2, Gemma 4 and some Live/Transcribe/TTS models. 3.1 Pro Preview and Omni Flash are paid only. No free image models. Search grounding isn't free for 3.x.
- Free-tier rate limits aren't published; they're shown per project in AI Studio. On 6 Dec 2025, 2.5 Flash dropped to ~5 requests/minute and 20/day; 2.5 Pro to zero.
- **Data use (key finding):** Google's pricing page says *"free-tier content is used to improve Google's products"*. Outside the EEA/Switzerland/UK, human reviewers may read free-tier prompts; Google advises not sending sensitive or personal information. Apps serving EEA/UK/Swiss users may use only the paid tier.
- **Implication:** prompts that contain hiring managers' LinkedIn details are third-party personal data. Don't send them to a free tier that trains on inputs.
- Paid spend caps from 1 Apr 2026: Tier 1 $250/month, Tier 2 $2,000, Tier 3 $20,000–100,000+.
- Other dates: 2 Mar 2026 (no $300 Cloud credit for new accounts on the Gemini API); 1 Jun 2026 (Gemini 2.0 Flash shut down); 18 Sep 2026 (2.5 models limited to prior users); 8 Oct 2026 (3.7 and 3.5 Flash deprecated); ~12 Oct 2026 (Postpay → Prepay cutover); **1 Jan 2027: Flash prices double** ($0.75/$3.75 → $1.50/$7.50 per million tokens for 3.8 and 3.6 Flash).

Other Gemini pages found: [AgentDeals: Gemini API pricing 2026](https://agentdeals.dev/gemini-api-pricing-2026), [TinkerLLM](https://tinkerllm.com/blog/gemini-api-free-tier-limits-rate-quotas/), [Yingtu: free tier limits 2026](https://yingtu.ai/en/blog/google-gemini-api-free-tier-limits-2026), [Yingtu: free tier guide](https://yingtu.ai/en/blog/google-gemini-api-free-tier), [Laozhang: free tier](https://blog.laozhang.ai/en/posts/gemini-api-free-tier), [Laozhang: pricing](https://blog.laozhang.ai/en/posts/gemini-api-pricing.md), [RapidDevelopers](https://www.rapidevelopers.com/md/ai-api-limits-performance-matrix/gemini-1-5-flash).

### 6.2 Not researched yet
Claude, OpenAI, Groq/open models and local models: cost per 1,000 emails and data-use terms. Left to Part 1 of the self-prompt.

---

## 7. Benchmarks

### 7.1 Instantly 2026 cold email benchmark
Source: [Instantly: Cold email benchmark report 2026](https://instantly.ai/cold-email-benchmark-report-2026) (data 1 Jan–18 Dec 2025; Instantly is a vendor). Confidence: Medium. These are **sales** numbers, not job-seeker numbers.
- **Average reply rate:** 3.43%. Top quartile: 5.5%+. Top 10%: 10.7%+ (2–4× average).
- **58% of replies come from the first email**, 42% from follow-ups.
- **4–7 touchpoints** optimal; fewer than 4 gives up too early; more than 7 has diminishing returns unless each adds value.
- **Days:** Tuesday and Wednesday peak (Wednesday highest); Monday best to launch; Friday brings more auto-replies.
- **Length:** top performers average under **80 words** per first email.
- Step-2 emails framed like replies beat formal follow-ups by ~30%. Stable domain health and consistent sending: 15–20% more replies. Keep bounces under 2%.
- Personalisation impact: not quantified (micro-segmentation and problem-focused messaging named as contributors).

Other benchmark pages found: [Instantly: AI sales agent benchmarks 2026](https://instantly.ai/blog/ai-sales-agent-benchmarks-2026-the-complete-performance-report/), [Lemlist: Cold email benchmarks](https://lemlist.com/blog/cold-email-benchmarks/), [Unify: how many follow-ups](https://www.unifygtm.com/explore/how-many-follow-ups-cold-email), [ColorWhistle: cold email statistics](https://colorwhistle.com/?p=109464), [Something Inc: first email wins most replies](https://somethinginc.com/blog/first-email-wins-most-replies/), [Something Inc: positive reply rate](https://somethinginc.com/blog/positive-reply-rate-cold-email/), [LeadHaste: outbound sales benchmarks 2026](https://www.leadhaste.com/blog/outbound-sales-benchmarks-2026).

### 7.2 Job-seeker / recruiting outreach (pages found, not read)
These are mostly recruiter → candidate data, which is close but not the same as candidate → hiring manager:
[Pin: recruiting outreach benchmarks 2026](https://www.pin.com/blog/recruiting-outreach-benchmark-report/), [Pin: recruiting email templates](https://www.pin.com/blog/recruiting-email-templates/), [Noon: candidate reply rate by seniority](https://www.noon.ai/blog/articles/335-candidate-reply-rate-by-seniority), [Noon: recruiting subject line statistics](https://www.noon.ai/blog/articles/337-recruiting-email-subject-line-statistics), [Noon: recruiter cold email response rate 2026](https://www.noon.ai/blog/articles/332-recruiter-cold-email-response-rate-2026), [Noon: email length vs reply rate](https://www.noon.ai/blog/articles/338-recruiting-email-length-reply-rate), [Jobrise: cold email to a recruiter](https://jobrise.io/en/blog/how-to-write-cold-email-recruiter/), [Prospeo: cold recruiting email templates](https://prospeo.io/s/cold-recruiting-email-template).

---

## 8. Law and compliance

### 8.1 India DPDP Act and Rules
Source: [AZB & Partners: DPDP phased rollout](https://www.azbpartners.com/bank/indias-digital-personal-data-protection-act-phased-rollout-and-key-compliance-milestones/) (14 Nov 2025; law firm). Confidence: High.
- Notifications dated **13 Nov 2025**: staggered start of the DPDP Act, the DPDP Rules, and the Data Protection Board.
- **Immediate (13 Nov 2025):** Act sections 1(2), 2, 18–26, 35, 38–43, 44(1) & (3); Rules 1, 2, 17–21 (definitions, Board, rulemaking).
- **After 1 year (~12 Nov 2026):** Section 6(9) and 27(1)(d) (consent managers); Rule 4.
- **After 18 months (~12–13 May 2027):** everything else, including the core **notice and consent** duties (Sections 3–5, 6(1)–(8) and (10), 7–17; Rules 3, 5–16, 22, 23).
- The article doesn't cover the personal-purpose exemption. From the Act itself (general knowledge, to be confirmed): the Act doesn't apply to personal data processed by an individual for a personal or domestic purpose. Open question: does one job seeker's own outreach qualify, and does a system run for many job seekers?

Other DPDP pages found: [Deccan Herald](https://www.deccanherald.com/amp/story/india%2Fcentre-notifies-dpdp-rules-implementation-planned-in-phases-spread-over-12-18-months-3798465), [Outlook Business](https://www.outlookbusiness.com/deeptech/tech/govt-notifies-dpdp-rules-experts-flag-need-for-data-mapping-consent-systems), [PIB official document](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf), [AZB: framework comes into effect](https://www.azbpartners.com/bank/update-indias-digital-personal-data-protection-framework-comes-into-effect/), [Anantam IAS](https://anantamias.com/current-affairs/dpdp-rules-data-protection-framework-2025/?pdf=1).

### 8.2 Not researched yet
CAN-SPAM (is job-seeking email "commercial"?), GDPR legitimate interest, UK PECR, Canada CASL, Australia Spam Act, UAE rules, India IT Act. Left to Part 1 of the self-prompt.

---

## 9. What this means for a $20/month, 100/day job-seeker setup (my working conclusions)

These are hypotheses from the findings above, not verified recommendations. Part 1 of the self-prompt tests each one (H1–H7).

1. **Volume maths:** at 20–30 sends per inbox per day after ramp-up, 100/day needs about **4–5 inboxes**. With a 3-touch sequence, only about a third of daily sends are new first touches (~33 new people/day).
2. **Budget pressure:** every paid sequencer ($24–47/month) and every inbox reseller ($39+/month) alone breaks the $20 budget. Building the sender in the existing n8n costs $0, so that's likely the right call.
3. **Inbox cost is the main lever:** Google Workspace at $7–8.40/inbox makes 4–5 inboxes cost $28–42. Zoho Mail Lite (~$1/inbox, IMAP/SMTP) or Microsoft 365 (~$6) fit better, but their deliverability and cold-outreach policies need checking. India pricing for Workspace may also be lower.
4. **Warm-up:** Google treated automated warm-up as a ToS violation in 2023. A slow manual ramp (5–10/day rising over 3–4 weeks) is the safer default, especially on Google.
5. **Monitoring:** Postmaster Tools will likely be blank at our volume, so rely on bounce rate, reply trends, seed-inbox tests, mail-tester and DMARC reports.
6. **LinkedIn context:** after Proxycurl, the lowest-risk method is the job seeker capturing profile details by hand in their own browser. Automated scrapers and account-based tools add ToS and account risk.
7. **AI:** don't put prospects' personal data into free LLM tiers that train on inputs. A cheap paid model is the safer choice; cost per email still needs measuring.
8. **Writing:** short (under ~80–100 words), plain text, one clear ask, follow-ups sent as replies in the same thread. Job seekers probably need fewer touches (around 3) than sales (4–7). Still to be confirmed.
9. **Law:** India's DPDP consent/notice duties start around May 2027. Other countries' rules for job-seeking email still need research.
