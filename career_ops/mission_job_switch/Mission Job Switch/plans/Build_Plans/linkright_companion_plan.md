# linkright-companion — Skill Plan

**Skill:** `/linkright-companion`  
**Version:** 1.0.0 (planned)  
**Build Phase:** Phase 4 — Build Last  
**Status:** Not yet built  

---

## 1. What This Skill Does

`linkright-companion` is the daily operating layer of Linkright. It synthesizes what all other skills produce into situational awareness and prioritized action.

It is the difference between having a job search system and actually running one.

It answers:
- What should I do today, in what order?
- How is my job search actually going?
- What decisions have I made, and are they working?
- What patterns am I missing?
- Where am I losing — and why?

**Built last for a reason:** The companion needs data from all other skills to be meaningful. Without pipeline data from hunt, memory from mem, and outcomes to analyze, it's just a to-do list. With them, it becomes strategic intelligence.

**Constraint source:** Reads `user_setup.md` for target CTC, role targets, hard constraints, and timeline.

---

## 2. Core Modules

### Module 1 — Morning Briefing

Run at start of day or on demand.

```
LINKRIGHT DAILY BRIEF — [date]

PIPELINE STATUS:
  Active applications: [N]
  Awaiting response: [N] (names listed)
  In-progress: [N] (names + stage)
  Overdue follow-up: [N] (names + days elapsed)

HIGHEST LEVERAGE ACTIONS TODAY:
  1. [Specific action — e.g. "Tailor resume for Company X JD (deadline this week)"]
  2. [Specific action — e.g. "Follow up with Company Y — 12 days since last contact"]
  3. [Specific action — e.g. "Publish POT post before Company Z interview next week"]

OPTIONAL (if energy allows):
  [Lower priority item]

CURRENT GOAL PROGRESS:
  [Goal from user_setup] — [days elapsed / days remaining]
  On track: [yes/borderline/behind]
```

Rules:
- Max 3 "highest leverage" actions — not a 10-item list
- Each action must be specific and immediately actionable, not vague
- "Overdue" = any applied application with no outcome recorded after 14 days

### Module 2 — Weekly Review

Run at end of week (Sunday or Monday).

```
WEEKLY REVIEW — Week of [date range]

ACTIVITY:
  Applications sent:          [N]
  Interviews / calls:         [N] (which ones)
  Outcomes recorded:          [N]
  Posts published:            [N]
  New opportunities found:    [N] (saved / discarded breakdown)
  Cold emails sent:           [N]

PIPELINE STATE:
  [stage-by-stage count]

SHORTLIST MODEL UPDATE:
  [only if new outcomes recorded]
  "This week's outcomes: [summary]"
  "Model now has [N] outcomes — confidence: [level]"

WHAT WORKED:
  [1-2 specific things]

WHAT TO IMPROVE:
  [1-2 specific gaps — must be actionable, not vague]

NEXT WEEK FOCUS:
  [3 specific priorities for next week]
```

### Module 3 — Decision Journal

Log career decisions with structured reasoning.

```
DECISION LOG ENTRY

Decision: [brief title]
Date: [date]
Context: [what situation prompted this decision]
Options considered:
  A) [option] — pros: [...] cons: [...]
  B) [option] — pros: [...] cons: [...]
Chosen: [which option]
Reasoning: [why]
Key assumption: [what would have to be true for this to be right]
Review date: [+2 weeks or specific date]
```

On review date: companion surfaces this entry and asks: "Does the reasoning still hold?"

Why this matters: Most people never study their own decision quality. The journal reveals patterns over time — which types of decisions you make well, which ones you consistently get wrong.

### Module 4 — Rejection / Ghosting Analysis

Triggered when user records a ghosted or rejected outcome in linkright-hunt.

```
OUTCOME ANALYSIS — [Company] — [Role]
Outcome: [Ghosted / Early Reject / Post-Interview Reject]

STAGE WHERE IT FAILED:
  [Didn't get call / Failed screen / Failed interview]

LIKELY CAUSE (probabilistic — not definitive):
  [Based on JD signal analysis + profile signals at time of application]
  e.g. "JD emphasized growth_experimentation as primary signal.
        Your profile has this signal at LOW strength.
        This is a plausible fit gap."

CONFOUNDERS (things we can't control):
  e.g. Internal candidate / Hiring freeze / Timing / ATS keyword filter

MEMORY UPDATE SUGGESTED:
  "This outcome contributes to your shortlist model.
   Your profile may under-index for growth PM roles currently.
   3 similar rejections now — pattern worth noting."

ACTION ITEMS:
  [0-1 specific things — not a 5-point plan]
```

Rules:
- Never assign definitive blame — always probabilistic language ("likely", "plausible")
- Always list confounders — rejection has many causes, fit gap is one of them
- Never trigger emotional spiral — analytical framing only
- Always route outcome to linkright-hunt shortlist model

### Module 5 — Offer Evaluation

Triggered when user records an offer in linkright-hunt.

```
OFFER EVALUATION — [Company] — [Role]

COMPENSATION CHECK:
  Offered: [base + equity + bonus]
  Your floor (from setup): [target_ctc_min]
  Your target: [target_ctc_target]
  Verdict: [above target / within range / below floor]
  
  [If below floor]:
  "This is below your stated minimum. Recommend negotiating before any decision.
   Suggested opening: [pulls from interview skill salary script]"

ROLE FIT:
  Signals covered: [N/N priority signals]
  Archetype match: [%]
  Career trajectory: [good / neutral / sideways / backward]

PIPELINE CONTEXT:
  Other active opportunities: [N]
  In-interview stage: [list]
  Timeline: [any time-sensitive decisions elsewhere?]

DECISION FRAMEWORK QUESTIONS:
  1. Does this role move you toward or away from your target archetype?
  2. What signal does taking this role send to your next employer?
  3. What would you have to give up to take this?
  4. Would you regret NOT taking it in 2 years?

This evaluation is analytical input, not a recommendation.
The decision is yours.
```

### Module 6 — Diary Ingestion

Short daily or weekly work reflection → routes to memory enrichment.

```
INPUT: Free-text reflection
  e.g. "Today I ran the quarterly roadmap review with 4 VPs.
        Huge scope disagreement — I had to cut 2 features on the spot.
        Realized I'm better at real-time negotiation than I thought."

EXTRACTION:
  New fact candidate: "Led quarterly roadmap review with VP-level stakeholders"
  Signal evidence: "stakeholder_leadership + real-time_negotiation" 
  Interview story candidate: "Scope cuts under executive pressure"
  Learning: "stronger at real-time negotiation than expected"

ROUTING:
  Fact candidates → linkright-mem for confirmation
  Story candidates → linkright-interview for banking
  Signal evidence → linkright-mem for signal update

NOTHING PERSISTS without user confirmation.
```

---

## 3. Goal Tracking

User sets a primary job search goal in user_setup.md (or updates via companion):

```
EXAMPLE GOAL:
  Receive offer at [target_ctc_target] or above for [target_archetype] role
  by [target_date]

CHECKPOINTS:
  □ Memory fully built (linkright-mem complete)
  □ Pipeline populated (≥10 active opportunities)
  □ ≥3 companies in interview stage simultaneously
  □ ≥1 offer received
  □ Offer meets CTC floor from user_setup

Weekly review shows: which checkpoints are met, which are behind, recommended action.
```

---

## 4. Skill Gates

### Gate 1 — Mode Selection

```
What do you need today?
a) Morning briefing
b) Weekly review
c) Log a decision
d) Analyze a rejection or ghosting
e) Evaluate an offer
f) Add a diary entry
g) Check progress toward goal
h) Surface decision journal entries due for review
```

### Gate 2 — Load State

Load relevant data based on mode:
- Pipeline: read `memory/pipeline.json` from linkright-push (or local)
- Memory state: read `memory/facts.md` + `memory/signals.md` via linkright-mem
- Decisions: read `memory/decisions/decision_log.md`
- Goal: read user_setup.md goals section

### Gate 3 — Generate Output

Based on mode, generate the relevant module output.

For diary: extract fact/signal/story candidates.  
For rejection: run analysis, propose outcome recording + model update.  
For offer: run compensation check against user_setup.md automatically.

### Gate 4 — Route Updates (if any)

- New diary facts → route to linkright-mem for confirmation
- Rejection outcome → route to linkright-hunt for model update
- Decision log entries → write to `memory/decisions/`

---

## 5. Hard Rules

- **ALWAYS load user_setup.md before any compensation evaluation** — never hardcode numbers
- **ALWAYS flag if pipeline has fewer than 5 active opportunities** — this is a danger zone
- **ALWAYS surface decision journal entries on their review date**
- **NEVER interpret a rejection as definitive** — always list confounders
- **NEVER route diary entries to memory without user confirmation**
- **NEVER recommend accepting an offer without checking against target_ctc_min first**
- **ALWAYS route offer evaluation through compensation check automatically** — user shouldn't have to ask

---

## 6. References to Write

| File | Contents |
|---|---|
| `references/ref_01_briefing_templates.md` | Morning briefing format, weekly review format with all sections |
| `references/ref_02_decision_journal.md` | Decision logging format, review prompts, pattern analysis questions |
| `references/ref_03_rejection_framework.md` | Rejection analysis framework; common PM rejection patterns; confounder taxonomy |
| `references/ref_04_offer_evaluation.md` | Offer evaluation framework; CTC check logic; negotiation escalation paths |

---

## 7. Build Checklist

- [ ] Write ref_01_briefing_templates.md
- [ ] Write ref_02_decision_journal.md
- [ ] Write ref_03_rejection_framework.md
- [ ] Write ref_04_offer_evaluation.md
- [ ] Write SKILL.md (lean orchestrator)
- [ ] Connect pipeline.json reader (linkright-hunt output)
- [ ] Connect user_setup.md reader (compensation, goals, constraints)
- [ ] Connect memory reader (linkright-mem output)
- [ ] Test morning briefing with sample pipeline data
- [ ] Test diary ingestion → candidate extraction → memory routing
- [ ] Test offer evaluation against sample user_setup.md

---

## 8. Success Criteria

- Morning briefing generated in <30 seconds
- Weekly review surfaces correct improvement areas
- Decision journal reviewed on schedule (zero missed entries)
- Rejection analysis completed for every ghosted/rejected opportunity
- Offer compensation check runs automatically and uses user_setup.md values
- Diary ingestion extracts ≥1 useful fact/signal candidate per entry
