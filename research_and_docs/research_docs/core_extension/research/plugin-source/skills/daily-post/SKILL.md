---
name: daily-post
description: Produces one finished, on-voice, gated LinkedIn post with its media asset and a first-hour engagement plan. Use when the user says "write today's post", "daily post", "make a LinkedIn post", "run the content engine", or gives topics to post about. Run setup first if the user has no config or voice profile yet.
---

# Daily Post

The one button daily run. Take candidate topics and produce one finished, gated, ready to publish post, its asset, and an engagement plan. Follow the conductor at `${CLAUDE_PLUGIN_ROOT}/engine/daily-post-conductor.md`, and `${CLAUDE_PLUGIN_ROOT}/engine/EXECUTION.md` for how each workflow runs.

## Before running

The user's working folder must have `config/user-config.yaml` and `knowledge-base/voice-profile.md`. If either is missing, run the setup skill first.

## Inputs

Candidate topics for the day. The user can paste them, or run the topic-hunt skill to generate them. If none are given, ask for topics or run topic-hunt.

## The run

Follow the conductor in order, strategy, then drafting, then media, with the Master Evaluator gate between each, then engagement. Write each stage's output into a dated run folder, and assemble the final post, asset, and engagement plan. Nothing ships without all three signoffs, and no post goes out without its asset.

## Output

A ready to publish post, its finished asset, and a first hour engagement plan, in the day's run folder. The user publishes or schedules, and works the first hour from the plan.
