# Antigravity Build Prompt — FileOS Local Review Dashboard

## Mission

Extend the **existing FileOS skill/plugin and Python CLI in place** with a local, evidence-first review dashboard. The dashboard must let a normal user inspect, understand, and manually verify every finding from an existing FileOS scan — including exact duplicate groups, likely document/version families, folder-hierarchy concerns, skipped items, AI adjudications, and proposed actions.

This is an add-on to the existing FileOS implementation. Do not create a separate product, a parallel skill, or a second analysis engine. Reuse the current scan outputs, IDs, evidence records, confidence/scoring logic, action plan, and safety model. First inspect the repository and actual report schemas. Do not assume JSON property names or invent missing evidence.

The example scan to support is the existing `LinkRight` report, which reports approximately 18,196 discovered files, 773+ directories, 18,113 ready/analyzed files, 83 skipped/excluded/unstable items, 2,689 exact duplicate groups, 2,361 document families, 255 hierarchy findings, and 2,944 proposed actions. These are **unverified report claims**, not ground truth. The dashboard must audit their internal consistency and expose the underlying evidence. Do not hardcode these counts.

## Product principle

**FileOS should speak like a helpful person, not like a filesystem engineer.**

Default interface language: **simple Hinglish**, because that is the user's chosen working language. Provide a visible language switch for:
- Hinglish (default)
- Hindi
- English

Use deterministic translation dictionaries and authored UI copy. Do not call an AI model to translate, explain, summarize, or render dashboard text. The dashboard must consume **zero AI tokens**.

Technical evidence must remain accessible behind an expandable `Technical details` / `Technical jaankari` section. Do not remove technical traceability; make it progressively visible.

## Non-negotiable safety and privacy rules

1. Dashboard startup, browsing, filtering, sorting, opening details, and saving review decisions must never move, rename, overwrite, or delete source files.
2. Keep the source scan root read-only. Store dashboard review state and any generated dashboard cache only in the external report directory or another explicit FileOS state directory.
3. Do not automatically run a new scan when the dashboard opens. The dashboard loads an already-generated report directory.
4. Do not re-read every source file merely to render the dashboard. Load report artifacts and evidence lazily. Open or compare source content only when the user explicitly requests it and the existing parser supports it.
5. Do not upload, transmit, or expose scan content to external services. Dashboard mode is local-only and uses no remote API, analytics, telemetry, external fonts, CDN, or hosted assets.
6. Bind the server to `127.0.0.1` only by default. Do not bind to `0.0.0.0` or the LAN. Print the exact local URL and the report path at startup.
7. Do not execute arbitrary shell commands from UI-provided paths. Treat report data and file paths as untrusted input. Escape all rendered text, prevent path traversal, and validate all report-relative paths against the scan root before any optional local-open operation.
8. Dashboard review decisions are not filesystem actions. Marking a finding `Correct` or `Incorrect` must not execute its proposed action.
9. Keep the existing explicit CLI approval gate. In this dashboard milestone, do not add a one-click bulk apply feature. The dashboard may show a copyable command for explicitly approved action IDs, but only the existing `fileos.py apply --approve ...` path may execute changes.
10. Never permanently delete files. Preserve existing quarantine/archive/undo rules.

## First task: inspect before changing code

Before implementation:

1. Inspect the repository tree, `SKILL.md`, linked references, CLI entry point, report generator, scan schema, `proposed-actions.json`, duplicate output, version-family output, hierarchy output, coverage output, AI usage ledger, and tests.
2. Run existing tests and record the baseline result.
3. Inspect a real report directory if accessible. If the actual LinkRight report directory is not present, do not fabricate it. Use the supplied scan summary only as a scenario and build a clearly labelled synthetic fixture.
4. Map every current report artifact to the UI screen that will consume it. If a required evidence field is not currently recorded, add it to future scan outputs and show older reports as `Evidence unavailable in this scan` rather than guessing.
5. Preserve backward compatibility with existing report directories where feasible. Add schema-version handling and clear errors for unsupported schemas.
6. Do not change scan results or scoring thresholds merely to make the dashboard look better.

Write a short implementation note listing existing schemas, missing evidence, baseline tests, and chosen UI approach before coding.

## Dashboard information architecture

Create a simple, calm, non-intimidating dashboard with these main areas. All findings must be discoverable; do not show only a sample or top results.

### 1. Home — `Your files at a glance`

Show:
- Scan folder name (not the full absolute path by default)
- Scan date and time
- Whether the scan is complete, partial, or has unresolved coverage gaps
- Files found, folders found, files successfully inspected, skipped items, excluded areas
- Deepest level reached and the actual deepest relative path
- Exact duplicate groups, file instances involved, extra copies, estimated duplicate data
- Possible document/version families
- Folder placement concerns
- Proposed actions awaiting review
- AI activity summary

Use everyday language. Example labels:
- `Files checked` rather than `Analyzed objects`
- `Folders checked` rather than `Directory entities`
- `Files FileOS could not check` rather than `Skipped / unstable / symlink items`
- `Possible duplicate sets` rather than `Exact duplicate groups`
- `Files that may belong somewhere else` rather than `Hierarchy anomalies`
- `Suggested changes to review` rather than `Proposed actions`

Every metric must have a `What does this mean?` explanation. Do not show a green success status if the scan is partial or if important counts fail integrity checks.

### 2. Review inbox — `Things worth checking`

A single filterable list of every finding, not just every action. Include:
- Duplicate groups
- Possible versions / document families
- Folder placement concerns
- Mixed-topic folders
- Related-but-not-identical files
- Missing/uncertain context
- Skipped or unreadable items
- Conflicting or protected authoritative versions

Required filters:
- Finding type
- Review status
- Confidence band, expressed in plain language
- Folder / path prefix
- Depth level
- Impact / risk
- Has a proposed action / no proposed action
- AI used / AI not used / AI queued / AI unavailable

Required sort options:
- Highest risk first
- Needs review first
- Deepest folder first
- Largest potential storage impact first
- Path A–Z

Use server-side pagination/search or an equivalent approach. Do not send the entire inventory or all extracted document text to the browser in one massive payload. The interface must remain usable with at least 20,000 files, 3,000+ actions, and several thousand findings.

Every finding row must show a short understandable sentence, not an internal code. Example:
- `These 3 files appear to contain exactly the same data.`
- `This may be a newer version of the same document.`
- `This folder's contents fit here, but the folder may not fit its parent project.`
- `FileOS could not check this item, so no conclusion was made.`

### 3. Duplicate review — `Repeated copies`

Make every duplicate group individually reviewable.

For each group show:
- Stable finding/group ID
- Number of file instances in the group
- All relative paths, with expandable path display
- File names, formats, sizes, modified timestamps
- SHA-256 digest (short form by default; full digest in technical details)
- Whether files are byte-for-byte identical, inferred to be hard links, or whether storage semantics are unknown
- Which copy FileOS currently proposes to keep and why, if a canonical copy is proposed
- Which copies are merely candidates for review — never label them safe to delete by default
- Estimated logical duplicate bytes separately from guaranteed reclaimable physical storage
- Linked proposed action IDs, if present

Friendly explanation:
`In files ke naam ya folders alag ho sakte hain, lekin inka actual content bilkul same hai.`

Actions available to the reviewer (review metadata only):
- `Yes, these are duplicate copies`
- `No, keep them separate`
- `Not sure`
- `Reviewed — no change needed`

Never delete or move anything from these buttons.

### 4. Version review — `Possible document versions`

Make every document family and every relationship inside it individually reviewable.

For each family show:
- Family ID and all member files
- Proposed relationship for each relevant pair/edge: possible revision, alternate format, exported copy, signed/approved version, branch/alternative, related document, or unrelated
- Relative path, filename, extension, size, modified time, available document dates/authors
- Evidence used: filename/version tokens, metadata, content fingerprint, text similarity, structural diff, archive/package relationship, or AI adjudication
- A simple timeline where ordering evidence exists; do not treat modified time alone as proof of version order
- Side-by-side or unified text comparison when extraction is supported
- Added, removed, and changed text/sections when a reliable diff exists
- Unique content in an older file that is not present in a proposed newer file
- Signed/approved/published status and any protection flags
- Extraction limitations, unsupported formats, password protection, or low-confidence parsing
- Linked proposed action IDs

Friendly explanation:
`Ye documents ek doosre se related lagte hain. Lekin zaroori nahi ki sab ek hi document ke versions hon.`

Reviewer choices:
- `Same document — newer version`
- `Same document — alternate format/export`
- `Related, but different documents`
- `Separate documents`
- `Keep both as separate versions/branches`
- `Not sure`

Do not auto-designate the newest modified file as the authoritative version. Preserve signed, approved, executed, published, and branch versions.

### 5. Folder placement review — `Does this folder belong here?`

This is a core FileOS differentiator. Make every parent-child folder edge separately reviewable, including edges at the deepest directory levels.

For each concern show a visual breadcrumb/tree, e.g.:

`LinkRight > Google career > 05_resume_portfolio > Satvik_Resume_v7 > bullet_bank`

Show the edge being evaluated clearly:
- `bullet_bank → Satvik_Resume_v7`

Separate these evidence categories:
1. Direct files inside this folder.
2. Immediate child folders.
3. Descendant content summaries (clearly labelled as inherited/descendant evidence).
4. Current parent folder's direct context.
5. Sibling folder names and contents.
6. User-confirmed relationships and previous decisions.

Do not blur direct-child evidence with descendant evidence. Do not infer that a folder is wrong merely because its name is generic or because one descendant file is unusual.

For every edge show:
- Current physical relationship
- FileOS's interpretation in plain language
- Evidence supporting the current placement
- Evidence against the current placement
- Whether this is a mixed-content folder, missing context, uncertain relationship, or a genuine conflict candidate
- Fit/confidence score components in expandable technical details; never present a heuristic score as a calibrated probability
- What could happen if the folder is moved as a whole
- Suggested next step: keep, inspect contents, split contents, relate to another project, or review a possible new location

Example user-facing copy:
`Is folder ke andar ki files ek resume bullet bank se related lagti hain. Lekin iska parent folder ek specific resume version hai. Ho sakta hai ye folder alag jagah better fit ho — pehle check kar lein.`

Reviewer choices:
- `This folder belongs here`
- `This folder belongs elsewhere`
- `Only some items belong here`
- `This folder relates to multiple projects`
- `Not enough context`
- `Ignore this suggestion`

A user decision must be saved as a review decision. It must not move the folder.

### 6. Action review — `Changes FileOS is suggesting`

Make every proposed action individually reviewable. Show:
- Action ID
- Plain-language action description
- Exact source path and destination path, if applicable
- Why FileOS suggested it
- Evidence IDs and clickable links to the underlying findings
- Risk and reversibility in plain language
- Whether the action affects a folder or multiple descendants
- Whether dependency analysis was performed, not supported, or found references
- Whether source file hashes/metadata still match the scan snapshot
- Any path conflict, permission, symlink, hard-link, sync-state, or external-drive concerns

Translate internal action types. Example:
- `move` → `Move this item to a suggested folder`
- `relationship_only` → `Link this item to a project without moving it`
- `review_duplicate` → `Review repeated copy`

Clearly distinguish:
- `Suggestion only — nothing has changed`
- `Reviewed by you`
- `Approved for a later apply step`
- `Applied` (only when verified from the actual operation journal)
- `Undone` (only when verified from the actual journal)

Dashboard v1 must not execute actions. It may store an explicit decision and generate a copyable CLI command listing only the action IDs the user has separately marked for approval. The command must use the existing `apply --approve ID...` pathway. Do not add `--yes`, implicit bulk approval, or a bypass.

Before a user copies an apply command, show a final plain-language summary of exactly what those IDs would do. Revalidate that the current report plan is the one being referenced.

### 7. Scan coverage — `What FileOS could and could not check`

Show all coverage states with counts and paths:
- Successfully inspected
- Skipped because of unreadable/locked/in-use files
- Symlinks not followed
- Excluded folders (with the exact exclusion rule)
- Permission denied
- Unsupported file formats
- Password-protected/encrypted
- Unstable or changing during scan
- Failed parsing/hashing
- Filesystem watcher or traversal errors
- User-specified depth cap, if any

Show a browsable directory tree with per-folder status. Every skipped/excluded path must be discoverable. Never show `100% complete` when any path was not evaluated. Clearly distinguish `not scanned`, `scanned but not parsed`, `parsed`, and `AI reviewed`.

### 8. AI usage — `When FileOS needed extra help`

Dashboard rendering and all routine calculations must use no AI.

Show separate counters:
- Deterministic checks completed (no AI)
- AI cases prepared/queued
- AI cases actually sent to a model
- AI responses received successfully
- Cached decisions reused
- Cases skipped due to budget
- Cases unresolved
- Excerpt characters sent
- Input/output tokens only when the model/runtime actually provides these numbers
- Provider/model name only if captured in the scan ledger

Never infer token count from character count and never label a queued packet as a model call. If only character count is known, say so. Example:
`10 cases were prepared for review; 0 were sent to an AI model.` — only if the ledger confirms exactly that.

Every AI-assisted finding must expose which evidence was sent, the pass/character budget, the result, and whether a human has reviewed it. Do not expose personal absolute paths or sensitive document text unnecessarily.

### 9. Review history — `Your decisions`

Persist reviewer feedback outside the scanned source directory, preferably as append-only `review-decisions.jsonl` plus a small index if needed.

Every decision record must include:
- Stable decision ID
- Finding ID and related action ID(s)
- Reviewer choice/status
- Optional user note
- Timestamp
- Scan ID/report fingerprint
- Relevant evidence fingerprint/version
- Skill/schema version

Support reopening the dashboard and resuming exactly where review stopped. Show progress such as `Reviewed 37 of 255 folder concerns`.

If the scan report or evidence changes, mark a prior decision as `Needs re-check` rather than silently applying it to changed evidence. Never rewrite the original scan report or original proposed action file to store review feedback.

## Language and writing rules for the UI

- Default to clear, friendly Hinglish, not corporate or engineering jargon.
- Offer Hindi and English through a fixed language selector.
- Keep sentences short and specific.
- Use neutral phrasing: `may belong elsewhere`, `looks similar`, `needs a closer look`. Avoid absolute claims unless there is deterministic proof, such as identical SHA-256 hashes.
- Never use terms such as `anomaly`, `supersession`, `semantic edge`, `heuristic`, `entity graph`, `adjudication`, `canonicalization`, `inode`, or `confidence score` as the main user-facing headline. Explain them under technical details.
- Do not use fear-inducing warnings like `corrupt`, `dangerous`, or `wrong` unless that exact state is proven.
- Each finding needs a one-line `Why am I seeing this?` explanation and an `What can I do?` section.
- Use status text and icons in addition to color; do not rely on color alone.
- Use readable typography, responsive layout, keyboard navigation, visible focus states, and accessible contrast.

Suggested Hinglish microcopy:

| Technical concept | User-facing label | Simple explanation |
|---|---|---|
| Exact duplicate | Bilkul same copy | Dono files ka actual content same hai. |
| Possible version family | Ek hi document ke possible versions | Ye files ek doosre se related lagti hain. |
| Hierarchy mismatch | Folder shayad galat jagah hai | Is folder ka content aur iska parent alag context dikhate hain. |
| Mixed-content folder | Is folder mein alag-alag topics hain | Folder ki saari files ek hi topic se related nahi lagti. |
| Low confidence | Abhi clear nahi hai | FileOS ke paas pakka conclusion nikalne ke liye enough evidence nahi hai. |
| Skipped item | File check nahi ho paayi | FileOS is file ko access ya read nahi kar paaya. |
| Relationship only | Bina file move kiye link karein | File ko usi jagah rehne dein, bas project se connect karein. |
| Superseded | Purana version ho sakta hai | Isse replace kiya gaya ho sakta hai, lekin pehle verify karein. |
| Protected version | Is version ko preserve karein | Ye signed/approved/important version ho sakta hai. |

## Correctness and audit requirements

The dashboard is not just a visualization. It must help establish whether the scan output is internally consistent and whether each finding has sufficient evidence.

### A. Run independent report-integrity checks

Implement a deterministic `audit` layer that reads the report artifacts and checks invariants without AI. Display every failed or inconclusive check prominently.

At minimum validate:

1. File counts reconcile across discovered, eligible, analyzed, skipped, excluded, unreadable, and unsupported categories. Define whether each category is inclusive or exclusive and avoid double-counting.
2. Directory counts reconcile and the depth convention is explicit (root depth 0 or 1). Show the deepest relative path, not only a number.
3. Duplicate group count, file-instance count, extra-copy count, and byte totals reconcile.
4. For SHA-256 exact duplicate groups, every member has the same content hash and compatible size. If hash values are missing, label the evidence incomplete.
5. Duplicate storage math uses `extra copies = sum(group member count - 1)` and `logical duplicate bytes = sum(size of extra copies)`. Do not call this guaranteed disk space reclaimed. Detect/report hard links where possible; do not claim physical space savings for multiple paths to the same inode. Treat reflinks/storage deduplication as unknown unless the platform can prove otherwise.
6. If `bytes hashed` is claimed to be the total bytes read for a full uncached scan, it must be at least the bytes of the files involved in duplicate groups. If hashes are reused from cache, report `bytes read and hashed this run` separately from `bytes covered by cached hashes`. Never silently compare unlike metrics.
7. AI queue count, sent count, success count, cached count and token counts reconcile with the actual AI usage ledger. A queued packet is not a model call. Characters are not tokens.
8. Every proposed action references existing finding/evidence IDs, where required. Every action ID is unique.
9. Every finding has a stable ID, category, status, evidence references, and report/scan ID.
10. No action is labelled applied or undone unless the operation journal verifies it.
11. A scan with skipped/excluded/unreadable items is shown as partial or as complete-with-coverage-gaps, never as a perfect full-content analysis.
12. Stale plan detection: compare the action's expected file fingerprint (hash/size/mtime as available) to the current file before any separate apply operation. A changed file must be marked `scan result may be outdated`.

### B. Independent verification of deterministic findings

- Exact duplicate verification must be reproducible by an independent verifier that re-hashes the listed files (or reports cached-hash provenance clearly). Do not merely repeat the same stored answer.
- Provide an optional command such as `fileos.py audit --input REPORT_DIR` that recomputes report-level metrics and, only when explicitly requested, rechecks selected duplicate groups on disk.
- Recheck selected groups in bounded batches; do not re-hash all 18,000 files whenever the dashboard opens.
- Show a verified timestamp, method, and result. If source files changed after the original scan, mark the old finding stale.

### C. Version-family correctness

- Do not equate similar filenames, extension differences, or the presence of words like `final`, `signed`, `v2` with proof of a version relationship.
- Show the actual signals supporting each relationship.
- Make every family member and relationship edge reviewable.
- Keep signed/approved/published/executed records protected unless the user explicitly confirms otherwise.
- If text extraction is unavailable or a family combines distinct formats (for example `.skill`, `.md`, `.py`, `.zip`), label the relationship as `possible related files` until evidence demonstrates the exact relationship. Do not invent content similarity.
- Provide a reliable diff only when the parser supports it; otherwise say `A readable comparison is not available for this file type.`

### D. Folder relationship correctness

- Evaluate every parent-child edge independently, at all depths.
- Show direct content separately from descendant summaries.
- Do not call a folder misplaced solely because the folder name or one descendant differs from its parent.
- For mixed-content folders, recommend reviewing/splitting contents rather than moving the whole folder.
- Show the precise evidence behind fit/conflict scores. Scores are ranking heuristics, not probabilities.

### E. Human review and sampling

Support 100% review of all listed findings through filters, search, stable IDs, and progress tracking. Also provide a suggested audit queue that prioritizes:
- All high-impact move actions
- All signed/approved/protected version families
- All low-confidence or conflicting hierarchy relationships
- All findings involving inaccessible/unsupported content
- A stratified sample across file types, folder depths, and finding categories

Do not claim that a sample proves every finding correct. Clearly distinguish `machine consistency check`, `independent recheck`, and `human reviewed`.

## Technical implementation constraints

1. Reuse the repository's existing Python stack and conventions. First check if a local UI framework is already installed and used.
2. Avoid adding a large framework or dependencies for appearance alone. If no framework exists, prefer a lightweight local web UI using the simplest maintainable approach already compatible with the repository. Explain the trade-off in the implementation note.
3. Keep the dashboard code separate from scan/plan/apply domain logic. Dashboard reads report data and review decisions; it must not duplicate the classifier.
4. Expose a new CLI command following existing conventions, for example:

   ```bash
   python3 FileOS/fileos-organizer-plugin/skills/fileos-organizer/scripts/fileos.py dashboard \
     --input /private/tmp/fileos-scan-linkright \
     --host 127.0.0.1 \
     --port 8765
   ```

   Adapt the actual path and flags to the repository. If the path or CLI structure differs, retain equivalent semantics.

5. The dashboard must handle JSON, JSONL, and CSV report artifacts using streaming/lazy reads where sensible. It must not assume that all reports fit comfortably in memory.
6. Use stable IDs for findings and actions. Never use array position as the only identity.
7. Add report schema versioning or migrations/compatibility adapters. Do not silently misread old report formats.
8. Add graceful empty, partial, corrupt, and unsupported report states.
9. Make the page usable if optional evidence artifacts are missing; show exactly what is unavailable.
10. Do not use model calls in rendering, translations, filtering, sorting, report summaries, or audit calculations.

## Required tests

Create tests using synthetic report fixtures, not the user's private LinkRight files. Include:

### Dashboard and data loading
- Loads a report directory with all expected files.
- Loads an older/partial report and labels missing evidence accurately.
- Handles 18,000+ file records and 3,000+ actions without loading all document contents into the browser at once.
- Every finding type can be located, opened, and reviewed.
- Search, filters, sorting, pagination, and language switch work.
- Refresh/restart preserves review decisions.
- Changed report fingerprint marks old decisions as needing re-check.

### Integrity checks
- Count reconciliation passes on a valid fixture.
- Count reconciliation fails with a deliberate missing/duplicated record.
- Duplicate group counts distinguish groups, members, and extra copies.
- Duplicate byte calculation handles groups of 2, 3, and more copies.
- Hard-link paths are not counted as guaranteed reclaimable storage.
- The 211 MB versus 718.3 MB scenario is flagged if the report claims full uncached hashing; it is explained correctly if cache accounting is present.
- AI queued/sent/cached/token metrics are never conflated.
- Orphan evidence references and duplicate IDs are caught.
- Action status cannot be inferred without the operation journal.

### Finding review
- Duplicate group shows every path and matching hash evidence.
- Version family shows every member and each relationship edge.
- Folder finding shows direct vs descendant evidence and exact parent-child edge.
- Skipped items show the reason and path.
- Reviewer choices persist without mutating source files or source report artifacts.

### Safety/security
- Server binds only to 127.0.0.1 by default.
- No source file is changed by dashboard startup, viewing, review, or audit.
- No external network request is made.
- UI cannot submit arbitrary shell commands or arbitrary filesystem paths.
- HTML is escaped and path traversal is rejected.
- No dashboard button bypasses the explicit CLI approval list.

## Acceptance criteria

Do not declare the work complete until all of the following are demonstrated:

1. The existing FileOS scan and plan commands still work and their tests pass.
2. A new `dashboard` command launches the local UI against a report directory.
3. The home screen explains the scan in simple Hinglish by default.
4. User can switch to Hindi and English without any AI call.
5. All findings are individually accessible, including every duplicate group, version family, hierarchy concern, skipped item, and proposed action.
6. Each finding detail explains why FileOS flagged it and shows supporting evidence.
7. User can mark every finding as correct, incorrect, uncertain, or another appropriate category-specific choice, with a persistent review trail.
8. The LinkRight metric inconsistencies described above are either reconciled from source artifacts or clearly flagged as unresolved — never hidden.
9. Dashboard usage consumes zero AI tokens and does not re-run analysis implicitly.
10. The source tree remains untouched during scan report review.
11. All tests pass, and the final response includes exact commands to launch the dashboard and the test output summary.

## Final deliverables from the coding agent

- Updated existing FileOS plugin/skill (not a parallel skill).
- New dashboard code and any small UI assets.
- New `dashboard` CLI command.
- Deterministic report-integrity audit module.
- Persistent review-decision store outside the scan root.
- Tests and synthetic report fixture.
- Updated `SKILL.md` / references so the skill knows how to launch the dashboard and explain its review-only nature.
- README with setup, launch command, supported report versions, privacy model, language selector, known limitations, and how to apply only explicitly approved action IDs using the existing CLI.
- A completion summary listing changed files, commands run, test outcomes, unresolved issues, and whether the real LinkRight report could actually be loaded.

## Agent operating instruction

Work autonomously from the existing repository. Do not ask the user to manually map report files or list findings. Inspect the code, infer the existing structure from evidence, and implement the dashboard as an additive extension. Do not fabricate results from the LinkRight summary. If the real report folder is not available, prove the dashboard with a synthetic fixture and state that real-data validation remains pending.

**The product outcome:** A user opens `http://127.0.0.1:<port>`, sees a calm explanation of what FileOS found, can inspect every finding and the exact evidence behind it, can record their own decisions, and can be confident that nothing in the scanned folder changed just because they opened the dashboard.
