# Cold Email Research Pack

Everything from the "cold email" project so far: the research, the decisions, and both self-prompts.

Exported 24 Oct 2026. Research done 14 Oct 2026.

## What's inside

| File | What it is |
|---|---|
| `README.md` | This index, plus the decisions taken so far |
| `01-research/research-findings.md` | All research findings by stage (mailbox rules, warm-up, inboxes, sequencers, LinkedIn data, AI, benchmarks, law), with sources, dates, confidence and caveats, plus working conclusions |
| `01-research/search-log.md` | Every search query run, every page read in full, and the known gaps |
| `02-prompts/cold-email-pipeline-self-prompt.md` | The 2-part cold email self-prompt (Part 1: deep research, Part 2: Claude Code / n8n build) |
| `02-prompts/contact-finder-pipeline-research-prompt.md` | The earlier 2-part contact-finder self-prompt (finds and verifies the emails the cold email pipeline sends to) |

## Decisions so far

| Question | Answer |
|---|---|
| Use case | Job-seeker outreach (hiring managers, team leads, recruiters, founders) |
| Who sends | Me, my brother, later more job seekers; each as themselves, under their own accounts |
| Target volume | ~100 emails/day total (first touches + follow-ups) |
| Budget | $20/month total (domains, inboxes, tools, AI) |
| Prompt format | 2-part: deep research prompt + Claude Code build prompt (same as the contact-finder) |
| Build platform | Existing self-hosted n8n |

## How the pieces fit

1. **Contact-finder pipeline** finds the right people and their verified emails.
2. **Cold email pipeline** sends personalised sequences to them, handles replies, and improves from results.
3. Bounces from the cold email pipeline feed back into the contact-finder.

## How to use

1. Paste Part 1 of `cold-email-pipeline-self-prompt.md` into a deep-research tool. Give it `01-research/` as background if it accepts files.
2. Put its report in a `research/` folder.
3. Paste Part 2 into Claude Code with that folder.

## Caveat

The research is a preliminary pass, mostly from secondary and vendor sources. Treat every number as "to be re-verified". Part 1 of the self-prompt is designed to do that re-check.
