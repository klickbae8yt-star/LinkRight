# P2-2 pilot: 60 real pairs judged by Claude (tier S, 13 Oct 2026)

Data: 135 scrubbed CVs (mostly freshers: 68 have 0 years) and 73 open India jobs. Pairs picked blind: 15 top-1 by today's pipeline (raw cosine + years window), 15 top-1 by prefix + CSLS, 10 from ranks 2 to 5, 20 random that pass the years window. Order of the CV and job blocks flips by pair number.

## Gate numbers
| Check | Mark | Result |
|---|---|---|
| Quote validity | 100% | 60 of 60 (code checks every quote letter for letter) |
| Order flip: 14 pairs re-read in the other block order | at most 10% change in final | 0 of 14 changed (final); 1 of 14 changed in the manager stage (r030 NO to MAYBE) |
| Self-agreement per stage (same 14) | at least 0.85 | skim 1.00, screen 1.00, domain 1.00, level 1.00, manager 0.93, risk 1.00, final 1.00 |
| Tokens per pair | measured | about 4k of session tokens per pair when each pair is read and written alone (read 2k, write 1k, rest is overhead) |

**Caveat (do not skip):** the re-judge ran in the same session, so I remembered the first answers. Treat the numbers as an upper bound. The real self-agreement test is P3-3, a re-judge in a new session a day later.

## What the labels say
Final decision over 60 pairs: NO 47, HOLD 9, STRETCH 3, REFER 1. Risk stage: DO_NOT_REFER 47, BORDERLINE 12, SAFE 1.
| Picked by | n | NO | HOLD | STRETCH or REFER |
|---|---|---|---|---|
| today's top-1 (raw cosine, years window) | 15 | 10 | 3 | 2 |
| prefix + CSLS top-1 | 15 | 11 | 2 | 2 |
| ranks 2 to 5 | 10 | 7 | 3 | 0 |
| random pass | 20 | 19 | 1 | 0 |
Read this carefully: on this pool of 73 India jobs, about two thirds of today's top-1 picks are a clear mismatch (wrong family, far under the level, or the required skill missing). Prefix and CSLS do not change that (10 of 15 against 11 of 15, not different). This is not the live flow: the live flow also has a family rule and a 0.65 floor that this pool does not replay. Confidence that the live wrong rate is high: 0.6. It needs P3 on the real pool to settle.

## Patterns the judge saw most
1. At least one required skill missing: 46 of 47 NOs (two or more: 38). Typical: Python or SQL for analytics jobs, Japanese, calling experience.
2. Level under or over: 23 of 47 NOs (freshers against 2 to 5 year roles; people with 3+ years against "up to one year" apprenticeships).
3. Different domain: 27 of 47 NOs.
4. Master's degree is a stated minimum on some data science posts; the judge held those (HOLD), it did not reject.

## Bugs found on the way (all fixed test first)
- Phone glued to a roll number was kept; 6-digit PIN codes after "- ", "MP" or a spaced comma were kept; a street in a "Location:" line was kept.
- A name part next to [NAME] stayed ("Ahmad", "Sai Pradeep", "SINGH"); titled names like "Prof.Ankit Jain" stayed.
- The scrubber must never run on job text: it read a title as a name and removed it. Rule written in `tasks/lessons.md`.

## Decision
Gate met on the numbers, with the same-session caveat. Next: P3-1 pool and scale. Budget: at about 4k tokens per pair, 1,200 pairs would cost 4.8M and break the 4M cap. Plan: group pairs by job so each job text is read once, shorter outputs, about 800 pairs first (about 2.4M).
