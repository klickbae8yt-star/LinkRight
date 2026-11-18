# Live replay: what the real Cosine Top 5 does today, and what to change (14 Oct 2026)

Setup: 120 random candidates from `candidate_embeddings` (67 with 0 years, 15 with 1, 38 with 2+), all 467 open jobs, the candidates' own referral history, and the exact live code (v5, backed up in `backups/2026-10-14/`). Read-only. Replay harness: `tests/cosine_top5_replay.js`. Labels: Claude, rubric v1.1, 88 pairs (top-1 per candidate with the floor removed), tier S, confidence 0.6.

## Correction to the lab result
The lab tests (V-4, fresh test) used all 450 jobs in every country. The live code only shows jobs in the candidate's chosen countries (default India) and inside a years window. In that live pool the campus and masters rules change 0 of 88 top-1 picks. So rules U1 and U1b are kept in the code but are not worth shipping now. The lab gain was real for a worldwide pool, not for this one.

## What matters in the live flow
| Finding | Number |
|---|---|
| Candidates who get a job today (floor 0.75, default same_stretch) | 8 of 120 (7%). The other 112 are skipped. |
| Same, floor 0.72 / 0.70 / 0.65 / none | 30 / 46 / 83 / 88 of 120 |
| Why 32 still get nothing with no floor | the form answer "same field" removes every job (family guessed from top-3 cosine jobs, and a small pool of 17 to 39 jobs) |
| Quality of the top-1 pick by cosine (88 labelled) | below 0.66: 17% acceptable. 0.66 to 0.70: 63% acceptable, 50% STRETCH or better. 0.70 to 0.72: 87% / 67%. 0.72 to 0.75: 96% / 83%. 0.75 and up: 100% / 60% (n=5) |
| If the floor were 0.70 | keeps 44 of 88 picks: 93% acceptable, 75% STRETCH or better, 25% REFER |
| If the floor were 0.72 | keeps 29: 97% / 79% / 28% |
| The Japanese-language job ("Operations Support", JLPT N3) | 7 of 88 picks, all 7 NO. A language rule fixes exactly these |
| Concentration | two jobs (Analyst-Data Science, Site Reliability Engineer I) take 49 of 88 picks (56%) |

## Advice
1. Lower the cosine floor from 0.75 to 0.70. In the live pool, cosine does separate good from bad picks, and the 0.70 to 0.75 band is as good as the top band. Yield goes from 7% to about 38% of candidates with 75% of picks STRETCH or better. 0.72 is the safer step (25%).
2. Turn on the language rule (`RULES.language = 'on'`): a job that asks for a language the CV does not name is not offered. Zero risk of harm; removes 8% of picks that are always wrong.
3. Turn on the per-job soft cap (`SOFT_CAP`, already in the code, off today) or near-tie spreading, because two jobs take 56% of picks.
4. Fix the family reading for the "same field" answer (use the resume-only family, `src/cvfamily.py`) so fewer people get `no_job_for_preference`. Needs its own test on the live pool.
5. Keep campus and masters rules in `shadow`.

## Deployed 14 Oct 2026, 01:49 IST
- SUB `JmV3niatmJiOgbmY` Cosine Top 5 v6 is live. Version 20af6af3 -> c156ff5e. Read-back equals build.
- Floor 0.70. Language rule on. Campus and masters rules in shadow. SOFT_CAP off, no value (Satvik: set later, configurable).
- Rollback: `n8n-cli workflow update JmV3niatmJiOgbmY --file backups/2026-10-14/JmV3niatmJiOgbmY_ROLLBACK_body.json`
- Next: check first real batch for errors and yield; read `staticData.shadow_v6`.
