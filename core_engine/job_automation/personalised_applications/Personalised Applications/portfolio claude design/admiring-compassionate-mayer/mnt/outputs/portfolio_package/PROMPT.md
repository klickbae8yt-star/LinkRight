# PORTFOLIO BUILD PROMPT — SATVIK JAIN
## One-shot instruction for Claude Design. Build exactly this. No improvisation.

---

Build a complete, production-ready, **single HTML file** portfolio website for Satvik Jain, Product Manager. Every word of copy, every color, every layout rule is defined below. Follow exactly.

---

## DESIGN SYSTEM

### Colors
```
Background:       #0a1628   (deep navy)
Surface:          #111f3a   (card backgrounds)
Surface-2:        #1a2f4f   (hover, active states)
Accent:           #0FBEAF   ← LinkRight brand teal (from LinkRight Design System colors_and_type.css)   (LinkRight teal — pipeline, highlights, active states)
Accent-dim:       #0C9A8E   (teal-600 — borders, dimmed accent)
Text-primary:     #f1f5f9   (headlines)
Text-secondary:   #94a3b8   (body copy, dates)
Text-muted:       #475569   (labels, secondary info)
Green:            #10b981   (active/shipped)
Gold:             #E5B80B   (awards, recognition)
Border:           rgba(15,190,175,0.15)
Glow:             rgba(15,190,175,0.6)
```

### Typography
```
Font: Inter from Google Fonts (weights 300,400,500,600,700,800)
Import: <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

H1 name:          64px / weight 800 / tracking -2px / Text-primary
Section labels:   13px / weight 600 / tracking 4px / UPPERCASE / Accent
Chapter titles:   28px / weight 700 / Text-primary
Body:             16px / weight 400 / line-height 1.75 / Text-secondary
Labels/tags:      11px / weight 500 / tracking 1px / UPPERCASE / Text-muted
Stat numbers:     48px / weight 800 / Accent
```

### Layout
```
Max content width: 1100px centered
Section padding:   100px top/bottom
Card radius:       12px
Mobile break:      768px
```

### Animations
```
All transitions:   cubic-bezier(0.4,0,0.2,1) 300ms
Scroll reveal:     opacity 0→1, translateY 20px→0, 400ms (IntersectionObserver)
Pipeline:          animateMotion dot along SVG path, 4s loop
Accordion:         max-height 0→600px, overflow hidden, 300ms
Reduced motion:    prefers-reduced-motion: reduce skips all animation
```

---

## PAGE STRUCTURE

Fixed nav → Hero → Story → Case Studies → Credentials → Build Diary → Contact

---

## NAVIGATION BAR

Fixed top, height 60px, `background: rgba(10,22,40,0.92)`, `backdrop-filter: blur(12px)`, bottom border `1px solid rgba(15,190,175,0.1)`.

Left: "SJ" — 16px weight 800, Accent color.
Right links: Story · Work · Credentials · Diary · Contact — 13px weight 500, Text-muted. Hover = Text-primary. Active section = Accent.
Mobile (<768px): hamburger → fullscreen overlay menu.

---

## SECTION 1: HERO (`#hero`)

Full viewport height. Content centered vertically.

### Pipeline Visualization (SVG, spans ~80% viewport width)

5 nodes left to right, connected by 2px line (Accent at 40% opacity). Animated glowing dot (10px, Accent, `box-shadow: 0 0 12px #0FBEAF`) travels the path on loop (4s, animateMotion).

```
Node 1: "Product Analyst"    2022   circle color: Text-muted
Node 2: "Qatar + Walmart"    2023   circle color: Accent
Node 3: "PM Transition"      2024   circle color: Accent
Node 4: "AmEx Risk PM"       2024–  circle color: Green
Node 5: "Builder"            2025–  circle color: Gold
```

Each node: 16px circle, label below (11px Text-secondary), year below that (10px Text-muted).

### Below pipeline (center-aligned):

```
[H1]
Satvik Jain

[Sub — 20px, Text-secondary, weight 400]
Product Manager · IIT Delhi

[Descriptor — 16px, Text-secondary, max-width 580px, margin auto, line-height 1.8]
I turn messy, ambiguous problems into products people actually use —
by going deep on the data, earning trust with the room,
and shipping before I ask for the title.

[Stats row — 3 items with dividers · centered]
  4+ years        ·    $32M+ shaped    ·    60+ features shipped solo
  [12px Text-muted label below each number]
  "building"           "in deals"           "as sole PM"

[CTA button — Accent bg, Text-primary, 44px height, 24px padding, 8px radius]
See the work ↓   [links to #case-studies]

[Secondary link — text only, 13px, Text-muted, margin-top 12px]
↓ Or read the story first
[links to #story]
```

---

## SECTION 2: THE STORY (`#story`)

Section label: "THE STORY" + 40px Accent underline bar.
Layout: single column, max-width 720px, centered.
Each chapter: fade-in scroll reveal (IntersectionObserver, threshold 0.1).
Between chapters: 72px gap + 1px Border rule.

Chapter structure:
```
[CHAPTER 0X]   — 11px Text-muted uppercase tracking 2px
[Title]        — 28px weight 700 Text-primary
[Body]         — 16px weight 400 line-height 1.85 Text-secondary
               — em tags render in italic, Text-primary color
```

---

### CHAPTER 01 — The Foundation

**Number:** CHAPTER 01
**Title:** The Foundation

My father died when I was 11.

I'm not starting here for sympathy. I'm starting here because it's the most honest explanation for how I operate. When something important breaks, you figure out who's responsible — and you become that person.

My family didn't fall apart. It held. My mother worked. My sister studied. And I watched, very closely, how systems either support people during hard moments or quietly fail them.

That question — *why do some systems work and others collapse* — became the lens I've used to look at every problem since.

---

### CHAPTER 02 — The Theory vs. Practice Problem

**Number:** CHAPTER 02
**Title:** The Theory vs. Practice Problem

IIT Delhi was academically hard for me. I graduated with a 6.43 CGPA in Civil Engineering — not a number I hide.

What I can also tell you: I scored 10/10 in every single practical lab I ever sat in. That gap wasn't about intelligence. It was about how I learn. I don't absorb things from textbooks. I absorb them by doing. When the problem is real and the stakes are present, something shifts.

This pattern has followed me everywhere. The Sprinklr Gold Medal. The AmEx roadmap built from scratch. LinkRight, shipped while holding a full-time job. The fastest I've ever grown is when the problem is slightly too large for me and I have to figure it out on the way.

---

### CHAPTER 03 — The Gold Medal Nobody Saw Coming

**Number:** CHAPTER 03
**Title:** The Gold Medal Nobody Saw Coming

Six months into my first real job, my director put my name on a slide in a global all-hands meeting.

Number one. Out of every product analyst at Sprinklr worldwide. 10/10 customer satisfaction.

I wasn't chasing a medal. I was just trying not to drown in my first enterprise engagement. The award mattered less than what it proved to me: that when I'm in an environment where I can apply what I know *practically*, I operate at a very high level.

What followed was the biggest deal Sprinklr had ever signed — a $32 million engagement with the Government of Qatar. Forty ministries. Citizens interacting with public services. Arabic-language dashboards for the Prime Minister's office. And a Black Friday night at Walmart, pulling live data insights in real time for a room full of VPs.

The best products are built by people who stay in the room when it gets messy, not just when it's clean.

---

### CHAPTER 04 — Solo Ownership

**Number:** CHAPTER 04
**Title:** Solo Ownership

When I joined American Express in 2024, I was the only product manager on my team.

No one above me. An 18-person engineering team that needed direction. A document with 21 requirements and no roadmap.

I spent the first few weeks talking to compliance analysts across 6 global regions — understanding what people actually needed before I touched any plan. By week 6, I had a 3-year roadmap. By week 8, the SVP of Risk Management gave me an award for it. I hadn't shipped a single feature yet.

Then I ran 10 consecutive sprints. Alone. And then, twice in the same year, the strategy changed completely. Both times, the team was watching how I'd respond. Both times, we were back in motion within a week.

The value of a product manager is directly proportional to how fast they can reorient *without losing the team*.

---

### CHAPTER 05 — Building Things That Matter

**Number:** CHAPTER 05
**Title:** Building Things That Matter

LinkRight started as a tool I built for myself. I was running a job search and the AI tools available were making me sound like someone I wasn't. Polished. Inflated. Unrecognizable.

Before writing a single line of code, I spent months talking to 147 people and reaching out to over 7,000 more to understand whether this problem was uniquely mine. It wasn't.

I'm still building it, while holding my AmEx role full-time.

But the thing that means most to me this year isn't a product. It's the colleague who came to stay with me after a layoff. We ran 15 to 20 mock interview sessions together over 3 months. He secured a product role without a single day of unemployment.

Building something is great. Watching someone go from zero confidence to performing at their ceiling is a different kind of impact entirely.

---

## SECTION 3: CASE STUDIES (`#case-studies`)

Section label: "THE WORK"

Layout: 2×3 grid on desktop (3 columns, 2 rows). 1-column on mobile.
Each card: click-to-expand accordion.

Card style: Surface bg, Border border, 12px radius. Hover: Surface-2 bg, border → `rgba(15,190,175,0.4)`. Expanded: left border 3px solid Accent.

Card structure:
```
[TAG]           — 10px uppercase tracking 2px Text-muted
[Project name]  — 22px weight 700 Text-primary
[Summary]       — 14px Text-secondary
[↓ / ↑]        — right-aligned expand toggle, Accent color

--- EXPANDED (smooth height animation) ---
[Problem / What I did / What changed] — bold label + paragraph
Key numbers in expanded body: wrap in <span style="color:#0FBEAF;font-weight:600">
External links: show as small "↗ Source" links in Accent, 12px
```

---

### Card 01 — Qatar ($32M)
**Tag:** ENTERPRISE · $32M
**Name:** Qatar Citizen Experience Platform
**Summary:** Built real-time Arabic dashboards for 40 government ministries.

**EXPANDED:**
*The problem:* Qatar ranked 78th globally on e-government services — behind every Gulf country. The government needed real-time visibility into how citizens felt about interacting with 40 different ministries.

*What I did:* Led the insights product layer for Sprinklr's largest-ever deal. Built Arabic-language dashboards for the Prime Minister's office. Scaled the delivery team from 6 to 14 people and reviewed 120 dashboards in 4 weeks.

*What changed:* Time to insight dropped from **2 days to 2 hours**. Qatar's UN e-government ranking moved from **78th to 53rd** — a 25-position jump.

[Link: "↗ Official press release" → https://www.sprinklr.com/newsroom/the-state-of-qatar-debuts-unified-citizen-experience-management-platform/]

---

### Card 02 — Walmart GenAI
**Tag:** GENAI · ANALYTICS
**Name:** Walmart Spark Driver Root Cause Analysis
**Summary:** Built the system that told Walmart why its gig drivers were quitting.

**EXPANDED:**
*The problem:* Walmart's gig driver platform was losing most of its drivers within 2 months. Over 100,000 monthly support cases. Data scattered across 6 completely different sources with no unified picture.

*What I did:* Designed and built a root cause product that unified all 6 data sources and used machine learning to automatically surface the patterns behind driver churn. Led daily cross-functional work and weekly updates to Walmart's VP of Product.

*What changed:* Time to insight went from **7 days to same-day**. The pilot converted to a **$1.2M deal** with **$9M+ in follow-on pipeline**.

---

### Card 03 — AmEx Risk Platform
**Tag:** FINTECH · SOLO PM
**Name:** American Express Customer Risk Rating Platform
**Summary:** Built the risk scoring platform for 100M+ customer accounts. Alone.

**EXPANDED:**
*The problem:* AmEx needed to rebuild the system that determines the risk profile of every customer — **100 million+ accounts** across **40+ markets**. The platform hadn't been properly updated in years.

*What I did:* Joined as the only PM. Turned a 21-requirement document into a coherent product architecture and 3-year roadmap. Led **10 consecutive sprints** solo, shipped **60+ features**, navigated 2 major strategy pivots, and designed 3 core interfaces from scratch in Figma.

*What changed:* Risk configuration that used to take **10 days now takes 3**. Received the **highest performance rating** among all Band 30 Product Owners in my VP's organization. **120% bonus.**

---

### Card 04 — LinkRight
**Tag:** AI · SOLO BUILD · LIVE
**Name:** LinkRight — Career Navigation Platform
**Summary:** Built an AI system that helps people apply for jobs as themselves.

**EXPANDED:**
*The problem:* AI career tools were helping people sound polished — but not honest. Job seekers were applying as inflated, unrecognizable versions of themselves.

*What I did:* Validated the problem with **147 survey responses** and **7,000+ outreach contacts** before writing any code. Built a career navigation platform solo — AI resume parser, 16-dimension evaluation framework, fabrication guards — while holding a full-time role at AmEx.

*Where it is:* **44 features shipped**, published to PyPI. Still building.

[Link: "↗ pip install linkright" → https://github.com/satvik-jain-iitd]

---

### Card 05 — AutoFlow
**Tag:** AI · AUTOMATION · IN PROGRESS
**Name:** AutoFlow — Automation That Builds Automations
**Summary:** Describe what you want automated. AutoFlow builds it for you.

**EXPANDED:**
*The problem:* Building automations is still too technical for most people. You need to know the tool, think in logic flows, and map triggers before you've even started. Most people give up.

*What I'm building:* An AI-powered system that takes a plain-English description of what you want automated — and generates the workflow. You describe the outcome; AutoFlow designs the logic and builds the steps.

*Why this matters:* Every team wants to automate. Very few people can actually build automations without hand-holding. AutoFlow closes that gap.

*Status:* In active development.

---

### Card 06 — Miraya Media House
**Tag:** AUTOMATION · ADVISORY · IN PROGRESS
**Name:** Miraya Media House — Automation Pipeline
**Summary:** Building the operational backbone for a growing influencer marketing agency.

**EXPANDED:**
*The problem:* Miraya Media House is a growing influencer marketing agency. As campaign volume scales, the operational load grows faster than the team — outreach, tracking, reporting, follow-ups, all manual.

*What I'm doing:* Designing and building their end-to-end automation pipeline as a product advisor — from creator outreach sequences to campaign performance reporting. The goal: let a small team run at 3× the volume.

*Why this:* I've built automation pipelines before and I know how to design them as products — not just scripts that break. Miraya needed someone who could think about the system, not just the tool.

*Status:* In active development.

---

## SECTION 4: CREDENTIALS (`#credentials`)

Section label: "RECOGNITION"
Subtitle (14px Text-muted italic): "The moments that came with paperwork."

Layout: 3-column card row on desktop. Stack on mobile.

Each credential card:
- Surface bg, Border border, 12px radius, 28px padding
- If image file present: show `<img>` at top, 100% width, max-height 180px, object-fit: cover, border-radius 8px
- If image absent: show a styled placeholder div (Surface-2 bg, 180px height, centered icon + credential name)
- Below image: credential name (16px weight 600 Text-primary), issuer (13px Text-muted), date (12px Text-muted)

### Credential 01 — AmEx Leadership Award
**Image file:** `assets/credentials/amex_leadership_award.png`
**Name:** Leadership in Action Award
**Issuer:** American Express · CMRC
**Date:** Q4 2024 · Signed by SVP of Risk
**Detail:** For CRR Engine Modernization — GCIP

### Credential 02 — GGI Fellowship
**Image file:** `assets/credentials/ggi_fellowship_letter.png`
**Name:** GGI Fellow 2024
**Issuer:** Global Governance Initiative · Impact Fellowship
**Date:** 2024
**Detail:** Competitive pre-MBA program. Consulting projects, stress interviews, mentor-led learning.

### Credential 03 — GTI Startup Weekend 1st Place
**Image file:** `assets/credentials/gti_startup_weekend_1st.png`
**Name:** 1st Place — Startup Weekend
**Issuer:** Global Tech Initiative
**Date:** 2024
**Detail:** First place out of all competing teams.

---

## SECTION 5: BUILD DIARY (`#diary`)

Section label: "BUILD DIARY"
Subtitle (14px Text-muted italic): "Not every milestone. The ones that changed something."

Layout: 3-column CSS masonry (columns: 3, column-gap: 20px) on desktop. 2-col tablet. 1-col mobile.

Postcard style: Surface bg, 1px Border border, 12px radius, 24px padding, left border 3px solid `rgba(15,190,175,0.3)`. No hover animation — they should feel like paper.

Structure per card:
```
[DATE]   — 11px Text-muted uppercase tracking 1px
[Title]  — 16px weight 600 Text-primary
[Body]   — 14px line-height 1.7 Text-secondary
```

---

### Postcard 01
**Date:** NOV 2022
**Title:** The Gold Medal Nobody Expected
Six months in, my director put my name on a slide in a global all-hands meeting. Number one globally. 10/10 customer satisfaction. I remember thinking: *maybe I'm better at this than I thought.* That was the first time in years I let myself believe it.

### Postcard 02
**Date:** JAN 2023
**Title:** Midnight in Doha
The Qatar project was 40 ministries, all in Arabic, all live. Four weeks, 120 dashboards, 14 people. The moment I realized the Prime Minister's office would use this to make decisions about citizens — that there was no draft — changed how I approach every project since.

### Postcard 03
**Date:** NOV 2023
**Title:** Walmart, Black Friday, Real-Time
10 VPs watching a live system. The machine was ingesting data automatically. But someone had to translate what it meant in real time — what the driver churn patterns said, what to watch for. I was pulling screenshots and narrating live. No script. That's the part AI won't replace anytime soon.

### Postcard 04
**Date:** FEB 2024
**Title:** The Invite That Changed Everything
Anish Singhal, VP of Product at Sprinklr, scheduled a call with me. He asked if I wanted to join his product team. I'd been running the project like a PM without the title. He saw it. The formal transition happened because the work spoke first. I try to remember that every time I'm tempted to ask for recognition before I've earned it.

### Postcard 05
**Date:** SEP 2024
**Title:** An Award Before I Shipped Anything
Three weeks at AmEx. No roadmap, a 21-requirement document, no structure. I spent my first weeks just listening. By week 6 I had a 3-year roadmap. By week 8 the SVP gave me a Leadership in Action Award. I hadn't shipped a single feature. Clarity, delivered early, is a product.

### Postcard 06
**Date:** OCT 2024
**Title:** GGI Fellowship — Graduated
Completed the GGI Impact Fellowship — a competitive program with stress interviews, consulting-style projects, and mentors from top consulting firms. My Impact Lab project was a digital transformation for Sukha Education, an NGO in Chennai. The consulting toolkit and the PM toolkit are more similar than most people think.

### Postcard 07
**Date:** 2024
**Title:** 1st Place, GTI Startup Weekend
Competed against teams across disciplines. Our team placed first. The experience reinforced something I keep relearning: the best pitch is a crisp problem statement and a solution that's actually simpler than people expect.

### Postcard 08
**Date:** DEC 2024
**Title:** The Week the Strategy Changed
We were weeks from production. The data team couldn't deliver. Leadership paused everything. 18-person team. 18-month build. Paused. I had 3 days to redirect the energy in the room. I turned the pause into a project — mapped the problem from scratch, scoped a solution. That project is still running today. Sometimes the pivot *is* the product.

### Postcard 09
**Date:** JAN 2025
**Title:** Rank 21 of 400 Teams
24-hour hackathon at AmEx. We built a bot that auto-drafts user stories from requirements. Ranked 21st out of 400+ teams. The company later productionized the concept. The best ideas are usually the simplest ones.

### Postcard 10
**Date:** MAR 2025
**Title:** 147 People Said Yes Before Line 1 of Code
I ran a survey before building LinkRight. 147 responses. 7,000+ cold outreach. Every response was some version of: *the tools make me sound like someone I'm not.* That one sentence became the north star. Build the thing that lets people be themselves.

### Postcard 11
**Date:** JUN 2025
**Title:** pip install linkright
First time I ran it and it worked. Quieter than I expected — more like relief than celebration. The thing I'd built alone, across 11 months and 44 features, was now a package anyone could install. That's when I understood why people keep building even when it's hard.

### Postcard 12
**Date:** JUL 2025
**Title:** Zero Days Unemployed
A junior colleague came to stay with me after a layoff. We ran 15–20 mock interview sessions over 3 months. He got a product role without a single day of unemployment. I've shipped a lot of things. That one still means the most.

### Postcard 13
**Date:** 2025–
**Title:** AutoFlow — Building the Builder
I kept running into the same problem: people who wanted to automate things couldn't do it themselves, and couldn't afford someone to do it for them. The tool knowledge is a wall. AutoFlow is my attempt to take that wall down. Still building. The problem is real enough that I can't stop.

### Postcard 14
**Date:** 2026
**Title:** Miraya Media House
Friends run an influencer marketing agency — Miraya Media House. Good at what they do, drowning in ops. I'm building their automation backbone. It's a different kind of PM work — no sprint board, just a real business that needs the chaos removed. I find that just as interesting as anything I've done.

---

## SECTION 6: CONTACT (`#contact`)

Full-width, Surface bg, 120px vertical padding. All centered.

```
[Section label]
WHAT'S NEXT

[Headline — 48px weight 800 Text-primary centered]
Let's build something worth building.

[Body — 18px Text-secondary centered, max-width 520px margin auto]
I'm currently open to Senior PM and Lead PM roles at companies building
things that matter — in AI, fintech, or anywhere the product problem is
genuinely hard. If that's you, I'd like to hear about it.

[Links row — centered, 24px gap, flex-wrap]
  [Email — Accent bg, Text-primary, 48px height, 28px padding, 8px radius]
  satvik.jain@iitdalumni.com
  href="mailto:satvik.jain@iitdalumni.com"

  [LinkedIn — Surface-2 bg, Text-secondary, same height]
  LinkedIn ↗
  href="https://linkedin.com/in/satvik-jain-iitd" target="_blank"

  [GitHub — Surface-2 bg, Text-secondary, same height]
  GitHub ↗
  href="https://github.com/satvik-jain-iitd" target="_blank"

  [AI Songs — Surface-2 bg, Gold color, same height]
  AI Songs ↗
  href="https://drive.google.com/drive/folders/1f8WyRNSA2u6x0BmSugD6U01G9yxWTtj-" target="_blank"

[Footer — 12px Text-muted centered, margin-top 60px]
Satvik Jain · IIT Delhi · Built with care · 2026
```

---

## JAVASCRIPT REQUIREMENTS

1. **Scroll reveal:** `.reveal` class → opacity 0→1 + translateY 20→0, 400ms, IntersectionObserver threshold 0.1. Add `.revealed` class when triggered.

2. **Pipeline animation:** SVG path with CSS `stroke-dasharray` + `stroke-dashoffset` animation. Circle follows `<animateMotion>` along path, 4s duration, `repeatCount="indefinite"`.

3. **Accordion:** Click card → toggle `.expanded` class → animate `max-height` 0↔600px, overflow hidden, 300ms ease. Toggle arrow direction (↓↔↑).

4. **Active nav:** IntersectionObserver on each section, >50% visible → add `.active` to nav link.

5. **Smooth scroll:** `scroll-behavior: smooth` on `html` element.

6. **Reduced motion:** `@media (prefers-reduced-motion: reduce)` — disable all transitions and animations.

7. **Mobile nav:** hamburger (≡) at <768px → fullscreen overlay, `position: fixed`, Surface bg, all nav links stacked. Click anywhere outside or × to close.

---

## MOBILE RESPONSIVE RULES (<768px)

- Hero pipeline: simplify to vertical node list OR 2-column 3-node layout
- Case study grid: 1 column
- Credentials: 1 column stack
- Diary: 1 column (CSS columns:1)
- All font sizes: scale down ~15%
- Stats row: stack vertically, centered
- Contact links: stack vertically, full width

---

## FINAL CHECKLIST

- [ ] Single HTML file, no external CSS/JS
- [ ] Inter from Google Fonts
- [ ] Dark navy (#0a1628) throughout
- [ ] Fixed nav with active scroll states
- [ ] Hero: pipeline SVG + animated dot + name + stats + CTA
- [ ] Story: 5 chapters with scroll reveal
- [ ] Work: 6 accordion cards (Qatar, Walmart, AmEx, LinkRight, AutoFlow, Miraya)
- [ ] Credentials: 3 certificate cards (AmEx award, GGI Fellowship, GTI 1st place)
- [ ] Diary: 14 postcard entries in masonry grid
- [ ] Contact: email/LinkedIn/GitHub/AI Songs links
- [ ] Qatar card links to official Sprinklr press release
- [ ] Mobile responsive at 768px
- [ ] No Lorem Ipsum — all copy from this prompt verbatim
- [ ] Credential images load from `assets/credentials/` folder (graceful placeholder if missing)
