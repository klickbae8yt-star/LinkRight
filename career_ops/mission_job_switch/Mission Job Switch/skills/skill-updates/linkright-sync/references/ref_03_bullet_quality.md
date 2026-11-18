# ref_03 — Bullet Quality Standards

Loaded at Gate 4 (HTML path). Complete guide to writing and validating resume bullets.

---

## The Non-Negotiable Rules

Every bullet must pass all 5 before it ships:

1. **Specific action verb** — not on the banned list; not "managed", "worked on", "helped with"
2. **Signal-carrying** — demonstrates at least one priority signal from the coverage map
3. **Quantified or honest** — a number, %, time delta, scale indicator, or an honest "~" estimate
4. **Defensible** — you can answer "why did you do it that way?" and "what was the actual impact?"
5. **Clean last line** — final line of the bullet ≥3 words (no orphaned single word)

---

## Strong Action Verb Bank

Use these. Rotate. Don't repeat the same verb more than twice in a resume.

**Defining & Scoping**
defined, scoped, designed, architected, formulated, mapped, structured, framed

**Building & Shipping**
built, launched, shipped, deployed, delivered, developed, implemented, created, wrote

**Driving & Leading**
led, drove, directed, owned, headed, steered, ran, managed

**Analyzing & Discovering**
identified, analyzed, diagnosed, uncovered, modeled, benchmarked, measured, evaluated

**Improving & Optimizing**
reduced, improved, accelerated, cut, streamlined (use sparingly), eliminated, optimized, refactored

**Aligning & Influencing**
aligned, partnered, negotiated, influenced, secured, earned, persuaded, convinced

**Initiating**
initiated, proposed, introduced, piloted, prototyped, established, set up

**Communicating**
presented, authored, documented, briefed, synthesized, communicated, published

---

## Banned Verbs (Run ai_smell_checker.py — these are flagged)

```
spearheaded, championed, orchestrated, catalyzed, evangelized, synergized,
leveraged, utilized, facilitated, revolutionized, transformed, pioneered,
architected (overused), garnered, curated, ideated, conceptualized,
socialized (in the "socialized the idea" sense), operationalized,
institutionalized, galvanized
```

---

## Banned Phrases (Run ai_smell_checker.py — these are flagged)

```
"significant improvement / increase / reduction"
"dramatic improvement"
"key stakeholders" (use specific names/roles instead)
"cross-functional stakeholders"
"end-to-end ownership" (show it, don't say it)
"took ownership of"
"holistic approach / solution"
"thought leadership"
"best-in-class", "world-class", "cutting-edge", "state-of-the-art"
"seamless experience / integration"
"proven track record of"
"results-oriented"
"strong communication skills"
"team player"
"detail-oriented"
"successfully launched/delivered" ("successfully" is filler — just say "launched/delivered")
"ability to [do X]" — replace with "demonstrated [X] by..."
```

---

## Quantification Rules

**Always prefer:** specific number > range > qualifier > nothing

| Instead of | Write |
|---|---|
| "many stakeholders" | "12 stakeholders across 4 orgs" |
| "significantly faster" | "40% faster" or "from 14 days to 3 days" |
| "large user base" | "18,000 users" or "~18K MAU" |
| "improved conversion" | "increased trial conversion from 12% to 19%" |
| "reduced support tickets" | "reduced L1 support volume by 35%" |

**When you have to estimate:** Use `~` and own it. "~40% reduction (based on support ticket count pre/post)"
This is more credible than a vague claim and fully defensible.

**When you genuinely have no metric:** Say something about scale or scope instead.
"Owned roadmap for 3 enterprise integrations serving 200+ internal users"
Scale + ownership is better than a fabricated number.

---

## Structure Patterns by Signal

### systems_thinking
> "[Action] [complex system/cross-team scenario], coordinating [N teams / roles],
> resulting in [outcome that shows end-to-end thinking]."

### stakeholder_leadership
> "[Action] alignment across [specific roles], [what was the disagreement/complexity],
> [how resolved], [outcome]."

### execution_rigor
> "[Delivered/Shipped] [what] [on time / ahead of schedule / within scope] for [N users / teams],
> [specific metric or milestone]."

### data_fluency
> "[Analyzed/Built/Designed] [specific data artifact] using [tool if notable],
> enabling [specific decision or outcome with number]."

### ai_workflow_design
> "[Designed/Built] [AI feature/pipeline], [what it does], [how it handles edge cases / human review],
> [adoption or quality outcome]."

### growth_experimentation
> "[Designed/Ran] [A/B test or experiment] on [hypothesis], achieving [result],
> [what decision this unlocked]."

---

## Width Fill Guidance

Target: 95–100% of BULLET_BUDGET (158.07mm for HTML Roboto 9.5pt)

**If bullet is too short (<85%):**
- Add a specific result or number
- Add the team/org context ("across 4 engineering teams")
- Add the "so what" — what did this enable downstream?
- Add the constraint that made it hard ("in 6 weeks despite API instability")

**If bullet is too long (>100%):**
- Use `scripts/suggest_synonyms.py` for shorter word swaps
- Remove filler: "in order to" → "to", "was able to" → remove, "in the context of" → "in"
- Cut the weakest qualifying clause
- Move a phrase to a separate bullet if it's truly a separate achievement

---

## Section-Level Rules

### Work Experience bullets
- 3–5 bullets per role (more for recent/relevant, fewer for older)
- First bullet in each role: the most signal-dense, most quantified achievement
- Last bullet in each role: can be broader scope/ownership statement
- Never two consecutive bullets that start with the same verb

### Skills section
- List tools/technologies that appear in the JD or demonstrate relevant signal
- No soft skills in the skills section (communication, leadership — prove these in bullets)
- Group logically: PM tools | Data | Technical | Domain

### Education section
- For 3+ years experience: 2 lines max (degree, university, year, GPA only if strong)
- For <3 years: can add relevant coursework, but only if genuinely relevant to the role
- Never list GPA below 3.5/7.0 equivalent
