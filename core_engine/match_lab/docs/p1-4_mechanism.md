# P1-4 mechanism table (synthetic set, tier S, mechanism only)

Set: 24 candidates x 14 jobs = 336 pairs; gold = constructed truth (Claude agreed on 120 pairs, 0.975). Good pairs (REFER/STRETCH): 22. Wrong rate = share of referred top-1 picks whose truth is NO. n = number of candidates referred (of 24). Last column: relative drop of wrong rate at n=12 vs P0, 95% bootstrap interval of the difference, fixed adopt rule.

| pipeline | wrong n=8 | wrong n=12 | unsafe n=12 | critical n=12 | P@1 | nDCG@5 | MRR | top-1 AUC | len corr | top-2 job share | vs P0 (n=12) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P0 today: raw cosine | 0.50 | 0.42 | 0.42 | 2 | 0.46 | 0.79 | 0.53 | 0.66 | 0.43 | 0.42 | +0% [+0.00,+0.00] no |
| P0y raw cosine + years window | 0.38 | 0.25 | 0.25 | 0 | 0.54 | 0.85 | 0.58 | 0.64 | 0.20 | 0.42 | +40% [+0.00,+0.33] no |
| H0 prefix only | 0.25 | 0.25 | 0.33 | 1 | 0.46 | 0.82 | 0.53 | 0.84 | 0.50 | 0.50 | +40% [+0.00,+0.33] no |
| H1 strip boilerplate/old roles only | 0.12 | 0.33 | 0.33 | 2 | 0.46 | 0.75 | 0.51 | 0.80 | 0.59 | 0.50 | +20% [-0.17,+0.33] no |
| H2a CSLS (k=3) on raw | 0.25 | 0.33 | 0.33 | 1 | 0.50 | 0.84 | 0.56 | 0.74 | 0.37 | 0.33 | +20% [-0.08,+0.33] no |
| H2b centred vectors | 0.12 | 0.25 | 0.25 | 1 | 0.54 | 0.86 | 0.58 | 0.73 | 0.34 | 0.42 | +40% [+0.00,+0.42] no |
| H3 BM25 + cosine RRF | 0.25 | 0.25 | 0.25 | 3 | 0.58 | 0.90 | 0.60 | 0.65 | 0.52 | 0.50 | +40% [-0.08,+0.42] no |
| H4 years gate x skill coverage in bullets | 0.00 | 0.00 | 0.00 | 0 | 0.62 | 1.00 | 0.62 | 1.00 | 0.43 | 0.25 | +100% [+0.17,+0.67] ADOPT |
| H5 late interaction (per must-have) | 0.25 | 0.17 | 0.25 | 1 | 0.54 | 0.88 | 0.58 | 0.83 | 0.38 | 0.33 | +60% [-0.08,+0.50] no |
| H8 cosine + title match | 0.00 | 0.08 | 0.17 | 0 | 0.62 | 0.92 | 0.62 | 0.77 | 0.50 | 0.25 | +80% [+0.00,+0.58] no |
| P1 = H0+H1 | 0.25 | 0.33 | 0.33 | 2 | 0.46 | 0.76 | 0.52 | 0.74 | 0.60 | 0.42 | +20% [-0.17,+0.33] no |
| P2 = P1 + CSLS | 0.12 | 0.25 | 0.25 | 2 | 0.50 | 0.80 | 0.53 | 0.79 | 0.58 | 0.42 | +40% [+0.00,+0.33] no |
| P3 = P2 + BM25 + coverage + years gate (RRF) | 0.00 | 0.00 | 0.08 | 0 | 0.58 | 0.93 | 0.60 | 0.98 | 0.25 | 0.33 | +100% [+0.17,+0.67] ADOPT |
| P5 = learned fusion (leave-one-candidate-out) | 0.00 | 0.00 | 0.08 | 0 | 0.62 | 1.00 | 0.62 | 0.88 | 0.57 | 0.33 | +100% [+0.17,+0.58] ADOPT |
| Ceiling: constructed truth | 0.00 | 0.00 | 0.00 | 0 | 0.62 | 1.00 | 0.62 | 1.00 | 0.39 | 0.25 | +100% [+0.17,+0.67] ADOPT |

Not run (need a model that is not on this box; a pull needs a go): H6 other embedders (mxbai-embed-large, bge-m3), H7 cross-encoder rerank (bge-reranker-v2-m3), P4. H10 typed checks: Claude is the teacher; its ceiling is the last row. Warning: the generator and the structured features share one vocabulary, so H4/H5/P3/P5 are optimistic here. Adoption needs the real sample.

## Reading the table (tier S, confidence in brackets)
- Only 22 of 336 pairs are good, and n is 24 candidates, so every interval is wide. Only the structured and learned rows pass the fixed adopt rule, and they share the generator's vocabulary. Treat them as "the idea can work" (0.5), not as proof.
- Prefix alone (H0) lifts the top-1 AUC from 0.66 to 0.84 and halves the wrong rate at n=12 (0.42 to 0.25), but the interval touches zero. It is cheap, so it goes into the real-data test (0.6).
- A years window on top of raw cosine (P0y) already removes the two critical errors. Skill coverage in bullets (H4) is the strongest single factor here (0.7 that it helps on real CVs; real skill words are messier).
- Hub and length drift: raw cosine correlates 0.43 with CV length. Only P3 (0.25) and P0y (0.20) bring it down.
- This Mac's Ollama returns HTTP 400 ("input length exceeds the context length") for the 1,695-word CV, where the Oracle probe saw a silent tail drop. Same model, different behaviour. Check the Oracle box again before any change (open question, 0.5).
- Not run: H6 (other embedders) and H7 (cross-encoder). They need a model pull.
