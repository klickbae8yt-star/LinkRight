# FileOS — M0 & M1 Implementation Specification

**Planning baseline:** 11 November 2026  
**Product decisions:** Balanced prioritisation; personal users first; cloud-first AI; local-first file storage; selective AI invocation.  
**Scope:** M0 Baseline Freeze and M1 Data Integrity. This document is both the milestone specification and the implementation contract for the coding agent.

---

## 1. Locked product direction

| Decision | Locked direction | Practical consequence |
|---|---|---|
| Prioritisation | Balanced | Correctness, user experience and intelligence all matter; do not optimise only for engineering metrics. |
| First release audience | Individual/personal users | Single-user setup, approachable language, simple controls and no team-workflow complexity in the first release. |
| AI execution | Cloud-first | The first actual AI provider will be a cloud provider, not a local model. |
| File storage | Local-first | Original files, primary scan reports and the initial intelligence index remain on the user's machine. |
| AI invocation | Selective | Deterministic methods run first; cloud inference is reserved for genuinely ambiguous cases. |
| Privacy | Privacy-first | Explicit opt-in, minimum necessary excerpts, folder exclusions, visible usage and no silent uploads. |
| Commercial direction | SaaS-ready, not SaaS-now | Do not build accounts, billing, multi-tenancy or cloud sync in M0/M1. Avoid coupling core logic to a future license model. |

### Important architecture distinction

**Cloud AI does not mean cloud file management.** The intended first release is a local personal file-management product that may send a bounded, user-authorized excerpt and minimum contextual evidence to a cloud model for a specific ambiguous decision. Do not upload whole directories, entire file collections, or original binaries by default.

M0 and M1 must not introduce live cloud model calls. They should document the future cloud-first boundary and make AI usage accounting truthful. Actual cloud inference belongs to a later, explicitly approved milestone after the user-facing privacy and consent experience exists.

---

## 2. Current baseline supplied for this plan

The latest system overview describes:

- A Python-standard-library implementation with `fileos.py`, `dashboard.py` and `audit.py` (approximately 3,566 lines total).
- 41 tests across seven test files, reported passing.
- Seven CLI commands: `scan`, `plan`, `report`, `apply`, `undo`, `audit`, `dashboard`.
- Recursive iterative DFS traversal, configurable depth, exclusion rules and optional symlink following.
- Local report artefacts including `coverage.json`, `inventory.jsonl`, `folders.jsonl`, duplicate groups, document families, hierarchy anomalies, proposed actions, AI usage, summary, operation journal and review decisions.
- Twelve deterministic audit checks.
- A localhost dashboard described as having nine tabs and APIs for findings, coverage, history, audit, decisions and text diff.
- Two real scan reports described as passing 12/12 audit checks: LinkRight and Google career.

These are **reported baseline facts**, not independent verification by this specification's author. The coding agent must inspect the actual workspace and current reports before changing anything. If code, tests or report outputs differ from this baseline, record the discrepancy; do not silently make the documentation match an assumption.

---

# Part A — M0: Baseline Freeze and Reproducibility

## 3. M0 objective

Create a reproducible, documented and recoverable baseline of the currently working FileOS implementation. M0 is primarily an inspection, inventory, documentation and fixture milestone. It is not a broad refactor.

**M0 outcome:** Any future agent or developer can identify the exact starting state, run the same tests, understand the output contracts, reproduce known behaviours with synthetic fixtures and compare later changes against the baseline.

## 4. M0 workstreams

| ID | Workstream | Required work | Deliverable |
|---|---|---|---|
| M0.1 | Workspace inspection | Inspect the skill directory, scripts, tests, references, examples and current install path. Identify duplicate or divergent installed copies. | `BASELINE_INVENTORY.md` |
| M0.2 | Repository safety | Inspect Git status and current branch if Git is present. Do not discard, overwrite or reset user changes. Create a local baseline branch/tag only if safe and appropriate; never push. If Git is absent, document that fact and use a non-destructive backup strategy approved by the environment. | Baseline revision or documented fallback |
| M0.3 | Runtime record | Record OS, Python version, invocation commands, dependency policy, test command and relevant environment assumptions. | Runtime section in `BASELINE_INVENTORY.md` |
| M0.4 | Test baseline | Run the full existing suite before changes. Record exact command, number passed/failed/skipped, duration and output. | `MILESTONE_STATUS.md` baseline entry |
| M0.5 | Output contract inventory | Document each report file, record key, ID format, required fields, producer, consumer and whether it is append-only or regenerated. | `references/OUTPUT_SCHEMA.md` updated or reconciled |
| M0.6 | CLI and data-flow inventory | Document all seven CLI commands, input/output paths, side effects and safety gates. Verify actual behaviour against source code. | `references/ARCHITECTURE.md` |
| M0.7 | Golden synthetic fixtures | Create small synthetic fixture trees for known cases. Do not use personal document contents as fixtures. | `tests/fixtures/` and fixture expectations |
| M0.8 | Architecture decisions | Record local-first storage, cloud-first AI provider direction, selective AI, privacy boundary and deferred SaaS features. | `references/ARCHITECTURE_DECISIONS.md` |
| M0.9 | Roadmap hygiene | Create or update roadmap, milestone status and changelog without claiming unbuilt capabilities. | `ROADMAP.md`, `MILESTONE_STATUS.md`, `CHANGELOG.md` |

## 5. M0 golden fixture set

Create deterministic, tiny temporary directory structures. Fixtures must be synthetic and safe to recreate.

| Fixture | Example | Expected baseline behaviour |
|---|---|---|
| Exact duplicate | Same bytes, different names and paths | One exact duplicate group with correct members |
| Renamed duplicate | Same bytes, unrelated filenames | Detected by hash, independent of filename |
| Different content, same name | Same filename, different bytes | Not classified as exact duplicate |
| Version tokens | `Plan_v1`, `Plan_v2`, `Plan_final` | Current version-family behaviour recorded, including limitations |
| Branch-like versions | `Plan_internal`, `Plan_client` | Do not assume linear supersession solely from names |
| Nested hierarchy | Root/Project/Folder/File at 12+ levels | Every permitted level is visited |
| Parent mismatch | File fits child folder, child conflicts with parent | Separate edges are represented independently |
| Mixed folder | One folder contains two unrelated synthetic topics | Folder is flagged for review; do not recommend blindly moving the whole folder |
| Empty folder | Directory with no files | Directory is counted and classified without inventing content |
| Hidden file | Dotfile in a scanned folder | Behaviour matches the documented hidden-file policy |
| Excluded subtree | A folder excluded by rule | Exclusion is visible; descendants are not fabricated as discovered files |
| Symlink cases | File link, directory link, broken link, loop | Behaviour matches configured policy and is clearly counted |
| Unstable file | `.part` or `.crdownload` | Not processed as a stable complete file |
| Inaccessible path | Permission-denied simulation where supported | Reported with a reason; scan does not falsely claim complete coverage |
| Unicode and long names | Unicode path and nested path | No crash or silent path corruption |
| Destination collision | Existing target path | Apply is blocked or follows documented safe conflict behaviour |
| File changes during scan | File changes between stat and read | File is marked unstable/changed; no misleading hash is recorded |

Every fixture must have an expected-results manifest. The manifest must specify counts and statuses, not just “test passes”.

## 6. M0 acceptance criteria

M0 is complete only when all conditions below are met:

1. The agent has inspected the actual active workspace and global skill installation and documented any divergence.
2. The pre-change test baseline is recorded exactly. The target is the reported 41/41, but if the actual result differs, the milestone records the true value and investigates before proceeding.
3. Existing source code and user data are preserved. No destructive Git operation, source-file operation or production apply action is performed.
4. The CLI, report artefacts, schemas, IDs, side effects and data flow are documented from code, not guessed.
5. Golden synthetic fixtures and expected-results manifests exist for the cases in Section 5, with platform-dependent cases explicitly marked.
6. The roadmap and milestone status clearly distinguish built, partial, not built and unverified capabilities.
7. The future cloud-first AI boundary is documented without adding live network calls.
8. All existing tests still pass after M0 documentation/fixture changes.

**M0 non-goals:** No core-engine refactor, no new AI provider, no cloud upload, no dashboard redesign, no automatic file movement, no large new feature and no SaaS backend.

---

# Part B — M1: Data Integrity, Scan Identity and Stale-State Protection

## 7. M1 objective

Make every scan result mathematically reconcilable, every finding traceable to evidence, and every plan/review decision tied to the exact scan state from which it was created.

M1 is not about adding more intelligence. It is about establishing that FileOS can reliably explain **what it saw, what it could not inspect, what it calculated and which evidence supports each conclusion**.

## 8. M1.1 — Define unambiguous inventory accounting

The current audit checks refer to discovered, analysed, skipped, failed, eligible and coverage counts. M1 must define these terms precisely and ensure that counters do not overlap.

Use explicit definitions and document them in the output schema. Recommended accounting model:

### Files

| Metric | Definition |
|---|---|
| `file_entries_observed` | Regular-file entries actually encountered while enumerating directories that FileOS was permitted to traverse. |
| `files_excluded` | Observed file entries intentionally excluded by a configured file-level rule. |
| `files_eligible` | `file_entries_observed - files_excluded`. These are candidates for normal analysis. |
| `files_analysed` | Eligible files for which the core inventory operation completed and a valid inventory record was written. This does not imply every content parser supports the format. |
| `files_skipped` | Eligible files deliberately not analysed, with a specific reason such as unstable, policy skip or unsupported core operation. |
| `files_failed` | Eligible files for which an attempted core operation failed unexpectedly. |
| `files_partial_content` | Analysed files whose metadata/hash succeeded but whose optional content extraction was incomplete or unsupported. This is a quality attribute, not an additional mutually exclusive terminal count. |

Required invariants:

- `file_entries_observed = files_excluded + files_eligible`
- `files_eligible = files_analysed + files_skipped + files_failed`
- Each eligible file has exactly one terminal core-analysis status.
- Content-extraction status is tracked separately and must not double-count a file in the core accounting equation.
- Files inside a directory subtree that was excluded before traversal are **unknown/unobserved**, not discovered files. Do not estimate or fabricate their count.

If the existing model cannot safely adopt these exact field names, preserve compatibility through a versioned schema and explicit mapping. Do not silently redefine old fields.

### Directories

| Metric | Definition |
|---|---|
| `directories_observed` | Real directory nodes observed, including the scan root exactly once according to a documented convention. |
| `directories_scanned` | Directories whose entries were successfully enumerated. |
| `directories_excluded` | Directories intentionally excluded by policy before descent. |
| `directories_inaccessible` | Directories that could not be enumerated due to permissions or I/O errors. |
| `directories_depth_skipped` | Directories intentionally not descended into because of an explicit depth cap. |

Required invariant:

- `directories_observed = directories_scanned + directories_excluded + directories_inaccessible + directories_depth_skipped`
- Each observed real directory has exactly one terminal traversal status.
- If a directory is only partially enumerated before an I/O failure, its status and observed child entries must be represented without double-counting. Document the exact policy.

### Other filesystem entries

Track symlinks and non-file/non-directory entries separately. Do not force symlinks into file or directory totals. Where symlinks are not followed, record their count and reason. Where they are followed, record link identity and target traversal while preventing loops and duplicate traversal.

### Coverage semantics

Coverage must disclose:

- The root path and scan configuration.
- Directories visited and excluded.
- Known files analysed, skipped and failed.
- Symlinks and non-regular entries.
- Depth limits and inaccessible paths.
- Descendants hidden behind excluded or inaccessible subtrees as unknown, not zero.

A scan is `complete` only when the configured scan scope was fully traversed and all relevant items meet the declared completion policy. A scan may be `successful but partial`; do not collapse success and completeness into one boolean.

## 9. M1.2 — Make byte and duplicate-storage metrics truthful

The report must distinguish the following metrics:

| Metric | Meaning |
|---|---|
| `eligible_file_bytes` | Sum of observed sizes for eligible regular files, using a documented stat snapshot. |
| `bytes_read_for_hashing` | Actual bytes read from storage for hashing during this scan. |
| `bytes_reused_from_hash_cache` | Bytes represented by reused hashes; these bytes were not read again during this scan. |
| `duplicate_group_count` | Number of exact duplicate groups. |
| `duplicate_member_file_count` | Total file instances across those groups. |
| `duplicate_group_logical_bytes` | Sum of sizes of every member in every exact duplicate group. |
| `potential_extra_copy_bytes` | For each group, sum of all member sizes except one retained copy, using verified identical content and stable sizes. |

Rules:

- Never label `duplicate_group_count` as duplicate file count.
- Never label logical duplicate bytes as reclaimable savings.
- Describe extra-copy bytes as a theoretical storage opportunity, not an instruction or guarantee to delete.
- Explain whether hashes were computed, reused, or unavailable.
- A hash is valid only for a stable file snapshot. Record size/mtime or equivalent before and after reading; if the file changes, invalidate the hash result and mark the file unstable/changed.
- Audit math independently from the production calculation where practical.

## 10. M1.3 — Scan identity and configuration fingerprint

Every scan must have a unique `scan_id` and a deterministic `scan_config_fingerprint`.

The fingerprint should cover analysis-affecting configuration, including:

- Canonical scan root identity.
- Exclusion and inclusion rules.
- Maximum depth.
- Symlink policy.
- Hash algorithm and relevant hashing options.
- Supported parser/extractor version or capability-set version.
- Relevant FileOS engine/schema version.

Do not include secrets, API keys or user file contents in the configuration fingerprint. Avoid exposing unnecessary absolute paths in any future cloud payload.

Each generated report and each finding must be traceable to `scan_id` and schema version. A scan ID identifies one run; the configuration fingerprint identifies the settings that shaped it. These are not interchangeable.

## 11. M1.4 — Plan freshness and action preconditions

Every plan must record:

- `plan_id`.
- `source_scan_id`.
- `source_scan_config_fingerprint`.
- A stable digest or reference to the evidence used by each action.
- Source file path and expected identity/fingerprint.
- Proposed destination and relevant destination preconditions.
- Generation timestamp and action schema version.

Before `apply` executes any approved action, it must revalidate at least:

1. The plan schema is supported.
2. The source scan and evidence references exist.
3. The source still exists at the expected location.
4. The source still matches its expected hash or other declared identity check.
5. The destination state has not unexpectedly changed.
6. The action is still explicitly approved by its exact action ID.
7. No protected, signed, authoritative or user-protected file is being moved contrary to policy.

A failed precondition must block that action with a clear explanation. Never silently recalculate or broaden the user's approval.

M1 does not add a general-purpose batch rollback feature; that remains a later safe-automation milestone. Preserve the existing journal and undo behaviour.

## 12. M1.5 — Review decision freshness

Every review decision must link to:

- `decision_id`.
- `finding_id`.
- `scan_id`.
- A stable `finding_fingerprint` based on the finding's identity and supporting evidence.
- Choice, optional note and timestamp.

On a new scan:

- If the finding and evidence are unchanged, show that the earlier decision is associated with a previous scan and may be reusable only under an explicit compatibility rule.
- If evidence, source fingerprint, relationship, path or relevant configuration changed, mark the old decision as stale.
- If the finding disappeared, mark the decision as no longer applicable rather than deleting its history.
- Never silently carry an approval to a different or materially changed action.

The dashboard must distinguish current-scan decisions from historical decisions. Preserve append-only history.

## 13. M1.6 — Evidence traceability

Every finding and proposed action must have machine-verifiable evidence references.

| Finding type | Minimum evidence |
|---|---|
| Exact duplicate | Member paths/IDs, same SHA-256, sizes, stable-read status |
| Document family | Member paths/IDs, normalized stems, version tokens and similarity basis used |
| Hierarchy anomaly | Exact parent-child edge, child and parent folder IDs, fit signals/scores and reason flags |
| Proposed move | Source, destination, originating finding IDs, supporting evidence and safety preconditions |
| Skipped/failed item | Path or safe display identifier, reason code, operation stage and recoverability |

The dashboard must be able to resolve each evidence reference. Audit must fail if a finding refers to missing or mismatched evidence.

## 14. M1.7 — AI usage ledger truthfulness (no live AI yet)

M1 must prepare accurate accounting without implementing cloud inference.

Track distinct states such as:

- `candidate_created`
- `queued`
- `not_sent`
- `sent`
- `succeeded`
- `failed`
- `cached`
- `skipped_by_policy`

Required rules:

- A queued packet is not a model call.
- Characters are not tokens. Never estimate tokens from character counts unless explicitly labelled as an estimate and never report it as actual provider usage.
- Actual request counts, provider usage and billed usage must come from provider responses once a provider exists.
- In M0/M1, expected external network/model calls are exactly zero.
- Add a test that fails if scan, plan, audit or dashboard makes an unexpected network request.

Do not add an unused cloud SDK dependency or send real content to an AI provider during these milestones.

## 15. M1.8 — Auditor updates

Review all twelve existing checks. Preserve their IDs where possible, but refine definitions and add checks only when needed. At minimum, ensure coverage for:

1. File accounting reconciliation.
2. Directory accounting reconciliation.
3. Symlink/non-regular-entry accounting.
4. Duplicate group membership validity.
5. Duplicate hash consistency.
6. Duplicate storage arithmetic.
7. Hash read/cache/duplicate-byte metric consistency.
8. AI ledger state consistency and no-call distinction.
9. Unique IDs and evidence reference integrity.
10. Plan/action status and journal consistency.
11. Scan completeness/partial status consistency.
12. Source sample existence and freshness.
13. Scan ID and configuration fingerprint integrity.
14. Plan source-scan linkage and action precondition integrity.
15. Review decision scan/finding linkage and stale-state classification.

If new checks are added, update the documented total and tests. Do not claim `12/12` if the suite has become 15 checks; report `15/15` or the true result. Historical reports must retain their original auditor/schema version and remain readable where feasible.

## 16. M1 test requirements

Add or extend tests for:

- File accounting with normal files, exclusions, unstable items, failures and unsupported extraction.
- Directory accounting with root inclusion, excluded subtrees, inaccessible folders and explicit depth limits.
- Symlink file, symlink directory, broken symlink, symlink loop and follow/no-follow modes.
- A directory excluded before traversal: descendants remain unknown, not counted as observed.
- File mutation during hashing: no trusted hash is emitted.
- Byte metrics: actual bytes read, cache reuse, group logical bytes and extra-copy bytes.
- Duplicate group count versus member count distinction.
- Scan ID uniqueness and configuration fingerprint stability/change behaviour.
- Same input/configuration producing stable substantive outputs despite a different scan ID or timestamp.
- Plan invalidation after source modification, rename, deletion or destination collision.
- Review decision stale-state behaviour after a new scan.
- Evidence references resolving to the right source records.
- AI queue count versus actual model-call count; zero external calls in M1.
- Dry-run immutability for source files and directories.
- Existing apply/undo protections remain intact.
- Old report compatibility or a documented migration/read-only policy.

All tests must use temporary synthetic fixtures. Tests must never move, rename, overwrite or delete the user's real workspace files.

## 17. M1 real-report validation

When the report directories still exist and are accessible, validate the current LinkRight and Google career reports against the new accounting model.

Known paths from the supplied system overview include:

- `/private/tmp/fileos-scan-linkright-v2`
- `/private/tmp/fileos-output-googlecareer`

Do not assume either path still exists. Check before use. Validation must be read-only. If the report schema predates M1, run a compatibility audit and state which checks cannot be evaluated from historical artefacts. Do not rewrite old reports in place.

The agent must report:

- Audit results for each report.
- File and directory accounting equations with actual operands.
- Unobserved/excluded subtree handling.
- Duplicate byte arithmetic with at least one independently recomputed sample.
- Stale plan/review decisions found, if any.
- Any metric that cannot be verified from report artefacts.

Never run `apply` as part of M1 validation.

## 18. M1 acceptance criteria

M1 is complete only when:

1. File and directory accounting equations reconcile exactly for every synthetic test fixture.
2. Every observed eligible file and directory has exactly one terminal status under the documented policy.
3. Excluded/untraversed descendants are reported as unknown, not fabricated as zero or discovered.
4. Byte and duplicate-storage metrics have clear, independently testable definitions.
5. File mutation during hashing cannot produce a trusted stale hash.
6. Every scan has a scan ID and configuration fingerprint.
7. Every plan is linked to a source scan and revalidates action preconditions before apply.
8. Review decisions are scan-aware and stale decisions are visibly distinguished.
9. Every finding/action evidence reference resolves; broken references fail audit.
10. AI queue, actual model calls, characters and actual tokens are distinct; no external model calls occur in M1.
11. All existing tests pass and new M1 tests pass.
12. Existing real reports are validated where accessible, with historical-schema limitations explicitly reported.
13. Scan, plan, report, audit and dashboard remain source-read-only; apply remains exact-ID approval-gated.
14. `MILESTONE_STATUS.md` contains measured before/after results and no unsupported completion claims.

**M1 non-goals:** Near-duplicate AI analysis, semantic search, full-text extraction, OCR, live cloud AI, local AI, subscriptions, SaaS backend, incremental scan/watch mode, new automatic move recommendations, bulk file operations or full dashboard redesign.

---

# Part C — Cross-milestone engineering contract

## 19. Balanced prioritisation rule

Every milestone should include work in these three dimensions where relevant:

| Dimension | Question | Minimum evidence |
|---|---|---|
| Correctness | Is the result technically and mathematically defensible? | Tests, invariants, audit results and evidence traceability |
| User experience | Can a personal user understand what happened and what to do? | Plain-language messages, clear statuses and no misleading labels |
| Intelligence | Does the feature add useful context without overclaiming? | Explicit confidence/limitations and deterministic-vs-AI boundary |

Do not add an advanced intelligence feature if its evidence cannot be explained in the UI. Do not sacrifice accounting correctness for a richer dashboard. Do not add friction without a user-safety reason.

## 20. Low-token development rules for Antigravity

- Read the relevant files and references only; do not paste the full repository into model context.
- Use shell/Python scripts, tests, schema inspection and deterministic diffing for routine analysis.
- Inspect only the necessary code ranges and report records.
- Never ask an AI model to classify all files or all folders in bulk.
- Record model calls, payload character counts and actual provider tokens separately once cloud inference exists.
- Cache analysis by stable content and model/prompt version; invalidate when relevant inputs change.
- Never claim that a packet was processed merely because it was queued.
- Keep the skill instructions concise; put detailed contracts in reference files and execution logic in Python.

## 21. Mandatory milestone workflow

For each milestone, the coding agent must:

1. Read this specification and the existing `MILESTONE_STATUS.md`.
2. Inspect the actual code before proposing edits.
3. Run the full existing test suite and capture baseline results.
4. Write a short implementation plan with exact files and risks.
5. Implement only the approved milestone scope.
6. Add synthetic tests before or alongside implementation.
7. Run targeted tests, full regression tests and relevant audits.
8. Inspect the diff for accidental scope expansion and source-data mutation.
9. Update `MILESTONE_STATUS.md`, `CHANGELOG.md`, roadmap and relevant schema docs.
10. Report completed, partial, blocked and deferred criteria separately.

Never mark a milestone complete solely because the code was written. Completion is based on acceptance criteria passing.

## 22. Global safety rules

- Do not run `apply` or change any real source files during M0/M1.
- Do not delete, move or rename files in the user's personal workspace.
- Do not overwrite user changes or reset the repository.
- Do not push branches or publish the skill/plugin.
- Do not make network calls or cloud AI requests in M0/M1.
- Do not store personal file contents in test fixtures or commit reports containing private paths/content.
- Keep the dashboard bound to localhost as currently specified.
- Report uncertainty explicitly; never turn missing evidence into a confident classification.

---

# Part D — Copy-paste Antigravity execution prompt

Use the prompt below as the next task in Google Antigravity with the existing FileOS skill workspace open.

<BEGIN AGENT PROMPT>

You are the implementation agent for FileOS Organizer. Your task is to execute **M0 and M1 only** from `FILEOS_M0_M1_IMPLEMENTATION_SPEC.md`.

## Product decisions you must preserve

- Balanced prioritisation: correctness, user experience and intelligence.
- First release audience: individual/personal users.
- File storage and primary processing remain local-first.
- AI strategy is cloud-first, but AI is selective and must only be invoked when deterministic methods are insufficient.
- Do not implement live cloud AI in M0/M1. Do not make network calls. M0/M1 must record zero actual AI/model calls.
- SaaS, accounts, billing, multi-tenant infrastructure, sync and team workflows are outside this task.

## Execution sequence

### Step 1 — Inspect before editing

1. Locate the active FileOS skill workspace and global installed copy.
2. Inspect Git status, current branch, scripts, tests, references, report schemas and CLI entry points.
3. Run the existing full test suite before changes. Record the exact baseline.
4. Check whether the supplied LinkRight and Google career report directories exist. Do not assume they do.
5. Compare actual implementation with the supplied baseline description. Report discrepancies instead of silently reconciling them.

### Step 2 — Complete M0

1. Freeze/document the baseline without broad refactoring.
2. Create or update `BASELINE_INVENTORY.md`, `ROADMAP.md`, `MILESTONE_STATUS.md`, `CHANGELOG.md`, `references/ARCHITECTURE.md`, `references/ARCHITECTURE_DECISIONS.md` and `references/OUTPUT_SCHEMA.md` as appropriate.
3. Build the synthetic golden fixtures and expected-result manifests specified in Section 5.
4. Record the existing command/data-flow contracts and source-file mutation boundaries.
5. Record the cloud-first AI decision as a future provider boundary only; no live provider or network code.
6. Re-run all existing tests and confirm no regression.

Do not refactor the engine merely to make documentation easier. Do not change existing behaviour unless a safety-critical defect prevents a valid baseline; if so, stop and report the issue before making a scoped fix.

### Step 3 — Complete M1

Implement the M1 requirements in Sections 8–18:

1. Define non-overlapping file and directory accounting states.
2. Correctly represent excluded and unobserved subtrees as unknown, not invented counts.
3. Separate bytes read, bytes reused, duplicate group count, duplicate member count, logical duplicate bytes and potential extra-copy bytes.
4. Add scan IDs and configuration fingerprints.
5. Link plans and actions to source scans and revalidate preconditions before apply.
6. Make review decisions scan-aware and visibly stale when evidence changes.
7. Ensure every finding/action evidence reference resolves.
8. Make AI ledger states truthful; distinguish queue, send, actual calls, characters and provider-reported tokens.
9. Ensure no network/model calls are made in M0/M1.
10. Review/update audit checks and their documented total.
11. Add synthetic tests for all M1 requirements.
12. Validate real reports read-only where they are accessible.

Preserve historical report compatibility where feasible. Do not rewrite old reports in place. If migration is necessary, add a separate, non-destructive migration path and test it on copies.

### Step 4 — Validate

Run:

- The full original test suite.
- All newly added M0/M1 tests.
- Golden fixture scans and audits.
- Read-only compatibility audits on available LinkRight and Google career reports.
- Source immutability checks.
- A check that no network calls occurred.

Never run `apply` on the user's real workspace. You may test apply/undo only inside temporary synthetic fixtures.

### Step 5 — Update milestone status

For each acceptance criterion, record one of:

- `PASS` — proven by test or direct verification.
- `PARTIAL` — some but not all expected behaviour is implemented.
- `BLOCKED` — cannot be completed because of a concrete dependency or environment issue.
- `NOT DONE` — not implemented.

Include evidence: test names, audit IDs, commands, report paths (without exposing private file content), and actual counts. Do not use vague statements such as “fully validated” without evidence.

## Required final response

Return a concise milestone report with these tables:

1. M0 acceptance criteria: status and evidence.
2. M1 acceptance criteria: status and evidence.
3. Test baseline versus final: passed, failed, skipped and new test count.
4. Auditor results: exact check count and pass/fail for each available report.
5. Accounting equations: actual operands and reconciliation results.
6. Scan identity, plan freshness and decision-staleness behaviour.
7. Source immutability and network-call verification.
8. Files changed and why.
9. Remaining blockers and deferred work.
10. Whether M0 and M1 are genuinely complete.

Do not start M2 or any later milestone. Stop after M0/M1 and await the user's direction.

<END AGENT PROMPT>

---

## 23. Definition of success for this planning cycle

At the end of M0/M1, FileOS should not necessarily be much more “AI intelligent”. It should be much more **trustworthy**:

- We know exactly what was scanned and what was not.
- Every count and storage figure reconciles.
- Every finding points to its evidence.
- Every plan points to the scan that produced it.
- Old decisions cannot silently approve changed findings.
- The user can understand partial coverage and uncertainty.
- No AI/cloud request occurs unexpectedly.
- The original working system remains recoverable and regression-tested.

Only after that foundation is stable should FileOS expand its intelligence and automation.
