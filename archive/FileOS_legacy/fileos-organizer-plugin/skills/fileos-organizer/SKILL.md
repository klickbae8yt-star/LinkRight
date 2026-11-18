---
name: fileos-organizer
description: Local-first, deterministic-first file organizer that recursively discovers duplicate files, document version families, and folder hierarchy contradictions across complete directory trees with strict AI token caps and a local zero-token review dashboard.
---

# FileOS Organizer Skill

FileOS recursively inspects, analyzes, and organizes complete directory trees using deterministic Python standard library scripts, using model reasoning only to adjudicate genuinely ambiguous edge cases.

## Core Principles

1. **Recursive-by-Default:** Scans entire directory trees to the deepest reachable leaf directory. Traversal is iterative and stack-safe (no depth limit by default).
2. **Folders as First-Class Entities:** All folders (including empty folders and intermediate containers) are indexed with direct vs. descendant metrics, dominant extension, and fit score.
3. **Edge-by-Edge Hierarchy Intelligence:** Evaluates `File → Immediate Folder` and `Folder → Parent Project` independently.
4. **Strict Shared AI Token Budgets:** Files and folders share run caps: Pass 0 (0 chars), Pass 1 (2,000 chars), Pass 2 (8,000 chars), Pass 3 (16,000 chars). Maximum 10 packets and 20,000 characters total per scan.
5. **Safety & Zero Destructive Defaults:** `scan` and `plan` are strictly read-only. No permanent file deletion. No files are moved without explicit action ID approvals. Reversible operation journals allow single-command undo.
6. **Auto-Integrity Audit:** Every scan automatically runs 12 deterministic integrity checks and prints a summary. No AI tokens consumed.
7. **Local Review Dashboard:** Self-contained local web UI (Hinglish/Hindi/English) for reviewing findings, marking decisions, comparing file versions side-by-side, and generating apply commands. Binds strictly to 127.0.0.1.

---

## Command Reference

The agent invokes `fileos.py` via shell commands:

```bash
# 1. Recursive Scan (auto-audits after completion)
python3 <skill-dir>/scripts/fileos.py scan "<target-path>" \
  [--output "<output-folder>"] \
  [--max-depth <N>] \
  [--exclude "node_modules,.git"] \
  [--follow-symlinks]

# 2. Generate Proposed Plan (dry-run, never moves files)
python3 <skill-dir>/scripts/fileos.py plan \
  --scan "<output-folder>/inventory.jsonl"

# 3. View Report Summary
python3 <skill-dir>/scripts/fileos.py report \
  --input "<output-folder>"

# 4. Apply Approved Actions (requires explicit Action IDs)
python3 <skill-dir>/scripts/fileos.py apply \
  --plan "<output-folder>/proposed-actions.json" \
  --approve ACT-001 ACT-002

# 5. Undo a Journalled Operation
python3 <skill-dir>/scripts/fileos.py undo \
  --root "<target-folder>" \
  --journal-id JRN-001

# 6. Run Integrity Audit on Existing Report (12 checks, zero AI)
python3 <skill-dir>/scripts/fileos.py audit \
  --input "<output-folder>" \
  [--root "<target-folder>"]

# 7. Launch Local Review Dashboard (Hinglish/Hindi/English UI)
python3 <skill-dir>/scripts/fileos.py dashboard \
  --input "<output-folder>" \
  [--root "<target-folder>"]  \  # enables file diff tab
  [--port 8765]
```

---

## Dashboard Tabs

| Tab | What it shows |
|---|---|
| **Overview** | Key stats: files, folders, duplicate space, audit health |
| **Review Inbox** | All findings unified — search, paginate, mark decisions |
| **Duplicates** | Exact duplicate groups by SHA-256 |
| **Document Families** | Version clusters — select A/B paths for inline diff |
| **Folder Placement** | Hierarchy anomalies with breadcrumb path display |
| **Suggested Actions** | Proposed ACT-* actions to approve or reject |
| **Coverage** | Per-folder scan status, depth distribution, excluded dirs |
| **Review History** | Decision progress bar, timeline, copyable CLI apply command |
| **Integrity Audit** | Live 12-check audit results |

---

## Report Artifacts

Every scan produces these files in `<output-folder>/`:

| File | Contents |
|---|---|
| `coverage.json` | Scan coverage stats (discovered, scanned, excluded, depths) |
| `inventory.jsonl` | One record per file (hash, size, readiness, depth, family) |
| `folders.jsonl` | One record per folder (metrics, fit score, anomaly flags) |
| `duplicate-groups.csv` | Exact duplicate sets by SHA-256 |
| `document-families.csv` | Version/format clusters |
| `hierarchy-anomalies.csv` | Folder placement contradictions |
| `proposed-actions.json` | Proposed ACT-* actions (dry-run only) |
| `ai-usage.json` | AI token budget ledger |
| `summary.md` | Human-readable scan summary |
| `unresolved-review-queue.json` | Edge cases queued for model review |

---

## Agent Workflow for User Requests

When a user asks: *"Organize this folder"* or *"Analyze files in this directory"*:

1. **Scan & Plan First:**
   Execute `scan` then `plan`. The scan auto-audits and prints 12-check results. Never modify the user's files during discovery.

2. **Present Findings:**
   Read `<output-folder>/summary.md` and present a concise summary:
   - Coverage metrics (dirs scanned vs. skipped, files discovered).
   - Exact duplicates and potential space savings.
   - Document families with authoritative versions flagged.
   - Edge-by-edge hierarchy contradictions and mixed-topic folders.
   - Unresolved review packets from `unresolved-review-queue.json`.

3. **Offer Dashboard:**
   ```
   Launch the local review dashboard for a visual walkthrough:
   python3 fileos.py dashboard --input <output-folder> --root <target>
   Open: http://127.0.0.1:8765
   ```

4. **Model Adjudication (if queue present):**
   Evaluate bounded excerpts (Pass 1 max 2,000 chars) and recommend:
   - `confirm_exception`: Retain folder as intentional exception.
   - `move_folder`: Relocate folder to suggested project.
   - `split_contents`: Folder is mixed-topic; address individual files.

5. **Approval Gate:**
   Present Action IDs (`ACT-001`, `ACT-002`, …) and ask which to execute.

6. **Safe Apply:**
   Only execute `apply` with the exact IDs the user explicitly confirms.

---

For detailed decision rules and schemas, see:
- [DECISION_TREE.md](references/DECISION_TREE.md)
- [OUTPUT_SCHEMA.md](references/OUTPUT_SCHEMA.md)
