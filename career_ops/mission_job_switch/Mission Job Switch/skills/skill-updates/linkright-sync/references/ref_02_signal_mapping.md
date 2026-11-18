# ref_02 — Signal Mapping & Coverage Assessment

Loaded at Gate 3. Defines how to map JD signal requirements against user profile.

---

## Signal Strength Definitions

When assessing a user's profile against a signal, classify strength as:

| Strength | Definition | Evidence Required |
|---|---|---|
| **STRONG** | Signal is clearly and repeatedly demonstrated | 3+ confirmed facts; quantified outcomes |
| **MEDIUM** | Signal is present but not the dominant pattern | 1–2 confirmed facts; one quantified outcome |
| **WEAK** | Signal exists but is implied or minor | 1 fact, unquantified or mentioned in passing |
| **ABSENT** | No evidence of this signal in the profile | 0 facts |

---

## Signal → Fact Mapping

For each required signal, find supporting facts in the user's profile (layer_1 / career profile):

### systems_thinking
Look for: end-to-end ownership stories, cross-functional coordination across 3+ teams, breaking down complex systems into components, identifying upstream/downstream dependencies.

### ambiguity_handling
Look for: 0-to-1 projects, moments where the user had to define the problem before solving it, greenfield initiatives, pivots mid-execution.

### stakeholder_leadership
Look for: presenting to VP/C-level, aligning conflicting parties, getting sign-off without direct authority, managing disagreement productively.

### execution_rigor
Look for: on-time launches, multi-sprint planning, risk management, managing scope cuts, tracking velocity.

### user_empathy
Look for: user interviews conducted, feedback loops created, features changed based on user insight, customer advisory panels.

### data_fluency
Look for: SQL queries written, metrics frameworks built, A/B tests run, dashboards created, data-driven prioritization decisions.

### communication_clarity
Look for: docs written (PRDs, strategy docs), all-hands presentations, external communication (customer-facing), written clarity under pressure.

### ai_workflow_design
Look for: designing features with AI/ML components, prompt engineering work, human-in-the-loop systems, AI output validation.

### model_evaluation
Look for: evaluating LLM/ML outputs for quality, defining eval criteria, building evals frameworks, comparing model versions.

### enterprise_workflow_ownership
Look for: owning implementation from sale through go-live, managing customer integration timelines, post-sale product ownership.

### b2b_buyer_psychology
Look for: involvement in sales cycles, understanding procurement steps, navigating security reviews, building business cases for customers.

### growth_experimentation
Look for: A/B test design and execution, hypothesis documentation, statistical significance, learning synthesis.

### funnel_optimization
Look for: conversion rate work, activation improvements, drop-off analysis, funnel instrumentation.

### api_design_thinking
Look for: working with engineering on API contracts, versioning decisions, developer-facing feature design.

### data_pipeline_ownership
Look for: owning data products, defining data contracts, working with data engineers on reliability.

### self_serve_analytics
Look for: building BI dashboards, enabling non-technical teams to answer questions with data, reducing analyst dependency.

---

## Coverage Map Output Format

For each signal in the requirement list, output one line:

```
[signal_name]    → Profile: [STRONG/MEDIUM/WEAK/ABSENT]  ([N] fact(s): [brief desc])  [✓/△/✗]
```

Example:
```
systems_thinking       → Profile: STRONG  (3 facts: CRR architecture, Procol integration, AmEx pipeline) ✓
ai_workflow_design     → Profile: MEDIUM  (1 fact: GenAI extraction pipeline at AmEx) △
data_fluency           → Profile: WEAK    (1 fact: SQL usage mentioned, unquantified) △
model_evaluation       → Profile: ABSENT  (0 facts) ✗  ← GAP
```

---

## Gap Handling Protocol

For each ABSENT or WEAK signal that is **Primary** in the JD:

1. **Ask the user directly:**
   > "The JD requires [signal_name] as a primary signal, but your profile has [ABSENT/WEAK] coverage.
   > Do you have any work related to [brief description of what this signal means] that isn't
   > captured in your profile yet?"

2. **If user provides new fact:** Add to gap_fills for Gate 4. Use in bullet generation.

3. **If user confirms absence:** Note `[signal] — NOT CLAIMED`. Do not generate bullets for this.
   Never overclaim a signal you have no evidence for.

4. **For WEAK secondary/mentioned signals:** No need to ask. Note them as low-confidence.
   Write at most one gentle signal mention in a bullet.

---

## Archetype-Level Coverage Thresholds

For the resume to be credible for a given archetype:

| Archetype | Minimum primary signal coverage |
|---|---|
| AI PM | 2 of 3 AI-specific signals at MEDIUM+ |
| Enterprise PM | enterprise_workflow_ownership at STRONG; b2b_buyer_psychology at MEDIUM+ |
| Growth PM | growth_experimentation at MEDIUM+; funnel_optimization at any level |
| Platform PM | api_design_thinking at any level; developer_experience context present |
| Data/Analytics PM | data_fluency at STRONG; one of data_pipeline_ownership or self_serve_analytics at MEDIUM+ |

If user falls below threshold for their target archetype: flag it clearly and discuss.
Don't build a resume that misrepresents the candidate.
