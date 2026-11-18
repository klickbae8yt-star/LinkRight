# CLAUDE.md - match-lab (read this first)

Goal: never send a wrong referral. Find a scorer better than cosine, build a deep recruiter + hiring-manager judge (Claude Code session only, NEVER the Claude API), fine-tune Laya on those judgements so it beats TypeSafe Jev, then serve it for the Amex referral flow. Plan: `docs/PLAN.md` (the one plan). To-do list: beads, epic `ml-nva`.

## Rules (override the generic block below)
- Start every session with `bd ready` and `bd show <id>`; claim with `bd update <id> --claim`; close a bead only with proof in the note. New work = new bead (`--deps discovered-from:<id>`). Pass marks in beads and in `docs/PLAN.md` are never edited without a decision bead and Satvik's yes.
- No Claude API. No subagents. TDD: red, green, re-run all. Every claim has a tier (A/B/C/S) and a 0 to 1 confidence.
- Personal data: scrub before any model, log or file is read (no name, email, phone, links). Real data only under `data/` (git-ignored), never in a commit, never in chat output.
- Ask first (beads labelled `needs-satvik`): real export, first Jev call (cap Rs 100), new Mongo collection, new workflow, new pm2 process, any change to a live workflow, any push.
- No git remote. Do not run `git push`. The generic "session completion: git push" text below does not apply here; instead commit only when Satvik asks.
- Secrets only in `~/Desktop/Secrets/`. Chat in Romanized Hindi, files in simple English. Effort in C1 to C5.
- The Amex repo (`~/Documents/referral_automation`) is read-only for this project except the durable result files named in the plan (experiments.md rows E4/E5, research notes).

## Layout
`src/` code, `tests/` tests (run all: `node --test tests/` or the command in README), `data/` git-ignored, `docs/` plan, rubric, state, `tasks/changelog.md`.

This file provides instructions and context for AI coding agents working on this project.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->


## Build & Test

_Add your build and test commands here_

```bash
# Example:
# npm install
# npm test
```

## Architecture Overview

_Add a brief overview of your project architecture_

## Conventions & Patterns

_Add your project-specific conventions here_

## Radar first (owner, 25 Oct 2026, strictest rule)

Before any new component, script, skill, workflow or tool in this project: run the `radar` skill (`radar@agi`) on the need, read the top 3 READMEs, record the run in `docs/research/repo-radar.md`, reuse or borrow first. Build from scratch only when the run found nothing, and say so. No radar run, no new code. Full text: `~/.claude/CLAUDE.md` section 2, rule 0.
