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



# LAYER 1: THE REAL
### The unfiltered truth — everything that actually happened, raw and complete.
### Rule: Nothing is ever removed from this file. Every detail lives here.
### Audience: Private. Only for Satvik and this system.

---

> **What this file is:**
> Every fact, every context, every emotion, every messy behind-the-scenes reality.
> The things that didn't make it to the resume. The things that explain *why* something happened.
> The unvarnished version — including failures, politics, frustrations, and the full story.

---

## S1 — Early Life, Family & Tragedy (1999–2010)

**✅ CONFIRMED ACCURATE — sourced from career profile, validated by Satvik**

Satvik Jain was born into a family that moved frequently across Madhya Pradesh and later Jharkhand due to his father's career as a bank manager at Canara Bank. His father was deeply invested in his holistic development — UCMAS Abacus Mental Math, drawing & sketching, classical music vocal training. He would wake at 4 AM every morning to carry Satvik and his sister Sanika's school bags to the van pickup by 5:30 AM. He took the family on trips to Kullu Manali, Shimla, Gangtok, and Assam.

**The defining event — July 8, 2010:**
When Satvik was 11 years old, his father took his own life. The family was on summer vacation at his nani's house. The circumstances remain painful and uncertain — the family suspects someone may have been pressurizing him, possibly related to a wrong judgment or bribe during his tenure as bank manager. Someone reportedly appeared at the branch that morning; what happened in that exchange pushed him to take that extreme step. The family has never fully confirmed whether it was voluntary or forced.

This loss was devastating. Satvik was suddenly the eldest and only male in the family, responsible for his younger sister Sanika and his mother. No other support structure existed. He cried frequently in the beginning, then gradually shut that down — he needed to be the strong one. He grew up ten years overnight.

For the next 15 years, he rarely allowed himself to remember his father deeply because he knew it would break him. He essentially erased many memories of his father as a coping mechanism — a survival strategy that left lasting marks on how he processes vulnerability and grief.

---

## S2 — Schooling & Early Achievements in Chhatarpur (2010–2017)

**✅ CONFIRMED ACCURATE — sourced from career profile, validated by Satvik**

After his father's death, the family spent ~1 year at his nani's house in Panna before settling in Chhatarpur, which remains the family's home base (his mother still lives there). Academic excellence became his way of honoring his father and securing the family's future.

**Key achievements:**
- **Class 9 (~2013–14):** Ranked 3rd at State level in the 9th UCMAS Abacus Mental Math Competition — qualified for nationals. The training had been started by his father years earlier.
- **Class 9:** Selected as one of Top 2 students out of 125 CBSE Board students in all of Madhya Pradesh for the national Vigyan Manthan Yatra science trip — a government-organized program selecting a tiny number of students from each state.
- **Class 10 (2015):** Ranked 1st in school, scored a perfect 10/10 CGPA in CBSE Boards. Felicitated personally by **Smriti Irani**, the Union Education Minister of India at the time — a national-level recognition.
- **Class 12 (2017, MPBSE):** Ranked 1st in the entire Chhatarpur District with 94.2%. Scored 100/100 in both Mathematics and Chemistry. Earned a merit scholarship worth Rs. 5,000. If he had scored just 4 more marks, he would have made the state top-10 merit list. Achieved this with approximately 1 month of board exam preparation — the rest of the year was spent in Kota for JEE coaching.

---

## S3 — JEE Preparation in Kota & the JEE Advanced Crisis (2015–2017)

**✅ CONFIRMED ACCURATE — sourced from career profile, validated by Satvik**

Satvik moved to Kota for two years of intensive JEE preparation. He witnessed firsthand the mental health pressure of that environment — students facing depression and breakdown regularly. This resonated with him given his father's death.

He describes himself as a **slow learner who needs time to build foundations correctly**. In Class 11 he started slowly; by Class 12 he had picked up pace because the basics were solid. Strengths: Physics and Mathematics — logical, practical problem-solving. Weakness: memorization-heavy theory, especially Chemistry.

**The JEE Advanced moment — one of the most defining days of his life:**
During Paper 1, in deep concentration, he forgot to fill in the paper code. He only discovered this when filling in Paper 2 details, when an invigilator pointed it out.

For the next 3–4 minutes, he entered a dark psychological state — vision blurred, hearing compromised, literal darkness in his eyes, ears ringing. Two years of Kota preparation felt destroyed by one administrative oversight.

Then something shifted. He asked himself: *"What is the worst thing that could happen?"* The answer: nothing. He could come back. He told himself: "I came here to give this exam to the best of my ability. That's what I'm going to do today."

He scored 111 in Paper 1, 127 in Paper 2 — but lost ~16 marks due to the psychological disorientation (filling wrong bubbles, errors he'd never make normally).

**Final ranks:**
- JEE Mains: **9713**
- JEE Advanced: **2446** (Top 0.002% of 12+ lakh candidates)

The dramatic jump from Mains to Advanced reflects his strength in deep conceptual problem-solving (Advanced's style) vs. speed-based pattern recognition (Mains' style).

---

## S4 — IIT Delhi: Civil Engineering & Struggle (2017–2021)

**✅ CONFIRMED ACCURATE — sourced from career profile, validated by Satvik**

JEE Advanced rank 2446 got him into IIT Delhi. Civil Engineering was not his choice — it was what his rank could get him at the best college. Relatives convinced him the IIT Delhi environment would matter more than the branch. He chose college over branch and considers it a poor decision in retrospect.

**Academic reality:**
IIT Delhi's Civil Engineering curriculum was heavily theoretical and memorization-based — the exact opposite of his learning style. CGPA: **6.43/10**. Maximum grade in any theoretical subject: 8/10. First semester GPA: 5.3–5.4 — a devastating start that was nearly impossible to recover from over remaining semesters.

**The one consistent strength:**
He scored **10/10 in almost all practical lab courses**. He was the go-to person in his batch for lab reports, practical experiments, and presentations. This pattern — struggling in theory, excelling in practice — became the defining signal of how he learns.

**No campus placements. No internships through IIT placement system.** Only internship was a local civil engineer gig where he observed construction on a B.Ed government college — minimal learnings, got a certificate. No technical projects, no hackathons.

**Hostel:** Udaigiri Hostel, IIT Delhi.

**Extracurriculars:**
- Junior Diploma in Indian Classical Music Vocals — 5 years of training (started by his father in childhood). Also learned Harmonium. Secured Rank 2 in the group song competition organized by Mridang (IIT Delhi music club) across all 12 hostels.
- Secured Rank 2 for Udaigiri Hostel in the Wall Painting competition organized by the Fine Arts & Crafts Club, competing across all 12 hostels.
- Secured Rank 1 three consecutive times in Navratri drawing & sketching competitions in his hometown community.

**B.Tech project:** Geothermal pile foundation for direct heating purposes. By his own admission, he didn't do a great job on it — required for coursework, nothing more.

---

## S5 — Depression & Recovery at IIT Delhi

**✅ CONFIRMED ACCURATE — sourced from career profile, validated by Satvik**

The academic struggle was layered on top of a deeper personal crisis. In first year, after the 5.3–5.4 GPA, Satvik went through a deeply painful personal experience. He had a crush on a girl from his neighborhood back home. They had been in contact, but she suddenly ghosted him entirely — one day they were talking, the next day she blocked all communication with no explanation. This left a deep scar.

He spiraled into depression that lasted 2–3 semesters. He stopped trusting people. Changed his wing in the hostel, moved away from his CE batchmates, found a new roommate on a different floor. He pushed himself into complete isolation. He once told his mother: *"People have friend circles, but I don't even have a straight line. I don't even have two endpoints where I have a friend at the other end."*

He dropped all hobbies, avoided social activities, became a ghost of his former self. He stopped asking for help — which he describes as probably his biggest mistake. Pride, shame, and the belief he had to handle everything alone kept him from reaching out.

**The turning points:**
1. **Samarth** — his roommate, a mechanical engineer who had successfully changed his branch through hard work, was excelling in coding. Hardworking, motivated, and consistently encouraged Satvik to keep working on himself. The only person Satvik trusted during those difficult times.
2. **His girlfriend** — met during an internship, the person he plans to marry in 2027 (both families know, relationship is 6+ years). After years of trust issues, this relationship slowly helped him break down barriers and learn to be vulnerable again. She helped him get out of the insecurity and restored his faith in human connections.

**Why this matters for the career narrative:**
Every story of Satvik excelling — Gold Medal at Sprinklr, solo sprints at AmEx, stepping up when no one asked — is grounded in someone who had to rebuild belief in himself from scratch after real trauma and real failure. That's not a cliché. It's the actual foundation.

---

## S6 — The Gap Year: GATE, ESE & the PwC Decision (2021–2022)

**✅ CONFIRMED ACCURATE — sourced from career profile, validated by Satvik**

After graduating in 2021, Satvik did not immediately enter the workforce. He spent ~10 months preparing for ESE (Engineering Services Examination) and GATE. Goal: PSU job for financial stability. He never took ESE seriously — knew his weakness in theoretical memorization. Primary focus was GATE.

**Family context:** As the only earning-age male in the family (mother + sister Sanika), the weight of financial responsibility was real. Not having a job by 2021 was stressful.

**The PwC decision:**
During this period, PricewaterhouseCoopers offered him a full-time position in real estate dispute consulting — a role seeking civil engineers. He cleared the interview. PwC was offering 6–7 LPA. He declined — he had already committed to GATE preparation and set his sights on PSU positions paying 15–16 LPA. He bet on himself to score high enough. This was a calculated but high-risk decision: IIT Delhi, 6.43 CGPA, no work experience, no internships, declining the only offer in hand.

**GATE 2022 result:**
- Score: 65/100 (68 raw, normalized to 65)
- AIR: ~1463 — Top 1.5% of 100,000+ candidates
- Just 6–7 marks short of PSU interview cutoffs. If he had scored 71–72 normalized, he would have made it — he was confident he could clear PSU interviews. Didn't get the chance.

**Post-GATE pivot:**
PSU path closed. No interest in M.Tech in Civil Engineering. He wanted to go into teaching — a lifelong aspiration inspired by his love for mentoring. But COVID had closed coaching institutes and they weren't hiring. He applied broadly: faculty roles at coaching institutes (₹40,000/month), 9th–10th grade teaching positions, a project manager role elsewhere. Eventually found a work-from-home opportunity at Sprinklr — and took it, not fully knowing what it was.

---

## S7 — Sprinklr: Product Implementation Consultant (Apr 2022 – Apr 2023)

**How I got in:**
Applied through Naukri.com. Wasn't sure what the role was or what my day-to-day responsibilities would be going in. The interview had 6 rounds — they tested me on my CV, some behavioral questions, and one guesstimate. I was only partially able to solve the guesstimate — gave the approach and the formula, but the final answer wasn't perfect. My confidence was good throughout. I genuinely feel I got lucky and Sprinklr took a bet on me. The interview process revealed to me, for the first time after years of depression and academic struggle, that communication was actually my strength — something I had forgotten.

**The Gold Medal:**
In my first 6 months, I received the Global Gold Medal for Implementation Consultants. It was a virtual award announced in a combined quarterly meeting of all ICs across Sprinklr globally. My director presented a slide with my name and my specific achievements — the driver was a 10/10 customer happiness score and multiple customer appreciation emails after project completions. I was not pushing for promotion at all at that point — I was just 6 months in and focused on the work.

**The promotion — and the politics behind it:**
After 11 months, I was the only consultant out of 8 people on my team to get promoted to Senior IC. My manager told me about the promotion the same day he resigned. Here's the full story of what led there:

**December 2022 — the Snapchat situation:**
During winter holidays, everyone else went home and I was the only one left as backup across all ongoing projects. I was managing 18 projects simultaneously at that point. One of those was the Snapchat project which had started December 2nd — they needed an urgent go-live within 4 weeks. I was the lead, and a colleague named Jay was the support consultant.

During a discovery call with the Snapchat client, they shared a Google Doc link that listed all their required use cases. I understood the list right there on the call and told Jay to note it down so we could review it later. Jay was careless and didn't properly review or track that document. Despite this gap, we delivered the project well overall.

**The review call — where it went wrong:**
A few months later, project reviews were happening. In one such call, my manager and the VP were present along with the rest of the team. The success manager had, by this time, added that original Google Doc to Snapchat's shared Google Drive. My manager spotted it on the call and started using it to defend my work — assuming we had followed it throughout the project.

But the VP was using this call specifically to call me out and make me a "bad example." While my manager was defending me with this document, I genuinely could not recall that document in the moment — Jay's negligence had meant we never properly worked with it — and I blurted out: "I am seeing this document for the first time."

The moment I said that, it looked like my manager had been lying to defend me — like he was clutching at straws. The VP now believed my manager was covering for me with no real basis.

**The fallout for my manager:**
The VP, instead of promoting my manager, gave a double promotion to another manager (from the Insights & Analytics team) and told my manager to report to that person — effectively demoting him in the org chart. My manager, who had been advocating for me and took the political hit for my mistake, decided to quit.

**What my manager did before leaving:**
Before putting down his papers, my manager made sure my promotion to Senior IC was processed and finalized. He got me promoted first, then resigned. I found out about my promotion and his resignation on the same day.

**What this taught me:**
Organizations run on perception as much as performance. In that call, the truth was nuanced — we had delivered the project well, Jay had dropped the ball on the document, and I hadn't lied — but the optics of me saying "I'm seeing this for the first time" in front of the VP destroyed my manager's credibility. Good work alone doesn't protect you or the people advocating for you. Visibility, documentation, and knowing the political landscape of a room matter enormously.

**Adobe — data unification and spam model:**
I worked on the Adobe account alone. The data was coming from 3 sources, each with completely different schemas and metrics:
- Earned: social listening data
- Organic: Adobe's own brand social media posts
- Paid: paid posts and ads

Previously, each analysis cycle was taking 4 days of manual work. I unified all three sources using SQL and built data pipelines to automate the analysis — bringing it down to 1 day effort (75% reduction). This was actual hands-on SQL and pipeline work, not just defining requirements.

For spam detection: I built a spam detection model for Adobe using Sprinklr's internal product called **AI Studio**. AI Studio is a no-code/low-code ML platform with a UI — you annotate and tag messages through the interface, and the model learns to predict categories on its own. I did NOT write Python or custom ML code for this. I configured the tool, did the annotation work to train it, and validated the outputs. The model achieved an F1 Score of 87%. The credit here is in understanding what "spam" meant for Adobe's use case and doing the data labeling correctly — not in writing code.

**Other client work (S7 period):**
- **Snapchat**: Increased month-over-month brand engagement by 15% in the music, sport, and fashion segments by analyzing user behavior and recommending engagement strategies.
- **Discord**: Reduced brand reputation risk by 25% by building a custom AI-based detection system for identifying hate comments on Discord servers. ✅ CONFIRMED: Built using Sprinklr AI Studio (same tool as Adobe spam model — no-code annotation-based ML). Same workflow: annotate/label hate comments through the UI, model learns to classify, Satvik did the labeling and validation. Credit is in understanding what "hate" meant for Discord's brand context and building the right golden dataset for it.
- **Mars Inc.**: Recommended product strategies by identifying trends across the Top 10 high-performing and low-performing products in their portfolio.
- **Case response rate**: Improved case response rate by 10% across customer care cases by creating AI-powered automated workflows for skill-based routing.

**Emotional reality:**
This was the first job I had ever held. Coming from an IIT with a 6.43 CGPA, no campus placements, no internships (except a local civil engineer gig), I had massive self-doubt. The Gold Medal in 6 months was personally huge — it was proof that I could be excellent at something when given the right environment. The depression and isolation from IIT had made me forget I was capable. This period rebuilt that belief.

---

## S8 — Sprinklr: Senior Product Implementation Consultant (Apr 2023 – May 2024)

### S8a — Qatar CGB Project (Full Context)

**The deal:**
Project name internally: CGB — Civil Services & Government Development Bureau of Qatar.
Deal size: $6.2M ARR / $32M TCV / 5-year agreement. Announced January 30, 2023. At the time, the largest net new deal Sprinklr had ever signed. The deal was closed by the sales and pre-sales team (Cyril Abi Nader, Haitham Elkhatib, Dina Masri etc.) before Satvik's involvement. Satvik was brought in as the implementation resource.

Satvik was NOT on the sales team. He was brought in as the **Sprinklr Insights consultant** for all 5 Sprinklr Insights products on this project. His role was implementation and delivery — not deal-making.

**"Sharek" — what it actually was:**
"Sharek" was the Qatar government's pre-existing citizen feedback initiative — not something Satvik named or built. The Sharek initiative was already defined by Qatar's CGB to capture citizen feedback and improve public services. Sprinklr was the tech platform being implemented to power it. The mobile app was an EXISTING Sprinklr mobile application that was modified and customized for the Sharek initiative branding and use case.

**Satvik's actual role on the mobile app:**
The AVP of Product Management at Sprinklr, Manish Pandey (named in the deal announcement email), asked Satvik to help test, QA, and design the customized version of the Sprinklr mobile app for the ministers of the Prime Minister's Office of Qatar. Satvik was NOT talking to engineers directly — someone else handled that communication. He was involved in discussions and meetings.

**Honest self-assessment:** Satvik says he "prefers to say product owner since it sounds more impressive." The reality: he was functionally acting as a product owner for the mobile experience — owning the QA, testing, design decisions, and ensuring the customization met the ministers' needs — but his official role was Insights Consultant.

His primary focus on the mobile app:
- Making dashboards and widgets presented to the Prime Minister and other ministers easy to understand
- Building a coherent story from the data
- Giving actionable insights about ministry performance
- Arabic localization (RTL adaptation) of the entire interface
- The app was an iOS app

**The Reverse-KT onboarding process:**
Satvik did NOT invent the Reverse-KT methodology. He learned it from his first manager at Sprinklr, Keerti Rondla, in his very first month on the job. When 13 new consultants joined the Qatar project team, he applied this same process to onboard them. He:
- Recorded each session
- Collected all feedback and open questions
- Maintained a shared repository accessible to the entire team
- Spent approximately 4+ extra hours per week planning, organizing, and running these sessions alongside his regular project work

**The 120 dashboards — real breakdown:**
- Satvik created a **base template** for the dashboards
- Taught his team of 8 the step-by-step customization process
- Distributed the build effort across the team
- **He personally reviewed every single dashboard** for filters, tags, and sharing permissions
- All dashboards were in Arabic
- Each ministry had customized dashboards — not identical copies
- The 4-week timeline was aggressive but achievable because of the template + process he designed

**Numbers confirmed:**
- Team size: started at 6, scaled to 14 in 3 months
- Satvik onboarded **8 consultants** (not 13) as the team scaled 6 → 14
- Of those 8, approximately 6 were near-peers who joined within 3-4 months of Satvik — he was senior to them but they weren't pure juniors; the remaining few were actual juniors whom he fully trained, onboarded, and mentored
- Led a team of 8 to deliver 120 dashboards across 40 ministries in 4 weeks
- 7-day retention improved from 40% → 55%
- Time-to-insight reduced from 2 days → 2 hours
- Sentiment model F1 improved by 11%, Intuition model by 13% (for Arabic language validation)
- Qatar's UN E-Government Development Index rank improved from 78 → 53 (25-position jump) — this was a country-level outcome, not solely Satvik's contribution, but the platform Satvik implemented was part of the infrastructure that enabled it

**What the deal email confirms:**
The email from January 30, 2023 is a real internal Sprinklr announcement. Satvik has a copy forwarded to himself. The deal figures ($6.2M ARR, $32M TCV, 5 years, 40 entities) are confirmed. Manish Pandey and Anish Singhal (VP of Product, who later saw Satvik's Walmart work) are both named in the email as part of the product leadership team involved in this win.

### S8b — Walmart Spark Driver Support

**What Satvik actually did on this project:**
This was not a pure analysis project. Satvik was functioning as the de facto project lead and PM — without the title. He was working with a cross-functional team that included product analysts, engineers, pre-sales solutions consultants, and account executives. His actual work:

- **Running daily sprints**: posting daily progress on action items in the team's common group, keeping everything aligned and unblocked
- **Configuring Data Pipelines**: This is a specific Sprinklr product. Using SQL joins and data transformation logic to combine multiple raw data sources (in-app reviews, app store reviews, NPS surveys, voice call transcripts, support emails, support chat exports, public social media including Reddit/Twitter/Facebook) into unified reports. This required hands-on technical configuration, not just defining requirements for others.
- **Engineering escalations**: When issues arose with the product configuration or data pipeline, Satvik was directly escalating and resolving these with engineers and product analysts/APMs on the team — not waiting for a PM to do it
- **Client requirements ownership**: He owned the requirements gathering from Walmart, the schema design, and the architectural design of the entire solution — from raw, chaotic, multi-source data to structured, actionable root causes
- **Insights Assistant (ML product)**: The root cause analysis was calculated by Sprinklr's "Insights Assistant" — an ML product. Satvik configured this product and worked with its outputs
- **Live presentations and displays**: He designed and configured live dashboards and display screens that were presented to the Walmart team
- **Leadership updates to Anish Singhal**: Satvik was personally leading the updates to Anish Singhal (VP of Product at Sprinklr). This is how Anish came to know him.

**The Anish Singhal conversation — the real story of how the PM door opened:**
Anish saw Satvik's work, ownership, and groundwork through the Walmart leadership updates. He was impressed enough that one day he scheduled a call directly with Satvik and asked him: "Do you want to be in the product team, and why?"

The context behind that question: Anish's main PM was about to go on maternity leave. He had a product (what became the Use Case Hub) that needed someone with deep hands-on configuration knowledge and implementation knowledge — not a traditional PM who would need to be ramped up on the product. He wanted Satvik to lead it.

This was NOT a formal PM promotion process — it was Anish handpicking Satvik because he had a specific need and Satvik had the right skills at the right time.

**The Black Friday pilot — confirmed details:**
The automation was complete: data pull, ML tagging (supervised + unsupervised), analysis — all automated and connected to live displays and presentations Satvik had built. The system was surfacing insights in real time on its own.

The WhatsApp group had 10–12 people:
- Walmart side (5–6): VP, Director, Senior Managers
- Sprinklr side (5–6): APMs, ICs, Project Manager, VP, 2 Solution Consultants, 1 Account Executive

Satvik's role in the group: he was pulling screenshots from the dashboards as insights "sparked up," sending the highlights into the WhatsApp group, AND interpreting and narrating what they meant. The machine surfaced the signals; Satvik was the human intelligence layer translating them into business meaning for Walmart leadership in real time.

**Revenue numbers — source confirmed:**
Numbers came from the AE and Solution Consultant on the project who had these figures on their decks. Satvik did not calculate them himself.
- $1.2M TCV from POC-to-deal conversion — confirmed by AE/SC
- $9M+ pipeline opportunity for Q4 FY24 — confirmed by AE/SC
- $2M "Last Mile Delivery" deal (signed after Satvik left): friends still at Sprinklr told him after the final approvals from Walmart leadership came in

**Driver retention data (confirmed):**
- D7 retention: ~65%
- D30 retention: ~35%
- D60 retention: ~18%
- Pre-analysis contact volume: 100K+ contacts
- Time-to-insight went from 7 days (old manual process) → same-day delivery

**The L1/L2/L3 taxonomy:**
Satvik designed a custom three-level issue taxonomy. The specific structure and what it covered needs to be confirmed — but it was designed to categorize root causes from broad (L1) to specific (L3) and was built as a unified data architecture joining internal support data with public social escalation data via SQL backend joins.

### S8c — Use Case Hub

**IMPORTANT CORRECTIONS vs. existing career profile:**
Several things in the existing profile are overstated or inaccurate. Everything below is the real version.

**What the Use Case Hub actually was:**
An internal Sprinklr product that increased adoption of the Social Listening module specifically, targeting small and medium enterprise clients with less than $1M ARR. It allowed clients to self-serve setup using industry templates instead of requiring a full manual implementation.

**The "Listen Learn Act" framework:**
This was NOT Satvik's original invention. It is how Sprinklr's product was already structured. He did not conceptualize it from scratch. The existing career profile overstates this. This claim should not appear in Layer 3.

**Satvik's actual role — the honest version:**
Satvik joined this project as a **Product Analyst** — not as the PM. This was his first time ever:
- Observing product team + engineering team discussions
- Giving standup updates to product team members about what he planned to work on
- Working inside the PM + engineering rhythm (PRDs, sprints, grooming)

**Surabhi Goyal was the actual PM.** She:
- Wrote PRDs
- Acted as the Agile Champion
- Led engineering team connects

When Surabhi went on maternity leave, the entire expectation shifted suddenly to Satvik — do everything she was doing, immediately. No ramp. No additional compensation. He was thrown in the deep end.

**What Satvik actually contributed:**
- Product strategy input and roadmap conversations
- Feature prioritization discussions
- Product planning and grooming sessions
- QA work
- Analysis of the 1,500+ existing client dashboard repository (15 industries × 10 sub-verticals × 10 use cases) — he personally reviewed patterns, not each dashboard deeply, but enough to understand what templates existed and why, to inform the Use Case Hub structure

**Use Case Hub metrics — updated status (product IS now live):**
Product was not released before Satvik left, but it IS live now (~2 years post-launch as of May 2026). Sprinklr teammates who stayed after Satvik left shared outcomes with him.

**What teammates confirmed (directional, not precisely measured by Satvik):**
- Product became the **primary entry point for the dashboard creation journey** on the entire Sprinklr platform — the most visited area on the platform
- Adoption directionally ~35% → ~85% — directional estimate from teammates
- TTV reduction directionally ~75% — directional from teammates
- 15 industry verticals enabled for self-serve — plausible given template work done

**Source:** Sprinklr teammates who remained after Satvik left. Same credibility as Walmart revenue numbers. Not self-measured but from people on the ground.

**Interview answer if asked "how did you measure this?":**
"I had moved to AmEx by the time the product fully launched, but teammates who stayed shared the impact — the product became the primary entry point for dashboard creation across the platform, which was exactly the goal we'd built toward."

**What IS precisely true regardless:**
- He stepped into PO + PM responsibilities after Surabhi went on maternity leave
- His title was Senior Product Analyst but doing Product Owner and PM work
- He analyzed 1,500+ client dashboard patterns across 15 industries
- He contributed to product strategy, roadmap prioritization, sprint grooming, QA
- The product targeted SME clients under $1M ARR on the Social Listening module

**The dual-role period and burnout — the real story:**
The dual role (Senior IC in US time zone + product team in India time zone, 9 AM to 3 AM days) lasted approximately **6 months**. Satvik was absorbing both silently, waiting for an internal transition to be formalized. No one explicitly acknowledged how much he was doing.

When the internal transition finally happened, Satvik made a mistake he still thinks about: **he undersold himself.** He asked for a "Senior Product Analyst" title — when he should have asked for APM (Associate Product Manager). Because he asked for less, he got exactly what he asked for — a dry title change with no salary increase, no extra compensation.

He felt thrown under the bus. Expectations were enormous, there was no time to learn properly, and he was doing two full jobs for the salary of one with the recognition of neither. Over time, this led to **bad burnout**.

When he applied for 1–2 months of leave, leadership perceived it as a potential resignation risk. Only then — when they thought he might leave — did they give him the Senior Product Analyst title officially. The title came as a retention move, not as genuine recognition.

**Why this matters for the career narrative:**
This is a real and painful story of someone who delivered extraordinary work, undersold himself at the negotiating table, got burned out doing it, and ultimately had to leave to get the recognition elsewhere. It explains why he left Sprinklr and why he took the AmEx role seriously from day one.

---

## S9 — Sprinklr: Senior Product Analyst & Final Months (May 2024 – Jul 2024)

**The Advocacy team — the real version:**
After the burnout from the Use Case Hub dual-role period, Satvik thought he'd transfer to a different product team and get some breathing room — a chance to learn at his own pace without being thrown in the deep end. He moved to the Advocacy team for the last 1–2 months.

That slower pace never materialized. He didn't get time to breathe or learn properly there either.

**What he actually did on Advocacy:**
He put together a product strategy document — covering five business pillars, a competitive landscape analysis, and a quarterly feature roadmap for FY25. He presented this to his VP.

**Honest self-assessment (his own words):** "Maine ye jo product strategy & roadmap ka likha hai wo bas yunhi likh diya tha thodi PM level ki ownership bolne ke liye, maine is new team me jyada kuchh kiya nhin tha by the way." Translation: He wrote the strategy document casually, mainly to have something PM-level to show. He didn't actually do much in that team.

The $7M → $9.8M ARR figures, $400–700M market size, 9–10% CAGR, the competitive analysis against FirstUp/EveryoneSocial/etc. — these were in the document he put together but were desk research, not original analysis he personally validated.

**Why he left:**
A better offer came — American Express. He took it. The Advocacy team work was not a meaningful chapter; it was a transitional period while he was already looking for the exit.

**Title timeline clarification:**
- Senior Product Analyst title was given as a retention move when he applied for leave (burnout)
- The title came ~5 days before his second AmEx interview
- He left Sprinklr in July 2024

---

## S10 — American Express: Senior Associate Product Manager (Jul 2024 – Present)

### S10a — Joining & First Assignment (Vendor Evaluation)

**⚠️ MAJOR CORRECTION vs. existing career profile:**
The career profile describes Satvik as having "led the entire vendor evaluation end-to-end" from July–September 2024 (or February–August 2024 per the interview story). **This is incorrect and overstated.**

The vendor evaluation (Build vs. Buy for the CRR platform) was done by **Satvik's manager**, before Satvik joined AmEx or during the very early onboarding period. Satvik was given basic context about it but was not deeply involved. He does not know much about the details of the evaluation even now.

**His own words:** "thoda senior dikhne ke liye maine likh diya tha" — he wrote it in the career profile to appear more senior.

**The interview story in the career profile** ("I led the entire evaluation — 15+ vendors down to 8, to 3, to 2 finalists: NICE Actimize and Symphony AI…") is therefore also **not a story Satvik can tell in an interview** as his own. It belongs to his manager, not him.

**What Satvik actually did when he joined (July 2024):**
He was placed on the AML Customer Risk Rating (CRR) team. His first real assignment was understanding the product end-to-end — gaining domain knowledge in AML risk scoring, understanding the existing BRD (Business Requirements Document with 21 requirements), and beginning to build the foundation for the CRR modernization program.

He was the only PM/PO on the team when he joined — double-hatting as both strategic PM and execution-focused PO from day one, with no manager supervision initially. The team was understaffed.

### S10b — CRR Platform Build (Jan 2025 – Mid 2025)

**The "10 sprints single-handedly" — confirmed true:**
For the first 10 sprints of execution, Satvik was the only PM/PO on the CRR platform. He was genuinely managing the entire scope alone — all product ownership, all sprint planning, all backlog management, all cross-functional coordination.

**Pallavi joining and the split:**
After those 10 sprints, a Senior Manager of Product Management named **Pallavi** joined the team. Responsibilities were divided:
- **Satvik:** Platform UI, backend, and customer user journeys
- **Pallavi:** Data requirements

This split is important for accurately describing the scope — Satvik did not own the full product end-to-end for the entire time, only for the first 10 sprints. After Pallavi joined, his ownership was the UI/backend/user journey portion.

**Leadership in Action Award — correct version:**
The award came as:
1. A callout at a VP meeting
2. A certificate by email
3. Blue rewards (6,000 Rs worth) from his VP

**✅ CONFIRMED:** Award was given by Nerses Kazarian, SVP of Risk Management. Career profile is correct on this.

**What the award was for (confirmed):**
- Taking ownership of the CRR modernization program
- Delivering a 3-year roadmap with prioritization

**Performance ratings (confirmed):**
- First year: G3L2 (above standard G3L3) → 40% higher bonus
- Most recent cycle: G1L2 → 120% bonus increase
- ✅ CORRECTED: Highest rating among ~12–15 Band 30 level Product Owners in Gregory Liss's org. "Band 30" is a salary band level at AmEx — NOT a cohort of 30 people. The career profile's phrasing "30 Band-30 Product Owners" was misleading. Correct framing: "highest-rated among Band 30 Product Owners in the VP's org (~12–15 people)"
**People Leadership at AmEx — full picture:**
- **Direct report:** Shivani (UX Designer) — reports directly to Satvik, hired through 12-round competitive selection, managing her for 6 months
- **Informal mentorship:** 3 Product Owners who joined after Satvik (Tahcin, Suprana, Sakshi) — he mentored them unofficially, gave feedback, helped them grow. Not formal direct reports but real mentorship investment.
- **Scrum team leadership:** Led an 18-member scrum team (engineers, data engineers, QA, POs, UX) — leadership by influence and feedback, not by authority. Helped team members improve through right feedback at the right time.
- This is substantial people leadership for a 4-year PM. Most PMs at this level have no direct reports and no team management experience.

### S10c — Strategy Pivots & Crisis Management

**✅ CONFIRMED ACCURATE** — everything in the career profile is correct. Key facts:
- **Pivot 1 (end of PI 25.2):** Methodology change — business reversed from new simplified scoring to legacy "Cadence" logic. Simultaneously, timeline shrunk from 2-year full modernization to 1-year lift-and-shift (just enough to decommission Cadence). Satvik reprioritized entire backlog within 1 week.
- **Pivot 2:** CDL data layer underperformance by a supporting team → decision to stop CRR platform build and pivot to fixing the data layer (Consolidated Data Layer) first. CRR MVP had reached staging/QA but was never pushed to production.
- Both pivots are genuine and verifiable experiences.

### S10d — CDL Strategy (Current Project)

**✅ CONFIRMED ACCURATE** — everything in the career profile is correct. Key facts:
- Problem: DAM (Data Access Manager) layer delivers only fractionally standardized data; raw SOR values cannot be used by CRR rules
- Product Type: 136,738 raw records → 12,408 standardized → 64 categories (2,137:1 compression)
- Industry Type: 521,583 raw → 42,182 standardized → 98 categories (5,322:1 compression)
- 5-step pipeline: Translation → Standardization → Categorization → Derivation → Master List
- 54 data points scoped; P1+P2 = 21 data points covering 58% of risk elements
- Execution roadmap: 85.3% coverage by end of PI 26.5 (Individual portfolios); 96.5% by PI 27.1 (Entity portfolios)
- Currently Phase 0 (pre-standardization discovery)
- Three-bucket framework Satvik created: Discard & Rebuild / Educate Business / Transform
- Cross-references currently maintained manually in Excel — Satvik's strategy automates this

### S10e — Side Achievements at Amex (Growth Hack, Negative News Agent, AI Adoption)

**Growth Hack — confirmed accurate:**
Everything in the career profile is correct.
- 2-day innovation event, January 2025
- Led a 6-member team (Satvik was the captain/leader)
- Built an AI Backlog Grooming bot — Slack-integrated, connected to Rally (Amex's project management tool), auto-generated user stories and product features using AI
- Ranked #21 out of 400+ teams — Top 6%
- The concept was later productionized by GMNS (Global Merchant and Network Services) as "QE Assist"

**Negative News / Adverse Media Triage Agent — ⚠️ CORRECTION:**
The career profile says Satvik "was given a stretch role on the Negative News and Adverse Media Triage Agent project — integrating Work Fusion's EvantAgent into the financial crimes platform."
**Real version:** Satvik supported this project. He did not own it or lead it. It was someone else's project. He played a supporting role.
→ **Do NOT present this as a project Satvik owned or led. Remove ownership language from Layer 3.**

**ChatGPT Enterprise / AI Adoption — confirmed accurate:**
- Drove ChatGPT Enterprise adoption within his team
- Achieved 80% AI-assisted story drafting for sprint planning and backlog management
- This is correct and usable.

---

## S11 — GoGoGo Startup Involvement (Sep 2024 – Jun 2025)

**What Satvik actually did — ENRICHED version (May 2026):**
Started as a side hustle. Involvement spanned multiple phases:

**Phase 1 — Early building (pre-launch):**
- Helped think of the name and spread the word around the GoGoGo brand
- Created initial designs, initial posters, and initial logos
- Helped onboard founding team members
- Created a driver welfare group — community infrastructure for driver relationships
- Active role in driver acquisition phase
- Brainstormed and actively contributed ideas in initial strategy building phase

**Phase 2 — Go-to-market and fundraising:**
- Pitched GoGoGo to investors (productivity consulting firms and others)
- Attended **Startup Mahakumbh** to preach GoGoGo's vision and meet the ecosystem
- Attended **StartupTech Summit, Bangalore** to spread the word around GoGoGo's vision
- Led content and brand marketing: LinkedIn automation, content copywriting, content creation
- Created an **AI anthem (AI-generated song)** for GoGoGo — used in their marketing and GTM
- Created **AI videos** for marketing and promotional material
- Created design artifacts for the brand

**Phase 3 — Advisory and investment:**
- Angel investor: received equity in GoGoGo
- Product advisor: reviewing product strategy and giving feedback
- Helped the founder and business navigate a period of deep financial difficulty (confirmed by user May 2026 — was previously marked unverified; now confirmed to have happened, but do not use in resume/professional context)

**Chief of Staff — the real story:**
The founders wanted to bring Satvik on as Chief of Staff. This was announced publicly — the founders posted on LinkedIn with his photo and name titled "Chief of Staff." But in reality, the role was never formalized. It "hote hote reh gayi" — kept getting delayed and never actually happened.
→ **Chief of Staff is NOT a title he held in practice.** It was announced but not operationalized. Do NOT use this title anywhere.

**Compensation:**
Equity in GoGoGo. No formal salary.

**Events attended on behalf of GoGoGo:**
- Startup Mahakumbh (in-person, pitched GoGoGo vision)
- StartupTech Summit, Bangalore (in-person, promoted GoGoGo brand)

**Current status (as of May 2026):**
Satvik left GoGoGo around June 5, 2025 but remains on bi-weekly board calls. The startup is operational in Indore, expanding to other cities including Vadodara. ~Rs. 2.5 crore raised (pre-seed). About 5 months of runway remaining. No VC interest in ride-hailing currently.

---

## S12 — ContentStack: AI Product Manager (Nov 2024 – Jun 2025)

**Engagement model — confirmed:**
Part-time freelance AI PM. Paid consultant. Not an employee. Concurrent with AmEx full-time role.

**Products built (3 AI products):**
1. **Compose AI** — AI content creation tool (LinkedIn, Twitter copywriting optimization)
2. **DesignerAI** — AI website creation tool
3. **Lens** — Website performance monitoring tool

**What he actually did — ENRICHED version (May 2026):**

**PRD and product strategy:**
- Wrote PRDs for all 3 products
- Defined and maintained the product backlog
- Contributed UX ideas to build the best possible AI content/website creation platform
- Competitive benchmarking: studied 10+ competitors per product domain

**AI features launched (6 total):**
1. **AI Ghost Writing** — automated long-form content generation
2. **Quick AI Edit** — inline AI editing for existing content
3. **AI Embedding** — embedding AI into existing content workflows
4. **Word Replacement** — AI-powered word swap/optimization
5. **GEO (Generative Engine Optimization)** — optimizing marketing content to surface in LLM-powered search (Perplexity, Google Gemini, ChatGPT search, etc.) — the SEO equivalent for LLMs
6. One more feature (not recalled by name)

**LLM evaluation and quality:**
- Conducted LLM evaluations — tested and judged LLM output quality for mistakes and errors
- Ran A/B testing on designs — captured feedback from multiple stakeholders, conducted surveys
- Shared copywriting best practices for LinkedIn, Twitter
- Worked on prompt engineering for AI features
- Built/configured agent tech workflows

**Design:**
- Created wireframes hands-on for the products

**He did NOT write code.** His role was product strategy, feature definition, LLM evaluation, UX, and execution delivery.

**Team size:** 1 developer + 1 designer.

**This is legitimate concurrent PM experience** — he was doing real PM work at ContentStack (freelance) while holding his AmEx role. Worth including in Layer 3 as proof of AI PM breadth, LLM eval depth, and GEO/AI content domain knowledge.

---

## S13 — Miraya Media House (2024 – Present)

**Real version:**
Satvik contributes almost nothing formal here. Occasionally advises his sister and her boyfriend on CRM, hiring, innovation, and scaling. It is their side business — doing ~₹2–3 lakh/month revenue.

**Resume relevance:** None. This is informal family involvement. Do NOT include in Layer 3.

---

## S14 — Masters Union Decision & LinkRight (2025 – Present)

**Masters Union decision — confirmed accurate per existing profile.**

**LinkRight — real version:**
Started as a side hustle and passion project. Initially others were involved but they all left ("sab akele chhod gaye") and Satvik ended up building it alone.

**Current honest status:**
- **Revenue:** Zero. No revenue currently.
- **Users:** Only Satvik himself. No other users.
- **Stage:** Passion project / working product in development. Not a startup with customers.

**What IS real about LinkRight:**
- The technical depth is genuine — LLM pipelines, fabrication guards, evaluation frameworks, CLI ergonomics, PyPI publishing, Oracle VPS with 9 models, hybrid parsing architecture. All of this is real and demonstrable.
- Published on PyPI: `pip install linkright` works globally
- Live at sync.linkright.in
- 44 of 57 issues shipped (77%) solo over 11 months while holding a full-time AmEx role
- The vision (career navigation OS, career memory graph) is coherent and well-documented in the Roadmap_Linkright folder

**How to frame this honestly:**
Not a startup with traction. A deeply serious passion project that demonstrates technical PM ability, AI product thinking, shipping discipline, and solo execution — things that are real and verifiable. Don't overstate it as a "company" or imply there are users/revenue when there aren't.

---

## S15 — Voluntary Work: Sukha Education (Jan 2025 – Apr/May 2025)

**✅ FULLY CONFIRMED ACCURATE — additionally enriched from the GGI Impact Lab final deck (uploaded May 2026)**

**The client:** Sukha Education Foundation, Chennai. NGO teaching communicative English to underprivileged children — 2,000+ students, 25+ partner institutions, 50+ volunteers.

**The problem:**
Fragmented operations across three dimensions:
- Lesson plans shared via WhatsApp, no structured repository
- Volunteer data scattered across disconnected spreadsheets
- Communication siloed — no shared channel, no visibility across the volunteer network
- Result: ~40% volunteer churn. People weren't leaving because they didn't care — the system made it too hard to stay engaged.

**Satvik's approach — three-pillar digital transformation strategy:**
1. **Google Workspace** — Powering productivity. Shared drives for lesson plans and teaching materials, Google Sheets for attendance tracking, Google Meet for professional communication.
2. **Slack & Workflows** — Smarter collaboration. Slack bots for automated attendance marking, real-time class updates, peer support channels, volunteer engagement features (leaderboards, appreciation automation).
3. **Salesforce CRM** — Data-driven growth. Impact dashboards for donors and partners, role-based access, impact tracking, automated reporting. (Zoho evaluated as interim option and documented with feature comparison.)

**Deliverable structure (from the deck):**
- Executive Summary with cost-of-inaction analysis (the source of the ₹60,000 annual savings figure — calculated from manual overhead, volunteer churn cost, and coordination inefficiency)
- Stakeholder mapping: Volunteers, Donors & Partners, Sukha leadership — each with distinct tool-benefit mapping
- Risk mitigation framework covering: user adoption resistance, data integrity, scalability, technical challenges, engagement drop-off — with specific mitigation strategies for each
- Change management section
- Phased 12-week execution roadmap:
  - **Weeks 1–4:** Foundation & Training — stakeholder onboarding, governance setup, training on all three tools, data protocols
  - **Weeks 2–8:** Pilot & Refinement — test Slack bots, pilot lesson plans + automated scheduling, feedback loops
  - **Weeks 9–12:** Full-Scale Deployment — expand across all staff and volunteers, integrate Salesforce, automate attendance/lesson plans/reporting
  - **Week 12+:** Optimization & Scaling — Salesforce + Slack analytics monitoring, process improvement, long-term digital strategy

**Outcomes:**
- ~₹60,000 annual cost savings (confirmed)
- 50+ volunteers onboarded onto the new systems
- 12-week phased rollout completed
- Full consulting-grade deck delivered to the Sukha team

**Framing note:** This was done as a GGI Fellow (GGI Impact Lab program) — the Fellowship was competitive, consulting-style, included stress interviews and mentorship. The Sukha project was the Impact Lab component. Satvik graduated as **GGI Fellow 2024**.

---

## S16 — Navii / HeyNavii: Beta PM Engagement (End of 2025, ~1 Month)

**Real version:**
Unpaid beta tester + Growth PM role (~1 month) for Navii (also known as HeyNavii), an AI-powered career navigation app. Satvik did structured product feedback work — not just casual usage.

**Specific deliverables confirmed:**
- Documented **14 bugs** across the product
- Identified and logged **9 product enhancements**
- Mapped **5+ distinct user journeys** across key flows
- Wrote **Scribehow onboarding guides** + onboarding videos for user flows
- **Built N8N automations** (workflow automation pipelines)
- **Built Chrome extension(s)** for the product
- Explored **AI/UGC content automation** and **AI Image/Video generation pipelines** (AI Influencer angle)
- Managed / moderated the **job-seeker community** (user base engagement)
- Conducted **user interviews and surveys** for product feedback
- Navii user base grew from **~2K → ~20K users** during Satvik's beta engagement period (**cannot take full credit** — growth had multiple contributors)

Navii initially wanted to hire him as a growth hacker / Growth PM but never reinitiated the conversation after the beta engagement ended.

**Resume framing guidance:** Lead with the 2K→20K growth metric (framed as "during beta engagement" to avoid overclaiming). Mention N8N automations + Chrome extension as concrete technical deliverables. Include 14 bugs + 9 enhancements for structured QA signal. User interviews / surveys show VOC discipline. Do NOT claim full ownership of the 20K growth.

**Resume relevance:** Borderline. The numbers (14 bugs, 9 enhancements, 5 journeys, Scribehow guides) now make it defensible for a Ventures & Advisory or Projects entry, especially for Growth PM or early-stage PM roles. Strongest framing: "Beta Growth PM — documented 14 bugs + 9 enhancements across 5+ user journeys; wrote Scribehow onboarding guides." Do NOT include unless explicitly relevant to the target role or there is space to spare. Unpaid and short duration.

---

## S17 — Mentorship Legacy

**✅ FULLY CONFIRMED ACCURATE.** Both major stories are real:

**Sister Sanika:**
- Satvik guided her JEE prep — she made it to IIT BHU (Electronics & Communication Engineering)
- Only girl from IIT BHU to get a Google internship; topped girls' category in ECE with 9.2/10 GPA
- Reached final waitlist at Confluent (6th round), competing against CS graduates
- Now Senior Software Developer at Oracle

**Junior colleague (laid off from Sprinklr):**
- From poor farming family in Rajasthan; educated at Jawahar Navodaya Vidyalaya and Super 30; NIT Warangal graduate
- Came to live with Satvik after Sprinklr layoff
- Satvik provided 3 months of intensive mentorship — PM, data analytics, interview skills, communication
- They gave 15–20 interviews together
- Secured APM role at Next Wave without being unemployed for a single day

---

## S18 — Skills & Tools

All skills below are drawn from confirmed, validated project work across S7–S16.

**Product Management:**
- Product Strategy, Roadmapping, Prioritization (RICE, MoSCoW), PRDs — used at AmEx and Sprinklr product work
- OKR/KPI definition, Feature prioritization, GTM strategy — AmEx CRR program
- Stakeholder management, Cross-functional collaboration — Qatar (40 ministries), AmEx (global teams), Walmart (VP/Director level)
- Product lifecycle management — Use Case Hub, CRR platform end-to-end
- SAFe / Agile (PI Planning, Sprint ceremonies) — AmEx
- UX Research (20+ sessions at AmEx), Figma (wireframes for Asset Manager, Rule Builder, Sandbox UI)
- A/B testing — Sprinklr

**Data & Analytics:**
- SQL (production-grade: Walmart data joins, Adobe pipeline unification, Sprinklr Data Pipelines configuration) — confirmed used in real work
- Python (data preprocessing scripts for Walmart, ML pipeline scripting for LinkRight) — confirmed
- BigQuery, Tableau, Mixpanel, Amplitude, PowerBI, MS Office — confirmed in profile
- Data architecture design (schema design, unified data layers) — Walmart, CDL strategy at AmEx

**AI / ML:**
- LLM pipeline design and evaluation (LinkRight — production work, confirmed)
- Prompt engineering with fabrication guards (LinkRight)
- Supervised and unsupervised ML (Sprinklr Insights Assistant configuration — Walmart)
- AI Studio (Sprinklr no-code ML annotation tool — Adobe spam model F1 87%, Discord hate detection -25% brand risk). **Confirmed both models built via AI Studio.**
- **What Satvik actually knows about model building (beyond Python coding):** bias-variance tradeoff (underfitting vs overfitting), all core performance metrics (accuracy, precision, recall, F1, AUC-ROC — and when to use which), validation workflows (train/val/test splits, cross-validation), retraining triggers and cadence, sampling strategies (class imbalance handling, stratified sampling), golden dataset principles (what makes a good labeled dataset, annotation guidelines, inter-annotator agreement). This is real working knowledge, not theoretical — it comes from configuring, validating, and retraining these annotation-based models hands-on.
- Sentiment analysis / NLP (Arabic models — Qatar; hate detection — Discord)
- Embedding + retrieval systems (LinkRight career memory graph)
- Self-hosted LLMs on Oracle VPS (LinkRight)

**Engineering-adjacent:**
- Data Pipelines configuration (Sprinklr product — SQL joins, data transformation)
- API concepts (LinkRight FastAPI backend)
- N8N workflow automation (Navi internship, LinkRight Broadcast)
- CLI design (LinkRight — Click-based, published to PyPI)

**Design & Prototyping:**
- Figma (AmEx: rule builder UI, Asset Manager, Sandbox Versioning — full screen designs)
- UI/UX design fundamentals — confirmed across multiple projects

**Collaboration Tools:**
- JIRA, Trello, Lucidchart, Rally (AmEx's PM tool), Slack, ChatGPT Enterprise

---

## S18b — Certifications & Programs

**✅ CONFIRMED — both real, both worth including on resume if space allows**

1. **GGI Fellow 2024 — Global Governance Initiative**
   - Pre-MBA consulting and public policy fellowship. Competitive cohort-based program — consulting-style papers, stress interviews, mentorship from practitioners, case-based learning. Run by co-founders Naman & Shatakshi. Graduation letter confirmed.
   - The Sukha Education engagement (S15) was the Impact Lab project delivered during this fellowship.
   - ⚠️ NOTE: "Feynman Fellowship" was a misremembering — correct name is GGI Fellow, Global Governance Initiative, 2024.
   - **Resume line:** GGI Fellow · Global Governance Initiative · 2024

2. **Scaler Academy — Completed Certifications (✅ All done):**
   - SQL · Excel · Tableau · Power BI · Python · Product Analytics
   - All 6 completed. All from Scaler Academy (Indian ed-tech platform, well-known in tech hiring circles).
   - These validate the technical skills already demonstrated in project work. Use on resume to back up the skills section.
   - **Resume line:** SQL · Excel · Tableau · Power BI · Python · Product Analytics — Scaler Academy

3. **Scaler Academy — Data Science & Machine Learning** (In Progress, not completed)
   - Topics: Product & Data Analytics, Machine Learning, Neural Networks, Computer Vision
   - Satvik's honest self-assessment: still learning, not proficient yet.
   - ⚠️ DO NOT list on resume until completed. Mention only conversationally if asked about technical upskilling.

---

## S19 — Why Satvik Is Leaving AmEx (The Real Reasons)

**✅ CONFIRMED — Satvik's own stated reasons**

Not a single reason — a combination:

1. **Title gap:** He is doing Product Manager-level work but his title is "Senior Associate Product Manager / PO." He has not had a clean PM title yet in his career. This matters for FAANG applications and for how the market values him.

2. **Domain is boring and B2B:** AML compliance and financial risk scoring. Deeply enterprise, deeply regulatory, deeply removed from consumer products or anything that would build FAANG-relevant product intuition. He feels the work is not making him PM-world ready.

3. **Growth ceiling:** He has hit a point where the next meaningful career growth at AmEx is slow and politically constrained. He's the highest-rated PO in the VP's org but advancement isn't straightforward from here.

4. **Long-term desire:** He wants to have his own business one day. This is a real ambition, not a throwaway line — LinkRight is early evidence of this. But it's not happening right now. Right now he needs a strong PM title at a company that gives him real PM experience, better domain exposure, and a path toward eventually building something of his own.

**How to frame this in interviews:**
Don't lead with the boring domain — sounds petty. Lead with growth ceiling + ambition. "I've done well at AmEx — highest rated in my cohort, SVP award, led the CRR modernization program. But the domain is niche, the career path is slow, and I want to work on problems that directly impact end users at scale. That's where I'm headed."

---

## S20 — Job Search Context & Salary Negotiation

**Location preference:**
Satvik wants a **remote-first or fully remote role** so he can settle in Indore post-marriage (October 2026). His girlfriend (marrying in October) teaches in Indore. His mother in Chhatarpur will likely move to Indore too. GoGoGo founders are also Indore-based. This is the real life plan. Remote is a hard requirement, not a preference.

**Do NOT mention Indore/remote in applications or early interview rounds.** Raise only after receiving an offer, during negotiation: "I'm currently in Gurgaam but planning to relocate to Indore later this year — is the role flexible on location?"

**Timing urgency:** Marriage in October 2026. Needs to start new job by July–August 2026 at the latest to be settled before the wedding. Applications must start immediately (May 2026).

**Business ambitions:** Wants his own business eventually. LinkRight is the vehicle being built nights and weekends. Strategy: get strong PM title + remote job first → let LinkRight reach partial stability → then evaluate the leap. Will NOT quit job to start a business prematurely.

---

**Current Compensation (AmEx):**
- Base salary: ~31 LPA
- Total CTC (base + performance bonus + allowances): ~35 LPA
- ⚠️ AmEx's official salary export only shows the lower base figure — a deliberate tactic that anchors new employer negotiations at a lower number.

**Negotiation rules:**
- Always quote **35 LPA as current CTC** — that is the real number
- If asked for salary slip: explain "base is 31 LPA, total comp including bonus and allowances is 35 LPA"
- **Target for new role: 45–50 LPA minimum CTC** — a 30–40% jump is standard for a title upgrade + company switch
- For US-headquartered remote companies with India PMs: potential upside of 50–70 LPA
- Do NOT accept 37–38 LPA offers unless equity or growth trajectory is exceptional — that's lateral movement with a better title sticker

---




# LAYER 2: THE TELL
### The spoken narrative — how you frame and communicate your story.
### Rule: Facts from Layer 1 only. Nothing invented. But strategically framed.
### Audience: Hiring managers, interviewers, networking conversations, "tell me about yourself."

---

> **What this file is:**
> The version of each story you'd tell in a 30-minute interview conversation.
> STAR-structured where needed. Honest, but strategically angled.
> This is where the *meaning* of the experience gets shaped — not what happened, but what it signals about you as a professional.
> This is also the source for your LinkedIn "About", your intro pitch, and your walk-me-through-your-resume answer.

---

## MASTER NARRATIVE — The Through-Line

**The pattern across everything Satvik has done:**
He consistently enters situations where the work is ambiguous, the data is messy, the problem hasn't been properly defined — and he builds structure out of chaos. He owns deeply, learns by doing, and earns trust by delivering before asking for recognition. He has the technical fluency to get into the details (SQL, ML configuration, LLM pipelines, data architecture) while keeping sight of the business outcome.

**The throughline in one sentence:**
*"I turn messy, ambiguous problems into structured products — by going deep on the data, earning trust with the people in the room, and shipping before I ask for the title."*

**Career arc narrative (for "walk me through your background"):**
"I started at Sprinklr as a fresher — IIT Delhi background, but civil engineering, no traditional tech or PM pedigree. Within 6 months I was ranked #1 globally among all implementation consultants. What I was actually doing there was product work: I owned client requirements, designed data architectures, built ML-powered analytics pipelines, and led the delivery on some of Sprinklr's biggest engagements — including the Government of Qatar's $32 million citizen experience platform and Walmart's driver support root cause analysis product.

I transitioned into product management the way I've done most things — by doing the job first and getting the title later. The VP of Product at Sprinklr saw my work and invited me to join the product team. I moved into the Use Case Hub, stepped into full PM responsibilities when the lead PM went on maternity leave, and learned by doing in ways that no classroom could teach.

I joined American Express in mid-2024 as a Senior Associate Product Manager on the AML Customer Risk Rating team. I was the only PM on the team when I joined — no manager supervision, understaffed team, 21-requirement BRD that needed to become a coherent product. I built the 3-year roadmap, ran 10 sprints solo, navigated two major strategy pivots without losing the team's momentum, and got the highest performance rating among Band 30 Product Owners in my VP's organization.

In parallel, I've been building an AI-native career navigation platform called LinkRight — solo, while holding the full-time AmEx role. It's taught me more about how to build honest, reliable AI products than anything else I've done.

Now I'm looking for a role where I can bring all of that — enterprise product ownership, data and AI fluency, and the ability to go from strategy to execution — to a company that's building something I genuinely care about."

---

## INTRO PITCH — "Walk me through your background"

**90-second version:**
"I'm a product manager with about 4 years of experience across enterprise SaaS and financial services. I started at Sprinklr — where I went from zero PM experience to leading delivery on some of their biggest client engagements globally, including a $32 million government platform for Qatar and a GenAI root cause product for Walmart. I transitioned into product formally when the VP of Product invited me to join his team after seeing my work. Then I moved to American Express, where I've been the PM on the AML Customer Risk Rating modernization — building a risk scoring platform that powers 100 million+ customer accounts across 40+ markets. I got the highest performance rating among Band 30 Product Owners in my VP's org last cycle. Alongside all of that I've been building an AI career navigation platform called LinkRight — solo, shipped to PyPI, fully production-grade. What ties all of it together is that I go deep on the problem before I touch the solution — whether that's data pipelines, LLM architectures, or compliance workflows."

**3-minute version:** Use the Master Narrative above verbatim.

---

## S1–S5 — Personal Foundation (Why you are the way you are)

**For "what shaped you" / "tell me something about yourself beyond your resume" questions — 3–4 sentences, use judgment on how much to share:**

"I grew up in a family that moved frequently across Madhya Pradesh. When I was 11, my father passed away suddenly, and overnight I became the eldest in the family — responsible for my mother and younger sister. That set the tone for how I operate: I don't wait to be given responsibility, I take it, because I learned early that waiting isn't a real option.

IIT Delhi was academically hard for me — I struggled in theory, but I scored 10/10 in every practical lab I ever took. That pattern has followed me everywhere since. I'm not a person who learns from textbooks — I learn by building. At Sprinklr, at AmEx, and in LinkRight, the way I've grown fastest is always by owning something that's too big for me and figuring it out on the way."

**When NOT to share:** Don't go into father's death unprompted in an interview. Only use if the question specifically invites a personal story and the environment feels appropriate. The IITD lab vs. theory contrast is always safe and genuinely useful — it explains your learning style without requiring emotional disclosure.

---

## S6 — The Gap Year & PwC Bet

**For "I see a gap year — what were you doing?" (30 seconds):**

"After IIT Delhi I spent about 10 months preparing for the GATE exam — I was targeting a PSU role. I scored in the top 1.5% nationally but just missed the cutoff. During that period PwC offered me a role in real estate consulting — I declined it because I'd already committed to the GATE path. In hindsight, it was a calculated bet that didn't pay off the way I planned, but it did teach me to bet on myself even when the safe option is on the table. That decision led directly to me finding Sprinklr, which ended up being the right path anyway."

---

## S7 — Sprinklr IC (The Foundation Story)

**Framing:** This is where the PM journey actually begins, before the title. The narrative is: "I came in without knowing exactly what I was walking into, and I figured it out by going deep on the work — deep enough that I became the top-ranked IC globally in 6 months."

**For "walk me through your background" — S7 portion (30 seconds):**
"I started at Sprinklr as an Implementation Consultant in 2022 — which was really my first real exposure to product and data work at enterprise scale. Within 6 months I ranked #1 globally among all ICs for customer satisfaction, and within 11 months I was the only person on my team promoted to Senior IC. What I was actually doing there was sitting at the intersection of data engineering and product thinking — working directly with enterprise clients like Adobe, Walmart, Snapchat, and Discord to understand their pain points and build data systems and dashboards that changed how they made decisions."

**Adobe story (for "tell me about a complex technical problem you solved"):**
"Adobe was one of my first major clients. The problem was that their social media data was completely fragmented — they had three separate sources: earned media, organic posts, and paid ads — each with different schemas, different metrics, different formats. Every time they needed a full analysis, someone was spending 4 days manually pulling and reconciling all of this. I built a unified SQL-based pipeline that standardized all three sources into a single schema and automated the analysis workflow. We took that 4-day cycle down to 1 day. On the same engagement, I also built a spam detection model using Sprinklr's AI Studio — an annotation-based ML tool — to filter out low-quality signals from their analytics. That model hit an F1 score of 87%."

**On the Gold Medal (for "tell me about an early win or a time you exceeded expectations"):**
"Six months into my first job, my director presented a slide with my name in a global all-hands meeting — I had received the highest customer satisfaction score across all Implementation Consultants worldwide. That wasn't something I was gunning for. I was just focused on the work. But it told me something I hadn't fully believed about myself since college — that when I'm in an environment where I can actually apply what I know practically, I operate at a very high level."

**The promotion framing:**
"After 11 months, I was the only person out of 8 consultants on my team to be promoted to Senior IC. I found out on the same day my manager resigned. He had gone to bat for me in an internal review — there was a situation where I inadvertently made things worse for him by saying something honest but poorly timed in front of the VP, and it cost him politically. He still made sure my promotion went through before he left. That was a formative lesson for me — not about being political, but about understanding the difference between what's true and what's legible in a room. How you say something, when you say it, and who's in the room changes outcomes dramatically. That shaped how I think about stakeholder communication to this day."

**For "tell me about a time you failed / made a mistake" (optional use — judgment call per interview):**
"Early at Sprinklr, there was a project review call where my manager was defending my work. A document came up that I genuinely hadn't worked with — a colleague had dropped the ball on tracking it — and in the moment I said, 'I'm seeing this for the first time.' Factually true. But the optics in that room meant it looked like my manager had been lying to protect me. He took a career hit because of how that played out. It cost him a promotion he deserved. I didn't lie, but I also didn't read the room. That experience made me much more deliberate about how I communicate under pressure, especially in front of senior stakeholders."

---

## S8a — Qatar CGB Project

**Framing:** This is your "nation-scale impact" story. Lead with the scale, then go deep on your specific contribution. Don't claim the deal — you weren't on the sales team. Own the implementation and the outcomes.

**For "tell me about the biggest / most complex project you've worked on" (2–3 minutes):**

"One of the most significant projects I worked on was Sprinklr's largest-ever net new deal — a $32 million, 5-year partnership with the Government of Qatar to build a unified citizen experience platform across 40 ministries. The context was that Qatar was ranked 78th on the UN E-Government Development Index — behind all GCC countries — and they wanted to transform how citizens interacted with public services.

I was brought in as the Insights implementation lead for all five Sprinklr Insights products on this project. My work had two main tracks.

The first was building the data and insights layer. I was asked by Sprinklr's AVP of Product Management to own the product experience for the ministers of the Prime Minister's Office — specifically the mobile app and dashboards they'd use to monitor citizen sentiment across all 40 ministries in real time. The entire interface had to be in Arabic — which meant full RTL adaptation, not just translation. I focused on making the insights genuinely actionable: not just raw data on a screen, but a clear story about which ministries had issues and where intervention was needed. We got time-to-insight from 2 days down to 2 hours.

The second track was scaling the team to deliver. The project team grew from 6 to 14 people in 3 months. I onboarded 8 consultants using a structured knowledge transfer process — I designed a base dashboard template, taught the team how to customize it for each ministry, and personally reviewed every one of the 120 dashboards we delivered across 40 ministries in 4 weeks. That was aggressive, but the process made it possible.

By the time the implementation was complete, Qatar had moved from rank 78 to rank 53 on the UN E-Government Index — a 25-position jump."

**On the Arabic localization specifically (for interviews with technical or platform PM interest):**
"The localization wasn't just translation. Arabic is RTL — right to left — which means the entire layout logic, navigation flow, icon direction, and data visualization had to be reconsidered. You can't just flip text. We led a dedicated effort to ensure the RTL adaptation was correct throughout, which also required validating the NLP models for Arabic sentiment — we improved the sentiment model F1 by 11% and the intuition model by 13% specifically for Arabic."

**On team scaling and onboarding (for "tell me about a time you led a team or developed others"):**
"I used a practice called reverse-KT — instead of me sitting down and lecturing new team members, I structured the sessions so that they were actively extracting knowledge through a guided framework. I'd record every session, capture open questions, and maintain a shared repository. It took about 4 extra hours a week on top of the project work, but it meant 13 new people got up to speed fast enough to contribute to 120 dashboards in 4 weeks."

---

## S8b — Walmart Spark Driver Support

**Framing:** This is your "I was a PM before I had the title" story. Lead with the problem, show the cross-functional ownership, land on the Anish conversation as the proof point of what it led to.

**For "tell me about a complex product problem you solved" (2–3 minutes):**

"At Sprinklr, I worked on the Walmart Spark Driver Support engagement — Walmart's gig driver platform was hemorrhaging drivers. The data showed D30 retention was around 35% and D60 was around 18% — most drivers were churning before they'd completed two months on the platform. Contact volume was over 100,000 cases, and no one had a clear picture of why.

My job was to build a root cause analysis product that could answer that question. But this wasn't a clean data problem — the sources were completely disparate. In-app feedback, App Store and Play Store reviews, NPS surveys, voice call transcripts, support chat exports, Reddit threads, Twitter posts. All in raw form, all with different schemas. I personally owned the requirements gathering, the schema design, and the full architectural design of how these sources would be combined. I used Sprinklr's Data Pipelines product — which I configured directly using SQL joins and data transformation logic — to unify everything into a single coherent data layer.

What I was also doing in parallel was running the project itself — daily standups, unblocking the team, escalating engineering issues directly when things got stuck, and leading the weekly leadership updates to Anish Singhal, who was Sprinklr's VP of Product at the time.

The output was a GenAI root cause product that automatically identified the top drivers of contact volume and churn, with a custom L1/L2/L3 issue taxonomy, and auto-routed mitigation actions to engineering and fraud teams. Time-to-insight went from 7 days to same-day.

What it led to: Anish scheduled a direct call with me. He asked me if I wanted to join the product team and why. That's how I moved into the Use Case Hub PM role."

**On the Anish conversation specifically (for "how did you transition into product management"):**
"The transition wasn't a formal process. I had been leading the Walmart project end-to-end — requirements, architecture, client comms, leadership updates — essentially doing the PM job without the title. Anish Singhal, Sprinklr's VP of Product, was receiving the leadership updates I was running. One day he scheduled a call directly with me and asked if I wanted to be in his product team. His main PM was going on maternity leave and he needed someone who understood the product from the inside — someone who'd configured it, debugged it, and shipped with it. That was me. The PM title came from doing the work first, not from applying for it."

**On the Black Friday pilot specifically (for "tell me about high-stakes real-time product work"):**
"One moment that stands out was the Black Friday pilot. We had a group with Walmart leadership — VPs, Directors, Senior Managers — plus the Sprinklr leadership team. About 10–12 people total. The system was running automatically — data ingestion, ML tagging, root cause classification — all live. But someone had to be the intelligence layer on top of it. I was pulling screenshots from the dashboards as significant insights surfaced, sending them into the group, and narrating in real time what it meant for driver behavior during one of the highest-volume weekends of the year. That was a trust moment — Walmart leadership was watching the system perform live, and I was the one translating it for them."

---

## S8c — Use Case Hub

**Framing:** Don't lead with the adoption metric — it's unverified. Lead with what's real: stepping up into PM responsibilities for the first time when the PM went on maternity leave, doing it for 6 months across two time zones with no additional pay, and the lesson you learned about self-advocacy. This is a better story than inflated numbers.

**For "how did you first get into product management" (this is the real transition story):**
"My transition into product management at Sprinklr happened gradually, and honestly, partly by accident. I was brought in as a Product Analyst on the Use Case Hub — a product to help smaller enterprise clients self-serve their setup on the Social Listening module. The PM on the project, Surabhi Goyal, was the one running PRDs, agile ceremonies, and engineering connects. I was learning by watching.

When she went on maternity leave, the expectation shifted entirely to me — immediately. No ramp, no title change, no additional compensation. I was still managing my Senior IC workload in the US time zone and picking up the PM responsibilities in the India time zone. That went on for about 6 months. 9 AM to 3 AM was a normal day.

I contributed to the product strategy, roadmap, prioritization, grooming, and QA — and I also did a deep-pattern review of over 1,500 client dashboards across 15 industries to understand what templates and use cases actually existed in the wild, which helped shape the Use Case Hub structure.

When the formal transition finally happened, I made a mistake I still think about — I asked for 'Senior Product Analyst' when I should have asked for APM. I undersold myself. I got a dry title change with no salary increase. That was a hard lesson in knowing your worth and asking for it explicitly."

**On why you left Sprinklr (for "why did you leave your previous role"):**
"I burned out. I had been doing two jobs for 6 months for one salary, got a dry promotion with no recognition, and by the time I was ready to leave, I had applied for a couple of months of leave. Leadership's reaction to that request was telling — they gave me the title I should have had months earlier, but only because they thought I was about to walk. When recognition only comes as a retention move, it's a signal about the culture. I decided it was time to take what I'd built and go somewhere I could be valued from day one."

---

## S9 — Sprinklr to AmEx Transition

**Framing:** The Advocacy period is not worth bringing up in interviews — it was brief, lightweight, and didn't produce much. Don't mention it unless directly asked "what were you doing in your last few months at Sprinklr?" If asked, be brief.

**If asked about the Advocacy period:**
"In my last couple of months at Sprinklr I moved to the Advocacy product team — I was exploring whether a different product area would give me more structured growth. But honestly, the right move came faster than expected: I got the AmEx offer and took it."

**On why you left Sprinklr (full version — use judgment on how much to share):**
"At Sprinklr I was doing strong work — the Qatar project, Walmart, and then stepping into PM responsibilities on the Use Case Hub. But the recognition never caught up with the reality. I was doing two full jobs for about 6 months with no title change and no salary change. When the title finally came, it came as a retention move after I applied for leave — not as genuine recognition. I realized I needed to be somewhere that would value my contributions from the start, not as damage control. AmEx came at the right time."

**Short version (for "why did you leave") — 2 sentences:**
"I had delivered significant work at Sprinklr across some of the company's biggest projects, but hit a ceiling where growth was more political than performance-based. When AmEx came with a proper PM role and the right scope, it was an easy decision."

---

## S10a — Amex Vendor Evaluation (Build vs Buy)

**⚠️ DO NOT USE THIS AS A STORY IN INTERVIEWS.**
The vendor evaluation was done by Satvik's manager. He received basic context about it. The detailed interview story in the old career profile ("I ran the entire evaluation end-to-end, 15+ vendors down to 2 finalists…") is not his to tell. Using it in an interview would be a fabrication he cannot defend if probed.

**If asked about vendor evaluation context (brief acknowledgment only):**
"When I joined, the team had already worked through the build vs. buy decision and landed on building in-house. I was brought up to speed on the rationale — the key factors were configurability, integration fit with Amex's ecosystem, and the specific requirements around hierarchy scoring that vendors couldn't fully cover. My job from day one was to pick up the BRD and start building."

**The REAL first chapter at AmEx — what he actually did:**
The real story of his early months is the 3-year roadmap and the 21-to-6 capability framework. That is genuinely his work and the reason he got the Leadership in Action Award. This is the story to tell.

---

## S10b — CRR Platform Build

**Framing:** This is your "owned a product end-to-end from zero" story. Lead with the scope, the solo ownership, and the structural clarity you brought to a chaotic situation.

**For "tell me about a product you owned end to end" / "most complex technical product" (2–3 minutes):**

"When I joined American Express in mid-2024, I was placed on the AML Customer Risk Rating team. The CRR system is what AmEx uses to score the risk profile of every customer on the platform — 100 million+ accounts across 40+ markets. It hadn't been properly modernized in years.

When I joined, I was the only PM or PO on the team. No manager supervision, understaffed, and the foundation document was a 21-requirement BRD that listed what the platform needed to do but had no structure, no prioritization, and no roadmap. My first job was to turn that into a buildable plan.

I spent the first weeks doing a deep audit — talking to compliance analysts across 6 global regions, running 20+ UX research sessions, mapping every requirement against the actual user workflows. Out of those 21 requirements, I identified 6 core platform capabilities that everything else fell under: rule configuration, asset management, sandbox versioning, audit trail, advanced configurations, and the customer journey layer. That became the product architecture. I built the 3-year roadmap off that framework and presented it to the SVP of Risk Management. That roadmap, done before a single sprint was run, was the reason I received the Leadership in Action Award from the SVP.

Then I ran 10 consecutive sprints as the only PM on the team — all sprint planning, all backlog grooming, all cross-functional coordination with an 18-member team. We delivered 60+ features across the core capabilities with zero spillover across 4 consecutive PIs.

For the first 3 UI capabilities, I designed the interfaces myself in Figma — the Asset Manager, the Advanced Rule Configurations screen, and the Sandbox Versioning flow. That required me to be both PM and hands-on UX designer simultaneously.

By the end of PI 25.2, CRR MVP had reached staging and QA. It was not deployed to production — a strategy pivot redirected us to fix the data foundation first. But the platform itself was built, validated, and ready."

---

## S10c — Strategy Pivots & Crisis Management

**Framing:** This is your "I handle ambiguity at the product level, not just the sprint level" story. The two pivots happened within months of each other — show the pattern, not just one event.

**For "tell me about a time you handled a sudden change in direction" (90 seconds):**

"At AmEx, I went through two major strategy pivots within the same year — and they happened back to back.

The first was a methodology change. We had been building the CRR platform around a new, simplified scoring approach. Midway through the program, the business reversed that decision — they decided to go back to the legacy Cadence methodology they'd used for years. Simultaneously, the scope was cut from a 2-year full modernization to a 1-year lift-and-shift: just enough to decommission the old system and migrate to the new platform. The entire product strategy I'd been building had to be repriced and reprioritized. I reprioritized the full backlog within one week — not by doing less, but by ruthlessly figuring out what was actually essential to the new goal versus what was nice-to-have for the original vision.

The second pivot came when the CRR MVP had reached staging and QA — right on the edge of production. The data team that was supposed to deliver clean, standardized data to the platform had been underperforming. The CRR rules couldn't function on the raw data being provided. Leadership decided to pause the CRR platform and fix the data layer first.

I took that pivot and turned it into a product — what became the CDL strategy. Rather than waiting for someone else to fix the data problem, I scoped it, designed a solution architecture, and led the discovery myself.

Both pivots were disorienting in the moment. But the pattern they reinforced was that product work is never a straight line — and your value as a PM is directly proportional to how fast you can reorient without losing the team."

---

## S10d — CDL Strategy

**Framing:** This is your "platform thinking and data architecture" story — and it's current work. Shows you can think 3 levels above the feature layer.

**For "tell me about a data or platform strategy problem you've worked on" (2 minutes):**

"The current project I'm leading is the Consolidated Data Layer strategy for the AML platform at AmEx.

The root problem is that the platform was getting inconsistent, un-standardized data from the underlying data layer. The raw SOR (system of record) values are completely fragmented — 136,000+ raw Product Type records, 521,000+ Industry Type records — in forms that can't be used by the risk scoring rules that depend on them.

My job was to design a solution that could take this chaos and turn it into a reliable, governed data foundation.

I designed a 5-step pipeline: Translation → Standardization → Categorization → Derivation → Master List. Then I built a three-bucket prioritization framework for every raw record: Discard and Rebuild, Educate the Business, or Transform. That framework let me take 136,000 product type records down to 64 usable categories, and 521,000 industry type records down to 98 categories — without losing the business logic embedded in any of them.

The roadmap targets 85.3% risk element coverage by PI 26.5, and 96.5% by PI 27.1. We're currently in Phase 0 discovery with a 4-person team that reports to me directly.

What made this problem interesting is that it wasn't a feature problem — it was a data infrastructure problem disguised as a product problem. The business had been managing cross-references manually in Excel for years. No one had stepped back to ask why the data was broken at the source. That's the question I asked, and the CDL strategy is the answer."

---

## S11 — GoGoGo

**Framing:** Brief mention only. Don't overclaim. Don't say Chief of Staff — it was announced but never real. Use "Product Advisor and early operator" framing. Most useful as evidence of startup exposure and founding-team proximity, not as a primary story.

**If asked about GoGoGo (30 seconds max):**
"Alongside my AmEx work I was an early operator and product advisor at GoGoGo — a ride-hailing startup competing with Ola/Uber. I helped with early team building, marketing, and driver acquisition in the beginning. As the company matured I moved into a product advisory role — reviewing the product, giving feedback, sitting on board calls. I have equity in the company. It gave me real firsthand exposure to zero-to-one building, fundraising realities, and the operational chaos of an early-stage startup — which is a very different environment from what I was doing at AmEx."

---

## S12 — ContentStack

**Framing:** This is real PM work — don't undersell it. You were paid, you owned product strategy and execution, you shipped 3 AI products. The framing challenge is explaining the concurrent nature without it sounding unfocused. Lead with the AI product depth.

**If asked about ContentStack (45 seconds):**
"In parallel with AmEx, I took on a part-time freelance PM role at ContentStack — a CMS platform. I owned the product strategy and execution for three AI-native tools: an AI content creation tool called Compose AI, an AI website builder called DesignerAI, and a website performance monitoring product called Lens. I was the PM — defining features, prioritizing the roadmap, working with developers and designers, following up on execution. It was a great way to apply AI product thinking in a B2B SaaS context outside of financial services, and it kept me sharp on what AI-first product development actually looks like at the feature level."

**Why this matters for your narrative:**
ContentStack is proof that your AI PM skills aren't just theoretical — you were trusted by a real company to define and ship AI products as a freelancer while holding a full-time role. That's signal.

---

## S14 — LinkRight

**Framing:** Pitch this as the deepest proof of how you think about AI products: evaluation-driven, honesty-first, shipping discipline, solo ownership. The story is about *what it reveals about you as a builder*, not just business metrics. Importantly — you did validate before building (147-response survey, 7,000+ cold-outreach) so this isn't a garage project no one ever used; it's a disciplined 0-to-1 execution story.

**For "tell me about a passion project / how you think about AI products" (2–3 minutes):**
Use the full Story 3 narrative from the career profile — it's genuine, detailed, and compelling. The key beats:
1. Started to solve my own job search problem
2. Realized the real problem was stateless AI — no persistent career memory
3. Insight shifted: it's not a resume builder, it's a career memory graph
4. Validated before building: 147-response survey + 7,000+ cold-outreach defined 3 ICP segments pre-build
5. Technical depth: benchmarked 8 LLMs, built hybrid parser (deterministic + LLM), fabrication guards, evaluation framework with 16 dimensions
6. Shipping discipline: 44 of 57 issues shipped solo while holding AmEx full-time role; published to PyPI
7. What I learned about myself: I'm the same practical learner who scored 10/10 in every IIT lab while struggling in theory — I build by doing

**On the validation work (for "how do you know there's a market" questions):**
"Before writing a single line of code, I ran a 147-response survey and did 7,000+ cold outreach touches to define 3 ICP segments. That's not a side project approach — that's the same discovery discipline I'd apply at any company. The product exists because the signal was clear, not because I thought it was a cool idea."

**On stage honesty (for "how many users / what's the traction"):**
"It's a working product used in real job search workflows. Early validation was strong — 147 survey respondents, 7K+ cold-reached. I'm in the phase of converting that signal into an active user base. The value I bring to an AI PM role isn't the numbers yet — it's that I know how to build AI products that are honest, measurable, and ship. That's what LinkRight proves."

---

## S15 — Sukha Education

**Framing:** This is your "I apply product and strategy thinking outside my day job" story. Clean, mission-driven, real outcomes. Also doubles as evidence of structured consulting thinking — problem framing, stakeholder mapping, cost-of-inaction analysis, phased execution.

**For "tell me about leadership or impact outside your primary role" (60–90 seconds):**

"Earlier in 2025 I did a strategy consulting engagement for Sukha Education — an NGO in Chennai teaching communicative English to underprivileged children, with 2,000+ students and 25+ partner institutions. I did this as a GGI Fellow through the Global Governance Initiative's Impact Lab program — a competitive pre-MBA fellowship.

The problem was operational fragmentation. Lesson plans were shared over WhatsApp, volunteer data was scattered across spreadsheets, no shared communication infrastructure existed. The result: around 40% volunteer churn — not because people didn't care, but because the system made it too hard to stay.

I approached it the way I'd approach any product problem — stakeholder mapping first (volunteers, donors, partners — each with different needs), then a three-pillar strategy: Google Workspace for productivity, Slack and automated workflows for collaboration, and Salesforce CRM for impact tracking and donor reporting. I built a cost-of-inaction analysis to quantify the problem — that's where the ₹60,000 annual savings figure came from. Then delivered a 12-week phased rollout plan with risk mitigation for user adoption, data integrity, and engagement drop-off.

The outcome was ~₹60,000 in annual cost savings and a 50+ volunteer organization with actual operating infrastructure for the first time.

What I took from it: the PM toolkit — problem framing, stakeholder alignment, phased rollout, change management — transfers exactly to consulting. The domain changes. The method doesn't."

**For a shorter version (30 seconds):**
"I was a GGI Fellow in 2024 — a competitive pre-MBA program. My Impact Lab project was a digital transformation for Sukha Education, an NGO in Chennai. Three-pillar strategy: Google Workspace, Slack, and Salesforce. 12-week rollout. ~₹60,000 annual savings. 50+ volunteers on the platform. Delivered as a full consulting deck to the Sukha leadership team."

---

## S16 — Navii (HeyNavii): Beta Growth PM

**Framing:** Brief. Don't overclaim — you were unpaid, ~1 month, and the 20K growth had multiple contributors. Use this as evidence of (a) consumer app exposure, (b) structured product thinking applied to a real product, and (c) technical execution (N8N automations, Chrome extension). It's a supporting signal, not a headline story.

**If asked about Navii / consumer app experience (30–45 seconds):**
"In late 2025 I was the Beta Growth PM for Navii — an AI-powered career navigation app. It was a structured engagement: I mapped 5+ user journeys end-to-end, documented 14 bugs and 9 product enhancements, wrote onboarding guides and videos for key flows, built N8N automation pipelines and a Chrome extension, and conducted user interviews. During that period the platform grew from about 2,000 to 20,000 users — I can't take full credit for that growth, it had multiple contributors, but I was deep in the product the whole time. What it gave me was firsthand exposure to a consumer app with real users reacting to changes in real time — very different from the B2B enterprise work I'd been doing."

**When it adds value to your narrative:**
- For Consumer/App PM roles: leads cleanly into "here's the closest I've gotten to a consumer product"
- For Growth PM roles: shows you can work in a high-growth early-stage product context
- For startup PM roles: shows you can operate without structure and still produce structured outputs

**When NOT to use:**
- Don't bring it up unprompted in an enterprise/big-tech PM interview where the engagement is too small to signal
- Don't claim the 20K growth as your own — always say "during the beta period" and "multiple contributors"

---

## S17 — Mentorship Stories

**Framing:** These two stories are about what kind of person you are beyond the work. Use them for "tell me about someone you've developed" or "what does leadership mean to you" questions.

**Story 1 — Sister Sanika (for "how have you developed others / mentorship"):**
"My sister Sanika is one of the proudest outcomes of anything I've done outside work. She was preparing for JEE while I was navigating IIT and my first job — I guided her prep through that entire period. She made it to IIT BHU in Electronics and Communication Engineering. She went on to be the only girl from IIT BHU to get a Google internship, topped the girls' category in ECE with a 9.2/10 CGPA, reached the final waitlist at Confluent despite competing against CS graduates, and is now a Senior Software Developer at Oracle.

What I take from that is simple: if you understand how someone learns and you believe in them before they believe in themselves, you can change their trajectory. That's what good mentorship actually is."

**Story 2 — Junior colleague after Sprinklr layoff (for "tell me about a time you invested in someone"):**
"After Sprinklr went through a layoff round, a junior colleague of mine — someone from a farming family in Rajasthan, educated through Jawahar Navodaya Vidyalaya and Super 30, NIT Warangal graduate — found himself without a job and came to stay with me.

I mentored him intensively for 3 months. We covered PM fundamentals, data analytics, interview skills, communication. We gave 15–20 mock interviews together, I gave him feedback after every one, and we iterated on how he told his story and how he answered questions under pressure.

He secured an APM role at Next Wave without a single day of unemployment.

The reason I tell this story isn't to make myself sound good — it's because it clarified something for me about what I find meaningful in the work. Building something is great. But watching someone go from zero confidence to performing at their ceiling — that's a different kind of impact."

---

## COMMON INTERVIEW QUESTIONS — Pre-drafted Answers

### "Why do you want to leave AmEx?"

**Short version (use by default):**
"I've had a strong run at AmEx — highest-rated in my cohort, built the CRR platform from scratch, got recognized by the SVP. But the domain is deeply niche — AML compliance — and I've reached a point where the next meaningful growth is slow. I want to work on products that directly impact end users at scale. That's the direction I'm moving."

**Full version (if probed further):**
"There are a few honest reasons. The domain — financial crimes compliance — is important work, but it's deeply B2B and regulatory. It's not building the product intuition I want for where I'm headed. The career path at AmEx is also incremental from here — I've already been the highest-rated in my band, and the step-up isn't fast. And honestly, I want to work at a company where the product problems are harder to ignore — where if you ship something bad, users push back immediately. That feedback loop is valuable. I'm not getting it in AML."

**⚠️ Do NOT mention wanting your own business in interviews.** It reads as "I'll leave as soon as I can." Keep it about growth, domain, and impact on real users.

---

### "Why Product Management? Why now?"

"I didn't choose PM — PM chose me, twice. The first time was when Anish Singhal at Sprinklr saw my work on the Walmart project and asked if I wanted to join the product team. I had been running the project like a PM — requirements, architecture, client management, leadership updates — without the title. He saw that and offered me the door.

The second time was at AmEx, where I joined as a PO and immediately found myself doing everything a PM does: roadmap, UX research, design, strategy, stakeholder management, pivots. There was no PM above me for the first 10 sprints. I was just doing the job because it needed to get done.

So the honest answer to 'why PM' is: because I've been doing it for 4 years regardless of what my title said. I'm formalizing that now."

**If the question is "why now specifically":**
"Because now I want a role where the title matches the scope, where I'm not the only PM on the team figuring it out solo, and where the product problems connect to real user behavior I can observe and measure. AmEx was the right training ground. Now I want the full game."

---

### "Tell me about a time you failed."

**Use the Snapchat/manager story — it's the best one.**
*(Full text already in S7 — "For 'tell me about a time you failed / made a mistake'")*

Key beats: Blurted "I'm seeing this document for the first time" in a VP meeting. True statement. Destroyed my manager's credibility. He lost a promotion and quit. The lesson: honesty without calibration is not always a virtue. You have to understand the room before you speak, especially under pressure.

---

### "Tell me about a time you influenced without authority."

**Use the CRR Platform story — 10 sprints solo, led 18-member scrum team by influence.**

"When I joined AmEx, I was the only PM/PO on the CRR team — but I wasn't the most senior person in the room. I was working with senior engineers, data engineers, QA leads, and POs who had been at AmEx for years. I had no authority over any of them.

What I could offer was clarity. I had done the work to turn 21 vague requirements into 6 structured capabilities and a 3-year roadmap. Every time there was confusion about priorities, I could point to the framework. Every time someone pushed back on scope, I had the research — 20+ sessions with compliance analysts across 6 regions — to defend the decision.

Over time, the team came to me not because they had to, but because I had the best view of where we were going and why. That's the only kind of authority that lasts in a cross-functional team."

---

### "What's your biggest weakness?"

**Honest and interview-safe version:**
"I have a tendency to go very deep before I surface. When I'm in a new problem, I want to understand it completely before I start talking about it — which is often a strength, but it can slow down early alignment. At AmEx I learned to balance that — you can't always wait until you have the full picture before you bring stakeholders in. I've gotten better at structuring ambiguity publicly rather than resolving it privately first."

**Why this works:** It's real (not a fake strength dressed as a weakness), it's PM-relevant (stakeholder communication), and the self-awareness shows growth.

---

### "Why this company / this role?"

*[Template — customize per application. Key elements to always include:]*
1. Specific thing about their product or problem space that you genuinely find interesting — not generic praise
2. Connect it to something from your background that's directly relevant
3. One honest thing about the company's growth stage / culture that you find energizing

*Example structure:* "I've been watching [Company] for [reason] — specifically [specific product decision or metric]. That connects directly to [your relevant experience]. What I want now is [what this role gives you that AmEx didn't], and [Company] is one of the few places where [that's genuinely possible]."

---




# LAYER 3: THE WRITE
### The resume / portfolio layer — compressed, strategic, ATS-optimized.
### Rule: Every bullet must be traceable to a confirmed fact in Layer 1.
### Audience: Recruiters (6-second scan), ATS systems, hiring managers reading in 2 minutes.

---

> **What this file is:**
> The expression layer — the final, polished, compressed output.
> Maximum signal per line. Outcome-first. Seniority signals embedded.
> This is NOT written until Layer 1 is validated. Bullets here are the last step, not the first.
> 4 resume archetypes will be extracted from this file once it's complete.

---

## HEADLINE / POSITIONING STATEMENT

**Base (archetype-neutral):**
Product Manager · Enterprise SaaS & AI · Data-Driven Builder · IIT Delhi

**Archetype A — Enterprise/Big Tech:**
Senior Product Manager · AML Risk & Compliance Platforms · AI-Powered Analytics · IIT Delhi

**Archetype B — Series A/B Startup:**
Product Manager · AI-Native Products · 0→1 Builder · Data & LLM Pipelines · IIT Delhi

**Archetype C — AI/Data PM:**
AI Product Manager · LLM Pipelines · Evaluation Frameworks · Data Architecture · IIT Delhi

**Archetype D — Platform/Infra PM:**
Platform Product Manager · Data Infrastructure · API-First Thinking · Self-Hosted AI · IIT Delhi

---

## RESUME ARCHETYPE TARGETS

Once this file is complete, 7 versions will be derived:

1. **Archetype A — Enterprise/Big Tech PM** (Google, Razorpay, PhonePe, Zepto, Paytm)
2. **Archetype B — Series A/B Startup PM** (Attentive.ai, Navi, Wishlink, fast-growing SaaS)
3. **Archetype C — AI/Data PM** (companies where AI-native product thinking is the primary differentiator)
4. **Archetype D — Platform/Infra PM** (companies building developer tools, APIs, platform products)
5. **Archetype E — Fintech/Risk PM** (banks, BFSI, fintech startups: Razorpay, Setu, M2P, Fi, Perfios, CRED)
6. **Archetype F — 0-to-1 Startup PM** (early-stage startups, seed/Series A, founding PM roles)
7. **Archetype G — Consumer/App PM** (consumer apps, mobile-first, B2C products: Swiggy, Zomato, Urban Company, healthtech, edtech)

---

## PROFESSIONAL SUMMARY

**Archetype A — Enterprise/Big Tech PM:**
Product Manager with 4 years across enterprise SaaS and financial services. Built AML risk scoring platform at American Express from scratch — 3-year roadmap, 60+ features shipped, highest-rated PM in VP's org (G1L2). Previously led delivery on Sprinklr's largest-ever deals including a $32M Qatar government transformation and a GenAI root cause product for Walmart. IIT Delhi. Strong in SQL, data architecture, and AI/ML product thinking.

**Archetype B — Series A/B Startup PM:**
Product Manager who transitions ambiguous problems into shipped products. Stepped into full PM ownership without the title — twice. At Sprinklr, grew platform adoption from ~35% → ~85% and drove $1.2M TCV at Walmart. At AmEx, ran 10 consecutive sprints solo on an understaffed AML platform and shipped 60+ features. Building an AI career navigation tool solo on the side (LinkRight, PyPI). Comfortable with zero structure, messy data, and leading without authority.

**Archetype C — AI/Data PM:**
AI-native Product Manager with hands-on LLM pipeline design, evaluation frameworks, and production ML deployment. Built GenAI root cause analysis product for Walmart (100K+ monthly contacts, 7 days → same-day insight). Designed CDL data architecture at AmEx (136K+ raw records → 64 governed categories). Built LinkRight solo: hybrid resume parser, 16-dimension evaluation scorecard, fabrication guard system, 9 self-hosted models on Oracle VPS. Knows the difference between demo AI and production AI.

**Archetype D — Platform/Infra PM:**
Platform-thinking Product Manager with strong data infrastructure background. Designed CDL pipeline (5-step: Translation → Standardization → Categorization → Derivation → Master List) at AmEx — targeting 96.5% AML risk element coverage. Built unified multi-source data architectures at Sprinklr (Walmart, Adobe). Published CLI tool to PyPI, designed FastAPI backend, self-hosted LLM stack on Oracle VPS. Understands developer tooling, API design, and what "platform" actually means at the infrastructure layer.

---

## EXPERIENCE SECTION

---

### American Express — Senior Associate Product Manager (Jul 2024 – Present)

**AML Customer Risk Rating (CRR) Platform**

- Joined as sole PM/PO on understaffed AML CRR team; distilled 21-requirement BRD into **6 core platform capabilities** and a **3-year prioritized roadmap** — recognized with Leadership in Action Award from **SVP of Risk Management** for setting the program foundation before execution began
- Led **18-member scrum team** (engineers, data engineers, QA, POs, UX) through influence and structured feedback; **1 direct report** (UX Designer, hired via 12-round selection); informally mentored **3 incoming Product Owners** on product craft and execution
- Led **10 consecutive sprints solo** as the only PM on the team before additional PM support joined; delivered **4 zero-spillover PIs** and **60+ features** across rule configuration, asset management, sandbox, and audit trail capabilities; **MVP-1 reached staging & QA** (not deployed to production — project pivoted to data strategy)
- Owned Platform UI, backend product design, and customer user journeys end-to-end; led **20+ UX research sessions** with compliance analysts across 6 global regions; designed 3 new capability UIs (Asset Manager, Advanced Rule Configurations, Sandbox Versioning); **directly manages UX Designer** hired through 12-round selection
- Reduced speed-to-market for risk scoring configuration changes from **10 days → 3 days (70% reduction)**; navigated 2 major strategy pivots (methodology change + scope reduction from 2-year modernization to 1-year lift-and-shift) — reprioritized entire backlog within 1 week on each pivot
- Received **G1L2 performance rating** — highest-rated among all Band 30 Product Owners in VP's organization (~12–15 peers); **120% bonus increase**
- ⚠️ NOTE: Vendor evaluation story (NICE Actimize / Symphony AI) was manager's work — DO NOT use as own story

**Consolidated Data Layer (CDL) Strategy — Current (PI 26.1–Present)**

- Architected CDL strategy to fix AML platform's data foundation: 54 data points scoped across a 5-step pipeline (Translation → Standardization → Categorization → Derivation → Master List); replaced manual Excel-based cross-reference maintenance with a scalable automated approach
- Designed three-bucket prioritization framework (Discard & Rebuild / Educate Business / Transform) to categorize 136K+ raw Product Type records (→ 64 categories) and 521K+ Industry Type records (→ 98 categories)
- Roadmap targets **85.3% risk element coverage by PI 26.5** and **96.5% by PI 27.1**; currently leading Phase 0 discovery with a 4-person team under direct leadership visibility

**Side Achievements at AmEx**

- **Growth Hack (Jan 2025):** Led 6-member team; built AI Backlog Grooming bot (Slack + Rally integration, auto-generates user stories via AI); ranked **#21 of 400+ teams (Top 6%)** — concept productionized by GMNS as "QE Assist"
- Drove **ChatGPT Enterprise adoption** within team — achieved **80% AI-assisted story drafting** for sprint planning and backlog management
- ⚠️ Negative News / Adverse Media Agent: SUPPORTING ROLE ONLY — do not claim ownership

---

### Sprinklr — Product Analyst → Senior Product Analyst (Apr 2022 – Jul 2024)

**Use Case Hub — Social Listening Self-Serve Platform (2023–2024)**

- Stepped into full PM + PO ownership when lead PM went on maternity leave; owned product strategy, roadmap prioritization, sprint grooming, and QA across a **6-month dual-role period** running two time zones simultaneously
- Analyzed **1,500+ client dashboard patterns** across **15 industry verticals** to architect self-serve template library; product became the **#1 entry point for dashboard creation** across the entire Sprinklr platform post-launch
- Grew Social Listening module adoption **~35% → ~85%** for SME clients (<$1M ARR); eliminated 7-day manual onboarding cycle — **~75% reduction in time-to-value**

**Walmart Spark Driver Support — GenAI Root Cause Analysis (2023)**

- Led end-to-end delivery of a GenAI root cause product for Walmart's **100K+ monthly driver support contacts**; owned requirements, schema design, and unified data architecture across 6+ sources (in-app, app store, NPS, call transcripts, chat, social) via SQL joins and data transformation
- Designed L1/L2/L3 issue taxonomy; deployed unsupervised ML clustering for root cause detection — reduced time-to-insight **7 days → same-day**; auto-routed mitigations to Walmart engineering and fraud teams
- Diagnosed driver retention collapse (D7 ~65% → D30 ~35% → D60 ~18%) across 4 cohorts; drove **$1.2M TCV** POC-to-deal conversion + **$9M+ Q4 pipeline**; foundation led to **$2M follow-on deal** post-departure
- Led daily cross-functional sprints (product, engineering, pre-sales, AEs); ran leadership updates directly to VP of Product — work led to direct invitation to join product team

**Government of Qatar — $32M CXM Transformation (2023)**

- Insights lead on Sprinklr's largest-ever net new deal ($32M TCV / $6.2M ARR, 5-year) — unified citizen experience platform across **40 Qatar government ministries**
- Owned PM's office dashboard product experience; drove full Arabic RTL localization; reduced **time-to-insight 2 days → 2 hours**; improved Arabic sentiment model F1 **+11%**, intuition model **+13%**
- Scaled team 6 → 14 in 3 months; onboarded and mentored **8 consultants** via structured KT; delivered **120 Arabic dashboards across 40 ministries in 4 weeks**
- Improved citizen app **7-day retention 40% → 55%**; platform contributed to Qatar's UN E-Gov Index rank **78 → 53** (25-position jump)

**Enterprise Clients — Adobe, Snapchat, Discord, Mars (2022–2023)**

- Ranked **#1 globally** among all Sprinklr Implementation Consultants within first 6 months (10/10 CSAT); **only IC of 8** promoted within 11 months
- Unified Adobe's social data (Earned / Organic / Paid, 3 schemas) via SQL pipelines — analysis cycle **4 days → 1 day (75% reduction)**; built spam detection model (Sprinklr AI Studio) — **F1 87%**
- Grew Snapchat brand engagement **+15% MoM**; reduced Discord brand reputation risk **25%** via AI hate-comment detection; identified top/bottom 10 product trends for Mars Inc.

---

## SIDE PROJECTS

### LinkRight — Founder & Product Engineer (Jun 2025 – Present)
- Building AI-native career navigation platform solo alongside full-time AmEx role; shipped **44/57 features (77%)** in 11 months; published to PyPI (`pip install linkright`); live at sync.linkright.in
- Built production-grade LLM pipeline: hybrid resume parser, fabrication guard system, 16-dimension evaluation scorecard, Oracle VPS with 9 self-hosted models + fallback LLM chain

### Navii (HeyNavii) — Beta Growth PM (2025)
- Structured beta engagement for AI-powered career navigation app; mapped **5+ user journeys**, logged **14 bugs** + **9 enhancements**, wrote onboarding guides + videos; built N8N automations + Chrome extension
- Platform grew **~2K → ~20K users** during beta period (multiple contributors — cannot claim sole ownership)

### Sukha Education — Strategy Consultant (Jan–May 2025)
- Delivered digital transformation roadmap for Chennai NGO (2,000+ students, 25+ partner institutions); Google Workspace + Slack + Salesforce rollout across 50+ volunteers — **~₹60,000 annual savings**

---

## EDUCATION

**Indian Institute of Technology (IIT) Delhi**
B.Tech, Civil Engineering | 2017–2021 | CGPA: 6.43/10

*[Any additional achievements to surface here — to be confirmed]*

---

## SKILLS

**Product:** Strategy & Roadmapping · PRD Writing · Feature Prioritization (RICE/MoSCoW) · OKR/KPI Definition · UX Research · Stakeholder Management · SAFe/Agile · PI Planning · A/B Testing · GTM Strategy

**Data & Analytics:** SQL (production-grade) · Python · BigQuery · Tableau · Mixpanel · Amplitude · PowerBI · Data Architecture & Schema Design

**AI/ML:** LLM Pipeline Design · Prompt Engineering · Fabrication Guard Systems · Evaluation Frameworks · Supervised & Unsupervised ML · NLP / Sentiment Analysis · Embedding + Retrieval Systems · Self-hosted LLMs (Ollama)

**Design & Tools:** Figma · UI/UX Prototyping · JIRA · Rally · N8N Workflow Automation · ChatGPT Enterprise · Lucidchart

---

## CERTIFICATIONS & PROGRAMS

- **GGI Fellow** · Global Governance Initiative · 2024 — Pre-MBA consulting & public policy fellowship; Impact Lab project: Sukha Education digital transformation
- **SQL · Excel · Tableau · Power BI · Python · Product Analytics** · Scaler Academy ✅
- ~~Scaler Academy — Data Science & ML~~ · In Progress — ⚠️ Do NOT include until completed.

---

## METRICS BANK
### (Confirmed, validated numbers only — never invented)

| Metric | Source | Confirmed? |
|--------|--------|------------|
| Use Case Hub adoption: ~35% → ~85% | Sprinklr teammates (post-launch) | ✅ Directional — product live, teammates confirmed |
| Use Case Hub TTV reduction: ~75% | Sprinklr teammates (post-launch) | ✅ Directional — product live, teammates confirmed |
| Walmart: $1.2M TCV POC→deal | Sprinklr | ✅ |
| Walmart: $9M+ pipeline Q4 FY24 | Sprinklr | ✅ |
| Qatar: 40% → 55% 7-day retention | Sprinklr Qatar | ✅ |
| Qatar: 2 days → 2 hours time-to-insight | Sprinklr Qatar | ✅ |
| Qatar: UN E-Gov rank 78 → 53 | Qatar/UN | ✅ |
| Qatar: Sentiment model F1 +11%, Intuition +13% | Sprinklr Qatar | ✅ |
| CRR: 10 days → 3 days speed-to-market (-70%) | AmEx | ✅ |
| CRR: 4 consecutive zero-spillover PIs | AmEx | ✅ |
| CRR: 60+ features delivered | AmEx | ✅ |
| Amex perf rating: G1L2 (highest among ~12–15 Band 30 POs in VP's org) | AmEx | ✅ |
| Amex bonus increase: 120% | AmEx | ✅ |
| Growth Hack: Top 6% (rank 21/400+ teams) | AmEx | ✅ |
| Adobe spam model F1: 87% | Sprinklr | ✅ |
| Discord hate-comment detection: -25% brand risk | Sprinklr | ✅ |
| Snapchat engagement: +15% MoM | Sprinklr | ✅ |
| Sprinklr Gold Medal Globally (rank 1) | Sprinklr | ✅ |
| Advocacy ARR: $7M → $9.8M Q2→Q3 2024 | Sprinklr | ⚠️ IN DOCUMENT — Satvik didn't own this, it was background context in the strategy doc. Do not attribute to him. |
| CDL: Product Type 136K raw → 64 categories | AmEx | ✅ |
| CDL: Industry Type 521K raw → 98 categories | AmEx | ✅ |
| LinkRight: 44/57 issues shipped (77%) solo | LinkRight | ✅ |
| LinkRight: 147-response validation survey | LinkRight | ✅ |
| LinkRight: 7,000+ cold-outreach touches pre-build | LinkRight | ✅ |
| LinkRight: 3 ICP segments defined pre-build | LinkRight | ✅ |
| Navii: User base 2K → 20K during beta (multiple contributors) | Navii | ✅ Directional — cannot claim sole ownership |
| Navii: 14 bugs + 9 enhancements logged | Navii | ✅ |
| Navii: 5+ user journeys mapped | Navii | ✅ |
| LinkedIn followers: 8–9K in 2–3 months | Personal | ✅ |
| Sukha: ₹60K annual savings, 50+ volunteers | Sukha NGO | ✅ |

*[More metrics to be confirmed through validation conversations]*

---


