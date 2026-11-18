---
name: linkright-sync
description: >
  Build a pixel-perfect, single-page, ATS-safe Overleaf/LaTeX resume from a user's
  career profile and a job description or target archetype. Part of the Linkright system.
  Trigger on: "resume", "CV", "tailor my resume", "build a resume for [company]", "one-page resume",
  "archetype resume", "linkright-sync", or any request to create/optimize a job application document.
version: 2.4.0
---

# linkright-sync — Resume Generation Skill

Build a pixel-perfect, print-ready, ATS-safe LaTeX resume with company brand colors and
width-optimized bullets. Output is always a `.tex` file compiled in Overleaf (pdfLaTeX).

**Every line of the page must be utilized — no blank areas, no wasted real estate.**

---

## CRITICAL: Read Before Any Other Section

This skill has two paths. **Choose the right one before doing anything else.**

| Trigger | Path | What you do |
|---|---|---|
| JD given + matching archetype `.tex` already exists | **Quick Customization** | Open existing file → surgical swaps only → bank-first for every swap → compile |
| No existing file, or building a new archetype | **Full Build** | 7-gate pipeline, bank-first at every bullet slot |

**The most common case is Quick Customization.** Before starting any work, check whether a base
archetype file already exists in `resumes/resumes_latex_do_not_edit/` or `resumes/resumes_amex/`.
If it does, you are on the Quick Customization path — do not rebuild from scratch.

---

## Quick Customization Path — Surgical Swap Workflow

**Use this path whenever an existing archetype `.tex` file covers the target role.**

This is NOT a rebuild. You are making the minimum changes required to match the new JD.
The goal is to leave as many existing bullets unchanged as possible.

### Step 1 — Load the existing file

Open the closest matching archetype file:
```
resumes/resumes_latex_do_not_edit/resume_[archetype]-pm_base_[date].tex
```
or the company-specific file if one already exists:
```
resumes/resumes_amex/[company]/resume_[archetype]-pm_[company]_light_[date].tex
```

Extract every existing bullet and list them with their fact IDs:
```
EXISTING BULLETS:
  [A1]  Architected 5-step CDL pipeline; governs 521K+ records...
  [S3]  Built Walmart GenAI root-cause pipeline (6 sources, 100K+ contacts)...
  [L3]  Shipped 44/57 features (77%) in 11 months...
  ...
```

### Step 2 — Run JD signal analysis (lightweight)

Extract the primary and secondary signals from the JD (same as Gate 2 in the full pipeline,
but you only need signal names — not full analysis output).

```
JD SIGNALS:
  Primary (must cover):    [signal_1], [signal_2], [signal_3]
  Secondary (nice to have): [signal_4], [signal_5]
```

### Step 3 — Map existing bullets to JD signals

For each JD signal, check which existing bullets already cover it.
Mark each bullet: KEEP, SWAP, or ADD.

```
BULLET MAPPING:
  [A1] CDL pipeline    → covers: data_architecture, aml_risk   → KEEP
  [S3] Walmart GenAI   → covers: ai_workflows, insight_latency → KEEP
  [A4] 4 zero-spillover PIs → covers: execution_rigor         → KEEP
  [S5] Qatar Sharek    → covers: stakeholder_scale, revenue    → KEEP (low JD fit, but no better option)
  [L3] LinkRight       → covers: 0-to-1, solo_pm              → SWAP ← JD wants enterprise PM signals
  GAP: cloud_platform_exp → no existing bullet covers this    → ADD
```

**KEEP:** Bullet already covers a required JD signal — do not touch it, do not rewrite it.
**SWAP:** Bullet covers a signal the JD does not prioritize; replace with a bank variant that better matches.
**ADD:** JD requires a signal not covered by any existing bullet; source from bank or write fresh.

### Step 4 — Resolve every SWAP and ADD from the bank first

```
FOR EACH SWAP or ADD slot:

  1. Look up the slot's fact ID in bullet_bank.md
  2. Check the rating column for the target archetype

  IF a rated 4–5 variant exists for this archetype:
    → Use it verbatim. Width already validated. Do not touch it.

  IF a rated 3 variant exists:
    → Use it as a starting point. Adjust for JD signal. Run savebox. Validate width.

  IF no suitable variant exists:
    → Write fresh bullet. Draft at 100–110% width. Optimize. Mark [NEW] for bank append.
```

**NEVER write a fresh bullet for a slot where a 4–5 rated bank variant already exists.**
**NEVER rewrite a KEEP bullet just because you think you can improve it.**
Rewriting introduces new width problems and loses validated measurements.

### Step 5 — Apply company design layer (if company changed)

If the target company differs from the existing file's design layer, update the COMPANY DESIGN
LAYER block (two hex codes only — see Gate 6 below). Do not touch content.

### Step 6 — Compile, validate, deliver

- Compile in Overleaf → verify 1 page
- Run `ats_scanner.py` and `ai_smell_checker.py`
- Verify all KEEP bullets are byte-for-byte unchanged from the source file
- Show summary:

```
QUICK CUSTOMIZATION SUMMARY — [Company] — [Date]
  Base file used:       resume_[archetype]_base_[date].tex
  Bullets kept:         X  (unchanged from base)
  Bullets swapped:      Y  (from bank: Z verbatim, W adjusted)
  Bullets added fresh:  V  (marked [NEW] for bank append)
  Design layer updated: YES / NO
```

---

**ALWAYS check the bullet bank before generating any bullet — in both paths.** A bank bullet
rated 4–5 for the target archetype is pre-measured, pre-validated, and ready to drop in verbatim.

---

## Exact LaTeX Preamble Template (MANDATORY — Never Deviate)

**ALWAYS start from this exact preamble. Copy verbatim. Never add or remove packages without
explicit user approval. Package order matters for font rendering.**

### Base preamble (Gates 1–5 — content phase, no design yet)

```latex
\documentclass[a4paper,10pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage[T1]{fontenc}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1.0in}
\addtolength{\topmargin}{-.6in}
\addtolength{\textheight}{1.2in}

\urlstyle{same}
\raggedbottom
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large\bfseries
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\pdfgentounicode=1

\newcommand{\resumeItem}[1]{
  \item\small{#1\vspace{-2pt}}
}
\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
  \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
    \textbf{#1} & #2 \\
    \textit{\small#3} & \textit{\small #4} \\
  \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeSubSubheading}[2]{
  \item
  \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
    \textit{\small#1} & \textit{\small #2} \\
  \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeProjectHeading}[2]{
  \item
  \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
    \small#1 & #2 \\
  \end{tabular*}\vspace{-7pt}
}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}\parfillskip=0pt}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}
```

### Gate 6 additions (design phase — added only at Gate 6, never before)

At Gate 6, three things change in the preamble:

**1.** `\usepackage[usenames,dvipsnames]{color}` → `\usepackage[usenames,dvipsnames]{xcolor}`

**2.** After `\usepackage[T1]{fontenc}`, insert:
```latex
\usepackage{eso-pic}
\usepackage{tikz}
```

**3.** After `\input{glyphtounicode}`, insert the COMPANY DESIGN LAYER + border code:
```latex
% ═══════════════════════════════════════════════════════════════════
% COMPANY DESIGN LAYER — [Company]
% RULE: primary = border (dominant brand color)
%        section = dividers (secondary brand color, visible on white)
%        name    = #1A1A1A always — do not change
% ┌── SWAP COMPANY: Change only these two hex codes ──────────────────┐
\definecolor{cprimary}{HTML}{XXXXXX}   % Border
\definecolor{csection}{HTML}{XXXXXX}   % Section rules
% └─────────────────────────────────────────────────────────────────┘
% ═══════════════════════════════════════════════════════════════════

% ── Inset border: 1.5pt rule, 8pt gap from page edges on all four sides ──
\AddToShipoutPictureBG{%
  \begin{tikzpicture}[remember picture, overlay]
    \draw[color=cprimary, line width=1.5pt]
      ([xshift=8pt,yshift=-8pt]current page.north west)
      rectangle
      ([xshift=-8pt,yshift=8pt]current page.south east);
  \end{tikzpicture}%
}
```

**4.** In `\titleformat{\section}`: `[\color{black}\titlerule` → `[\color{csection}\titlerule`

**5.** In the name heading: `\textbf{\Huge \scshape [Name]}` → `\textcolor[HTML]{1A1A1A}{\textbf{\Huge \scshape [Name]}}`

**⚠️ Critical package notes:**
- `\usepackage[T1]{fontenc}` — MUST be present in every file. Controls glyph rendering. Never omit.
- `\resumeItemListStart` → `\begin{itemize}\parfillskip=0pt` — `\parfillskip=0pt` MUST be at list scope here, NOT inside `\resumeItem`'s braces (TeX group scoping cancels it silently).
- **NEVER add `\usepackage{lmodern}`** — changes character widths, breaks all bullet width measurements.
- **NEVER add `\usepackage{xcolor}` before Gate 6.** It is a design package, not a content package.
- **NEVER add `\usepackage{eso-pic}` or `\usepackage{tikz}` before Gate 6.**

**Line width budget:** 492.39783pt (from this exact geometry). Any bullet measured against a different geometry is invalid.

---

## Exact Resume Structure Template (MANDATORY — Section Order and Format)

**Always follow this exact structure. Section names are exact (case-sensitive in LaTeX `\section{}`).**

```latex
\begin{document}

%--- HEADER ---
\begin{center}
  \textcolor[HTML]{1A1A1A}{\textbf{\Huge \scshape [Full Name]}} \\ \vspace{1pt}
  \small [phone] $|$
  \href{mailto:[email]}{\underline{[email]}} $|$
  \href{[linkedin]}{\underline{LinkedIn}} $|$
  \href{[github]}{\underline{GitHub}} $|$
  \href{[portfolio_or_other]}{\underline{[link_label]}}
\end{center}

%--- SUMMARY ---
\section{Summary}
[3-4 lines of plain text — NO bullets, NO \resumeItem, NO bold except metrics]
[Line 1: Positioning + years + core domain]
[Line 2: Strongest specific metric or achievement]
[Line 3: Technical/tooling depth signal]
[Line 4 (optional): IIT Delhi. or similar credential close]

%--- EXPERIENCE ---
\section{Experience}
\resumeSubHeadingListStart
  \resumeSubheading
    {[Company Name]}{[Start] -- [End or Present]}
    {[Job Title]}{[City, Country]}
  \resumeItemListStart
    \resumeItem{[bullet 1]}
    \resumeItem{[bullet 2]}
    \resumeItem{[bullet 3]}
    \resumeItem{[bullet 4]}
  \resumeItemListEnd

  % Promotion at same company — use SubSubheading
  \resumeSubSubheading
    {[Previous Title]}{[Start] -- [End]}
  \resumeItemListStart
    \resumeItem{[bullet 1]}
    \resumeItem{[bullet 2]}
  \resumeItemListEnd
\resumeSubHeadingListEnd

%--- VENTURES & ADVISORY (if applicable) ---
\section{Ventures \& Advisory}
\resumeSubHeadingListStart
  \resumeProjectHeading
    {\textbf{[Venture Name]} $|$ \emph{[Role]}}{[Year or Date Range]}
  \resumeItemListStart
    \resumeItem{[bullet]}
  \resumeItemListEnd
\resumeSubHeadingListEnd

%--- PROJECTS (if applicable) ---
\section{Projects}
\resumeSubHeadingListStart
  \resumeProjectHeading
    {\textbf{[Project Name]} $|$ \emph{[Role]}}{[Date Range]}
  \resumeItemListStart
    \resumeItem{[bullet]}
  \resumeItemListEnd
\resumeSubHeadingListEnd

%--- SKILLS ---
\section{Skills}
\begin{itemize}[leftmargin=0.15in, label={}]
  \small{\item{
    \textbf{[Domain 1]:}{ [keyword, keyword, keyword, ...]} \\
    \textbf{[Domain 2]:}{ [keyword, keyword, keyword, ...]} \\
    \textbf{[Domain 3]:}{ [keyword, keyword, keyword, ...]} \\
    \textbf{Tools:}{ [tool, tool, tool, ...]}
  }}
\end{itemize}

%--- EDUCATION ---
\section{Education}
\resumeSubHeadingListStart
  \resumeSubheading
    {[Institution]}{[Start] -- [End]}
    {[Degree, Field]}{[Score or GPA]}
  \resumeItemListStart
    \resumeItem{[scholastic achievement 1]}
    \resumeItem{[scholastic achievement 2 / certifications]}
  \resumeItemListEnd
\resumeSubHeadingListEnd

%--- REFERENCES ---
\vspace{-6pt}
\section{References}
\begin{itemize}[leftmargin=0.15in, label={}]
  \small{\item{
    \href{[linkedin_url]}{\textbf{\underline{[Name]}}} $|$ [Title, Company] $|$ ([phone]) \\
    \href{[linkedin_url]}{\textbf{\underline{[Name]}}} $|$ [Title, Company] $|$ ([phone]) \\
    \href{[linkedin_url]}{\textbf{\underline{[Name]}}} $|$ [Title, Company] $|$ ([phone])
  }}
\end{itemize}

\end{document}
```

**Structure rules (NEVER violate):**
- NEVER change section name casing — `\section{Experience}` ≠ `\section{experience}`
- NEVER add a 5th skills bucket (page overflow risk)
- NEVER put bullets in the Summary section — it is prose only
- NEVER use `\begin{tabular}` inside any `\resumeItem`
- ALWAYS include References section — 3 references from `layer_1_the_real.md`

---

## Bullet Writing Rules — NON-NEGOTIABLE

**These rules apply to EVERY bullet in EVERY resume. No exceptions.**

### Rule 1: XYZ Format — Always
Every bullet must follow one of these structures:
- **X by Y, resulting in Z** → "Cut analysis cycle **4 days → 1 day** by unifying 3 Adobe schemas via SQL, enabling same-day insight"
- **Verb + metric/outcome** → "Grew Social Listening adoption **~35% → ~85%** for SME clients; removed onboarding friction, cut TTV ~75%"
- **Verb + [bold metric] + context + [bold outcome]** → "Built LLM Grooming bot; ranked **#21 of 400+ teams (Top 6%)** at AmEx Hackathon; productionized as **QE Assist**"

**NEVER write a bullet without at least one number, percentage, or concrete outcome.**
**NEVER write a bullet that describes what you did with no result.**

### Rule 2: Action Verb Uniqueness — Strictly Enforced
- NEVER start two bullets with the same action verb in the same resume
- Track every bullet-start verb as you write. Maintain a working list.
- After all bullets are written, audit the list. Any duplicate → rewrite the weaker bullet.
- Strong starting verbs (use each at most once): Built, Designed, Led, Drove, Shipped, Launched, Architected, Owned, Grew, Reduced, Cut, Delivered, Secured, Deployed, Ranked, Stepped, Earned, Unified, Mapped, Validated, Diagnosed, Covered
- **NEVER start with**: "Worked on", "Helped with", "Assisted in", "Responsible for", "Managed various"

### Rule 3: Bold Usage
- Bold only the most important metric or outcome — ONE `\textbf{}` per bullet, max TWO
- NEVER bold an entire phrase — only the number/metric/outcome itself

### Rule 4: No AI-Smell Language
**NEVER use**: "leveraged", "utilized", "spearheaded", "pioneered", "strategized", "orchestrated", "synergized", "proactively", "successfully", "impactful", "transformative", "cutting-edge", "state-of-the-art", "best-in-class", "passionate about"

### Rule 5: Tilde for Approximations
- ALWAYS use `$\sim$` for approximations in LaTeX (e.g., `$\sim$35\%`)
- NEVER use `~` directly — it renders as non-breaking space in LaTeX, not a tilde

### Rule 6: Special Character Escaping
| Character | LaTeX code |
|---|---|
| → (arrow) | `$\rightarrow$` |
| ~35% | `$\sim$35\%` |
| **bold** | `\textbf{text}` |
| $1.2M | `\$1.2M` |
| #1 | `\#1` |
| & | `\&` |
| % | `\%` |

---

## Architecture

Claude handles all language tasks. **Always delegate precision computation to scripts. Never eyeball widths or page fit.**

**Scripts** — run via `bash python ${CLAUDE_PLUGIN_ROOT}/skills/linkright-sync/scripts/<name>.py '<json>'`

| Script | Purpose | When |
|---|---|---|
| `log_parser.py` | Parse LaTeX .log → error summary (NOT for bullet width) | Error diagnosis only |
| `ai_smell_checker.py` | Flag AI-generated language patterns | Gate 4 before showing user |
| `ats_scanner.py` | Check .tex for ATS-hostile formatting | Gate 7 |
| `constraint_checker.py` | Validate content against user_setup.md | Gate 5 |

**NEVER use `measure_width.py` on LaTeX text** (wrong font metrics — gives false results).
**NEVER rely on `.log` hbox warnings** to detect short/long bullets — `\raggedright` suppresses ALL underfull hbox warnings.
Use the `\savebox` harness documented in `ref_04_pixel_perfect_bullets.md`.

---

## 7-Gate Pipeline — MANDATORY

**Stop at every gate. Wait for explicit user confirmation. Never auto-advance. Never skip.**

| Gate | Phase | What You Do | User Confirms |
|---|---|---|---|
| **1** | Input Collection | Load profile + JD/archetype + bullet bank | Inputs correct? |
| **2** | JD / Archetype Analysis | Extract signals, archetype, recruiter language | Analysis accurate? |
| **3** | Signal Coverage Map | Map JD requirements vs user profile | Gaps addressed? |
| **4** | Content Generation (B&W) | Bank-first bullet selection → fresh bullets where needed → width-optimize each | Section by section |
| **5** | Content Review + Constraints | Full resume preview + constraint validation | All content approved |
| **6** | Design / Brand Colors | Apply company design layer, compile, verify 1 page | Colors + compile approved |
| **7** | Final Delivery | ATS scan, AI-smell scan, file output + bank update | Ship it |

### B&W Content Rule (Gates 1–5)

> **NEVER introduce brand colors during Gates 1–5. Write everything in plain black.**

Lock every word, every bullet, every section order, confirm page fit — BEFORE touching design.
Colors are introduced exactly once, at Gate 6.

---

## Gate 1 — Input Collection + Path Decision

Collect:
1. **JD source** — one of:
   - Paste URL → fetch full JD text
   - Paste JD text directly
   - "No JD — target archetype instead" → ask which archetype
2. **Target company** (if known) — for brand color lookup at Gate 6
3. **Bullet bank** — load `bullet_bank.md` silently

Then immediately check for an existing file:

```
PATH DETECTION:
  Check resumes/resumes_latex_do_not_edit/ for a matching archetype base file.
  Check resumes/resumes_amex/[company]/ for a company-specific file.

  IF a matching file exists:
    → PATH = Quick Customization
    → Load that file now. Extract all bullets. List them with fact IDs.
    → Skip to the Quick Customization Path section above.
    → Do NOT run the full 7-gate pipeline.

  IF no matching file exists:
    → PATH = Full Build
    → Continue to Gate 2 below.
```

Show parsed summary:
```
INPUTS PARSED:
  JD/Target:    [company + role title, or archetype name]
  Path chosen:  Quick Customization (base: [filename]) / Full Build
  Bank bullets ready (rated 4–5 for target archetype): [list fact IDs]
```

Ask: "Anything to correct before we continue?"

---

## Gate 2 — JD / Archetype Analysis

Load `references/ref_01_jd_analysis.md` for full analysis protocol.

**If JD provided — run full JD analysis:**

```
ARCHETYPE DETECTED: [e.g., AI Enterprise PM]

SIGNAL REQUIREMENTS:
  Primary (must cover):    [signal_1], [signal_2], [signal_3]
  Secondary (should cover): [signal_4], [signal_5]
  Mentioned (nice to have): [signal_6]
  Negative (avoid):        [signal_7]

RECRUITER LANGUAGE (mirror these in bullets):
  "[phrase from JD]", "[phrase]", "[phrase]"

RED FLAGS:
  [Anything unusual: niche stack required, comp not listed, etc.]
```

**If archetype only (no JD) — run archetype profile:**

```
TARGET ARCHETYPE: [AI PM / Growth PM / Data PM / Platform PM / FinTech PM / Startup PM / Consumer PM]

CANONICAL SIGNAL REQUIREMENTS (from bullet_bank.md cheat sheet):
  Primary:   [signal_1], [signal_2], [signal_3]
  Secondary: [signal_4], [signal_5]

POSITIONING ANGLE:
  [1-sentence framing — what the resume narrative should signal]
```

Ask: "Does this analysis look right? Anything to override?"

---

## Gate 3 — Signal Coverage Map

Load `references/ref_02_signal_mapping.md` for signal strength definitions.

```
SIGNAL COVERAGE MAP

Primary Signals (must cover):
  systems_thinking        → Profile: STRONG  (3 facts confirmed) ✓
  ai_workflow_design      → Profile: MEDIUM  (1 fact) △
  stakeholder_leadership  → Profile: STRONG  (4 facts confirmed) ✓

Secondary Signals (should cover):
  data_fluency            → Profile: WEAK    (0 confirmed facts)  ✗ ← gap
  execution_rigor         → Profile: STRONG  (2 facts confirmed) ✓

GAP SIGNALS: data_fluency
```

For each gap signal, ask the user before proceeding. Both "yes I have that" and "no I don't" are valid answers. Never overclaim an absent signal.

Confirm: "Coverage map looks correct? Any signal strengths to override?"

---

## Gate 4 — Content Generation (B&W Mode)

Load `references/ref_04_pixel_perfect_bullets.md`.

Generate all resume content in plain black text. **Zero color anywhere.**

### Section Order (default — adjust at Gate 1 if user overrides)

| Career Level | Recommended Order |
|---|---|
| 0–3 yrs | Header → Education → Experience → Skills → Projects |
| 3–8 yrs | Header → Experience → Ventures & Advisory → Projects → Skills → Education → References |
| 8+ yrs | Header → Experience → Skills → (Education optional) |

### MANDATORY: Bank-First Decision Tree — Apply to EVERY Bullet Slot

```
FOR EACH bullet slot in the resume:

  1. Look up the underlying fact in bullet_bank.md
     → Find the matching Fact block (A1–A8, S1–S9, P1–P3, L1–L5, K1, M1, V1–V3, E1–E3)

  2. Check the rating table for the target archetype column (AI/GR/DA/PL/EN/FT/ST/CA)

  IF rating ≥ 4 AND a variant exists for this archetype:
    → COPY the bank variant verbatim into the resume
    → Mark it [FROM BANK] in working draft
    → SKIP the width check (already measured and validated)
    → NEVER rewrite it — you will likely break the width

  IF rating = 3 AND a variant exists:
    → Use bank variant as a STARTING POINT only
    → Write a fresh bullet targeting the archetype's primary signals
    → Apply the full optimization loop to the new bullet

  IF rating ≤ 2 OR no variant exists:
    → Write fresh bullet (see "Fresh Bullet Generation" below)
    → Mark it [NEW] for Gate 7 bank append
```

### Fresh Bullet Generation — Only When Bank Has No 4+ Variant

**Step 1 — Draft at 100–110% width (intentionally long)**

Write a first draft that is slightly too long — approximately 100–110% of the line budget.
Pack in all the signal first, then trim. Starting long produces better bullets than starting short.

> Target: 492pt–541pt for LaTeX first draft. Too long by 0–50pt is easy to trim.

**Forbidden padding words:**
- "successfully", "proactively", "in a timely manner", "in a fast-paced environment"
- "various", "multiple stakeholders", "cross-functional teams" (without specifics)
- "was responsible for" — always replace with the actual action verb

**Step 2 — Measure the draft**

LaTeX: `/tmp/test_bullet.sh '[bullet text]'`
→ Outputs: `OK 489pt` | `SHORT 432pt` | `OVERFLOW 557pt`

**Step 3 — Shrink to 95–100% range (OVERFLOW) or expand (SHORT)**

```
OVERFLOW (>492pt):
  1. Remove filler: "in order to"→"to", "on a monthly basis"→"monthly"
  2. Swap for shorter synonym: "redesigning"→"redesign", "utilizing"→"using"
  3. Restructure: "by redesigning X and automating Y" → "via X redesign and Y automation"
  4. Remove weakest qualifying detail
  5. Structural rewrite (600pt+) — bullet is doing too much; pick the strongest signal

SHORT (<418pt):
  1. Add a specific result: "zero sprint spillovers", "Top 6%", "120% bonus"
  2. Add team/org context: "across two time zones", "40 government ministries"
  3. Add the method: "via SQL pipelines", "using unsupervised ML clustering"
  4. Spell out an abbreviation once if it gains ~10pt and adds clarity

OK at 85–95% (418–467pt): Keep iterating — try to reach 95%+.
OK at 95–97% (467–481pt): One more expansion attempt. Lock if still in range.
OK at 98–100% (482–492pt): LOCK IT immediately. Never iterate past 98%.
```

**Step 4 — Max 10 iterations. If still below 95% → rewrite from scratch with a different sentence structure.**

**Step 5 — LOCK the bullet. Never touch it again.**

> **Lock one bullet before touching the next. Never edit two simultaneously.**

### Action Verb Tracking

Maintain a running list of all bullet-start verbs as you write:
```
VERB TRACKER (update after each bullet):
  Built, Drove, Grew, Ranked, Stepped, Unified, Mapped, Launched, Validated, ...
```
**Before delivering Gate 4 content: audit the tracker. Any duplicate start verb → rewrite the weaker bullet.**

### Width Reference

```
Budget:   492.39783pt (FAANGPath A4 geometry — THIS template only)
Target:   98–100%  = 482–492pt  ← LOCK immediately
OK:       95–97%   = 467–481pt  ← try one more expansion, then lock
Acceptable: 85–94% = 418–466pt  ← try to expand, ship if you can't reach 95
Floor:    85%      = 418pt      ← absolute minimum. Below this = must rewrite
OVERFLOW: >492pt               ← must trim
```

Show content section by section and get confirmation before moving to the next section.
**Never show the full resume in one wall of text.**

---

## Gate 5 — Content Review + Constraint Validation

Show the complete resume content (B&W, all sections assembled).

**Run constraint validation:**
```bash
python constraint_checker.py --resume "[resume_text]" --setup "path/to/user_setup.md"
```

If `user_setup.md` is not found, manually check:
- No companies from `do_not_mention.companies` list
- No projects from `do_not_mention.projects` list
- No claimed work tagged as NOT-OWNED in user's profile
- No metrics beyond what user can defend in an interview

**For Satvik Jain specifically — these are hard stops:**
- NEVER include "Chief of Staff" as a title for GoGoGo — announced but never formalized
- NEVER include the GoGoGo financial difficulty story in any professional context
- NEVER mention Indore/remote in applications — raise only after offer
- NEVER include Navii growth (2K→20K) as a claim Satvik owns solo — always "during beta" with team credit

**On any violation:** Show exact text + reason. Block delivery until resolved.

Ask: "Any edits before we apply design? This is the last chance to change content."

Only approved content proceeds to Gate 6.

---

## Gate 6 — Design / Brand Colors

**Apply visual design ONLY after content is fully approved at Gate 5.**

### Step 1 — Source the two brand color tokens

Check if a pre-made company file already exists in `resumes/resumes_amex/[company]/`.
If yes — open that file, copy its COMPANY DESIGN LAYER block. Done.

If no — source colors from:
- Company brand guide / press kit
- Inspect their website CSS: look for `--primary`, `--brand`, `--accent` CSS variables
- Brandfetch.com → search company → Colors tab

### Step 2 — Apply the universal two-token color rule

```
cprimary = most dominant / recognizable brand color → border frame
csection = secondary brand color (must be clearly visible on white background) → section dividers
cname    = #1A1A1A always → name heading (hardcoded — do not change for any company)
background = white always → never add \pagecolor
```

**Contrast rule for csection:** The secondary color must be clearly legible on a white background.
If the candidate secondary is too light (yellows, pale tones, light grays), fall back to `cprimary`
for section rules as well. Monochromatic brands (OpenAI, Meta, Apple) use the same color for both — that is correct, not an error.

**Examples:**
| Company | cprimary (border) | csection (rules) | Why |
|---------|------------------|-----------------|-----|
| Google | `4285F4` | `EA4335` | Blue dominant; Red secondary legible on white |
| Amazon | `FF9900` | `232F3E` | Orange dominant; Navy secondary for contrast |
| Stripe | `635BFF` | `0A2540` | Purple dominant; Navy secondary for contrast |
| OpenAI | `10A37F` | `10A37F` | Monochromatic — same color for both |
| YouTube | `FF0000` | `000000` | Red dominant; Black secondary |

### Step 3 — Apply the six preamble changes

1. `\usepackage[usenames,dvipsnames]{color}` → `\usepackage[usenames,dvipsnames]{xcolor}`
2. After `\usepackage[T1]{fontenc}`: add `\usepackage{eso-pic}` and `\usepackage{tikz}`
3. After `\input{glyphtounicode}`: insert COMPANY DESIGN LAYER block + border code (see preamble template above)
4. In `\titleformat{\section}`: `[\color{black}\titlerule` → `[\color{csection}\titlerule`
5. Name heading: wrap in `\textcolor[HTML]{1A1A1A}{...}` (or verify already applied)
6. Compile → verify 1 page, check `.log` for Overfull \hbox errors

Ask: "Approve colors and compile result?"

---

## Gate 7 — Final Delivery

Run full validation checklist before shipping:

```
QUALITY GATE CHECKLIST:
[ ] ATS scan:       run ats_scanner.py → zero table-layout or column violations
[ ] AI-smell scan:  run ai_smell_checker.py → zero flagged phrases
[ ] Page fit:       1 page confirmed (PDF page count = 1)
[ ] Width:          all bullets 95–100% (savebox-verified) or acceptable 85–94%
[ ] Constraints:    zero violations from constraint_checker.py
[ ] Signals:        all primary signals covered by at least one bullet
[ ] Orphans:        no bullet's last line ends with fewer than 3 words
[ ] Verb audit:     no start verb repeated across all bullets
[ ] Template:       preamble matches skeleton (T1 fontenc, parfillskip at list scope)
[ ] Design layer:   cprimary + csection defined, cname = 1A1A1A, background white
```

Show report:
```
QUALITY REPORT — [Company/Archetype] — [Date]
  ATS:         PASS
  AI-smell:    PASS (0 flags)
  Page fit:    PASS (1 page)
  Width:       PASS (all bullets 95–100%)
  Constraints: PASS (0 violations)
  Verb audit:  PASS (no duplicates)
  Design:      cprimary=XXXXXX / csection=XXXXXX / cname=1A1A1A ✓
  Signal coverage: [signal_1] ✓ / [signal_2] ✓ / [signal_3] △
```

Output filename conventions:
- Archetype base: `resume_[archetype-slug]_base_[date].tex`
- Company customization: `resume_[archetype-slug]_[company-slug]_light_[date].tex`

**Bullet Bank Update (mandatory if any [NEW] bullets exist):**

1. Find the matching Fact block in `bullet_bank.md` or create a new one.
2. Add the new variant line under the appropriate Fact block.
3. Rate it across all 8 archetype columns (AI / GR / DA / PL / EN / FT / ST / CA).
4. Measure its width with the `\savebox` harness and record the pt value.
5. Update "Last updated" at the top of `bullet_bank.md`.

Show summary:
```
BANK UPDATE — [Company] — [Date]
  Bullets reused from bank:  X
  New bullets appended:      Y
  Bank now contains:         Z total fact blocks
```

Ask: "Approve and download?"

---

## Hard Rules — Complete List (All Non-Negotiable)

### ALWAYS Do This

- **ALWAYS** start from the exact preamble template above — never improvise the structure
- **ALWAYS** load bullet_bank.md at Gate 1 and identify pre-validated 4–5 rated bullets before writing a single word
- **ALWAYS** generate content in B&W (Gates 1–5) — zero colors until Gate 6
- **ALWAYS** use the `\savebox` harness for every new LaTeX bullet — never eyeball
- **ALWAYS** run `constraint_checker.py` at Gate 5 before showing final content
- **ALWAYS** run `ats_scanner.py` and `ai_smell_checker.py` at Gate 7
- **ALWAYS** stop at every gate — never auto-advance, never combine two gates
- **ALWAYS** draft new bullets at 100–110% width first, then shrink to 95–100%
- **ALWAYS** lock one bullet before touching the next
- **ALWAYS** use `\parfillskip=0pt` in `\resumeItemListStart`, not inside `\resumeItem`'s braces
- **ALWAYS** use `\usepackage[T1]{fontenc}` in every new .tex file
- **ALWAYS** use `$\sim$` for tildes/approximations in LaTeX, never the bare `~` character
- **ALWAYS** update bullet_bank.md with any [NEW] bullets after Gate 7
- **ALWAYS** use XYZ bullet format: outcome/metric is visible in every bullet
- **ALWAYS** audit action verb uniqueness before shipping
- **ALWAYS** use `\textcolor[HTML]{1A1A1A}` for the name heading in every file
- **ALWAYS** keep background white — never add `\pagecolor` to any resume
- **ALWAYS** source brand colors from the existing `resumes/resumes_amex/[company]/` file first before looking elsewhere
- **ALWAYS** check for an existing archetype `.tex` file at Gate 1 — if one exists, use Quick Customization path, not a full rebuild
- **ALWAYS** map existing bullets to JD signals before deciding what to swap — most bullets will be KEEP

### NEVER Do This

- **NEVER** auto-advance gates without explicit user confirmation
- **NEVER** write a bullet without running it through the `\savebox` width harness
- **NEVER** use `measure_width.py` on LaTeX text — wrong font metrics, false results
- **NEVER** rely on `.log` hbox warnings for bullet width — `\raggedright` suppresses all of them
- **NEVER** add `\usepackage{xcolor}` before Gate 6
- **NEVER** add `\usepackage{eso-pic}` or `\usepackage{tikz}` before Gate 6
- **NEVER** add `\usepackage{lmodern}` — changes character widths, breaks all measured bullet fills
- **NEVER** put `\parfillskip=0pt` inside `\resumeItem`'s braces — TeX group scope cancels it silently
- **NEVER** deliver with any Overfull \hbox in the `.log` file
- **NEVER** write a bullet without a specific number, percentage, or outcome
- **NEVER** start two bullets with the same action verb in the same resume
- **NEVER** use AI-smell words: "leveraged", "utilized", "spearheaded", "pioneered", "strategized", "synergized", "proactively", "successfully", "impactful", "transformative"
- **NEVER** claim metrics the user cannot defend in an interview
- **NEVER** rewrite a bank bullet rated 4–5 for the target archetype — use it verbatim
- **NEVER** write a bullet with "worked on", "helped with", "assisted in", "was responsible for"
- **NEVER** show the full resume as a wall of text — section by section, gate by gate
- **NEVER** pad short bullets with filler ("in a fast-paced environment", "across various teams")
- **NEVER** modify the preamble template without explicit user approval and a full recompile/remeasure
- **NEVER** change section names from the exact template (capitalization matters)
- **NEVER** add a 5th skills bucket (page overflow risk)
- **NEVER** add `\pagecolor` to any resume — background is always white
- **NEVER** change `cname` or the name text color away from `#1A1A1A` for any brand
- **NEVER** use a csection color that is not clearly legible on a white background
- **NEVER** produce HTML resume output — Overleaf/LaTeX is the only format
- **NEVER** rebuild a resume from scratch when a matching archetype file already exists — use Quick Customization
- **NEVER** rewrite a KEEP bullet — if it already covers the JD signal, leave it byte-for-byte unchanged
- **NEVER** write a fresh bullet for a swap/add slot when a 4–5 rated bank variant exists for that archetype

---

## Cover Letter (Optional — After Gate 7)

Structure:
1. **Opening** — why this company, why this role; must reference something real (a product, a decision, a stated challenge)
2. **Evidence** — 2–3 sentences bridging strongest signals to stated requirements
3. **Close** — confident ask, specific

Hard rules:
- **NEVER** open with: "I am excited to apply", "I am writing to express", "I believe I would be a great fit"
- **ALWAYS** reference something specific and real about the company
- **Maximum 280 words**
- Run `constraint_checker.py` on cover letter before delivery

---

## References (Load Gate-by-Gate — Do Not Load All Upfront)

| Gate | Load |
|---|---|
| Gate 2 | `references/ref_01_jd_analysis.md` |
| Gate 3 | `references/ref_02_signal_mapping.md` |
| Gate 4 | `references/ref_04_pixel_perfect_bullets.md` — full \savebox harness, worked examples, escape reference |
| Gate 7 | `references/ref_06_ats_rules.md` |
| Any gate | `bullet_bank.md` — loaded at Gate 1, kept in context throughout |
| Any gate | `layer_3_the_write.md` — summaries and archetype-specific language |
| Gate 6 | `resumes/resumes_amex/[company]/` — pre-made company design files (check here first) |

**Do NOT load all references at Gate 1.** Load each at its gate only.
