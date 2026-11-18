# FileOS Organizer: M0, M1 & Architectural Gaps Implementation Plan

> **Scope:** M0 Baseline Freeze, M1 Data Integrity & Verification, and Six Core Architectural Gaps (Incremental Scan, Near-Duplicate Detection, Dashboard Streaming, Apply Dry-Run, Folder Tree View, and Watch/Cron Mode).  
> **Source Specification:** `fileos_agentic_coding_pack/FILEOS_M0_M1_IMPLEMENTATION_SPEC.md` & `ANTIGRAVITY_M0_M1_EXECUTION_PROMPT.md`.

---

## 1. Executive Summary & Architecture Strategy

### 1.1 Core Principles (Preserved & Enforced)
1. **Local-First & Zero AI Cloud Overhead for M0/M1:** The core engine, primary scans, reports, dashboard, and testing run purely on the user's local machine with **0 external network requests** and standard-library Python.
2. **Deterministic-First:** File operations, hash deduplication, version clustering, and integrity verification are strictly mathematical and rule-based.
3. **Safety & Zero Destructive Defaults:** All file mutations (`apply`, `undo`) require explicit, exact Action IDs (`ACT-xxx`), strict precondition revalidation, snapshot hash checks, and collision detection. Dry-run mode (`apply --dry-run`) provides full simulation without touching disk.
4. **Balanced Prioritization:** Engineering correctness (clean accounting invariants), user experience (clear visual feedback, breadcrumbs, trilingual UI), and intelligence (near-duplicate detection and edge anomalies).

---

## 2. Phased Roadmap Breakdown

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: M0 Baseline Freeze & Golden Fixtures                               │
│  - Document current state (3,566 LOC, 41 tests)                             │
│  - Create 17 synthetic golden fixtures with expected-results manifests      │
│  - Architecture & Schema documentation lock                                 │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: M1 Data Integrity, Scan Identity & Auditor Expansion               │
│  - Non-overlapping inventory & directory accounting equations               │
│  - Truthful byte metrics & snapshot mutation invalidation                   │
│  - Deterministic `scan_id` & `scan_config_fingerprint`                       │
│  - Freshness checking & precondition revalidation for plans & decisions     │
│  - Expand auditor to 15+ integrity checks & historical report compatibility │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: Core Architectural Gap Fixes                                       │
│  - Gap 1: `apply --dry-run` simulation flag                                 │
│  - Gap 2: Streaming & Chunked IO in Dashboard (100K+ files scalability)     │
│  - Gap 3: Incremental Scan Engine (`--incremental` with mtime cache)        │
│  - Gap 4: Near-Duplicate Detection (MinHash / Shingle Jaccard similarity)   │
│  - Gap 5: Collapsible Visual Directory Tree in Dashboard Coverage Tab       │
│  - Gap 6: Watch / Daemon Scan Mode (`fileos.py watch`)                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Workstreams & Tasks

### Phase 1: M0 — Baseline Freeze & Golden Fixtures

#### Task M0.1: Workspace Inventory & Safety Freeze
- **Target Files:**
  - Create: `skills/fileos-organizer/BASELINE_INVENTORY.md`
  - Create: `skills/fileos-organizer/ROADMAP.md`
  - Create: `skills/fileos-organizer/MILESTONE_STATUS.md`
  - Create: `skills/fileos-organizer/CHANGELOG.md`
  - Update: `skills/fileos-organizer/references/ARCHITECTURE.md`
  - Update: `skills/fileos-organizer/references/ARCHITECTURE_DECISIONS.md`
  - Update: `skills/fileos-organizer/references/OUTPUT_SCHEMA.md`
- **Actions:**
  1. Record current workspace layout: Python 3 stdlib, 41 tests passing in ~0.24s, 7 CLI commands.
  2. Inspect Git status to ensure no uncommitted user changes are trampled.
  3. Formally document all current report artifacts: `coverage.json`, `inventory.jsonl`, `folders.jsonl`, `duplicate-groups.csv`, `document-families.csv`, `hierarchy-anomalies.csv`, `proposed-actions.json`, `ai-usage.json`, `summary.md`, `operation-journal.jsonl`, `review-decisions.jsonl`.
  4. Document the locked architectural boundary: Local-first file operations, cloud-first AI boundary in future milestones, zero external network calls in M0/M1.

#### Task M0.2: Synthetic Golden Fixture Suite (17 Scenarios)
- **Target Files:**
  - Create: `skills/fileos-organizer/tests/fixtures/golden_manifests.json`
  - Create: `skills/fileos-organizer/tests/test_golden_fixtures.py`
- **Actions:**
  Implement synthetic, non-destructive test fixtures for all 17 cases specified in Section 5 of `FILEOS_M0_M1_IMPLEMENTATION_SPEC.md`:
  1. Exact duplicate (identical bytes, different names/paths).
  2. Renamed duplicate (identical bytes, unrelated stems).
  3. Content difference with same name.
  4. Version tokens (`_v1`, `_v2`, `_final`).
  5. Branch-like versions (`_internal`, `_client`).
  6. Deep hierarchy (12+ levels).
  7. Parent mismatch (file fits child, child contradicts parent).
  8. Mixed folder (unrelated topics under single parent).
  9. Empty folders (zero-file directories).
  10. Hidden files (`.dotfile` handling).
  11. Excluded subtrees (`node_modules`, `.git`).
  12. Symlink variants (file link, directory link, broken link, recursive loop).
  13. Unstable downloads (`.crdownload`, `.part`).
  14. Inaccessible paths (mocked/chmod permission denial).
  15. Unicode paths and long filenames (`📁 Pröjécts 2026/Démo & Spécs #1/résumé.txt`).
  16. Destination collision on apply.
  17. File modification mid-scan (mtime/size changed between stat and hash).
  - Every fixture validates against its explicit JSON expectation manifest (counts, statuses, flags).

---

### Phase 2: M1 — Data Integrity, Scan Identity & Verification

#### Task M1.1: Unambiguous Non-Overlapping Accounting Equations
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/fileos.py`
  - Modify: `skills/fileos-organizer/scripts/audit.py`
  - Test: `skills/fileos-organizer/tests/test_accounting.py`
- **Actions:**
  1. Refactor `CoverageRecord` and scan counters to strictly enforce non-overlapping states:
     - **File Equation:**
       $$\text{files\_observed} = \text{files\_excluded} + \text{files\_eligible}$$
       $$\text{files\_eligible} = \text{files\_analysed} + \text{files\_skipped} + \text{files\_failed}$$
     - **Directory Equation:**
       $$\text{directories\_observed} = \text{directories\_scanned} + \text{directories\_excluded} + \text{directories\_inaccessible} + \text{directories\_depth\_skipped}$$
     - **Unobserved Subtree Rule:** Excluded or inaccessible directory descendants are counted as `unknown`, never fabricated as discovered or zero.
  2. Track optional text extraction status as a secondary orthogonal quality field (`extraction_status`: `success` | `partial` | `unsupported`), never affecting core inventory counts.

#### Task M1.2: Truthful Byte & Storage Metrics
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/fileos.py`
  - Modify: `skills/fileos-organizer/scripts/audit.py`
- **Actions:**
  1. In `coverage.json`, separate:
     - `eligible_file_bytes`: Sum of observed stat sizes.
     - `bytes_read_for_hashing`: Actual bytes streamed from disk during this run.
     - `bytes_reused_from_hash_cache`: Bytes verified via incremental cache (0 in cold scan).
     - `duplicate_group_count`: Number of distinct duplicate clusters.
     - `duplicate_member_file_count`: Total file instances in those groups.
     - `duplicate_group_logical_bytes`: Sum of all file sizes in all duplicate groups.
     - `potential_extra_copy_bytes`: Logical size of redundant copies ($\sum (\text{count} - 1) \times \text{size}$).
  2. Implement atomic stat-checking: Check `(mtime, size)` before and after reading; if modified during hashing, mark file `unstable` and discard the hash.

#### Task M1.3: Scan Identity & Deterministic Configuration Fingerprint
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/fileos.py`
  - Modify: `skills/fileos-organizer/scripts/dashboard.py`
- **Actions:**
  1. Generate unique `scan_id`: `SCN-YYYYMMDDTHHMMSSZ-<random6>`.
  2. Compute canonical `scan_config_fingerprint`: SHA-256 of `(canonical_root, max_depth, exclusions, follow_symlinks, engine_version)`.
  3. Stamp `scan_id` and `scan_config_fingerprint` into `coverage.json`, `inventory.jsonl`, `folders.jsonl`, and `proposed-actions.json`.

#### Task M1.4: Plan Freshness & Action Precondition Gates
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/fileos.py` (`plan` & `apply` methods)
  - Test: `skills/fileos-organizer/tests/test_safety.py`
- **Actions:**
  1. In `proposed-actions.json`, record `plan_id`, `source_scan_id`, `source_scan_config_fingerprint`, and an evidence hash digest per action.
  2. Before executing any action in `fileos.py apply`, strictly enforce **7 Preconditions**:
     - Precondition 1: Plan schema is supported.
     - Precondition 2: Source scan and evidence records exist.
     - Precondition 3: Source file currently exists at expected path.
     - Precondition 4: Source file current hash matches the scan-time SHA-256.
     - Precondition 5: Destination path does not exist (collision block).
     - Precondition 6: Action ID is explicitly listed in `--approve`.
     - Precondition 7: Target file is not flagged as authoritative (`is_authoritative: True`) or protected.

#### Task M1.5: Review Decision Freshness & Staleness Detection
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/dashboard.py`
  - Test: `skills/fileos-organizer/tests/test_dashboard.py`
- **Actions:**
  1. Stored decisions in `review-decisions.jsonl` record `finding_fingerprint` and `scan_id`.
  2. When the dashboard loads a report:
     - If decision's `scan_id` matches current report $\rightarrow$ **Current**.
     - If finding still exists with identical evidence but older `scan_id` $\rightarrow$ **Historical (Compatible)**.
     - If finding evidence has changed $\rightarrow$ **Stale (Needs Re-check)**.
     - If finding no longer exists $\rightarrow$ **Obsolete / No Longer Applicable**.

#### Task M1.6: AI Usage Ledger Truthfulness
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/fileos.py`
  - Modify: `skills/fileos-organizer/scripts/audit.py`
  - Test: `skills/fileos-organizer/tests/test_network_isolation.py`
- **Actions:**
  1. Record explicit ledger states in `ai-usage.json`: `candidate_created`, `queued`, `not_sent`, `sent`, `succeeded`, `failed`, `cached`, `skipped_by_policy`.
  2. Enforce zero model calls: `actual_model_calls: 0`, `provider_tokens_billed: 0`.
  3. Add automated test intercepting socket/HTTP calls to verify 0 network requests during scan, plan, report, audit, and dashboard execution.

#### Task M1.7: Auditor Expansion to 15+ Checks
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/audit.py`
- **Actions:**
  Expand from 12 to 15 comprehensive checks:
  - `CHK-001`: File counts reconciliation (observed = excluded + eligible; eligible = analysed + skipped + failed).
  - `CHK-002`: Directory counts reconciliation (observed = scanned + excluded + inaccessible + depth_skipped).
  - `CHK-003`: Duplicate group membership (all groups $\ge 2$ members).
  - `CHK-004`: Duplicate SHA-256 consistency.
  - `CHK-005`: Duplicate storage mathematics (extra copies $\times$ verified size).
  - `CHK-006`: Bytes hashed vs duplicate footprint consistency.
  - `CHK-007`: AI usage ledger truthfulness (queued $\ne$ model calls, chars $\ne$ tokens).
  - `CHK-008`: Proposed action IDs uniqueness and evidence traceability.
  - `CHK-009`: Stable finding IDs (`ANO-*`, `DUP-*`, `FAM-*`).
  - `CHK-010`: Applied action status verified via journal.
  - `CHK-011`: Coverage status honesty (`complete` vs `partial`).
  - `CHK-012`: Stale plan snapshot verification against live disk.
  - `CHK-013` *(New)*: Scan ID & configuration fingerprint format and consistency.
  - `CHK-014` *(New)*: Plan-to-scan linkage and action precondition readiness.
  - `CHK-015` *(New)*: Symlink loop and unobserved subtree accounting integrity.

---

### Phase 3: Architectural Gap Fixes

#### Gap 1: `apply --dry-run` Mode
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/fileos.py`
  - Test: `skills/fileos-organizer/tests/test_safety.py`
- **Design:**
  - Add `--dry-run` flag to `fileos.py apply`.
  - Simulates each approved action: checks all 7 preconditions, prints planned source $\rightarrow$ destination transitions, calculates net filesystem changes, but never calls `shutil.move` or writes to `operation-journal.jsonl`.
  - Output format: Clear terminal table and JSON summary of simulated results.

#### Gap 2: Streaming & Chunked IO in Dashboard
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/dashboard.py`
- **Design:**
  - Replace full-file `json.load()` and `csv.DictReader` in `get_findings()` and `get_coverage()` with line-by-line streaming generators.
  - Use file offset indexing (`.idx` cache) or byte-range seek for fast pagination on massive (100K+ files) `inventory.jsonl` and `folders.jsonl`.
  - Memory consumption remains under 35 MB regardless of report size.

#### Gap 3: Incremental Scan Engine (`--incremental`)
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/fileos.py`
  - Test: `skills/fileos-organizer/tests/test_incremental.py`
- **Design:**
  - Add `--incremental` flag to `fileos.py scan`.
  - Stores a lightweight state cache: `.fileos-cache.json` containing `{rel_path: (mtime, size_bytes, sha256)}`.
  - On re-scan:
    - If file exists with identical `mtime` and `size_bytes`, reuse cached SHA-256 and increment `bytes_reused_from_hash_cache`.
    - If `mtime` or `size_bytes` differs, re-read, re-hash, and increment `bytes_read_for_hashing`.
    - Detect deleted files and remove from state.
  - Drops re-scan time on LinkRight (18K files) from ~30s down to <1.5s!

#### Gap 4: Near-Duplicate Detection Engine
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/fileos.py`
  - Create: `skills/fileos-organizer/scripts/similarity.py`
  - Test: `skills/fileos-organizer/tests/test_near_duplicates.py`
- **Design:**
  - Pure Python, zero pip dependencies.
  - Extracts 3-gram character shingles or word tokens from text/DOCX documents.
  - Computes MinHash signatures (64 bit hashes) or pairwise Jaccard coefficient on candidates sharing similar size ($\pm 20\%$) and document family stems.
  - Pairs with Jaccard similarity $\ge 0.85$ are flagged in `near-duplicates.csv` with shared similarity percentage, diff overview, and recommended action (`review_draft_consolidation`).

#### Gap 5: Visual Collapsible Folder Tree in Dashboard
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/dashboard.py`
- **Design:**
  - In the **Scan Coverage** tab, provide a toggle between "Flat List" and "Interactive Tree".
  - Tree component built with pure Vanilla JS and CSS:
    - Collapsible directories with folder icons (📁 / 📂).
    - Color-coded badges for direct files, total descendants, and detected anomalies.
    - Click-to-filter: Clicking any folder node immediately filters the Review Inbox to findings within that subtree.

#### Gap 6: Watch / Daemon Scan Mode (`fileos.py watch`)
- **Target Files:**
  - Modify: `skills/fileos-organizer/scripts/fileos.py`
  - Test: `skills/fileos-organizer/tests/test_watch.py`
- **Design:**
  - Add `watch` subcommand:
    `python3 fileos.py watch <target-dir> --output <dir> --interval 60`
  - Uses a lightweight, non-blocking polling loop (stat checks across directory roots).
  - Automatically triggers an incremental scan when changes are detected, updates the report, runs the integrity audit, and refreshes the live dashboard.

---

## 4. Oracle Server Integration Analysis & Questions for User

Based on your system configuration (`~/.claude/tools.yaml`), we identified your standing **Oracle Cloud Always-Free VM** running:
- `n8n` (Workflow automation)
- `mongodb` (System & log document database)
- `ollama` (Local CPU LLM inference & `nomic-embed-text` embeddings)
- `free_llm_pool` (Free-tier key aggregator on port 8765)

### Key Questions for You:
1. **Scope Boundary for FileOS:**
   - The M0/M1 specification strictly mandates a **local-first personal tool** on your Mac with zero network calls and localhost binding.
   - Do you want FileOS core engine to remain **100% local-first on your Mac**, or do you envision FileOS eventually offloading background scans/dashboards to your Oracle VM?
2. **Oracle Server Role in Future Milestones (M2+):**
   - **Option A (Pure Local Mac):** Keep FileOS 100% on Mac. Oracle server is untouched.
   - **Option B (Oracle Remote Watcher/Worker):** Run the FileOS watch daemon or cron on Oracle for directories mounted/synced to the VM.
   - **Option C (Oracle AI Inference Gateway):** When M2 introduces selective AI adjudication, route ambiguous packets through your Oracle `ollama` instance or `free_llm_pool` instead of commercial cloud APIs.
3. **Database Preference:**
   - FileOS currently writes flat JSONL/CSV report files (portable, zero database setup). Would you like FileOS to optionally push completed scan summaries to your Oracle MongoDB database for long-term historical analytics, or keep it strictly file-based?

---

## 5. Verification & Acceptance Criteria

Every milestone and gap fix must satisfy the following validation gates before completion:
1. **Pre-test baseline:** 41/41 tests passing before any code modification.
2. **Regression-free:** All 41 original tests continue to pass.
3. **New test coverage:**
   - 17 golden fixture tests (`test_golden_fixtures.py`).
   - Accounting invariant tests (`test_accounting.py`).
   - Network isolation test (`test_network_isolation.py`).
   - Incremental scan test (`test_incremental.py`).
   - Near-duplicate similarity test (`test_near_duplicates.py`).
   - Dry-run apply test (`test_safety.py`).
4. **Audit Health:** All reports pass 15/15 checks with zero failures.
5. **Zero Data Loss:** Source files are never modified without explicit user CLI approval with `--approve`.

---
*Plan prepared for execution approval.*
