# Daily Post Conductor

The one button daily run. It takes candidate topics and produces one finished, gated, ready to publish post, its asset, and an engagement plan. The conductor stays thin on purpose, it dispatches each stage as an isolated subagent and never loads a stage's internal agents or knowledge into its own context. This is what keeps the run from overwhelming a single context, and forces every agent to actually load its own knowledge and run its own eval. Follow `EXECUTION.md` for how a workflow runs inside a subagent.

## The isolation rule

The conductor holds only three things in its own context, the run folder path, the candidate topics, and a short summary back from each stage. It does not read the strategy knowledge, the drafting knowledge, the media knowledge, or the agent files. Each stage runs in a fresh subagent that loads only its slice, does the work, writes its template to the run folder, and returns a five line summary. The conductor reads the summary, not the internals.

## Before running

Config exists at `config/user-config.yaml`. The voice profile exists at `knowledge-base/voice-profile.md`. If either is missing, run Setup first.

## Inputs

Candidate topics for the day, from the topic hunt or from the owner. If none are given, ask the owner or pull the latest topic hunt brief.

## The run, each stage a separate subagent

For each stage, dispatch one subagent with a tight brief, wait for its summary, then move on. The brief template is at the bottom.

1. Strategy subagent. Brief, run the `content-strategist` workflow on the candidate topics, write `runs/DATE/01-strategy-brief.yaml`. Returns, the chosen topic, the output path, pass or fail, any flag.

2. Strategy gate subagent. Brief, run the `strategy-reviewer` against `evals/strategy-signoff.md` on the brief, write `runs/DATE/02-strategy-signoff.md`. Returns PASS or REWORK with the named gap. On REWORK, re dispatch stage 1 with the gap, then re gate.

3. Drafting subagent. Brief, run the `content-drafter` workflow on the passed brief, run its own hard gate and voice loops inside this subagent, write `runs/DATE/03-content-handoff.yaml`. Returns, the scores, the iteration count, pass or fail. This is the heaviest stage, it stays fully isolated so its five agents and their knowledge never touch the conductor context.

4. Copy gate subagent. Brief, run the `copy-reviewer` and `ethics-and-risk-reviewer` against `evals/copy-signoff.md` and `evals/risk.md`, write `runs/DATE/04-copy-signoff.md`. Returns PASS or REWORK with the failing lens. On REWORK, re dispatch stage 3 with the note, then re gate.

5. Media subagent. Brief, run the `media-creator` workflow on the passed copy, render in the sandbox first, the external image generator is the fallback, write `runs/DATE/05-media-handoff.yaml` plus the rendered files. Returns the asset paths and pass or fail.

6. Media gate subagent. Brief, run the `media-reviewer` and `ethics-and-risk-reviewer` against `evals/media-signoff.md` and `evals/risk.md`, write `runs/DATE/06-media-signoff.md`. Returns PASS or REWORK. On REWORK, re dispatch stage 5, then re gate.

7. Engagement subagent. Brief, run the `engagement-ops` workflow on the passed post and asset, write `runs/DATE/07-engagement-plan.md`. Returns the post time and the plan path.

8. Assemble. The conductor itself, no subagent needed, gathers the final post text, the media files, and the engagement plan into `runs/DATE/08-final-package/`, and copies the package into the matching `30-Day-Engine/Day-NN/` folder.

9. Log. Write `runs/DATE/run-log.md` with the scores, the iteration counts, and the three signoffs, all pulled from the stage summaries.

## Subagent brief template

Give each dispatched subagent exactly this shape, nothing more.

```
You are running the <workflow code> workflow from the content engine.
Load <engine path>/workflows/<code>/workflow.yaml and follow EXECUTION.md.
Load only this workflow's agents, knowledge, and evals. Do not load other workflows.
Read your input: <the input file path>.
Do the work, run each agent's eval, honour the hard gates and the rubric threshold.
Write your output to: runs/DATE/<output file>.
Return only a five line summary: output path, pass or fail, key scores, iterations, any flag. Do not return the full content.
```

## Stop conditions

If any gate returns REWORK past its max loops, stop at that stage and write the reason into the run log for the owner. Nothing ships without all three signoffs. No post goes out without its asset, no text only posts.

## Output

A ready to publish post, its finished asset, and a first hour engagement plan, in the day's run folder and the calendar folder. The owner publishes or schedules, and works the first hour from the plan.

## Why this shape

Each stage gets a clean context with only its own material, so nothing gets crowded out and every eval actually runs. The conductor never holds more than the topics and a handful of short summaries, so it cannot overflow no matter how many agents the engine has. This is the difference between a system that looks complete and one that stays reliable on every run.
