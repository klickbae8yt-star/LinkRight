# Project Context

## Project
- **Name:** Multi-Portal Career API & n8n Ingestor
- **Objective:** Replace manual browser navigation and MHTML saves with direct plain-HTTP API calls per company career portal, feeding one unified fault-isolated n8n Data Table (`google_careers_jobs`, key: `job_id`).

## Acceptance Gates
- Zero browser or manual MHTML upload for enabled portals.
- One failing portal never breaks the rest of the loop.
- Every n8n Code node passes strict `node:vm` tests (no `URLSearchParams` or `require`).

## Decisions Log
| Date | Decision | Rationale |
|---|---|---|
| 2026-11-10 | Use Google Careers SSR `ds:1` plain GET instead of `batchexecute` | `batchexecute` fails without Google login `SNlM0e` token; SSR `ds:1` needs zero cookies and returns all 21 job fields. |
| 2026-11-10 | Store cloned `api-anything` and `rea` inside `vendor/` | Keeps reference repos local and workspace root clean. |
| 2026-11-11 | Use `Portal Registry` + `Fetch Portal` (`continueRegularOutput`, `batchSize: 1`) + `Parse Portal Jobs` (`try/catch` per portal) | Guarantees one broken portal never stops healthy portals from saving to the Data Table. |

