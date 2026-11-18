# Resume Design System — Border Frame
**Version:** 2.0 — 2026-05-23
**Base style:** Style 08 — Inset Border Frame (1.5pt, 8pt gap from page edges)
**Principle:** Design is purely decorative. Colors, border, background tint only. No content, font, spacing, or layout is ever changed.

---

## Structure of Every File

All 30 files share the same skeleton:

```latex
\usepackage[usenames,dvipsnames]{xcolor}
\usepackage{eso-pic}
\usepackage{tikz}
\input{glyphtounicode}

% ═══ COMPANY DESIGN LAYER ═══════════════════════════════════════
% ┌── SWAP COMPANY: Change only the hex codes below ──────────────┐
\definecolor{cprimary}{HTML}{XXXXXX}  % Border + section rules
\definecolor{cname}{HTML}{XXXXXX}     % Name heading
\definecolor{cpagebg}{HTML}{XXXXXX}   % Page background (tinted/dark only)
\pagecolor{cpagebg}                   % (tinted/dark only)
\definecolor{ctext}{HTML}{XXXXXX}     % Body text (dark mode only)
\AtBeginDocument{\color{ctext}}       % (dark mode only)
% └───────────────────────────────────────────────────────────────┘

\AddToShipoutPictureBG{%
  \begin{tikzpicture}[remember picture, overlay]
    \draw[color=cprimary, line width=1.5pt]
      ([xshift=8pt,yshift=-8pt]current page.north west)
      rectangle
      ([xshift=-8pt,yshift=8pt]current page.south east);
  \end{tikzpicture}%
}
```

---

## 3 Variant Types

| Variant | Background | Body text | What changes |
|---------|-----------|-----------|--------------|
| `light` | White (#FFFFFF) | Black (default) | `cprimary` + `cname` only |
| `tinted` | Very light brand tint | Black (default) | `cprimary` + `cname` + `cpagebg` + `\pagecolor` |
| `dark` | Deep dark brand bg | Light/white | All above + `ctext` + `\AtBeginDocument{\color{ctext}}` |

---

## 10 Companies — Color Reference

### Google → AI PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `4285F4` | `202124` | — | — |
| dark    | `8AB4F8` | `FFFFFF` | `202124` | `E8EAED` |
| tinted  | `4285F4` | `1A73E8` | `EEF3FE` | — |

### OpenAI → Startup PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `10A37F` | `0D0D0D` | — | — |
| dark    | `10A37F` | `FFFFFF` | `0D0D0D` | `ECECEC` |
| tinted  | `10A37F` | `0A7A5F` | `F0FBF8` | — |

### Meta → Growth PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `1877F2` | `1C1E21` | — | — |
| dark    | `2D88FF` | `FFFFFF` | `18191A` | `E4E6EB` |
| tinted  | `1877F2` | `166FE5` | `EEF5FF` | — |

### Amazon → Data PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `FF9900` | `232F3E` | — | — |
| dark    | `FF9900` | `FFFFFF` | `232F3E` | `CCCCCC` |
| tinted  | `FF9900` | `232F3E` | `FFF8EC` | — |

### Microsoft → Platform PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `00A4EF` | `243078` | — | — |
| dark    | `00A4EF` | `FFFFFF` | `201F1E` | `E5E5E5` |
| tinted  | `00A4EF` | `243078` | `EFF9FF` | — |

### Stripe → FinTech PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `635BFF` | `0A2540` | `F6F9FC` | — |
| dark    | `635BFF` | `FFFFFF` | `0A2540` | `C1C9D2` |
| tinted  | `635BFF` | `0A2540` | `F3F2FF` | — |

### Razorpay → FinTech PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `0D94FB` | `012652` | — | — |
| dark    | `3395FF` | `FFFFFF` | `012652` | `C8D8E8` |
| tinted  | `0D94FB` | `012652` | `EDF6FF` | — |

### Flipkart → Consumer/App PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `2874F0` | `172337` | — | — |
| dark    | `2874F0` | `FFB800` | `172337` | `E8E8E8` |
| tinted  | `2874F0` | `172337` | `F0F7FF` | — |

> **Note on Flipkart dark:** name color is Flipkart Yellow (`FFB800`) on dark navy — creates a distinctive two-brand-color look.

### Figma → Platform PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `A259FF` | `1E1E1E` | — | — |
| dark    | `A259FF` | `FFFFFF` | `1E1E1E` | `E5E5E5` |
| tinted  | `A259FF` | `1E1E1E` | `FAF5FF` | — |

### Apple → Consumer/App PM archetype
| Variant | cprimary | cname | cpagebg | ctext |
|---------|----------|-------|---------|-------|
| light   | `0066CC` | `1D1D1F` | — | — |
| dark    | `007AFF` | `FFFFFF` | `1D1D1F` | `F5F5F7` |
| tinted  | `0066CC` | `1D1D1F` | `F0F6FF` | — |

---

## How to Swap to a New Company

1. Pick the right archetype file (or any existing company file as a starting point)
2. Open the COMPANY DESIGN LAYER block near the top
3. Change only the hex codes — everything else stays identical
4. **To add a new company from scratch:** find their official hex from their brand guide or website CSS, then pick Light / Dark / Tinted variants

**Quick color sourcing:**
- Brand guidelines pages, press kits, or media kits
- Inspect element on their website → look for CSS `--primary`, `--brand`, or similar variables
- Brandfetch.com → search company name → "Colors" tab

---

## Company Quick-Pick Table

| Target Company | Folder | Archetype used | Why this archetype |
|----------------|--------|----------------|--------------------|
| Google | `google/` | AI PM | Google deepest hiring in AI PM / Gemini |
| OpenAI | `openai/` | Startup PM | Pure AI company, 0-to-1 build culture |
| Meta | `meta/` | Growth PM | Growth-obsessed, data-driven scaling |
| Amazon | `amazon/` | Data PM | Data/working-backwards culture, AWS |
| Microsoft | `microsoft/` | Platform PM | Platform/cloud/enterprise products |
| Stripe | `stripe/` | FinTech PM | Payments infra, risk, developer fintech |
| Razorpay | `razorpay/` | FinTech PM | Indian fintech leader, payments/risk |
| Flipkart | `flipkart/` | Consumer App PM | Consumer e-commerce, growth loops |
| Figma | `figma/` | Platform PM | Design platform, developer tools, API |
| Apple | `apple/` | Consumer App PM | Consumer product design, iOS/macOS |

---

## What Is Never Changed

- `\documentclass[a4paper,10pt]{article}` — never touch
- Margins — never touch
- Font family (Computer Modern) — never add `lmodern`
- `\usepackage[T1]{fontenc}` — always present
- `\resumeItemListStart` / `\parfillskip=0pt` — never touch
- Bullet content, action verbs, metrics — never touch
- Section order, spacing, tabularx widths — never touch

---

## File Inventory

```
resumes_amex/
├── DESIGN_SYSTEM.md
├── resume_fintech-risk-pm_amex-08_border_frame_2026-05-23.tex   ← canonical Style 08 reference
├── _archive/         ← old styles 01–07 (archived, not deleted)
├── google/
│   ├── resume_ai-pm_google_light_2026-05-23.tex
│   ├── resume_ai-pm_google_dark_2026-05-23.tex
│   └── resume_ai-pm_google_tinted_2026-05-23.tex
├── openai/
│   ├── resume_startup-pm_openai_light_2026-05-23.tex
│   ├── resume_startup-pm_openai_dark_2026-05-23.tex
│   └── resume_startup-pm_openai_tinted_2026-05-23.tex
├── meta/
│   ├── resume_growth-pm_meta_light_2026-05-23.tex
│   ├── resume_growth-pm_meta_dark_2026-05-23.tex
│   └── resume_growth-pm_meta_tinted_2026-05-23.tex
├── amazon/
│   ├── resume_data-pm_amazon_light_2026-05-23.tex
│   ├── resume_data-pm_amazon_dark_2026-05-23.tex
│   └── resume_data-pm_amazon_tinted_2026-05-23.tex
├── microsoft/
│   ├── resume_platform-pm_microsoft_light_2026-05-23.tex
│   ├── resume_platform-pm_microsoft_dark_2026-05-23.tex
│   └── resume_platform-pm_microsoft_tinted_2026-05-23.tex
├── stripe/
│   ├── resume_fintech-risk-pm_stripe_light_2026-05-23.tex
│   ├── resume_fintech-risk-pm_stripe_dark_2026-05-23.tex
│   └── resume_fintech-risk-pm_stripe_tinted_2026-05-23.tex
├── razorpay/
│   ├── resume_fintech-risk-pm_razorpay_light_2026-05-23.tex
│   ├── resume_fintech-risk-pm_razorpay_dark_2026-05-23.tex
│   └── resume_fintech-risk-pm_razorpay_tinted_2026-05-23.tex
├── flipkart/
│   ├── resume_consumer-app-pm_flipkart_light_2026-05-23.tex
│   ├── resume_consumer-app-pm_flipkart_dark_2026-05-23.tex
│   └── resume_consumer-app-pm_flipkart_tinted_2026-05-23.tex
├── figma/
│   ├── resume_platform-pm_figma_light_2026-05-23.tex
│   ├── resume_platform-pm_figma_dark_2026-05-23.tex
│   └── resume_platform-pm_figma_tinted_2026-05-23.tex
└── apple/
    ├── resume_consumer-app-pm_apple_light_2026-05-23.tex
    ├── resume_consumer-app-pm_apple_dark_2026-05-23.tex
    └── resume_consumer-app-pm_apple_tinted_2026-05-23.tex
```

Compile any file directly in Overleaf (pdfLaTeX). Each is fully self-contained.
