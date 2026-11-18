# linkright-mem — Skill Plan

**Skill:** `/linkright-mem`  
**Version:** 1.0.0 (planned)  
**Build Phase:** Phase 1 — Build First  
**Status:** Not yet built  

---

## 1. What This Skill Does

`linkright-mem` is the memory and profile intelligence engine of the entire Linkright system.

It is responsible for:
- Ingesting raw career material (resumes, LinkedIn exports, diary entries, any career document)
- Extracting and confirming facts with the user
- Building and maintaining the canonical 5-layer memory graph
- Making professional evidence available for all other skills
- Maintaining identity consistency across all career outputs

**Why this must be built first:** Every other skill works from raw pasted text without this. With this, every skill has a clean, confirmed, reusable, traceable evidence base that gets richer over time.

---

## 2. The 5-Layer Memory Architecture

```
LAYER 1: EVIDENCE
Raw source material — original text, unchanged, timestamped
↓
LAYER 2: FACTS
Confirmed factual atoms — specific, grounded, evidence-linked
↓
LAYER 3: SIGNALS
Reusable professional meaning — what the facts say about you
↓
LAYER 4: INTERPRETATIONS
Strategic framing — how to position signals for specific archetypes/opportunities
↓
LAYER 5: EXPRESSIONS
Generated outputs — bullets, stories, posts — cached but NOT canonical truth
```

### Layer Definitions

**Evidence** — Raw source material exactly as provided. A resume PDF, LinkedIn export, diary entry, recruiter email. Never rewritten. Always traceable. Stored as-is with source metadata.

**Facts** — Specific, confirmed atoms of professional truth. Terse, strategically neutral, evidence-linked. Examples:
- `Led onboarding workflow redesign for enterprise clients`
- `Worked cross-functionally with engineering, support, and success teams`
- `Reduced time-to-first-value from 14 days to 6 days (user estimate)`

**Signals** — Reusable professional meaning derived from multiple facts. Examples:
- `systems_thinking` (supported by: onboarding redesign + workflow automation + cross-team coordination)
- `ambiguity_handling` (supported by: defining scope in early-stage role)
- `enterprise_workflow_ownership` (supported by: 3+ enterprise-focused facts)

**Interpretations** — How to frame signals for a specific archetype or opportunity. Context-dependent, evolving. Examples:
- For "AI-native enterprise PM": emphasize workflow automation + systems thinking + data fluency
- For "Growth PM": de-emphasize enterprise depth, bring forward experimentation + funnel thinking

**Expressions** — Generated text. Resume bullets, STAR stories, LinkedIn posts. Cached for reuse. Traced to facts/signals. **Not** canonical — facts are truth, expressions are outputs.

---

## 3. Memory Storage Architecture

**Decision: Hybrid — Structured Markdown + Optional sqlite-vec**

### File Structure

```
memory/
├── facts.md              ← all confirmed facts (YAML blocks)
├── signals.md            ← all derived signals (YAML blocks)
├── outcomes.json         ← application outcomes for adaptive model
├── evidence/
│   ├── resume_<version>.md
│   ├── linkedin_<date>.md
│   └── diary_<date>.md
├── interpretations/
│   ├── archetype_ai_enterprise_pm.md
│   ├── archetype_growth_pm.md
│   └── archetype_<name>.md
├── expressions/
│   ├── bullets/
│   └── stories/
└── vectors/              ← optional, add when >200 facts
    └── facts.db          ← sqlite-vec embeddings
```

### facts.md Schema

```yaml
---
id: FACT_001
text: "Led onboarding workflow redesign for enterprise clients"
role: "Product Manager, [Company]"
period: "2023"
evidence_refs:
  - "resume_2025_v3.md:line_47"
confidence: confirmed       # confirmed | user_estimate | inferred
signals_derived:
  - SIG_001
  - SIG_003
last_updated: "2026-03-10"
---
```

### signals.md Schema

```yaml
---
id: SIG_001
name: "systems_thinking"
label: "Systems Thinking"
description: "Designs and redesigns complex interconnected workflows; sees whole system, not just parts"
supporting_facts:
  - FACT_001
  - FACT_007
  - FACT_012
archetypes:
  - ai_enterprise_pm
  - platform_pm
  - ops_pm
strength: high              # high | medium | low
confidence: confirmed
market_relevance: high
last_updated: "2026-03-10"
---
```

---

## 4. Retrieval System

### Multi-Query Search

When a skill or user queries memory:

```python
def search_memory(query, memory_dir):
    # Step 1: Decompose query into 3-5 sub-queries (LLM)
    sub_queries = decompose(query)
    
    # Step 2: Grep facts.md and signals.md for each
    candidates = []
    for sq in sub_queries:
        candidates += grep(memory_dir + "/facts.md", sq)
        candidates += grep(memory_dir + "/signals.md", sq)
    
    # Step 3: Deduplicate
    candidates = deduplicate(candidates)
    
    # Step 4: LLM rerank by relevance to original query
    ranked = llm_rerank(candidates, original_query=query)
    
    return ranked[:10]
```

### Signal-First Retrieval (for skills that call mem)

When `linkright-sync`, `linkright-interview`, or `linkright-portfolio` requests profile data for a target archetype:

```
1. Load archetype definition from interpretations/archetype_<name>.md
2. Get required signals for that archetype
3. For each required signal:
   a. Find signal in signals.md (strength, supporting facts)
   b. Retrieve supporting facts
   c. Check for cached expressions
4. Return: signals (strength-ranked) + supporting facts + any cached expressions
```

---

## 5. Ingestion Workflows

### Resume / LinkedIn Ingestion

```
STEP 1: Parse input
  → Detect format (PDF text, DOCX, LinkedIn export JSON, plain text)
  → Extract all role/tenure blocks
  → Extract all bullet points / responsibilities / achievements

STEP 2: Generate candidate facts
  → One fact per specific claim
  → Strip superlatives, keep substance
  → Flag any metrics as "user_estimate" if not externally verifiable

STEP 3: Conflict detection
  → Compare against existing facts.md
  → If conflict found: surface BOTH versions with evidence references
  → Ask user to resolve — never silently overwrite

STEP 4: Review
  → Show all candidate facts to user in batches
  → User: confirm / edit / reject each
  → Only confirmed facts persist

STEP 5: Signal derivation
  → From confirmed fact batch: derive candidate signals
  → Group related facts, name the signal
  → Show to user: "These facts suggest this signal. Confirm?"
  → Only confirmed signals persist

STEP 6: Persist + version
  → Write to facts.md and signals.md
  → Tag with source document and date
  → Create memory version snapshot
```

### Diary / Reflection Ingestion

```
INPUT: Free-text work reflection (daily/weekly)
  e.g. "Today I led the design review for the new checkout flow.
        Engineering pushed back on timeline — I resolved it by cutting scope.
        Realized I default to scope cuts over timeline push."

EXTRACTION:
  → New fact candidates: "Led design review for [feature] [date]"
  → Signal evidence: "scope vs timeline trade-off navigation" → supports systems_thinking
  → Potential interview story: "Scope cutting under pressure"
  → Learning log entry

CONFIRMATION:
  → Show fact candidates, ask to confirm
  → Show signal evidence additions, ask to confirm
  → Flag if a story emerged worth banking for interviews
```

---

## 6. Identity Consistency Scoring

The skill computes a coherence score for any target archetype:

```
Given profile signals:
  systems_thinking (high) ✓
  enterprise_workflow_ownership (high) ✓
  stakeholder_leadership (high) ✓
  ambiguity_handling (high) ✓
  ai_workflow_design (medium) ✓
  data_fluency (low) △
  growth_experimentation (low) △

Target archetype: "ai_native_enterprise_pm"

Required signals for this archetype (from KB):
  systems_thinking ✓ STRONG
  workflow_orchestration ✓ MATCH (via enterprise_workflow_ownership)
  ambiguity_handling ✓ STRONG
  ai_native_tooling △ WEAK (ai_workflow_design is medium)
  data_fluency ✗ MISSING

Consistency score: 3/5 fully met, 1/5 partially met, 1/5 missing
Score: 72%

Gap signals: data_fluency (missing), ai_native_tooling (weak)
Recommendation: Find facts in your history that demonstrate data-driven decisions
               or AI tool design/evaluation to address these gaps
```

---

## 7. Constraint Validation

The skill reads `user_setup.md` hard constraints and checks on every ingestion:

```
CONSTRAINT CHECK:
For each confirmed fact, check against user's do_not_mention list and hard_constraints
If violation found: show red flag → "This fact references [X] which is in your
do-not-mention list. Exclude from memory? [Yes/No/Add as private-only]"

Private-only facts:
  → Stored in memory but NEVER surfaced in any output (resume, post, story)
  → Useful for personal context without public exposure risk
```

---

## 8. Skill Gates

### Gate 1 — Detect Intent

```
What do you want to do?
a) Ingest new material (resume, LinkedIn, diary, notes)
b) Search memory
c) Review current profile state
d) Run identity consistency audit
e) Edit or correct a fact/signal
f) Version / snapshot current state
g) Onboard (first-time setup)
```

### Gate 2 — Execute (based on intent)

**Ingest:** Run ingestion workflow above for detected format.  
**Search:** Run multi-query search; return ranked results with evidence refs.  
**Review:** Show fact count by role/period, signal count by archetype, consistency score.  
**Audit:** Check stale facts (>6 months), signals with <2 supporting facts, archetype gaps.  
**Edit:** Create pending diff → show impact → confirm → write.  
**Version:** Tag current memory state with timestamp + optional label.  
**Onboard:** Load user_setup.md → ingest first resume → derive signals → compute first consistency score.

### Gate 3 — Confirmation

Nothing writes to facts.md or signals.md without:
- User sees the diff
- User explicitly confirms
- Source is tagged on every write

---

## 9. Hard Rules

- **NEVER write to facts.md or signals.md without explicit user confirmation**
- **NEVER delete a fact** — only mark as `stale: true` (historical preservation)
- **NEVER let a signal exist with 0 supporting facts** — auto-flag for deletion
- **ALWAYS preserve evidence_refs** so every fact traces to a source
- **ALWAYS surface conflicts** instead of silently overwriting
- **ALWAYS show the diff before any write**
- **ALWAYS tag every write** with timestamp + source document
- **NEVER generate resume/story content in this skill** — that's sync/interview/portfolio

---

## 10. References to Write

| File | Contents |
|---|---|
| `references/ref_01_ingestion_rules.md` | Format parsing rules per document type; what to extract from resumes vs LinkedIn vs diary |
| `references/ref_02_signal_taxonomy.md` | Full signal catalogue (shared with hunt); derivation rules from facts; PM archetype signal maps |
| `references/ref_03_archetype_requirements.md` | 8 PM archetypes; required signals; signal priority weights; consistency scoring logic |

---

## 11. Scripts to Build

| Script | Purpose |
|---|---|
| `scripts/grep_memory.py` | Multi-query grep across facts.md + signals.md |
| `scripts/fact_extractor.py` | Parse resume/LinkedIn/diary text → candidate facts |
| `scripts/signal_deriver.py` | Given confirmed facts → candidate signals |
| `scripts/consistency_scorer.py` | Score profile signals against target archetype |
| `scripts/stale_detector.py` | Find facts/signals older than threshold without refresh |
| `scripts/constraint_checker.py` | Check any text/fact against user_setup.md constraints |

---

## 12. Build Checklist

- [ ] Design facts.md YAML schema
- [ ] Design signals.md YAML schema
- [ ] Create memory/ folder structure template
- [ ] Write ref_01_ingestion_rules.md
- [ ] Write ref_02_signal_taxonomy.md (draw from Research_Linkright KB)
- [ ] Write ref_03_archetype_requirements.md (draw from Research_Linkright KB)
- [ ] Write scripts/fact_extractor.py
- [ ] Write scripts/signal_deriver.py
- [ ] Write scripts/consistency_scorer.py
- [ ] Write SKILL.md (lean orchestrator, <400 lines)
- [ ] Test: ingest a sample resume → confirm facts → derive signals → compute consistency score
- [ ] Test: conflict detection (two versions of same resume)
- [ ] Test: constraint checker against sample user_setup.md

---

## 13. Success Criteria

- All resume bullets traceable to a confirmed fact in facts.md
- Identity consistency score computed correctly for at least 3 target archetypes
- Search returns relevant results in <5 seconds for any query
- Zero facts written without user confirmation
- Conflict detection catches 100% of direct contradictions between documents
- Stale detection flags facts >6 months old that haven't been refreshed
