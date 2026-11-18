# FileOS Organizer — Changelog

All notable changes to the FileOS project will be documented in this file.

## [2026-11-11] - M0 Baseline & M1 Data Integrity + Architectural Gaps
### Added
- **M0 Baseline Freeze**:
  - Baseline inventory, architecture records (ADR-001, ADR-002, ADR-003), and roadmap.
  - 17 synthetic golden fixtures covering edge-case folder layouts, version ladders, and corrupt files.
- **M1 Data Integrity & Verification**:
  - Non-overlapping accounting equations for files and directories.
  - Atomic SHA-256 calculation with pre/post stat checks to drop files modified during read.
  - Plan-apply decoupling with cryptographic `evidence_hash` stamping and `plan_id` linkage.
  - Strict 7-precondition revalidation before executing moves/renames.
  - Deterministic report auditor expanded to 15 checks (`CHK-013`, `CHK-014`, `CHK-015`).
  - Zero-network mock isolation test.
- **Architectural Gaps Resolved**:
  - **Gap 1 (`apply --dry-run`)**: Safe simulation mode testing all preconditions without mutating disk.
  - **Gap 2 (Streaming Dashboard I/O)**: Generator-based line-by-line reading maintaining <35MB RAM footprint on 100K+ files.
  - **Gap 3 (Incremental Scan)**: `--incremental` flag with `.fileos-cache.json` tracking `(mtime, size)` and skipping unneeded disk reads.
  - **Gap 4 (Near-Duplicate Detection)**: `scripts/similarity.py` using n-gram word/character shingles and Jaccard similarity ($\ge 85\%$) generating `near-duplicates.csv`.
  - **Gap 5 (Collapsible Directory Tree)**: Interactive tree hierarchy with anomaly markers in dashboard Scan Coverage tab via `/api/tree`.
  - **Gap 6 (Watch Daemon Mode)**: `fileos.py watch` with debounced mtime fingerprinting for background change detection.
  - **Oracle Cloud Connectors**: `connectors/oracle_pool.py` (free_llm_pool/ollama client) and `connectors/mongo_history.py` (MongoDB sync adapter).
- **Test Suite**: Expanded to 77 tests across 13 test suites (100% passing in ~0.52s).

## [2026-11-11]
### Added
- Local review web dashboard (`dashboard.py`) with 9 tabs (Overview, Inbox, Duplicates, Versions, Folder Placement, Actions, Coverage, History, Audit).
- Trilingual localization engine (Hinglish, Hindi, English).
- In-browser unified text diff tool with path traversal protection.
- Deterministic 12-check report integrity auditor (`audit.py`).
- Automatic integrity audit after every `fileos.py scan`.
- Full recursive directory traversal with folder-as-entity indexing (`folders.jsonl`) and edge contradiction detection.
- Comprehensive 41-test suite across 7 files.
- Synchronized global Antigravity skill installation at `~/.gemini/config/skills/fileos-organizer`.

