---
name: setup
description: First time setup for the content engine. Captures the user's settings, then builds their writing voice from a short interview. Use when the user says "set me up", "onboard me", "get started", "build my voice", or runs the engine for the first time. Run this once before any content work.
---

# Setup

Stand up the engine for a new user. One sitting, two parts, settings then voice. Follow `${CLAUDE_PLUGIN_ROOT}/engine/EXECUTION.md` for how each workflow runs.

## Part 1, settings

Run the Onboarding workflow, `${CLAUDE_PLUGIN_ROOT}/engine/workflows/onboarding/workflow.yaml`. Interview the user only for what is missing, pre fill from anything they have already shared. Write their answers into `config/user-config.yaml` in the user's working folder, using `${CLAUDE_PLUGIN_ROOT}/engine/templates/user-config.template.yaml` as the shape. This config is the single source of truth every other skill reads.

## Part 2, voice

Once the config exists, run the Voice Building workflow, `${CLAUDE_PLUGIN_ROOT}/engine/workflows/voice-architect/workflow.yaml`. Interview the user on a comfortable topic, mine their words for the language fingerprint, and write `knowledge-base/voice-profile.md` and `knowledge-base/voice-examples.md` into the user's working folder. This is the most important file in the system, every post is scored against it.

## Done when

The working folder has a filled `config/user-config.yaml` and a `knowledge-base/voice-profile.md`. After that, the daily-post skill can run.

## Note

The engine ships generic. Everything specific to this user is created here, in their own folder. Settings can be re run alone later, the voice can be refreshed when it drifts.
