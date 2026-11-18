# FileOS Organizer — Baseline Inventory (M0 Freeze)

**Frozen Date:** 2026-11-11  
**Runtime Environment:** macOS (Darwin), Python 3.9.6 (Standard Library only)  
**Dependencies:** Zero external PyPI / pip dependencies  
**Pre-change Test Suite Status:** 41 tests across 7 test files, 100% passing (0.214s runtime)  

---

## 1. Codebase Layout & Line Counts

| File | LOC | Purpose |
|---|---|---|
| `scripts/fileos.py` | 1,523 | Primary recursive scan, duplicate detection, family clustering, hierarchy scoring, plan generator, safe apply and undo engine |
| `scripts/audit.py` | 543 | Deterministic 12-check report integrity auditor (zero model calls) |
| `scripts/dashboard.py` | 1,506 | Self-contained localhost review web UI server (127.0.0.1:8765, trilingual Hinglish/Hindi/English) |
| **Total Python Code** | **3,572** | **100% Python Standard Library** |

### Test Files (7 files, 41 tests)
- `tests/test_inventory.py` (4 tests): Exclusions, unstable downloads, symlinks, DOCX text extraction
- `tests/test_duplicates.py` (2 tests): Exact SHA-256 grouping, cross-directory duplicates
- `tests/test_versions.py` (2 tests): Document families, version token parsing
- `tests/test_hierarchy.py` (3 tests): Project/Folder/File edge contradictions, empty directories, mixed topics
- `tests/test_safety.py` (6 tests): Read-only dry runs, explicit approval gate, apply/undo cycle, collision block, prompt injection safety, character budget caps
- `tests/test_recursive.py` (16 tests): Uncapped traversal, depth cap, folder entity tracking, edge evaluation, deepest path mismatches, hidden files, symlink loop protection, permission denials, Unicode paths, coverage reconciliation, determinism, shared AI budget, immutability
- `tests/test_dashboard.py` (8 tests): Stats API, pagination/search, decision persistence, auditor all-pass, duplicate action ID detection, hash mismatch detection, 127.0.0.1 binding enforcement, trilingual translation key parity

---

## 2. Installation Paths & Divergence Analysis

- **Authoritative Workspace:** `/Users/satvikjain/Documents/LinkRight/FileOS/fileos-organizer-plugin/skills/fileos-organizer`
- **Global Installed Skill:** `~/.gemini/config/skills/fileos-organizer`
- **Divergence Check:** Synchronized via `cp -r`. Global skill contains identical scripts, references, and SKILL.md.

---

## 3. CLI Command Surface & Safety Gates

1. `fileos.py scan <path> [--output <dir>] [--max-depth <N>] [--exclude <patterns>] [--follow-symlinks]`
   - Read-only traversal. Never alters source files. Automatically triggers `audit.py`.
2. `fileos.py plan --scan <inventory.jsonl> [--output <actions.json>]`
   - Read-only plan generation. Writes proposed actions with unique `ACT-xxx` IDs.
3. `fileos.py report --input <dir>`
   - Formats and displays `summary.md`.
4. `fileos.py apply --plan <actions.json> --approve <ACT-IDs...>`
   - **Gated mutation.** Refuses to execute without exact `--approve` arguments. Pre-verifies hashes, verifies destination non-existence, atomically checks post-move hash, logs to `operation-journal.jsonl`.
5. `fileos.py undo --root <path> --journal-id <JRN-xxx>`
   - Inverts previously journalled file moves using verified reverse actions.
6. `fileos.py audit --input <dir> [--root <path>]`
   - Deterministic 12-check report integrity verification. Zero model calls.
7. `fileos.py dashboard --input <dir> [--root <path>] [--port 8765]`
   - Binds strictly to `127.0.0.1`. Serves 9 tabs (Overview, Inbox, Duplicates, Versions/Diff, Folder Placement, Actions, Coverage, History, Audit). Persists review choices to `review-decisions.jsonl`.

---

## 4. Report Artifacts Contract

Every scan writes into `<output-dir>/`:
- `coverage.json`: Scope metrics, traversal accounting, and completion status.
- `inventory.jsonl`: Line-delimited JSON of all eligible files.
- `folders.jsonl`: Line-delimited JSON of all folder entities with fit scores and anomaly flags.
- `duplicate-groups.csv`: Exact SHA-256 duplicate sets.
- `document-families.csv`: Normalized stem version clusters with lifecycle flags.
- `hierarchy-anomalies.csv`: Edge-by-edge structural contradictions.
- `proposed-actions.json`: Concrete proposed actions (`ACT-xxx`).
- `ai-usage.json`: Token budget ledger.
- `summary.md`: Human-readable markdown overview.
- `unresolved-review-queue.json`: Ambiguous edge cases queued for optional model adjudication.
- `review-decisions.jsonl`: Append-only user review decisions from the dashboard.
- `operation-journal.jsonl`: Audit log of applied operations.

