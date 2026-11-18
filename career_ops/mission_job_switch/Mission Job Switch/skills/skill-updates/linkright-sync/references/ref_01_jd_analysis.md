# ref_01 — JD Analysis Protocol

Loaded at Gate 2. Full protocol for extracting signal requirements from a job description.

---

## Step 1 — Archetype Detection

Read the JD and classify into one primary archetype:

| Archetype | Key Indicators in JD |
|---|---|
| **AI PM** | "LLM", "model evaluation", "AI product", "prompt", "inference", "AI/ML roadmap", "foundation models" |
| **Enterprise PM** | "B2B", "enterprise clients", "implementation", "SLAs", "procurement", "stakeholder alignment across orgs" |
| **Growth PM** | "funnel", "conversion", "experimentation", "A/B test", "activation", "retention", "growth metrics" |
| **Platform PM** | "API", "developer experience", "SDK", "platform governance", "internal tools", "infrastructure PM" |
| **Data/Analytics PM** | "data pipelines", "BI", "analytics product", "data contracts", "SQL", "instrumentation", "self-serve analytics" |
| **Consumer PM** | "mobile", "DAU/MAU", "onboarding", "engagement", "viral loops", "consumer UX" |
| **Generalist PM** | Broad scope, no dominant archetype signal |

Note: Some JDs straddle two archetypes (e.g., AI + Enterprise). Flag both.

---

## Step 2 — Signal Extraction

Scan every sentence of the JD. Classify each signal as:

| Priority | Definition | How to identify |
|---|---|---|
| **Primary** | Explicitly required; mentioned 2+ times or in first 3 requirements | "required", "must have", repeated emphasis |
| **Secondary** | Expected but not the core focus; mentioned once in requirements | Listed in requirements, not in headline |
| **Mentioned** | Nice-to-have; appears in "bonus" or "preferred" section | "nice to have", "bonus", "preferred" |
| **Negative** | Explicitly NOT wanted; or signals the role is specifically moving away from | "not a coding role", "not data science" |

### Universal PM Signals (Tier 1)
```
systems_thinking         — "think holistically", "end-to-end", "cross-functional complexity"
ambiguity_handling       — "0-to-1", "undefined problem", "greenfield", "fast-changing"
stakeholder_leadership   — "align stakeholders", "influence without authority", "executive visibility"
execution_rigor          — "ship on time", "delivery track record", "project management"
user_empathy             — "customer research", "user interviews", "voice of customer"
data_fluency             — "data-driven", "metrics", "SQL", "analytics", "experiment design"
communication_clarity    — "write clearly", "present to leadership", "documentation"
```

### Archetype-Specific Signals (Tier 2)
```
AI PM:
  ai_workflow_design       — "design AI-powered features", "prompt systems", "human-in-the-loop"
  model_evaluation         — "evaluate model outputs", "quality metrics", "evals framework"
  ai_trust_ux              — "AI explainability", "user trust", "responsible AI"

Enterprise PM:
  enterprise_workflow_ownership — "own end-to-end implementation", "customer success integration"
  b2b_buyer_psychology     — "champion the deal", "procurement cycle", "IT security review"
  complex_org_navigation   — "multiple stakeholders", "cross-company alignment"

Growth PM:
  growth_experimentation   — "A/B testing", "experimentation platform", "hypothesis-driven"
  funnel_optimization      — "conversion rate", "activation", "retention loops"
  growth_loop_design       — "viral coefficient", "referral mechanics", "network effects"

Platform PM:
  api_design_thinking      — "REST API", "developer API", "versioning strategy"
  developer_experience     — "DX", "developer portal", "SDK", "documentation quality"
  platform_governance      — "breaking changes", "deprecation policy", "internal platform"

Data/Analytics PM:
  data_pipeline_ownership  — "data models", "ETL", "data contracts", "pipeline reliability"
  self_serve_analytics     — "BI tools", "Looker/Tableau", "data democratization"
  instrumentation_design   — "event tracking", "metrics framework", "data quality"
```

---

## Step 3 — Recruiter Language Extraction

Extract 5–10 specific phrases the JD uses that should be mirrored in the resume:

- Look for: unusual verbs, specific methodologies named, company-specific terminology
- These phrases signal that the resume "speaks their language"
- Do NOT mirror generic phrases like "drive results" or "work cross-functionally"

Examples of good mirror phrases:
- "partner with engineering and data science" → use "partner with" not "collaborate with"
- "shape the roadmap" → use "shape" not "build" or "define"
- "hypothesis-driven approach" → use this exact phrase

---

## Step 4 — Red Flag Detection

Flag any of the following in the JD:
- Compensation not listed (for senior roles — means underpaying or uncertainty)
- Role listed under 3+ departments simultaneously (unclear ownership)
- "Wear many hats" at a non-startup (means no support, burnout risk)
- Stack requires very niche expertise that user doesn't have
- "Fast-paced startup environment" in an enterprise company (culture mismatch signal)
- No mention of team size or reporting structure

---

## Output Format

```
ARCHETYPE: [primary] (+ [secondary if applicable])

SIGNAL REQUIREMENTS:
  Primary:    [signal], [signal], [signal]
  Secondary:  [signal], [signal]
  Mentioned:  [signal]
  Negative:   [signal] (avoid emphasizing this)

RECRUITER LANGUAGE TO MIRROR:
  "[phrase 1]", "[phrase 2]", "[phrase 3]", "[phrase 4]", "[phrase 5]"

RED FLAGS:
  [flag or "None detected"]
```
