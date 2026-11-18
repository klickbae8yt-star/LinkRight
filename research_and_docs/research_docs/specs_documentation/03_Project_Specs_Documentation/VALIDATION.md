# Validation Rubric

Walk the final output against the user's requirements. The question: can a downstream consumer extract cleanly, with every requirement resolved and every decision committed?

Two passes. Pass 1 is mechanical coverage; Pass 2 is judgment. Severity tracks downstream impact, not fix difficulty.

## Pass 1: Mechanical Coverage

### 1. Requirement Coverage

Extract every user requirement, use case, or stated need from the user's input. Verify each has been addressed in the final output. Missing requirements are critical when they correspond to a stated requirement.

### 2. Token Completeness

Extract every token in the master prompt and every referenced value. Verify each is defined. Critical: tokens referenced but not defined.

### 3. Quality Check Coverage

Verify each of the three mandatory quality checks was applied:
- AI Signal Check: Em dashes, en dashes, complex structures removed
- Copy-Paste Readiness: Correct formatting for target medium (plain text, JSON, CSV, etc.)
- Psychological Safety: Language that triggers skepticism, anxiety, or distrust removed

### 4. Sign-Off Coverage

Verify all three experts provided explicit sign-off (✅). Missing sign-offs are critical.

### 5. Process Compliance

Verify the process followed the defined stages:
- Stage 0: Requirements Discovery complete
- Stage 1: Conceptual Alignment complete
- Stage 2: Execution Refinement complete
- Final: Quality Checks and Sign-Off complete

## Pass 2: Judgment

### 6. Bloat and Overspecification

- Prose where a table or diagram would land harder
- Sections no downstream consumer would read
- Decorative narrative untied to a decision
- Repetition of information already captured elsewhere

### 7. Inheritance Discipline

- Requirements appear verbatim from user input
- Components named consistently across all sections
- References resolve to actual defined tokens
- Task type IDs (M, P, AD, S, AU, O) match across all references

### 8. Shape Fit

- All required sections present (Stage 0-2, Sign-Off, Quality Checks)
- Dropped sections defensible
- Invented sections earn their place (e.g., offline, internationalization, motion)

## Report Shape

Render findings under a Validation Report heading. Group by severity, not by category.

```markdown
## Validation Report

**Overall verdict:** [What's strong, what's broken]

**Category verdicts:**
- Requirement coverage: [verdict]
- Token completeness: [verdict]
- Quality check coverage: [verdict]
- Sign-off coverage: [verdict]
- Process compliance: [verdict]
- Bloat & overspecification: [verdict]
- Inheritance discipline: [verdict]
- Shape fit: [verdict]

### Critical (n)
- [Finding] (location). Fix: [suggestion].

### High (n)
- ...

### Medium (n)
- ...

### Low (n)
- ...

After presenting, offer to roll critical and high findings into a revision pass that updates the master prompt accordingly.

## Severity Definitions

| Severity | Description |
| :--- | :--- |
| **Critical** | Blocking deployment. Fix required before final sign-off. Examples: missing requirement, undefined token, missing sign-off. |
| **High** | Significant risk to user trust or system integrity. Should be addressed before production use. Examples: ambiguous flow, inconsistent naming. |
| **Medium** | Quality of life. Impact on downstream consumers. Examples: bloated prose, missing progress update. |
| **Low** | Polish. Examples: minor clarity issues, stylistic preferences. |
