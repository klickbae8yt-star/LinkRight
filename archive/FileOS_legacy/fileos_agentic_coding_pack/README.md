# FileOS Agentic Coding Build Pack

This pack contains the product/skill specification and Antigravity prompts for incrementally evolving FileOS Organizer.

## Files

- `FILEOS_LOW_TOKEN_SKILL_SPEC.md` — original low-token FileOS skill and processing specification.
- `ANTIGRAVITY_SELF_PROMPT.md` — prompt to build the initial skill/plugin.
- `ANTIGRAVITY_RECURSIVE_DIRECTORY_ADDON_PROMPT.md` — add recursive directory and nested folder intelligence.
- `ANTIGRAVITY_LOCAL_REVIEW_DASHBOARD_PROMPT.md` — build the local human review dashboard.
- `FILEOS_M0_M1_IMPLEMENTATION_SPEC.md` — locked roadmap decisions plus detailed M0/M1 requirements, acceptance criteria and tests.
- `ANTIGRAVITY_M0_M1_EXECUTION_PROMPT.md` — shorter copy-paste task prompt directing Antigravity to execute only M0/M1 using the specification.

## Current recommended use

Open the existing FileOS skill workspace in Google Antigravity and provide `ANTIGRAVITY_M0_M1_EXECUTION_PROMPT.md` as the task prompt and `FILEOS_M0_M1_IMPLEMENTATION_SPEC.md` as its reference. Ask the agent to execute only M0 and M1. Do not ask it to implement later milestones in the same task.

## Safety

M0/M1 are baseline and integrity milestones. They must not run `apply` on real user files, make cloud/AI network calls, or alter the original workspace data. Test apply/undo only on synthetic temporary fixtures.
