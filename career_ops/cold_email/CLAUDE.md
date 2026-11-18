# Cold Email Engine

A generic, configurable cold-email tool. The purpose is a config profile, not code.
Profile 1 is job search (Satvik). Miraya is a later profile.

## Where things are
- `_source/`: the two original zips from Downloads. Never edit.
- `research/`: extracted research and the two self-prompts. The two prompt files exist twice (identical); use the copy in `cold-email-research-pack/02-prompts/`.
- The research is a preliminary pass. Mostly vendor sources. Every number is "to be verified". Verified facts go in `research/VERIFIED.md` with tier and confidence.
- Plan: step O1 to O6 in `~/.claude/plans/https-github-com-madslorentzen-ai-job-se-generic-harbor.md`.

## Rules
- Nothing is sent without `dry_run=false` and the owner's yes. First sends go to his own seed addresses.
- No automated warm-up networks on Google accounts. Manual ramp only (until O3 says otherwise).
- No LinkedIn scraping or logged-in tools. Business emails only.
- Third-party personal data stays on the Mac or Oracle. Never in free LLM tiers that train on inputs.
- n8n work: read `~/.claude/n8n-rulebook.md` first, and load skill `n8n-canvas-layout`.
- Budget: USD 20 a month in total. Target 100 a day only after warm-up; start at 30 to 40.
- Keys and passwords: `~/Desktop/Secrets/` only.

## Radar first (owner, 25 Oct 2026, strictest rule)

Before any new component, script, skill, workflow or tool in this project: run the `radar` skill (`radar@agi`) on the need, read the top 3 READMEs, record the run in `docs/research/repo-radar.md`, reuse or borrow first. Build from scratch only when the run found nothing, and say so. No radar run, no new code. Full text: `~/.claude/CLAUDE.md` section 2, rule 0.
