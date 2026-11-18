# FileOS Technical Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     USER'S MACHINE                       │
│                                                          │
│  ┌──────────────┐    7 CLI commands    ┌──────────────┐ │
│  │   fileos.py  │◄────────────────────►│   Terminal   │ │
│  │  (engine)    │                      └──────────────┘ │
│  └──────┬───────┘                                        │
│         │  reads filesystem (read-only until apply)      │
│         ▼                                                 │
│  ┌──────────────────────────────────┐                    │
│  │   <output-dir>/   (report)       │                    │
│  │   coverage.json                  │                    │
│  │   inventory.jsonl  (1 per file)  │                    │
│  │   folders.jsonl    (1 per dir)   │                    │
│  │   duplicate-groups.csv           │                    │
│  │   document-families.csv          │                    │
│  │   hierarchy-anomalies.csv        │                    │
│  │   proposed-actions.json          │                    │
│  │   ai-usage.json                  │                    │
│  │   summary.md                     │                    │
│  │   operation-journal.jsonl        │  ← written by apply│
│  │   review-decisions.jsonl         │  ← written by UI   │
│  └──────────────┬───────────────────┘                    │
│                 │                                         │
│        ┌────────┴────────┐                               │
│        │                 │                               │
│  ┌─────▼──────┐  ┌───────▼──────┐                       │
│  │  audit.py  │  │ dashboard.py │                        │
│  │ 12+ checks │  │  HTTP :8765  │                        │
│  │  no AI     │  │  no AI       │                        │
│  └────────────┘  └──────────────┘                        │
│                        ▲                                  │
│                  browser opens                            │
│              http://127.0.0.1:8765                        │
└─────────────────────────────────────────────────────────┘
```

## 1. Core Modules

### 1.1 `scripts/fileos.py` (Core Engine)
- **Traversal:** Iterative stack-based DFS traversal with loop detection. Visited real paths are tracked to prevent symlink circularities.
- **Data Models:** `FileRecord`, `FolderRecord`, `CoverageRecord`, `ProposedAction`, `JournalEntry`.
- **Deduplication:** Chunked streaming SHA-256 computation (64KB blocks). Exact duplicate groups are written to `duplicate-groups.csv`.
- **Document Families:** Regex-based stem normalization stripping version markers (`v1`, `v2`, `final`, `draft`, `copy`). Clustered by normalized stem.
- **Hierarchy Analysis:** Two-stage evaluation:
  - `File -> Immediate Folder Fit`: Evaluates file names against folder names.
  - `Folder -> Parent Folder Fit`: Evaluates whether child folder matches parent context.
  - Anomaly flags generated when child contradicts parent (`anomaly_flags`).
- **Plan Generation:** Reads inventory, identifies actionable moves/renames, generates deterministic `ACT-xxx` proposed actions.
- **Safe Apply:** Strict approval gate (`--approve ACT-xxx`). Requires hash match before and after move; rolls back on mismatch; logs to `operation-journal.jsonl`.
- **Undo Engine:** Reverses operations listed in `operation-journal.jsonl` using recorded reverse actions.

### 1.2 `scripts/audit.py` (Report Integrity Auditor)
- 12 deterministic mathematical and relational checks executed without invoking any model.
- Verifies count reconciliations, hash uniqueness, byte math, stable IDs, journal verification, and freshness.
- Auto-triggered at the end of every `fileos.py scan`.

### 1.3 `scripts/dashboard.py` (Local Review Web UI)
- Python stdlib `http.server` bound strictly to `127.0.0.1`.
- Serves responsive HTML5/CSS/Vanilla JS UI with trilingual support (Hinglish/Hindi/English).
- 9 review tabs: Overview, Review Inbox, Duplicates, Versions (with inline file diff), Folder Placement (with breadcrumbs), Suggested Actions, Coverage, Review History (with CLI command copy), and Audit.
- REST JSON APIs: `/api/stats`, `/api/findings`, `/api/audit`, `/api/decisions`, `/api/coverage`, `/api/history`, `/api/diff`.
- Persists user decisions to `<report-dir>/review-decisions.jsonl`.

