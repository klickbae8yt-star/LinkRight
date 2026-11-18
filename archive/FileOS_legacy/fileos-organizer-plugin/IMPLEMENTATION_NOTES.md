# FileOS Local Review Dashboard — Implementation Notes

## 1. Existing Report Schemas & Architecture
The FileOS scan engine outputs the following artifacts in the report directory:
- `coverage.json`: Machine-readable scan coverage (directories/files discovered, scanned, excluded, inaccessible, depth capped, mount/symlink accounting, `is_complete`, `partial_reasons`).
- `folders.jsonl`: First-class folder index with `folder_id`, direct vs. descendant counts, aggregate size, extension distribution, token summaries, and parent relationship status.
- `inventory.jsonl`: Comprehensive file inventory with `file_id`, relative path, normalized stem, SHA-256 hash, timestamps, readiness, and depth.
- `duplicate-groups.csv`: Exact duplicate groups (`group_id`, `sha256`, `size_bytes`, `rel_path`, `basename`).
- `document-families.csv`: Document version families (`family_id`, `family_stem`, `rel_path`, `basename`, `revision`, `lifecycle`, `is_authoritative`).
- `hierarchy-anomalies.csv`: Edge-by-edge folder anomalies (`anomaly_id`, `edge`, `folder`, `parent`, `depth`, `status`, `file_folder_fit`, `folder_parent_fit`, `evidence`, `suggested_action`).
- `unresolved-review-queue.json`: Bounded AI triage packets (max 10 packets, max 20,000 chars total) with excerpts.
- `proposed-actions.json`: Dry-run action plan with `action_id`, `action_type`, `source`, `destination`, `reason`, `confidence`, `dependency_check`, `reversibility`.
- `ai-usage.json`: AI token & excerpt character ledger.
- `summary.md`: Consolidated human-readable report.

## 2. Missing Evidence & Backward Compatibility Strategy
- If older report directories lack `coverage.json` or `folders.jsonl`, the dashboard and audit layer synthesize backward-compatible summary objects and label missing properties as `Evidence unavailable in this scan`.
- If hash values or file sizes are absent, they are explicitly flagged as incomplete evidence.
- The UI gracefully falls back to empty states if optional files are missing without crashing.

## 3. Baseline Verification Status
- Full test suite execution: **33 / 33 tests passed in 0.263s**.
- Tested real report: `/private/tmp/fileos-scan-linkright` (18,196 files, 2,689 duplicate groups, 255 anomalies, 2,944 actions).

## 4. Chosen UI Architecture
- **Server:** Built-in Python standard library `http.server.HTTPServer` + `BaseHTTPRequestHandler`. Zero external package dependencies.
- **Security:** Binds strictly to `127.0.0.1`. Refuses non-localhost binding. Path traversal protection checks all paths against root and report directories.
- **Frontend:** Pure HTML5, CSS3, and modern Vanilla JavaScript in a single self-contained asset bundle. Zero CDN requests, zero remote fonts, zero analytics.
- **Performance & Scalability:** Server exposes paginated, filterable JSON APIs (`/api/findings`, `/api/duplicates`, `/api/families`, `/api/anomalies`, `/api/actions`, `/api/coverage`, `/api/stats`, `/api/audit`, `/api/decisions`) so large reports (18,000+ files) load in milliseconds without pushing massive payloads to the browser.
- **Languages:** Authored deterministic localization dictionary for Hinglish (default), Hindi, and English. Zero AI tokens used for UI text or translation.
- **Review Decisions Store:** Append-only `<report-dir>/review-decisions.jsonl` tracking finding ID, user choice, timestamp, user note, and report fingerprint. Reopening the dashboard seamlessly resumes prior review progress.
- **Safety Guarantee:** Read-only viewing and review. Action execution remains gated behind the explicit CLI approval command (`fileos.py apply --approve ACT-...`).

