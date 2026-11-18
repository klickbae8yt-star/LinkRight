---
name: optimize
description: Reviews recent post performance and improves the system, scoring weights, knowledge, and voice drift. Use when the user says "optimize", "review performance", "weekly review", "what's working", "tune the system", or runs a weekly or monthly improvement pass.
---

# Optimize

Read what performed and make the engine better. Follow `${CLAUDE_PLUGIN_ROOT}/engine/EXECUTION.md` and run the System Improvement workflow, `${CLAUDE_PLUGIN_ROOT}/engine/workflows/system-optimizer/workflow.yaml`.

## Run

1. Read the user's `knowledge-base/performance-data/posts.csv` and recent posts.
2. Find what over and under performed, weighted to saves, dwell, and inbound, not vanity likes. Flag small samples.
3. Fold evidence backed findings into the knowledge and scoring weights, logging every change so it can be rolled back.
4. Check recent posts against the voice profile for drift, and flag a voice refresh if needed.

## Output

An optimization report in the run folder, plus any logged knowledge edits. This is the only skill allowed to edit the engine knowledge, and only with evidence.

## Cadence

A light pass weekly, a deeper pass monthly. Can be run on demand or on a schedule.
