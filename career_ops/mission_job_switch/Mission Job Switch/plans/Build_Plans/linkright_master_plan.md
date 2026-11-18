# Linkright — Master System Plan

**Version:** 2.0.0  
**Status:** Product Design Spec  
**Audience:** Anyone building or using the Linkright skill suite  

---

## 1. What Linkright Is

Linkright is a personal career acceleration operating system — a structured, evidence-driven intelligence layer that sits above your raw professional history and below every artifact you produce (resumes, cover letters, emails, posts, interview answers).

It is **not** a job board.  
It is **not** a resume builder.  
It is **not** a chatbot.  

It is the system that makes every career action faster, stronger, and more strategically consistent — and smarter over time.

**Target user:** Any PM (Product Manager) actively navigating a job search or building long-term career leverage.  

**Setup:** User fills in `user_setup_template.md` once. All skills read constraints, targets, and preferences from there. No personal data is hardcoded in any skill.

---

## 2. Core Design Philosophy

| Principle | Meaning |
|---|---|
| Evidence-first | Every claim traces to a real fact the user confirmed |
| Identity consistency | Signals reinforce each other across all outputs |
| Strategic, not generic | Outputs are tuned to specific roles / companies / archetypes |
| Defensible positioning | Nothing in a resume you can't explain in an interview |
| Human in the loop | Claude infers, user confirms — nothing persists without consent |
| Compounding intelligence | Each session makes the next one faster and better |
| Adaptive learning | The system learns from outcomes and improves its recommendations |
| Local-first | User's data lives in their repo, not a SaaS |
| Lean context | Skills load only what the current gate needs |
| Product-grade | Any PM should be able to use this — not just the person who built it |

---

## 3. The 8-Skill Catalogue

### 3.1 Catalogue Table

| # | Skill | Slash Command | Build Phase | Priority |
|---|---|---|---|---|
| 1 | linkright-mem | `/linkright-mem` | Phase 1 | Foundational |
| 2 | linkright-push | `/linkright-push` | Phase 1 | GitHub backbone |
| 3 | linkright-hunt | `/linkright-hunt` | Phase 2 | High |
| 4 | linkright-sync | `/linkright-sync` | Phase 2 | High (v2.0.0 exists) |
| 5 | linkright-interview | `/linkright-interview` | Phase 2 | High |
| 6 | linkright-portfolio | `/linkright-portfolio` | Phase 3 | Medium |
| 7 | linkright-social | `/linkright-social` | Phase 3 | Medium |
| 8 | linkright-companion | `/linkright-companion` | Phase 4 | Long-term |

---

### 3.2 Full Use-Case Matrix

#### `/linkright-mem` — Memory & Profile Intelligence

| Use Case | Inputs | Outputs |
|---|---|---|
| Initial profile ingestion | Resume, LinkedIn export, portfolio | Canonical fact layer |
| Diary / reflection ingestion | Free-text work reflection | Signal enrichment |
| Conflict resolution | Two conflicting documents | Resolved canonical fact |
| Signal extraction | Confirmed fact layer | Signal layer |
| Profile review | — | Full profile state |
| Memory search | Query string | Ranked facts + signals |
| Profile versioning | — | Versioned snapshot |
| Stale fact detection | — | Stale fact list |
| Identity consistency audit | Profile + target archetype | Consistency score + gaps |
| Deduplication | — | Cleaned memory |

#### `/linkright-hunt` — Job Discovery & Adaptive Matching

| Use Case | Inputs | Outputs |
|---|---|---|
| ATS probe | Company name/slug | ATS type + live job listings |
| Free API search | Role keywords + filters | Ranked job list |
| Browser passive capture | DOM signal from job page visit | Opportunity record |
| JD deep analysis | JD text | Archetype, required signals, red flags, domain |
| Profile fit score | JD + profile signals | Fit score + gap analysis |
| Shortlist probability score | JD + outcome history | Probability of getting a call |
| Manual signal enrichment | User notes ("they seem to value X") | Enriched opportunity record |
| Pipeline management | — | Kanban view by stage |
| Outcome recording | "Got shortlisted", "cleared round 2", "ghosted" | Model weight update |
| Adaptive model report | — | "Jobs like X convert best for your profile" |

#### `/linkright-sync` — Resume & Cover Letter Generation

| Use Case | Inputs | Outputs |
|---|---|---|
| Resume tailoring (HTML) | JD + profile | Width-optimized HTML resume |
| Resume tailoring (LaTeX) | JD + profile | FAANGPath .tex resume |
| Cover letter generation | JD + profile | Cover letter |
| Width optimization | HTML or .tex file | Optimized file |
| Signal balance audit | Resume + target archetype | Balance report |
| ATS scan | HTML or .tex | ATS issues list |
| AI-smell detection | Resume | Flagged bullets |
| Constraint validation | Resume | Hard constraint violations |

#### `/linkright-portfolio` — Portfolio & Proof of Work

| Use Case | Inputs | Outputs |
|---|---|---|
| Case study builder | Project facts from memory | Structured case study |
| Proof-of-thinking write-up | Target company | 400-600 word POT |
| Portfolio site generation | Case studies | GitHub Pages HTML site |
| Metrics extraction | Memory | Quantified impact table |
| Company-specific deep dive | Company name | Research brief |
| Featured project selection | Profile + target archetype | Project shortlist |

#### `/linkright-interview` — Interview Preparation

| Use Case | Inputs | Outputs |
|---|---|---|
| STAR story builder | Facts + signals from memory | STAR-L story bank |
| Question bank generation | JD + target archetype | Likely question list |
| Answer drafting | Question + profile | Draft answer |
| Constraint validation | Any answer | Hard constraint violation flags |
| Mock interview | — | Simulated Q&A transcript |
| Stress test | Story | Follow-up questions + robustness score |
| Tell-me-about-yourself | Profile + target role | 90-second intro script |
| Salary framing | User setup (CTC config) | Negotiation script |

#### `/linkright-social` — Content & Presence

| Use Case | Inputs | Outputs |
|---|---|---|
| LinkedIn post generation | Signal or topic | Voice-checked post draft |
| Content calendar | Goals + target archetypes | 4-week post plan |
| Proof-of-thinking post | Target company | POT post |
| Voice consistency check | Draft post | Voice score + edits |
| Cold outreach email | Person + role | Email draft |
| Post scheduling | Post draft | LinkedIn API call |
| Brand audit | Post history | Voice consistency report |

#### `/linkright-companion` — Daily Operating System

| Use Case | Inputs | Outputs |
|---|---|---|
| Morning briefing | Pipeline + memory | Priority task list |
| Weekly review | Week activity | Review summary + improvements |
| Decision journal | Decision text | Structured log |
| Rejection / ghosting analysis | Outcome context | Analysis + memory update |
| Offer evaluation | Offer details + user setup | Evaluation + negotiation guidance |
| Diary ingestion | Work reflection | Memory-enriched learning |
| Goal tracking | Goals + pipeline state | Progress report |

#### `/linkright-push` — GitHub Backbone

| Use Case | Inputs | Outputs |
|---|---|---|
| Push resume | HTML or PDF file | Public GitHub Pages URL |
| Pull resume | Company + role slug | Local file for editing |
| Push memory vault | Memory folder | Versioned private commit |
| Pull memory | — | Local memory files |
| Deploy portfolio | Portfolio HTML | Live portfolio URL |
| Pipeline dashboard | pipeline.json | Live Kanban + metrics page |
| Repo scaffold | — | All 3 repos created + configured |

---

## 4. System Architecture

### 4.1 Component Map

```
┌─────────────────────────────────────────────────────────────┐
│                       LINKRIGHT SYSTEM                       │
│                                                             │
│  ┌──────────────┐    ┌───────────────────────────────────┐  │
│  │ linkright-   │    │        CANONICAL MEMORY GRAPH      │  │
│  │    mem       │◄──►│  Evidence / Fact / Signal /        │  │
│  └──────────────┘    │  Interpretation / Expression       │  │
│                      └──────────────┬────────────────────┘  │
│  ┌──────────────┐                   │                        │
│  │ linkright-   │                   ▼                        │
│  │    hunt      │    ┌───────────────────────────────────┐  │
│  │              │    │     SIGNAL INTELLIGENCE LAYER      │  │
│  │  ┌─────────┐ │    │  KB taxonomy → JD extraction →    │  │
│  │  │Adaptive │◄├───►│  Profile match → Shortlist model  │  │
│  │  │ Model   │ │    └───────────────────────────────────┘  │
│  │  └─────────┘ │                                            │
│  └──────────────┘    ┌───────────────────────────────────┐  │
│                      │       GITHUB BACKBONE              │  │
│  ┌──────────────┐    │  Public: resume URLs + portfolio  │  │
│  │ linkright-   │◄──►│  Private: memory vault + pipeline │  │
│  │    push      │    │  Dashboard: Kanban + metrics       │  │
│  └──────────────┘    └───────────────────────────────────┘  │
│                                                             │
│  ┌──────────────┐    ┌───────────────────────────────────┐  │
│  │ linkright-   │    │        DETERMINISTIC TOOLS         │  │
│  │    sync      │    │  measure_width.py (HTML)           │  │
│  └──────────────┘    │  log_parser.py (LaTeX)             │  │
│                      │  ats_probe.py                      │  │
│  ┌──────────────┐    │  fit_scorer.py                     │  │
│  │ linkright-   │    │  truth_engine.py                   │  │
│  │  interview   │    └───────────────────────────────────┘  │
│  └──────────────┘                                            │
│                      ┌───────────────────────────────────┐  │
│  ┌──────────────┐    │        KNOWLEDGE BASE              │  │
│  │ linkright-   │    │  PM signal taxonomy                │  │
│  │  portfolio   │    │  Archetype requirements            │  │
│  └──────────────┘    │  JD analysis frameworks            │  │
│                      │  Industry domain knowledge         │  │
│  ┌──────────────┐    │  Interview question banks          │  │
│  │ linkright-   │    └───────────────────────────────────┘  │
│  │   social     │                                            │
│  └──────────────┘                                            │
│                                                             │
│  ┌──────────────┐                                            │
│  │ linkright-   │                                            │
│  │  companion   │                                            │
│  └──────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Memory Architecture: Hybrid (Structured Markdown + Optional Vectors)

| Layer | Storage | Retrieval Method |
|---|---|---|
| Evidence | `memory/evidence/*.md` | File read |
| Facts | `memory/facts.md` (YAML blocks) | Grep + LLM rerank |
| Signals | `memory/signals.md` (YAML blocks) | Grep + LLM rerank |
| Interpretations | `memory/interpretations/<archetype>.md` | File read by archetype |
| Expressions | `memory/expressions/*.md` | Grep + keyword |
| Outcome log | `memory/outcomes.json` | JSON parse |
| Vectors (optional) | `memory/vectors/facts.db` (sqlite-vec) | ANN search fallback |

**Why structured markdown over pure vector RAG:**  
- No embedding server required — fully local/offline  
- Fully explainable (show exact matching lines)  
- Fast enough at PM career scale (<500 facts)  
- Add vectors later when volume warrants  
- Grep is deterministic; embeddings are probabilistic

### 4.3 Lean Context Architecture

Every skill follows this file layout:

```
skills/linkright-<name>/
├── SKILL.md              ← Lean: pipeline, gates, load map, hard rules only
├── references/
│   ├── ref_01_<topic>.md ← loaded at Gate X only
│   └── ref_02_<topic>.md ← loaded at Gate Y only
└── scripts/
    └── <tool>.py         ← deterministic computation only
```

**Rule: SKILL.md never exceeds 400 lines. Deep knowledge lives in `references/`.**

### 4.4 User Config Architecture

No skill hardcodes any personal data. All personal constraints, targets, and preferences are read from the user's `user_setup.md` (filled during onboarding, stored in private repo).

```
On first run of any skill:
→ Check if user_setup.md is loaded
→ If not: prompt user to complete onboarding (/linkright-mem onboard)
→ If yes: read relevant sections (CTC only for interview/companion, constraints for all, etc.)
```

This makes the skill system portable — any PM can use it without modifying any skill files.

### 4.5 Goal Loop (Karpathy-Style)

Used by skills with iterative output improvement:

```
Set /goal
    │
    ▼
Worker Turn (tools, edits, generation)
    │
    ▼
Judge Turn (reads transcript only — no tools, pure evaluation)
    │
    ▼
Condition met?
 ├─ Yes → Clear goal, report result
 └─ No  → Worker loop again (max 5 iterations then report blocker)
```

Used by: `linkright-sync` (width loop), `linkright-interview` (answer quality), `linkright-social` (voice loop)

---

## 5. GitHub Backbone Architecture

### Three-Repo Structure

```
GitHub Account
├── [PUBLIC]  linkright-resume
│   ├── index.html                    ← latest resume
│   └── roles/<role-slug>/
│       ├── index.html                ← role-specific version
│       └── resume.pdf
│
├── [PUBLIC]  linkright-portfolio
│   ├── index.html                    ← portfolio home
│   ├── cases/<case-slug>.html
│   └── dashboard/index.html          ← pipeline Kanban + metrics
│
└── [PRIVATE] linkright-memory
    ├── user_setup.md                 ← personal config (private)
    ├── memory/
    │   ├── facts.md
    │   ├── signals.md
    │   ├── outcomes.json             ← shortlist/interview/offer log
    │   ├── evidence/
    │   ├── interpretations/
    │   └── expressions/
    ├── pipeline.json
    └── diary/
```

---

## 6. Cross-Skill Data Flows

```
linkright-mem
    ├──► linkright-sync (signals + facts → resumes)
    ├──► linkright-interview (signals + facts → STAR stories)
    ├──► linkright-portfolio (facts → case studies)
    └──► linkright-social (signals → posts)

linkright-hunt
    ├──► linkright-sync (JD → resume tailoring trigger)
    ├──► linkright-interview (JD → question bank)
    └──► linkright-companion (pipeline state → daily briefing)

linkright-push
    ├──► stores linkright-sync outputs (resume URLs)
    ├──► stores linkright-portfolio outputs (portfolio site)
    ├──► stores linkright-mem outputs (memory vault)
    └──► hosts dashboard fed by linkright-hunt (pipeline.json)

linkright-companion
    ← reads from: linkright-hunt (pipeline) + linkright-mem (memory)
    → routes diary entries to: linkright-mem
    → routes rejection analysis to: linkright-hunt (outcome recording)
```

---

## 7. The Adaptive Signal Model (Hunt Intelligence)

This is the compounding intelligence layer — the part that gets smarter over time.

### Two-Score System

Every opportunity gets two independent scores:

**Score A: Profile Fit Score**  
How well does your profile match what this job requires?  
Computed from: JD signal extraction × profile signal strength  
This is static — it doesn't learn from outcomes.

**Score B: Shortlist Probability Score**  
Based on jobs you've applied to before — what does your actual shortlisting history say about how likely you are to get a call for this type of job?  
Computed from: outcome history × job similarity  
This is adaptive — it learns every time you record an outcome.

**Combined: Opportunity Score**  
Weighted combination — user can tune the weight (default: 50/50)

### Why Separate?

A job can have high fit but low shortlist probability (e.g. you're qualified but the company always wants internal hires). Or low fit but high shortlist probability (you consistently get calls from this archetype even when you feel underqualified). Separating them gives you better prioritization intelligence.

### Learning Loop

```
Apply to job → Record outcome (shortlisted / ghosted / rejected early)
    │
    ├─ Shortlisted: job's signals get weight boost in shortlist model
    ├─ Cleared interview stage: stronger boost to relevant signals
    ├─ Ghosted after 14 days: small negative signal
    └─ Rejected early: moderate negative signal
    
Over time:
→ System identifies: "You consistently get shortlisted for roles requiring
  systems_thinking + enterprise_workflow + ambiguity_handling"
→ Future jobs with those signal clusters get higher shortlist probability
→ System also identifies: "You rarely get called for roles emphasizing
  growth_experimentation as primary signal — deprioritize those"
```

See `linkright_hunt_plan.md` for full model design.

---

## 8. Build Sequence

### Phase 1 — Foundation

1. **`linkright-mem`** — Build the memory substrate first. Without memory, all other skills work from raw resume paste (fragile, unrepeatable).
2. **`linkright-push`** — Establish the GitHub backbone. Every other skill needs somewhere to persist and version its outputs.

### Phase 2 — Core Workflow

3. **`linkright-hunt`** — Job discovery + adaptive matching. Start simple (fit score only), add shortlist model after first 10 applications.
4. **`linkright-sync`** (already v2.0.0) — Upgrade to pull from mem instead of requiring paste.
5. **`linkright-interview`** — STAR bank + mock interview.

### Phase 3 — Amplification

6. **`linkright-portfolio`** — Case studies + proof-of-thinking.
7. **`linkright-social`** — Content calendar + voice system.

### Phase 4 — Intelligence Layer

8. **`linkright-companion`** — Daily briefing + longitudinal tracking. Depends on all other skills having data.

---

## 9. Onboarding Flow (New User)

```
Step 1: Fill user_setup_template.md
        → compensation, targets, constraints, do-not-mention list

Step 2: /linkright-mem onboard
        → loads user_setup.md into memory
        → ingests resume/LinkedIn
        → confirms facts
        → derives signals
        → computes initial identity score vs target archetype

Step 3: /linkright-push scaffold
        → creates 3 GitHub repos
        → enables GitHub Pages
        → pushes first memory commit

Step 4: /linkright-sync (ready to use)
        → pulls from memory automatically

Step 5: /linkright-hunt first-search
        → ATS probe for tier-1 target companies
        → returns first batch of opportunities with fit scores

Step 6: Apply, record outcomes, model starts learning
```

---

## 10. Metrics to Track (Product-Level)

| Metric | Definition |
|---|---|
| Memory completeness | % of career facts confirmed in memory |
| Signal coverage | % of target archetype signals present at medium+ strength |
| Shortlist rate | Applications sent / shortlisted (track over time) |
| Shortlist model accuracy | Did the model correctly predict high-probability shortlists? |
| Interview conversion | Screenings → interviews |
| Offer rate | Applications → offers |
| Resume generation speed | JD paste → send-ready resume time |
| Width optimization coverage | % of bullets at 95-100% fill |
| Voice consistency | Social posts passing voice check (≥7/10) |

---

## 11. Individual Skill Plan Files

| File | Skill |
|---|---|
| `linkright_mem_plan.md` | Memory & Profile Intelligence |
| `linkright_hunt_plan.md` | Job Discovery & Adaptive Matching |
| `linkright_sync_plan.md` | Resume & Cover Letter |
| `linkright_portfolio_plan.md` | Portfolio & Proof of Work |
| `linkright_interview_plan.md` | Interview Preparation |
| `linkright_social_plan.md` | Content & Presence |
| `linkright_companion_plan.md` | Daily Operating System |
| `linkright_push_plan.md` | GitHub Backbone |
| `user_setup_template.md` | Per-user configuration template |

---

*This is the root architectural reference for all Linkright skill builds.*  
*When in doubt about cross-skill dependencies, goal loops, or user config, start here.*
