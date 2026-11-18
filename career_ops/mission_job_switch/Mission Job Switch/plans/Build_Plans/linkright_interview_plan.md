# linkright-interview — Skill Plan

**Skill:** `/linkright-interview`  
**Version:** 1.0.0 (planned)  
**Build Phase:** Phase 2  
**Status:** Not yet built  

---

## 1. What This Skill Does

`linkright-interview` prepares you for every stage of the interview process — screening calls to final panel rounds.

It produces:
- STAR-format answer banks from confirmed memory facts
- Likely question lists tailored to JD and archetype
- Answer drafts with constraint validation
- Mock interview sessions with stress-testing
- Salary negotiation scripts (pulled from user_setup.md)
- Tell-me-about-yourself intros per target role/archetype

Core philosophy: **Every answer must survive the follow-up.** A polished answer you can't defend when pressed is worse than a simple answer you fully own.

---

## 2. The STAR-L Format

Standard STAR (Situation → Task → Action → Result) extended with Learning:

```
SITUATION:   Set context — company stage, team size, time period (2 sentences max)
TASK:        What was specifically yours to own (not "we worked on")
ACTION:      What YOU specifically did — decisions made, trade-offs navigated
RESULT:      Quantified where possible; estimates are fine if labeled honestly
LEARNING:    One honest takeaway — shows self-awareness, separates top candidates
```

**The Learning component** is optional to say in a real interview, but mandatory when building the story — it helps you speak authentically and catch stories that don't actually reflect well on you before you're in the room.

**Defensibility rule:** Before any story is finalized, ask: "If they follow up with 'Why that approach?' and 'What would you do differently?' — can you answer both fluently?" If not, the story needs more work.

---

## 3. Story Types

Every PM interview tests from a set of ~8 story types. Each user should have at least 2 strong stories per type:

| Story Type | Core Test | Sample Question |
|---|---|---|
| Ambiguity handling | Can you operate without clear direction? | "Tell me about a time you had to define scope from scratch" |
| Stakeholder conflict | Can you navigate org complexity? | "Tell me about a disagreement with an engineering partner" |
| Data-driven decision | Data vs intuition balance | "How did you decide between two competing product directions?" |
| Failure + learning | Self-awareness, resilience | "Tell me about a product that didn't land as expected" |
| Cross-functional leadership | Lead without authority | "How did you get other teams to prioritize your roadmap?" |
| Systems thinking | Sees whole system, not just parts | "Walk me through how you approached this complex problem" |
| Customer obsession | Users are real, not abstract | "Tell me about a time user insight changed your direction" |
| Vision + prioritization | Long-term thinking under pressure | "How do you prioritize when everything seems urgent?" |

**Minimum viable story bank:** 2 stories × 8 types = 16 stories  
**Strong story bank:** 3 stories × 8 types = 24 stories (handles follow-ups like "tell me another")

---

## 4. Constraint Validation (Truth Engine)

Before any story is added to the story bank, it runs through constraint validation:

```
CHECK 1: Hard constraints
  → Read user_setup.md hard_constraints
  → Flag any story that references work listed as NOT-OWNED or DO-NOT-CLAIM
  → Flag any company/project in do_not_mention list

CHECK 2: Unquantified metrics
  → "significantly improved" without a number → flag as weak
  → "dramatically reduced" without evidence → flag

CHECK 3: Ownership clarity
  → "We built..." without specifying what YOUR role was → flag
  → Scope creep: claiming outcomes of a team as personal outcome → flag

CHECK 4: Defensibility self-test
  → Would you be comfortable if interviewer did a reference check on this specific claim?
  → Can you answer: "Why that approach specifically?" and "What would you do differently?"
  → If no to either: flag as needs strengthening
```

If flagged: show exact issue, offer targeted rewrite. User must resolve before story is saved.

---

## 5. Question Bank Generation

Given a JD and archetype, generate likely interview questions:

**Layer 1 — Universal PM questions (archetype-independent):**
From the KB behavioral question taxonomy: 10-15 questions every PM is asked.

**Layer 2 — Archetype-specific questions:**
- AI PM: model evaluation decisions, AI trust UX, prompt system design
- Enterprise PM: large-org navigation, implementation management, B2B buyer dynamics
- Growth PM: experiment design, metric tradeoffs, growth loop design
- Platform PM: API design philosophy, developer experience, platform governance

**Layer 3 — JD-derived questions:**
Extract specific scenarios from the JD text → generate likely behavioral questions
e.g. "JD mentions 'leading without authority across 5 teams' → likely question: stakeholder conflict story"

**Layer 4 — Company-stage questions:**
- Startup: "How do you prioritize with no data?" "Tell me about working with limited resources"
- Enterprise: "How do you drive change in a complex org?" "Tell me about managing stakeholder politics"

For each question: suggest the best matching story from the user's story bank.

---

## 6. Mock Interview Mode

Full simulated interview:

```
ROUND 1: Warm-up
  Interviewer: "Tell me about yourself."
  User: [gives intro]
  Interviewer: [follows up on one specific claim in the intro]

ROUND 2: Behavioral
  Interviewer: [asks from generated question bank]
  User: [answers]
  Interviewer: [ONE follow-up: probes the weakest part of the answer]

ROUND 3: Stress test
  Interviewer: "Let me push back on [specific claim]..."
  User: defends

JUDGE PASS (after each round):
  Evaluate: Was the answer defensible? Was the STAR structure clear?
  Score: 1-5 on each: clarity, specificity, defensibility, authenticity
  Flag: single weakest moment

DEBRIEF:
  - Strongest story
  - Weakest moment + why + how to fix
  - One specific language improvement
```

Mock interview rules:
- Always probe at least once per answer
- Feedback must be concrete — not "great job" but "the result in your second story was vague; what was the actual metric?"
- Identify the single story most likely to fail under a tough interviewer

---

## 7. Tell-Me-About-Yourself Framework

Three versions: one per target archetype in user_setup.md.

Structure (90-120 seconds):
```
Past: "[X] years in [domain] — what I've been building toward"
Present: "Currently [or most recently], I [strongest signal] at [company]"
This role: "I'm specifically interested in [company] because [real specific reason]"
Hook: "[One sentence that connects your past to this exact opportunity]"
```

Rules:
- Under 120 seconds when spoken aloud (record yourself to check)
- Must signal target archetype in first 2 sentences
- Must reference something specific about the company (not generic "I love your mission")
- Ends with a hook that invites them to ask a follow-up you're prepared for

---

## 8. Salary Negotiation Scripts

Pulled from user_setup.md (`current_ctc`, `target_ctc_min`, `target_ctc_target`).

**Opening line (when asked "what are your expectations?"):**
```
Personalized from user_setup:
"I'm currently at [current_ctc]. For this role and seniority level,
I'm targeting [target_ctc_target]. Does that work within your range?"
```

**If pushed below target_min:**
```
"I appreciate the context. Before I can say whether there's flexibility,
could you walk me through the full package — base, equity, and bonus?
I want to evaluate total compensation."
```

**If they reveal range first:**
```
If range includes your target: anchor at the top of the range
If range is below target_min: "That's a bit below what I was targeting —
is there flexibility there, or should we talk about other parts of the package?"
```

**Rules:**
- Never volunteer a lower number to "seem reasonable"
- Never say "I'm flexible" without anchoring first
- Never negotiate against yourself before they've made an offer

---

## 9. Skill Gates

### Gate 1 — Mode Selection

```
What do you need?
a) Build STAR stories from my experience
b) Generate likely questions for a specific JD
c) Draft answer to a specific question
d) Run full mock interview
e) Prepare tell-me-about-yourself intro
f) Build salary negotiation script
g) Stress-test a story I already have
```

### Gate 2 — Load Context

For a-d: Load signals + facts + existing story bank from linkright-mem.  
For b-d: Load JD analysis from linkright-hunt (if opportunity exists) or parse pasted JD.  
For f: Load compensation config from user_setup.md.

### Gate 3 — Generate Draft

**STAR story building:**
1. For each story type, find best supporting fact cluster in memory
2. Write STAR-L story
3. Show to user: "Does this accurately represent what happened?"
4. User corrects any factual inaccuracy
5. Run constraint validation
6. Save to `memory/expressions/stories/<story-id>.md`

**Question bank:**
Generate layered question list → map each question to best existing story → show gaps.

**Answer draft:**
Match question to story → write answer → run constraint validation → show user.

### Gate 4 — Constraint Validation

Run Truth Engine on all outputs. Block delivery on any violation.

### Gate 5 — Save / Update Story Bank

All finalized stories saved to memory with:
- Story type tag
- Signals it demonstrates
- Date created/updated
- Constraint validation status: clean

---

## 10. Hard Rules

- **ALWAYS run constraint validation before any story is finalized** — no exceptions
- **ALWAYS enforce: every claim must be defensible under "why?" follow-up**
- **NEVER mark a story as clean if it contains unresolved constraint flags**
- **ALWAYS build salary script from user_setup.md** — never hardcode numbers
- **ALWAYS stress-test in mock interview** — a story that hasn't been follow-up questioned is not ready
- **NEVER claim work as owned if user_setup.md marks it as someone else's**

---

## 11. References to Write

| File | Contents |
|---|---|
| `references/ref_01_story_bank.md` | All confirmed STAR-L stories, organized by story type and signal |
| `references/ref_02_question_bank.md` | Master question bank: universal PM + 8 archetypes |
| `references/ref_03_intro_scripts.md` | Tell-me-about-yourself versions by archetype (generated from user's profile) |
| `references/ref_04_salary_framework.md` | Salary negotiation frameworks, scripts, and escalation paths |
| `references/ref_05_mock_rubric.md` | Mock interview scoring rubric, debrief format, debrief questions |

---

## 12. Build Checklist

- [ ] Write ref_02_question_bank.md (draw from Research_Linkright KB — archetype question patterns)
- [ ] Write ref_04_salary_framework.md (negotiation logic, not hardcoded numbers)
- [ ] Write ref_05_mock_rubric.md
- [ ] Write SKILL.md (lean orchestrator)
- [ ] Write scripts/constraint_validator.py
- [ ] Test: ingest 3 facts → generate STAR story → validate constraints → save
- [ ] Test: generate question bank from sample JD
- [ ] Test: mock interview with debrief

---

## 13. Success Criteria

- Minimum viable story bank: 16 stories (2 per type)
- All stories constraint-validated clean
- Tell-me-about-yourself under 120 seconds spoken
- Salary script anchored correctly from user_setup.md
- Mock interview: all stories survive 1 follow-up question
