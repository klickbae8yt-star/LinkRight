---
name: profile-search
description: Searches public professional profiles for people who match the user's target personas, verifies them, and appends new finds to a deduped list. Use when the user says "find people", "profile search", "find leads", "people to connect with", "find candidates", "who should I reach out to", or runs a daily prospect search. Reads its targets from config, so it works for any goal.
---

# Profile Search

Surface and verify public professional profiles that match the user's targets, and keep a clean, deduped running list. This skill is config driven, it carries no fixed target of its own.

## Load the config

Read `config/user-config.yaml`, the `profile_search` block. If it is empty, ask the user who they are trying to find and why, then offer to save it. The block holds:

- `purpose`, why search, for example people to connect with, hire, learn from, or sell to
- `target_personas`, each a named persona with a core search string and a few variations
- `verification_checks`, what must be true for a profile to count
- `output_fields`, the columns to deliver per profile
- `dedupe_file`, the csv that stores results and prevents duplicates

## Run

1. Check existing. Read the `dedupe_file` if it exists, pull the known profiles into context so none are added twice. If it does not exist, create it with the `output_fields` as the header.
2. Search. For each persona in `target_personas`, run the core search string, then its variations, to widen the pool. Scan the whole profile, not just the headline, the past experience, education, and honors all count.
3. Verify. Include a profile only if it passes every check in `verification_checks`. Drop false positives, and if a result fails, find another with a different search string.
4. Deduplicate. Discard anyone already in the `dedupe_file`.

## Deliver

Return the verified profiles in a clean table using the `output_fields`, no intro or outro prose. Then append the new rows to the `dedupe_file` with the date. Report how many new profiles were added and the file path.

## Notes

Use only public profile information. Every included profile must pass the verification checks, quality over volume. This skill can be run on demand or on a daily schedule.
