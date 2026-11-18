# V-4: do the fancier scorers pick better jobs than plain cosine? (14 Oct 2026)

Test: 150 random CVs (resume-only family known, years window applied, same 445 open jobs with text). Each variant picks one job per CV. Claude read each pair (CV snippet + JD gist) and gave `REFER / STRETCH / HOLD / NO` and domain `same / adjacent / different` by rubric v1.1. Labels: tier S, confidence 0.6 (one judge, snippets only, 373 pairs; me, not a human). Metrics: share of picks that are HOLD or better, STRETCH or better, REFER, and not a different domain. Intervals: paired bootstrap over CVs, 5000 draws, against plain cosine on the same CVs. File: `src/v4_metrics.py`. Labels: `data/v4/labels.jsonl`.

Pass marks fixed before the run: at least +15 points on top-1 acceptable with the interval above 0; top-2 job share at most 25%; family-correct at least 0.90; batch under 30 s.

| variant | acceptable (HOLD+) | good (STRETCH+) | REFER | domain not different |
|---|---|---|---|---|
| raw | 0.780 | 0.627 | 0.307 | 0.947 |
| gate_csls | 0.680 (-10.0; -16.7 to -4.0) | 0.540 (-8.7; -16.0 to -1.3) | 0.267 (-4.0; -10.7 to +2.0) | 0.887 (-6.0; -10.7 to -1.3) |
| gate_sink | 0.667 (-11.3; -19.3 to -3.3) | 0.513 (-11.3; -21.3 to -1.3) | 0.160 (-14.7; -22.7 to -6.7) | 0.900 (-4.7; -9.3 to +0.0) |
| gate_raw | 0.740 (-4.0; -8.0 to -0.7) | 0.600 (-2.7; -6.7 to +1.3) | 0.280 (-2.7; -5.3 to -0.7) | 0.920 (-2.7; -6.0 to +0.0) |
| neartie_d0.01 | 0.707 (-7.3; -12.0 to -3.3) | 0.547 (-8.0; -14.0 to -2.7) | 0.267 (-4.0; -8.0 to +0.7) | 0.893 (-5.3; -9.3 to -1.3) |
| neartie_d0.02 | 0.700 (-8.0; -13.3 to -2.7) | 0.540 (-8.7; -15.3 to -2.0) | 0.200 (-10.7; -16.0 to -4.7) | 0.887 (-6.0; -10.7 to -1.3) |
| raw_elig | 0.860 (+8.0; +4.0 to +12.7) | 0.707 (+8.0; +4.0 to +12.7) | 0.380 (+7.3; +3.3 to +11.3) | 0.940 (-0.7; -2.0 to +0.0) |
| elig_neartie_d0.01 | 0.813 (+3.3; -2.7 to +9.3) | 0.647 (+2.0; -4.7 to +8.7) | 0.353 (+4.7; -0.7 to +10.7) | 0.927 (-2.0; -5.3 to +0.7) |

Spread (full 3,586 batch, from the free check): raw top-2 share 0.25 to 0.27; gate + Sinkhorn caps 0.08; near-tie spreading (delta 0.01) 0.20; eligibility + near-tie 0.23.

## What the numbers say
1. No variant met the +15 mark. The best was plain cosine plus one deterministic rule: +8.0 points (interval +4.0 to +12.7) on top-1 acceptable, +7.3 on REFER.
2. The maths that spreads load (CSLS, Sinkhorn caps, near-tie spreading) lowered pick quality by 7 to 11 points on acceptable. Spreading has a price: the second-best job is usually a little worse than the best one. Plain cosine's top-1 is not the broken part (78% acceptable, 5% different domain on this test).
3. The family gate alone also lost 4 points. It changed only 19 of 150 picks, and in 10 of those the old pick was better. The changed rows are mostly CVs whose family was guessed as product, ops or sales, where the family reader is weakest (few gold examples).
4. The big, boring finding: 25 of 150 plain-cosine picks were campus, apprentice or internship roles given to people with 1 or more years of work. For people with 2 or more years, 13 of 15 such picks were NO. For 0 to 1 year they were fine. Rule: campus-type titles (campus, apprentice, internship, intern, graduate program, early career) are shown only to people with 1 year or less of experience. 118 of 450 open jobs are campus-type.
5. Caution: that rule was found by looking at these same labels, so +8 is optimistic. It needs a fresh test on new CVs before it goes live. The reason behind the rule is real (eligibility), so confidence that it helps is 0.75; confidence in the size is 0.5.

## What to do next (needs Satvik's yes)
- Shadow-run the eligibility rule on plain cosine in `Cosine Top 5` and count how many picks change (no effect on referrals).
- Keep CSLS, Sinkhorn caps and the gate as tools for the load problem only, not as the main ranker. If we want spread, use near-tie spreading on top of the eligibility rule (quality stays within noise: +3.3, interval -2.7 to +9.3; top-2 share 0.23).
- Fix the weak part (family reading for product, ops, sales CVs) before any hard family gate is used again.
