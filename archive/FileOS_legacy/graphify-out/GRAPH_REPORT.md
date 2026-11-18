# Graph Report - FileOS  (2026-11-16)

## Corpus Check
- 51 files · ~80,293 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .zip 1)

## Summary
- 974 nodes · 1337 edges · 56 communities (31 shown, 25 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 122 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Local Review Dashboard Server
- Product Chat History & Architecture Principles
- Local Review Dashboard Server
- Low-Token Organization Architecture
- Low-Token Organization Architecture
- Low-Token Organization Architecture
- Recursive Directory Traversal
- Quality Audit & Diagnostics
- Low-Token Organization Architecture
- Recursive Directory Traversal
- Recursive Directory Traversal
- Local Review Dashboard Server
- Recursive Directory Traversal
- Local Review Dashboard Server
- Local Review Dashboard Server
- Recursive Directory Traversal
- Antigravity Execution Prompts
- Antigravity Execution Prompts
- Queue Subsystem
- Recursive Directory Traversal
- Standard Library Dependencies
- Dependency Guard & Validation
- Recursive Directory Traversal
- Quality Audit & Diagnostics
- Recursive Directory Traversal
- Files Subsystem
- M0-M1 Implementation Milestones
- Folders Subsystem
- Baseline Subsystem
- Different Subsystem
- Plan Subsystem
- Local Review Dashboard Server
- Local Review Dashboard Server
- Dependency Guard & Validation
- Pack Subsystem
- Changelog Subsystem
- Checklist Subsystem
- Architecture Subsystem
- Local Review Dashboard Server
- Path Subsystem
- Detects Subsystem
- Antigravity Execution Prompts
- Repository Radar & Research
- Milestone Subsystem

## God Nodes (most connected - your core abstractions)
1. `FileOSEngine` - 89 edges
2. `ReportAuditor` - 37 edges
3. `DashboardDataRepo` - 27 edges
4. `TestGoldenFixtures` - 21 edges
5. `TestRecursiveTree` - 20 edges
6. `TestDashboardAndAudit` - 18 edges
7. `compute_sha256()` - 12 edges
8. `main()` - 12 edges
9. `TestSafety` - 11 edges
10. `extract_bounded_content()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `DashboardDataRepo` --uses--> `ReportAuditor`  [INFERRED]
  fileos-organizer-plugin/skills/fileos-organizer/scripts/dashboard.py → fileos-organizer-plugin/skills/fileos-organizer/scripts/audit.py
- `DashboardHTTPHandler` --uses--> `ReportAuditor`  [INFERRED]
  fileos-organizer-plugin/skills/fileos-organizer/scripts/dashboard.py → fileos-organizer-plugin/skills/fileos-organizer/scripts/audit.py
- `TestDashboardAndAudit` --uses--> `ReportAuditor`  [INFERRED]
  fileos-organizer-plugin/skills/fileos-organizer/tests/test_dashboard.py → fileos-organizer-plugin/skills/fileos-organizer/scripts/audit.py
- `TestNetworkIsolation` --uses--> `ReportAuditor`  [INFERRED]
  fileos-organizer-plugin/skills/fileos-organizer/tests/test_network_isolation.py → fileos-organizer-plugin/skills/fileos-organizer/scripts/audit.py
- `FileOSEngine` --uses--> `NearDuplicateDetector`  [INFERRED]
  fileos-organizer-plugin/skills/fileos-organizer/scripts/fileos.py → fileos-organizer-plugin/skills/fileos-organizer/scripts/similarity.py

## Import Cycles
- None detected.

## Communities (56 total, 25 thin omitted)

### Community 0 - "Local Review Dashboard Server"
Cohesion: 0.08
Nodes (3): check_file_readiness(), normalize_text(), tokenize()

### Community 1 - "Product Chat History & Architecture Principles"
Cohesion: 0.03
Nodes (68): 10. Co-founder verdict, 1. Architectural principle, 1. Problem ko technically samajhte hain, 1. Sabse important overlooked problems, 1. Tumhari teen problems ka breakdown, 2. Common AI interface, 2. Existing solutions: Market research, 2. Operational and workflow problems (+60 more)

### Community 2 - "Local Review Dashboard Server"
Cohesion: 0.07
Nodes (3): DashboardDataRepo, run_dashboard_server(), TestDashboardAndAudit

### Community 3 - "Low-Token Organization Architecture"
Cohesion: 0.05
Nodes (43): 10. Parser capability registry, 11.1 Summary report sections, 11.2 Every proposed action must include, 11. Reports and output contracts, 12. Suggested scoring model, 13. CLI interface expectations, 14. Testing requirements, 15. Definition of done (+35 more)

### Community 4 - "Low-Token Organization Architecture"
Cohesion: 0.05
Nodes (43): 10. Parser capability registry, 11.1 Summary report sections, 11.2 Every proposed action must include, 11. Reports and output contracts, 12. Suggested scoring model, 13. CLI interface expectations, 14. Testing requirements, 15. Definition of done (+35 more)

### Community 5 - "Low-Token Organization Architecture"
Cohesion: 0.05
Nodes (43): 10. Parser capability registry, 11.1 Summary report sections, 11.2 Every proposed action must include, 11. Reports and output contracts, 12. Suggested scoring model, 13. CLI interface expectations, 14. Testing requirements, 15. Definition of done (+35 more)

### Community 6 - "Recursive Directory Traversal"
Cohesion: 0.07
Nodes (3): FileOSEngine, TestGoldenFixtures, TestIncrementalScan

### Community 7 - "Quality Audit & Diagnostics"
Cohesion: 0.05
Nodes (41): 10. M1.3 — Scan identity and configuration fingerprint, 11. M1.4 — Plan freshness and action preconditions, 12. M1.5 — Review decision freshness, 13. M1.6 — Evidence traceability, 14. M1.7 — AI usage ledger truthfulness (no live AI yet), 15. M1.8 — Auditor updates, 16. M1 test requirements, 17. M1 real-report validation (+33 more)

### Community 8 - "Low-Token Organization Architecture"
Cohesion: 0.05
Nodes (40): 10.1 Extraction (`extract.py`), 10.2 Chunking (`chunk.py`, `chunker_ver = "c1"`), 10.3 Embeddings and relations (`semantic.py`), 10.4 Summaries (`summarize.py`, `prompt_ver = "p1"`), 10. Understanding (Layers 1 and 2), 11. Wiki output (Obsidian vault), 12.1 API (OpenAI-compatible subset), 12.2 Errors (OpenAI shape `{"error":{"type","message"}}`) (+32 more)

### Community 9 - "Recursive Directory Traversal"
Cohesion: 0.10
Nodes (9): calculate_token_fit(), CoverageRecord, FileRecord, FolderRecord, main(), parse_version_tokens(), PhaseTimer, VersionInfo (+1 more)

### Community 11 - "Local Review Dashboard Server"
Cohesion: 0.06
Nodes (31): 1. Home — `Your files at a glance`, 2. Review inbox — `Things worth checking`, 3. Duplicate review — `Repeated copies`, 4. Version review — `Possible document versions`, 5. Folder placement review — `Does this folder belong here?`, 6. Action review — `Changes FileOS is suggesting`, 7. Scan coverage — `What FileOS could and could not check`, 8. AI usage — `When FileOS needed extra help` (+23 more)

### Community 12 - "Recursive Directory Traversal"
Cohesion: 0.07
Nodes (28): 10. Update the skill instructions and documentation, 11. Final validation and response, 1. Exact outcome required, 2. First diagnose the current limitation, 3. Recursive traversal contract, 4. Folder-first data model, 5. Folder context and recursive hierarchy intelligence, 6. Low-token and low-compute rules for full trees (+20 more)

### Community 13 - "Local Review Dashboard Server"
Cohesion: 0.07
Nodes (25): 1. Recursive Directory Traversal & Coverage Contract, 2. Hierarchy Relationship & Edge Evaluation, 3. Progressive AI Escalation & Shared Budget, FileOS Decision Tree & Recursive Traversal Intelligence, Shared Hard Run Budgets (Files + Folders):, 1. `coverage.json`, 2. `inventory.jsonl`, 3. `folders.jsonl` (+17 more)

### Community 14 - "Local Review Dashboard Server"
Cohesion: 0.07
Nodes (26): 1.1 Core Principles (Preserved & Enforced), 1. Executive Summary & Architecture Strategy, 2. Phased Roadmap Breakdown, 3. Detailed Workstreams & Tasks, 4. Oracle Server Integration Analysis & Questions for User, 5. Verification & Acceptance Criteria, FileOS Organizer: M0, M1 & Architectural Gaps Implementation Plan, Gap 1: `apply --dry-run` Mode (+18 more)

### Community 15 - "Recursive Directory Traversal"
Cohesion: 0.08
Nodes (4): extract_bounded_content(), _read_candidate_text(), TestInventory, TestSafety

### Community 16 - "Antigravity Execution Prompts"
Cohesion: 0.09
Nodes (22): 10. Code quality expectations, 11. Validation and packaging, 12. How to work efficiently (important), 13. Final response format, 1. Mission, 2. First inspect the workspace; do not assume, 3. Required implementation outputs, 4.1 Python-first deterministic core (+14 more)

### Community 17 - "Antigravity Execution Prompts"
Cohesion: 0.09
Nodes (22): 10. Code quality expectations, 11. Validation and packaging, 12. How to work efficiently (important), 13. Final response format, 1. Mission, 2. First inspect the workspace; do not assume, 3. Required implementation outputs, 4.1 Python-first deterministic core (+14 more)

### Community 18 - "Queue Subsystem"
Cohesion: 0.13
Nodes (3): MongoHistorySync, OracleAIPoolClient, TestOracleConnectors

### Community 20 - "Standard Library Dependencies"
Cohesion: 0.12
Nodes (6): compute_jaccard_similarity(), get_character_shingles(), get_word_shingles(), NearDuplicatePair, normalize_text_for_shingling(), TestNearDuplicateDetection

### Community 21 - "Dependency Guard & Validation"
Cohesion: 0.11
Nodes (18): 10. Milestones (each one: red test, green code, all old tests pass), 11. Test fixtures I must build, 12. Done means, 13. Not in scope (v1), 1. The problem in one story, 2. What the user wants, 3. What exists today (checked in the code, 11 Nov 2026), 4. Rules I must follow (+10 more)

### Community 22 - "Recursive Directory Traversal"
Cohesion: 0.14
Nodes (13): 1. Scan (Recursive by Default, Read-Only), 2. Plan (Dry-Run), 3. Report, 4. Apply (Approval-Gated), 5. Undo, CLI Usage, Directory Layout, FileOS Organizer Plugin (+5 more)

### Community 25 - "Recursive Directory Traversal"
Cohesion: 0.17
Nodes (11): 1. Coverage & Tree Metrics, 2. Directory Hierarchy Overview (Depth Markers), 3. Hierarchy Anomalies (Edge-by-Edge), 4. Exact Duplicates (Preserved), 5. Document Families & Versions, 6. AI Usage & Token Budget Ledger, Family FAM-001: `guide`, Family FAM-002: `firmware_bootloader` (+3 more)

### Community 27 - "M0-M1 Implementation Milestones"
Cohesion: 0.22
Nodes (8): Antigravity Task — Execute FileOS M0 and M1 Only, Execute in this order, Final report — required tables, Locked direction, M0 — Baseline freeze, M1 — Integrity and scan-state correctness, Mandatory safety rules, Validation

### Community 29 - "Baseline Subsystem"
Cohesion: 0.29
Nodes (6): 1. Codebase Layout & Line Counts, 2. Installation Paths & Divergence Analysis, 3. CLI Command Surface & Safety Gates, 4. Report Artifacts Contract, FileOS Organizer — Baseline Inventory (M0 Freeze), Test Files (7 files, 41 tests)

### Community 32 - "Local Review Dashboard Server"
Cohesion: 0.33
Nodes (5): 1. Existing Report Schemas & Architecture, 2. Missing Evidence & Backward Compatibility Strategy, 3. Baseline Verification Status, 4. Chosen UI Architecture, FileOS Local Review Dashboard — Implementation Notes

### Community 33 - "Local Review Dashboard Server"
Cohesion: 0.33
Nodes (5): 1.1 `scripts/fileos.py` (Core Engine), 1.2 `scripts/audit.py` (Report Integrity Auditor), 1.3 `scripts/dashboard.py` (Local Review Web UI), 1. Core Modules, FileOS Technical Architecture

### Community 35 - "Pack Subsystem"
Cohesion: 0.40
Nodes (4): Current recommended use, FileOS Agentic Coding Build Pack, Files, Safety

### Community 36 - "Changelog Subsystem"
Cohesion: 0.40
Nodes (4): [2026-11-11], [2026-11-11] - M0 Baseline & M1 Data Integrity + Architectural Gaps, Added, FileOS Organizer — Changelog

### Community 37 - "Checklist Subsystem"
Cohesion: 0.40
Nodes (4): Architectural Gaps Resolution Checklist, FileOS Organizer — Milestone Status, M0 Acceptance Checklist, M1 Acceptance Checklist

### Community 38 - "Architecture Subsystem"
Cohesion: 0.40
Nodes (4): ADR-001: Product Direction & System Boundaries, ADR-002: Deterministic-First & Shared AI Token Caps, ADR-003: Non-Overlapping Inventory & Directory Accounting, FileOS Architecture Decisions Record (ADR)

### Community 42 - "Antigravity Execution Prompts"
Cohesion: 0.40
Nodes (4): Antigravity documentation, FileOS Antigravity Skill Build Pack, Files, Recommended use

## Knowledge Gaps
- **521 isolated node(s):** `Antigravity Self-Prompt — Build the FileOS Low-Token Organizer Skill/Plugin`, `1. Mission`, `2. First inspect the workspace; do not assume`, `3. Required implementation outputs`, `4. Architecture and implementation constraints` (+516 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 706 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FileOSEngine` connect `Recursive Directory Traversal` to `Local Review Dashboard Server`, `Dependency Guard & Validation`, `Path Subsystem`, `Recursive Directory Traversal`, `Recursive Directory Traversal`, `Detects Subsystem`, `Recursive Directory Traversal`, `Recursive Directory Traversal`, `Standard Library Dependencies`, `Files Subsystem`, `Folders Subsystem`, `Different Subsystem`, `Plan Subsystem`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 69 inferred relationships involving `FileOSEngine` (e.g. with `NearDuplicateDetector` and `TestAccountingInvariants`) actually correct?**
  _`FileOSEngine` has 69 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Antigravity Self-Prompt — Build the FileOS Low-Token Organizer Skill/Plugin`, `1. Mission`, `2. First inspect the workspace; do not assume` to the rest of the system?**
  _521 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Local Review Dashboard Server` be split into smaller, more focused modules?**
  _Cohesion score 0.07701863354037267 - nodes in this community are weakly interconnected._
- **Why does `ReportAuditor` connect `Quality Audit & Diagnostics` to `Local Review Dashboard Server`, `Local Review Dashboard Server`, `Dependency Guard & Validation`, `Local Review Dashboard Server`, `Recursive Directory Traversal`, `File Subsystem`, `Directory Subsystem`, `Check Subsystem`, `Check Subsystem`, `Check Subsystem`, `Check Subsystem`, `Check Subsystem`, `Scan Subsystem`, `Recursive Directory Traversal`, `Quality Audit & Diagnostics`, `Check Subsystem`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `ReportAuditor` (e.g. with `DashboardDataRepo` and `DashboardHTTPHandler`) actually correct?**
  _`ReportAuditor` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Should `Product Chat History & Architecture Principles` be split into smaller, more focused modules?**
  _Cohesion score 0.028985507246376812 - nodes in this community are weakly interconnected._