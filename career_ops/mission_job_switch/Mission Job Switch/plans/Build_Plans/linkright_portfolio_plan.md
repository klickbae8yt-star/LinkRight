# linkright-portfolio — Skill Plan

**Skill:** `/linkright-portfolio`  
**Version:** 1.0.0 (planned)  
**Build Phase:** Phase 3  
**Status:** Not yet built  

---

## 1. What This Skill Does

`linkright-portfolio` converts raw professional experience into structured, externally-shareable proof of work.

It produces:
- PM case studies in a consistent structured format
- Proof-of-thinking (POT) write-ups targeting specific companies
- A GitHub Pages portfolio site (hosted via linkright-push)
- Company research briefs for interview preparation

The philosophy: **Show your thinking, not just your history.** Any PM can list what they did. A strong PM portfolio demonstrates how they think about products — what problems they see, what trade-offs they navigate, what they'd do differently.

---

## 2. Case Study Structure

Every case study uses this 7-section format. All 7 sections are required:

```
1. CONTEXT
   Company stage, team composition, your specific role, timeframe.
   (What was the environment you were operating in?)

2. PROBLEM
   What was broken, missing, or unclear? What evidence showed this?
   (Not "we wanted to improve X" — what was actually wrong?)

3. CONSTRAINTS
   What you could NOT change: tech debt, org constraints, time, resources, politics.
   (This section shows PM maturity more than any other)

4. APPROACH
   How you thought about it — frameworks used, hypotheses formed,
   what alternatives you considered and why you chose this path.
   (Show your reasoning, not just your actions)

5. EXECUTION
   What you actually did — who you worked with, what decisions you made,
   how you kept things moving, what got hard and how you navigated it.
   (Specific > generic)

6. OUTCOME
   Quantified results wherever possible.
   If estimating: label it honestly ("user-reported", "internal estimate").
   Be clear about your direct contribution vs team contribution.

7. WHAT I LEARNED
   One honest, specific learning. Not a PR statement.
   "I learned that I underweighted engineering complexity when making timeline promises."
   This section is NON-OPTIONAL — it's what separates strong PMs from polished ones.
```

**The constraint check:** Before finalizing any case study, verify it passes the user's constraint validation — no work claimed that isn't theirs, no companies that shouldn't be mentioned, no metrics inflated beyond what they can defend.

---

## 3. Proof-of-Thinking (POT) Format

A POT is a 400-600 word analysis of a specific product decision or opportunity at a real company.

Structure:
```
OBSERVATION
  One specific thing you noticed: a feature, a UX decision, a missing capability,
  an unusual metric, a pricing choice. Specific, not general.

HYPOTHESIS
  Why do you think this is the case? What was the company optimizing for?
  What constraint or incentive explains their current state?

TRADE-OFF
  What did their decision optimize for, and what did it sacrifice?
  There is always a trade-off — surface it specifically.

YOUR TAKE
  What would you explore or change if you were the PM?
  Concrete, actionable, and honest about uncertainty.
  "I would run a test on X because Y" > "I think they should improve X"

SIGNAL
  (Optional) What this analysis reveals about your approach or values as a PM.
```

**POT hard rules:**
- ALWAYS specific to ONE thing — not "thoughts on Company X's strategy"
- NEVER generic praise of the company
- ALWAYS shows a concrete trade-off or decision point
- NEVER just criticism — curious and constructive, not snarky
- MUST reference something real and verifiable (a feature that exists, not speculation)
- Research the company before writing — 15 minutes of actual product usage minimum

---

## 4. Portfolio Site Architecture

Hosted on GitHub Pages via linkright-push.

```
portfolio/
├── index.html              ← intro + featured projects + contact
├── cases/
│   ├── <case-slug>.html    ← each full case study as its own page
│   └── ...
└── about.html              ← professional narrative (not a resume)
```

**Site design principles:**
- Clean and fast — no heavy JS frameworks
- Mobile-first rendering
- Each case study page: full 7-section case study + 3-bullet summary for quick scanners
- No personal photos unless user provides one
- Strong information hierarchy: recruiter should see your best story in 10 seconds

**Featured projects:** Select 3 for the homepage based on:
- Strongest quantified outcomes
- Best match for target archetype
- Most differentiated (avoid 3 similar stories)

---

## 5. Metrics Extraction

Before writing case studies, extract all quantified outcomes from memory:

```
From memory/facts.md:
Scan for: percentages, ratios, time reductions, adoption numbers,
          dollar amounts, user counts, frequency changes

Output: metrics_inventory.md
  - Metric, context, confidence level, fact_id

Examples of metric types to capture:
  - Time savings: "reduced from X days to Y days"
  - Adoption: "increased from X% to Y%"
  - Volume: "handled N users / requests / tickets"
  - Revenue: "contributed to $X ARR / cost savings"
  - Efficiency: "cut X by Y%"
```

**Metrics rules:**
- NEVER fabricate or inflate
- If metric is an estimate: label it ("user-reported estimate", "internal tracking")
- Percentage changes preferred over absolute numbers (harder to question without context)
- If you don't have a metric: say "we didn't measure this rigorously" — more credible than a vague claim

---

## 6. Company Research Brief

For each target company, before a POT or interview:

```
OUTPUT: 1-page research brief

SECTIONS:
1. Product overview: what they sell, to whom, at what stage
2. Core product decisions: notable UX, pricing, or strategy choices
3. Known PM challenges: from job descriptions, PM blog posts, Glassdoor
4. Recent news: funding, launches, pivots, team changes
5. What kind of PM they seem to value: signals from their hiring language
6. POT opportunity: one specific angle you could explore in writing
```

---

## 7. Skill Gates

### Gate 1 — Mode Selection

```
What do you want to create?
a) Case study for a specific project
b) Proof-of-thinking for a target company
c) Full portfolio site
d) Extract and organize metrics from memory
e) Company research brief
```

### Gate 2 — Content Gathering

**Case study:** Load relevant facts and signals from linkright-mem. Identify any gaps. Ask user to fill gaps.  
**POT:** Research target company product (web search + user's own observation). Identify the specific angle.  
**Portfolio:** Load all existing case studies. Select top 3 for homepage.  
**Research brief:** Web search + user's observations.

### Gate 3 — Draft Generation

Write full draft following the relevant structure exactly.

For case studies: use 7-section structure — no section skipped.  
For POT: use 5-section structure — observation must be specific and real.  
For portfolio: generate HTML pages following site architecture.

### Gate 4 — Constraint Validation

Run all content through user_setup.md constraint check:
- No claimed work that is marked as not owned
- No companies in the do-not-mention list
- No metrics beyond what user can defend

Block delivery on any violation.

### Gate 5 — Review + Finalize

Show draft. User reviews section by section.  
For case studies: especially scrutinize Section 7 (What I Learned) — should be honest, not performative.

### Gate 6 — Publish

Write final files.  
If portfolio site: call linkright-push to deploy to GitHub Pages.  
Return URLs of published content.

---

## 8. Hard Rules

- **ALWAYS include Section 7 (What I Learned)** in every case study — non-negotiable
- **ALWAYS label estimated metrics** — never present estimates as hard numbers
- **NEVER write generic POT** — must reference a specific, real product decision
- **ALWAYS run constraint validation** before any case study is published
- **NEVER publish work that violates user_setup.md** hard_constraints
- **NEVER claim team outcomes as personal outcomes** without clear scope framing

---

## 9. References to Write

| File | Contents |
|---|---|
| `references/ref_01_case_study_template.md` | Full template with examples; section-by-section guidance; strong vs weak examples for each section |
| `references/ref_02_pot_examples.md` | 3 example POT write-ups: one strong, one mediocre, one weak — with annotated differences |
| `references/ref_03_portfolio_html_template.md` | Full HTML/CSS template for portfolio pages; index + case study page layout |
| `references/ref_04_research_prompts.md` | Company research checklist and structured prompt for research brief generation |

---

## 10. Build Checklist

- [ ] Write ref_01_case_study_template.md
- [ ] Write ref_02_pot_examples.md
- [ ] Write ref_03_portfolio_html_template.md
- [ ] Write SKILL.md (lean orchestrator)
- [ ] Generate first case study from existing memory
- [ ] Generate first POT for one target company
- [ ] Build portfolio HTML shell
- [ ] Push to GitHub Pages via linkright-push
- [ ] Confirm live URL and rendering

---

## 11. Success Criteria

- At least 3 case studies with quantified outcomes
- Each case study passes constraint validation
- At least 2 POT write-ups ready before first interview at target company
- Portfolio site live on GitHub Pages
- No case study missing Section 7 (What I Learned)
