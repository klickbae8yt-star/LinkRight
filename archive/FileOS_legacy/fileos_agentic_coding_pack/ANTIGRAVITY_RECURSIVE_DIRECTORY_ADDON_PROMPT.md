# Add-on Prompt — Extend FileOS to Recursively Analyse Complete Directory Trees

You are Google Antigravity, acting as a senior Python engineer and agent-skill maintainer. Extend the **existing FileOS Organizer skill/plugin in this workspace** so that it works on complete folder trees, not merely on individual files or a single directory level.

This is an implementation task. Inspect the existing skill, scripts, tests, and `FILEOS_LOW_TOKEN_SKILL_SPEC.md`; then modify the existing implementation in place. Do not create a second unrelated skill or replace working functionality. Preserve all existing low-token, deterministic-first, read-only-by-default, approval, journaling, and undo requirements. Treat the existing specification as the baseline contract and this prompt as an additional mandatory requirement.

## 1. Exact outcome required

When the user provides a root directory, FileOS must:

1. Start at that selected root directory.
2. Discover every real subdirectory under it, including nested subdirectories at any depth, until each reachable leaf directory has been visited.
3. Inventory every eligible file in every discovered directory, including files several levels below the root.
4. Analyse **folders as first-class entities**, not merely as paths used to locate files.
5. Analyse the relationship between every folder and its immediate parent folder, and between every file and its immediate parent folder.
6. Build enough bottom-up and top-down context to identify cases where a file fits its immediate folder but that folder does not fit its parent project.
7. Produce one consolidated report for the selected tree, with coverage information and findings grouped by directory path/depth.

The default directory scan must be recursive. There must be no arbitrary default depth limit such as 1, 2, 3, or 5. If a user explicitly supplies `--max-depth`, honour it and clearly report what was not scanned. Otherwise, scan to the deepest reachable level.

**Do not interpret “recursive” as “scan the root folder and its immediate children only.”** The scan must continue through grandchildren, great-grandchildren, and every further level.

## 2. First diagnose the current limitation

Before coding:

- Inspect the existing CLI argument handling and identify why the current skill only processes individual files or shallow paths.
- Inspect the traversal implementation, directory filters, path handling, and tests.
- Reproduce the issue with a synthetic nested directory tree.
- Record the root cause briefly in the implementation notes or README.
- Fix the actual cause rather than adding a second scanning pathway that behaves differently.

Do not read the entire repository into model context. Use directory listings, targeted search, `--help`, and focused source ranges. Use Python tests/scripts for exhaustive checks.

## 3. Recursive traversal contract

Implement a robust traversal engine with these requirements:

- Accept a selected **file path or directory path**. A file input retains the existing single-file workflow. A directory input invokes recursive tree scanning by default.
- Treat the selected directory as the scan root. Store paths relative to this root in reports and AI packets; do not expose unnecessary absolute paths.
- Visit all descendant directories to the deepest reachable level unless the user configures a depth limit or an exclusion.
- Use an iterative traversal or another implementation that will not fail merely because a directory tree is deeply nested. Do not rely on Python recursion for filesystem depth.
- Sort entries deterministically so repeated scans produce stable reports.
- Keep file and directory records distinct. Do not mistake a directory for a file or hash directory metadata as though it were file content.
- Preserve Unicode names, spaces, punctuation, and platform-specific path separators safely.
- Never follow symlinks by default. Record each skipped symlink and its target/type where safe. Prevent symlink loops if the user explicitly enables following links.
- Do not silently skip unreadable or inaccessible directories. Record the path-relative identifier, error category, and reason in the coverage report; continue scanning other accessible branches.
- Respect existing exclusions for system/cache/runtime folders and user-configured exclusions. Every excluded directory must be counted and reported with its exclusion reason. Do not silently introduce broad exclusions that hide ordinary user folders.
- Hidden folders must not be skipped merely because they are hidden. Apply only explicit/known system exclusions; otherwise scan them and mark them as hidden in metadata.
- Do not accidentally escape the selected root through `..`, symlinks, junctions, aliases, or path canonicalisation.
- Treat incomplete downloads, temporary files, active/unstable files, cloud placeholders, and unreadable files according to the existing safety spec. Record skipped items rather than pretending they were analysed.
- Avoid scanning special files, sockets, pipes, device nodes, or other non-regular filesystem objects as normal documents.
- Do not silently cross into unrelated mounted volumes or network shares. Detect mount/boundary transitions and make the policy explicit in CLI options. If the default safely skips a boundary, show it prominently as `boundary_not_scanned` and provide a documented opt-in to include it. A user-selected root that itself resides on an external/network volume must still be scanned within that selected root.

### CLI behaviour

Adapt the existing CLI instead of inventing a parallel interface. The resulting behaviour should be equivalent to:

```bash
# Recursive scan is the default for directory inputs
python fileos.py scan "/path/to/root-directory"

# Explicit depth cap (root is depth 0; direct children are depth 1)
python fileos.py scan "/path/to/root-directory" --max-depth 4

# Optional explicit exclusions / inclusion controls, using the project's established CLI style
python fileos.py scan "/path/to/root-directory" --exclude "node_modules,.git,Library/Caches"

# A single-file input remains supported
python fileos.py scan "/path/to/a-document.pdf"
```

The command names/flags may follow the existing CLI conventions, but the semantics above are mandatory. `--recursive` may exist for clarity, but directory scans must be recursive even when the flag is omitted. If a non-recursive mode is supported, it must require explicit user opt-in and must never be the default.

## 4. Folder-first data model

Create or extend a `FolderRecord` (or equivalent) as a first-class indexed entity. At minimum store:

- stable `folder_id`;
- root-relative path and display name;
- parent folder ID;
- depth from scan root;
- direct child folder IDs;
- direct file IDs;
- direct file count and descendant file count;
- direct child-folder count and descendant-folder count;
- aggregate size where safely computable;
- extension/type distribution;
- hidden/system/excluded/accessibility status;
- scan status and last scan time;
- errors or skipped-reason records;
- compact deterministic name/content/context signals;
- relationship status and evidence for its edge to its parent.

Keep `direct_*` values separate from `descendant_*` values. Do not allow a large, unrelated nested subtree to make the immediate folder look coherent merely because its aggregate tokens dominate the entire parent.

A folder can contain other folders and files. Empty folders must remain represented in the tree. Do not drop them because they have no files.

Store the full inventory and tree index in machine-readable output (JSON/JSONL or the existing database). Do not paste the entire file/folder inventory into the model context. Reports shown to the user should be concise and navigable.

## 5. Folder context and recursive hierarchy intelligence

Run two deterministic context passes:

### A. Bottom-up folder summarisation

Starting from leaf folders and moving towards the root, create a compact summary for each folder using:

- folder name and path tokens;
- names of direct child folders;
- names/types of direct child files;
- direct-child type/extension distribution;
- lightweight file metadata and cheap local fingerprints already produced by FileOS;
- compact summaries of child folders;
- counts, sizes, date ranges and other deterministic metadata.

Keep direct-child evidence distinct from inherited descendant evidence. Track where every signal came from so the report can explain a mismatch.

For large folders, cap the summary deterministically (for example, top frequent file types, selected representative filenames, newest/largest samples, and compact token counts). The full inventory remains on disk. Do not pass thousands of child names to the model.

### B. Top-down parent-context evaluation

Starting at the selected root and moving down, evaluate each folder in the context of its parent and relevant ancestor project/topic folders. Use the parent's name, sibling-folder patterns, user-confirmed project labels, and previously established relationships as context.

Do not assume that every root folder is a project. A root may be a general Downloads, Documents, Desktop, archive, or mixed workspace directory. Infer a project/subject anchor only when supported by evidence or user confirmation.

### Mandatory edge-by-edge checks

Independently evaluate:

1. **File → immediate parent folder** for every eligible file.
2. **Child folder → immediate parent folder** for every non-root folder.
3. **Folder/subtree → relevant ancestor project/topic** where the ancestor is a supported project or context anchor.

Do not propagate a positive relationship upward automatically. Each edge needs its own evidence and result.

The mandatory regression scenario is:

```text
Root/
└── Project X/
    └── Folder Y/
        └── File Z
```

Expected result must be possible and test-covered:

- `File Z → Folder Y`: `supported` or `confirmed` because Z fits Y.
- `Folder Y → Project X`: `conflicting` or `uncertain` if Y's own identity/content does not fit X.
- The system must explicitly explain that the child file's good fit with Y does **not** prove that Y belongs in X.
- Suggested action may be to review/move Y, reassign Y to another project, split Y, or ignore the finding. Do not move anything automatically.

### Relationship states

Use the existing schema where possible, but support at least:

- `confirmed` — explicitly established by the user;
- `supported` — good deterministic evidence;
- `uncertain` — insufficient or mixed evidence;
- `conflicting` — meaningful evidence contradicts the parent relationship;
- `unknown` — no adequate evidence;
- `not_evaluated` — not analysed due to an explicit limit/exclusion/error.

Do not label `unknown` as `conflicting`.

### Special folder cases

- **Empty folder:** preserve it; relationship is usually `unknown`, not conflicting.
- **Generic folder name** (`New Folder`, `Misc`, `Others`, `Temp`): rely on contents and context; do not overclaim from the name.
- **Mixed-topic folder:** mark `mixed`/`uncertain`, show evidence clusters, and suggest reviewing individual children rather than moving the entire folder.
- **One-file folder:** do not confidently infer a project or mismatch from one weak signal.
- **Nested coherent subtree under unrelated parent:** flag the exact parent-child edge where the mismatch starts.
- **Folder name fits parent but contents do not:** surface a content-vs-name contradiction.
- **Contents fit parent but folder name is misleading:** surface the evidence and offer a rename suggestion, but do not rename automatically.
- **Multi-project documents:** allow a logical document/file to relate to multiple projects; do not force it into one folder solely to make the tree look tidy.

## 6. Low-token and low-compute rules for full trees

Recursive scanning must not multiply AI calls by the number of files or folders.

### Deterministic-only operations

The following must be handled in Python without AI:

- recursive enumeration and sorting;
- directory/file counts and depth calculation;
- folder tree construction;
- relative path and parent-child edge creation;
- metadata extraction;
- hashing and exact duplicate detection;
- extension/type distribution;
- filename normalization and obvious version token parsing;
- compact token/frequency summaries;
- folder aggregation and deterministic scoring;
- exclusions, permissions, symlink and mount-boundary handling;
- report generation and coverage accounting.

Never ask the LLM to walk the tree, enumerate children, count files, or construct the complete tree from pasted paths.

### AI escalation for folders

Only escalate a folder or folder-edge when:

1. deterministic signals disagree or are too weak;
2. the folder has enough meaningful evidence to interpret;
3. resolving the ambiguity materially improves organization or avoids a risky action; and
4. the case fits the existing scan-level AI budget.

Use compact folder packets with:

- folder ID and root-relative label;
- depth and parent label;
- direct-child summary;
- compact descendant summary;
- sibling/ancestor context needed for the exact edge;
- evidence that supports and contradicts the relationship;
- only the smallest representative child-file excerpts needed.

Do not send one packet for every folder. Group related ambiguous edges where doing so does not blur the decisions. A packet must identify each edge separately.

The existing AI budgets from `FILEOS_LOW_TOKEN_SKILL_SPEC.md` remain hard caps. Folder packets and file packets share the same limits; do not create a separate folder budget or exceed the combined limits. In particular, preserve the 10-packet and 20,000-excerpt-character per-run caps unless the user explicitly changes the configuration. Metadata-only folder packets should not be counted as excerpt characters, but they still count as AI packets if sent to the model.

Use the same progressive excerpt policy already specified: start with 2,000 characters for a selected unresolved candidate; expand to 8,000 total only when necessary; 16,000 total only for exceptional/high-impact cases, always subject to the scan-wide character budget. Reuse already-extracted excerpts and cached decisions. Do not re-read or re-send unchanged content.

If the budget is exhausted, leave remaining folder edges `uncertain`/`not_evaluated`, explain the reason, and allow a later targeted review. Never silently expand the budget.

## 7. Full-tree report and coverage contract

The report must include:

### Scan overview

- selected root label;
- recursive mode and configured maximum depth (or `unlimited`);
- scan start/end time;
- total directories discovered, scanned, excluded, inaccessible, and not scanned;
- total files discovered, eligible, analysed, skipped, and failed;
- deepest discovered depth and deepest successfully scanned depth;
- total bytes hashed/read where available;
- symlinks skipped, mount boundaries skipped, cloud placeholders skipped, and permission errors;
- whether the scan is complete or partial, with exact reasons.

### Tree overview

- a compact folder tree with depth markers;
- per-folder direct and descendant counts;
- folder relationship status to parent;
- notable file/folder anomalies;
- mixed or ambiguous folders;
- empty folders and inaccessible branches where relevant.

### Findings

Group findings by:

- root-relative folder path;
- depth;
- finding category (`hierarchy_mismatch`, `mixed_folder`, `misleading_name`, `document_family`, `duplicate`, `missing_context`, etc.);
- confidence/status;
- evidence;
- suggested next step.

Show the exact edge involved, for example:

`Project X/Folder Y → Project X` — conflicting relationship.

Do not only show a generic alert such as “Folder issue detected.”

### Coverage honesty

- A scan is `complete` only if every in-scope directory was enumerated and every eligible file was processed or explicitly accounted for.
- If any path was excluded, inaccessible, beyond a user-specified depth, blocked by a mount boundary, or skipped for another reason, label the scan `partial` and enumerate those reasons.
- Never report “all files analysed” when some were skipped or not readable.
- Provide a machine-readable coverage section in the JSON output.

## 8. Performance and incremental scanning

- Use incremental scanning and cache directory/file fingerprints where available.
- Avoid re-hashing unchanged files when reliable metadata/cache validation allows reuse; if metadata changed or cache confidence is low, re-hash.
- Recompute a folder summary when its direct children change or when a child-folder summary changes.
- A change deep in the tree should invalidate only affected ancestors, not force a full AI re-analysis of the entire tree.
- Keep memory usage bounded; do not hold all file contents in memory.
- Stream hashes and large-file reads in chunks.
- Provide progress summaries from the script, not repeated AI narration.
- Support graceful interruption and resumable scans if compatible with the current implementation.

## 9. Required tests

Add synthetic fixture tests that exercise the actual CLI and traversal engine. At minimum:

1. **Deep recursion:** files nested at least 12 directory levels are discovered and indexed by the default scan.
2. **No arbitrary depth cap:** a directory deeper than any old hard-coded limit is still scanned when `--max-depth` is not supplied.
3. **Explicit depth cap:** a user-supplied depth limit is honoured and omitted descendants are reported as `not_evaluated`/partial.
4. **Folder as an entity:** empty folders and folders containing only subfolders are represented in the index.
5. **File-to-folder versus folder-to-parent mismatch:** `Project X/Folder Y/File Z` can produce `Z → Y = supported` and `Y → X = conflicting/uncertain`.
6. **Deepest mismatch location:** a mismatch several levels below root is attached to the correct parent-child edge, not only the root.
7. **Mixed folder:** unrelated direct children result in `mixed`/`uncertain`, not an automatic whole-folder move recommendation.
8. **Hidden folder:** ordinary hidden folders are scanned unless explicitly excluded or known system/cache exclusions apply.
9. **Symlink loop:** default scan skips symlinks; explicit link-follow mode cannot loop forever or escape root.
10. **Permission/access error:** inaccessible branch is recorded while sibling branches continue; make the test platform-aware.
11. **Special files and incomplete downloads:** are not treated as normal completed documents.
12. **Unicode and spaces:** nested paths with Unicode, spaces and punctuation are preserved.
13. **Coverage accounting:** totals reconcile: discovered = scanned + explicitly skipped/not-scanned, with no silent omissions.
14. **Deterministic repeat run:** same unchanged tree produces stable ordering and equivalent findings (ignoring timestamps/run IDs).
15. **AI budget:** folder packets share the existing run-wide caps with file packets and never exceed them.
16. **No mutation in scan/plan:** recursive scans and plans never move, rename, overwrite, or delete source items.

Include a representative nested fixture tree and a sample full-tree report. Tests must not use the user's real files.

## 10. Update the skill instructions and documentation

Update the existing `SKILL.md`, references, CLI help, README and output schema so the skill clearly states:

- directory scans are recursive by default;
- all nested levels are included until the deepest reachable directory;
- folders are independently analysed as first-class entities;
- every parent-child folder edge is evaluated separately;
- `--max-depth` is optional and unlimited by default;
- exclusions, symlinks, inaccessible paths and mount boundaries are visible in coverage;
- AI budgets are shared across file and folder adjudication.

Keep `SKILL.md` concise. Place detailed traversal/hierarchy rules in a reference document and link it from `SKILL.md`.

## 11. Final validation and response

After implementation:

1. Run the complete existing test suite.
2. Run the new recursive-directory tests.
3. Run CLI `--help` and demonstrate a default recursive scan against the synthetic fixture.
4. Show a short tree report proving that the deepest nested test file was found.
5. Show the `Project X/Folder Y/File Z` edge results.
6. Verify that scan/plan did not mutate the fixture tree.
7. Summarise changed files, root cause, tests passed/failed, any platform-dependent limitations, and exact usage examples.
8. If a required test fails, fix it or explicitly report the failure. Do not claim completion without evidence.

Do not ask the user to manually enumerate folders. Do not stop at the first level. Do not solve this by asking the LLM to read all files. Implement recursive traversal and folder intelligence in Python, preserving the original low-token architecture.
