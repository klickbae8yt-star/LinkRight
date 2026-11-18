# U-3: fresh test of the final updates (14 Oct 2026)

New random 150 CVs (not in V-4), 231 labelled pairs, same method as V-4 (Claude, rubric v1.1, compact; tier S, confidence 0.6; one judge, snippets only). Variants: plain cosine (`raw`); `U1` = campus-type roles only for people with years <= 1; `U1U2` = U1 + small bonus when the job title shares a specific word with the person's latest title; `U1U3` = U1 + near-tie load spreading; `U1U1b` = U1 + U1b (jobs titled "Campus Graduate ..." need a master-type degree word in the CV; found after seeing the first labels of this very test, so it is optimistic); `U1U1bU3` = U1 + U1b + near-tie.
Pass marks fixed in the plan: U1 at least +5 acceptable with interval above 0; U2 kept only if it adds at least +3; U3 kept only if quality loss is within noise and top-2 share <= 0.25.

| variant | acceptable (HOLD+) | good (STRETCH+) | REFER | domain not different |
|---|---|---|---|---|
| raw | 0.813 | 0.587 | 0.307 | 0.960 |
| U1 | 0.887 (+7.3; +3.3 to +12.0) | 0.653 (+6.7; +2.7 to +11.3) | 0.360 (+5.3; +1.3 to +10.0) | 0.953 (-0.7; -2.0 to +0.0) |
| U1U2 | 0.893 (+8.0; +3.3 to +12.7) | 0.660 (+7.3; +2.7 to +12.7) | 0.360 (+5.3; +1.3 to +10.0) | 0.960 (+0.0; -2.0 to +2.0) |
| U1U3 | 0.867 (+5.3; +0.0 to +10.7) | 0.653 (+6.7; +0.7 to +12.7) | 0.353 (+4.7; +0.0 to +9.3) | 0.933 (-2.7; -5.3 to -0.7) |
| U1U1b | 0.887 (+7.3; +3.3 to +12.0) | 0.813 (+22.7; +16.0 to +29.3) | 0.427 (+12.0; +6.7 to +18.0) | 0.953 (-0.7; -2.0 to +0.0) |
| U1U1bU3 | 0.867 (+5.3; +0.0 to +10.7) | 0.807 (+22.0; +14.0 to +30.0) | 0.413 (+10.7; +5.3 to +16.7) | 0.933 (-2.7; -5.3 to -0.7) |

## Reading
1. U1 holds on fresh CVs: +7.3 points acceptable (interval +3.3 to +12.0) and +6.7 on STRETCH or better. Same size as in V-4 (+8.0). Pass mark met.
2. U2 (closeness to the latest title) adds +0.7 acceptable over U1. Mark was +3. Dropped for now (the earlier 71% vs 56% signal was mostly about campus roles, not titles).
3. U3 (near-tie spreading): -2.0 acceptable vs U1 (interval -4.7 to +0.7), 0.0 on STRETCH or better. Within noise; top-2 job share falls from 0.30 to 0.23; jobs used 155 to 176 (full 3,586 batch). Keep as an option, not required. Domain-not-different drops 2.7 points, so watch it in shadow.
4. U1b is the larger win: STRETCH or better goes 65% to 81% (+16 over U1, interval +10.7 to +22.0); REFER 36% to 43%. Reason: 108 labelled pairs in V-4 + this test were "Campus Graduate / Masters" programs; for CVs with no master-type degree none was a REFER (8 STRETCH, 54 HOLD, 21 NO). Caveat: rule found on these labels. Logic is plain (the JD says master's required), so confidence in direction 0.8; in size 0.5. A third sample (new 150 CVs) is the cleanest check; shadow numbers on a real batch can serve instead.
5. Cost: eligibility + masters masks take about 2.5 s for all 3,586 x 450 pairs (limit 30 s). 99.9% of resumes still get a job.

## Decision for the live update
Ship U1 + U1b (both are plain eligibility rules). U3 optional. U2 dropped. Next step: SHADOW in `Cosine Top 5` (needs Satvik's haan).
