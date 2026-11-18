# Self-Prompt: FileOS Dependency Guard

Who reads this: me (Claude), before I write any code for this feature.
Target code: `fileos-organizer-plugin/skills/fileos-organizer/scripts/fileos.py`.
Date: 11 Nov 2026.

---

## 1. The problem in one story

A file sits in a place for a reason.
A script opens `data/prices.csv`.
A web page loads `img/logo.png`.
A launchd job runs `~/tools/backup.sh`.

FileOS moves or deletes that file.
Nothing warns anyone.
The script breaks the next morning.

This must never happen because of FileOS.

## 2. What the user wants

For every file FileOS wants to move, rename, archive or delete:

1. **Who needs this file?** (inbound links, "dependents")
   If this file goes away, which files, jobs or links break?
2. **What does this file need?** (outbound links, "dependencies")
   If this file moves, which of its own paths stop working?
3. **What should I do?** One clear suggestion, in plain words.
   The user must never be confused about the next step.

## 3. What exists today (checked in the code, 11 Nov 2026)

- Spec section 8.4 asks for "dependency awareness". It is not built.
- `plan` writes `"dependency_check": "not_supported"` for duplicates. That is honest.
- `plan` writes `"dependency_check": "checked_no_deps"` for hierarchy items
  (`fileos.py`, near line 1366). **This is hardcoded. No check runs. It is a false claim.**
  Fix this first.
- `apply` checks: source exists, no collision, hash unchanged, not authoritative.
  It does not check who uses the file.
- Symlinks are skipped during scan. Nobody asks "does a symlink point at this file?"
- `.git` folders are excluded. Nobody asks "is this file tracked by git?"

## 4. Rules I must follow

1. **Radar first.** Before any new code, run:
   `python3 ~/Documents/AGI/plugins/radar/scripts/scout.py --need "find which files reference a given file path, so moving or deleting it does not break code"`
   plus a GitHub `topic:` search (dependency-graph, reference-finder).
   Read the top 3 READMEs. Write the run in `FileOS/docs/research/repo-radar.md`.
   Reuse or borrow if anything fits. Build only if nothing fits, and say so.
2. **Python standard library only.** Same as the rest of FileOS.
3. **No AI in this feature.** Every check is plain code. Low tokens, no cost.
4. **Read-only by default.** Finding links never changes a file.
5. **Never say "safe" without proof.** If a check did not run, say so.
6. **Test first (TDD).** Write a failing test. Watch it fail. Then write code.
7. **Small steps.** One milestone at a time. Tests pass before the next one.

## 5. How links are found (all plain code)

Each found link is one **edge**: `from_file` → `to_file`, with `kind`, `line`, `evidence`, `confidence`.

### Layer A: inside the scanned folder

| Kind | Where it hides | How to find it |
|---|---|---|
| `python_import` | `import x`, `from .x import y` | `ast` module, resolve to a `.py` file |
| `js_import` | `import ... from './x'`, `require('./x')` | regex, resolve with `.js/.ts/.json/index.*` |
| `path_string` | `open("data/x.csv")`, `"./config.yaml"` in any text file | regex for path-like strings, resolve from the file's folder and from root |
| `html_css` | `src=`, `href=`, `url(...)` | regex |
| `markdown_link` | `[a](../x.md)`, `![](img.png)` | regex |
| `notebook` | paths inside `.ipynb` cells | read JSON, then the `path_string` rule |
| `manifest` | `package.json` main/bin/scripts, `pyproject.toml`, `requirements.txt -r`, `Dockerfile COPY`, `docker-compose` volumes, `Makefile`, `tsconfig` paths | small parser per format |
| `office_link` | `.docx/.xlsx/.pptx` external links | `zipfile`, read `_rels/*.rels` with `TargetMode="External"` |
| `symlink_in` | a symlink inside root that points at the file | `os.readlink` on every skipped symlink |

### Layer B: outside the scanned folder (opt-in, `--check-outside`)

Things outside the folder can also break. These are listed, read only, never changed:

- `~/Library/LaunchAgents/*.plist` (paths in `ProgramArguments`, `WorkingDirectory`)
- `crontab -l`
- shell files: `~/.zshrc`, `~/.bashrc`, `~/.zprofile`
- symlinks in the home folder that point into root (bounded search, time cap)

### Layer C: special places (the file is part of something bigger)

- **Git repo:** the file is inside a git work tree and is tracked.
  Moving it changes the repo. Suggest `git mv`, inside the same repo only.
- **Project root:** a folder with `.git`, `package.json`, `pyproject.toml`, `Cargo.toml`
  and similar is one unit. Never pull single files out of it.

### What I cannot see (must be reported, never hidden)

- Paths built at run time: `f"{base}/{name}.csv"`, `os.path.join(x, y)`, globs.
  Mark the file that does this as `dynamic_paths_present`.
  Any file in its reach gets `partial` coverage, not `none_found`.
- Finder aliases (binary bookmark data): `not_supported` in v1.
- Apps that remember recent files, databases, cloud links, other computers.

## 6. The dependency status (replaces the hardcoded value)

Every planned action gets one of these. No other values.

| Status | Meaning | Can it auto-move? |
|---|---|---|
| `refs_found` | One or more files or jobs use it. | No. Blocked until the user picks a fix. |
| `none_found_full` | All checks for this file type ran. Nothing found. | Yes, after approval. |
| `partial` | Some checks ran. Dynamic paths or unsupported types nearby. | Only with an extra warning. |
| `not_checked` | The check did not run. | No "safe" wording allowed. |

## 7. What FileOS suggests (one choice first, always)

| Situation | First suggestion | Other choices |
|---|---|---|
| Others use this file | **Keep it where it is.** | Move and update the links (show each change). Move and leave a symlink at the old place. |
| File is in a git repo or project root | **Keep it. Use git or the project's own tools.** | `git mv` inside the same repo. |
| Delete, but others use it | **Do not delete.** | Move to FileOS quarantine (can restore). Delete only after the user fixes the links. |
| File needs other files (outbound) and moves | **Move it with the files it needs**, or update its paths. | Keep it where it is. |
| Nothing found, full check | Move as planned. | Keep it. |
| Partial check | Keep it, or move and run the user's test command after. | Move anyway, with the warning shown. |

**Update the links** is a separate action:
- FileOS shows a before and after for every line it will change.
- The user approves it by its own action ID.
- It is journalled and `undo` puts the old lines back.
- It never edits a file outside root.

## 8. How it talks to the user

Every flagged file gets one card. Grade 5 English. No jargon.

```
prices.csv  (data/prices.csv)

3 files use this file:
  - scripts/report.py, line 12: open("data/prices.csv")
  - notebooks/check.ipynb, cell 4
  - launchd job "com.me.report" (outside this folder)

If you move or delete it, these 3 will break.

What we suggest: keep it where it is.

Your choices:
  [A] Keep it here (recommended)
  [B] Move it and update the 2 files (see changes first)
  [C] Move it and leave a link at the old place

We checked: code, notebooks, config, launchd jobs.
We could not check: Finder aliases, apps that remember recent files.
```

Rules for the card:
- Say what breaks, in their words, with the line.
- Say what we checked and what we could not check.
- One suggestion marked "recommended". At most 3 choices.
- Never say "safe" when the status is `partial` or `not_checked`.

## 9. New outputs and commands

- `dependencies.jsonl` in the report folder: one edge per line.
- `scan --deps`: build the edges during scan.
- `deps <path>`: show in-links and out-links for one file. Fast, read only.
- `plan`: every move, rename, archive or delete action carries
  `dependency_status`, `dependents[]`, `dependencies[]`, `suggestion`, `choices[]`.
- `apply`: **re-check links for that one file right before it acts.**
  New link found since the scan = stop, explain, ask again.
- `apply` after a move: re-resolve every edge that touched the file.
  Any broken edge = undo at once and report.
- Optional `--verify-cmd "<cmd>"` (for example `pytest`): run it after apply,
  only if the user gives it. Fail = undo.
- Report and dashboard: a "Who uses this file" section with the cards.

## 10. Milestones (each one: red test, green code, all old tests pass)

- **D0.** Radar run, recorded. Remove the hardcoded `checked_no_deps`. Use `not_checked`. Test that no action claims a check that did not run.
- **D1.** Edge finder, Layer A: `path_string`, `python_import`, `markdown_link`, `html_css`, `symlink_in`. Write `dependencies.jsonl`. `deps <path>` command.
- **D2.** Status per action and the suggestion table. Cards in the report.
- **D3.** Apply gate: re-check before acting, block on `refs_found`, quarantine instead of delete.
- **D4.** "Move and update links" action with diff, journal and undo.
- **D5.** Layer B (outside root, opt-in) and Layer C (git, project roots). JS imports, manifests, notebooks, office links.
- **D6.** Dashboard tab. `--verify-cmd`.

## 11. Test fixtures I must build

1. `report.py` opens `data/prices.csv`. Move the CSV: blocked, card names `report.py` line.
2. `app.py` does `from utils import helper`. Move `utils.py`: blocked.
3. `index.html` loads `img/logo.png`. Edge found.
4. `README.md` links `docs/setup.md`. Edge found.
5. A symlink `latest.csv` points at `data/prices.csv`. Edge found.
6. A file builds a path with an f-string. Status `partial`, never `none_found_full`.
7. A lonely `notes.txt` with no links. Status `none_found_full`.
8. Delete a used file: blocked, quarantine offered.
9. Move with "update links": both lines changed, `undo` restores both, hashes match.
10. A new link appears after scan, before apply: apply stops.
11. A launchd plist outside root names a file (only with `--check-outside`): edge found.
12. A file inside a git repo: Layer C flag, `git mv` suggested.

## 12. Done means

- All 12 fixtures pass. All old tests still pass.
- No action anywhere says a check ran when it did not.
- A user reading one card knows what breaks and what to click, without help.
- Scan time on a 10,000 file folder grows by less than 2x with `--deps`.
- No AI call, no network, no new package.

## 13. Not in scope (v1)

- 100 percent proof for every file type. We say what we checked.
- Reading inside databases, cloud apps or other computers.
- Finder alias decoding.
- Changing any file outside the scanned root.
