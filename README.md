# LinkRight

LinkRight helps job seekers. It tailors resumes to a job, preps interviews, finds roles, and gets referrals.
Live app: sync.linkright.in. Map checked by reading each folder on 2026-10-09.

## The products
| Folder | What it is | GitHub |
|---|---|---|
| `resume_sync_engine/` | **Sync**, the web app. Next.js site, Python resume worker, Chrome extension, Supabase and Oracle. Old local clone kept in its `versions/`. | sync-resume-engine |
| `production/` | **LinkRight CLI**, on PyPI as `linkright`. Code in `context/cli/linkright/`. | linkright_production |
| `skills_suite/` | **Claude Code plugin**: 10 `linkright-*` skills that share one career memory. | linkright-skills |

## Satvik's own use of the product (Client #0)
`linkright-push` makes three repos for every user. These are Satvik's.
| Folder | What it is | GitHub |
|---|---|---|
| `my_instance/memory/` | Career facts, signals, outcomes, job pipeline. Private. | linkright-memory |
| `my_instance/portfolio/` | Portfolio site and job Kanban dashboard. | linkright-portfolio |
| `my_instance/resume/` | Resume per role, on GitHub Pages. | linkright-resume |

## Automations
| Folder | What it is |
|---|---|
| `referral_automation/` | Refers other job seekers to American Express roles. n8n, MongoDB, a portal bot. Live. |
| `job_automation/` | Satvik's own PM job hunt, May 2026. Scrapes jobs, ranks them, makes tailored applications. |
| `job_automation/versions/` | Two copies of the scraper. The second is a link into `resume_sync_engine/Job automate` (some files are tracked there). |
| `job_automation/personalised_applications/` | 13 tailored applications. |
| `job_automation/references/` | Other people's open source job tools: career-ops, AIHawk. |
| `referral_automation/data_exports_2026-06_to_09/` | Amex referral CSVs and two MAIN n8n workflows (from `automation_exports`). |

`automation_exports/` and `automation_scripts/` now hold only links. Miraya leads, the LinkedIn post collector and `new_linkedin_campaign` moved to Miraya. The Oracle cloud resource list moved to AutoFlow `docs/`.

## GitHub plan (Satvik, 2026-10-09, idea ID045)
Keep all ~22 LinkRight repos. Later, merge what is needed into one codebase and drop what is not.

## Other
| Folder | What it is |
|---|---|
| `navii/` | Part-time growth work for Navii (heynavii.ai), a friend's startup. Resume screening pipeline, LinkedIn exports, `research_wiki/` (moved out of the CLI repo). |
| `research_docs/` | Specs, design handoff, plugin zips (`core_extension`, `specs_documentation`, `plugins`). |
| `resumes_vault/` | Satvik's CVs, other people's resumes, career profile. |
| `mission_job_switch/`, `interview_prep/`, `research/` | Satvik's personal job switch. Cluttered. To study deeply later (Satvik, 2026-10-09). |

`pm_toolkit` moved to `~/Desktop/Tools/pm_toolkit` (general PM skills).

Old paths still open through symlinks. Keys live in `~/Desktop/Secrets/linkright/`.
