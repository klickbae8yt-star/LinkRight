---
name: sync
description: >
  Build pixel-perfect, brand-customized, single-page resumes (HTML or Overleaf/LaTeX) from a candidate's resume, job description, and target company.
  This skill should be used when the user mentions "resume", "CV", "job application", "career document", "optimize my resume",
  "tailor my resume", "make my resume look professional", "build a resume for [company]", "one-page resume", "branded resume",
  or anything related to creating or improving a resume for a specific job posting. Also trigger if the user provides a job
  description and asks to align their experience with it. Even casual mentions like "I'm applying to Google" or "help me with
  my job application" should trigger this skill.
version: 2.0.0
---

# Sync — Resume Optimization Skill

Build a pixel-perfect, single-page, print-ready resume with rich brand colors, justified typography, and two-tier emphasis.  
**Every pixel of the page MUST be utilized — no blank areas, no wasted real estate, horizontally or vertically.**

---

## Format Fork — ALWAYS Ask at Gate 1

**ALWAYS ask the user this question before doing any other work:**

> "Do you want an **HTML resume** (browser-rendered, CSS-styled) or an **Overleaf/LaTeX resume** (FAANGPath template, compiles to PDF)?"

**NEVER proceed past Gate 1 without this answer.** All subsequent phases branch based on this choice. The two paths share the same content pipeline (Gates 1–5) but diverge at Gate 6 (design/colors) and delivery.

| | **HTML Path** | **Overleaf Path** |
|---|---|---|
| Template | `assets/template.html` | FAANGPath Simple Template |
| Font | Roboto 9.5pt (Google Fonts CDN) | Default (Helvetica/CM) |
| Width check | `measure_width.py` — run before EVERY line ships | Compile `.tex` → parse `.log` for `\hbox` warnings |
| Page fit check | `validate_page_fit.py` — run after EVERY company | Compile `.tex` → parse `.log` for `\vbox` overflow |
| Colors | CSS variables (`--brand-primary-color` etc.) | `\usepackage{xcolor}` + `\definecolor` |
| Output file | `.html` → optional PDF via Chrome Print | `.tex` → Overleaf compiles PDF |

---

## Architecture

You (Claude) handle all language tasks: interviewing, writing, strategy, emphasis. **ALWAYS delegate precision computation to bundled Python scripts via bash. NEVER eyeball widths, contrast, or page fit — always run the script.**

**Scripts** (in `scripts/` directory — run via `python ${CLAUDE_PLUGIN_ROOT}/skills/sync/scripts/<name>.py '<json>'`):

| Script | Purpose | When to Call |
|--------|---------|-------------|
| `measure_width.py` | Character-unit width of text vs line budget | **ALWAYS — before every single line ships (HTML path only)** |
| `score_bullets.py` | BRS scoring + tiering of candidate bullets | Gate 4 (Strategy) |
| `validate_contrast.py` | WCAG 2.0 AA color contrast check | **ALWAYS at Gate 6 — NEVER skip contrast validation** |
| `validate_page_fit.py` | Vertical A4 page budget — **HTML path only** | **ALWAYS after every company in Gates 3, 5, 7** |
| `suggest_synonyms.py` | Width-calibrated word swaps | Gate 5 when lines need trimming |
| `assemble_html.py` | Final HTML assembly from template — **HTML path only** | Gate 7 |

**Overleaf path — NEVER use `measure_width.py` or `validate_page_fit.py`.** These scripts are calibrated for Roboto 9.5pt web font and are meaningless in a LaTeX context. Always use `.log` parsing instead (see Overleaf section).

---

## 7-Gate Human-in-the-Loop Pipeline — MANDATORY

**ALWAYS stop at every gate and wait for explicit user confirmation before proceeding. NEVER auto-advance. NEVER skip a gate. NEVER combine two gates into one step.**

### Content-First Rule — B&W Mode (Gates 1–5)

> **NEVER introduce brand colors, CSS variable color assignments, or `\textcolor`/`\definecolor` commands during Gates 1–5.**

Write the entire resume in plain black-and-white mode through all content gates. Lock every word, every bullet, every section order, and confirm page fit BEFORE touching design.  
**Colors are introduced EXACTLY ONCE — at Gate 6 — after content is 100% approved by the user.**

| Gate | Phase | Present to User | User Must Confirm |
|------|-------|-----------------|-------------------|
| **1** | Intake + Format Choice | Parsed resume structure, JD keywords, company, **format choice (HTML vs Overleaf)** | "Inputs correct? HTML or Overleaf?" |
| **2** | Career Level + Section Order | Detected level + recommended section order | "Level correct? Overrides?" |
| **3** | Vertical Space + Page Budget | Remaining mm/lines + content volume options | "Which options to add?" |
| **4** | Strategy | Strategy recommendation + JD signals + BRS scores | "Accept or choose?" |
| **5** | Content Review (B&W) | Full section-by-section preview — **plain black text, zero colors** — all lines 95-100% fill confirmed | "Approve content? Edits?" |
| **6** | Design / Brand Colors | Color swatches with hex codes → apply to template | "Approve colors?" |
| **7** | Final Visual Review + Delivery | Quality grade report + file link | "Approve final resume?" |

Read `references/pipeline.md` for the complete phase-by-phase guide with gate details.

---

## Critical Rules

### NEVER GUESS DATES, LOCATIONS, OR TITLES
**ALWAYS use EXACTLY the dates, locations, job titles, company names, and degree names the candidate provided.** If any detail is missing or ambiguous, STOP and ASK — never infer, never approximate. Every single factual detail MUST come directly from the candidate's own words or documents.

### Contact Bar — ALWAYS Hyperlink Everything
- **Phone:** ALWAYS use full number, hyperlinked with `tel:` protocol
- **Email:** ALWAYS use full address, hyperlinked with `mailto:` protocol
- **LinkedIn:** ALWAYS display "LinkedIn" as visible text (NEVER the full URL), hyperlinked to profile
- **Portfolio:** ALWAYS use short domain as visible text, hyperlinked to full URL
- **NEVER display a raw URL as visible text in the contact bar**

### Bullet Grouping — HTML Path ONLY
**ALWAYS separate groups using `<li class="bullet-group-spacer" aria-hidden="true"></li>` and NOTHING ELSE.**  
**NEVER use `<div class="project-title">` or any visible project title element** — project titles are internal logic only, never rendered on the resume.

**Splitting table — ALWAYS follow this:** 2→[2], 3→[3], 4→[2]+[2], 5→[3]+[2], 6→[3]+[3]  
**NEVER place fewer than 2 bullets in a group. NEVER place more than 3. NEVER put more than 6 total bullets per company.**

### Strict One-Page Enforcement — NEVER Allow Page 2
- **HTML path:** A4 = 271.6mm usable height. **ALWAYS run `validate_page_fit.py` after EVERY company written in Gate 5.** If overflow detected, MUST trim the lowest-BRS bullet immediately. Do not defer trimming.
- **Overleaf path:** **ALWAYS compile `.tex` and check `.log` for `Overfull \vbox (Xpt too tall)` after writing each section.** If `X > 0`, MUST trim the lowest-BRS bullet and recompile before moving on.
- **NEVER deliver or present a resume that overflows to page 2 on either path.**

### Width Measurement — NEVER Skip, NEVER Eyeball
**NEVER publish a line without measuring it first. Target: exactly 95-100% fill. NEVER ship a line below 95%.**

**Tool by path — use the correct one, ALWAYS:**
- **HTML path:** ALWAYS measure with `measure_width.py` before a line ships. The browser gives no feedback — the script is the ONLY valid ruler.
- **Overleaf path:** ALWAYS compile and parse `.log` for `\hbox` warnings. NEVER use `measure_width.py` on LaTeX text — it will give wrong results.

**Methodology — ALWAYS write long, then trim down:**
1. Write first draft targeting **95-110%** of line budget.
   - If first draft lands 95-100%: **ship immediately. No further iteration required.**
   - If first draft lands 100-110%: trim using `suggest_synonyms.py` (HTML) or synonym swaps (Overleaf) until 95-100%.
2. Max 3 attempts per line.
3. If still outside 95-100% after 3 attempts: **rewrite the sentence from scratch.**

**NEVER start short and expand.** Starting long and shrinking is always faster and produces better vocabulary choices.

### Justify Threshold — NEVER Use Left-Align as a Fallback
**ALWAYS justify all published lines.** HTML: `text-align: justify`. LaTeX: full justification (default).  
**NEVER fall back to `text-align: left` because a line is short.** A line below 95% fill means the sentence needs more content — rewrite it, do not change the alignment.

### No Overflow Clipping — HTML Path
**NEVER set `height: 1.2em; overflow: hidden;`** on `li`, `.edge-to-edge-line`, or any bullet container, under any circumstances.  
**NEVER clip content to make it appear to fit.** Content MUST genuinely fit in one line through correct wording alone. If text wraps, the bullet is too long — shorten it.

### X-Y-Z Bullet Format — ALWAYS
**ALWAYS write bullets in X-Y-Z format:** "Accomplished [X—outcome] as measured by [Y—metric] by doing [Z—action]." All three elements in one natural sentence.  
**NEVER write a bullet with only one or two elements.** Read `references/xyz_format.md` for examples.

### Two-Tier Emphasis — NEVER Apply Color Before Gate 6
**HTML path:**
- **Tier 1 (Bold + Color):** `<b style="color: var(--brand-primary-color)">↑40%</b>` — metrics ONLY
- **Tier 2 (Bold only):** `<b>keyword</b>` — JD-aligned terms
- **NEVER exceed 2 colored segments per line. NEVER exceed 20% bold budget per line.**
- **NEVER add `color:` styling to any element during Gates 1–5.** Gate 5 draft MUST use plain `<b>` with no inline color. Color is applied ONLY at Gate 6.

**Overleaf path:**
- **Tier 1 (Bold + Color):** `\textbf{\textcolor{primary}{↑40\%}}` — metrics ONLY (Gate 6+)
- **Tier 2 (Bold only):** `\textbf{keyword}` — JD-aligned terms
- **NEVER exceed 2 colored segments per line. NEVER exceed 20% bold budget per line.**
- **NEVER use `\textcolor{}` before Gate 6.** Gate 5 MUST use plain `\textbf{}` only.

### Zero Verb Repetition — NEVER Repeat
**NEVER use the same action verb more than once across the entire resume.** Track all verbs from the first bullet written. If a verb is already used, always choose a different one.

---

## HTML Path: Section Patterns

### Experience (spacer-separated groups) — ALWAYS use this exact structure
```html
<ul>
  <li><span class="li-content">Bullet with <b style="color: var(--brand-primary-color)">↑40% metric</b> and <b>keyword</b>.</span></li>
  <li><span class="li-content">Second bullet same group.</span></li>
  <li class="bullet-group-spacer" aria-hidden="true"></li>
  <li><span class="li-content">First bullet second group.</span></li>
  <li><span class="li-content">Second bullet second group.</span></li>
</ul>
```

### Contact Bar — ALWAYS use this exact structure
```html
<span><b>Phone:</b> <a href="tel:+91-9876543210" style="color: inherit; text-decoration: none;">+91-9876543210</a></span>
<span><b>Email:</b> <a href="mailto:jane@example.com" style="color: inherit; text-decoration: none;">jane@example.com</a></span>
<span><b>LinkedIn:</b> <a href="https://linkedin.com/in/jane" style="color: inherit; text-decoration: none;">LinkedIn</a></span>
```

---

## Overleaf Path: FAANGPath Template

**Template:** https://www.overleaf.com/latex/templates/faangpath-simple-template/npsfpdqnxmbc  
**ALWAYS copy both `main.tex` and `resume.cls` to the user's Overleaf project. NEVER use only one file — the template requires both.**

### Page Setup — ALWAYS Change US Letter → A4
**NEVER leave the default `letterpaper`. ALWAYS change to `a4paper` first before writing any content.**
```latex
% WRONG — never use this:
\documentclass[letterpaper,10pt]{resume}

% ALWAYS use this:
\documentclass[a4paper,10pt]{resume}
```

### Section Command — ALWAYS use `\begin{rSection}`
```latex
\begin{rSection}{EXPERIENCE}
  % roles go here
\end{rSection}
```

### Role Header — ALWAYS use `\hfill` for right-aligned dates
```latex
{\bf Senior Associate Product Manager} \hfill {Jan 2023 -- Present} \\
{\it American Express} \hfill {\it Gurugram, India}
```

### Bullet Points — ALWAYS use `\itemsep -3pt`
**NEVER omit `\itemsep -3pt {}` — it controls line spacing and page fit.**
```latex
\begin{itemize}
    \itemsep -3pt {}
    \item {Bullet text here with \textbf{keyword} and metric.}
    \item {Second bullet.}
\end{itemize}
```

### Color — Gate 6 ONLY. NEVER add before content is locked.
**NEVER add `\usepackage{xcolor}` or any `\definecolor` or `\textcolor` command before Gate 6.**
```latex
% Add to preamble at Gate 6 — ONLY after content is 100% approved:
\usepackage{xcolor}
\definecolor{primary}{HTML}{0F766E}
\definecolor{secondary}{HTML}{0D9488}
\definecolor{tertiary}{HTML}{5EEAD4}
\definecolor{quaternary}{HTML}{042F2E}

% Metric emphasis in bullets (Gate 6+):
\textbf{\textcolor{primary}{↑40\%}}

% Section title color — adjust resume.cls \rSection definition to use \color{primary}
```

### LaTeX Width Measurement — ALWAYS Parse `.log` After Every Compile

**NEVER use `measure_width.py` on LaTeX text.** It is calibrated for Roboto 9.5pt and will give incorrect results for LaTeX fonts. **ALWAYS use the `.log` file instead** — the TeX typesetter reports both overflow and underfill for every line automatically.

**ALWAYS parse the `.log` for these two signals after every compile:**

```
Overfull \hbox (Xpt too wide)    → bullet too long, wraps to 2nd line → MUST trim
Underfull \hbox (badness XXXX)   → bullet too short, spacing sparse   → MUST expand
```

**Badness ↔ Fill quality — ALWAYS target the green zone:**

| Badness | Fill quality | Required action |
|---------|-------------|-----------------|
| 0 | Perfect (~100%) | Ship immediately |
| 1–200 | Excellent (~95-100%) — **TARGET ZONE** | Ship immediately |
| 201–1000 | Acceptable but noticeable gap | Expand if possible |
| 1001–9999 | Bad — line looks sparse | MUST rewrite |
| 10000 | Terrible — nearly empty line | MUST rewrite |

**Target: ALWAYS ship with no `Overfull \hbox` AND badness ≤ 200 on every bullet line.**

**ALWAYS follow this compile loop — NEVER ship without it:**
1. Write first draft at 95-110% natural length instinct.
2. Compile. ALWAYS read the `.log`.
   - No `\hbox` warning on the line → ships immediately.
   - `Overfull \hbox` → trim via synonym swaps or rephrase → recompile.
   - `Underfull \hbox` with badness > 200 → expand → recompile.
3. Max 3 compile iterations per bullet. If still outside target after 3: **rewrite from scratch.**

### LaTeX Page Fit Check (Vertical) — ALWAYS Run After Each Section
**ALWAYS check the `.log` for vertical overflow after writing every section. NEVER wait until the resume is complete.**
```
Overfull \vbox (Xpt too tall) has occurred ...
```
- Line absent or `X = 0` → page fits — continue
- `X > 0` → MUST trim the lowest-BRS bullet and recompile before proceeding

Convert pt to mm if needed: 1pt ≈ 0.353mm.

---

## Gate 6: Design / Brand Colors — ALWAYS Wait for Approval First

**NEVER apply any color to the resume before the user explicitly approves the palette at Gate 6.**

**HTML path — ALWAYS follow this sequence:**
1. Present color swatches with hex codes and labels: Primary, Secondary, Tertiary, Quaternary.
2. **STOP. Wait for explicit user approval. NEVER apply colors speculatively.**
3. After approval — set CSS variables in `<style>`:
   ```css
   :root {
     --brand-primary-color: #0F766E;
     --brand-secondary-color: #0D9488;
     --brand-tertiary-color: #5EEAD4;
     --brand-quaternary-color: #042F2E;
   }
   ```
4. Apply `<b style="color: var(--brand-primary-color)">` to all metric segments.
5. **ALWAYS run `validate_contrast.py`. NEVER deliver colored output that fails WCAG AA (4.5:1 contrast).**

**Overleaf path — ALWAYS follow this sequence:**
1. Same color approval step — present swatches, wait for confirmation.
2. Add `\usepackage{xcolor}` + `\definecolor` block to preamble.
3. Add `\textcolor{primary}{}` to all metric segments in bullets.
4. **ALWAYS recompile and verify no new `\hbox` or `\vbox` overflow from the color additions before presenting to user.**

---

## PDF Export (Optional — User-Driven)

PDF export is **optional**. **NEVER block delivery waiting for a PDF** — always deliver the source file first.

**HTML path (DIY — always offer this first):**
> Open the `.html` file in Chrome → ⌘P (Print) → Destination: Save as PDF → More settings → Background graphics: **ON** → Margins: **None** → Save.
> ⚠️ Background graphics MUST be ON or all colors and gradients will be lost.

**HTML path (Claude exports):** Use `assemble_html.py` to produce the final file. Offer Chrome export only if the user explicitly requests it.

**Overleaf path:** Overleaf compiles directly to PDF. No separate export step required — the PDF is always available in Overleaf after a successful compile.

---

## Color System (HTML Path)

9 CSS variables + 2 derived. Primary drives identity horizon, section titles, metric emphasis. Color expansion when <4 brand colors provided. **ALWAYS validate all colors for WCAG AA (4.5:1 contrast) before delivering.** Read `references/pipeline.md` Phase D for full details.

---

## Quality Grade System

6 checks: Keyword Coverage (30%), Width Fill (25%), Verb Dedup (15%), Page Fit (15%), Color Contrast (10%), ATS Compliance (5%). Grade A ≥ 90. **ALWAYS target Grade A. NEVER deliver below Grade B.**

---

## References (load on demand)

- `references/pipeline.md` — Complete 9-phase pipeline with all 7 gates
- `references/career_profiles.md` — 5 career levels with detection criteria and section orders
- `references/strategies.md` — 5 optimization strategies with triggers and examples
- `references/xyz_format.md` — X-Y-Z bullet format guide with examples per career level
