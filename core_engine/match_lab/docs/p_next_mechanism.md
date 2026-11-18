# Next mechanism: free checks (13 Oct 2026)

Data: 3,586 resumes x 450 open jobs (production vectors), years window applied, country not applied yet. No labels used. Tier S, confidence 0.6 for the direction, 0.3 for any quality claim (no label has judged these picks yet).
"Family = CV family" uses the new classifier (`src/fieldclf.py`). "Gate" = job family must equal CV family (the form default: same field, same level).

families: {'data': 95, 'engineer': 72, 'finance_risk': 97, 'manager': 12, 'ops': 22, 'product': 59, 'sales_travel': 93}
| variant | resumes with a job | jobs used | top-2 share | max load | family = CV family | same as raw top-1 | ms |
|---|---|---|---|---|---|---|---|
| raw cosine | 1.00 | 169 | 0.25 | 472 | 0.79 | 0.60 | 0 |
| centred | 1.00 | 299 | 0.14 | 296 | 0.69 | 0.17 | 122 |
| CSLS(raw) | 1.00 | 257 | 0.24 | 539 | 0.80 | 0.36 | 358 |
| CSLS(centred) | 1.00 | 321 | 0.22 | 547 | 0.72 | 0.16 | 500 |
| sinkhorn caps(centred) | 1.00 | 339 | 0.04 | 73 | 0.56 | 0.12 | 2607 |
| gate + raw | 1.00 | 166 | 0.23 | 506 | 1.00 | 0.48 | 0 |
| gate + CSLS | 1.00 | 227 | 0.25 | 583 | 1.00 | 0.34 | 420 |
| gate + CSLS(centred) | 1.00 | 258 | 0.25 | 660 | 1.00 | 0.17 | 672 |
| gate + sinkhorn caps | 1.00 | 245 | 0.09 | 168 | 1.00 | 0.15 | 3082 |
| field anchor lam=0.5 + CSLS gate | 1.00 | 249 | 0.17 | 336 | 1.00 | 0.27 | 582 |
| field anchor lam=1.0 + CSLS gate | 1.00 | 209 | 0.20 | 496 | 1.00 | 0.24 | 649 |

Reading:
- Raw cosine puts the top-1 job in the CV's own family only 79% of the time. A gate makes it 100%.
- Sinkhorn with soft caps cuts the top-2 job share from 25% to 9% and the busiest job from 506 to 168 resumes.
- Sinkhorn takes about 3.7 s per full batch. The pass mark is 30 s.
- These numbers say nothing about whether the picks are good. That needs labels (V-4).
- Leading candidate for V-4: gate + sinkhorn caps. Control: raw cosine. Second: gate + CSLS.

## F-4 rerun (14 Oct 2026): gate now uses the resume-only family
CV family = 50/50 mix of `cvfamily` (titles + summary) and the embedding classifier; gate = same group, with engineer and data as one "tech" group. Column "family = CV family" is the EXACT family, so it stays below 1.0 by design.

| variant | resumes with a job | jobs used | top-2 share | max load | family = CV family | same as raw top-1 | ms |
|---|---|---|---|---|---|---|---|
| raw cosine | 1.00 | 169 | 0.25 | 472 | 0.69 | 0.60 | 0 |
| centred | 1.00 | 299 | 0.14 | 296 | 0.62 | 0.17 | 371 |
| CSLS(raw) | 1.00 | 257 | 0.24 | 539 | 0.72 | 0.36 | 569 |
| CSLS(centred) | 1.00 | 321 | 0.22 | 547 | 0.66 | 0.16 | 921 |
| sinkhorn caps(centred) | 1.00 | 339 | 0.04 | 73 | 0.51 | 0.12 | 3209 |
| gate + raw | 0.99 | 186 | 0.25 | 463 | 0.82 | 0.52 | 0 |
| gate + CSLS | 0.99 | 253 | 0.25 | 571 | 0.87 | 0.33 | 402 |
| gate + CSLS(centred) | 0.99 | 310 | 0.26 | 681 | 0.88 | 0.16 | 568 |
| gate + sinkhorn caps | 0.99 | 308 | 0.08 | 135 | 0.79 | 0.14 | 4105 |
| gate + CSLS + exact-family bonus | 0.99 | 253 | 0.25 | 573 | 0.88 | 0.33 | 1531 |
| gate + sinkhorn caps + exact bonus | 0.99 | 308 | 0.07 | 132 | 0.80 | 0.13 | 3577 |
| field anchor lam=0.5 + CSLS gate | 0.99 | 287 | 0.17 | 349 | 0.95 | 0.25 | 640 |
| field anchor lam=1.0 + CSLS gate | 0.99 | 238 | 0.21 | 518 | 0.98 | 0.21 | 1292 |

Reading: with the resume-only gate, 99% of resumes still get a job. Gate + Sinkhorn caps: 308 jobs used (raw 169), top-2 share 0.08 (raw 0.25), busiest job 135 resumes (raw 472), 2.3 s per batch. Inside the tech group, only 79% of picks have the exact family of the CV; the small exact-family bonus (0.05) does nothing. Pick quality is still unmeasured; it needs V-4 labels.
