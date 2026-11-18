# FileOS v2: Full Specification (CLI + Oracle gateway + Obsidian wiki)

Status: spec only, 11 Nov 2026. Nothing is built yet. The build waits for the owner's go.
It becomes the single source of truth.
- The old `FILEOS_LOW_TOKEN_SKILL_SPEC.md` stays as the v1 engine reference. Its sections 6 to 12 still hold for the scan engine.
- The dependency-guard self-prompt is folded in here (section 9).

Reading level: short sentences. Code names stay as they are.

---

## 1. Why this exists

Files pile up in the wrong places. Copies multiply. Versions get lost. A folder sits in a project it does not belong to.
Moving a file can break a script that needs it.

FileOS reads a folder tree and tells the owner, in plain words:
- what each file and folder is about;
- what belongs together, and what sits in the wrong place;
- what is a copy or an old version;
- who uses a file, so moving it is safe or not;
- one suggested next step, which he approves by ID.

It must do this **cheaply**:
- No Claude tokens are spent on file content.
- Reading and summarizing happen on the owner's own Oracle box, with small local models, slowly, chunk by chunk.
- Fast embeddings come first. A small model writes text only where it is needed.

The output is also a **linked wiki that opens in Obsidian** (Karpathy's LLM-wiki pattern). The owner sees files and folders as a graph.

## 2. Users and surfaces

| Surface | Who | Notes |
|---|---|---|
| `fileos` CLI | Owner now; any laptop user later | The engine. Works with no Claude at all. |
| FileOS app UI (`fileos ui`) | Owner | Our own Obsidian-style screen: tree, note, graph, review inbox (section 14b). |
| Obsidian vault | Owner | Plain-markdown export of the same map. It opens in Obsidian too. |
| Claude plugin `fileos` (4 skills) | Owner inside Claude Code | Thin. Runs the CLI. Never reads file content. |
| Desktop app | Later | Calls the CLI with `--json`, and the gateway with its own key. |
| `fileos-llm` gateway | Oracle box | Public HTTPS. One key per user or install. No SSH for anyone. |

## 3. Principles (each is testable)

1. **Cheapest layer first.** Layer 0 (code) → Layer 1 (embeddings) → Layer 2 (small model). A higher layer runs only when a lower one cannot answer.
2. **Read-only by default.** `scan`, `deps`, `understand`, `wiki`, `plan`, `tidy`, `report` never change the user's files.
3. **Approval by ID.** Only `apply --approve ACT-...` changes files. Every change is journalled and undoable.
4. **Never claim a check that did not run.** Statuses say exactly what was checked.
5. **Unknown is a valid answer.** No forced move.
6. **The owner's rules beat inference.** His recorded decisions win.
7. **Secrets never leave the laptop.**
8. **State lives outside the scanned folder.** Everything goes in `~/.fileos/`.
9. **Pay once.** Every model result is cached by content hash. An unchanged file costs zero calls, forever.
10. **No vendor lock.** The client speaks the OpenAI-compatible API. Any base URL works.

## 4. Non-goals (v2)

- Entity and concept pages (the full Karpathy wiki). Small models are too weak. Later, only after an eval passes.
- Full proof of dependencies for every file type. We report coverage instead.
- Finder alias decoding, app-internal "recent files", databases, cloud links.
- Editing any file outside the scanned root.
- Accounts, billing, a hosted service for strangers.
- A Rust rewrite (only if a measured step is too slow).

---

## 5. Research behind the design (radar, 11 Nov 2026)

| Source | Score / licence | Decision |
|---|---|---|
| Karpathy `llm-wiki.md` gist (Tier A for the pattern) | idea file | **Adopt the pattern.** Raw sources are immutable → a generated markdown wiki → a schema file. Operations: ingest, query, lint. `index.md` and `log.md`. `[[wikilinks]]`. |
| Obsidian | closed app, plain-md data | **Copy the layout pattern for our own UI (14b).** The vault export stays Obsidian-compatible, so the owner can also open it there. |
| `nashsu/llm_wiki` | 61 watch, GPL-3.0 | **Borrow ideas only.** The ideas: a persistent ingest queue, folder import with folder context, a 4-signal graph (links, overlap, Adamic-Adar, type), community clusters, a review queue. No code, because GPL would spread. Too LLM-heavy for 1B models. |
| `abhigyanpatwari/GitNexus` | 57 watch, PolyForm Noncommercial | **Optional adapter, personal use only.** It is a symbol-level code graph (`impact`). Its MCP is already installed. Never shipped in a product. |
| `thedotmack/claude-mem` | Apache-2.0, installed | **Use beside FileOS, not inside it.** It mirrors the owner's decisions for Claude sessions. Borrow its 3-step progressive disclosure. |

The scorer's ranking confidence is 0.6. Nothing is adopted as code without a smoke test.
The run is recorded in `FileOS/docs/research/repo-radar.md` in P0.

---

## 6. Architecture

```
User's laptop                                         Oracle box
┌─────────────────────────────────────────┐          ┌───────────────────────────────────┐
│ Claude plugin "fileos" (thin skills)    │          │ Cloudflare tunnel llm.linkright.in│
│              │ runs                      │  HTTPS   │              │                    │
│              ▼                           │  Bearer  │              ▼                    │
│ fileos CLI  (Python 3.11+, stdlib only)  │ ───────▶ │ fileos-llm gateway 127.0.0.1:8790 │
│   L0 deterministic  scan, hash, deps     │   key    │  keys · limits · queue · aliases  │
│   L1 embeddings     fit, related, clusters│         │       │                 │         │
│   L2 small model    chunk→file→folder    │          │  Ollama :11434   embed backend    │
│   wiki writer       Obsidian vault       │          └───────────────────────────────────┘
│   ~/.fileos         cache, runs, journal │
└─────────────────────────────────────────┘
```

Facts this rests on (checked 11 Nov 2026):
- **Mac:** Python 3.12.7, `pipx`, `pdftotext`, `textutil`, numpy 1.26.
- **Box:** aarch64, 4 CPU, 22 GB. Ollama has `gemma3:270m`, `qwen3.5:0.8b`, `gemma3:1b`, `llama3.2:1b`, `nomic-embed-text` (one call 0.33 s). MiniLM ONNX is on `:8766`. Tunnel `oracle-linkright`.
- **Code today:** `fileos.py` (1,989 lines, `FileOSEngine`), `audit.py`, `similarity.py`, `dashboard.py`. 79 tests pass.

---

## 7. Package and files

```
FileOS/fileos/                  (moved from FileOS/fileos-organizer-plugin/; inside the FileOS repo, 18b)
├── pyproject.toml              [project.scripts] fileos = "fileos.cli:main"; dependencies = []
├── src/fileos/
│   ├── __main__.py   cli.py    argparse + dispatch; global --json, --quiet
│   ├── engine.py               old fileos.py (scan, plan, apply, undo, watch); imports made relative
│   ├── audit.py similarity.py dashboard.py
│   ├── paths.py                ~/.fileos layout, run dirs, latest pointer
│   ├── config.py               config.json + params.json (versioned tunables)
│   ├── extract.py              text extraction (section 10.1)
│   ├── guard.py                secret denylist + scrubber + .fileosignore (section 15)
│   ├── chunk.py                chunker (section 10.2)
│   ├── deps.py                 dependency guard (section 9)
│   ├── llm.py                  OpenAI-compatible client (section 12)
│   ├── cache.py                sqlite store (section 8.2)
│   ├── semantic.py             vectors, fit, related, clusters (section 10.3)
│   ├── summarize.py            roll-up summaries (section 10.4)
│   ├── rules.py                owner decisions (section 8.4)
│   ├── wiki.py                 Obsidian vault writer (section 11)
│   ├── tidy.py                 one-shot pipeline (section 13)
│   └── adapters/gitnexus.py    optional, personal use only
├── server/gateway.py  server/keys.py  server/fileos-llm.service  server/README.md
├── plugin/.claude-plugin/{plugin.json,marketplace.json}  plugin/skills/{fileos-tidy,fileos-deps,fileos-understand,fileos-apply}/SKILL.md
├── tests/                      old 79 tests (imports → fileos.engine) + new tests + fixtures/
├── references/                 v1 SPEC, DECISION_TREE, OUTPUT_SCHEMA, ARCHITECTURE
└── docs/research/              repo-radar.md, experiments.md
```
- `connectors/oracle_pool.py` (mock only) is removed. `llm.py` replaces it.
- `connectors/mongo_history.py` stays with its test.
- Ship: `pipx install FileOS/fileos` (dev). A single file `fileos.pyz` via `python -m zipapp` (users; needs only `python3`).

---

## 8. Data and contracts

### 8.1 Layout of `~/.fileos/`

| Path | Mode | Content |
|---|---|---|
| `config.json` | 0644 | `base_url`, `aliases` (`embed`, `summary`), `budgets`, `vault_root`, extra denylist globs |
| `params.json` | 0644 | tunables with `version`; changes logged in `params-history.jsonl` (meta-workflow rule) |
| `credentials.json` | 0600 | `{ "base_url": "...", "key": "fos_..." }` from `fileos login`. Env `FILEOS_LLM_URL` and `FILEOS_LLM_KEY` win. |
| `cache.sqlite` | 0600 | section 8.2 |
| `calls.jsonl` | 0600 | one line per model call (section 8.3) |
| `rules.jsonl` | 0644 | owner decisions (section 8.4) |
| `runs/<slug>-<hash8>/<run_id>/` | 0700 | scan outputs (v1 files + new ones); `latest` is a symlink |
| `journal/<roothash8>.jsonl` | 0600 | apply and undo entries |
| `quarantine/<date>/<roothash8>/<rel_path>` | 0700 | "deleted" files, restorable |
| `wiki/<slug>/` | 0755 | the Obsidian vault (section 11) |

`<slug>` = root folder name, lowercased, with spaces as `-`. `<hash8>` = the first 8 hex chars of sha256 of the absolute root path.

### 8.2 Cache tables (`cache.sqlite`)

```sql
CREATE TABLE chunks (
  key TEXT PRIMARY KEY,          -- sha256(chunk_text) : chunker_ver
  file_sha TEXT, idx INTEGER, chars INTEGER, secret_dropped INTEGER DEFAULT 0);
CREATE TABLE vectors (
  key TEXT, model TEXT, dim INTEGER, vec BLOB,   -- float32 little-endian
  PRIMARY KEY (key, model));
CREATE TABLE summaries (
  key TEXT, level TEXT CHECK(level IN ('chunk','file','folder','group')),
  model TEXT, prompt_ver TEXT, text TEXT, ms INTEGER, created TEXT,
  PRIMARY KEY (key, level, model, prompt_ver));
CREATE TABLE file_map (                       -- which files map to which content
  file_sha TEXT, chunk_keys TEXT,              -- JSON list, in order
  extractor TEXT, chunker_ver TEXT, PRIMARY KEY (file_sha, chunker_ver));
```
- File key = content sha256. So the same content anywhere is processed once. A moved file is never re-read.
- Folder summary key = sha256 of the sorted list of its children's summary keys. A deep change only redoes its own path up to the root.

### 8.3 `calls.jsonl` (no content, ever)

`{"ts","endpoint":"embeddings|chat","alias","model","n_inputs","in_chars","out_chars","ms","status","run_id"}`

It is used for budgets, speed numbers and the fine-tune dataset index. The texts themselves live in the cache.

### 8.4 `rules.jsonl` (owner decisions)

`{"id":"R-0001","ts","kind":"keep|belongs_to|not_related|reject_action|accept_action","path","target","note","source":"cli|dashboard|skill"}`
- `plan` reads the rules first. A `keep` rule blocks any move of that path. `belongs_to` sets the fit to certain.
- `fileos rule add|list|remove` manages them.
- The `fileos-apply` skill mirrors each new rule to claude-mem (`save_memory`, one line).

### 8.5 New run outputs (beside the v1 files)

| File | Rows |
|---|---|
| `dependencies.jsonl` | `{from, to, kind, line, evidence, confidence, resolved:true/false}` |
| `deps-coverage.json` | per file type: parsed, failed, unsupported; dynamic-path files and their scope |
| `semantic-links.csv` | `file_a, file_b, cosine, shared_neighbours, reason` |
| `folder-fit.csv` | `path, kind(file/folder), own, own_fit, best_alt, best_alt_fit, margin, verdict` |
| `clusters.csv` | `cluster_id, path, keywords, suggested_folder` |
| `proposed-actions.json` | v1 fields **plus** `dependency_status, dependents[], dependencies[], suggestion, choices[], semantic` |

---

## 9. Dependency guard (Layer 0)

### 9.1 Edge finders (inside root)

| Kind | Files | Rule |
|---|---|---|
| `python_import` | `.py` | `ast` `Import`/`ImportFrom`; resolve the module against the file's folder, root, and `src/` |
| `js_import` | `.js .mjs .cjs .ts .tsx .jsx` | regex `import ... from '...'`, `require('...')`, `import('...')`; try `.js .ts .tsx .json /index.*` |
| `path_string` | every text file | quoted strings with `/` or a known extension; resolve from the file's folder, then root, then `~` |
| `markdown_link` | `.md` | `[..](x)`, `![..](x)`, `[[x]]`; drop URLs |
| `html_css` | `.html .htm .css .scss` | `src=`, `href=`, `url(...)` |
| `notebook` | `.ipynb` | read JSON cells, then `path_string` |
| `manifest` | `package.json`, `pyproject.toml`, `requirements*.txt`, `Dockerfile`, `docker-compose*.yml`, `Makefile`, `tsconfig.json` | small parser each (P2: `package.json`, `requirements`; the rest in D5) |
| `office_link` | `.docx .xlsx .pptx` | `_rels/*.rels` with `TargetMode="External"` |
| `symlink_in` | symlinks under root | `os.readlink`, resolved |

- **Confidence:** exact resolved path = 1.0. A unique basename match only = 0.4 ("weak", shown as "maybe").
- **Dynamic paths:** a file with f-strings, `os.path.join`, `Path(...) /` or `glob` on non-literals is flagged `dynamic_paths_present`. Its scope is its own folder and all subfolders.

### 9.2 Status per target file

| Status | Rule |
|---|---|
| `refs_found` | at least one edge with confidence ≥ 0.4 points to it |
| `none_found_full` | no edges; every text file in root parsed without error; no dynamic-path scope covers it |
| `partial` | no edges, but a parse failed, a text-like type is unsupported, or a dynamic scope covers it |
| `not_checked` | `--deps` did not run |

- The hardcoded `"checked_no_deps"` in `engine.plan` is removed (D0).
- "Outside this folder" is always listed as not checked, unless `--check-outside` ran (D5: launchd plists, crontab, shell rc files, home symlinks).

### 9.3 Behaviour

- `deps <file>` prints the in-links (dependents) and the out-links (dependencies), the status, and one suggestion.
- **`apply` gate:**
  - Re-run the finders for the target right before acting.
  - `refs_found` → exit 3, print the card, no change.
  - Delete never removes. It moves to `quarantine/` and journals the move.
  - After a move, re-resolve every edge that touched the file. A broken one → auto-undo, exit 3.
- **Suggestion table:**

| Situation | Recommended | Other choices |
|---|---|---|
| used by others | keep it here | move + update links (D4); move + leave a symlink |
| in a git repo / project root | keep it; use `git mv` inside the repo | — |
| delete, but used | do not delete | quarantine |
| moving file has out-links | move with what it needs | keep |
| none found, full | do the action | keep |
| partial | keep, or move then run your test command | move anyway (warning shown) |

- **GitNexus adapter (optional, personal):** in a git repo with `gitnexus` on PATH and an index present, `deps` adds `gitnexus impact <file>` callers as `kind: code_symbol` edges. It is off in shipped builds.

---

## 10. Understanding (Layers 1 and 2)

### 10.1 Extraction (`extract.py`)

| Types | Method | Capability tag |
|---|---|---|
| text and code (`.txt .md .csv .json .py .js .ts .html .sh .yaml .yml .xml .toml .ini .sql .css .ipynb` ...) | read utf-8, replace errors | `plain_text` |
| `.docx` | zip + XML (moved from the engine) | `docx_xml` |
| `.pptx .xlsx` | zip + XML text nodes | `ooxml` |
| `.pdf` | `pdftotext -layout` if on PATH | `pdftotext` |
| `.doc .rtf .rtfd .webarchive .odt` | `textutil -convert txt -stdout` (macOS) | `textutil` |
| anything else | no text; name-only vector (path + name) | `name_only` |

Text is capped at 200,000 chars per file. Over the cap → `truncated: true` in the inventory.

### 10.2 Chunking (`chunk.py`, `chunker_ver = "c1"`)

- Split on blank lines. Pack paragraphs up to 1,000 chars. Split long paragraphs at a sentence end, else hard-cut at 1,000.
- No overlap. Deterministic: same text in, same chunks out.
- 1,000 chars fits MiniLM's 256-token cap and small-model context.

### 10.3 Embeddings and relations (`semantic.py`)

- **Sampling for embeddings:** up to 8 chunks per file (first, last, evenly spaced). Summaries still read all chunks.
- **Batching:** 32 inputs per `/v1/embeddings` call. Vectors are stored normalized.
- **Vectors:** file = mean of its chunk vectors. Folder = mean of all file vectors under it (recursive). Vectors are compared only within the same model.
- **File → folder fit:**
  - `own_fit` = cosine(file, centroid of its folder without the file).
  - Candidates: sibling folders, the parent's siblings, and top-level folders of root (cap 50).
  - `margin = best_alt_fit − own_fit`.
  - Verdict:
    - `misfiled` if margin ≥ `params.fit_margin` (start 0.08) **and** own_fit < `params.fit_floor` (start 0.35) **and** the best folder has ≥ 3 files;
    - `fits` if own_fit ≥ `params.fit_floor`;
    - else `unknown`.
  - The start values are guesses until the owner labels 30 cases (experiments.md).
- **Folder → parent fit:** the same, one level up. It feeds the v1 hierarchy anomaly rows as a new evidence signal.
- **Related files:**
  - Random-hyperplane LSH, 16 bits, 4 tables (stdlib `random` with a fixed seed). Compare only inside buckets.
  - Keep the top 5 with cosine ≥ `params.related_min` (start 0.6).
  - Edge weight = 0.5·cosine + 0.2·dependency + 0.2·same-family + 0.1·Adamic-Adar.
  - `ponytail:` pure Python is O(n·bucket); fine to about 20k files; numpy is used when importable.
- **Clusters:** label propagation on the weighted graph (20 rounds, fixed seed).
  - Clusters of size ≥ 3 that span ≥ 2 folders are written.
  - Suggested folder name = top 3 TF-IDF words of member names and summaries (deterministic).

### 10.4 Summaries (`summarize.py`, `prompt_ver = "p1"`)

All calls use `temperature 0`.

| Level | Input | Output cap | Prompt (short form) |
|---|---|---|---|
| chunk | one chunk | `max_tokens 80` | "Summarize in 1–2 short sentences what this text is about. No preamble." |
| group | up to 8 summaries (≤ 1,500 chars) | 100 | "Combine these notes into 2 sentences. Keep names and numbers." |
| file | its chunk summaries (via groups if over 1,500 chars) | 100 | "This is file `<name>`. In 2 sentences, what is it and what is it for?" |
| folder | children's summaries + names (via groups) | 120 | "This is folder `<name>`. In 2 sentences, what does it hold and what is it for?" |

- **Order:** named targets first, then shallow before deep for discovery. Folders are built bottom-up once all their children are done.
- **Budget:** `--max-calls N` and `--max-minutes M`. On stop: exit 4, print "x of y done; run again to continue". The cache is the queue, so no queue file is needed.
- **Fine-tune dataset:** cached inputs and outputs, plus the owner's edits from the wiki (`summary_override` in frontmatter, read back on the next run) form the training set later.

---

## 11. Wiki output (Obsidian vault)

`fileos wiki <path> [--vault DIR] [--all-notes]` builds the vault **from the cache and run files only. It makes zero model calls.**

```
<vault>/
├── schema.md   how pages are made (Karpathy "schema"); the owner may edit; FileOS never overwrites it after creation
├── index.md    folder tree with one-line summaries and [[links]]
├── log.md      append-only, "## [2026-11-11] scan | <root> | 1,240 files"
├── lint.md     copies, version families, misfiled, folder misfits, refs into missing files, orphans, unknowns
├── folders/<slug>.md   files/<slug>.md   clusters/<id>.md
```

**Note slug:** the relative path with `/` → `__`, unsafe characters → `_`. The Obsidian `aliases` field holds the plain file name.

**File note frontmatter:**
```yaml
fileos: 1
path: "Projects/report.py"
abs: "/Users/.../Projects/report.py"
sha256: "…"
size: 1834
type: "py"
capability: "plain_text"
summary_model: "fileos-summary@gemma3:270m"
fit: { own: 0.41, best_alt: "Scripts", margin: 0.02, verdict: "fits" }
dependency_status: "refs_found"
summary_override: ""        # owner may write here; FileOS keeps it and uses it
```

**File note body sections:**
- `## Summary`
- `## Used by` (dependents)
- `## Uses` (dependencies)
- `## Related` (cosine, with the reason)
- `## Same file` (exact copies)
- `## Versions`
- `[Open original](file://...)`

**Folder note:** a summary, the children as links, "Fits in parent?" with its numbers, and the suggestion.

**Rules:**
- A file gets its own note only when it is text or is linked; binaries are listed in their folder note. `--all-notes` lifts this.
- A note is written only when its rendered content changed.
- The vault is never inside the scanned root, and is not SecondBrain.

---

## 12. Gateway (Oracle box)

### 12.1 API (OpenAI-compatible subset)

| Method, path | Auth | Purpose |
|---|---|---|
| `GET /health` | none | `{"ok":true}` |
| `GET /v1/models` | key | the aliases this key may use |
| `POST /v1/embeddings` | key | `{"model":"fileos-embed","input":[...≤32]}` |
| `POST /v1/chat/completions` | key | `{"model":"fileos-summary","messages":[...],"max_tokens":≤200}`; `stream` is not supported in v2 |

Anything else → 404. Ollama's own paths are never reachable.

### 12.2 Errors (OpenAI shape `{"error":{"type","message"}}`)

| Code | When |
|---|---|
| 400 | bad JSON or fields |
| 401 | missing, unknown or revoked key |
| 403 | alias not allowed for this key |
| 413 | body over 64 KB, or over 32 inputs |
| 429 | per-key rpm or daily cap hit, or queue wait over 60 s; always with `Retry-After` |
| 502 / 504 | backend down / backend over 90 s (under Cloudflare's 100 s cut) |

### 12.3 Keys, limits, logging

- **Key format:** `fos_` + 32 url-safe random chars. It is stored only as sha256 in `keys.json` (0600) as `{name, hash, created, rpm, daily, aliases, revoked}`. Compared with `hmac.compare_digest`.
- **Key tool:**
  - `python3 server/keys.py add <name> [--rpm 30 --daily 5000]` prints the key once;
  - `revoke <name>`, `list`.
- **Concurrency:** one chat generation and one embed batch at a time (4-CPU box). The others wait in FIFO order.
- **Aliases:** in `aliases.json`, for example `{"fileos-embed":"<winner>","fileos-summary":"<winner>"}`. Changing one needs a restart and no client change.
- **Log:** `gateway.jsonl` holds `{ts, key_name, path, alias, n, in_chars, out_chars, ms, status}`. Never text.
- **Runtime:** stdlib `http.server` with `ThreadingHTTPServer` and systemd `fileos-llm.service`.
  - Only if the radar check (LiteLLM proxy, `ollama-proxy-server`) finds a lighter fit do we use that instead.

### 12.4 Deploy (owner says yes first) and rollback

1. Back up `/etc/cloudflared/config.yml`.
2. Add `- hostname: llm.linkright.in / service: http://localhost:8790` above the 404 rule.
3. `cloudflared tunnel route dns oracle-linkright llm.linkright.in`.
4. Restart cloudflared.
5. Check that `n8n.linkright.in` and `oracle.linkright.in` return as before.

Rollback: restore the backup, restart cloudflared, `systemctl disable --now fileos-llm`.

The owner's key goes to `~/Desktop/Secrets/oracle_llm_api.env` (0600).

### 12.5 Model choice (evaluated, never assumed)

- **Embeddings:** a bake-off on 200 chunks of the owner's files.
  - Candidates: `nomic-embed-text`, MiniLM `:8766`, `fastembed` (own venv) with `bge-small-en-v1.5` and `snowflake-arctic-embed-xs`, Ollama `all-minilm` and `embeddinggemma`.
  - Measure chunks per second and p95 on the box, plus 20 related/unrelated pairs the owner labels.
  - Pick the fastest with ≥ 85% of pairs ordered right.
- **Summaries:** `gemma3:270m` → `qwen3.5:0.8b` → `gemma3:1b`, on 20 golden chunks.
  - Rubric per item, 0 or 1 each: right topic; no invented fact; ≤ 40 words.
  - Pick the smallest with ≥ 70% total. Measure p95.
- Before measuring, speed guesses are one third of the published number.
- Everything is recorded in `docs/research/experiments.md`.

---

## 13. Command reference

Global flags: `--json` (machine output for the future app), `--quiet`. Exit codes:
- 0 = ok;
- 1 = error;
- 2 = bad usage;
- 3 = blocked by a safety check;
- 4 = stopped by budget (resume later).

| Command | Does | Writes |
|---|---|---|
| `fileos tidy <path> [--budget-calls N]` | scan --deps → understand --embed-only → plan → wiki → prints the top 10 suggestions in plain words | run dir, cache, vault |
| `fileos scan <path> [--deps] [--incremental] [--max-depth N] [--exclude ...]` | v1 scan + deps edges | run dir |
| `fileos deps <file> [--root R] [--check-outside]` | in-links, out-links, status, suggestion | nothing |
| `fileos understand <path> --embed-only \| --summarize [--max-calls N] [--max-minutes M]` | L1 / L2 | cache, calls.jsonl |
| `fileos wiki <path> [--vault DIR] [--all-notes]` | vault from the cache | vault |
| `fileos plan [run]` · `report [run]` · `audit [run]` | v1 + new fields | run dir |
| `fileos apply --approve ACT-.. [--dry-run]` · `undo JRN-..` | gated changes | journal, quarantine |
| `fileos rule add\|list\|remove` | owner decisions | rules.jsonl |
| `fileos login --url U --key K` · `fileos doctor` | credentials; health check | credentials.json |
| `fileos dashboard [run]` · `watch <path>` | v1 | — |

`tidy` output (example):
```
FileOS looked at 1,240 files in 96 folders.   Model calls: 38 (embeddings only).

1. 14 exact copies use 230 MB.                       → fileos plan, ACT-001..ACT-014
2. "Old invoices" fits better in "Finance" (0.71 vs 0.22).  Nobody uses it.  → ACT-015
3. data/prices.csv looks misplaced, but report.py uses it. Keep it here.
...
Open the map in Obsidian: ~/.fileos/wiki/downloads/index.md
```

---

## 14. Claude plugin `fileos`

| Skill | Runs | Rule in the skill |
|---|---|---|
| `fileos-tidy` | `fileos tidy <path> --json` | default entry; read-only |
| `fileos-deps` | `fileos deps <file>` | use before any move or delete Claude itself would do |
| `fileos-understand` | `fileos understand ...` | state the call budget before running |
| `fileos-apply` | `fileos apply` / `undo` / `rule` | only explicit IDs; mirror each decision to claude-mem |

- Every skill: **never Read the user's file contents; the CLI and the Oracle models read them.**
- To answer a question, read `index.md` → one folder note → one file note (3 steps).
- Install: `claude plugin marketplace add FileOS/fileos/plugin`, then `claude plugin install fileos@fileos`.

---

## 14b. FileOS app UI (our own, Obsidian-style layout)

The owner wants our own UI, laid out like Obsidian, with only the features we need. It replaces "open the vault in Obsidian" as the main way to look. The vault stays as plain-markdown export (rule 13).
- **Our own brand.** No Obsidian name, logo or colours. We copy the layout pattern (tree, note, graph, side panels), which is common to many apps.
- **Shape:** `fileos ui [path]` serves one local web app on `127.0.0.1` (it grows from today's `dashboard.py`; stdlib server, no CDN, works offline; the screens use `@astryxdesign/core` per ShipQuick rule 38, see 18b). The future desktop app wraps the same page in a webview, so it is built once.
- The graph view: a library component if one fits; otherwise a ShipQuick `component-request` (rule 38). A candidate to check is vendored `d3-force` (ISC licence).

**Screens and features (only these):**

| Area | What it does |
|---|---|
| Left: file tree | The scanned root with badges: copy, version, misfiled, used-by count, unknown, secret-skipped. Filter by badge. Search. |
| Centre: note | The selected file or folder: summary, Used by, Uses, Related, Same file, Versions, fit numbers, "Open original". Action buttons: Keep here, Move to…, Quarantine. Each makes a rule or an approved action. |
| Right: panel | Local graph (neighbours of the selected item) and backlinks. |
| Graph view | The whole tree. Colour by cluster. Misfits highlighted. Click to open the note. |
| Review inbox | The suggestion cards (section 9.3 and 13) in plain words. Recommended choice first. Approve shows a dry-run preview, then applies. An undo toast follows. |
| Status bar | Model calls used versus the budget, the background summary progress, gateway online or offline, cache size. |
| Command palette (Cmd+K) | Scan folder, Tidy, Understand, Open note, Settings. |
| Settings | Gateway URL and key (`login`), budgets, denylist, vault export. |

**Not included:** a markdown editor, plugins, canvas, themes, sync, publish, multiple vaults.

**Full journey** (design covers each step; happy path left to right, sister branches under it, per the design rules):

| Step | Happy path | Sister branches (EDGE / SAD / ERROR) |
|---|---|---|
| 1 First open | empty state: "Pick a folder" | ERROR gateway not set → works offline (name-only) with a banner |
| 2 Connect | paste the gateway key, test → green | SAD bad key → 401 message; ERROR box down → retry later, still usable |
| 3 Scan | progress: files counted (L0), then embeddings with a call counter (L1) | EDGE secrets skipped notice; EDGE huge folder → "this will take ~N min" |
| 4 Home | health: copies, misfiled, unknown, files in use + top 5 suggestions | EDGE nothing to fix → "all tidy" |
| 5 Explore | tree + note + local graph | EDGE binary file → folder-level note only; EDGE partial deps check warning |
| 6 Graph | clusters, misfits glow, click opens the note | EDGE 10k files → clustered view first |
| 7 Review a suggestion | card → choose → dry-run preview → apply → undo toast | SAD blocked: "report.py uses this file, keep it here"; ERROR file changed since scan → re-scan prompt |
| 8 Summaries in background | budget set, progress in the status bar, resume next day | EDGE budget reached → "x of y done, continue?" |

**Design process (owner's rules, before any UI code):**
1. Use the Claude design artifact type (quickstart, intent `design`), with a stage-column canvas.
2. **Round 1:**
   - one journey map board with all 8 steps and their branches as labelled boxes (low-fi);
   - plus **2 or 3 hi-fi frames** of the direction: Home, Explore (tree + note + graph), Review card.
   - Then ask the owner what he likes.
3. Next rounds: at most 2 or 3 screens at a time, in journey order, each with a one-line "which design rule this shows".
4. Contrast ≥ 4.5:1. Nothing outside its board. Learnings board kept.
5. Only after the owner approves a screen does it move to "Approved not built". The UI is built from approved boards only.

## 15. Security and privacy

- **Never sent (path denylist):** anything under `~/Desktop/Secrets`, `~/.ssh`, `~/.gnupg`, `~/.aws`, `~/.config/gh`. Also `.env*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `id_rsa*`, `id_ed25519*`, `*keystore*`, `credentials*`, `*.kdbx`, and the `.fileosignore` globs.
- **Scrubber:** a chunk is dropped (never sent, `secret_dropped=1`) when it matches any of these:
  - private key blocks;
  - `AKIA[0-9A-Z]{16}`, `sk-[A-Za-z0-9_-]{20,}`, `ghp_`/`gho_`/`github_pat_`, `xox[abp]-`, `AIza[0-9A-Za-z_-]{35}`;
  - JWT `eyJ...\.eyJ...\.`;
  - `(password|passwd|secret|token|api_key)\s*[:=]\s*\S{8,}`.
- **What leaves the laptop:** scrubbed chunk text, plus file and folder names in the summary prompts (`--no-names` drops the names). Nothing else.
- **Transit:** HTTPS to Cloudflare. Cloudflare ends TLS, so Cloudflare and the box owner can see the chunks. The README says this in plain words for future users.
- **The gateway** stores no text. Keys are hashed. There is no shell or file access through it.
- **Dashboard** stays bound to 127.0.0.1 (v1 rule).
- **Box note:** Postgres listens on `0.0.0.0:5432`. Out of scope here. Flagged to the owner once.

---

## 16. Performance budgets

| Step | Budget |
|---|---|
| scan --deps, 10k files | ≤ 2× plain scan time |
| tidy, 1k files, warm cache | ≤ 60 s, 0 model calls |
| embed throughput | measured in the bake-off; the target is a 1k-file folder embedded in ≤ 15 min |
| summaries | slow by design: they run in the background with a budget; speed is measured, not promised |
| wiki rebuild, 10k files, no change | ≤ 30 s, 0 notes rewritten |

---

## 17. Tests (stdlib `unittest`, no network)

- All 79 old tests pass after the move.
- `test_deps.py`: the self-prompt fixtures 1 to 8 and 10. Also: there is no `checked_no_deps` anywhere in the plan output.
- `test_guard.py`: a Secrets path is skipped; an `sk-...` chunk is never sent (the fake server sees zero requests).
- `test_llm.py`: a fake OpenAI server in a thread: retry on 502, wait on 429 `Retry-After`, ledger line written.
- `test_cache.py`: a second run makes 0 calls; a moved file makes 0 calls; one changed file redoes only its path to the root.
- `test_semantic.py`: hand-made vectors give the expected `misfiled` / `fits` / `unknown` and clusters.
- `test_summarize.py`: budget stop → exit 4; resume finishes; folder key changes only up the changed path.
- `test_wiki.py`: the notes, the frontmatter, `[[links]]` both ways, `summary_override` kept, a second run writes 0 notes.
- `test_gateway.py` (server, fake backend): 401, 403, 404, 413, 429 with `Retry-After`, revoked key, no text in the log.
- `test_tidy.py`: end to end on a fixture tree with the fake server.
- Live smoke (manual, env `FILEOS_LIVE=1`): against the real gateway.

---

## 18. Acceptance (done means)

1. `pipx install FileOS/fileos`, then `fileos doctor` is all green. `fileos.pyz` runs.
2. `fileos tidy FileOS/` writes nothing inside `FileOS/`. It prints plain-words suggestions, and the vault opens in Obsidian with a working graph.
3. No action anywhere claims a check that did not run.
4. A move of a used file is blocked at `apply` with the card.
5. Gateway: no key → 401; a valid key → 200; `/api/pull` → 404; a revoked key → 401; a burst → 429 with `Retry-After`; the n8n and oracle hosts are unchanged.
6. The second `understand` run makes 0 calls. A secret is never sent (proved by a test).
7. `experiments.md` holds both bake-offs with model, p95 and score.
8. The 4 skills install. A skill run makes Claude read no user file content.

---

## 18b. Project setup with ShipQuick (owner, 11 Nov 2026)

- **Repo root = `FileOS/`.** Run `git init`. The package stays at `FileOS/fileos/`. The zip and the chat history are git-ignored.
- **Submodule:** `git submodule add -b dev https://github.com/satvik-jain-iitd/shipquick_latest.git knowledge/shipquick_latest`. This is the same path, URL and branch as GoServe and Miraya. The submodule is never edited in place; it is bumped after upstream merges.
- **Adopt:**
  - `knowledge/shipquick_latest/scripts/adopt.sh .` writes the pinned CI caller and pre-commit hooks;
  - the project `CLAUDE.md` comes from `docs/CLAUDE.project.template.md` (stack, folders, ADR pointers);
  - `docs/` gets the ShipQuick set: `process-trace.md`, `discussions/2026-11-11.md`, `ideas.md`, `assumptions.md`, `follow-ups.md`, `LEARNINGS.md`, `decisions/ADR-001` (this architecture), `data/model-calls.md` (every model call site: rule 32 matches section 10.4), `tests/test-cases.md`, `TEAM_ROSTER.md`.
- **What ShipQuick changes in this spec:**
  - **Rule 4, work from issues:** every phase below becomes an epic, with stories as GitHub issues. Branches are `feat/<issue>-<slug>` from `dev`. PRs come from the build account `klickbae8yt-star`; the review account `satvik-jain-iitd` reviews.
  - **Rule 21, live roadmap:** set up with the first epic.
  - **Rule 31, design process:** the UI design goes through the canvas manifest (`canvas_stage.py`) and stage columns. No UI code before a board is approved.
  - **Rule 38, library first:** web screens use `@astryxdesign/core` (exact version pinned) instead of the hand-written vanilla UI in 14b. They are built once to static files and shipped inside the package, so `fileos ui` still works offline from the stdlib server. The graph view, if no library component fits, goes through a `component-request`, never a hand-drawn stand-in.
  - **Rule 32, model load:** micro-task calls, smallest model first, and the `model-calls.md` list are already in this spec. They are checked with `scripts/model_calls.sh --check`.
  - **Rule 28, runtime:** the CLI must run on the laptop, because it reads local files. That is the stated exception. Everything model-side runs on the Oracle box.
- **Needs the owner (asked after this plan):**
  - the ShipQuick mode (`! bash knowledge/shipquick_latest/scripts/mode.sh set <manual|semi|auto>`, typed by him);
  - the GitHub repo owner and name (creating it is outward-facing).

## 19. Build order (one phase at a time; red test first; all green before the next)

| Phase | Work |
|---|---|
| P-1 | Project setup (18b): `git init`, ShipQuick submodule, `adopt.sh`, project `CLAUDE.md`, docs set, GitHub repo + epics/issues (after the owner's yes), live roadmap. |
| P0 | Radar the gateway need (LiteLLM proxy, `ollama-proxy-server`). |
| P1 | Package move, `cli.py`, relative imports, `paths.py`/`config.py`, state in `~/.fileos`, `login`, `doctor`, `--json`, zipapp. Plugin manifest named `fileos`. |
| P2 | `deps.py` D0 to D3, `rules.py`. |
| P3 | `server/` gateway + keys + tests; deploy after the owner's yes; the owner's key into Secrets. |
| P4 | `extract`, `guard`, `chunk`, `llm`, `cache`, `semantic`; embeddings bake-off. |
| P5 | `summarize`; summary-model eval. |
| P6 | `wiki`, `tidy`, plan uses fit + deps + rules; optional GitNexus adapter. |
| P7 | 4 skills, plugin install, claude-mem mirroring. |
| UI-D | **Runs right after P0, in parallel with P1 to P3:** design round 1 (journey map + 2 or 3 hi-fi frames) → owner feedback → the rest in rounds of 2 or 3. |
| UI-B | `fileos ui` built from approved boards only, after P6 (it needs the data). Tests: the page loads offline, binds to 127.0.0.1, and approve goes through the same `apply` gate. |
| Later | D4 to D6 (update-links action, outside-root checks, git), the full Karpathy entity pages after an eval, the desktop app, and testing claude-mem on the gateway. |

## 20. Open questions for the owner

1. Vault place: is `~/.fileos/wiki/<root>/` fine, or should it go inside SecondBrain as its own folder?
2. Hostname: is `llm.linkright.in` fine?
3. First real folder to run on after the tests: `~/Downloads`, or `~/Documents/LinkRight`?
4. ShipQuick mode for FileOS: manual, semi or auto?
5. GitHub repo: `klickbae8yt-star/fileos` or `satvik-jain-iitd/fileos`? Private?
