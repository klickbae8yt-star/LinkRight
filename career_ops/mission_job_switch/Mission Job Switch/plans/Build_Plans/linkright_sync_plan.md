# linkright-sync — Skill Plan

**Skill:** `/linkright-sync`  
**Version:** 2.0.0 (exists) → 2.1.0 (planned upgrade)  
**Build Phase:** Phase 2 upgrade  
**Status:** v2.0.0 SKILL.md operational; needs mem integration + generalization  

---

## 1. What This Skill Does

`linkright-sync` generates tailored, width-optimized, ATS-safe resumes and cover letters for specific job opportunities.

**v2.0.0 (current):** Works from raw resume text pasted by user.  
**v2.1.0 (upgrade):** Pulls facts + signals directly from `linkright-mem`. No pasting required. The same canonical memory produces consistent outputs across multiple applications.

**Two output paths:**
- **HTML:** Single-file, Tailwind CSS, pixel-perfect, hosted on GitHub Pages via linkright-push
- **Overleaf/LaTeX:** FAANGPath template, XeLaTeX, width-measured via .log file

---

## 2. Format Paths

### Path A — HTML Resume

- Single HTML file with inline Tailwind CSS
- Width measurement: `scripts/measure_width.py` (Roboto 10px, BULLET_BUDGET = 158.07mm for A4)
- Target: 95–100% line fill per bullet
- Rendered to PDF via browser print
- Best for: tech companies, startups, modern hiring processes

### Path B — Overleaf / LaTeX Resume

- FAANGPath template: `\documentclass[a4paper,10pt]{resume}`
- Width measurement: LaTeX `.log` file analysis
  - `Overfull \hbox` = bullet too long → trim
  - `Underfull \hbox (badness N)` = bullet too short → expand
  - Target: zero hbox warnings + badness ≤ 200
- Best for: companies where LaTeX is expected or user prefers LaTeX workflow

---

## 3. The 7-Gate Pipeline

### Gate 0 — Format Fork (ALWAYS FIRST)

```
FIRST QUESTION, NO EXCEPTIONS:
Which output format?
A) HTML (Tailwind CSS, pixel-perfect, GitHub Pages)
B) Overleaf/LaTeX (FAANGPath template, XeLaTeX)
```

Format choice governs all downstream behavior. Must be documented at session start.

### Gate 1 — Input Collection

1. JD source: paste URL → fetch, or paste text directly
2. Profile source:
   - v2.0.0: "Paste your current resume text"
   - v2.1.0: Automatic load from linkright-mem (no paste)
3. Target archetype: inferred from JD analysis, or ask user to confirm

### Gate 2 — JD Analysis

Run full JD analysis (same pipeline as linkright-hunt):
- Extract archetype, primary signals, secondary signals
- Extract recruiter language (vocabulary to mirror)
- Identify negative signals to avoid emphasizing
- Extract red flags

### Gate 3 — Signal Coverage Map

From user profile, compute coverage of JD requirements:

```
SIGNAL COVERAGE MAP:

JD Primary Signals:
  systems_thinking        → Profile: STRONG (3 facts) ✓
  ai_workflow_design      → Profile: MEDIUM (1 fact)  △
  stakeholder_leadership  → Profile: STRONG (4 facts) ✓

JD Secondary Signals:
  data_fluency            → Profile: WEAK (0 facts)  ✗ ← gap
  execution_rigor         → Profile: STRONG (2 facts) ✓

GAP SIGNALS: data_fluency
→ "I see data_fluency is required but your profile has no confirmed facts here.
   Do you have any data-related work I should know about before writing?"
```

User addresses gaps or confirms they don't have that signal. Both are fine — better to know now than have an undefendable resume bullet.

### Gate 4 — Content Generation (B&W Mode, ALWAYS)

Generate ALL resume content without any design decisions. Colors stay black. No accent. No styling.

**Why B&W first:** Design decisions should never influence content decisions. Width-optimize first, then apply color.

**HTML path:** Write all bullets using `color: #000000`. No accent colors anywhere.  
**LaTeX path:** Write all `\begin{rSection}{}` blocks and `\item` lines. Zero `\usepackage{xcolor}` yet.

**Bullet quality rules (applied to every bullet):**
- Lead with a strong, specific action verb
- Quantify outcomes where possible; if estimating, that's OK — own it
- Each bullet carries at least one priority signal
- No orphaned words: final line of any bullet ≥3 words
- No AI-smell phrases (see ref_03_bullet_quality.md for banned list)
- Every claim must be defensible in an interview — if you can't answer "why" or "how much", rewrite

**Width optimization loop — runs on EVERY bullet:**

HTML path:
```
Write bullet (aim for 95-110% of budget)
→ Run measure_width.py
→ <85%: expand until ≥95%
→ 95-100%: ship
→ >100%: trim until ≤100%
→ Max 3 iterations; if stuck, rewrite from scratch
```

LaTeX path:
```
Write bullet (aim for 95-110% of budget in character count)
→ Compile with XeLaTeX
→ Check .log:
    No hbox warning + badness 0-200 → ship
    Overfull \hbox → trim
    Underfull \hbox badness 201-1000 → expand if possible
    Underfull \hbox badness >1000 → rewrite
→ Max 3 iterations; if stuck, rewrite
```

**LaTeX badness reference:**
| Badness | Status | Action |
|---|---|---|
| 0 | Perfect | Ship |
| 1–200 | Target zone | Ship |
| 201–1000 | Acceptable | Try to expand |
| 1001–9999 | Sparse | Rewrite |
| 10000 | Terrible | Rewrite |

### Gate 5 — Content Review

Show complete resume content to user, section by section.

Run constraint validation:
- Check all content against user_setup.md `hard_constraints` and `do_not_mention`
- Flag any violation with exact text and reason
- Block delivery until all flags are resolved

User approves or requests edits. Only approved content proceeds to Gate 6.

### Gate 6 — Design Application

Apply visual design ONLY after content is approved and width-optimized.

**HTML path:**
- Apply accent color (from user_setup.md preferences, or ask)
- Apply font pairing
- Apply section spacing
- Run one final measure_width.py pass — verify widths didn't shift after styling

**LaTeX path:**
- Add `\usepackage{xcolor}` (NOW, not before)
- Add `\definecolor{accent}{HTML}{[color]}` 
- Apply color to section headers and name
- Compile final PDF
- Check .log one final time

### Gate 7 — Delivery

Final validation checklist:
- [ ] ATS scan: no tables, no text boxes, no columns that break parsing
- [ ] AI-smell scan: no flagged phrases
- [ ] One-page check (or confirmed two-page if senior/long career)
- [ ] Constraint validation: zero violations
- [ ] Width: all bullets 95-100% (HTML) or badness ≤200 (LaTeX)
- [ ] Identity consistency: signals in resume match target archetype

Output:
- HTML: `resume_<company-slug>_<date>.html` + PDF
- LaTeX: `resume_<company-slug>_<date>.tex` + PDF
- Store version in linkright-push (if connected)
- Return: files + public URL (if pushed)

---

## 4. Width Optimization — Absolute Rules

### HTML Path
- `BULLET_BUDGET = 158.07mm` (Roboto 10px, A4, standard margins)
- Tool: `scripts/measure_width.py`
- Target: 95–100% fill
- **NEVER** set `height: 1.2em; overflow: hidden;` on any bullet container — this hides content, doesn't fix it
- **NEVER** skip measurement and eyeball — every single bullet must be measured

### LaTeX Path
- Budget: defined by FAANGPath geometry (standard A4)
- Tool: `.log` file from XeLaTeX compilation
- Target: zero hbox warnings, badness ≤ 200
- **NEVER** use `measure_width.py` on LaTeX — wrong font metrics
- **NEVER** add `\usepackage{xcolor}` before Gate 6

---

## 5. Cover Letter Generation

After resume is finalized, cover letter is optional but follows strict rules:

Structure:
1. **Opening:** Why this company, why this role — must be specific to something real (a product, a decision, a challenge)
2. **Evidence:** 2-3 sentences bridging your strongest signals to their stated requirements
3. **Ask:** Clear, confident close with specific ask

Hard rules:
- **NEVER** open with: "I am excited to apply for..." — universally weak
- **NEVER** write: "I believe I would be a great fit" — tell, don't beg
- **ALWAYS** mention something specific about the company (real product, recent news, stated challenge)
- **Maximum 300 words**

---

## 6. ATS Optimization Rules

Apply to both HTML and LaTeX output:

- NO tables for layout
- NO text boxes or floating elements
- NO headers/footers carrying critical information
- NO graphics or icons that carry meaning
- Section headings: plain text only
- HTML fonts: web-safe (Roboto via Google Fonts is fine)
- Always provide PDF alongside HTML

---

## 7. v2.1.0 Upgrade: linkright-mem Integration

After linkright-mem is operational, Gate 1 changes:

```
BEFORE (v2.0.0):
User pastes resume → skill parses raw text → writes bullets

AFTER (v2.1.0):
Skill calls linkright-mem with target archetype
→ Gets: ranked signals + strength + supporting facts + cached expressions
→ Signal coverage map is auto-populated
→ User reviews the map, not raw text
→ Bullets are written from confirmed facts, not inferred from paste

BENEFIT:
  Same facts → same signals → consistent positioning across all applications
  No manual paste → faster startup
  Every bullet traces to a confirmed fact → fully defensible
```

---

## 8. Hard Rules (Complete List)

- **ALWAYS** ask format (HTML vs Overleaf) as the very first question
- **ALWAYS** generate content in B&W before applying any color
- **ALWAYS** run width measurement on every bullet — no exceptions ever
- **ALWAYS** run constraint validation before showing user final output
- **ALWAYS** run ATS scan before delivery
- **NEVER** add `\usepackage{xcolor}` before Gate 6
- **NEVER** use `measure_width.py` on LaTeX text
- **NEVER** set `height: 1.2em; overflow: hidden;` on bullet containers (HTML)
- **NEVER** deliver a resume with any bullet at >100% budget (HTML) or Overfull hbox (LaTeX)
- **NEVER** include content that violates user_setup.md hard_constraints
- **NEVER** write cover letter that opens with "excited to apply" or "great fit"

---

## 9. References to Load (Gate-by-Gate)

| Gate | Load |
|---|---|
| Gate 0-1 | Nothing |
| Gate 2 | `ref_01_jd_analysis.md` |
| Gate 3 | `ref_02_signal_mapping.md` |
| Gate 4 | `ref_03_bullet_quality.md` (HTML) OR `ref_04_faangpath_template.md` (LaTeX) |
| Gate 6 HTML | `ref_05_html_design.md` |
| Gate 7 | `ref_06_ats_rules.md` |

---

## 10. Scripts

| Script | Purpose |
|---|---|
| `scripts/measure_width.py` | Measure HTML bullet width in mm (Roboto 10px) |
| `scripts/log_parser.py` | Parse XeLaTeX .log → hbox warnings + badness per line |
| `scripts/ai_smell_checker.py` | Flag AI-generated language patterns |
| `scripts/ats_scanner.py` | Check HTML/tex for ATS-hostile formatting |
| `scripts/constraint_checker.py` | Check resume content against user_setup.md |

---

## 11. Build Checklist (v2.1.0 Upgrade)

- [ ] Connect Gate 1 to linkright-mem signal retrieval API
- [ ] Update Gate 3 signal coverage map to pull from memory
- [ ] Write ref_01_jd_analysis.md
- [ ] Write ref_02_signal_mapping.md
- [ ] Write ref_03_bullet_quality.md (verb bank + banned phrases list)
- [ ] Write ref_04_faangpath_template.md (full command reference)
- [ ] Write ref_05_html_design.md (design system, color palettes)
- [ ] Write ref_06_ats_rules.md
- [ ] Upgrade constraint_checker.py to read from user_setup.md
- [ ] End-to-end test: JD → HTML resume → measure_width pass → delivery
- [ ] End-to-end test: JD → LaTeX resume → compile → log check → delivery

---

## 12. Success Criteria

- 100% of bullets width-measured (zero eyeballed)
- Zero constraint violations at delivery
- ATS scan passes for all output
- Cover letter never opens with a banned phrase
- Resume generation time Gate 0 → Gate 7: <25 minutes for experienced user
- v2.1.0: No manual resume paste required — full mem integration
