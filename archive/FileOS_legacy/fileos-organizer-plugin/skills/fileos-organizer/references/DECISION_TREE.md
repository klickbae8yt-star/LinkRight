# FileOS Decision Tree & Recursive Traversal Intelligence

This document defines the deterministic rules, recursive tree traversal contracts, threshold boundaries, and progressive disclosure escalation paths used by the FileOS engine.

---

## 1. Recursive Directory Traversal & Coverage Contract

1. **Default Unlimited Recursion:**
   - Any directory input triggers recursive traversal to the deepest reachable leaf directory.
   - Iterative traversal prevents stack/call recursion limits on deeply nested directories (e.g. 12+ levels deep).
   - Alphabetical sorting of directory and file entries ensures deterministic, reproducible scans.

2. **Folder as a First-Class Indexed Entity:**
   - Every folder (including empty folders and intermediate container folders) is assigned a `folder_id` and indexed in `folders.jsonl`.
   - Separate accounting for `direct_*` (files/folders directly in this folder) and `descendant_*` (all files/folders in the nested subtree).

3. **Coverage Accounting:**
   - Tracks directories discovered, scanned, excluded, inaccessible, and depth-capped.
   - Tracks files discovered, eligible, analysed, skipped, and failed.
   - Scan is marked `complete` only if zero directories or files were omitted without explicit user scope. Otherwise labeled `partial` with specific reasons enumerated.

4. **Depth Constraints & Boundaries:**
   - `--max-depth <int>`: Optional flag (root = depth 0). Directories beyond max depth are recorded as `depth_limit_reached` in coverage.
   - Symlinks: Skipped by default (`readiness="skipped_symlink"`). If `--follow-symlinks` is enabled, inode tracking `(st_dev, st_ino)` prevents infinite loops.
   - Mount boundaries: Cross-device directory transitions (`st_dev` change) are skipped as `boundary_not_scanned` by default.

---

## 2. Hierarchy Relationship & Edge Evaluation

For any path `Ancestor.../Parent/Child`:

1. **Child -> Parent Evaluation:**
   - Evaluated independently from Parent -> Grandparent.
   - Token overlap between Child filename (normalized) and Parent folder name.
   - Direct-child coherence: If >= 60% of sibling files share common tokens or prefix with Child and Parent.
   - Status assignment:
     - `confirmed`: Explicit user rule exists.
     - `supported`: Overlap >= 0.70 with valid signals.
     - `uncertain`: Overlap between 0.40 and 0.69, or single-file folder.
     - `conflicting`: Strong token match to another project, or negative contradiction score.
     - `unknown`: Empty folder, generic names (`misc`, `new folder`, `temp`, `files`), or score < 0.40.

2. **Parent -> Grandparent (Project) Evaluation:**
   - Evaluated independently from Child -> Parent.
   - A folder `Folder Y` may be strongly supported by its child files `File Z`, but `Folder Y` may conflict with `Project X`.
   - Never propagate `File Z -> Folder Y` support upward to validate `Folder Y -> Project X`.

3. **Mandatory Acceptance Case (`Project X / Folder Y / File Z`):**
   - If `File Z -> Folder Y` is `supported` AND `Folder Y -> Project X` is `conflicting`:
     - Highlight anomaly attached to the exact edge: `Project X / Folder Y -> Project X`.
     - Action proposed: `review_and_relocate_folder` or `relationship_only`. Do NOT move anything automatically without explicit approval.

4. **Mixed-Topic Folders:**
   - Folders with >= 4 files containing diverse, uncorrelated topics with no dominant token cluster are flagged as `mixed_topic`.
   - Action proposed: `split_contents` (address individual files), never whole-folder moves.

---

## 3. Progressive AI Escalation & Shared Budget

| Pass | Max Characters | Trigger Condition | Exit Rule |
|---|---:|---|---|
| **Pass 0** | 0 | Deterministic rules (inventory, hashes, filenames, tokens) | If confidence >= 0.70 or status is `supported`/`confirmed`, stop. |
| **Pass 1** | 2,000 | Ambiguous document identity or hierarchy conflict | Extract first 2,000 chars of text/metadata. Model returns JSON decision. |
| **Pass 2** | 8,000 | Pass 1 returned `uncertain` or requested `more_excerpt` | Extract up to 8,000 chars with headings and key snippets. |
| **Pass 3** | 16,000 | High-impact conflict still unresolved + explicit user request | Extract up to 16,000 chars. If still inconclusive, record `unknown` and ask user. |

### Shared Hard Run Budgets (Files + Folders):
- Max 10 packets per run.
- Max 20,000 characters total across all packets.
- Max 5 candidates escalated to Pass 2.
- Max 2 candidates escalated to Pass 3.
- Metadata-only folder packets share the 10-packet limit without consuming excerpt characters.
