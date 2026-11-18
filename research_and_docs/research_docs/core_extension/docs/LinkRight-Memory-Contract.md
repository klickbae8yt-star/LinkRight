# LinkRight, Career Memory Contract v1.0

Phase A deliverable. Date 2026-06-05. This is the keystone. It defines the one career memory that every LinkRight tool reads from and writes to. Design only, no code. Every other phase builds against this.

---

## 1. Purpose and role

LinkRight has one source of truth about a person's career. Every tool reads from it, the resume, the interview prep, the LinkedIn content, the job hunt, the companion. Every tool that learns something new writes back to it. The user sets it up once, and from then on nothing is re asked and nothing contradicts.

The memory has three layers, plus the outputs it produces.

Memory, the raw private record. Facts, confirmed statements. Strengths, strategic abstractions. Expressions, the outputs, resume bullets, posts, interview answers, stories, derived from Facts and Strengths, never stored as a fourth layer.

---

## 2. The three layers, and the outputs

Layer 1, Memory. The unfiltered, private, lived record. Diary entries, raw resume and document text, uploaded evidence, reflections, decisions at crossroads. Append only, nothing is ever deleted. Private by default. This is the ground truth that everything else traces back to.

Layer 2, Facts. Atomic, confirmed statements derived from Memory. One claim each. Every Fact carries the Memory items it came from, a confidence level, and a credibility tag. A Fact is the smallest unit a resume or an answer can safely stand on.

Layer 3, Strengths. Strategic abstractions derived from Facts. A Strength is a professional theme the Facts add up to, for example ownership before the title, or data fluency. Each Strength names the Facts that back it. Strengths are what a reader actually cares about, and what positioning and content lean on.

Expressions, the outputs. The resume, the cover letter, the LinkedIn post, the interview answer, the STAR story. Generated on demand from Facts and Strengths, and traceable back to the Facts they used. Never invented beyond what the Facts support.

---

## 3. Data shapes

Storage agnostic. These shapes can live as markdown, JSONL, or a database row, as long as the fields hold.

Memory item.
- id
- type, one of diary, document, evidence, reflection, decision
- content, the raw text
- source, where it came from, an upload, an interview, a diary entry
- date
- private, true or false, default true
- created_at

Fact.
- id
- statement, one atomic claim
- evidence_ids, the Memory items that back it
- confidence, one of exact, strong, directional, thin
- credibility, one of confirmed, correction, supporting_role_only, do_not_use
- user_confirmed, true or false
- tags
- created_at, updated_at

Strength.
- id
- name, the strategic theme
- summary, one or two lines
- fact_ids, the Facts that support it
- tags
- created_at, updated_at

Expression.
- id
- kind, one of resume_bullet, cover_letter, post, interview_answer, story
- text, the produced output
- fact_ids, the Facts it draws on
- strength_ids, the Strengths it leans on
- target, the role, company, or post type it was made for
- created_at

---

## 4. Provenance and credibility, the truth engine

This is the moat. No claim ships without backing.

Every Fact links to the Memory it came from. Every Expression links to the Facts it used. A reader, or the user, can always trace a resume bullet back to a confirmed Fact and to the raw Memory behind it.

Confidence levels. Exact, a hard number or a verified detail. Strong, well supported but not exact. Directional, a reasonable estimate, often from someone else's report. Thin, weak, flagged, not used in a final output unless the user upgrades it.

Credibility tags. Confirmed, true and owned by the user. Correction, a fix that overrides an older or inflated claim. Supporting_role_only, real but the user supported, did not own it, so it must not be framed as owned. Do_not_use, never put this in any output, for example a title that was announced but never held.

The rule. An Expression may only use Facts that are user_confirmed and not tagged do_not_use, and it must respect supporting_role_only framing. A synthesized or illustrative number is allowed only where history is thin, must be marked, and must be locked so it never contradicts a later output.

---

## 5. Privacy model

Layer 1 Memory is private by default and never leaves the user's own store. The vault is a private repo.

Sensitive Memory, personal hardship, health, salary, private conflict, carries a private marker and is never surfaced into an Expression, even when a Fact derived from it is used. The Fact can be used, the raw private detail behind it stays hidden.

Only Expressions are ever shown outside, and only after the per post or per resume gates pass. Facts and Strengths are internal working layers. Memory is never public.

---

## 6. Read and write rules

Who writes what. Onboarding and the diary feed Memory. An extraction step reads Memory and proposes Facts. The user confirms or corrects each Fact before it is trusted, this is the truth engine loop. A second step rolls confirmed Facts up into Strengths. Expressions are produced on demand by the resume, content, and interview tools.

Append only Memory. Memory is never overwritten, corrections are added as new items and as Correction tagged Facts, so history is preserved.

Confirmation before commit. The vault is git backed. No write to Facts or Strengths is committed silently, the user sees a diff and confirms, matching how linkright-memory already works.

One writer per layer at a time. To avoid conflicts, a given run writes one layer, it does not edit Memory and Strengths in the same pass.

---

## 7. The retrieval interface, claude-mem inspired

Tools do not load the whole memory into context. They ask for what they need.

A query takes a task context, for example a job description, an interview question, or a content topic, and a target depth, Facts, Strengths, or Stories. It returns a small set of the most relevant items, in a tight form, each with its id for citation.

Retrieval is hybrid, semantic plus keyword, so it catches both meaning and exact terms. It is progressive, it returns the least context that answers the task, and it can go deeper on request, down to raw Memory for a deep dive.

The same interface serves two corpora, the per user Career Memory, and the generic engine knowledge base. One retrieval primitive, two sources.

---

## 8. Knowledge loading, must follow versus situational

This governs how engine knowledge, not just memory, reaches an agent.

Must follow, always loaded. The hard gates, the scoring thresholds, the voice core, the config. Small, deterministic, always relevant. Loaded directly, never through retrieval, so a missed query can never drop a rule.

Situational, retrieved. The large reference, post types, psychology, algorithm mechanics, design principles, the bullet bank. Fetched on demand by sharp queries through the retrieval interface in section 7.

Config schema. In each agent config, dependencies.knowledge splits into two lists.
- knowledge.always, files loaded directly every run.
- knowledge.retrieve, sources queried at run time and pulled in as tight, cited snippets.

This lets the knowledge base grow without limit while the context per run stays tight.

---

## 9. What each consumer reads

| Tool | Reads from the memory |
|---|---|
| Resume, sync | Facts and Strengths, plus do_not_use and supporting_role_only constraints |
| Cover letter | Facts and Strengths, plus the target role |
| Interview, coach | Stories and the Facts behind them, plus credibility tags |
| Content, network | Strengths, the voice profile, and supporting Facts |
| Job hunt | Strengths and Facts for matching against roles |
| Companion | Pipeline state plus recent Facts and decisions |

Every one of them reads through the retrieval interface, not by loading the whole vault.

---

## 10. Storage, one contract, adapters per surface

The contract defines shapes and rules, not a database. Each surface keeps its own store but conforms to these shapes.
- CLI and the Cowork skills, markdown and JSONL in ~/.linkright, the linkright-memory vault.
- Web app, its own database, the same Memory, Facts, Strengths shapes.

Because the shapes match, a Fact written by the CLI and a Fact written by the web app mean the same thing, and the retrieval behaves the same everywhere.

---

## 11. Naming reconciliation

This contract unifies the names that exist today.
- The CLI's Evidence, Fact, Signal become Memory, Facts, Strengths.
- The content project's the real, the tell, the write become Memory, Facts, Strengths plus Expressions.
- The vault's facts.md stays Facts, signals.md becomes Strengths, expressions and stories stay Expressions.
- The old graph, nuggets, and atoms are retired into this model.

One vocabulary everywhere, Memory, Facts, Strengths, Expressions.

---

## 12. In scope and out of scope

In scope, the shapes, the rules, the credibility and privacy model, the retrieval interface, and the knowledge split. This is the contract every tool honours.

Out of scope for Phase A, the actual code, the embedding model choice, the exact file layout, and the migration of existing data. Those come in Phase D, when the retrieval layer is built, and they must conform to this contract.

Done when, the shapes, rules, and interfaces here are agreed, so every later phase has a firm thing to build against.
