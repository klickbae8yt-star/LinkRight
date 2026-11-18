---
name: topic-hunt
description: Hunts the web for high-signal, recent stories in the user's field to fuel content ideas. Use when the user says "find topics", "topic hunt", "what should I post about", "find me trending stories", "content ideas", or runs a daily idea search. Reads its focus from config, so it works for any niche.
---

# Topic Hunt

Find a short set of high-signal, recent stories in the user's field that make strong content ideas. This skill is config driven, it carries no fixed niche of its own.

## Load the config

Read `config/user-config.yaml`, the `topic_hunt` block. If the block is empty, ask the user for the niche and what counts as a high-signal story, then offer to save it. The block holds:

- `niche`, the domain to hunt in
- `signal_of_interest`, what makes a story worth surfacing
- `dimensions`, the angles or metrics to extract from each story
- `sources`, where to look, blank means the open web
- `lookback_days`, how recent
- `story_count`, how many to return
- `ignore`, what to skip
- `output_fields`, the fields to deliver per story

## Run

1. Search the web for stories in `niche` from the last `lookback_days`, biased to the `signal_of_interest`. Prefer the named `sources` if given.
2. Keep only stories that show a real, specific signal, a number that moved, a launch, a shift, a decision. Drop anything on the `ignore` list.
3. For each kept story, extract the `dimensions`, the concrete detail, and the surprise, the non obvious part.
4. Select the `story_count` strongest, most distinct stories.

## Deliver

Write a brief with one entry per story, using the `output_fields` if set, otherwise: product or subject, the specific signal with its number, the surprise, the angle for content, and the source. No intro or outro prose, just the brief. Save it to a dated file the content workflow can read, and report the path.

## Notes

Every claim carries a source. Do not invent a number. If the field is thin this week, return fewer strong stories rather than padding with weak ones. This skill can be run on demand or on a daily schedule.
