# Antigravity Task — Execute FileOS M0 and M1 Only

Open the existing FileOS Organizer skill workspace. Read `FILEOS_M0_M1_IMPLEMENTATION_SPEC.md` completely before editing. That specification is the source of truth for locked product decisions, scope, accounting definitions, tests, safety rules and acceptance criteria.

## Locked direction

- Prioritisation: balanced — correctness, user experience and intelligence.
- First release audience: individual/personal users.
- Storage and primary processing: local-first.
- AI strategy: cloud-first, selective invocation only when deterministic methods are insufficient.
- M0/M1: no live cloud AI, no network calls, and exactly zero actual model calls.
- SaaS, accounts, billing, multi-tenancy, cloud sync and team features are out of scope.

## Execute in this order

### M0 — Baseline freeze

1. Inspect the active workspace, global installed skill, Git status, scripts, tests, report schemas and CLI commands.
2. Run the full existing test suite before changes and record the exact baseline.
3. Check whether the known LinkRight and Google career report directories exist; do not assume they do.
4. Document the actual implementation, output artefacts, schema fields, data flow, side effects and safety gates.
5. Create/update `BASELINE_INVENTORY.md`, `ROADMAP.md`, `MILESTONE_STATUS.md`, `CHANGELOG.md`, `references/ARCHITECTURE.md`, `references/ARCHITECTURE_DECISIONS.md` and `references/OUTPUT_SCHEMA.md` as appropriate.
6. Create synthetic golden fixtures and expected-result manifests from Section 5 of the specification.
7. Record cloud-first AI as a future provider boundary only. Do not add a provider or network calls.
8. Re-run all existing tests.

Do not broad-refactor the engine during M0. Preserve all user changes and real files.

### M1 — Integrity and scan-state correctness

Implement and test the M1 requirements in Sections 8–18 of the specification:

1. Precisely define non-overlapping file and directory accounting states and reconciliation equations.
2. Count excluded/untraversed descendants as unknown, never as invented zero or discovered file totals.
3. Separate bytes read, cached bytes, duplicate group count, duplicate member count, logical duplicate bytes and potential extra-copy bytes.
4. Add a unique `scan_id` and deterministic scan-configuration fingerprint.
5. Link plans/actions to their source scan and revalidate action preconditions before apply.
6. Make review decisions scan-aware and mark materially changed decisions stale.
7. Make every finding/action evidence reference traceable and auditable.
8. Distinguish AI candidate, queue, sent, actual call, success/failure, characters and provider-reported tokens.
9. Ensure no external requests/model calls occur in M0/M1.
10. Review the twelve existing audit checks; add checks if needed and update the total accurately.
11. Add synthetic tests for all new invariants and stale-state cases.
12. Validate historical LinkRight and Google career reports read-only when available; do not rewrite them.

## Mandatory safety rules

- Never run `apply` on the user's real workspace during M0/M1.
- Test apply/undo only on synthetic temporary fixtures.
- Do not move, rename, overwrite or delete user files.
- Do not reset or overwrite user changes; do not push or publish.
- Do not make network calls or send content to a model.
- Do not put personal file contents or private reports into committed fixtures.
- Preserve localhost-only dashboard binding and existing approval gates.

## Validation

Run the full original test suite, all new tests, golden fixture scans, audit checks, source-immutability checks and a no-network-call check. For real historical reports, state which checks are possible from their existing schema and which are not.

## Final report — required tables

1. M0 acceptance criteria: PASS / PARTIAL / BLOCKED / NOT DONE with evidence.
2. M1 acceptance criteria: PASS / PARTIAL / BLOCKED / NOT DONE with evidence.
3. Original versus final test counts, including new tests.
4. Audit check count and exact results per available report.
5. Actual file/directory accounting equations with operands.
6. Byte metrics and independently recomputed duplicate-storage sample.
7. Scan identity, plan freshness, decision staleness and evidence traceability.
8. Source immutability and zero network/model call verification.
9. Files changed and reason for each.
10. Remaining blockers and deferred work.

Do not start M2 or any later milestone. Do not declare completion unless all acceptance criteria in the specification have evidence. Stop after M0/M1 and await the user's direction.
