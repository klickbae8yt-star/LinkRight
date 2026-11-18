# Linkright — User Setup Template

**Fill this once. All skills read from here.**  
**Keep this file private (store in linkright-memory private repo).**  

---

## 1. Identity

```yaml
name: ""
email: ""
linkedin_url: ""
github_username: ""
location_city: ""
location_country: ""
open_to_remote: true/false
mention_location_before_offer: false   # always false unless you want to filter early
```

---

## 2. Compensation

```yaml
current_ctc: ""         # exact number + currency (e.g. "35 LPA", "$120k")
current_ctc_components: ""  # e.g. "28 base + 5 bonus + 2 RSU"
target_ctc_min: ""      # absolute floor — never accept below this
target_ctc_target: ""   # what you're actively asking for
target_ctc_stretch: ""  # if they exceed expectations
currency: "INR/USD/GBP" # pick one
note_on_ctc: ""         # any nuance (e.g. "always quote gross not take-home")
```

---

## 3. Target Role Profile

```yaml
primary_role_type: ""     # e.g. "Senior Product Manager", "Group PM", "Director of Product"
target_archetypes:        # pick 1-2 from: ai_pm, enterprise_pm, growth_pm, platform_pm, 
  - ""                    # consumer_pm, ops_pm, data_pm, founding_pm
  - ""
target_domains:           # e.g. AI/ML, Fintech, SaaS, Consumer, B2B, Platform
  - ""
target_company_stages:    # startup, scaleup, enterprise, faang
  - ""
target_seniority: ""      # IC4 / IC5 / IC6 equivalent, or title-based
timeline_to_offer: ""     # e.g. "within 3 months"
```

---

## 4. Hard Constraints

These are things the skill system should NEVER violate without explicit override.

```yaml
hard_constraints:
  - id: HC_001
    description: ""     # e.g. "Do not include [company X] on resume — moonlighting"
    applies_to: []      # skills this applies to: sync, interview, social, etc.
  
  - id: HC_002
    description: ""
    applies_to: []
  
  # Add as many as needed
```

Common constraint types to consider:
- Work you cannot claim ownership of (someone else's project)
- Companies you cannot mention (moonlighting, NDA, etc.)
- Skills/certifications you cannot claim yet (in progress)
- Personal preferences to withhold until offer stage (location, notice period)
- Stories you shouldn't tell (too risky, not defensible, not yours)

---

## 5. Do Not Mention

Things that should never appear in any output — resume, cover letter, posts, interview answers:

```yaml
do_not_mention:
  companies: []       # e.g. ["company X", "company Y"]
  projects: []        # specific project names
  technologies: []    # e.g. unlaunched internal tools
  personal_info: []   # e.g. ["side business", "location"]
  other: []
```

---

## 6. Current Employer Situation

```yaml
current_employer: ""
current_title: ""
current_notice_period: ""     # e.g. "90 days" / "immediate"
reveal_notice_before_offer: false
currently_employed: true/false
gap_explanation: ""           # if not currently employed
```

---

## 7. Resume Constraints

```yaml
resume_max_pages: 1          # 1 for most PM roles; 2 if >10 years experience
include_education: true
include_certifications: true
certifications_to_exclude: []  # in-progress certs not yet complete
```

---

## 8. Interview Constraints

```yaml
salary_disclosure_strategy: "anchor_high"  # anchor_high | deflect | match_range
salary_opening_line: ""    # fill in your preferred opening line for salary questions

topics_to_avoid_in_interviews:
  - ""    # e.g. "don't mention plans to start own company"

```

---

## 9. Social / Content Constraints

```yaml
topics_to_avoid_in_posts: []
companies_not_to_comment_on: []   # e.g. current employer
max_post_frequency: "3/week"
linkedin_api_connected: false     # set true after OAuth setup
```

---

## 10. Target Companies

```yaml
tier_1_targets:           # dream companies — apply to everything relevant
  - name: ""
    reason: ""

tier_2_targets:           # strong interest — apply selectively
  - name: ""
    reason: ""

tier_3_watchlist:         # track but don't prioritize yet
  - name: ""

companies_to_avoid:       # never apply here
  - name: ""
    reason: ""            # e.g. "bad culture", "burned bridge"
```

---

## 11. Linkright Repo Config

```yaml
github_username: ""
resume_repo: "linkright-resume"
portfolio_repo: "linkright-portfolio"
memory_repo: "linkright-memory"
resume_base_url: ""    # e.g. "https://username.github.io/linkright-resume"
portfolio_base_url: "" # e.g. "https://username.github.io/linkright-portfolio"
```

---

## Setup Checklist

- [ ] Filled compensation section
- [ ] Listed all hard constraints
- [ ] Listed all do-not-mention items
- [ ] Defined target role profile (archetype + domain)
- [ ] Listed tier 1 target companies
- [ ] GitHub repos created and URLs filled in

---

*Once this file is complete, run `/linkright-mem onboard` to load it into your canonical profile.*
