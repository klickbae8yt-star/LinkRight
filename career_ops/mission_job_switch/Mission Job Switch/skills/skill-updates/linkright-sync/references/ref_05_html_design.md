# ref_05 — HTML Design System

Loaded at Gate 6. Color palettes, typography tokens, and design application rules for HTML resumes.

---

## CSS Variable Map (assets/template.html)

These are the variables to set at Gate 6:

```css
:root {
  --brand-primary-color:     [accent — used for name, section headers, rule lines]
  --brand-secondary-color:   [secondary accent — job titles, company names]
  --brand-tertiary-color:    [optional tertiary — dates, contact info icons]
  --brand-quaternary-color:  [optional quaternary — rarely used]

  --ui-canvas-bg-color:      #F1F3F4   /* keep unless user wants dark mode */
  --ui-page-bg-color:        #FFFFFF   /* always white for print */
  --ui-text-primary-color:   #202124   /* always near-black for body text */
  --ui-text-secondary-color: #5F6368   /* meta text, dates, etc. */
  --ui-divider-color:        #DADCE0   /* hairline dividers */
}
```

**Only `--brand-primary-color` and `--brand-secondary-color` change per company.**
Everything else stays at defaults unless user explicitly requests changes.

---

## Pre-Built Company Palettes

Use these when the user targets a known company. Cite the exact hex values.

| Company | Primary | Secondary | Notes |
|---|---|---|---|
| Google | #4285F4 | #EA4335 | Classic Google Blue/Red |
| Amazon | #FF9900 | #232F3E | Amazon Orange on dark navy |
| Microsoft | #0078D4 | #106EBE | Microsoft Blue family |
| Meta | #0866FF | #1877F2 | Meta Blue |
| Apple | #000000 | #6E6E73 | Black with gray secondary |
| Anthropic | #D4A853 | #1A1A1A | Warm gold on near-black |
| OpenAI | #10A37F | #1A1A1A | OpenAI teal on near-black |
| Stripe | #635BFF | #0A2540 | Stripe purple on dark navy |
| Airbnb | #FF5A5F | #484848 | Coral on charcoal |
| Uber | #000000 | #276EF1 | Black + Uber Blue |
| Flipkart | #2874F0 | #FFE500 | Flipkart Blue + Yellow |
| Meesho | #9B2FAB | #F43397 | Purple-Pink palette |
| PhonePe | #5F259F | #FFFFFF | PhonePe Purple |
| Razorpay | #3395FF | #072654 | Razorpay Blue |
| CRED | #1D1D1D | #C5A64F | Near-black + Gold |
| Groww | #5367FF | #00D09C | Blue-Green fintech |
| Zepto | #9B2FAB | #FC3F4B | Purple-Red quick commerce |
| American Express | #006FCF | #53565A | Science Blue primary + Abbey gray secondary |
| Mastercard | #EB001B | #F79E1B | Red-Orange classic |
| PayPal | #003087 | #009CDE | Deep navy + Sky blue |
| Procol | #1B4F9B | #F5811F | Navy Blue + Orange |
| Sprinklr | #6C1D8F | #E8490F | Purple + Orange |

---

## Neutral Palettes (No specific company)

Use for archetype base resumes:

| Archetype | Primary | Secondary | Vibe |
|---|---|---|---|
| AI PM | #1A1A2E | #E94560 | Dark navy + Electric red |
| Enterprise PM | #1B4F9B | #2E86AB | Professional blue family |
| Growth PM | #00C853 | #1565C0 | Green-Blue growth energy |
| Platform PM | #37474F | #607D8B | Slate blue-grey, engineering feel |
| Data/Analytics PM | #1565C0 | #FF6F00 | Deep blue + Amber |
| Generalist PM | #2C3E50 | #2980B9 | Classic navy professional |

---

## Contrast Validation

Run `validate_contrast.py` after setting colors. WCAG 2.0 AA minimum:

- **Normal text** (body, bullets): contrast ratio ≥ 4.5:1 against white page
- **Large text** (name, section headers): contrast ratio ≥ 3:1 against white page

Primary color on white (#FFFFFF) must meet the large-text threshold at minimum.

**Quick check:** contrast ratio of text color vs white background.
- `#4285F4` (Google Blue) on white = 3.04:1 → OK for large text (name/headers)
- `#202124` on white = 16.1:1 → excellent for body text
- `#5F6368` on white = 5.74:1 → OK for secondary text

If primary color fails contrast on white: darken it by 10–20% until it passes.

---

## Typography Tokens (Do Not Change)

These are calibrated for A4 single-page print. Don't modify without re-calibrating measure_width.py.

```
--font-size-name:     20pt  (full name in header)
--font-size-header:   13pt  (section headers: EXPERIENCE, EDUCATION, etc.)
--font-size-subhead:  10.5pt (job titles, company names)
--font-size-body:     9.5pt  (bullet text — this is what measure_width.py is calibrated for)
--font-size-contact:  9pt    (contact info line)
```

---

## Design Application Checklist (Gate 6)

- [ ] Set `--brand-primary-color` and `--brand-secondary-color` in `:root`
- [ ] Run `validate_contrast.py` — both colors pass WCAG AA on white
- [ ] Run final `measure_width.py` pass on 3 random bullets — confirm widths unchanged
- [ ] Print preview at 100% zoom — check no content spills below A4 fold
- [ ] Confirm name in header uses `--brand-primary-color`
- [ ] Confirm section headers use `--brand-primary-color`
- [ ] Confirm job titles use `--brand-secondary-color`
- [ ] Confirm body text uses `--ui-text-primary-color` (#202124)
- [ ] Confirm dates/meta text uses `--ui-text-secondary-color` (#5F6368)
