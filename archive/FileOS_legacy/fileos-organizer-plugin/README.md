# FileOS Organizer Plugin

A local-first, deterministic-first file organization skill and plugin for Antigravity and Agentic CLI environments.

FileOS organizes files and identifies structure anomalies without feeding large document trees to LLMs. All routine inventory, hashing, duplicate grouping, version parsing, and recursive tree traversal is handled in Python using only the standard library. The model is called only to adjudicate ambiguous edge cases using strictly bounded excerpts.

---

## Key Features

- **Recursive by Default:** Traverses entire directory trees to the deepest reachable leaf level (e.g. 12+ levels deep) using iterative stack traversal. Optional `--max-depth` allows capping when desired.
- **Folders as First-Class Entities:** Emits `folders.jsonl` with direct vs. descendant file counts, folder hierarchy edges, and token clusters. Empty folders and intermediate subfolder containers are preserved.
- **Edge-by-Edge Hierarchy Intelligence:** Independently analyzes `File -> Immediate Folder` and `Folder -> Parent Project`. Correctly isolates cases where files fit their folder, but the folder is misplaced within the parent project.
- **Document Family & Lifecycle Tracking:** Groups revisions (`v1`, `v2`) and derivatives (`.docx`, `.pdf`). Never assumes the newest file replaces an older signed or authoritative document.
- **Strict Shared AI Token Budgets:**
  - Pass 0: 0 characters (metadata and hashes).
  - Pass 1: 2,000 characters maximum per candidate.
  - Pass 2: 8,000 characters maximum per candidate.
  - Pass 3: 16,000 characters maximum per candidate.
  - Run Budget: Maximum 10 packets and 20,000 total characters per run across all file and folder candidates.
- **Safety First & Undoable:**
  - `scan` and `plan` are 100% read-only.
  - No automatic deletion.
  - `apply` requires explicit Action IDs (`--approve ACT-001 ...`).
  - Destination collisions are prevented.
  - Hashes are verified before and after every operation.
  - Reversible JSONL operation journal enables instant `undo`.

---

## Directory Layout

```text
fileos-organizer-plugin/
├── plugin.json
├── README.md
├── .gitignore
└── skills/
    └── fileos-organizer/
        ├── SKILL.md
        ├── references/
        │   ├── SPEC.md
        │   ├── DECISION_TREE.md
        │   └── OUTPUT_SCHEMA.md
        ├── scripts/
        │   └── fileos.py
        ├── tests/
        │   ├── test_inventory.py
        │   ├── test_duplicates.py
        │   ├── test_versions.py
        │   ├── test_hierarchy.py
        │   ├── test_safety.py
        │   └── test_recursive.py
        └── examples/
            └── sample_report.md
```

---

## CLI Usage

### 1. Scan (Recursive by Default, Read-Only)
Inspects a directory tree or single file, computes SHA-256 hashes, parses version tokens, detects exact duplicates, indexes all folders, and builds the AI review queue:
```bash
# Scan directory recursively (all depths)
python3 skills/fileos-organizer/scripts/fileos.py scan "/path/to/folder" --output "/path/to/report"

# Scan directory with explicit depth limit
python3 skills/fileos-organizer/scripts/fileos.py scan "/path/to/folder" --max-depth 4

# Scan a single file
python3 skills/fileos-organizer/scripts/fileos.py scan "/path/to/document.pdf"
```

### 2. Plan (Dry-Run)
Generates proposed actions without altering any filesystem files:
```bash
python3 skills/fileos-organizer/scripts/fileos.py plan --scan "/path/to/report/inventory.jsonl"
```

### 3. Report
Displays formatted Markdown summary of the scan:
```bash
python3 skills/fileos-organizer/scripts/fileos.py report --input "/path/to/report"
```

### 4. Apply (Approval-Gated)
Applies ONLY specified action IDs:
```bash
python3 skills/fileos-organizer/scripts/fileos.py apply --plan "/path/to/report/proposed-actions.json" --approve ACT-001 ACT-002
```

### 5. Undo
Reverses an applied operation and verifies destination hash:
```bash
python3 skills/fileos-organizer/scripts/fileos.py undo --root "/path/to/folder" --journal-id JRN-001
```

---

## Running Tests

All 33 tests run using Python standard library `unittest`:
```bash
python3 -m unittest discover -s skills/fileos-organizer/tests -p "test_*.py" -v
```
