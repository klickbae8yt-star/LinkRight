# linkright-mcp

MCP server for the Linkright resume system. Converts the `sync-resume-optimizer`
plugin's three skills into MCP tools, resources and prompts, and exposes the
deterministic checkers that back their quality gates.

Transport: stdio. SDK: `mcp>=2.0`.

## What it exposes

Ten tools, all read-only, all prefixed `linkright_`.

### Instruction tools (progressive disclosure)

| Tool | Purpose |
|---|---|
| `linkright_list_skills` | Route a task to coach, sync, or review. Call this first. |
| `linkright_get_skill` | Full operating procedure for one skill, plus a reference index. |
| `linkright_get_stage` | One gate/phase/step only — resume mid-pipeline without loading the whole document. |
| `linkright_get_reference` | One reference document, loaded at the gate that calls for it. |

### Analysis tools (deterministic)

| Tool | Backed by | Runs at |
|---|---|---|
| `linkright_check_ai_smell` | `ai_smell_checker.py` | sync gate 4 and gate 7 |
| `linkright_scan_ats` | `ats_scanner.py` | sync gate 7 |
| `linkright_check_constraints` | `constraint_checker.py` | sync gate 5 |
| `linkright_parse_latex_log` | `log_parser.py` | sync gate 5.5 |
| `linkright_measure_width` | `measure_width.py` | HTML path only |
| `linkright_run_quality_gate` | all of the above, concurrently | sync gate 7 |

### Resources

- `linkright://skill/{skill}` — coach, sync, or review
- `linkright://reference/{skill}/{reference}`

### Prompts

- `linkright_capture_career(language)`
- `linkright_build_master(archetype)`
- `linkright_tailor_for_jd(company, role)`

## Ownership boundaries

The server enforces nothing at runtime — the boundaries live in the skill text —
but tool descriptions state them, so an agent reading the schema sees them:

```
coach  -> owns the FACTS      -> layers, user_setup, archetype ratings
sync   -> owns the ARTIFACT   -> append-only master resume + measured bullet bank
review -> owns the JD         -> tailored one-pager by selection only + two briefs
```

Review never writes a bullet. Sync never sees a full job description. Coach never
measures width.

## Install and run

```bash
pip install -e .
python -m linkright_mcp.server        # stdio
```

Register with a client using `mcp.example.json` as a template.

Inspect interactively:

```bash
npx @modelcontextprotocol/inspector python -m linkright_mcp.server
```

Run the end-to-end checks (launches the server over stdio and exercises every
tool, resource and prompt):

```bash
python tests/test_server.py
```

## Design notes

**Skipped is not passed.** `linkright_check_constraints` errors rather than
running with no constraint file, and `linkright_run_quality_gate` reports
absent inputs as `skipped`. A check that never ran must never read as clean.

**A parsed file with zero constraints is a warning.** If `user_setup.md` loads
but no section names are recognised, the result is downgraded to `warn` with the
expected shape printed. Expected format:

```yaml
do_not_mention:
  companies:
    - Acme Corp
  projects:
    - Project Halcyon
  technologies:
    - InternalTool
  personal_info:
    - home address
```

**Width has two paths and they are not interchangeable.** `linkright_measure_width`
is calibrated for Roboto 9.5pt on the HTML path. On the LaTeX path, compile the
real resume and read `linkright_parse_latex_log`. Running the mm estimator on
LaTeX source returns a confidently wrong number.

**Path inputs are never joined from caller strings.** Skill and reference lookups
resolve against a fixed bundle and reject anything outside it, including
traversal attempts.

## Known gaps carried over from the skills

These were absent from the source plugin and are surfaced, not hidden — 
`linkright_get_skill` prints a "Missing References" block naming them:

- `linkright-sync` instructs loading `ref_00_template.md` and `ref_07_human_clarity.md`; neither is bundled.
- `linkright-coach` instructs loading `elicitation.md`, `tracks.md`, `layers_spec.md` and `interview_prep.md`; none are bundled.

The skill documents state enough inline to proceed, but the referenced detail is
not available until those files are written.

## Fix applied to a bundled script

`log_parser.py` matched `Overfull\hbox` with no space. Real XeLaTeX logs write
`Overfull \hbox`, so the parser reported every log as clean — the failure mode
being a resume that ships with a wrapped bullet. The three affected patterns now
allow the space.
