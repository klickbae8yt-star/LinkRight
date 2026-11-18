# ref_06 — ATS Rules & Final Delivery Checklist

Loaded at Gate 7. Complete ATS compliance rules and delivery protocol.

---

## What ATS Does (and Why It Matters)

ATS (Applicant Tracking Systems) — Greenhouse, Lever, Ashby, Workday — parse your resume as
raw text before any human reads it. They extract: name, contact, job titles, companies, dates,
and keywords. If parsing fails, your resume is invisible to the recruiter.

Common ATS failure modes:
- Tables scramble column order into nonsense
- Text in absolute-positioned divs is missed entirely
- Multi-column layouts get read left-to-right across columns (chaos)
- Content clipped by `overflow:hidden` simply doesn't exist to ATS
- Fonts loaded from CDN that fail to load can cause layout reflow

---

## HTML ATS Requirements

**Must pass:**
- [ ] No `<table>` used for layout (tables for actual data OK, but verify)
- [ ] No `position: absolute` or `position: fixed` on any text-containing element
- [ ] No `column-count: 2+` or multi-column CSS
- [ ] No `overflow: hidden` on any element that contains text content
- [ ] No `height: [fixed]` + `overflow: hidden` combo on bullet containers
- [ ] No `<canvas>` elements
- [ ] Contact information is in the document body (not CSS-generated content)
- [ ] Section headers are plain text elements (`<h2>`, `<div>`, `<p>`) — not images
- [ ] All hyperlinks have visible, readable text (not just colored dots or icons)

**Recommended:**
- [ ] Use `<a href="mailto:...">` for email (parseable)
- [ ] LinkedIn URL in plain text (not just a linked logo)
- [ ] Phone number in plain text
- [ ] Name in an `<h1>` or large text element near top of document

---

## LaTeX ATS Requirements

**Must pass:**
- [ ] No `\begin{minipage}` side by side (multi-column)
- [ ] No `\begin{tabular}` for layout
- [ ] No textbox packages (`textpos`, `tcolorbox` for layout)
- [ ] All contact information in document body (not in header/footer via `\fancyhead`)
- [ ] No critical information in `\includegraphics`
- [ ] `\href{url}{visible text}` — text is readable, not just a symbol

---

## Pre-Delivery Validation Sequence

Run in this order. Don't ship until all pass.

```
Step 1: python ats_scanner.py '{"content": "[resume_html]", "format": "html"}'
        → Must be status: "pass" (no critical issues)

Step 2: python ai_smell_checker.py '{"text": "[all_bullet_text]"}'
        → Must be status: "pass" (0 flags)
        → "warn" (1-2 flags) acceptable only if user reviewed and approved

Step 3: python constraint_checker.py '{"resume_text": "[full_text]", "setup_path": "[path]"}'
        → Must be status: "pass" (0 violations)

Step 4: python validate_page_fit.py '{"html_path": "[path]"}'  [HTML only]
        → Must confirm: fits on 1 page

Step 5: Final measure_width.py sample check (3 random bullets)
        → Must confirm: widths unchanged after Gate 6 styling
```

---

## File Naming Convention

```
HTML:   resume_[company-slug]_[YYYY-MM-DD].html
LaTeX:  resume_[company-slug]_[YYYY-MM-DD].tex

Archetype base (no JD):
        resume_ai-pm_base_[YYYY-MM-DD].html
        resume_enterprise-pm_base_[YYYY-MM-DD].html
        resume_growth-pm_base_[YYYY-MM-DD].html
        resume_platform-pm_base_[YYYY-MM-DD].html
        resume_data-pm_base_[YYYY-MM-DD].html

Internal use (not for ATS submission):
        resume_amex-internal_platform-pm_[YYYY-MM-DD].html
```

---

## Quality Report Template

Show this to user at Gate 7 before final approval:

```
QUALITY REPORT — [Company/Archetype] — [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATS scan:          [PASS / FAIL — N critical issues]
AI-smell:          [PASS / WARN N flags / FAIL N flags]
Page fit:          [PASS 1 page / FAIL — N mm overflow]
Width coverage:    [N/N bullets at 95–100%]
Constraint check:  [PASS / FAIL — N violations]

Signal coverage:
  [signal] ✓    [signal] △    [signal] ✗ (not claimed)

Format:   [HTML / LaTeX]
Output:   [filename.html]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

All items must show PASS before asking for final approval.
If any FAIL: fix and rerun the failed check. Never ship with a known failure.
