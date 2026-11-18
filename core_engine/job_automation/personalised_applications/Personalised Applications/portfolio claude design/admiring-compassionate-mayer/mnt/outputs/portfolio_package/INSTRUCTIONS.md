# INSTRUCTIONS FOR CLAUDE DESIGN
## Read this file first, then PROMPT.md, then build.

---

## What this package is

This is a complete brief for building Satvik Jain's portfolio website. Everything you need is in this folder — every word of copy, every color code, every layout rule, every asset reference.

**Your job:** Build a single, production-ready HTML file. Open `PROMPT.md` now and follow it exactly.

---

## Folder structure

```
portfolio_package/
├── INSTRUCTIONS.md          ← You are here. Read first.
├── PROMPT.md                ← Full build specification. Read second, execute completely.
├── content/
│   └── portfolio_content.md ← All written copy for every section (already embedded in PROMPT.md)
├── assets/
│   ├── credentials/         ← Certificate images (place actual files here before building)
│   │   ├── amex_leadership_award.png     ← AmEx CMRC Leadership in Action Award, Q4'2024
│   │   ├── ggi_fellowship_letter.png     ← GGI Fellow 2024 graduation letter
│   │   └── gti_startup_weekend_1st.png   ← GTI Startup Weekend — 1st Place certificate
│   ├── brands/
│   │   └── gogogo_brand.png              ← GoGoGo ride-hailing brand image
│   └── asset_notes.md       ← Notes on each asset and how to use it
└── references/
    ├── qatar_press_release.md   ← Full text of Sprinklr Qatar official press release
    └── horizon_prd_summary.md  ← Horizon PRD summary (published GGI project)
```

---

## Critical rules

1. **Output = one single HTML file.** No separate CSS or JS files.
2. **Use all copy from PROMPT.md verbatim.** Do not rewrite or paraphrase.
3. **Use the exact colors from the design system.** Do not substitute.
4. **All 6 case studies must appear.** All 14 postcards must appear.
5. **Credentials section must appear** — show the 3 certificates as visual cards with images.
6. **If an image file is present in assets/**, reference it with `<img src="assets/...">` — the user will host these alongside the HTML.
7. **If an image file is missing**, render a styled placeholder div with the credential name and details — do not skip the section.
8. **All external links** open in `target="_blank"`.
9. **Mobile responsive** at 768px breakpoint.
10. **No Lorem Ipsum anywhere.**

---

## Key external links to embed

- Qatar press release: https://www.sprinklr.com/newsroom/the-state-of-qatar-debuts-unified-citizen-experience-management-platform/
- Horizon PRD (published): https://www.councilonsustainabledevelopment.org/post/horizon-a-gamified-stock-market-app-for-new-retail-investors
- LinkedIn: https://linkedin.com/in/satvik-jain-iitd
- GitHub: https://github.com/satvik-jain-iitd
- Email: satvik.jain@iitdalumni.com
- AI Songs (Google Drive): https://drive.google.com/drive/folders/1f8WyRNSA2u6x0BmSugD6U01G9yxWTtj-
- GoGoGo YouTube (brand anthem): https://www.youtube.com/watch?v=Lzx6c835UCA

---

## Start now. Open PROMPT.md.
