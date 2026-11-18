# Cold Email Project: Export

Exported 24 Oct 2026 from the "cold email" project.

## Contents

| File | What it is |
|---|---|
| `00-README.md` | This index |
| `01-preliminary-tool-notes.md` | The starting notes on email-finder tools (free / freemium / paid) shared at the start of the conversation. Not yet verified. |
| `contact-finder-pipeline-research-prompt.md` | Part 1: deep research prompt for email/phone finder tools. Part 2: Claude Code prompt to audit, design and build the n8n lead-enrichment pipeline (email only / phone only / both), wired into the existing ingestion pipeline. |
| `cold-email-pipeline-self-prompt.md` | Part 1: deep research prompt for cold email sending and deliverability. Part 2: Claude Code prompt to build the n8n sending pipeline that sits downstream of the contact finder ($20/month cap). |

## Status

- These files are **prompts and plans**. The deep research itself has not been run yet, so there is no verified research report.
- Next step: run Part 1 of each prompt in a deep-research tool, then give the report plus Part 2 to Claude Code.
- Order: contact finder first (it produces the verified leads), then cold email (it sends to them).
