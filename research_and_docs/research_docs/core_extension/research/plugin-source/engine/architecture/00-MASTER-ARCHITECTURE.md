> Note for readers of this shared engine. This document is the original design narrative. It uses Satvik, the first user, as the running example. The engine itself is generic, every user specific detail lives in that user's own config and instance files, never in the engine.

# Master Architecture, LinkedIn Content Engine

Status, draft v0.3 for iteration. Owner, Satvik. Date, 2026-06-04.

This is the source of truth for how the whole system is wired. Read this before any skill doc. v0.2 reshaped the system into the workflow and agent model, and mapped every expert lens to a concrete agent. v0.3 adopts the BMAD method convention, every agent and workflow is config driven in YAML, separate from execution, with its own persona, dependencies, and persistent memory. Sections 14 to 18 hold the BMAD aligned design.

---

## 1. Design philosophy

Five rules drive every decision below.

A skill is a workflow. Each skill is one process with a clear start and one deliverable. Voice building is a workflow. Strategy is a workflow. Drafting is a workflow.

A workflow is run by many agents. Inside a workflow, separate agents each own one job. Each agent is one expert lens, nothing more. This keeps every agent sharp and easy to score.

Agents stay lean, knowledge loads at run time. An agent file holds the steps only. The reference material it needs sits in the knowledge base as separate markdown, and the agent loads the exact files it needs when it runs. Improve the knowledge without rewriting the agent.

Every output is a template, every handoff is a file. An agent never passes data in the air. It writes a structured file at a fixed template, md, csv, or yaml. The next agent reads that file. The user gets clean deliverables.

Every agent carries its own eval. Before an agent hands off, it runs its own checklist. Hard rules are pass or fail gates. Soft quality is scored 0 to 10. Nothing moves forward dirty.

Config lives outside the skill, BMAD style. Every agent is a YAML file with its persona, responsibilities, do and do not lists, dependencies, and memory. Every workflow is a YAML file with its steps, inputs, validation, and outputs. The skill body stays thin, it just runs what the config declares. This is the v0.3 change, see sections 14 to 18.

The engine is user agnostic. No agent hardcodes a name, a domain, or a preference. An agent refers to the owner, and reads who that owner is, what they do, and how they want to write, from the user config. The engine is the reusable machine. The user instance is the data it runs on, the config, the voice profile, the positioning, the ledger, the memory. Swap the config and a different person's content engine runs. Satvik is simply the first user. See section 5.1.

---

## 2. The execution model

```
SKILL = WORKFLOW
   |
   +-- Agent  =  one expert lens
   |     |
   |     +-- loads   ->  knowledge files  (knowledge-base/*.md, *.csv)
   |     +-- runs    ->  eval checklist   (evals/*.md)
   |     +-- writes  ->  output template  (templates/*.yaml|md|csv)
   |
   +-- next Agent reads the previous template as its input
```

Read this as, a skill is a folder of steps, each step is an agent, each agent pulls its knowledge, checks itself against its eval, and drops a templated file for whoever is next.

---

## 3. The seven workflows

| # | Workflow (skill) | Purpose | Cadence |
|---|---|---|---|
| W0 | Onboarding, `onboarding` | Capture all settings once, write the central user config every agent reads | Once at setup, re run on change |
| W1 | Voice Building, `voice-architect` | Build Satvik's voice profile from interview plus stylometry | Once, then refresh on drift |
| W2 | Content Strategy, `content-strategist` | Decide topic, post type, media type, angle, triggers | Per post or per batch |
| W3 | Content Drafting, `content-drafter` | Write post copy plus media script | Per post |
| W4 | Media Production, `media-creator` | Turn the media script into finished assets | Per post |
| W5 | Evaluation, `master-evaluator` | Gatekeeper signoff after W2, W3, W4 | Cross cutting |
| W6 | Publish and Engage, `engagement-ops` | Post time, first comment, first hour replies | Per post, post launch |
| W7 | System Improvement, `system-optimizer` | Read performance, update knowledge and weights | Weekly and monthly |

W0 runs once at setup and produces the config every agent reads. W1 runs once and produces the voice profile the rest of the system reads forever. W2 to W6 run for every post. W7 runs on a schedule and is the only workflow allowed to edit the knowledge base.

W0 and W1 stay separate files but run in one sitting. A thin Setup conductor, `workflows/setup/workflow.yaml`, chains them, onboarding first so the config exists, then voice building which reads that fresh config. It feels like one onboarding to Satvik. They stay separate because they change for different reasons, a settings tweak must not force a voice rebuild, and the voice agents read the config, so config has to come first. Either one can also be re run alone later.

---

## 4. Expert to agent map, the core of v0.2

Every expert from the research is now a named agent inside a workflow. Each row shows what the agent loads, the eval it runs, and the template it writes.

### W0, Onboarding

| Agent | Expert lens | Loads (knowledge) | Eval (checklist) | Writes (template) |
|---|---|---|---|---|
| Onboarding Concierge | Settings capture | `CLAUDE.md`, career profile | `config-completeness.md` | `config/user-config.yaml` |

Deliverable, `config/user-config.yaml`. Runs once at setup. Every agent below reads this config, see section 16.

### W1, Voice Building

| Agent | Expert lens | Loads (knowledge) | Eval (checklist) | Writes (template) |
|---|---|---|---|---|
| Interviewer | Psychology, elicitation | `elicitation-method.md`, `personality-primer.md` | `interview-coverage.md` | `interview-transcript.md` |
| Stylometrist | Forensic linguist | `stylometry-method.md`, source chats and samples | `fingerprint-completeness.md` | `voice-metrics.csv` |
| Voice Synthesizer | Voice lead | the two outputs above | `voice-profile-qa.md` | `voice-profile.md`, `voice-examples.md` |

Deliverable, `knowledge-base/voice-profile.md`. This is the most important file in the system.

### W2, Content Strategy

| Agent | Expert lens | Loads | Eval | Writes |
|---|---|---|---|---|
| Audience Mapper | Audience, ICP researcher | `audience-icp.md` | `icp-match.md` | section of brief |
| Positioning Guard | Brand, positioning strategist | `positioning-pillars.md`, calendar | `positioning-ladder.md` | section of brief |
| Distribution Strategist | LinkedIn algorithm expert | `algorithm-mechanics.md`, `posts.csv` | `algorithm-fit.md` | section of brief |
| Topic Selector | Content strategist | `post-types.md`, `posts.csv`, calendar | `differentiation.md` | `strategy-brief.yaml` |

Deliverable, `strategy-brief.yaml`.

### W3, Content Drafting

| Agent | Expert lens | Loads | Eval | Writes |
|---|---|---|---|---|
| Domain SME | The user's domain, read from config | `config/user-config.yaml` expertise, career profile, `bullet_bank.md`, `metrics-ledger.md` | `credibility-and-metrics.md` | substance notes |
| Hook Writer | Direct response copywriter | `psychology-storytelling.md`, `mobile-syntax-rules.md` | `hook.md` | hook block |
| Storyteller | Narrative plus voice | `voice-profile.md`, `psychology-storytelling.md` | `voice-authenticity.md` (scored) | body block |
| Copy Chief | Editor | `mobile-syntax-rules.md`, `scoring-rubrics.md` | `hard-gates.md` (pass or fail) | clean copy |
| Media Scripter | Content to media bridge | `media-types.md` | `media-script-clarity.md` | `content-handoff.yaml` |

Deliverable, `content-handoff.yaml`.

### W4, Media Production

| Agent | Expert lens | Loads | Eval | Writes |
|---|---|---|---|---|
| Art Director | Brand identity designer | `design-principles.md`, `brand-identity.md` | `brand-consistency.md` | design system block |
| Asset Builder | Visual producer, branches by type | `media-types.md`, `design-principles.md` | `asset-quality.md` | rendered files |
| Accessibility | A11y specialist | `accessibility-rules.md` | `a11y.md` | alt text, captions, srt |

Deliverable, `media-handoff.yaml` plus the rendered files. Asset Builder branches into image, carousel or pdf, gif, and video sub paths. Render happens in the sandbox first, ChatGPT image generator is the fallback.

### W5, Evaluation, cross cutting

| Agent | Expert lens | Loads | Eval | Writes |
|---|---|---|---|---|
| Strategy Reviewer | Editorial director | `positioning-pillars.md`, `audience-icp.md` | `strategy-signoff.md` | signoff after W2 |
| Copy Reviewer | Three lens, scroll stopper, trust builder, action driver | `scoring-rubrics.md`, `voice-profile.md` | `copy-signoff.md` | signoff after W3 |
| Media Reviewer | Three lens, thumb stopper, brand ambassador, story visualizer | `design-principles.md` | `media-signoff.md` | signoff after W4 |
| Ethics and Risk Reviewer | Risk and credibility | `ethics-risk-rules.md`, `metrics-ledger.md` | `risk.md` | risk flag block |

Deliverable, `signoff.md` at each gate. The Ethics and Risk Reviewer is the one that checks teardowns of real companies for defamation risk, and checks that synthesized numbers match the ledger and stay defensible.

### W6, Publish and Engage

| Agent | Expert lens | Loads | Eval | Writes |
|---|---|---|---|---|
| Scheduler | Timing analyst | `algorithm-mechanics.md`, `posts.csv` | `timing.md` | time slot |
| First Comment | Community ops | `voice-profile.md`, `audience-icp.md` | `first-comment.md` | seed comment |
| Reply Strategist | Community ops | `audience-icp.md` | `reply-plan.md` | first hour plan |

Deliverable, `engagement-plan.md`. This used to be parked as a bonus. The research is clear, the first 60 minutes decide reach and comments weigh far more than likes, so this is core now.

### W7, System Improvement

| Agent | Expert lens | Loads | Eval | Writes |
|---|---|---|---|---|
| Data Analyst | Growth, experimentation | `posts.csv`, `scoring-rubrics.md` | `stats-sanity.md` | findings |
| Knowledge Curator | Knowledge ops | all knowledge files | `changelog-discipline.md` | KB edits plus changelog |
| Voice Drift Auditor | Voice QA | `voice-profile.md`, `voice-metrics.csv`, recent posts | `voice-drift.md` | drift flag |

Deliverable, `optimization-report.md` plus logged knowledge edits.

---

## 5. Knowledge base, the shared brain

All knowledge sits in `Content-Engine/knowledge-base/`. Agents load by path at run time. New files added in v0.2 are marked NEW.

### 5.1 Two kinds of knowledge, engine versus user instance

This split is what makes the engine reusable.

Engine knowledge, generic, ships with the system. Method and reference material that is true for any user. `elicitation-method.md`, `stylometry-method.md`, `personality-primer.md`, `post-types.md`, `algorithm-mechanics.md`, `psychology-storytelling.md`, `design-principles.md`, `media-types.md`, `accessibility-rules.md`, `scoring-rubrics.md`. These do not mention any person.

User instance knowledge, generated per user, never hardcoded. Produced by onboarding, voice building, and usage. `config/user-config.yaml`, `voice-profile.md`, `voice-examples.md`, `voice-metrics.csv`, `positioning-pillars.md`, `audience-icp.md`, `brand-identity.md`, `metrics-ledger.md`, `ethics-risk-rules.md` if user specific, `performance-data/`, and every `memory/` sanctum. A new user gets a fresh set of these, the engine knowledge stays untouched.

One note on writing rules. The hard writing rules live in `config/user-config.yaml` under writing_protocol, because they are the user's preference. `mobile-syntax-rules.md` is the generic explainer of how to apply such rules, the actual allowed punctuation, banned words, and hook signature are read from config. So a different user with different rules needs no code change.

Voice and language. `voice-profile.md`, `voice-examples.md`, `voice-metrics.csv`. Method files, `elicitation-method.md` NEW, `stylometry-method.md` NEW, `personality-primer.md` NEW.

Strategy. `post-types.md`, `audience-icp.md` NEW, `positioning-pillars.md` NEW, `algorithm-mechanics.md` NEW.

Craft. `psychology-storytelling.md`, `mobile-syntax-rules.md`, `scoring-rubrics.md`.

Media. `media-types.md`, `design-principles.md`, `brand-identity.md` NEW, `accessibility-rules.md` NEW.

Truth and risk. `metrics-ledger.md`, `ethics-risk-rules.md` NEW.

Performance. `performance-data/SCHEMA.md`, `performance-data/posts.csv`.

---

## 6. Templates registry, the output contracts

Every templated file lives in `Content-Engine/templates/` as a blank shape with field notes. Agents copy the shape and fill it. Two agents that share a template share a contract, so the verification step checks that producers and consumers agree on every field.

| Template | Format | Written by | Read by |
|---|---|---|---|
| `interview-transcript.md` | md | Interviewer | Stylometrist, Synthesizer |
| `voice-metrics.csv` | csv | Stylometrist | Synthesizer, Voice Drift Auditor |
| `voice-profile.md` | md | Voice Synthesizer | almost every agent |
| `voice-examples.md` | md | Voice Synthesizer | Storyteller, Copy Reviewer |
| `strategy-brief.yaml` | yaml | W2 agents | all W3 agents, Strategy Reviewer |
| `content-handoff.yaml` | yaml | W3 agents | W4 agents, Copy Reviewer |
| `media-handoff.yaml` | yaml | W4 agents | Media Reviewer, final package |
| `signoff.md` | md | W5 agents | conductor, run log |
| `engagement-plan.md` | md | W6 agents | Satvik |
| `optimization-report.md` | md | W7 agents | Satvik |
| `performance-data/SCHEMA.md` | md | set once | Scheduler, Data Analyst, Strategist |
| `posts.csv` | csv | Satvik, later Tampermonkey | Strategist, Data Analyst |

---

## 7. Evals, the checklists

Every checklist lives in `Content-Engine/evals/`. Two kinds.

Hard gates, pass or fail. A single failure means reject and rework, no score. These live mainly in `hard-gates.md` and cover punctuation, banned words, the hook signature with the red double exclamation, paragraph shape, no salesy closer, and metric consistency against the ledger.

Scored rubrics, 0 to 10. Defined once in `scoring-rubrics.md` and referenced by the agent level evals. Pass threshold, every dimension at or above 8, weighted average above 8.5, max 5 rewrite loops.

Scored dimensions and weights.

| Dimension | Measures | Weight |
|---|---|---|
| Voice authenticity | Idiolect and argument match to `voice-profile.md` | High |
| Human texture, anti AI | Sentence length variation, burstiness, not flat | High |
| Hook impact | Curiosity or emotion inside the mobile cutoff | High |
| Value density | Every line earns its place | High |
| Emotional connect | The story or insight lands | High |
| Algorithm fit | Dwell, comment bait, save worth, format choice | High |
| Positioning ladder | Post ladders up to the user's positioning through line, read from config | Medium |
| Originality | Fresh angle, not generic | Medium |
| Clarity | Easy to follow | Medium |
| Media script clarity | Enough for Media Creator to build | High |

Voice authenticity and human texture are the dimensions that separate this from a generic bot. They are the reason W1 exists.

---

## 8. Inter agent memory and the run lifecycle

Claude Code gives no shared live memory, so we do not rely on it. Every handoff is a file in a dated run folder. Runs are reproducible and resumable.

```
Content-Engine/runs/2026-06-04/
  01-strategy-brief.yaml
  02-strategy-signoff.md
  03-content-handoff.yaml
  04-copy-signoff.md
  05-media-handoff.yaml
  06-media-signoff.md
  07-engagement-plan.md
  08-final-package/        (post.md + media files, copied to 30-Day-Engine/Day-NN/)
  run-log.md               (scores, iterations, flags, what happened)
```

A thin conductor calls each workflow in order, writes its template, calls the Evaluator gate, and only proceeds on a pass. If a stage fails its gate after max loops, the conductor stops and writes the reason to `run-log.md`. Nothing ships without all three signoffs.

---

## 9. Metric consistency ledger

`metrics-ledger.md` locks every synthesized number ever used, with its value, frozen. The Walmart number stays the same number in every post. The Domain SME agent reads the ledger before using any figure, and appends any new locked value. The Ethics and Risk Reviewer checks no post contradicts it.

---

## 10. Performance data pipeline

MVP, manual CSV. Satvik fills `posts.csv` by hand at the schema in `SCHEMA.md`, one row per post. This proves the loop before any automation. Proposed columns, post date, day number, post type, media type, topic, hook text, impressions, reactions, comments, shares, saves, profile views, follower delta, dwell estimate, notes.

Later, passive automation. A Tampermonkey userscript watches LinkedIn while Satvik browses with the script on. It reads the metrics he already sees and appends to the same CSV at the same schema. No separate scraping, no separate login. I build it once the manual loop is proven. The schema does not change, so nothing downstream breaks.

---

## 11. Folder structure

```
LinkedIn Content/                      (project root, exists)
  CLAUDE.md
  satvik_jain_career_profile.md
  career-layers/
  30-Day-Engine/                       (calendar + daily output)
  Content-Engine/                      (this system)
    architecture/
      00-MASTER-ARCHITECTURE.md        (this file)
    config/                            (NEW v0.3, settings, user owned)
      user-config.yaml                 (the single source of truth for preferences)
    skills/                            (one design doc per workflow, the narrative)
      voice-architect.design.md
      content-strategist.design.md
      content-drafter.design.md
      media-creator.design.md
      master-evaluator.design.md
      engagement-ops.design.md
      system-optimizer.design.md
    workflows/                         (NEW v0.3, one workflow.yaml per skill)
      voice-architect/workflow.yaml
      ...
    agents/                            (NEW v0.3, one <code>.agent.yaml per agent)
      voice-architect/
        interviewer.agent.yaml
        stylometrist.agent.yaml
        voice-synthesizer.agent.yaml
      ...
    knowledge-base/                    (shared brain, section 5)
    templates/                         (output contracts, section 6, plus the YAML schemas)
    evals/                             (checklists, section 7)
    memory/                            (NEW v0.3, persistent per agent sanctum, section 17)
      stylometrist/MEMORY.md
      ...
    runs/                              (one folder per daily run)
```

Skill design docs are the narrative planning layer. The agent and workflow YAML files are the machine followable spec. Both point at the same central knowledge, templates, and evals by path, not copy them, so there is one source of truth.

---

## 12. How the experts mapped, summary

The original blueprint had one expert, psychology. v0.2 has eleven, each a named agent.

Psychology to Interviewer. Forensic linguist to Stylometrist. Audience researcher to Audience Mapper. Brand strategist to Positioning Guard. LinkedIn algorithm expert to Distribution Strategist. Content strategist to Topic Selector. B2C product SME to Domain SME. Direct response copywriter to Hook Writer. Editor to Copy Chief. Brand identity designer to Art Director. A11y specialist to Accessibility. Community ops to First Comment and Reply Strategist. Growth and experimentation to Data Analyst. Risk and credibility to Ethics and Risk Reviewer.

---

## 13. BMAD alignment, what we borrowed

The BMAD method install showed a clean pattern for config driven agents. What we take from it.

Agents are config, not code. Each agent is a declarative file. Identity, persona, principles, dependencies, memory. The runtime just reads the file and behaves. We use one YAML per agent instead of BMAD's split across SKILL.md plus sanctum files, because one file per agent is easier for Satvik to read and edit.

Dependencies are declared by path. An agent names the knowledge, checklists, templates, and memory it needs. Nothing is hidden inside prose. This is exactly the lean skill, external knowledge rule from section 1.

Personas carry behavior. BMAD pushes outcome driven design, the persona and principles tell the agent how to act, so the steps stay short. We keep do and do not lists explicit because our hard gates demand it.

Memory is a sanctum. BMAD agents persist a curated memory that grows across sessions and is pruned during a Pulse. We adopt this for the agents that benefit from learning, see section 16.

Customization surface. BMAD ships a customize file per agent for org and personal overrides without editing the agent. We keep a slim version for persistent facts and swappable knowledge paths.

## 14. Agent config model

Every agent is one file, `agents/<workflow>/<code>.agent.yaml`. This is the full shape. The blank schema with field notes lives at `templates/agent-config.template.yaml`.

```yaml
agent:
  code: stylometrist                 # stable id, matches file name
  title: Forensic Linguist
  icon: "🔬"
  role: Idiolect and language fingerprint analyst
  agent_type: memory                 # stateless | memory | autonomous
  workflow: voice-architect          # which workflow it belongs to

  persona:
    identity: >                      # who this agent is, 2 to 4 sentences
    communication_style: >           # how it talks to Satvik and to its peers
    principles:                      # the convictions that drive its judgement
      - ...

  responsibilities:                  # what this agent owns, outcomes not steps
    - ...

  dos:                               # explicit, scorable
    - ...
  donts:                             # explicit, gate worthy
    - ...

  dependencies:
    knowledge:                       # files loaded at run time
      - knowledge-base/stylometry-method.md
    checklists:                      # the evals it runs on itself
      - evals/fingerprint-completeness.md
    templates:
      reads:                         # inputs from upstream agents
        - templates/interview-transcript.md
      writes:                        # its output contract
        - templates/voice-metrics.csv
    memory:                          # persistent learning, section 16
      sanctum: memory/stylometrist/
      captures:
        - confirmed idiolect markers that repeat across runs
        - false positives to ignore
      improves: precision of future voice scoring

  team:                              # agent to agent coordination
    receives_from:
      - agent: interviewer
        input: templates/interview-transcript.md
    hands_off_to:
      - agent: voice-synthesizer
        output: templates/voice-metrics.csv
    coordinates_with:
      - agent: voice-drift-auditor
        via: voice-metrics.csv as the baseline

  activation:
    persistent_facts:
      - "file:knowledge-base/mobile-syntax-rules.md"
    execution_hints:
      interactive: false
      iterative: true
```

This single block answers everything asked, persona, responsibilities, do and do not, dependencies across checklists, knowledge, memory, templates, and the team coordination with named inputs and outputs.

## 15. Workflow config model

Every workflow is `workflows/<code>/workflow.yaml`, BMAD style. It names the agents in order, the shared config, the validation checklist, the output template, and the run hints. Blank schema at `templates/workflow.template.yaml`.

```yaml
workflow:
  code: voice-architect
  name: Voice Building
  purpose: Build Satvik's voice profile from interview plus stylometry
  cadence: once, refresh on drift

  config_source: knowledge-base/         # where shared knowledge resolves from
  output_folder: knowledge-base/         # voice-profile.md lands here

  agents:                                # run order
    - interviewer
    - stylometrist
    - voice-synthesizer

  validation: evals/voice-profile-qa.md  # the gate for the whole workflow
  primary_output: templates/voice-profile.md

  execution_hints:
    interactive: true                    # the interview needs Satvik live
    resumable: true                      # state saved between agents
```

## 16. Memory model, the sanctum

First, a distinction that matters. Settings are not memory.

Settings, the user config. Captured once by the Onboarding Concierge, stored in `config/user-config.yaml`. User owned and stable. Language, writing rules, positioning, cadence, audience, consents. Agents read this, none of them hardcode it and none of them change it. The Hinglish in, English out rule lives here, because it is Satvik's preference, not something an agent learned. When Satvik changes a setting, onboarding updates the config and logs it.

Memory, the agent sanctum. Owned by an agent, grown over runs. What the agent figured out by doing the work, the patterns it confirmed, the mistakes it stopped repeating. This is the rest of section 16.

Keeping these apart is the point. Config is law handed down by Satvik. Memory is wisdom earned by an agent. They never mix.

Agents that gain from experience keep a memory folder, `memory/<code>/`. Inside, `MEMORY.md` holds curated long term knowledge, capped small so it loads cheap every run. Raw run notes go in `memory/<code>/sessions/YYYY-MM-DD.md`, and get distilled into `MEMORY.md` during the System Optimizer pass, never bloating it.

This is the answer to what an agent stores to improve future quality. Examples. The Stylometrist remembers which idiolect markers proved stable, so it stops re deriving them. The Distribution Strategist remembers which hook shapes and formats actually drove reach, separate from the general knowledge file. The Copy Reviewer remembers the rewrites that lifted weak drafts, so its feedback sharpens over time.

Stateless agents keep no memory. Memory agents read and curate it. The only writer to a sanctum during a normal run is the agent itself. The System Optimizer is the only outside editor, and it logs every change.

## 17. Build and run lifecycle

Design phase, now. We write the narrative design doc per workflow, then its workflow.yaml and the agent.yaml files, then the knowledge, templates, and evals they point at.

Build phase, done. The runtime lives in `skills/`. `skills/EXECUTION.md` is the generic protocol for running any workflow from its YAML, load the config, run each agent in order, load its knowledge and memory, do its job, check its eval, write its template into the dated run folder. `skills/daily-post.md` is the conductor, it chains the per post workflows with the Master Evaluator gate between each, and assembles one finished gated post package.

Run phase. The conductor calls each workflow, each agent loads its knowledge and memory, does its job, checks its own eval, writes its template, and the Evaluator gates the handoff. Memory agents append session notes. Nothing ships without the three signoffs.

## 18. Open questions for the next iteration

Orchestration. One conductor skill that runs W2 to W6 end to end, or run each skill by hand and pass files. Smoother versus more control.

Evaluator model. Master Evaluator is meant to be a larger model. Confirm that cost on every post, or only on flagged posts.

Agent weight. Twenty plus agents is the full map. In practice some agents are a single quick pass. Confirm whether to merge any thin agents, for example Hook Writer into Storyteller, to cut run time.

Voice refresh cadence. After a fixed number of posts, or only when the Voice Drift Auditor flags it.

Calendar ownership. Does the Strategist own the 30 day calendar going forward, or only read it.
