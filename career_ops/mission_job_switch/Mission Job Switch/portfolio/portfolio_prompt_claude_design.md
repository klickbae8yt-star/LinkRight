# One-Shot Portfolio Prompt for Claude Design
**Version:** 1.0 — 2026-05-23
**Usage:** Paste the entire PROMPT section below into Claude.ai (claude.ai/new) as a single message.
**Credits:** Use on a fresh session. This is designed to produce the full portfolio in one pass.

---

## NOTES BEFORE YOU PASTE

- This prompt is self-contained. Every word of copy, every color, every layout rule is included.
- The output should be a single HTML file that can be opened directly in a browser.
- Do NOT split this across multiple messages — it is designed as one complete instruction.
- If Claude Design asks a clarifying question, answer with: "Use the defaults specified in the prompt."

---

## ─────────────────────────────────────────────
## PROMPT — COPY EVERYTHING BELOW THIS LINE
## ─────────────────────────────────────────────

Build me a complete, production-ready, single-file portfolio website as an HTML file. This is for Satvik Jain, a Product Manager. Every pixel of copy, every color, every layout spec is defined below. Follow them exactly.

---

## VISUAL CONCEPT: "Signal Flow"

Career as a data pipeline. Each stage of the career is a **node** connected by an animated flow line. The metaphor is: raw input → structured output. This person takes chaos and turns it into products.

The overall aesthetic is **clean, dark, and precise** — like a well-designed B2B dashboard. Not flashy startup landing page energy. Not corporate either. Something in between: confident, considered, a little bit sharp.

---

## DESIGN SYSTEM

### Colors
```
Background:       #0a1628   (deep navy — primary background)
Surface:          #111f3a   (slightly lighter navy — cards, sections)
Surface-2:        #1a2f4f   (hover states, active nodes)
Accent:           #3b82f6   (electric blue — pipeline lines, highlights, CTAs)
Accent-dim:       #1d4ed8   (darker blue — borders, subtle accents)
Text-primary:     #f1f5f9   (near-white — headlines, key text)
Text-secondary:   #94a3b8   (gray-blue — body copy, dates, labels)
Text-muted:       #475569   (dark gray — very secondary info)
Green:            #10b981   (confirmed, achieved, shipped)
Gold:             #f59e0b   (awards, recognition moments)
Border:           rgba(59, 130, 246, 0.15)  (subtle blue border for cards)
Pipeline-glow:    rgba(59, 130, 246, 0.6)   (glow on the animated pipeline line)
```

### Typography
```
Font stack: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
Import from Google Fonts: Inter (weights 300, 400, 500, 600, 700, 800)

Headlines (H1):   64px / weight 800 / tracking -2px / color Text-primary
Section titles:   13px / weight 600 / tracking 4px / UPPERCASE / color Accent
Chapter titles:   28px / weight 700 / color Text-primary
Body text:        16px / weight 400 / line-height 1.75 / color Text-secondary
Labels:           12px / weight 500 / tracking 1px / UPPERCASE / color Text-muted
Numbers/stats:    48px / weight 800 / color Accent
```

### Spacing & Layout
```
Max content width: 1100px, centered
Section padding:   100px top and bottom
Mobile breakpoint: 768px
Card border-radius: 12px
Button border-radius: 8px
```

### Animation Principles
```
All transitions: cubic-bezier(0.4, 0, 0.2, 1), 300ms unless specified
Scroll animations: Elements fade in from 20px below as they enter viewport (IntersectionObserver)
Pipeline animation: A glowing dot travels along the SVG path, looped, 4s duration
Hover on cards: translateY(-4px) + border-color brightens to Accent
No animation for users who prefer-reduced-motion (media query)
```

---

## HTML STRUCTURE

Single HTML file. Use `<style>` tag in `<head>` for all CSS. Use `<script>` tag before `</body>` for all JS.

Load Inter from Google Fonts via `<link>` in head.

The page has exactly 5 sections, in order:
1. `#hero` — Signal Flow pipeline + name + intro
2. `#story` — 5 career chapter scroll reveal
3. `#case-studies` — 4 expandable project cards
4. `#diary` — 12 postcard entries in grid
5. `#contact` — closing statement + links

Sticky top navigation bar with smooth-scroll links to each section.

---

## SECTION 1: HERO (`#hero`)

**Layout:** Full viewport height. Content centered vertically and horizontally.

**Top of section:** A horizontal SVG pipeline visualization spanning ~80% of the viewport width. The pipeline shows 5 nodes connected by a flowing line. A glowing blue dot animates along the path, left to right, looping continuously.

### Pipeline Nodes (left to right):
```
Node 1:  "Sprinklr IC"         2022    → color: Text-muted (starting point)
Node 2:  "Qatar + Walmart"     2023    → color: Accent
Node 3:  "PM Transition"       2024    → color: Accent
Node 4:  "AmEx Risk PM"        2024–   → color: Green (active/current)
Node 5:  "LinkRight"           2025–   → color: Gold (building)
```

Each node is a circle (16px diameter) with a label below it (name, 11px, Text-secondary) and a year below that (10px, Text-muted). The line connecting them is 2px, color Accent at 40% opacity. The animated dot is 10px, color Accent, with a radial glow (box-shadow: 0 0 12px Accent).

**Below the pipeline:**

```
[Large headline — center aligned]
Satvik Jain

[Sub-headline — center aligned, 20px, Text-secondary, weight 400]
Product Manager · IIT Delhi

[3-line descriptor — center aligned, 16px, Text-secondary, max-width 580px, margin auto]
I turn messy, ambiguous problems into products people actually use —
by going deep on the data, earning trust with the room,
and shipping before I ask for the title.

[Stats row — 3 items, centered, with dividers between]
4+ years    ·    $32M+ shaped    ·    60+ features shipped solo

[CTA button — centered, 44px height, Accent background]
See the work ↓
```

The stats row items: number in 20px weight 700 Accent, label in 12px Text-muted below.

CTA button links to `#case-studies` with smooth scroll.

---

## SECTION 2: THE STORY (`#story`)

**Layout:** Single column, max-width 720px, centered. Each chapter is a distinct block separated by a thin horizontal rule (1px, Border color).

**Section label above:** "THE STORY" in Label style (13px, uppercase, tracking 4px, Accent color). Below it, a thin 40px underline bar in Accent.

**Scroll animation:** Each chapter fades in from 20px below as it enters the viewport. Use IntersectionObserver with threshold 0.1.

### Chapter structure (repeat for all 5):
```
[Chapter number]  — 11px, Text-muted, uppercase, tracking 2px, e.g. "CHAPTER 01"
[Chapter title]   — 28px, weight 700, Text-primary
[Body text]       — 16px, weight 400, line-height 1.85, Text-secondary
```

**Spacing:** 72px between chapters.

### CHAPTER 01 — The Foundation

**Number:** CHAPTER 01
**Title:** The Foundation

**Body:**
My father died when I was 11.

I'm not starting here for sympathy. I'm starting here because it's the most honest explanation for how I operate. When something important breaks, you figure out who's responsible — and you become that person.

My family didn't fall apart. It held. My mother worked. My sister studied. And I watched, very closely, how systems either support people during hard moments or quietly fail them.

That question — *why do some systems work and others collapse* — became the lens I've used to look at every problem since.

---

### CHAPTER 02 — The Theory vs. Practice Problem

**Number:** CHAPTER 02
**Title:** The Theory vs. Practice Problem

**Body:**
IIT Delhi was academically hard for me. I graduated with a 6.43 CGPA in Civil Engineering — not a number I hide.

What I can also tell you: I scored 10/10 in every single practical lab I ever sat in. That gap wasn't about intelligence. It was about how I learn. I don't absorb things from textbooks. I absorb them by doing. When the problem is real and the stakes are present, something shifts.

This pattern has followed me everywhere. The Sprinklr Gold Medal. The AmEx roadmap built from scratch. LinkRight, shipped while holding a full-time job. The fastest I've ever grown is when the problem is slightly too large for me and I have to figure it out on the way.

---

### CHAPTER 03 — The Gold Medal Nobody Saw Coming

**Number:** CHAPTER 03
**Title:** The Gold Medal Nobody Saw Coming

**Body:**
Six months into my first real job, my director put my name on a slide in a global all-hands meeting.

Number one. Out of every implementation consultant at Sprinklr worldwide. 10/10 customer satisfaction.

I wasn't chasing a medal. I was just trying not to drown in my first enterprise engagement. The award mattered less than what it proved to me: that when I'm in an environment where I can apply what I know *practically*, I operate at a very high level.

What followed was the biggest deal Sprinklr had ever signed — a $32 million engagement with the Government of Qatar. Forty ministries. Citizens interacting with public services. Arabic-language dashboards for the Prime Minister's office. And a Black Friday night at Walmart, pulling live data insights in real time for a room full of VPs.

The best products are built by people who stay in the room when it gets messy, not just when it's clean.

---

### CHAPTER 04 — Solo Ownership

**Number:** CHAPTER 04
**Title:** Solo Ownership

**Body:**
When I joined American Express in 2024, I was the only product manager on my team.

No one above me. An 18-person engineering team that needed direction. A document with 21 requirements and no roadmap.

I spent the first few weeks talking to compliance analysts across 6 global regions — understanding what people actually needed before I touched any plan. By week 6, I had a 3-year roadmap. By week 8, the SVP of Risk Management gave me an award for it. I hadn't shipped a single feature yet.

Then I ran 10 consecutive sprints. Alone. And then, twice in the same year, the strategy changed completely. Both times, the team was watching how I'd respond. Both times, we were back in motion within a week.

The value of a product manager is directly proportional to how fast they can reorient *without losing the team*.

---

### CHAPTER 05 — Building Things That Matter

**Number:** CHAPTER 05
**Title:** Building Things That Matter

**Body:**
LinkRight started as a tool I built for myself. I was running a job search and the AI tools available were making me sound like someone I wasn't. Polished. Inflated. Unrecognizable.

Before writing a single line of code, I spent months talking to 147 people and reaching out to over 7,000 more to understand whether this problem was uniquely mine. It wasn't.

I'm still building it, while holding my AmEx role full-time.

But the thing that means most to me this year isn't a product. It's the colleague who came to stay with me after a layoff. We ran 15 to 20 mock interview sessions together over 3 months. He secured a product role without a single day of unemployment.

Building something is great. Watching someone go from zero confidence to performing at their ceiling is a different kind of impact entirely.

---

## SECTION 3: CASE STUDIES (`#case-studies`)

**Section label:** "THE WORK" in Label style.

**Layout:** 2×2 grid on desktop. 1-column stack on mobile. Each card is a click-to-expand accordion. Collapsed state shows summary. Expanded state reveals full details.

### Card structure:
```
[Tag/label]        — 10px, uppercase, tracking 2px — e.g. "ENTERPRISE · $32M"
[Project name]     — 22px, weight 700, Text-primary
[One-line summary] — 14px, Text-secondary
[Expand arrow]     — right-aligned ↓ / ↑ on toggle

--- EXPANDED (hidden by default, smooth height animation) ---
[Problem]   — bold label + paragraph
[What I did] — bold label + paragraph
[Outcome]   — bold label + paragraph, key numbers highlighted in Accent color
```

Cards: Surface background, Border border, 12px radius. On hover: Surface-2 background, border brightens to `rgba(59, 130, 246, 0.4)`. Expanded state: left border 3px solid Accent.

---

### Card 01 — Qatar Citizen Experience

**Tag:** ENTERPRISE · $32M
**Name:** Qatar Citizen Experience Platform
**Summary:** Built real-time Arabic dashboards for 40 government ministries.

**EXPANDED:**

*The problem:* Qatar ranked 78th globally on e-government services — behind every other Gulf country. The government needed to understand, in real time, how citizens felt about interacting with 40 different ministries.

*What I did:* Led the insights layer for Sprinklr's largest-ever deal. Built Arabic-language dashboards for the Prime Minister's office. Scaled the delivery team from 6 to 14 people and personally reviewed 120 dashboards in 4 weeks.

*What changed:* Time to insight dropped from **2 days to 2 hours**. Qatar's UN e-government ranking moved from **78th to 53rd** — a 25-position jump.

---

### Card 02 — Walmart Driver Retention

**Tag:** GENAI · ANALYTICS
**Name:** Walmart Spark Driver Root Cause Analysis
**Summary:** Built the system that told Walmart why its gig drivers were quitting.

**EXPANDED:**

*The problem:* Walmart's gig driver platform was losing most of its drivers within 2 months. Over 100,000 monthly support cases. Data scattered across 6 completely different sources with no unified picture.

*What I did:* Designed and built a root cause product that unified all 6 data sources and used machine learning to automatically surface the patterns behind driver churn. Led daily cross-functional work and weekly updates directly to Walmart's VP of Product.

*What changed:* Time to insight went from **7 days to same-day**. The pilot converted to a **$1.2M deal** with **$9M+ in pipeline** behind it.

---

### Card 03 — AmEx Risk Platform

**Tag:** FINTECH · SOLO PM
**Name:** American Express Customer Risk Rating Platform
**Summary:** Built the risk scoring platform for 100M+ customer accounts. Alone.

**EXPANDED:**

*The problem:* AmEx needed to rebuild the system that determines the risk profile of every customer account — 100 million+ accounts across 40+ markets. The platform hadn't been properly updated in years.

*What I did:* Joined as the only PM. Turned a 21-requirement document into a coherent product architecture and 3-year roadmap. Led 10 consecutive sprints solo, shipped 60+ features, navigated 2 major strategy pivots without losing momentum, and designed 3 core product interfaces from scratch.

*What changed:* Risk configuration that used to take **10 days now takes 3**. Received the **highest performance rating** among all Band 30 Product Owners in my VP's organization. **120% bonus.**

---

### Card 04 — LinkRight (Solo Build)

**Tag:** AI · SOLO BUILD · LIVE
**Name:** LinkRight — Career Navigation Platform
**Summary:** Built an AI system that helps people apply for jobs as themselves.

**EXPANDED:**

*The problem:* AI career tools were helping people sound polished — but not honest. Job seekers were applying as inflated, unrecognizable versions of themselves and getting filtered out.

*What I did:* Validated the problem with **147 survey responses** and **7,000+ outreach contacts** before building anything. Then built a career navigation platform solo — AI resume parser, 16-dimension evaluation system, fabrication guards — while holding a full-time job at AmEx.

*Where it is:* **44 features shipped**, published to PyPI (`pip install linkright`). Still building.

---

## SECTION 4: BUILD DIARY (`#diary`)

**Section label:** "BUILD DIARY"
**Subtitle (below label):** "Not every milestone. The ones that changed something." — 14px, Text-muted, italic

**Layout:** 3-column masonry grid on desktop (use CSS columns: 3 with column-gap 20px). 2-column on tablet. 1-column on mobile.

### Postcard structure:
```
[Date]       — 11px, Text-muted, uppercase, tracking 1px
[Title]      — 16px, weight 600, Text-primary
[Body]       — 14px, line-height 1.7, Text-secondary (2-4 sentences)
```

Card style: Surface background, 1px Border border, 12px radius, 24px padding. NO hover animation on postcards — they should feel like paper, not interactive elements.

Use a subtle left-border accent on cards — 3px solid at 30% opacity Accent — to give them a faint "tagged" feel.

---

### Postcard 01 — The Gold Medal
**Date:** NOV 2022
**Title:** The Gold Medal Nobody Expected

Six months in, my director put my name on a slide in a global all-hands meeting. Number one globally. 10/10 customer satisfaction. I remember thinking: *maybe I'm better at this than I thought.* That was the first time in years I let myself believe it.

---

### Postcard 02 — Midnight in Doha
**Date:** JAN 2023
**Title:** Midnight in Doha

The Qatar project was 40 ministries, all in Arabic, all live. Four weeks, 120 dashboards, 14 people. The moment I realized the Prime Minister's office would use this to make decisions about citizens — that there was no draft — changed how I approach every project since.

---

### Postcard 03 — Walmart, Black Friday
**Date:** NOV 2023
**Title:** Walmart, Black Friday, Real-Time

10 VPs watching a live system. The machine was ingesting data automatically. But someone had to translate what it meant in real time — what the driver churn patterns said, what to watch for. I was pulling screenshots and narrating live. No script. That's the part AI won't replace anytime soon.

---

### Postcard 04 — The Invite
**Date:** FEB 2024
**Title:** The Invite That Changed Everything

Anish Singhal, VP of Product at Sprinklr, scheduled a call with me. He asked if I wanted to join his product team. I'd been running the project like a PM — without the title. He saw it. The formal transition happened because the work spoke first. I try to remember that every time I'm tempted to ask for recognition before I've earned it.

---

### Postcard 05 — The Award Before Shipping
**Date:** SEP 2024
**Title:** An Award Before I Shipped Anything

Three weeks at AmEx. No roadmap, no structure, a 21-requirement document. I spent my first weeks just listening — compliance analysts in the US, Europe, Asia-Pacific. By week 6 I had a 3-year roadmap. By week 8 the SVP gave me a Leadership in Action Award. I hadn't shipped a single feature. Clarity, delivered early, is a product.

---

### Postcard 06 — The Week the Strategy Changed
**Date:** DEC 2024
**Title:** The Week the Strategy Changed

We were weeks from production. The data team couldn't deliver. Leadership paused everything. 18-person team. 18-month build. Paused. I had 3 days to redirect the energy in the room. I turned the pause into a project — mapped the problem from scratch, scoped a solution. That project is still running today. Sometimes the pivot *is* the product.

---

### Postcard 07 — 147 Responses
**Date:** MAR 2025
**Title:** 147 People Said Yes Before Line 1 of Code

I ran a survey before building LinkRight. 147 responses. 7,000+ cold outreach. Every response was some version of the same thing: *the tools make me sound like someone I'm not.* That one sentence became the north star. Build the thing that lets people be themselves.

---

### Postcard 08 — pip install linkright
**Date:** JUN 2025
**Title:** pip install linkright

First time I ran it and it worked. Quieter than I expected — more like relief than celebration. The thing I'd built alone, across 11 months and 44 features, was now a package anyone could install. That's when I understood why people keep building even when it's hard.

---

### Postcard 09 — Rank 21 of 400
**Date:** JAN 2025
**Title:** Rank 21 of 400 Teams

24-hour hackathon at AmEx. We built a bot that auto-drafts user stories from requirements. Ranked 21st out of 400+ teams. The company later productionized the concept. The best ideas are usually the simplest ones.

---

### Postcard 10 — Zero Days Unemployed
**Date:** JUL 2025
**Title:** Zero Days Unemployed

A junior colleague stayed with me after a layoff. We ran 15–20 mock interview sessions over 3 months. He got an APM role without a single day of unemployment. I've shipped a lot of things. That one still means the most.

---

### Postcard 11 — My Sister's Internship
**Date:** ONGOING
**Title:** My Sister and the Google Internship

I guided my sister through 2 years of JEE prep. She made IIT BHU. She became the only girl from her batch to get a Google internship. 9.2 CGPA. Senior developer at Oracle today. If you understand how someone learns and believe in them before they believe in themselves, you can change their trajectory.

---

### Postcard 12 — Why I'm Still Building
**Date:** MAY 2026
**Title:** Why I'm Still Building

LinkRight isn't done. The CDL project at AmEx is still running. Features from 8 months ago still on the backlog. None of that bothers me. The work that matters is always slightly ahead of where you are. If it's not, you've stopped growing. I've been chasing that edge since I was 11.

---

## SECTION 5: CONTACT (`#contact`)

**Layout:** Centered, full-width section with Surface background. Vertical padding 120px.

```
[Section label]
"WHAT'S NEXT"  — Label style

[Large headline — 48px, weight 800, Text-primary, centered]
Let's build something worth building.

[Body paragraph — 18px, Text-secondary, centered, max-width 520px, margin auto]
I'm currently open to Senior PM and Lead PM roles at companies building
things that matter — in AI, fintech, or anywhere the product problem is
genuinely hard. If that's you, I'd like to hear about it.

[Contact links row — centered, horizontal, 32px gap between]
  [Email button — Accent background, Text-primary, rounded, 48px height, padding 0 28px]
  satvik.jain@iitdalumni.com

  [LinkedIn link — Surface-2 background, Text-secondary, same height]
  LinkedIn ↗

  [GitHub link — Surface-2 background, Text-secondary, same height]
  GitHub ↗

[Small footer line — bottom, Text-muted, 12px]
Satvik Jain · Built with care · 2026
```

Email button: `href="mailto:satvik.jain@iitdalumni.com"`
LinkedIn: `href="https://linkedin.com/in/satvik-jain-iitd"` target="_blank"
GitHub: `href="https://github.com/satvik-jain-iitd"` target="_blank"

---

## NAVIGATION BAR

**Style:** Fixed top, full width, height 60px. Background: `rgba(10, 22, 40, 0.92)` with `backdrop-filter: blur(12px)`. Bottom border: 1px solid `rgba(59, 130, 246, 0.1)`.

**Left:** "SJ" monogram — 16px, weight 800, Accent color.

**Right:** Nav links — "Story · Work · Diary · Contact" — 13px, weight 500, Text-muted. On hover: Text-primary. Active section link (based on scroll position): Accent color.

Smooth scroll behavior on all anchor links. Use JS IntersectionObserver to highlight active nav link.

On mobile (< 768px): Hide nav links. Show only monogram + a hamburger icon that reveals a fullscreen overlay menu.

---

## JAVASCRIPT REQUIREMENTS

1. **Scroll reveal:** All `.reveal` elements animate in (opacity 0→1, translateY 20px→0, 400ms ease-out) when they enter the viewport. Apply class `revealed` via IntersectionObserver.

2. **Pipeline animation:** SVG `<path>` element with `stroke-dasharray` animation using CSS `@keyframes`. A glowing dot (`<circle>`) follows `animateMotion` along the path, looping every 4 seconds.

3. **Case study accordion:** Each card toggles an `.expanded` class on click. The body section animates from `max-height: 0` to `max-height: 600px` with overflow hidden and a 300ms ease transition.

4. **Active nav highlighting:** IntersectionObserver watches each section. When a section is >50% visible, add `active` class to corresponding nav link.

5. **Smooth scroll:** All anchor `href="#section"` links scroll smoothly via `scroll-behavior: smooth` on `html`.

6. **Reduced motion:** All animations check `prefers-reduced-motion: reduce` — if set, skip transitions entirely.

---

## MOBILE RESPONSIVENESS

At < 768px:
- Hero pipeline: stack nodes vertically OR show simplified 2-row version
- Story chapters: reduce font sizes by ~15%, full width
- Case study grid: 1 column
- Diary grid: 1 column
- Nav: hamburger menu
- Stats row: stack vertically

---

## FINAL CHECKLIST (build exactly this)

- [ ] Single HTML file, no external CSS/JS files
- [ ] Google Fonts Inter loaded via `<link>`
- [ ] Dark navy (#0a1628) background throughout
- [ ] All 5 sections present in order
- [ ] Animated pipeline in hero with 5 nodes
- [ ] 5 story chapters with scroll reveal
- [ ] 4 case study accordion cards
- [ ] 12 postcard diary entries in masonry grid
- [ ] Contact section with email/LinkedIn/GitHub links
- [ ] Fixed nav bar with smooth scroll and active state
- [ ] Mobile responsive
- [ ] No Lorem Ipsum — all copy from this prompt verbatim
- [ ] All colors from the design system above — no substitutions

---
*End of prompt.*
