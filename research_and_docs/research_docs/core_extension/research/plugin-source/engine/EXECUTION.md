# Execution Protocol

This is the runtime. It turns the config spec into action. Given any workflow, follow these steps exactly. This file is generic, it works for any user, all specifics come from config and the instance files.

## How to run one workflow

1. Resolve config. Load `config/user-config.yaml`. Hold its writing_protocol, positioning, expertise, audience, and language as law for this run.

2. Open the workflow. Read `workflows/<code>/workflow.yaml`. Note the agents list, that is the run order. Note the inputs, the validation eval, and the primary_output.

3. Locate the run folder. Use `runs/YYYY-MM-DD/` for today. Create it if missing. Every templated output for this run lands here, numbered in order.

4. Run each agent in order. For each agent in the workflow's list:
   a. Load `agents/<workflow>/<code>.agent.yaml`.
   b. Load its dependencies.knowledge files, and its activation.persistent_facts, including any `file:` references.
   c. If it is a memory agent, load `memory/<code>/MEMORY.md` if it exists.
   d. Read its input templates, the files named under dependencies.templates.reads.
   e. Do its responsibilities, acting through its persona, honouring its dos and donts.
   f. Run its checklist, the file under dependencies.checklists. Hard gates are pass or fail. Scored evals must clear the threshold in `knowledge-base/scoring-rubrics.md`.
   g. On a fail, follow the workflow's refinement_loop if it has one, rewrite up to the max, else send the work back to the named upstream agent. Never pass dirty work forward.
   h. Write its output template into the run folder.

5. Gate the workflow. Run the workflow's validation eval, or hand the output to the matching Master Evaluator agent. Only a pass lets the run proceed.

6. Memory agents log. A memory agent appends a short note to `memory/<code>/sessions/YYYY-MM-DD.md`. These get distilled into MEMORY.md later by the System Optimizer, never bloat MEMORY.md directly.

7. On a blocked gate. If a stage fails past its max loops, stop. Write the reason into `runs/YYYY-MM-DD/run-log.md` for the owner.

## Context isolation, so big runs stay reliable

A workflow runs inside its own context, it loads only its own agents, knowledge, and evals, never another workflow's. When the daily-post conductor chains several workflows, it dispatches each one as a separate subagent and keeps only a short summary from each. This is deliberate. A single context that tries to hold every agent and every knowledge file at once gets crowded, attention thins, and evals get skipped. Isolation keeps each context small, which keeps quality high and forces every agent to do its own loading and checking. Within a heavy workflow, an agent that needs a lot of its own context may itself be run as a sub subagent, but workflow level isolation is the floor.

## Standing rules

Only the System Optimizer edits the knowledge base. Only Onboarding edits the config. Every agent reads the owner from config, none hardcode a name or a domain. Nothing ships without its gate passing. The voice profile and the scoring rubric are the floor, a post that does not sound like the owner does not go out.

## Running a single workflow by hand

Any workflow can be run alone. Setup and Voice Building are one offs. System Optimizer runs on a schedule. The rest run per post, usually chained by the daily-post conductor. To run one alone, start at step 1 with that workflow's code.
