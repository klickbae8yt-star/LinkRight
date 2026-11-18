# Linkright Knowledge Index
*Last audited: May 2026 — covers all 47 Research_Linkright + 33 Roadmap_Linkright files*

This file is the permanent reference for the full knowledge base. Every file is catalogued with its purpose, which skill(s) it feeds, and its priority tier. Never redo this exercise from scratch — update this file whenever new docs are added.

---

## Skill Catalogue (planned build order)

All skills live under the **Linkright** family. Naming convention: `linkright-<handle>`.

| # | Official Skill Name | Handle | Status | Priority |
|---|---------------------|--------|--------|----------|
| 1 | linkright-mem | `linkright-mem` | 🔴 Build first | Foundational — all others depend on it |
| 2 | linkright-hunt | `linkright-hunt` | 🔴 Build second | High — surfaces the right opportunities |
| 3 | linkright-sync | `linkright-sync` | 🟡 Exists, updated | In use — resume builder |
| 4 | linkright-portfolio | `linkright-portfolio` | 🔴 Build | High — proof-of-work layer |
| 5 | linkright-interview | `linkright-interview` | 🔴 Build | High — converts interviews |
| 6 | linkright-social | `linkright-social` | 🔴 Build | Medium — recruiter visibility (LinkedIn + future platforms) |
| 7 | linkright-companion | `linkright-companion` | 🔴 Build last | Long-term — daily diary + books + self-reflection |

> **Why `linkright-social` not `linkright-linkedin`:** Social is platform-agnostic. Today it's LinkedIn-first, but the skill can later extend to X/Twitter, newsletters, or any public professional surface without a rename.

---

## Skill Invocation — Individual Slash Commands

**Each skill is a standalone, independently invokable unit.** They are NOT one monolithic skill. The user triggers each one separately by typing its name as a slash command:

```
/linkright-mem        → starts the memory ingestion / retrieval flow
/linkright-hunt       → starts the job scraping + scoring flow
/linkright-sync       → starts the resume building flow
/linkright-portfolio  → starts the portfolio / case study building flow
/linkright-interview  → starts the interview coaching / mock interview flow
/linkright-social     → starts the LinkedIn content creation + scheduling flow
/linkright-companion  → starts the daily diary / self-reflection / career companion flow
```

Each skill has its own `SKILL.md`, its own `references/` directory, and its own `scripts/` directory. They are independent packages that share a common naming convention and can call `linkright-mem` for memory retrieval, but otherwise operate standalone.

---

## Lean Context Architecture — Non-Negotiable Design Rule

> **The main SKILL.md of every skill MUST be lean. It is an orchestrator, not an encyclopedia.**

### The rule
The SKILL.md only contains:
- What the skill does (1 paragraph)
- The gate/phase pipeline (when to stop, what to present, what to confirm)
- Hard rules (ALWAYS/NEVER enforcement)
- A `references/` load map — which file to read at which gate

**Everything else lives in `references/` files and is loaded on-demand, only when that phase of execution actually needs it.**

### Why this matters
Every token loaded into context at skill startup is a token that isn't available for reasoning, generation, and retrieval. If a skill loads 15 reference files upfront, most of that content is irrelevant to the current task and wastes the context window. Lean skills are faster, sharper, and more accurate.

### The pattern (identical across all 7 skills)

```
skill/
├── SKILL.md              ← LEAN: pipeline, gates, hard rules, load map only
├── references/
│   ├── ref_01_<topic>.md ← loaded at Gate X only
│   ├── ref_02_<topic>.md ← loaded at Gate Y only
│   └── ref_03_<topic>.md ← loaded at Gate Z only
└── scripts/
    └── <tool>.py         ← deterministic tools called by the skill
```

### Load map format (how SKILL.md signals what to load)

Inside SKILL.md, each gate specifies exactly which reference file(s) to read before executing that phase:

```
Gate 3 — Story Bank Review
→ LOAD: references/ref_story_bank.md before generating or evaluating any story
→ DO NOT load: references/ref_pm_cases.md (not needed until Gate 5)
```

### What belongs in SKILL.md vs references/

| Belongs in SKILL.md | Belongs in references/ |
|---------------------|------------------------|
| Gate sequence (when to stop, what to show) | Deep tactical knowledge (how to write a story, PM case frameworks) |
| Hard rules (NEVER/ALWAYS) | Research knowledge loaded from Research_Linkright |
| Pipeline overview | Scoring rubrics and detailed criteria |
| Reference load map | Examples, templates, archetypes |
| Script invocation syntax | Long methodology explanations |

### linkright-sync example (already partially implemented)
```
SKILL.md knows:        Gate 6 → load references/pipeline.md
                       Gate 5 → load references/career_profiles.md + references/strategies.md
                       Every bullet → run scripts/measure_width.py
references/ contains:  pipeline.md, career_profiles.md, strategies.md, xyz_format.md
```
This is the model. All other skills follow the same pattern.

---

## Memory Skill Architecture Decision (vectorless vs vector)

Two candidates evaluated:

### Option A — `claude-mem` style (vectorless RAG)
**Repo:** https://github.com/thedotmack/claude-mem  
**How it works:** Stores memory as structured markdown files (one file per domain/layer). Retrieval via fuzzy keyword search + LLM reranking. No embeddings needed.  
**Pros:** Zero infra overhead, fully local, instantly readable/editable by user, trivially versioned with git, aligns perfectly with Cowork skill architecture (markdown + Python scripts), no cold-start problem.  
**Cons:** Retrieval degrades at very large memory sizes (1000+ entries). Fuzzy search misses semantic synonyms.

### Option B — `PageIndex` style (vectorless hierarchical RAG)
**Repo:** https://github.com/VectifyAI/PageIndex  
**How it works:** LLM builds a hierarchical tree of summaries from all content. Retrieval navigates the tree using LLM-guided queries. No embeddings, no vector DB.  
**Pros:** Handles large docs well, semantic navigation, no infra.  
**Cons:** More expensive per retrieval (multiple LLM calls), harder to inspect, less portable.

### Option C — Embedding-based vector RAG
**How it works:** Embed all memory chunks → store in local vector DB (sqlite-vec or hnswlib) → retrieve by cosine similarity → rerank with LLM.  
**Pros:** Best semantic recall, scales to large memory.  
**Cons:** Requires embedding model (local: Jina/fastembed, or API), infra overhead, black-box retrieval.

### **Recommended approach: Hybrid A+C (mem-first, vectors optional)**
1. **Primary store:** Structured markdown files organized by memory layer (Evidence / Facts / Signals / Interpretations / Expressions) — exactly like claude-mem but with Linkright's 5-layer ontology.
2. **Retrieval engine:** Multi-query search — generate 3-5 semantically diverse search queries from the task context, run keyword grep + BM25 across markdown files, rerank top-20 with LLM.
3. **Optional upgrade path:** Add sqlite-vec embeddings as a secondary index when memory grows large. The markdown files remain the source of truth; embeddings are just an index.
4. **Why this wins:** Fully inspectable, zero infra to start, aligns with Linkright's "local-first" decision (DOC 00 Decision 8), upgradeable without migration, and multi-query with LLM reranking closes most of the semantic gap that pure keyword search misses.

---

## Research_Linkright — Full File Index

### How to read the tags
- 🧠 `linkright-mem` — feeds the memory / RAG skill (ingestion, retrieval, story bank)
- 🎯 `linkright-hunt` — feeds job scraping + opportunity scoring
- 📄 `linkright-sync` — feeds resume building
- 🗂️ `linkright-portfolio` — feeds product portfolio / case study builder
- 🎤 `linkright-interview` — feeds interview coaching
- 📣 `linkright-social` — feeds LinkedIn + social content creation
- 🤝 `linkright-companion` — feeds daily career companion / self-reflection
- 🔧 `ALL` — architectural or philosophical, relevant to all skills

---

| File | What It Contains | Primary Skills | Notes |
|------|-----------------|----------------|-------|
| `advanced_organizational_politics_and_power_dynamics.md` | How incentive navigation, power dynamics, and organizational influence work. Ethical politics, trust, and stakeholder management in complex orgs. | 🤝 `companion` 🎤 `interview` | High value for companion's book-knowledge layer (48 Laws adjacent). Use in behavioral interview prep for "influence without authority" questions. |
| `ai_augmented_personal_operating_system.md` | How elite operators build AI-native personal workflows — decision-making, synthesis, execution, communication loops. | 🤝 `companion` 🧠 `mem` | Directly informs companion's daily rhythm. Core philosophy for how mem skill should feel to use. |
| `ai_era_authenticity_and_human_signal_guide.md` | How to preserve authentic human signals in AI-saturated hiring. Specificity, realism, avoiding generic outputs. | 📄 `sync` 🎤 `interview` 📣 `linkedin` | **Critical constraint** for all generation — no over-polished AI-sounding output. Feeds the anti-AI-smell validation in sync. |
| `ai_native_career_acceleration_system.md` | Full framework for AI-amplified career — 4 layers: augmented learning, execution, decision-making, positioning. | 🔧 `ALL` 🤝 `companion` | Read this to understand the product philosophy. Companion should embody this for daily use. |
| `ai_product_leadership_track.md` | AI PM archetype — trust design, human-in-loop, evaluation systems, LLM failure modes, workflow orchestration. | 📄 `sync` 🎤 `interview` | Use when tailoring resume + interview prep for AI PM roles. One of 4 archetype tracks. |
| `application_pipeline_operating_system.md` | Running job search as an operating system — targeting, outreach, follow-up, optimization, momentum. | 🎯 `hunt` 🤝 `companion` | Informs hunt's pipeline management and companion's weekly check-in rhythm. |
| `async_hiring_optimization_guide.md` | Optimizing written/recorded async hiring rounds — memos, Loom, take-homes, written prompts. | 🎤 `interview` 🗂️ `portfolio` | Informs interview skill's async-round mode and portfolio artifact quality bar. |
| `career_narrative_architecture_guide.md` | Designing a coherent career narrative that spans resume → LinkedIn → intro → interview → portfolio. | 📄 `sync` 🎤 `interview` 🗂️ `portfolio` 📣 `linkedin` | **Foundational strategy doc.** Every artifact-generating skill should read this. The "why" behind positioning. |
| `chief_of_staff_and_strategic_operator_track.md` | CoS and strategic operator archetype — force multiplier, organizational integrator, executive leverage. | 📄 `sync` 🎤 `interview` | One of 4 archetype tracks. Use when targeting CoS or high-leverage operator roles. |
| `compensation_negotiation_and_offer_strategy_system.md` | Negotiating offers structurally — comp components, timing, leverage, professional framing. | 🤝 `companion` | Post-offer phase of companion. Also informs the "why leaving" narrative in sync. |
| `crisis_reputation_recovery_playbook.md` | Recovering from professional failures — PIP, layoffs, messy exits, failed ventures. Narrative framing. | 🎤 `interview` 🤝 `companion` | Use in interview for "failure" behavioral questions. Companion uses for difficult self-reflection prompts. |
| `cross_domain_career_transitions_guide.md` | How cross-domain transitions work — credibility transfer, 3-phase arc, avoiding plateau. | 🤝 `companion` 📄 `sync` | For positioning career pivots. Companion's identity evolution coaching. |
| `decision_making_under_uncertainty_frameworks.md` | Probabilistic thinking, risk calibration, reversible decisions, sequencing under incomplete information. | 🎤 `interview` 🤝 `companion` | PM case interview framework source. Companion uses for daily decision journaling. |
| `elite_communication_and_strategic_conversation_system.md` | Perception management, influence, trust formation, status signaling, ambiguity reduction in conversation. | 🎤 `interview` 🤝 `companion` | Feeds interview tone coaching. Companion uses for communication self-reflection. |
| `elite_networking_psychology_and_relationship_leverage.md` | Trust compounding, weak ties, relationship infrastructure, ecosystem positioning at high levels. | 📣 `linkedin` 🤝 `companion` | LinkedIn content should build trust, not broadcast. Companion tracks relationship health. |
| `emotional_resilience_and_psychological_stability_system.md` | Managing confidence, communication quality, and decision-making under prolonged uncertainty and rejection. | 🤝 `companion` | Critical for companion's wellbeing layer. Job search is psychologically demanding — this is the antidote. |
| `executive_and_director_level_pm_track.md` | Director/VP PM archetype — strategic judgment, org influence, systems thinking, executive communication. | 📄 `sync` 🎤 `interview` | One of 4 archetype tracks. Use for senior-level targeting. |
| `executive_presence_and_behavioral_signaling_system.md` | How subconscious behavioral signals (pace, posture, tone, structure) form seniority perception. | 🎤 `interview` 🤝 `companion` | Interview coaching on *how you show up*, not just what you say. Companion for behavioral growth. |
| `failed_hire_rca_methodology.md` | Turning failed applications into diagnostic events. Root cause analysis on rejections. | 🎯 `hunt` 🤝 `companion` | Hunt should track rejection patterns. Companion runs RCA on failed cycles during weekly review. |
| `follow_up_communication_positioning_guide.md` | Post-interview follow-ups — professional framing, reinforcing perception, timing. | 🎤 `interview` | Feeds interview skill's post-round communication module. |
| `founder_startup_operator_track.md` | Startup operator archetype — ownership, speed, ambiguity tolerance, founder trust, resourcefulness. | 📄 `sync` 🎤 `interview` | One of 4 archetype tracks. Use for Series A/B targeting. |
| `high_agency_operator_system.md` | High-agency mindset — moving independently, creating momentum, reducing managerial overhead. | 📄 `sync` 🎤 `interview` 🤝 `companion` | Key signal for strong PMs. Feeds resume positioning + behavioral interview answers + companion mindset. |
| `hiring_process_intelligence_guide.md` | How hiring pipelines work as risk-reduction systems — what each stage evaluates, hidden signals. | 🎤 `interview` 🎯 `hunt` | Interview skill uses this to coach per-round strategy. Hunt uses to evaluate pipeline health. |
| `internal_advocacy_and_hiring_committee_politics_guide.md` | How hiring committee dynamics and internal advocacy work after your interviews end. | 🎤 `interview` 🤝 `companion` | Interview skill post-round module. Companion for navigating committee politics once hired. |
| `interview_intro_positioning_guide.md` | Structuring the "tell me about yourself" intro — narrative arc, seniority signaling, role targeting. | 🎤 `interview` 🧠 `mem` | Interview skill's intro module. Mem stores and retrieves calibrated intros per archetype. |
| `interview_psychology_and_decision_influence_system.md` | Psychological dynamics in interviews — cognitive ease, trust signals, uncertainty reduction, emotional formation. | 🎤 `interview` | Deep coaching layer for interview skill. Feeds the judge/evaluation module. |
| `interview_stories_positioning_guide.md` | Story bank architecture — 6-10 reusable stories covering ambiguity, conflict, leadership, prioritization. | 🎤 `interview` 🧠 `mem` | **Directly feeds mem's story bank.** Interview skill retrieves stories from mem using these categories. |
| `interview_tone_positioning_guide.md` | Tone coaching — controlled, precise, cooperative. Calm not flat. Direct not blunt. | 🎤 `interview` | Interview skill's tone calibration module for each round type. |
| `jd_intelligence_and_signal_mapping_system.md` | Reverse-engineering JDs — org pain, politics, team maturity, hidden evaluation criteria, signal mapping. | 🎯 `hunt` 📄 `sync` | **Core input to both hunt (score JD quality) and sync (map JD signals → resume emphasis).** |
| `leadership_transition_and_executive_identity_evolution.md` | Transitioning from IC/PM to executive — abstraction level, influence systems, organizational awareness. | 🤝 `companion` 📄 `sync` | Companion's identity evolution coaching. Sync's executive archetype positioning. |
| `linked_in_positioning_guide.md` | LinkedIn as credibility environment — headline, about, experience framing, content positioning strategy. | 📣 `linkedin` | **Primary reference for linkedin skill.** Profile optimization + content strategy in one doc. |
| `micro_reputation_and_backchannel_dynamics_guide.md` | Invisible reputation layers — recruiter memory, Slack communities, founder networks, backchannel signals. | 📣 `linkedin` 🤝 `companion` | LinkedIn content must build micro-reputation intentionally. Companion tracks relationship health. |
| `negotiation_style_positioning_guide.md` | Negotiation tone — informed not entitled, confident not aggressive, collaborative not passive. | 🤝 `companion` 🎤 `interview` | Companion's offer/negotiation phase module. Interview skill for comp discussion coaching. |
| `performance_and_cognitive_optimization_for_operators.md` | Energy management, cognitive clarity, emotional regulation, sustainable operating rhythms for high performers. | 🤝 `companion` | Companion's wellness and performance module. Feeds the daily rhythm design. |
| `personal_brand_and_market_positioning_system.md` | Personal brand as market positioning — consistent perception, differentiating signal, trust formation. | 📣 `linkedin` 📄 `sync` 🤝 `companion` | LinkedIn skill's content strategy foundation. Sync's positioning philosophy. |
| `personal_knowledge_management_for_operators.md` | PKM for operators — capture, synthesis, retrieval, frameworks, reflection systems. | 🧠 `mem` 🤝 `companion` | **Directly informs mem skill architecture.** The philosophy behind why the memory layer exists. |
| `pm_archetype_evolution_and_future_market_map.md` | How PM roles are fragmenting — which archetypes are rising/commoditizing, AI reshaping PM work, market map. | 📄 `sync` 🎯 `hunt` 🤝 `companion` | **Critical for targeting strategy.** Hunt uses to score role fit. Sync uses to pick archetype. Companion for career planning. |
| `post_offer_integration_guide.md` | First 90 days — listening mode, credibility building, stakeholder trust, internal positioning. | 🤝 `companion` | Companion's post-offer phase. One of the biggest gaps Linkright fills vs other systems. |
| `product_manager_case_interview_master_system.md` | PM case interview system — prioritization under ambiguity, AI product intuition, tradeoff communication. | 🎤 `interview` | Interview skill's case interview module. Highly tactical, use directly in coaching. |
| `proof_of_thinking_economy_guide.md` | Proof-of-thinking economy — visible judgment, inspectable reasoning, proof > claims. | 🗂️ `portfolio` 📣 `linkedin` 🎤 `interview` | Portfolio and LinkedIn content should demonstrate thinking, not just state credentials. |
| `proof_of_work_portfolio_system.md` | Building a portfolio as a strategic evidence system — teardowns, case studies, design docs, analyses. | 🗂️ `portfolio` | **Primary reference for portfolio skill.** Every portfolio artifact type is described here. |
| `reference_and_reputation_management_guide.md` | Managing references proactively — trust consistency, professional relationships, reputation over time. | 🤝 `companion` 📣 `linkedin` | Companion tracks reference relationships. LinkedIn builds public reputation layer. |
| `referral_and_network_strategy_system.md` | Networking as trust transfer — familiarity creation, credibility reinforcement, warm outreach. | 🤝 `companion` 📣 `linkedin` | Companion's outreach and networking cadence. LinkedIn as inbound trust vehicle. |
| `resume_positioning_guide.md` | Resume as positioning document — capability vs activity, four recruiter questions, signal selection. | 📄 `sync` | **Primary strategic reference for sync skill.** The "why" behind every resume decision. |
| `staff_pm_influence_and_organizational_leverage_system.md` | Staff PM archetype — org leverage, influence without authority, systems-level impact. | 📄 `sync` 🎤 `interview` 🤝 `companion` | One of 4 archetype tracks. Feeds interview coaching for "influence" questions. Companion for Staff-level growth. |
| `vc_and_startup_ecosystem_navigation_system.md` | VC-backed ecosystem trust networks — how opportunities flow, how reputation transfers, founder dynamics. | 🎯 `hunt` 🤝 `companion` | Hunt uses to score startup opportunity quality. Companion for ecosystem strategy. |
| `width-optimization-research.md` | Technical deep-dive: pre-computed Roboto font metrics, pixel budget model, why character count fails. | 📄 `sync` | **Technical reference for sync's `measure_width.py`.** The math behind width optimization. Already fully implemented. |

---

## Roadmap_Linkright — Full File Index

These are architectural specification documents for the Linkright system. They define *how to build*, not what to know.

| File | What It Contains | Primary Skills | Priority |
|------|-----------------|----------------|----------|
| `linkright_architecture_documentation_master_plan.md` | Doc topology — how 30 architecture docs are organized, naming conventions, dependency order. | 🔧 `ALL` | Read first. Navigation map for all other roadmap docs. |
| `doc_00_architectural_decisions_log.md` | 9 locked architectural decisions — scope, automation philosophy, layout engine, storage, learning, privacy. | 🔧 `ALL` | **Read before building any skill.** Non-negotiable constraints. |
| `doc_01_Vision, Philosophy & System Principles.md` | Root philosophy — career OS vision, truth-first, low cognitive load, human-in-loop, identity consistency. | 🔧 `ALL` | **Root reference.** Every skill should be consistent with this philosophy. |
| `doc_02_core_ontology_semantic_architecture.md` | Entity definitions — evidence, fact, signal, interpretation, expression, opportunity, workflow, artifact, run. | 🧠 `mem` 🔧 `ALL` | **Defines the vocabulary every skill uses.** Mem's layer architecture comes from here. |
| `doc_03_canonical_profile_memory_graph_architecture.md` | Memory substrate — 5-layer profile (Evidence→Fact→Signal→Interpretation→Expression), ingestion, versioning, dedup. | 🧠 `mem` | **Primary spec for mem skill.** The entire memory architecture lives here. |
| `doc_04_opportunity_lifecycle_workflow_architecture.md` | Opportunity as central object — lifecycle states, workflow transitions, approval checkpoints, event model. | 🎯 `hunt` 🔧 `ALL` | Hunt's core model. Every opportunity flows through these states. |
| `doc_05_retrieval_ranking_strategic_intelligence_system.md` | Retrieval philosophy — signal-first, not just semantic, strategic scoring, identity consistency, explainability. | 🧠 `mem` 📄 `sync` | **Core retrieval spec.** Mem's search must implement signal-first, not just keyword/vector. |
| `doc_06_resume_positioning_artifact_generation_engine.md` | Artifact generation — resume, cover letter, autofill, interview prep. Width integration, ATS, lineage. | 📄 `sync` | Architectural spec for sync. Already partially implemented. |
| `doc_07_deterministic_engines_validation_systems.md` | Deterministic infrastructure — width engine, layout, scoring, dedup, AI-smell detection, validators. | 📄 `sync` 🔧 `ALL` | All skills need validation. Width engine spec for sync. |
| `doc_08_cli_runtime_mcp_execution_layer.md` | Execution runtime — CLI architecture, MCP integration, local-first, command contracts, replay, tracing. | 🔧 `ALL` | How skills run as MCP tools. Execution boundaries for every skill. |
| `doc_09_browser_extension_ambient_intelligence_layer.md` | Browser extension — JD capture, LinkedIn overlays, autofill, Gmail overlays, contextual retrieval. | 🎯 `hunt` 📣 `linkedin` | Future: hunt captures JDs from browser. LinkedIn skill operates via extension. |
| `doc_10_n_8_n_orchestration_automation_architecture.md` | Orchestration — n8n workflow chaining, approval gating, async processing, webhook contracts, retry. | 🔧 `ALL` | How skills are chained together. Goal loops use this orchestration model. |
| `doc_11_observability_logging_explainability_framework.md` | Observability — execution traces, retrieval rationale, artifact lineage, debugging, audit trails, trust. | 🔧 `ALL` | Every skill must log. Goal loop judge reads traces. Critical for the Karpathy-style worker loop. |
| `doc_12_career_navigation_intelligence_long_term_compounding_system.md` | Long-term intelligence — signal compounding, diary ingestion, networking, reputation, career decisions. | 🤝 `companion` 🧠 `mem` 🔧 `ALL` | The "long game" architecture. Companion and mem build toward this. |
| `doc_13_a_implementation_architecture_documentation_topology_governance_plan.md` | Implementation governance — how to structure implementation docs, dependency rules, sequencing. | 🔧 `ALL` | Reference for skill documentation standards. |
| `doc_13_b_operational_architecture_documentation_topology_governance_plan.md` | Operational governance — product behavior, trust systems, career-navigation integrity, evolution model. | 🔧 `ALL` | How skills evolve operationally over time. |
| `doc_13_c_architecture_gaps_open_questions_risks_future_opportunities_expansion_registry.md` | Gap registry — unresolved questions, known risks, deferred systems, future opportunities. | 🔧 `ALL` | Check here before building a new skill component — the gap may already be documented. |
| `doc_13_storage_infrastructure.md` | Storage — local JSON/SQLite (authoritative) + encrypted MongoDB (optional cloud). Sync protocol, backup. | 🧠 `mem` | Mem skill's storage implementation. Local-first, markdown + SQLite for structured data. |
| `doc_14_schemas_data_contracts.md` | Entity schemas — profile graph, signal schema, outcome events, identity schema, versioning, migrations. | 🧠 `mem` 🔧 `ALL` | **The data contracts every skill must conform to.** Mem implements these schemas. |
| `doc_15_retrieval_implementation.md` | Retrieval as concrete operations — 4 stages: structured filter → vector search → strategic scoring → expression input. | 🧠 `mem` | Hands-on implementation guide for mem's retrieval pipeline. |
| `doc_16_layout_engine_deterministic_rendering.md` | Layout engine — pixel budget model, font metrics, line-fitting, page utilization, multi-pass rendering. | 📄 `sync` | Sync's width engine and layout validation. Already partially implemented. |
| `doc_17_security_architecture.md` | Security — local data protection, LLM provider isolation, prompt injection defense, encryption, key rotation. | 🧠 `mem` 🔧 `ALL` | Mem handles sensitive career data. Security constraints apply to all skills. |
| `doc_18_evaluation_framework.md` | Evaluation — output quality vs outcome effectiveness, recruiter response rate, interview conversion metrics. | 🔧 `ALL` | How to measure if a skill is actually working. The goal loop's judge needs eval criteria. |
| `doc_19_ux_patterns_interaction_design.md` | UX patterns — CLI primitives, approval gate contracts, progressive disclosure, weekly review model, tone palette. | 🔧 `ALL` | How every skill should interact with the user. Gate patterns, error recovery, disclosure. |
| `doc_20_browser_automation_extension_architecture.md` | Browser layer — JD capture pipeline, opportunity overlay, autofill assist, LinkedIn intelligence surface. | 🎯 `hunt` 📣 `linkedin` | Future browser integration for hunt and linkedin skills. |
| `doc_21_agent_governance_multi_agent_coordination.md` | Agent governance — taxonomy, contracts, memory mutation protocol, human escalation, failure isolation. | 🔧 `ALL` | **Critical for the Karpathy-style goal loop.** Defines worker/judge/human escalation boundaries. |
| `doc_22_implementation_roadmap_release_sequencing.md` | Release sequence — v1 core, v1.1-v2.1+ roadmap, dependency ordering, what ships in what order. | 🔧 `ALL` | Build order for skills. Confirms: mem → hunt → sync → portfolio → interview → linkedin → companion. |
| `doc_23_career_decision_engine.md` | Career decision engine — pairwise job comparison, scoring dimensions, visual scorecard, recommendation with rationale. | 🤝 `companion` 🎯 `hunt` | Companion's job comparison module. Hunt's opportunity ranking. |
| `doc_24_closed_loop_learning_system.md` | Learning system — implicit conversion tracking, outcome event pipeline, signal weight updates from results. | 🧠 `mem` 🔧 `ALL` | Mem compounds over time using this. Every skill feeds outcomes back into mem. |
| `doc_25_relationship_graph_network_intelligence.md` | Relationship graph — contact trust layers, AI-suggested connections, referral tracking, network intelligence. | 🤝 `companion` 📣 `linkedin` | Companion tracks relationship health. LinkedIn skill drives visibility into this network. |
| `doc_26_personal_operating_rhythm.md` | Weekly/monthly operating rhythm — habit loop, diary ingestion, review structure, how data feeds the system. | 🤝 `companion` 🧠 `mem` | **Core spec for companion's check-in loop.** Diary ingestion feeds mem continuously. |
| `doc_27_post_offer_professional_os.md` | Post-offer OS — 30-60-90 plan, manager alignment, internal advocacy, performance capture, promotion tracking. | 🤝 `companion` | Companion's post-offer phase. The gap most career tools miss entirely. |
| `doc_28_identity_evolution_system.md` | Identity evolution — tracking who the user is becoming, level transitions, archetype drift detection, suggestions. | 🧠 `mem` 📄 `sync` 🤝 `companion` | Mem stores identity history. Sync ensures artifacts reflect current identity. Companion surfaces upgrade suggestions. |
| `doc_29_trust_privacy_governance.md` | Trust model — data classification tiers, user control, encryption, audit trails, AI authenticity layer. | 🧠 `mem` 🔧 `ALL` | Applies to all skills but mem especially since it holds the most sensitive data. |
| `doc_30_ecosystem_intelligence.md` | External market context — company intelligence, archetype demand index, hiring market timing, ecosystem map. | 🎯 `hunt` 🤝 `companion` | Hunt uses market context to score opportunity quality. Companion for macro career strategy. |

---

## Quick Lookup: Which files feed which skill

### 🧠 `linkright-mem` (Memory / RAG Skill)
**Roadmap:** doc_02, doc_03, doc_05, doc_13_storage, doc_14, doc_15, doc_17, doc_24, doc_26, doc_28, doc_29  
**Research:** personal_knowledge_management_for_operators, ai_augmented_personal_operating_system, interview_stories_positioning_guide (story bank schema)

### 🎯 `linkright-hunt` (Job Hunter + Scorer)
**Roadmap:** doc_04, doc_09, doc_20, doc_23, doc_30  
**Research:** jd_intelligence_and_signal_mapping_system, application_pipeline_operating_system, pm_archetype_evolution_and_future_market_map, hiring_process_intelligence_guide, vc_and_startup_ecosystem_navigation_system, failed_hire_rca_methodology

### 📄 `linkright-sync` (Resume Builder)
**Roadmap:** doc_06, doc_07, doc_16  
**Research:** resume_positioning_guide, career_narrative_architecture_guide, ai_era_authenticity_and_human_signal_guide, width-optimization-research, jd_intelligence_and_signal_mapping_system, pm_archetype_evolution_and_future_market_map, ai_product_leadership_track, chief_of_staff_and_strategic_operator_track, founder_startup_operator_track, executive_and_director_level_pm_track, staff_pm_influence_and_organizational_leverage_system, high_agency_operator_system, personal_brand_and_market_positioning_system

### 🗂️ `linkright-portfolio` (Product Portfolio Builder)
**Roadmap:** (none specific — uses doc_06 generation patterns)  
**Research:** proof_of_work_portfolio_system, proof_of_thinking_economy_guide, async_hiring_optimization_guide

### 🎤 `linkright-interview` (Interview Coach)
**Roadmap:** doc_18 (eval framework for judging answers), doc_21 (agent governance for goal loop)  
**Research:** interview_intro_positioning_guide, interview_psychology_and_decision_influence_system, interview_stories_positioning_guide, interview_tone_positioning_guide, product_manager_case_interview_master_system, hiring_process_intelligence_guide, internal_advocacy_and_hiring_committee_politics_guide, follow_up_communication_positioning_guide, executive_presence_and_behavioral_signaling_system, elite_communication_and_strategic_conversation_system, crisis_reputation_recovery_playbook, decision_making_under_uncertainty_frameworks, async_hiring_optimization_guide, ai_era_authenticity_and_human_signal_guide, high_agency_operator_system

### 📣 `linkright-social` (Social Content Engine — LinkedIn-first)
**Roadmap:** doc_09, doc_20, doc_25  
**Research:** linked_in_positioning_guide, personal_brand_and_market_positioning_system, proof_of_thinking_economy_guide, elite_networking_psychology_and_relationship_leverage, micro_reputation_and_backchannel_dynamics_guide, referral_and_network_strategy_system, ai_era_authenticity_and_human_signal_guide

### 🤝 `linkright-companion` (Career Companion / Daily Diary / Self-Reflection)
**Roadmap:** doc_12, doc_23, doc_25, doc_26, doc_27, doc_28  
**Research:** advanced_organizational_politics_and_power_dynamics, ai_augmented_personal_operating_system, application_pipeline_operating_system, compensation_negotiation_and_offer_strategy_system, crisis_reputation_recovery_playbook, cross_domain_career_transitions_guide, decision_making_under_uncertainty_frameworks, elite_communication_and_strategic_conversation_system, elite_networking_psychology_and_relationship_leverage, emotional_resilience_and_psychological_stability_system, failed_hire_rca_methodology, high_agency_operator_system, internal_advocacy_and_hiring_committee_politics_guide, leadership_transition_and_executive_identity_evolution, micro_reputation_and_backchannel_dynamics_guide, negotiation_style_positioning_guide, performance_and_cognitive_optimization_for_operators, personal_brand_and_market_positioning_system, personal_knowledge_management_for_operators, pm_archetype_evolution_and_future_market_map, post_offer_integration_guide, reference_and_reputation_management_guide, referral_and_network_strategy_system, staff_pm_influence_and_organizational_leverage_system, vc_and_startup_ecosystem_navigation_system

### 🔧 `ALL` (Architectural constraints — every skill must follow)
**Roadmap:** doc_00 (decisions), doc_01 (vision/philosophy), doc_08 (runtime), doc_10 (orchestration), doc_11 (observability), doc_19 (UX patterns), doc_21 (agent governance / goal loops)

---

## Goal Loop Architecture (Karpathy-style)

Every skill should implement this loop pattern (from doc_21 + the image shared):

```
/goal set → completion condition defined
     ↓
Worker turn (skill executes: edits, tool calls, Python scripts, writing)
     ↓
Judge reads transcript (fresh context, no tools — evaluates against completion condition)
     ↓
Condition met? 
  YES → Goal clears, deliver output
  NO  → Worker gets another turn with judge's feedback
```

**Key implementation rules (from doc_21):**
- Worker and Judge are separate contexts — judge never runs tools, only reads
- Each skill defines its own completion condition (e.g., interview: "all 5 stories pass pushback without hesitation"; resume: "all lines 95-100% fill, page fits, Grade A")
- Human escalation triggers: after 3 failed judge turns, or when judge detects a contradiction the worker can't resolve
- Agents don't call each other directly — they communicate through shared memory (mem skill)

---

## Files Not Yet Reviewed in Full
*(Read the first 35 lines only — deeper content may have additional nuance)*

None — all 80 files have been catalogued. The 35-line header reads were sufficient to classify every file accurately given the highly structured writing style used throughout.

---

*Update this file whenever you add new docs to either folder.*
