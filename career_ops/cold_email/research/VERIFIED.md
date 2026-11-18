# Cold Email: Verified Research

Checked on 2026-10-24. This file re-checks the preliminary pack (14 Oct 2026).
Method: owner skill `web-research`. Official pages first. One request at a time. No logins, no sign-ups.
Tiers: A primary, B big data from a seller, C blog or vendor, S own data, P first-hand person, K book.
Confidence is 0 to 1. Under 0.7 means: test first, do not decide on it alone.
"Gain" means who profits if you believe the source.

Pages that blocked or failed (not retried): crtc.gc.ca (403), meity.gov.in (403), indiacode.nic.in (403). Some pages timed out (acma.gov.au, microsoft.com/en-in). The Microsoft Tech Community post and the Zoho price page load their text by script, so my fetch tool saw only the title. Where that hurt, the row says so.

---

## Q1. Google and warm-up networks. Safe manual ramp.

| Claim | Evidence | Tier | Conf. | Date | Source | What it changes for the build |
|---|---|---|---|---|---|---|
| Google has no written rule that names "warm-up networks". | The Workspace acceptable-use page bans large-scale unwanted email, evading filters, tampering with the service, and interfering with other users. Breaking it may lead to suspension or cancellation. It does not say "warm-up". A warm-up network (fake opens and replies between member inboxes) fits "evading filters" and "tampering" by a fair reading. | A (rule exists). Not proof of how Google acts. Gain: Google protects its inbox product. | 0.75 that the rule can be used against it. 0.5 that Google acts on it for a small sender. | 2026-10-24 | https://workspace.google.com/terms/use_policy/ | No warm-up network on any Google account. Keeps the CLAUDE.md rule. |
| In Jan 2023 Google told GMass to stop warm-up or lose Gmail API access. | GMass says so in its own words. No Google policy section is named. Page has no update after 2023 (page footer shows 2026, no news on this). | P-like vendor (first-hand, but GMass sells mail tools; tool sellers gain by blaming Google). | 0.7 that it happened. 0.4 that it is a written ToS rule. | 2023-02-06 | https://www.gmass.co/blog/warmup-shutting-down/ | Treat as risk, not proof. |
| Warm-up apps still sit in Google's own Marketplace in 2026. | WarmInbox lists "automated email warmup" using "a network of other inboxes". Last updated 2025-11-04. Developer Offpista LTD. Listing is not an endorsement. | A for "it is listed". Gain: developer sells it. | 0.9 that it is listed. | 2025-11-04 | https://workspace.google.com/marketplace/app/warminbox_email_warmup_for_gmail_deliver/900209538863 | Google may not ban it hard. But a Marketplace listing does not protect your account. Still no network. |
| I found no 2026 report of an account suspended only for using a warm-up network. | Searches gave vendor blogs only (MailReach, Suped). They list volume spikes, low engagement and high bounces as suspension causes. | C | 0.4 | 2026-10-24 | https://help.mailreach.co/en/article/user-suspended-by-google-the-causes-and-what-to-do-about-it-p31s5p/ | Open gap. Test on a burner (experiment E1) if you ever want a network. |
| Hard caps on Workspace: 2,000 sent per day per user (1,500 by mail merge, 500 on trial), 3,000 external recipients per day, 500 external recipients per message. | Google help page text, as quoted by search result. Not opened in full. | A | 0.85 | 2026-10-24 | https://knowledge.workspace.google.com/admin/gmail/gmail-sending-limits-in-google-workspace | Caps are far above our 40 to 100 a day. Cap is not the risk. Reputation is. |
| Safe manual ramp: start 5 to 10 a day, add about 5 every few days, reach 30 to 40 by week 4. Stay plain text, personal, one ask. | Only vendor advice (LeadHaste, GMass, MailReach). Google gives no ramp. | C | 0.45 | 2026-10 | https://leadhaste.com/blog/google-workspace-cold-email-limits-2026 | Use as the starting rule, then verify with seed inboxes (E2). Do not call it proven. |

---

## Q2. Mailbox prices and limits

| Claim | Evidence | Tier | Conf. | Date | Source | What it changes |
|---|---|---|---|---|---|---|
| Zoho Mail Lite is about USD 1 per user per month, billed yearly. | Capterra 2026 and a Zoho PDF (old, promo ended Nov 2023) agree on USD 1 for Lite and USD 4 for Premium. Zoho's own live price page fills prices by script, so I could not read it. | C/B. Gain: Capterra earns from listing leads. | 0.65 | 2026-10 | https://www.capterra.com/p/174694/Zoho-Mail/pricing/ ; https://www.zoho.com/mail/images/mail-pricing-usd.pdf | Cost is tiny either way. Read Zoho's page in a browser before paying. |
| Zoho Mail Lite in India: INR 59 per user per month (5 GB), INR 75 (10 GB) on yearly billing, plus 18% GST. Premium INR 199. No monthly billing. | One Zoho partner (Cloudfy) dated 2026-05-24. Other partners say INR 90, INR 99, or INR 480 a year. They disagree. | C. Gain: resellers sell it. | 0.5 | 2026-05-24 | https://cloudfysystems.com/blog/zoho-mail-pricing-plans-india-2025 | Plan for about INR 60 to 100 plus GST per inbox. Confirm in the cart. |
| Zoho external sending limit is 50 to 500 emails per hour, set by reputation. 150 external recipients per message (paid). No fixed daily cap. | Zoho's own limits page. | A | 0.85 | 2026-10-24 | https://www.zoho.com/mail/help/adminconsole/rates-and-limits.html | New account may sit near 50 an hour. That is fine for 40 a day. |
| Zoho says "bulk or burst sending: not supported, not permitted under business usage policy". It tells bulk senders to use Zoho Campaigns. It says to raise volume slowly. | Same page. The separate anti-spam policy page returned 404, so I did not read Zoho's exact rule on cold email. A forum thread suggests the policy is strict on mail without prior permission. | A (limits page). Forum is C. | 0.7 that one-to-one low volume is tolerated. 0.4 that Zoho allows cold mail by policy text. | 2026-10-24 | same; https://help.zoho.com/portal/de/community/topic/cold-emails-not-allowed | Real risk. Zoho can suspend. Do not put the main identity on Zoho. Test (E3). |
| Zoho IMAP/SMTP on Lite is unclear. Free plan has no IMAP/POP. | Cloudfy page says Lite has IMAP/POP/ActiveSync. A Zoho community thread says a Lite admin could not find the IMAP toggle; no staff answer. | C | 0.5 | 2026-10 | https://help.zoho.com/portal/en/community/topic/cannot-find-imap-smtp-enable-toggle-in-new-mail-admin-ui-mail-lite-plan | Confirm IMAP and SMTP work on a Lite trial before choosing Zoho. Stop point for n8n. |
| Microsoft 365 Business Basic India: about INR 145 per user per month, yearly term (resellers range INR 116 to 174). Not read on Microsoft's own page (timed out twice). | Many resellers. Most common figure INR 145, GST extra. | C | 0.5 | 2026-10 | https://cloudfysystems.com/blog/microsoft-365-business-basic-india | Open gap. Costs about 2x Zoho. |
| Google Workspace Business Starter India: INR 270 per user per month, shown for both flexible and annual views. Page does not say if GST is added. | Google's India price page, read today. | A (Google sells it). | 0.7 | 2026-10-24 | https://workspace.google.com/intl/en_in/pricing.html | Pack said USD 7 to 8.40. India is about USD 3.2. Two Google inboxes cost about INR 540 a month. |

---

## Q3. Domains

Porkbun prices come from Porkbun's own public price API (Tier A, today). Cloudflare prices come from a third-party list that tracks Cloudflare (NameBeta site, updated 2026-10-21; Tier C/B, confidence 0.7). Cloudflare's own page says prices are at cost, not marked up, and lists no per-TLD numbers.

| TLD | Porkbun year 1 | Porkbun renewal | Cloudflare year 1 | Cloudflare renewal |
|---|---|---|---|---|
| .com | USD 11.08 | 11.08 | 10.46 | 10.46 |
| .in | USD 7.83 | 7.83 | not listed (likely unsupported) | - |
| .co | USD 15.76 | 31.20 | 30.00 | 30.00 |
| .me | USD 17.27 | 17.27 | 16.56 | 16.56 |
| .dev | USD 8.75 | 12.87 | 8.20 | 12.20 |

| Claim | Evidence | Tier | Conf. | Date | Source | What it changes |
|---|---|---|---|---|---|---|
| Porkbun prices above. | Porkbun pricing API, no login. | A | 0.9 | 2026-10-24 | https://api.porkbun.com/api/json/v3/pricing/get | .com or .dev are the cheap choices. .co renewal doubles. |
| Cloudflare prices above; .in not offered. | NameBeta list. Cloudflare says it supports 430+ TLDs and names .com .net .org .ai .app .dev. The Cloudflare supported-TLD doc URL gave 404. | C | 0.65 (.in unsupported: 0.6) | 2026-10-21 | https://cfdomainpricing.com/ ; https://www.cloudflare.com/products/registrar/ | .com at Cloudflare is the lowest and has no markup. |
| WHOIS privacy: free at Cloudflare (redaction). Free at Porkbun except .in (and .uk, .de, .us, .ca, .au and more). | Both vendors' own pages. | A | 0.85 | 2026-10-24 | https://www.cloudflare.com/products/registrar/ ; https://porkbun.com/products/whois_privacy | Do not buy .in for a sender domain. Your name and address would show in WHOIS. |
| No rule bans cold mail from a fresh domain. A new domain has zero reputation, not a blacklist mark. No domain-age threshold is published. | Deliverability vendors say so. Google and Microsoft pages list no age rule. One vendor (Spamhaus page) says many filters flag domains for about 30 days; one claim only. | C (practitioner view). Gain: they sell warm-up. | 0.55 | 2026-10-24 | https://www.suped.com/learn/email-deliverability/why-does-gmail-mark-emails-from-new-domains-as-spam | Wait 2 to 4 weeks after buying, with only SPF/DKIM/DMARC set and a few real mails, before the first cold send. Test (E2). |
| Cold mail to strangers from a brand new domain is the weakest start. | Same vendor view: new domain plus unknown people plus low replies. | C | 0.5 | 2026-10 | same | Prefer a domain aged first. Or send first to people who may know you. |

---

## Q4. Sender rules at low volume (under 100 a day)

| Claim | Evidence | Tier | Conf. | Date | Source | What it changes |
|---|---|---|---|---|---|---|
| Google: every sender to Gmail needs SPF or DKIM, valid PTR, TLS, RFC 5322 format, and spam rate below 0.3%. Keep it below 0.10%. | Google page text. Rules took effect 2024-02-01. Google gains from clean inboxes. | A | 0.95 | 2026-10-24 | https://support.google.com/a/answer/81126 | Set SPF and DKIM both anyway. Cheap. |
| Google: SPF, DKIM, DMARC (p=none is enough), aligned From, one-click unsubscribe and visible link apply to bulk senders: more than 5,000 a day. Not to us. | Same page. | A | 0.95 | 2026-10-24 | same | Strict one-click is not required at 100 a day. |
| Unsubscribe header (if used): `List-Unsubscribe: <https URL>` and `List-Unsubscribe-Post: List-Unsubscribe=One-Click`. | Same page. | A | 0.95 | 2026-10-24 | same | Optional for us. For a one-to-one job email, a plain-text opt-out line is the better fit. |
| Gmail "ramps up enforcement" since Nov 2025: temporary (4xx) and permanent (5xx) rejections. Unauthenticated mail may bounce with `5.7.26`. | Google FAQ line quoted by an independent expert (Spam Resource); Google page confirms 5.7.26 text. | A/C | 0.85 | 2025-11-03 | https://www.spamresource.com/2025/11/google-warns-sender-requirements.html | SPF/DKIM/DMARC must pass from day one. |
| Yahoo: all senders need SPF or DKIM, spam rate below 0.3%, valid DNS. Bulk senders need both, DMARC at least p=none, one-click unsubscribe, honour within 2 days. Yahoo gives no number for "bulk". No low-volume carve-out. Yahoo "strongly urges" DMARC for everyone. | Yahoo sender page. | A | 0.9 | 2026-10-24 | https://senders.yahooinc.com/best-practices/ | Publish DMARC p=none with an `rua` address. |
| Microsoft (Outlook.com, Hotmail, Live): rules for senders above 5,000 a day. SPF, DKIM, DMARC. Enforcement began 2025-05-05: Junk first, later rejection `550 5.7.515`. | Petri (secondary) quoting Microsoft; a search summary of Microsoft's post says Outlook later moved to reject. I could not read Microsoft's own post. | C (secondary of A) | 0.75 | 2025-04-07 | https://petri.com/microsoft-outlook-email-authentication-rules/ | Same DNS set works for all three. |
| Microsoft does not require one-click unsubscribe (pack claim). | From a Mailgun summary. Not confirmed in Microsoft's text. | C | 0.5 | 2025 | https://www.mailgun.com/blog/deliverability/microsoft-sender-requirements/ | Not needed at our volume either way. |
| Postmaster Tools is usually blank under 100 a day to Gmail. | Suped planning note, not an official number. | C | 0.5 | 2026-06-25 | https://www.suped.com/blog/ultimate-guide-to-google-postmaster-tools-v2 | Do not rely on it. Use seed inboxes and bounces. |

---

## Q5. Law: one person, one-to-one cold email to business addresses

Not legal advice. The key unknown: is a job application a "commercial" message? Most laws define "commercial" by selling or promoting goods or services. A job seeker offering their own labour is a grey area. No source I found rules on it.

| Place | What the law says | Tier | Conf. | Source | What it requires if it applies | What it changes |
|---|---|---|---|---|---|---|
| US CAN-SPAM | "Commercial" means primary purpose is "commercial advertisement or promotion of a commercial product or service". No B2B exception. Penalty up to USD 53,088 per email. FTC does not name job-seeking mail. My reading: a personal job inquiry is probably not "commercial". | A for text. The job-seeking reading is my inference. | 0.8 text. 0.6 reading. | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business | True sender and headers, honest subject, postal address, working opt-out honoured in 10 business days. | Cheap to follow anyway: honest subject, real name, a PO box or address line, opt-out line. |
| EU GDPR | Recital 47: direct marketing "may be regarded as carried out for a legitimate interest". Art. 21(2)-(3): the person can object at any time and processing must stop. Art. 14: when data is not from the person, tell them who you are and why, at the latest at the first message (one month max). Art. 14(5) exempts if disproportionate effort. Whether a private person's job search is "household" (outside GDPR) is unclear. | A | 0.8 text. 0.4 on the household question. | https://gdpr-info.eu/recitals/no-47/ ; https://gdpr-info.eu/art-21-gdpr/ ; https://gdpr-info.eu/art-14-gdpr/ (gdpr-info.eu is run by a consultancy, Tier C mirror of A text) | Who you are, source of the address, purpose, how to stop. Delete on request. | Put a two-line "why you got this, how to stop" in each first email to EU contacts. Keep a suppression list. |
| EU ePrivacy and Germany | ePrivacy Art. 13 lets states protect companies too. Germany: UWG section 7 says email ads need prior consent, B2C or B2B (law-firm and vendor sources; I did not read the statute). | C | 0.6 | https://www.it-recht-kanzlei.de/werbung-email-social-media-telefon-fax-was-ist-erlaubt.html | Prior consent for advertising mail. | Skip Germany, Austria and similar strict states for cold mail until a lawyer or test says okay. |
| UK PECR | Companies, LLPs and government bodies: you can email any "corporate body" without consent. Sole traders and some partnerships count as individuals and need consent. Do not hide identity. Give a valid contact address to opt out. Keep a do-not-email list. ICO says the guide is under review (Data (Use and Access) Act). PECR covers marketing; ICO page says nothing on job applications. | A | 0.85 | https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/ | Identity, contact address, opt-out, suppression list. UK GDPR still applies to a named employee's work email. | Prefer addresses at limited companies. Avoid sole traders. |
| Canada CASL | A "commercial electronic message" has as one purpose to encourage commercial activity: offer or advertise goods, services, a business opportunity, or "promote a person's public image" as one who does so (Act s.1(2)). Implied consent if the address is conspicuously published, no "no unsolicited mail" notice, and the message fits the person's role (s.10(9)(b)). Unsubscribe: free, valid 60 days, honoured within 10 business days (s.11). Fines are large. Identification text (s.6(2)) not read. I was blocked by the CRTC site (403) and stopped. | A | 0.75 text. 0.4 on whether a job inquiry is "commercial". | https://laws-lois.justice.gc.ca/eng/acts/E-1.6/page-2.html | Name, mailing address, contact, working unsubscribe. | Highest fines of the group. Cold mail to Canada only with the full footer and only to published role addresses. |
| Australia Spam Act 2003 | Table of contents only read. From memory: three rules, consent (inferred from a published work address), identify, unsubscribe. Not verified today (ACMA timed out). | A (not read) | 0.4 | https://www.legislation.gov.au/C2004A01214/latest/text | Unconfirmed. | Open gap. Add the same footer as for Canada. |
| UAE | Federal Decree-Law 45/2021 (PDPL) needs consent for processing; right to object to direct marketing. TDRA spam rules (2010) aim at telecom providers and SMS. Free zones DIFC and ADGM have own rules. No source confirmed rules for one-to-one email. Executive regulations status unclear. | C | 0.4 | https://www.mondaq.com/compliance/1229090/compliance-%7c%7c-communications-with-customers | Unclear. | Open gap. Lawyer check before volume to UAE. |
| India | No stand-alone email spam law. IT Act has no anti-spam section (sources say remedies are for fraud and impersonation, sections 66C/66D, 43, 72). TRAI rules cover calls and SMS, not email. DPDP Act: staggered start. Rules and Board started 2025-11-13. Consent managers about 2026-11-12. Notice and consent duties about 2027-05-12/13. Personal or domestic purpose exemption exists in the Act (not read today; the Act site returned 403). | A (dates, law firm AZB) / C (no-spam-law claim) | 0.85 dates. 0.6 no spam law. 0.5 on exemption. | https://www.azbpartners.com/bank/indias-digital-personal-data-protection-act-phased-rollout-and-key-compliance-milestones/ ; https://advocategandhi.com/spam-emails-legal-challenges-cybersecurity-risks-and-regulatory-frameworks/ | From May 2027: notice and consent for personal data processing. | You have about 6 months. If more job seekers use the tool, the personal-use exemption may not fit. Build a "why you got this" notice and delete-on-request now. |

---

## Q6. Cost per 1,000 personalised emails and data terms

Assumption (mine, not measured): each email uses 1,500 input tokens (prompt, profile facts, template) and 250 output tokens. 1,000 emails = 1.5M input + 0.25M output tokens. Measure it in E5.

| Option | Cost per 1,000 emails | Data terms | Tier | Conf. | Source | What it changes |
|---|---|---|---|---|---|---|
| Local model (Ollama, 1B to 4B) | USD 0 marginal. Power cost not measured. | Stays on your Mac. | S (when measured) | 0.9 on privacy. Quality unmeasured. | n/a | Default for extraction and drafting, per owner doctrine. Quality needs the eval first. |
| Claude Haiku 5.5 (prompts up to 100k) | 1.5M x 0.10 + 0.25M x 0.50 = **USD 0.275**. Batch API half: about USD 0.14. Cache reads USD 0.01 per M. | Anthropic does not train on commercial API inputs or outputs by default (article dated 2026-08-18). | A (prices, terms). Gain: Anthropic sells tokens. | 0.9 | https://platform.claude.com/docs/en/about-claude/pricing ; https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training | The paid fallback costs about 3 cents per 100 emails. Budget is not the problem. |
| Claude Haiku 4.5 | 1.5 x 1 + 0.25 x 5 = USD 2.75 | same | A | 0.9 | same pricing page | Use 5.5 instead. |
| Groq free tier | USD 0. Limits I could not read officially. Search shows llama-3.1-8b-instant at 30 requests a minute, 6,000 tokens a minute, 14,400 requests a day. A 500,000 tokens a day cap appears only on an old community page. | Groq docs: no inference data kept by default; logs up to 30 days; Zero Data Retention can be turned on by every customer. The page says nothing on training and nothing on free versus paid. | A (retention). Training: unknown. | 0.6 on limits. 0.5 on "no training". | https://console.groq.com/docs/your-data ; https://console.groq.com/docs/rate-limits | At 6,000 TPM and 1,750 tokens per email, about 3 emails a minute. 100 a day is fine. Check the training clause in the Groq DPA before sending hiring managers' names. |
| Gemini API free tier | USD 0 | Google: unpaid content is used to improve its products, and human reviewers may read it. "Do not submit sensitive, confidential, or personal information." EEA, UK, Switzerland users must use paid terms. | A | 0.95 | https://ai.google.dev/gemini-api/terms | Confirms the CLAUDE.md rule. Never send third-party personal data here. |

---

## Q7. Benchmarks for job-seeker cold email

No Tier P account with a sent count and reply count was found. Treat all numbers below as weak.

| Claim | Evidence | Tier | Conf. | Date | Source | What it changes |
|---|---|---|---|---|---|---|
| Sales cold email average reply rate 3.43%, top quartile 5.5%+. 58% of replies come from email one. 4 to 7 touches. Top emails under 80 words. | Instantly report, data Jan to Dec 2025. Instantly sells email software. These are sales numbers. | B | 0.6 for sales. 0.3 for job seekers. | 2025-12 | https://instantly.ai/cold-email-benchmark-report-2026 | Use as a floor. Not a job-seeker number. |
| Job seeker to hiring manager: a "planning range" of 5 to 15% total replies; length 50 to 125 words; one follow-up after 5 to 7 business days; a third email feels like pressure. | The article says these are its own estimates and cites no job-seeker study. PitchHired sells an outreach tool. Gain: sells tool. | C | 0.3 | 2026 | https://pitchhired.com/blog/cold-email-reply-rates-job-search-data | Design for 1 first mail and 1 to 2 follow-ups. Do not promise 5 to 15%. |
| Claims of 15 to 25% (FirstSales) or 40 to 50% (TurnAndTurn) or up to 79% (a template seller) are not backed by a shown dataset. | Vendors and course sellers. | C | 0.15 | 2026 | https://firstsales.io/blog/cold-email-sales-job | Ignore. |
| 79 public job-seeker accounts (Reddit, X): 43 reached interview or later, 25 got an offer, 15 had no progress. The study cannot give a reply rate. No denominator. Bad-experience forum over-represented. Run by DearHiringManager.io, which sells hiring-manager lookups. Only 20 accounts were explicit cold outreach. | The page states these limits itself. | C/P-like (selected accounts, no evidence shown, seller behind it) | 0.35 | 2026 | https://dearhiringmanager.io/hiring-manager-outreach-study | Shows the tactic can work. Does not show how often. |
| Recruiter to candidate cold messages: 17.6% any reply; director/VP about 33%, individual contributor 15.8%. Not candidate to manager. | Noon.ai survey, a recruiting tool vendor. | B | 0.4 | 2026 | https://www.noon.ai/blog/articles/335-candidate-reply-rate-by-seniority | Does not transfer. |
| Opposite view: Whali cites general cold email reply rate falling (3.4% in 2026) and recruiting outreach at 5.8 to 7.2%. | Vendor summary. | C | 0.3 | 2026 | https://whali.co.uk/blog/cold-email-response-rates-benchmarks | Plan for low single digits until your own data says more. |

---

## Conflicts with the preliminary pack

| Pack said | Verified finding | Action |
|---|---|---|
| "Google treats automated warm-up as a ToS violation" (from GMass and Growbots) | Google's own acceptable-use page has no warm-up clause. The claim rests on one vendor's 2023 account. A warm-up app is on Google's Marketplace, updated Nov 2025. Fits "evasion" by a fair reading; not proven. | Keep "no network on Google" as a risk choice. Mark ToS claim 0.4. |
| Workspace Starter USD 7 to 8.40 | India price page shows INR 270 per user per month (about USD 3.2). | Re-cost with INR. |
| Zoho Lite has IMAP and SMTP | Unresolved. One partner says yes. A Lite admin could not find the toggle. | Trial test before buying. |
| Zoho acceptable use "not checked" | Zoho limits page: bulk and burst sending "not permitted under business usage policy". Anti-spam policy page not readable. | Keep Zoho as a secondary mailbox. |
| Zoho daily limit "not stated" | No daily cap. 50 to 500 per hour, set by reputation. 150 external recipients per message. | Fine for 40 to 100 a day. |
| Microsoft 365 about USD 6 | India about INR 145 (resellers, 0.5). Microsoft's own page timed out. | Open gap. |
| ".com about USD 10 to 11" | Cloudflare 10.46, Porkbun 11.08. Confirmed. .co renews at 30 to 31. .in has no free WHOIS privacy at Porkbun. | Avoid .co and .in. |
| Microsoft does not require one-click unsubscribe | Only from a Mailgun summary. Microsoft text unread. | Irrelevant under 5,000 a day. |
| Postmaster data blank under 100 a day | Planning note, not official. | Keep, but mark 0.5. |
| Gemini free tier trains on inputs | Confirmed in Google's terms. | No change. Added: EEA/UK users need paid terms. |
| "3-touch sequence for job seekers; 4 to 7 for sales" | No job-seeker evidence found for any count. Practitioner advice says 1 to 3. | Plan 1 + 2 follow-ups. Test (E4). |
| Bulk threshold 5,000 | Google and Microsoft: 5,000 a day. Yahoo gives no number. | Yahoo may judge us by lower volume. Keep authentication complete. |
| Law section "not researched" | Done above for US, EU, UK, Canada, India. Australia and UAE not verified. | See open gaps. |

---

## Experiments to run on seed inboxes

Seed inboxes are your own addresses at Gmail, Outlook.com, Yahoo and one work-style domain. Never use main accounts or real targets for tests. Log each result in `docs/research/experiments.md` when that file exists.

| # | Hypothesis | Design | Decision rule |
|---|---|---|---|
| E1 | A warm-up network on a burner Google account causes a flag or suspension within 4 weeks. | One burner Workspace account on a throwaway domain. Run a free-trial warm-up network for 4 weeks. Control: a second burner, manual ramp only. Never on your real account. | If the burner is flagged or suspended and the control is not: ban networks. If neither is: still no network (the gain is small, the loss is your account). |
| E2 | A domain aged 14 days with SPF, DKIM, DMARC reaches inbox at least as often as a domain used on day 1. | Two domains bought the same day. Send plain-text test mails (5 a day, same text, same hour) from domain A on day 1 and domain B on day 15, to 6 seed inboxes (Gmail, Outlook, Yahoo, 3 others). Record inbox / spam / missing. | If B beats A by 20 points or more: wait 2 weeks before first cold mail. If equal: no wait needed. |
| E3 | Zoho Lite lets 30 outgoing mails a day from a new domain without a block, and IMAP/SMTP work with n8n. | One Zoho Lite trial. Check IMAP and SMTP login first (go/no-go). Then ramp 5 to 30 a day over 3 weeks to seed inboxes. | Any suspension, 5xx, or no IMAP: drop Zoho for sending. Use it only for receiving. |
| E4 | One follow-up gets at least 40% of the replies of the whole 3-email sequence (so a third mail is not worth it). | Run a real small campaign once approved. Send A: first mail + 1 follow-up. B: first mail + 2 follow-ups. Alternate by company. Count positive replies per arm. | If B adds under 20% more positive replies than A: stop at 1 follow-up. Needs 100 or more sends per arm to say anything; until then: pending. |
| E5 | A local 3B model writes first lines that pass a lint check as often as Haiku 5.5. | 50 contacts. Same prompt. Score on: no banned words, name correct, one fact true, under 100 words. Count pass rate and tokens used. | If local pass rate is within 10 points of Haiku: go local. Otherwise use Haiku 5.5 (about USD 0.03 per 100 emails). Also records real tokens per email to replace my 1,750 guess. |
| E6 | Groq free tier does not train on API inputs. | Read Groq's DPA / terms of service text (no login needed if public) and check Data Controls for ZDR on a free account. | If the text says no training or ZDR is available on free: allowed for contact data. If silent: dummy data only. |
| E7 | A plain-text opt-out line does not hurt reply rate. | Seed test only for placement; for replies, compare with and without the line over 100 sends later. | If reply rate drops over 30% with it: still keep it for Canada, EU, UK (law first). |
| E8 | DMARC reports show alignment passes for the n8n sender. | Publish DMARC p=none with rua. Send 10 seed mails. Read reports after 3 days. | Any fail: fix DKIM/SPF alignment before any real send. |
