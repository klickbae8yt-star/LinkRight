# Satvik Jain — Resume Bullet Bank
*Last updated: 2026-05-23 | FAANGPath A4 LaTeX | Budget: 492.39783pt | Target: 95–100% (467–492pt) | Floor: 85% (418pt)*
*Version: 2.0 — Added ST (Startup PM) and CA (Consumer/App PM) columns across all tables; Summaries Bank added; V3 (Navii) and L5 (LinkRight Validation) fact blocks added; new P2/S5/L3 variants for ST/CA; Skills blocks for FT/ST/CA; cheat sheets updated*

---

## How to Use

**When customizing a JD:**
1. Pick your target archetype column.
2. Read down the Cheat Sheet priority order for that archetype — highest-rated facts first.
3. For each bullet slot, check the bank FIRST. If a variant rated 4–5 exists → use it directly, no generation needed.
4. Only write a fresh bullet if no bank variant scores 4+ for this fact/signal.
5. After finalizing the resume, scroll to **Appended Bullets** at the bottom and add any net-new bullets written for that JD.

**When adding a new bullet to the bank:**
- Find the matching Fact block (or create a new one) and add a new variant line.
- Format: `- **[ARCHETYPE] | [JD/Company slug] | [date]** ← \`[LaTeX text]\` *([width]pt)*`
- Update the ratings table if the new variant changes the relevance picture.
- Update "Last updated" at the top of this file.
- Copy the LaTeX line directly into your `.tex` file.
- Each bullet is width-validated and single-line — drop in without re-measuring.

**Rating scale:** 5 = core signal for this archetype | 4 = strong fit | 3 = good supporting bullet | 2 = include only if space | 1 = skip

**Archetypes:** AI = AI PM | GR = Growth PM | DA = Data/Technical PM | PL = Platform PM | EN = Enterprise SaaS PM | FT = Risk/FinTech PM | ST = 0-to-1 Startup PM | CA = Consumer/App PM

---

## SUMMARIES BANK

*Drop these directly into `\section{Summary}`. Each is the exact plain text from the compiled resume. Copy as-is into the `.tex` file.*

---

### AI PM Summary
```
AI Product Manager with 4+ years building AI-powered data products in production.
Designed GenAI root-cause pipeline for Walmart (100K+ monthly contacts; 7 days $\rightarrow$ same-day insight).
Built LLM evaluation framework, fabrication guard system, and 9 self-hosted models solo for LinkRight.
Hands-on with SQL, Python, prompt engineering, and ML deployment. Not just AI feature roadmaps.
IIT Delhi.
```

---

### Growth PM Summary
```
Growth-minded PM with 4+ years turning user research into measurable adoption and revenue.
Grew Sprinklr's Social Listening adoption from $\sim$35\% to $\sim$85\% for SME clients;
secured \$1.2M TCV POC-to-close for Walmart and \$9M+ Q4 pipeline.
Prioritization grounded in data: SQL, cohort analysis, and pattern research across 1,500+ client dashboards.
Strong on funnel diagnostics and time-to-value reduction; building A/B testing depth. IIT Delhi.
```

---

### Data / Technical PM Summary
```
Data \& Technical PM with 4+ years building data pipelines, risk platforms, and self-serve analytics products in production.
Architected AmEx's 5-step CDL pipeline governing 521K+ records across AML risk categories.
Unified multi-schema SQL pipelines and deployed ML models at Sprinklr for Fortune 500 clients.
Hands-on in SQL, Python, BigQuery, and FastAPI. Not just writing specs for engineers.
IIT Delhi.
```

---

### Platform PM Summary
```
Platform PM with \textbf{4+ years} across data infrastructure, configurable risk platforms, and self-serve analytics.
Architected AmEx's 5-step CDL pipeline targeting \textbf{96.5\% AML risk coverage}; shipped \textbf{60+ features} as sole PM on CRR.
Built Use Case Hub at Sprinklr, platform's \textbf{\#1 dashboard entry point}.
Independently built production LLM stack (FastAPI, PyPI, \textbf{9 self-hosted models}). IIT Delhi.
```
*Note: Platform PM summary uses `\textbf{}` — the only archetype that does. Leave as-is.*

---

### Risk / FinTech PM Summary
```
Risk platform PM with 4+ years across AML compliance, configurable rule engines, and data infrastructure.
Architected AmEx's CDL pipeline governing 521K+ records across AML risk categories;
shipped 60+ features as sole PM on CRR risk platform; cut speed-to-market 70\%.
Hands-on in SQL, Python, rule engine design, and API-automated workflows. IIT Delhi.
```

---

### 0-to-1 Startup PM Summary
```
0-to-1 PM who ships before asking for structure. Solo founder of LinkRight: 147-response validation,
7,000+ cold-outreach, 44 of 57 features shipped, 9 self-hosted LLMs, published to PyPI.
At AmEx, sole PM on 10-sprint platform through 2 major strategy pivots with zero spillover.
Stepped into PM ownership without the title twice. IIT Delhi.
```

---

### Consumer / App PM Summary
```
Growth-minded PM with consumer product exposure across ride-hailing, career navigation, and citizen CX.
Beta Growth PM on Navii ($\sim$2K $\rightarrow$ $\sim$20K users); angel investor and advisor at GoGoGo;
built and validated linkright.in with 147-response survey + 7,000+ cold outreach.
Strong on retention metrics, cohort analysis, and activation. IIT Delhi.
```

---

## AMERICAN EXPRESS (Jul 2024 – Present)

---

### Fact A1 — CDL Pipeline Architecture
*5-step pipeline governing 521K+ industry records and 136K+ product types*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 2 | 5 | 5 | 3 | 5 | 2 | 1 |

**Variants:**
- **DA / PL / FT** ← `Architected \textbf{5-step CDL pipeline}; governs \textbf{521K+ records $\rightarrow$ 98 categories}, \textbf{136K+ types $\rightarrow$ 64 categories}` *(472pt)*

---

### Fact A2 — CDL Coverage Roadmap
*AML risk coverage driven from 85.3% to 96.5%; replaced manual Excel cross-referencing*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 2 | 2 | 5 | 5 | 3 | 5 | 2 | 1 |

**Variants:**
- **DA / PL / FT** ← `Defined CDL data coverage roadmap (\textbf{85.3\% $\rightarrow$ 96.5\% AML risk}); automated monthly manual Excel categorization` *(483pt)*

---

### Fact A3 — CRR Platform Ownership
*Sole PM for 10 consecutive sprints; 60+ features: rule engine, asset mgmt, versioning, audit trail*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 5 | 5 | 4 | 4 | 4 | 2 |

**Variants:**
- **AI** ← `Sole PM on CRR for \textbf{10 consecutive sprints}; shipped \textbf{60+ features}: rule engine, asset mgmt, versioning, audit trail` *(485pt)*
- **DA / PL** ← `Owned CRR risk platform solo for \textbf{10 sprints}; shipped \textbf{60+ features}: rule engine, asset mgmt, versioning, audit trail` *(483pt)*
- **GR** ← `Led CRR platform for \textbf{10 sprints} (sole PM); shipped \textbf{60+ features}: rule engine, asset mgmt, versioning, audit trail` *(477pt)*
- **ST** ← `Sole PM on CRR for \textbf{10 consecutive sprints}; shipped \textbf{60+ features}: rule engine, asset mgmt, versioning, audit trail` *(485pt)*

---

### Fact A4 — AML Risk-Config Speed-to-Market
*10 days → 3 days (70% reduction) via rule UI redesign and API workflow automation*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 5 | 4 | 5 | 4 | 4 | 4 | 3 |

**Variants:**
- **DA / PL / ST** ← `Cut risk-config speed-to-market \textbf{10 days $\rightarrow$ 3 days (70\%)} via rule UI redesign and API-automated approval workflows` *(490pt)*
- **GR / CA** ← `Slashed AML risk-config speed-to-market \textbf{10 days $\rightarrow$ 3 days (70\%)} via rule UI redesign and API-automated approvals` *(490pt)*

---

### Fact A5 — Leadership Award + G1L2 Rating
*Leadership in Action Award from SVP Risk; G1L2 rating; top Band 30 PO in VP's org; 120% bonus*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 |

**Variants:**
- **AI / DA / PL / GR / FT** ← `Earned \textbf{Leadership in Action Award} from SVP Risk (6 months); rated \textbf{G1L2}, top Band 30 PO in org; \textbf{120\% bonus}` *(490pt)*

---

### Fact A6 — Zero-Spillover PI Delivery
*4 consecutive zero-spillover PIs; absorbed 2 full strategy pivots, reprioritizing within 1 week each*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 4 | 3 | 5 | 4 | 3 | 5 | 3 |

**Variants:**
- **AI / GR / ST** ← `Delivered \textbf{4 zero-spillover PIs} as sole PM; absorbed 2 strategy pivots, reprioritizing entire backlog within 1 week each` *(487pt)*
- **PL** ← `Shipped \textbf{4 zero-spillover PIs} as sole PM; absorbed 2 strategy pivots, reprioritizing entire backlog within 1 week each` *(482pt)*

---

### Fact A7 — LLM Hackathon / QE Assist
*#21 of 400+ teams (Top 6%); AI Grooming bot productionized as QE Assist by GMNS engineering*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 3 | 2 | 3 | 2 | 2 | 4 | 3 |

**Variants:**
- **AI / ST** ← `Built LLM Grooming bot; ranked \textbf{\#21 of 400+ teams (Top 6\%)} at AmEx Hackathon; productionized as \textbf{QE Assist}` *(489pt)*
- **GR / CA** ← `Built LLM Grooming bot; ranked \textbf{\#21 of 400+ teams (Top 6\%)} at AmEx Hackathon; productionized as \textbf{QE Assist}` *(489pt)*
- **PL** ← `Placed \textbf{\#21 of 400+ teams (Top 6\%)} at AmEx Hackathon; AI sprint-grooming bot productionized as \textbf{QE Assist}` *(477pt)*

---

### Fact A8 — AI-Assisted Story Drafting
*80% AI-assisted story drafting adoption via ChatGPT Enterprise; cut manual story-writing*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 4 | 2 | 3 | 2 | 2 | 3 | 3 |

**Variants:**
- **AI** ← `Drove \textbf{80\% AI-assisted story drafting} via ChatGPT Enterprise; cut manual story-writing across all sprint meetings` *(484pt)*
- **GR / CA** ← `Drove \textbf{80\% AI-assisted story drafting} adoption within team by introducing ChatGPT Enterprise for sprint planning` *(488pt)*

---

## SPRINKLR — Senior Product Analyst (Apr 2023 – Jul 2024)

---

### Fact S1 — Use Case Hub Launch
*1,500+ client patterns across 15 verticals; became platform's #1 entry point for dashboard creation*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 5 | 4 | 5 | 5 | 2 | 4 | 3 |

**Variants:**
- **DA** ← `Launched Use Case Hub (\textbf{1,500+ client patterns}, 15 verticals) as platform's \textbf{\#1 entry point} for dashboard creation` *(487pt)*
- **GR** ← `Analyzed \textbf{1,500+ client patterns} across 15 sectors; launched Use Case Hub, \textbf{\#1 entry point} for dashboard creation` *(486pt)*
- **PL / ST** ← `Grew Social Listening adoption \textbf{$\sim$35\% $\rightarrow$ $\sim$85\%} for SME clients; Use Case Hub became \textbf{\#1 dashboard entry point}` *(486pt)*

---

### Fact S2 — Social Listening Adoption Growth
*35% → 85% adoption for SME clients; onboarding friction removed; time-to-value cut ~75%*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 2 | 5 | 3 | 5 | 4 | 1 | 3 | 4 |

**Variants:**
- **GR** ← `Grew Social Listening adoption \textbf{$\sim$35\% $\rightarrow$ $\sim$85\%} for SME clients; removed onboarding friction, cut time-to-value \textbf{$\sim$75\%}` *(490pt)*

---

### Fact S3 — PM+PO Coverage (6 months)
*Covered full PM + PO scope during lead PM's leave; roadmap, grooming, QA across two time zones*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 4 | 3 | 5 | 4 | 3 | 5 | 3 |

**Variants:**
- **GR** ← `Covered PM + PO ownership for \textbf{6 months} during lead PM's leave; ran roadmap, grooming, QA across two time zones` *(484pt)*
- **PL** ← `Stepped into PM + PO for \textbf{6 months} during lead PM leave; ran roadmap, grooming, and QA across two time zones` *(475pt)*
- **ST** ← `Stepped into PM + PO for \textbf{6 months} during lead PM leave; ran roadmap, grooming, and QA across two time zones` *(475pt)*

---

### Fact S4 — Walmart GenAI Pipeline (Architecture)
*6 data sources, L1/L2/L3 taxonomy, unsupervised ML clustering; 7 days → same-day insight latency*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 3 | 5 | 4 | 4 | 2 | 4 | 2 |

**Variants:**
- **AI** ← `Led Walmart GenAI root-cause analysis pipeline across \textbf{6 data sources}, covering \textbf{100K+ monthly driver contacts}` *(484pt)*
- **AI (2nd bullet)** ← `Architected L1/L2/L3 issue taxonomy and unsupervised ML clustering pipeline; cut latency from \textbf{7 days to same-day}` *(488pt)*
- **DA** ← `Delivered Walmart GenAI pipeline (\textbf{6 data sources}, \textbf{100K+ contacts}); cut insight latency \textbf{7 days $\rightarrow$ same-day}` *(470pt)*
- **PL / ST** ← `Built Walmart GenAI root-cause pipeline (\textbf{6 sources}, \textbf{100K+ contacts}); cut insight latency \textbf{7 days $\rightarrow$ same-day}` *(473pt)*

---

### Fact S5 — Walmart Retention SQL Analysis
*Spark Driver D7 ~65% → D30 ~35% → D60 ~18% cohort deep-dive; diagnosed root cause*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 5 | 5 | 3 | 3 | 2 | 3 | 5 |

**Variants:**
- **GR** ← `Mapped Walmart Spark Driver retention collapse (D7 $\sim$65\% $\rightarrow$ D30 $\sim$35\% $\rightarrow$ D60 $\sim$18\%) via SQL; 4-cohort deep-dive` *(484pt)*
- **DA** ← `Diagnosed Spark retention (D7 $\sim$65\%, D30 $\sim$35\%, D60 $\sim$18\%) via SQL; secured \textbf{\$1.2M TCV} and \textbf{\$9M+ pipeline}` *(476pt)*
- **CA** ← `Mapped Walmart Spark Driver churn: D7 $\sim$65\%, D30 $\sim$35\%, D60 $\sim$18\%; SQL-driven 4-cohort root-cause deep-dive` *(470pt)*

---

### Fact S6 — Walmart TCV & Pipeline
*$1.2M TCV POC-to-close; $9M+ Q4 pipeline; $2M follow-on deal*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 5 | 3 | 3 | 5 | 2 | 3 | 2 |

**Variants:**
- **AI** ← `Secured \textbf{\$1.2M TCV} POC-to-deal and \textbf{\$9M+ Q4 pipeline}; GenAI pipeline foundation closed \textbf{\$2M follow-on deal}` *(488pt)*
- **GR** ← `Secured \textbf{\$1.2M TCV} POC-to-close, \textbf{\$9M+ Q4 pipeline}, and \textbf{\$2M follow-on deal} via Walmart GenAI pipeline` *(469pt)*

---

### Fact S7 — Arabic NLP / Sentiment Improvement
*F1 +11% and intuition +13% lift on Arabic sentiment; for Qatar Sharek 40-ministry platform*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 2 | 4 | 3 | 3 | 1 | 3 | 2 |

**Variants:**
- **AI / DA** ← `Lifted Arabic sentiment \textbf{F1 +11\%} and intuition \textbf{+13\%}; Qatar Sharek \textbf{40-ministry} government platform (\$32M TCV)` *(489pt)*

---

### Fact S8 — Qatar Sharek Platform Delivery
*$32M TCV; 40 ministries; team scaled 6→14; 120 Arabic dashboards in 4 weeks; retention 40% → 55%*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 4 | 3 | 5 | 5 | 1 | 3 | 4 |

**Variants:**
- **GR** ← `Lifted Qatar Sharek app \textbf{7-day retention 40\% $\rightarrow$ 55\%} across 40 government ministries (\$32M TCV, 120 dashboards)` *(488pt)*
- **PL** ← `Launched Qatar Sharek (\textbf{40-ministry} platform, \textbf{\$32M TCV}); scaled team \textbf{6$\rightarrow$14}; lifted 7-day retention \textbf{40\% $\rightarrow$ 55\%}` *(487pt)*
- **CA / FT** ← `Launched Qatar Sharek (Prime Minister's Office, \textbf{40 ministries}, \textbf{\$32M TCV}); scaled \textbf{6$\rightarrow$14}; retention \textbf{40\% $\rightarrow$ 55\%}` *(482pt)*

---

### Fact S9 — Adobe SQL Unification
*3 schemas (Earned / Organic / Paid) unified via SQL; analysis cycle 4 days → 1 day*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 4 | 5 | 4 | 4 | 2 | 2 | 2 |

**Variants:**
- **AI** ← `Unified Adobe Earned / Organic / Paid data via SQL; built spam detection model \textbf{F1 = 87\%} using Sprinklr AI Studio` *(488pt)*
- **GR** ← `Unified Adobe social data (Earned / Organic / Paid, 3 schemas) via SQL pipelines; cut analysis cycle \textbf{4 days $\rightarrow$ 1 day}` *(487pt)*
- **DA** ← `Unified Adobe Earned / Organic / Paid via SQL; built spam model \textbf{F1 = 87\%}; cut analysis cycle \textbf{4 days $\rightarrow$ 1 day}` *(475pt)*
- **PL / FT** ← `Unified Adobe Earned / Organic / Paid SQL pipelines; cut analysis cycle \textbf{4 days $\rightarrow$ 1 day}; spam model \textbf{F1 = 87\%}` *(476pt)*

---

## SPRINKLR — Product Analyst (Apr 2022 – Apr 2023)

---

### Fact P1 — #1 Global PO Ranking
*Ranked #1 globally among all Sprinklr POs in first 6 months; 10/10 CSAT; only 1 of 8 promoted at 11 months*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 |

**Variants:**
- **AI** ← `Ranked \textbf{\#1 globally} among all Sprinklr POs in 6 months (\textbf{10/10 CSAT}); only PO promoted at 11 months out of 8` *(478pt)*
- **DA / PL / FT** ← `Ranked \textbf{\#1 globally} among all Sprinklr POs in first 6 months (\textbf{10/10 CSAT}); only 1 of 8 promoted at 11 months` *(472pt)*
- **GR / ST / CA** ← `Ranked \textbf{\#1 globally} among all Sprinklr POs in first 6 months (\textbf{10/10 CSAT}); only 1 of 8 promoted at 11 months` *(472pt)*

---

### Fact P2 — Discord / Snapchat AI Engagement
*25% brand risk reduction via AI hate-comment detection (Discord); +15% MoM Snapchat engagement*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 3 | 3 | 4 | 1 | 3 | 5 |

**Variants:**
- **AI** ← `Reduced Discord brand reputation risk \textbf{25\%} via AI hate-comment detection; drove Snapchat engagement \textbf{+15\% MoM}` *(488pt)*
- **GR** ← `Scaled Snapchat brand engagement \textbf{+15\% MoM} across music and sport via data-driven content strategy optimization` *(485pt)*
- **CA** ← `Grew Snapchat brand engagement \textbf{+15\% MoM}; cut Discord brand reputation risk \textbf{25\%} via AI hate-comment classifier` *(490pt)*

---

### Fact P3 — Mars Inc. Case Response Rate
*Identified engagement trends via SQL; drove +10% Case Response Rate via AI routing recommendations*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 4 | 4 | 3 | 4 | 1 | 2 | 3 |

**Variants:**
- **GR** ← `Identified Mars Inc. product engagement trends; drove \textbf{+10\% Case Response Rate} via AI routing recommendations` *(485pt)*
- **DA** ← `Identified Mars Inc.\ engagement trends via SQL; drove \textbf{+10\% Case Response Rate} via AI routing recommendations` *(486pt)*

---

## LINKRIGHT (Jun 2025 – Present)

---

### Fact L1 — LLM Pipeline Architecture
*Hybrid resume parser, 16-dim eval scorecard, fabrication guard, automated feedback loop — built solo*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 2 | 5 | 4 | 2 | 1 | 5 | 2 |

**Variants:**
- **AI / ST** ← `Designed and built solo LLM pipeline: hybrid resume parser, \textbf{16-dim eval scorecard}, fabrication guard, feedback loop` *(487pt)*
- **DA** ← `Built data pipeline solo: hybrid resume parser, \textbf{16-dim eval scorecard}, fabrication guard, automated feedback loop` *(475pt)*

---

### Fact L2 — Self-Hosted LLM Deployment
*9 self-hosted LLMs on Oracle VPS (Ollama, fallback chain); FastAPI backend; CLI on PyPI*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 2 | 5 | 4 | 2 | 1 | 5 | 2 |

**Variants:**
- **AI / DA / ST** ← `Deployed \textbf{9 self-hosted LLMs} on Oracle VPS (Ollama, fallback chain); built FastAPI backend, CLI published to \textbf{PyPI}` *(492pt)*

---

### Fact L3 — Feature Delivery Velocity
*44 of 57 planned features (77%) in 11 months while holding full-time AmEx role*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 3 | 4 | 3 | 2 | 5 | 4 |

**Variants:**
- **AI** ← `Shipped \textbf{44 of 57 planned features (77\%)} in 11 months alongside full-time AmEx; solo-managed end-to-end roadmap` *(491pt)*
- **GR** ← `Shipped \textbf{44 of 57 planned features (77\%)} in 11 months while holding a full-time AmEx role; published CLI to \textbf{PyPI}` *(491pt)*
- **ST** ← `Shipped \textbf{44/57 features (77\%)} in 11 months; deployed \textbf{9 self-hosted LLMs} on Oracle VPS; published CLI to \textbf{PyPI}` *(487pt)*
- **CA / GR (PostHog variant)** ← `Shipped \textbf{44/57 features (77\%)} in 11 months; PostHog analytics, N8N automation; published CLI to \textbf{PyPI}` *(443pt — 90%, above floor; use when PostHog/growth tools are JD signal)*

---

### Fact L4 — Growth Analytics Integration
*PostHog analytics integration + N8N content automation workflows*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 5 | 2 | 3 | 2 | 1 | 4 | 4 |

**Variants:**
- **GR** ← `Built AI career navigation platform with PostHog growth analytics integration and N8N content automation workflows` *(483pt)*

---

### Fact L5 — LinkRight Validation (Pre-Build)
*147-response survey + 7,000+ cold-reach touches; 3 ICP segments defined before writing a line of code*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 4 | 2 | 3 | 2 | 2 | 5 | 4 |

**Variants:**
- **ST / CA** ← `Validated linkright.in via \textbf{147-response} survey + \textbf{7,000+} cold-reached; defined 3 ICP segments pre-build` *(432pt — 87.9%, above floor; this bullet earns its place through uniqueness of story)*

⚠️ *Width note: 432pt is above the 418pt floor but below the 95% target. The story is strong enough to justify inclusion. If space allows, consider combining with L3 ST variant into a single merged bullet (fintech resume does this as one combined bullet).*

**Combined variant (FT):** `Solo PM + engineer; \textbf{147-response} survey + \textbf{7,000+} cold-reached; \textbf{44/57 features (77\%)} in 11 months; \textbf{PyPI} CLI`

---

## SUKHA EDUCATION (Jan 2025 – May 2025)

---

### Fact K1 — Digital Transformation / GTM
*Digital transformation for Chennai NGO (2,000+ students); Salesforce + Workspace rollout; ~Rs.60K/year savings*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 2 | 3 | 2 | 2 | 3 | 1 | 3 | 2 |

**Variants:**
- **AI** ← `Launched digital transformation for Chennai NGO (2,000+ students); Salesforce + Workspace rollout; \textbf{$\sim$Rs.60K/year}` *(485pt)*
- **DA** ← `Drove digital transformation, Chennai NGO (2,000+ students); Salesforce + Workspace rollout; \textbf{$\sim$Rs.60K/year} savings` *(490pt)*
- **GR** ← `Launched GTM and digital transformation for Chennai NGO (2,000+ students); \textbf{$\sim$Rs.60K/year} in operational savings` *(488pt)*

---

## VENTURES & ADVISORY

---

### Fact V1 — ContentStack: Freelance AI PM (Nov 2024 – Jun 2025)
*Part-time freelance AI PM (paid). Concurrent with AmEx full-time role. 3 AI products: Compose AI (content creation), DesignerAI (website creation), Lens (performance monitoring). 6 AI features shipped: AI Ghost Writing, Quick AI Edit, AI Embedding, Word Replacement, GEO (Generative Engine Optimization), + 1 more.*
*Real PM work: PRDs for all 3 products, product backlog ownership, LLM evaluation, A/B testing with stakeholder surveys, 10+ competitor benchmarks per domain, wireframe design, prompt engineering, agent workflow configuration. Team: 1 dev + 1 designer.*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 5 | 3 | 4 | 3 | 4 | 2 | 4 | 3 |

**Locked variants (width-verified):**
- **B1 — All** ← `Wrote PRDs and shipped \textbf{6 AI features} across Compose AI, DesignerAI, and Lens at ContentStack (freelance AI PM)` *(487pt, 99.0%)*
- **B2 — AI / DA** ← `LLM output eval, stakeholder A/B surveys, \textbf{10+ competitor} benchmarks per domain; wireframes; prompt engineering` *(487pt, 99.0%)*
- **B2 alt — AI / DA** ← `LLM eval + A/B test designs; \textbf{10+ competitor} benchmarks per domain; wireframes; prompt + agent-workflow design` *(487pt, 98.8%)*
- **B1 alt — ST / CA** ← `Shipped \textbf{6 AI features} (Compose AI, DesignerAI, Lens); PRDs, LLM eval, \textbf{10+ competitor} benchmarks, wireframes, prompt engineering` *(use this for ST/CA resumes)*

**Heading (project heading line):**
- `{\textbf{ContentStack} $|$ \emph{Freelance AI PM}}{Nov 2024 -- Jun 2025}` — short, no overflow risk

---

### Fact V2 — GoGoGo: Angel Investor & Product Advisor (Sep 2024 – Jun 2025)
*Angel investor (equity). Pre-seed ride-hailing startup, Indore. Involvement spanned: early brand building (name ideation, logos, posters, AI anthem, AI videos), LinkedIn automation, driver acquisition, founding team onboarding, driver welfare group, product advisory, investor pitching, attended Startup Mahakumbh and StartupTech Summit Bangalore on behalf of GoGoGo. ~Rs.2.5Cr raised (pre-seed). Left active role Jun 2025; remains on bi-weekly board calls.*
*⚠️ Chief of Staff was publicly announced but NEVER formalized — do NOT use this title. Financial rescue involvement confirmed but do NOT include in resume/professional context.*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 4 | 2 | 3 | 3 | 2 | 5 | 5 |

**Locked variants (width-verified):**
- **Heading** ← `{\textbf{GoGoGo} $|$ \emph{Angel Investor}: pre-seed ride-hailing (Indore); backed, advised on product \& GTM; \textbf{$\sim$Rs.2.5Cr raised}}{}` *(471pt, 95.7%)*
- **B1 — Events/Investor** ← `Pitched to investors; attended \textbf{Startup Mahakumbh} and \textbf{StartupTech Summit Bangalore} on behalf of GoGoGo` *(481pt, 97.6%)* [NOT CURRENTLY IN RESUMES — space trade-off]
- **B2 — Brand/GTM (in all resumes)** ← `Built brand + GTM: AI anthem, AI video, LinkedIn automation; drove driver acquisition and founding team onboarding` *(492pt, 99.8%)*

---

### Fact V3 — Navii (HeyNavii): Beta Growth PM (2025)
*Voluntary beta contributor role. AI-powered career navigation app. Mapped 5+ user journeys, logged 14 bugs + 9 enhancements, wrote onboarding guides + videos, built N8N automations + Chrome extension, explored AI influencer/UGC automation and automated AI image/video generation pipelines. Platform grew ~2K → ~20K during beta period — multiple contributors, cannot claim sole ownership of growth.*
*⚠️ Do NOT claim sole credit for 2K→20K. Always say "during beta" or "multiple contributors".*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 5 | 2 | 3 | 2 | 1 | 4 | 5 |

**Locked variants (width-verified):**
- **Heading** ← `{\textbf{Navii (HeyNavii)} $|$ \emph{Beta Growth PM}}{2025}`
- **B1 — All** ← `User base \textbf{2K $\rightarrow$ 20K} during beta; built N8N automations + Chrome extension; logged \textbf{14 bugs} + \textbf{9 enhancements}` *(483pt, 98.2%)*

---

## MASTERS UNION (2025)

---

### Fact M1 — Scholarship + Prototype Sprint
*50% merit scholarship; shipped wellness app prototype + full GTM in 2 days*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 4 | 2 | 2 | 3 | 1 | 4 | 3 |

**Variants:**
- **AI / GR / ST** ← `Admitted Masters Union (2025) on \textbf{50\% merit scholarship}; shipped wellness app prototype and full GTM in \textbf{2 days}` *(484pt)*

---

## EDUCATION

---

### Fact E1 — JEE + Class 12 Scholastic
*JEE Advanced Rank 2446 (Top 0.002% of 1.2M+); Class 12 District Rank 1, 94.2%, 100/100 Maths & Chemistry*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 |

**Variants:**
- **All** ← `JEE Advanced \textbf{Rank 2446} (Top 0.002\% of 1.2M+); Class 12 \textbf{District Rank 1}, 94.2\%, 100/100 Maths \& Chemistry` *(478pt)*

---

### Fact E2 — GGI Fellow + Scaler Certifications

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 3 | 4 | 3 | 3 | 3 | 3 | 2 |

**Variants:**
- **All** ← `\textbf{GGI Fellow} (2024); Scaler Academy: SQL, Excel, Tableau, Power BI, Python, Product Analytics (all 6 completed)` *(473pt)*

---

### Fact E3 — GATE 2022 Engineering Exam
*AIR-1463, Top 1.5% of 100K+ candidates — not in any current resume*
*Use as 3rd education bullet in DA/FT resumes where technical depth is the key signal. Can replace E2 when GATE is more JD-relevant than certifications.*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 3 | 1 | 5 | 3 | 2 | 5 | 2 | 1 |

**Variants:**
- **DA / FT** ← `\textbf{GATE 2022}: \textbf{AIR-1463 (Top 1.5\%)} among 100K+ candidates; quantitative aptitude rank in top engineering cohort` *(486pt)*
- **DA / FT (alt)** ← `Secured \textbf{AIR-1463 (Top 1.5\%)} in GATE 2022 Engineering Exam; outperformed \textbf{100K+} candidates across India` *(467pt)*

⚠️ *Adding E3 as 3rd education bullet increases section height — compile and verify 1-page before shipping.*

---

### Other Scholastic Achievements (not in bank as bullets — reference only)
*These exist in older resumes. Too far back for a 4-year PM profile. Context only.*

- **Class 10 Rank 1 in School, 10/10 CGPA** — felicitated by State Education Minister of M.P. *(too far back; nice trivia, skip)*
- **UCMAS Abacus Rank 3 at State level** — qualified for National round *(niche; skip)*
- **Vigyan Manthan Yatra Top 2 of 125 CBSE students in MP** *(science curiosity signal; niche; skip)*

---

## Archetype Quick-Reference Cheat Sheet

*For each archetype: top-rated facts in priority order. When space is tight, drop from the bottom up.*

### AI PM — Priority Order
A7 (LLM Hackathon) · A8 (AI Drafting) · L1 (LLM Pipeline) · L2 (Self-Hosted LLMs) · S4 (Walmart GenAI) · S7 (Arabic NLP) · A3 (CRR) · L3 (Feature Velocity) · A5 (Award) · P1 (Ranking) · P2 (Discord AI) · A6 (Zero-Spillover) · S6 (TCV) · A1 (CDL Arch) · S9 (Adobe SQL) · V1 (ContentStack) · K1 (Sukha) · M1 (Masters Union) · E1 · E2

### Growth PM — Priority Order
S2 (Adoption 35→85%) · S1 (Use Case Hub) · S5 (Retention SQL) · S6 (TCV/Pipeline) · A4 (Speed-to-Market) · A8 (AI Drafting) · S8 (Qatar Retention) · A6 (Zero-Spillover) · P1 (Ranking) · P2 (Snapchat) · P3 (Mars CRR) · L4 (PostHog) · A3 (CRR) · L3 (Feature Velocity) · V3 (Navii) · M1 (Masters Union) · S3 (PM+PO) · K1 (Sukha) · E1 · E2

### Data/Technical PM — Priority Order
A1 (CDL Pipeline) · A2 (CDL Roadmap) · S4 (Walmart GenAI) · S9 (Adobe SQL) · S5 (Retention SQL) · A3 (CRR) · L1 (LLM Pipeline) · L2 (Self-Hosted LLMs) · A4 (Speed-to-Market) · S7 (Arabic NLP) · P3 (Mars SQL) · A5 (Award) · P1 (Ranking) · L3 (Feature Velocity) · A6 (Zero-Spillover) · K1 (Sukha) · E1 · E2

### Platform PM — Priority Order
A1 (CDL Pipeline) · A2 (CDL Roadmap) · A3 (CRR) · A6 (Zero-Spillover) · A4 (Speed-to-Market) · S1 (Use Case Hub) · S2 (Adoption) · S3 (PM+PO) · S8 (Qatar) · S9 (Adobe SQL) · A5 (Award) · A7 (Hackathon) · A8 (AI Drafting) · P1 (Ranking) · L1 (LLM Pipeline) · L3 (Feature Velocity) · K1 (Sukha) · E1 · E2

### Enterprise SaaS PM — Priority Order
S6 (TCV/Pipeline) · S8 (Qatar $32M) · S1 (Use Case Hub) · S2 (Adoption) · A4 (Speed-to-Market) · S3 (PM+PO) · P3 (Mars) · A3 (CRR) · A5 (Award) · A6 (Zero-Spillover) · P2 (Discord) · S5 (Retention SQL) · M1 (Masters Union) · K1 (Sukha) · A1 (CDL) · P1 (Ranking) · E1 · E2

### Risk / FinTech PM — Priority Order
A1 (CDL Pipeline) · A2 (CDL Roadmap) · A4 (Speed-to-Market) · A3 (CRR) · A5 (Award) · A6 (Zero-Spillover) · S4 (Walmart GenAI) · S9 (Adobe SQL) · A7 (Hackathon) · A8 (AI Drafting) · P1 (Ranking) · S5 (Retention SQL) · L1 (LLM Pipeline) · L2 (Self-Hosted LLMs) · E1 · E2 · E3 (optional)

### 0-to-1 Startup PM — Priority Order
A6 (Zero-Spillover) · S3 (PM+PO) · L3 (Feature Velocity) · L5 (Validation) · L2 (Self-Hosted LLMs) · L1 (LLM Pipeline) · A3 (CRR) · A7 (Hackathon) · V2 (GoGoGo) · V1 (ContentStack) · S4 (Walmart GenAI) · A4 (Speed-to-Market) · L4 (PostHog) · S1 (Use Case Hub) · M1 (Masters Union) · V3 (Navii) · A5 (Award) · S6 (TCV) · E1 · E2

### Consumer / App PM — Priority Order
P2 (Discord/Snapchat) · V2 (GoGoGo) · V3 (Navii) · S5 (Retention SQL) · S8 (Qatar Retention) · S2 (Adoption Growth) · L3 (Feature Velocity) · L4 (PostHog) · L5 (Validation) · A4 (Speed-to-Market) · A8 (AI Drafting) · A7 (Hackathon) · S1 (Use Case Hub) · A6 (Zero-Spillover) · A5 (Award) · P3 (Mars) · P1 (Ranking) · K1 (Sukha) · E1 · E2

---

## Missing Archetype Recommendations

Only one archetype worth building next:

**Enterprise SaaS PM (EN)** — Your Sprinklr work is textbook B2B enterprise: Walmart ($1.2M + $9M+ pipeline + $2M follow-on), Adobe (multi-schema integration), Qatar government ($32M TCV, 40 ministries), Mars Inc. Frame the story around large-deal complexity, multi-stakeholder rollouts, and platform adoption at enterprise scale. High-value archetype for Salesforce, HubSpot, ServiceNow, Zendesk, and similar companies. All other 7 archetypes (AI, GR, DA, PL, FT, ST, CA) now have base resumes as of 2026-05-23.

---

## Appended Bullets
*Net-new bullets generated during JD customizations. Add here after every new resume build so the bank grows.*
*Format: Fact ID | Archetype | JD/Company | Date | LaTeX | Width*

---

<!-- APPEND NEW BULLETS BELOW THIS LINE — one entry per bullet, newest at top -->

*(empty — first entry goes here)*

---

## SKILLS BANK

*One-stop reference for skills keywords. Use this before editing any `\section{Skills}` block.*
*Goal: dense ATS coverage. Include keywords even if you haven't used them personally — they exist for keyword-matching, not to be elaborated on in interviews.*

---

### How to Use the Skills Bank

1. Pick your archetype → go to its pre-built LaTeX block below.
2. Drop the block directly into your `.tex` file's `\section{Skills}`.
3. For a specific JD: scan the Master Index for domain-specific keywords in the JD → add any missing ones to the relevant bucket. Remove irrelevant buckets or thin ones.
4. Each block is designed to fit within 1 page of the current resume layouts. If adding keywords causes overflow, trim from the **Tools** bucket first (least ATS-weighted).

---

### Master Keyword Index (All Domains)

*Updated 2026-05-23. This dictionary is exhaustive — include all variations so JD-matching never misses a phrasing. Do NOT copy all of these into a resume skills section; use the pre-built LaTeX blocks below and tune per JD.*

---

**Data & Technical**
`SQL` · `SQL (production)` · `BigQuery` · `Python` · `FastAPI` · `ETL` · `ETL Architecture` · `Data Pipeline Design` · `Schema Design` · `Data Modeling` · `Data Governance` · `Data Quality` · `Data Lineage` · `REST APIs` · `API Design` · `GraphQL` · `Apache Kafka` · `Apache Spark` · `dbt` · `Airflow` · `Snowflake` · `Redshift` · `Databricks` · `Data Mesh` · `OLAP` · `OLTP` · `Event-Driven Architecture` · `Microservices` · `System Design` · `GCP` · `AWS` · `Azure` · `N8N` · `Workflow Automation` · `Data Contracts` · `Data Architecture` · `Data Infrastructure` · `Data Platform`

---

**AI / ML**
`LLM Pipeline Design` · `LLM Pipelines` · `Large Language Models` · `Generative AI` · `GenAI` · `Prompt Engineering` · `RAG Architecture` · `Retrieval-Augmented Generation` · `Agentic AI` · `AI Agents` · `Agent Workflows` · `Evaluation Frameworks` · `LLM Evaluation` · `Fabrication Guard Systems` · `Hallucination Detection` · `Self-Hosted LLMs` · `Self-Hosted LLMs (Ollama)` · `Ollama` · `LangChain` · `LlamaIndex` · `Fine-Tuning` · `RLHF` · `NLP` · `Sentiment Analysis` · `Named Entity Recognition` · `Embeddings` · `Vector Databases` · `Feature Engineering` · `Supervised ML` · `Unsupervised ML` · `Clustering` · `Predictive Modeling` · `MLOps` · `AI Safety` · `Responsible AI` · `ChatGPT Enterprise` · `GEO (Generative Engine Optimization)` · `AI-Assisted Analytics` · `AI Video Creation` · `AI Content Automation`

---

**Product & Strategy**
`Roadmapping` · `PRDs` · `OKR/KPI Design` · `Feature Prioritization` · `RICE` · `MoSCoW` · `User Research` · `UX Research` · `Customer Discovery` · `Jobs-to-Be-Done (JTBD)` · `GTM Strategy` · `Competitive Analysis` · `Market Research` · `Business Case Development` · `Stakeholder Management` · `Cross-Functional Leadership` · `SAFe Agile` · `Agile` · `PI Planning` · `Sprint Planning` · `Backlog Management` · `Product-Led Growth (PLG)` · `A/B Testing` · `Experimentation` · `Wireframing` · `Prototyping` · `Design Thinking` · `User Story Writing` · `ICP Segmentation` · `Problem Definition` · `Rapid Prototyping`

---

**Growth & Analytics**
`Funnel Analysis` · `Cohort Analysis` · `Retention Optimization` · `D7/D30/D60 Retention` · `Activation Metrics` · `Time-to-Value Reduction` · `Onboarding Optimization` · `Churn Reduction` · `LTV/CAC Analysis` · `DAU/MAU` · `Engagement Metrics` · `NPS` · `CSAT` · `AARRR Framework` · `Viral Loops` · `Growth Loops` · `Network Effects` · `Mixpanel` · `Amplitude` · `PostHog` · `Google Analytics` · `Tableau` · `PowerBI` · `Hotjar` · `FullStory` · `Optimizely` · `LinkedIn Automation` · `Brand Building` · `Investor Pitching`

---

**Platform & Infrastructure**
`API Product Design` · `API-First Design` · `Self-Serve Platform Design` · `Platform Strategy` · `Developer Experience (DX)` · `Rule Engine Design` · `Workflow Automation` · `Audit Trails` · `Versioning Systems` · `RBAC` · `Multi-Tenant Architecture` · `Data Pipeline Architecture` · `Platform Scalability` · `Event-Driven Architecture` · `Configurable Risk Platforms`

---

**Enterprise SaaS**
`B2B Product Management` · `Multi-Stakeholder Rollout` · `TCV` · `ARR` · `Revenue Growth` · `Customer Success Partnership` · `SLA Management` · `Churn Prevention` · `Expansion Revenue` · `Fortune 500 Clients` · `Enterprise Clients`

---

**Risk & Compliance**
`AML` · `Anti-Money Laundering` · `KYC` · `Know Your Customer` · `CDD` · `Risk Categorization` · `Risk Scoring` · `Risk Configuration` · `Risk Platform` · `Compliance Workflows` · `Compliance Automation` · `RegTech` · `FinTech` · `Financial Crime Prevention` · `Transaction Monitoring` · `Sanctions Screening` · `CDL Pipeline` · `AML Risk Coverage`

---

**Ventures & Entrepreneurship**
`Angel Investing` · `Pre-Seed Investing` · `Startup Advising` · `Product Advisory` · `Freelance Product Management` · `Investor Relations` · `Fundraising Support` · `Brand Building from Scratch` · `Driver Acquisition` · `Founding Team Building` · `GEO` · `AI Video Marketing` · `Growth Hacking`

---

### Pre-Built LaTeX Blocks by Archetype

*Drop these directly into `\section{Skills}` → `\begin{itemize}` → `\small{\item{...}}`.*
*All 7 compile to 1 page on their respective resume layouts as of 2026-05-23.*

---

#### AI PM

```latex
\textbf{AI/ML:}{ LLM Pipeline Design, Prompt Engineering, RAG Architecture, Evaluation Frameworks, Fabrication Guard Systems, NLP, Sentiment Analysis, Embeddings, Vector Databases, Self-Hosted LLMs (Ollama), LangChain, Fine-Tuning, Supervised \& Unsupervised ML, Feature Engineering, MLOps, AI Safety, Model Evaluation} \\
\textbf{Product:}{ AI Product Strategy, PRD Writing, Roadmapping, OKR/KPI Design, User Research, Go-to-Market Strategy, A/B Testing, Feature Prioritization, Customer Discovery, Competitive Analysis, North Star Metrics, SAFe Agile, PI Planning, Stakeholder Management} \\
\textbf{Data \& Engineering:}{ SQL (production), Python, BigQuery, FastAPI, REST APIs, Schema Design, Data Architecture, ETL Pipelines, Data Modeling, System Design, GCP, Tableau, Mixpanel, Amplitude} \\
\textbf{Tools:}{ JIRA, Rally, Figma, Lucidchart, ChatGPT Enterprise, N8N, PowerBI, Postman, GitHub, Confluence, Miro}
```

*JD tuning: add `LlamaIndex`, `Multimodal AI`, `Responsible AI`, `RLHF` if JD mentions them. Swap `Miro`/`Confluence` if space is tight.*

---

#### Growth PM

```latex
\textbf{Growth \& Product:}{ Funnel Analysis, Cohort Analysis, Retention Optimization, Activation Metrics, A/B Testing, Experimentation, Onboarding Optimization, Time-to-Value Reduction, Product-Led Growth (PLG), Churn Reduction, LTV/CAC Analysis, DAU/MAU, NPS, AARRR Framework, GTM Strategy, Roadmapping, PRDs, OKR/KPI Design, Stakeholder Management} \\
\textbf{Data:}{ SQL (production), Python, BigQuery, Mixpanel, Amplitude, Tableau, PostHog, Google Analytics, PowerBI, Cohort Modeling, Schema Design, Data Modeling} \\
\textbf{AI/ML:}{ NLP, Sentiment Analysis, Unsupervised ML Clustering, LLM Pipelines, Prompt Engineering, Predictive Modeling, Feature Engineering, AI-Assisted Analytics} \\
\textbf{Tools:}{ JIRA, Rally, Figma, SAFe Agile, ChatGPT Enterprise, N8N, Lucidchart, Hotjar, Optimizely, FullStory, PowerBI, Notion}
```

*JD tuning: add `Feature Flags`, `Viral Loops`, `Expansion Revenue` if mentioned. Remove `FullStory`/`Hotjar` for B2B/enterprise roles.*

---

#### Data / Technical PM

```latex
\textbf{Data \& Engineering:}{ SQL (production), Python, BigQuery, FastAPI, ETL Architecture, Schema Design, Data Pipeline Design, Data Modeling, Data Governance, Data Quality, REST APIs, Apache Kafka, dbt, Airflow, Snowflake, Event-Driven Architecture, N8N, System Design, GCP/AWS} \\
\textbf{Platform \& Product:}{ Data Product Strategy, Self-Serve Analytics, API Product Design, Data Democratization, Data Contracts, Roadmapping, PRDs, OKR/KPI Design, SAFe Agile, PI Planning, Metrics Frameworks, Stakeholder Management} \\
\textbf{AI/ML:}{ ML Model Integration, NLP, Sentiment Analysis, Unsupervised ML Clustering, LLM Pipelines, Prompt Engineering, Eval Frameworks, Self-Hosted LLMs (Ollama), Feature Engineering, MLOps} \\
\textbf{Tools:}{ JIRA, Rally, Figma, Tableau, Mixpanel, Amplitude, ChatGPT Enterprise, Lucidchart, PowerBI, dbt Cloud, Databricks, Notion}
```

*JD tuning: for pure data infra roles, elevate `Data Mesh`, `Data Lineage`, `OLAP/OLTP` from Master Index.*

---

#### Platform PM (AmEx Internal)

```latex
\textbf{Platform \& Product:}{ API Product Design, Self-Serve Platform Design, Rule Engine Design, Configurable Risk Platforms, Workflow Automation, Audit Trails, Versioning Systems, RBAC, Multi-Tenant Architecture, API Gateway, Developer Experience, Roadmapping, PRDs, SAFe Agile, PI Planning, OKRs, Stakeholder Management} \\
\textbf{Data \& Engineering:}{ SQL (production), Python, BigQuery, FastAPI, ETL Architecture, Schema Design, Data Pipeline Architecture, N8N Workflow Automation, REST APIs, Microservices, Event-Driven Architecture, Data Governance, System Design, GCP/AWS} \\
\textbf{AI/ML:}{ LLM Pipelines, Self-Hosted LLMs (Ollama), Prompt Engineering, Eval Frameworks, Supervised \& Unsupervised ML, NLP, Fabrication Guard Systems, Feature Engineering} \\
\textbf{Tools:}{ JIRA, Rally, Figma, Tableau, Mixpanel, Amplitude, ChatGPT Enterprise, Lucidchart, PowerBI, Confluence, Postman, Miro}
```

*JD tuning: for external platform/API product roles, swap `Configurable Risk Platforms` for `Developer Platform Strategy`. Add `AML`, `KYC`, `RegTech` for FinTech/Risk roles.*

---

#### Risk / FinTech PM

```latex
\textbf{Fintech \& Risk:}{ AML/KYC Risk Policy, Rule Engine Design, Configurable Risk Platforms, Regulatory Compliance, Workflow Automation, Audit Trails, Versioning Systems, RBAC, Data Governance, Risk Scoring Frameworks, Roadmapping, PRDs, OKR/KPI Design, SAFe Agile, PI Planning, Stakeholder Management} \\
\textbf{Data \& Engineering:}{ SQL (production), Python, BigQuery, FastAPI, ETL Architecture, Schema Design, Data Pipeline Design, Data Contracts, REST APIs, N8N Workflow Automation, Event-Driven Architecture, System Design, GCP/AWS} \\
\textbf{AI/ML:}{ LLM Pipelines, NLP, Sentiment Analysis, Prompt Engineering, Unsupervised ML Clustering, Eval Frameworks, Self-Hosted LLMs (Ollama), Feature Engineering, AI-Assisted Analytics} \\
\textbf{Tools:}{ JIRA, Rally, Figma, Tableau, Mixpanel, Amplitude, ChatGPT Enterprise, Lucidchart, PowerBI, Confluence, Postman, Miro}
```

*JD tuning: add `Transaction Monitoring`, `Sanctions Screening`, `EDD/CDD` from Master Index if JD is banking-heavy. Swap `Mixpanel`/`Amplitude` for `Palantir` or `SAS` if compliance analytics focus.*

---

#### 0-to-1 Startup PM

```latex
\textbf{0-to-1 \& Product:}{ Customer Discovery, ICP Segmentation, Problem Definition, Rapid Prototyping, A/B Testing, Experimentation, PLG, GTM Strategy, Roadmapping, PRDs, OKR/KPI Design, SAFe Agile, PI Planning, Stakeholder Management} \\
\textbf{Data:}{ SQL (production), Python, BigQuery, PostHog, Mixpanel, Amplitude, Tableau, Cohort Analysis, Funnel Analysis, Schema Design} \\
\textbf{AI/ML:}{ LLM Pipeline Design, Prompt Engineering, Self-Hosted LLMs (Ollama), Eval Frameworks, Fabrication Guard Systems, FastAPI, NLP, Feature Engineering, MLOps} \\
\textbf{Tools:}{ JIRA, Rally, Figma, N8N, ChatGPT Enterprise, Notion, GitHub, Lucidchart, PowerBI, Postman, Miro}
```

*JD tuning: for technical founding PM roles, move AI/ML bucket up. For ops/growth-heavy startups, expand Data bucket. Add `Jobs-to-Be-Done`, `Hypothesis-Driven Development`, `Lean Startup` if JD mentions framework familiarity.*

---

#### Consumer / App PM

```latex
\textbf{Growth \& Consumer:}{ Retention Optimization, Funnel Analysis, Cohort Analysis, A/B Testing, DAU/MAU, NPS, AARRR Framework, Product-Led Growth (PLG), Onboarding Optimization, Churn Reduction, Roadmapping, PRDs, OKR/KPI Design, GTM Strategy, Stakeholder Management} \\
\textbf{Data:}{ SQL (production), Python, BigQuery, PostHog, Mixpanel, Amplitude, Tableau, Google Analytics, Cohort Modeling, Schema Design} \\
\textbf{AI/ML:}{ NLP, Sentiment Analysis, LLM Pipelines, Prompt Engineering, Unsupervised ML Clustering, AI-Assisted Analytics, Feature Engineering} \\
\textbf{Tools:}{ JIRA, Rally, Figma, ChatGPT Enterprise, N8N, Hotjar, Optimizely, FullStory, Notion, Lucidchart, PowerBI}
```

*JD tuning: add `Feature Flags`, `Push Notifications`, `In-App Messaging`, `Mobile PM` from Master Index if JD is mobile-first. Add `Viral Loops`, `K-factor`, `Network Effects` for consumer social/marketplace roles.*

---

### Skills Section Design Rules

1. **Trim from Tools first** — ATS weights domain skills over tools.
2. **Never remove more than 2 keywords per bucket** without checking if they appear in the JD.
3. **Max 4 buckets** — don't add a 5th bucket (page overflow risk).
4. **Keyword order matters (weakly)** — put the most JD-matching keywords earlier in each bucket.
5. **`\&` not `&`** in LaTeX — always escape ampersands inside the itemize block.
6. **DAU/MAU warning** — the `/` in `DAU/MAU` is an unbreakable character in LaTeX. If it falls at a line boundary inside a Skills paragraph it can cause Overfull `\hbox`. If you see overflow after editing Skills, the fix is to adjust the text before `DAU/MAU` so it lands mid-line, not at the wrap point.

---

## New Fact Template
*Copy this block when a JD customization surfaces a genuinely new achievement not in the bank above.*

```
### Fact XX — [Short Name]
*[One-line plain-English description of the underlying achievement]*

| AI | GR | DA | PL | EN | FT | ST | CA |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| ?  | ?  | ?  | ?  | ?  | ?  | ?  | ?  |

**Variants:**
- **[ARCHETYPE] | [JD/Company slug] | [date]** ← `[LaTeX bullet text]` *([width]pt)*
```
