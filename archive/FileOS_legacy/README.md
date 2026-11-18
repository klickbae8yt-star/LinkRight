# FileOS Antigravity Skill Build Pack

This pack contains the requirements and build prompt for a deterministic-first, low-token file organization skill/plugin.

## Files

- `FILEOS_LOW_TOKEN_SKILL_SPEC.md` — product and engineering requirements, including staged character limits, hierarchy mismatch logic, safe file operations and acceptance tests.
- `ANTIGRAVITY_SELF_PROMPT.md` — copy-paste instruction for Google Antigravity CLI to build the actual skill/plugin from the spec.

## Recommended use

1. Put both Markdown files in the Antigravity workspace (or keep them together in a project folder).
2. Open the workspace in Antigravity CLI.
3. Paste the contents of `ANTIGRAVITY_SELF_PROMPT.md` as the task prompt and ensure the agent can read `FILEOS_LOW_TOKEN_SKILL_SPEC.md`.
4. Let it create the skill/plugin locally and run the tests.
5. Review the report and validation results before installing globally or scanning important folders.

The first version is intentionally read-only by default. The agent should not move, rename or delete user files without explicit approval of specific actions.

## Antigravity documentation

The prompt tells the coding agent to re-check the current official docs for plugin/skill layout and validation commands:

- https://antigravity.google/docs/skills
- https://antigravity.google/docs/plugins
