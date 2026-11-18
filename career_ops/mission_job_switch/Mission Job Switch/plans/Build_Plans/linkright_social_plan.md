# linkright-social — Skill Plan

**Skill:** `/linkright-social`  
**Version:** 1.0.0 (planned)  
**Build Phase:** Phase 3  
**Status:** Not yet built  

---

## 1. What This Skill Does

`linkright-social` creates LinkedIn content that builds professional presence and signals PM expertise to hiring managers at target companies.

It is NOT a "post for engagement" tool.  
It IS a strategic positioning tool.

Every post should do at least one of:
- Signal a specific PM competency to a relevant audience
- Demonstrate proof-of-thinking about real products
- Build recognition in the PM community aligned to your target archetype
- Reinforce the identity narrative your resume tells

**Platform:** LinkedIn only. Other platforms are out of scope.

**Constraint awareness:** The skill reads `user_setup.md` to know what topics, companies, and personal information to never mention in any post.

---

## 2. Voice System

The voice profile is the foundation of every post. Establish this before generating any content. Without it, posts become generic and interchangeable.

### Voice Profile Template

```yaml
TONE:           direct, considered, occasionally contrarian
STYLE:          opinion-first, not question-first
SPECIFICITY:    always names a real product, decision, or tension
LENGTH:         150-300 words standalone; shorter for short-take format
STRUCTURE:      Hook → Tension/Insight → Take → (optional) So what?
FORBIDDEN_OPENINGS:
  - "Excited to share"
  - "Humbled to announce"
  - "Hot take:"
  - "Unpopular opinion:"
  - "Lessons from X years in Y"
  - "I am proud to"
FORBIDDEN_CLOSINGS:
  - "Agree?"
  - "What do you think?"
  - "Drop your thoughts below"
AVOID_PHRASES:
  - "AI is changing everything"
  - "The future of [X] is..."
  - generic industry trend commentary
```

### Voice Rules

**Rule 1: Opinion first.**  
State your view in the first sentence. Let the argument follow.  
Bad: "Here's an interesting question about product prioritization..."  
Good: "Most product roadmaps fail at the same step — not planning, but saying no."

**Rule 2: Specific over generic.**  
Name the company, product, or decision.  
Bad: "Many SaaS companies struggle with onboarding."  
Good: "Notion's onboarding asks too much before showing what's possible."

**Rule 3: Surface the tension.**  
Every good post has two things pulling against each other.  
Examples: speed vs quality, user demand vs business model, simplicity vs flexibility.

**Rule 4: No performance.**  
Don't perform emotions. If you weren't humbled, don't write "humbled." If you weren't inspired, don't write "inspired." Readers detect performed emotions immediately.

**Rule 5: Consistent across all posts.**  
If you could swap an opener from one post into another without it feeling off, they're both too generic.

---

## 3. Post Types

| Type | Purpose | Target Frequency | Length |
|---|---|---|---|
| Proof-of-Thinking (POT) | Demonstrate product thinking about real companies | 2×/month | 200-300 words |
| PM Insight | Share a specific pattern, framework, or lesson | 2×/month | 150-250 words |
| Process Transparency | Show how you think about PM problems | 1×/month | 150-200 words |
| Short Take | Direct 1-3 sentence opinion on industry event or decision | As relevant | 50-100 words |
| Career Milestone | Genuine achievement (sparingly — not "excited to share") | Max 1×/quarter | 100-150 words |

**Avoid:** Engagement-bait polls, "I'm proud to announce" without substance, generic thought leadership listicles, "X things I learned from Y years in PM."

---

## 4. POT Post Format

Same foundation as portfolio POT but compressed for LinkedIn:

```
HOOK (1 sentence):
  A specific observation that's not obvious. 
  e.g. "Anthropic's onboarding makes an unusual design choice for an AI product."

OBSERVATION (2-3 sentences):
  What exactly you noticed — specific and verifiable.

THE TRADE-OFF (2-3 sentences):
  What they were optimizing for. What they gave up.
  Show you understand WHY they made this choice.

YOUR TAKE (2-3 sentences):
  What you'd explore differently, and specifically why.
  Concrete hypothesis, not vague "I think they could improve X"

(Optional) SIGNAL (1 sentence):
  What this reveals about the type of PM problems you think about.
```

**Research requirement:** Use the company's actual product for ≥15 minutes before writing. Reading about it is not enough.

---

## 5. 4-Week Content Calendar Template

| Week | Post Type | Topic/Signal to Feature |
|---|---|---|
| Week 1 | POT | Target company 1 — specific product observation |
| Week 1 | PM Insight | Signal from recent work (systems_thinking, etc.) |
| Week 2 | Short Take | Relevant industry event or announcement |
| Week 2 | Process Transparency | How you approach a specific PM problem type |
| Week 3 | POT | Target company 2 — different signal emphasis |
| Week 3 | PM Insight | Framework or mental model you actually use |
| Week 4 | Short Take | OR Career milestone (if genuinely significant) |
| Week 4 | PM Insight | Pattern recognition post (something you keep seeing) |

**3 posts/week during active job search.** Quality > quantity. One strong POT is worth more than five generic insight posts.

---

## 6. Voice Consistency Scoring

Every post gets scored before delivery:

```
VOICE SCORE RUBRIC (0-2 per criterion):

1. Opens with opinion (not question, not fact, not announcement)    [0-2]
2. References something specific (real company/product/decision)    [0-2]
3. Avoids all forbidden phrases from voice profile                  [0-2]
4. Has a clear position (doesn't hedge everything)                  [0-2]
5. Could only have been written by one person                       [0-2]

TOTAL: /10
THRESHOLD: 7/10 to proceed to user review
BELOW 7: Rewrite automatically, show what changed
```

---

## 7. LinkedIn API Scheduling

For users who want to schedule posts:

**Official LinkedIn Publishing API:**
- Endpoint: `https://api.linkedin.com/v2/ugcPosts`
- Auth: OAuth 2.0 (one-time setup, then persistent token)
- Rate limit: 150 posts/day (more than sufficient)

**Setup (first time):**
1. User creates LinkedIn Developer App (5 minutes)
2. Skill guides through OAuth flow
3. Access token stored in private linkright-memory repo
4. All future scheduling uses stored token

**Optimal posting times** (generalizable heuristics — user should adjust for their audience timezone):
- Early morning local time (catches overnight international engagement)
- Midday local time (peak professional browsing)
- Early evening local time (commute scroll)

**Note:** LinkedIn API is for posting only. NOT for reading, scraping, or any form of data collection. Any reading/scraping is outside API terms and risks account suspension.

---

## 8. Networking via Email (Not LinkedIn DMs)

For cold outreach to hiring managers and PMs at target companies:

**Why email not LinkedIn DMs:**
- Higher response rate (easier to miss in LinkedIn notifications)
- No character limit
- No implied LinkedIn connection request
- Doesn't inflate LinkedIn activity in ways that alert recruiters

**Email strategy:**
1. Find target name from LinkedIn (manual browsing — no automation)
2. Guess email format: `first.last@company.com` or `first@company.com`
3. Verify with Hunter.io free tier (25 lookups/month) or similar
4. Write with linkright-social email mode

**Cold email structure:**
```
SUBJECT: [specific topic] — quick question from a [brief identity signal]

BODY:
Para 1: One specific observation about their work/company/product (not generic praise).
        Shows you did homework.

Para 2: Who you are in one sentence + why their specific work is relevant to you.

Para 3: Specific ask — 20-minute call, one question via email, or advice on X.
        Make it easy to say yes or respond briefly.

No: "I'd love to pick your brain"
No: "I'm a big fan of your company"
Yes: Specificity that shows you know what they actually do
```

---

## 9. Skill Gates

### Gate 1 — Mode Selection

```
What do you want to create?
a) LinkedIn post (specify type)
b) 4-week content calendar
c) Cold outreach email to a person
d) Voice check on a draft I've written
e) Schedule a post via LinkedIn API
f) Brand audit of recent posts
```

### Gate 2 — Input Gathering

**Post:** Ask for topic/target company/signal to feature.  
**Calendar:** Goals, target companies, signals to emphasize this month.  
**Email:** Name, company, role, what you've observed about their work.  
**Voice check:** Paste the draft.

### Gate 3 — Research (if POT or email)

For POT: use web search to research the specific product/feature you're writing about.  
For email: review what this person has posted/published recently.

### Gate 4 — Draft + Voice Check

Write draft. Apply all voice profile rules.  
Run voice score. If <7: rewrite internally, show user the improved version with diff.

### Gate 5 — Constraint Check

Read user_setup.md: `topics_to_avoid_in_posts`, `companies_not_to_comment_on`, `do_not_mention`.  
Flag any violations. Block delivery until resolved.

### Gate 6 — Output / Schedule

If user wants to schedule: generate LinkedIn API call → show to user → on approval, POST.  
If manual: output as clean copy-ready text.

---

## 10. Hard Rules

- **ALWAYS run voice score before showing user any draft**
- **ALWAYS run constraint check** against user_setup.md before delivery
- **NEVER post anything** without user explicit approval
- **NEVER use LinkedIn API for reading or scraping** — posting only
- **NEVER automate any LinkedIn profile/connection/DM interaction**
- **NEVER open a post with a forbidden phrase** from voice profile
- **NEVER end a post with "Agree?" or "What do you think?"**
- **NEVER write generic trend commentary** without a specific, real anchor

---

## 11. References to Write

| File | Contents |
|---|---|
| `references/ref_01_voice_profile.md` | Full voice profile template; forbidden phrases; example post pairs (weak vs strong); voice scoring rubric |
| `references/ref_02_post_templates.md` | Templates for each post type with annotated examples |
| `references/ref_03_pot_library.md` | Archive of published POT posts (starts empty; user grows it) |
| `references/ref_04_linkedin_api.md` | LinkedIn Developer App setup; OAuth flow; posting endpoint; token management |
| `references/ref_05_cold_email_templates.md` | Email templates for: HM cold outreach, referral request, informational interview ask |

---

## 12. Build Checklist

- [ ] Write ref_01_voice_profile.md (voice framework with strong/weak examples)
- [ ] Write ref_02_post_templates.md (all 5 post types with examples)
- [ ] Write ref_03_pot_library.md (empty template with structure for user to populate)
- [ ] Write ref_04_linkedin_api.md (full OAuth + posting setup guide)
- [ ] Write ref_05_cold_email_templates.md
- [ ] Write SKILL.md (lean orchestrator)
- [ ] Build voice scoring script
- [ ] Create first 4-week content calendar from user's profile signals
- [ ] Draft first 3 posts for user review
- [ ] Guide LinkedIn API OAuth setup (one-time)

---

## 13. Success Criteria

- Voice score ≥7/10 on first draft for ≥80% of posts
- 4-week calendar created and executed
- At least 2 POT posts published before first target company interview
- Zero constraint violations in any published post
- LinkedIn API scheduling working (if user opts in)
- At least 1 cold email sent with research-backed opening line
