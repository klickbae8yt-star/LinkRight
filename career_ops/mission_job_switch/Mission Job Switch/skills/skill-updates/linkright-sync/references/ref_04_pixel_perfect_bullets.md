# ref_04 — Pixel-Perfect Bullet Width Optimization (LaTeX / Overleaf)

Loaded at Gate 5 (LaTeX path, width-check loop).
This file documents the **exact method used to achieve 95–100% line-fill on every bullet** in
the FAANGPath A4 LaTeX template — the same loop used to optimize all 4 Satvik archetype resumes.

---

## Why This Is Not Optional

A resume bullet that wraps to two lines is a red flag to a trained eye. It reads as sloppy. It wastes
vertical space, costing you bullets elsewhere. And in ATS parsing, wrapped bullets sometimes get
split mid-sentence.

A bullet at 95–100% of the available line width signals precision — the candidate is deliberate,
every word earns its place.

The naive approach (eyeballing in a PDF, or trusting LaTeX's zero-warning compile) **does not work**:
- `\raggedright` never generates underfull hbox warnings. A 10-line bullet produces zero warnings.
- PDF preview zoom changes perceived line breaks.
- The only ground truth is the **compiled font metric** — measuring actual rendered text width.

---

## The FAANGPath A4 Line Budget

Template geometry:
```
\usepackage[empty]{fullpage}      % 1in margins all sides
\addtolength{\textwidth}{1.0in}   % +1in width → 0.5in margins each side
\addtolength{\oddsidemargin}{-0.5in}
```

Inside `\resumeItemListStart` (a standard `\begin{itemize}`), the available linewidth is:

**492.39783pt ≈ 173.65mm**

Target fill range: **85–100%**, aim for **95–100%**
- Floor: 418.53pt (85%)
- Target floor: 467.78pt (95%)
- Hard ceiling: 492.39783pt (100%)

---

## The `\savebox` Width-Check Harness

This is the test script. Save it as `/tmp/test_bullet.sh` and run it on every bullet.

```bash
#!/bin/bash
BULLET="$1"
cat > /tmp/_b.tex << TEXEOF
\documentclass[a4paper,10pt]{article}
\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{enumitem}
\usepackage[T1]{fontenc}
\usepackage[hidelinks]{hyperref}

\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1.0in}
\addtolength{\topmargin}{-.6in}
\addtolength{\textheight}{1.2in}

\raggedright
\setlength{\tabcolsep}{0in}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}
\newsavebox{\bb}

\begin{document}
\resumeItemListStart
\item\small{\savebox{\bb}{$BULLET}%
  \ifdim\wd\bb>492.39783pt \typeout{OVERFLOW \the\wd\bb}%
  \else\ifdim\wd\bb<418.53pt \typeout{SHORT \the\wd\bb}%
  \else\typeout{OK \the\wd\bb}\fi\fi $BULLET\vspace{-2pt}}
\resumeItemListEnd
\end{document}
TEXEOF
cd /tmp && pdflatex -interaction=nonstopmode _b.tex 2>/dev/null | grep -E "^(OK|SHORT|OVERFLOW)"
```

Usage:
```bash
chmod +x /tmp/test_bullet.sh
/tmp/test_bullet.sh 'Cut AML risk-config speed-to-market \textbf{10 days $\rightarrow$ 3 days (70\%)} via rule UI redesign and API-automated approvals'
# → OK 490.50594pt
```

The output is one of:
- `OK 490.50pt` — width is 95–100%, bullet is done
- `SHORT 364.73pt` — bullet is too short, needs expansion
- `OVERFLOW 557.05pt` — bullet wraps to 2 lines, must be cut

---

## The Batch Pre-Scan Script

Run this first to get a full OVERFLOW/SHORT/OK report for all bullets in a resume before fixing anything.

```bash
#!/bin/bash
# check_all.sh — pass all bullets as an array
bullets=(
  'First bullet text with \textbf{bold} here'
  'Second bullet text here'
  # ... add all bullets
)

for i in "${!bullets[@]}"; do
  b="${bullets[$i]}"
  cat > /tmp/_b.tex << TEXEOF
\documentclass[a4paper,10pt]{article}
\usepackage[empty]{fullpage}
\usepackage{enumitem}
\usepackage[T1]{fontenc}
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1.0in}
\raggedright
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}}
\newsavebox{\bb}
\begin{document}
\resumeItemListStart
\item\small{\savebox{\bb}{$b}%
  \ifdim\wd\bb>492.39783pt \typeout{B$((i+1)) OVERFLOW \the\wd\bb}%
  \else\ifdim\wd\bb<418.53pt \typeout{B$((i+1)) SHORT \the\wd\bb}%
  \else\typeout{B$((i+1)) OK \the\wd\bb}\fi\fi $b\vspace{-2pt}}
\resumeItemListEnd
\end{document}
TEXEOF
  cd /tmp && pdflatex -interaction=nonstopmode _b.tex 2>/dev/null | grep -E "^B[0-9]+"
done
```

---

## The One-Bullet-at-a-Time Optimization Loop

This is the core method. Do NOT try to fix multiple bullets simultaneously — context gets confused.

### For OVERFLOW bullets (text > 492pt)

**Step 1 — Identify the excess.** How far over is it?
- 492–520pt: 1–2 words over. Small trim needed.
- 520–600pt: phrase-level cut needed.
- 600pt+: structural rewrite required. The bullet is doing too much.

**Step 2 — Apply trimming in order of preference:**

1. **Shorten or remove filler phrases**
   - "in order to" → "to"
   - "across the organization" → "org-wide" or cut
   - "as part of" → cut entirely
   - "fully automated" → "automated"
   - "on a monthly basis" → "monthly"

2. **Swap for a shorter synonym** (without losing meaning)
   - "redesigning" → "redesign" (drop -ing)
   - "utilizing" → "using" (never use "utilizing" anyway)
   - "implementation" → "rollout"
   - "configuration" → "config"
   - "recommendations" → "recommendations" → try shorter context

3. **Restructure the clause**
   - "by redesigning X and automating Y" → "via X redesign and Y automation"
   - "that became the platform's #1 entry point" → ", platform's #1 entry point"
   - "reduced insight latency from 7 days to same-day" → "cut insight latency 7 days → same-day"

4. **Remove the weakest qualifying detail**
   - "across 4 cohorts" can usually go if the D7/D30/D60 numbers are already there
   - "without drop in delivery velocity" is implied by zero-spillover elsewhere

5. **Structural rewrite for 600pt+ overflows**
   - The bullet is trying to say two things. Split the key metric from the context.
   - Keep the number, cut the backstory to a minimum.

**Step 3 — Test, iterate.** Run the harness on each candidate. Stop when you hit `OK` in 95–100% range.

### For SHORT bullets (text < 418pt)

**Step 1 — Add without padding.** Every addition must be substantive:

1. **Add a specific result** — "zero sprint spillovers", "10/10 CSAT", "120% bonus"
2. **Add team/org context** — "across two time zones", "for 40 government ministries"
3. **Add the method** — "via SQL pipelines", "using unsupervised ML clustering"
4. **Add the constraint** — "in 11 months while holding full-time role"
5. **Expand abbreviations once** — "config" → "configuration" if space allows

**Never pad with filler.** "in a fast-paced environment", "successfully", "proactively" — banned.

### The Width Sweet Spot

Aim for **488–492pt (99–100%)** if possible. This almost guarantees the bullet fits in one line
with every reasonable font rendering, including PDF export, print, and ATS.

Bullets at **470–487pt (95–98%)** are also fine — do not keep iterating past 5 attempts at this range.

Lock it and move on.

---

## LaTeX Special Characters — Escape Reference

When writing bullets in the shell harness, single-quote the string. Inside single-quoted bash strings,
you cannot use `'` directly. Workaround:

```bash
# Apostrophe inside single-quoted string:
'lead PM'\''s leave'   # closes quote, adds literal ', reopens quote
```

Common LaTeX in bullets:
| What you want | LaTeX code |
|---|---|
| → (arrow) | `$\rightarrow$` |
| ~35% | `\textasciitilde{}35\%` |
| **bold** | `\textbf{text}` |
| $1.2M | `\$1.2M` |
| #1 | `\#1` |
| Rs. symbol | `\textbf{Rs.60K/year}` or `\textbf{\textasciitilde{}Rs.60K/year}` |
| & | `\&` |

---

## Common Pitfalls

| Pitfall | What happens | Fix |
|---|---|---|
| Zero LaTeX warnings = single-line bullets | WRONG. `\raggedright` suppresses underfull hbox warnings. A 3-line bullet gives zero warnings. | Use `\savebox` harness — only accurate method. |
| Testing in Overleaf zoom ≠ 100% | Line breaks look different at 80% or 125% zoom. | Always set Overleaf to 100% zoom when visually checking, but trust the pt measurement. |
| Harness gives different result than full compile | Sometimes `\savebox` in isolation differs 1–2pt from full resume context due to list indentation. | Run the batch scan in context of actual itemize environment (the harness already does this). |
| Measuring HTML bullets with this harness | This harness is LaTeX only. HTML resumes use a different budget (158.07mm Roboto 9.5pt). | For HTML: use `measure_width.py` with `--font Roboto --size 9.5 --budget 158.07`. |
| Trying to fix multiple bullets at once | You lose track of which version you're on, and drift. | One bullet. Lock it. Move to next. |

---

## Worked Examples (Real Bullets, Real Measurements)

These are from the May 2026 optimization run on Satvik's archetype resumes.

| Final bullet | Width | % |
|---|---|---|
| `Sole PM on CRR for \textbf{10 consecutive sprints}; shipped \textbf{60+ features}: rule engine, asset mgmt, versioning, audit trail` | 484.84pt | 98.5% |
| `Built LLM Grooming bot; ranked \textbf{\#21 of 400+ teams (Top 6\%)} at AmEx Hackathon; productionized as \textbf{QE Assist}` | 489.73pt | 99.5% |
| `Drove \textbf{80\% AI-assisted story drafting} via ChatGPT Enterprise; cut manual story-writing across all sprint ceremonies` | 492.38pt | 100.0% |
| `Earned \textbf{Leadership in Action Award} from SVP Risk (6 months); rated \textbf{G1L2}, top Band 30 PO in org; \textbf{120\% bonus}` | 490.58pt | 99.6% |
| `Built Walmart GenAI root-cause analysis pipeline across \textbf{6 data sources}, covering \textbf{100K+ monthly driver contacts}` | 489.36pt | 99.4% |
| `Built L1/L2/L3 issue taxonomy and unsupervised ML clustering pipeline; cut insight latency from \textbf{7 days to same-day}` | 491.83pt | 99.9% |
| `Lifted Arabic sentiment \textbf{F1 +11\%} and intuition \textbf{+13\%}; Qatar Sharek \textbf{40-ministry} government platform (\$32M TCV)` | 489.38pt | 99.4% |
| `Unified Adobe Earned / Organic / Paid data via SQL; built spam detection model \textbf{F1 = 87\%} using Sprinklr AI Studio` | 488.30pt | 99.2% |
| `Ranked \textbf{\#1 globally} among all Sprinklr ICs within 6 months (\textbf{10/10 CSAT}); only IC promoted at 11 months out of 8` | 489.13pt | 99.4% |
| `Analyzed \textbf{1,500+ client patterns} across 15 verticals; launched Use Case Hub, \textbf{\#1 entry point} for dashboard creation` | 492.34pt | 100.0% |
| `Lifted Qatar Sharek app \textbf{7-day retention 40\% $\rightarrow$ 55\%} across 40 government ministries (\$32M TCV, 120 dashboards)` | 488.19pt | 99.1% |
| `Slashed AML risk-config speed-to-market \textbf{10 days $\rightarrow$ 3 days (70\%)} via rule UI redesign and API-automated approvals` | 490.51pt | 99.6% |
| `Shipped \textbf{44 of 57 planned features (77\%)} in 11 months while holding a full-time AmEx role; published CLI to \textbf{PyPI}` | 491.02pt | 99.7% |
| `Deployed \textbf{9 self-hosted LLMs} on Oracle VPS (Ollama, fallback chain); built FastAPI backend, CLI published to \textbf{PyPI}` | 492.07pt | 99.9% |

---

## The Full Workflow: Resume → Pixel-Perfect in Overleaf

```
1. Paste full resume .tex into Overleaf and compile once to confirm no errors.

2. Copy the batch scan script above, fill in ALL bullet strings as the array, run it.
   → Get a complete OVERFLOW / SHORT / OK report for every bullet in one pass.

3. For each OVERFLOW or SHORT bullet (one at a time, in order):
   a. Run /tmp/test_bullet.sh 'bullet text' → check result
   b. If OVERFLOW: apply trimming hierarchy (filler → synonym → restructure → rewrite)
   c. If SHORT: add substance (result → context → method → constraint)
   d. Iterate until OK in 95–100% range
   e. Lock the bullet — write it down
   f. Move to next bullet

4. Once all bullets are locked:
   a. Update the .tex file with all locked bullets
   b. Compile in Overleaf — verify 1 page, 0 errors
   c. Export PDF — do a final visual check at 100% zoom

5. Done. Every bullet is a single line at 95–100% fill.
```

**Rule: lock one bullet before touching the next. Never edit two bullets simultaneously.**

---

## Applying to HTML Resumes

The LaTeX `\savebox` method does not apply to HTML. For HTML resumes (template.html):

- Font: Roboto 9pt bullets
- Available width: ~158mm (varies by padding — measure by inspecting the rendered page)
- Method: use `scripts/measure_width.py --font Roboto --size 9 --budget 158`
- **NEVER use `text-align: justify`** on bullet containers — creates word gaps on multi-line bullets
- Always use `text-align: left` on `ul li`

See ref_05_html_design.md for the full HTML layout specification.
