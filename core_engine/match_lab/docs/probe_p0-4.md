# P0-4 probe: Ollama, nomic-embed-text, long inputs and task prefixes (13 Oct 2026)

Script: `src/probes/ollama_probe.py` (made-up text only, no personal data). Run on the Mac (Ollama 0.24.0) and, for the key fact, on the Oracle box (2 embeddings).

| Claim | Evidence (numbers) | Tier | Conf |
|---|---|---|---|
| `nomic-embed-text` is v1.5-class, 137M, **context length 2048**, Modelfile `num_ctx 8192` | `ollama show` on Mac and on Oracle: identical output | S | 0.95 |
| The model never sees more than **2048 tokens**, whatever `num_ctx` says | Mac: with default, `num_ctx` 2048 and `num_ctx` 8192, `tokens_seen` is capped at 2048; 3 text lengths | S | 0.95 |
| Text after the cap is **silently dropped**: the vector of the full text equals the vector of its first ~2000 words | Mac: cos(full, first 2000 words) = 1.0000 for 2,500 and 4,500 word inputs; cos(full, tail topic only) = 0.30. Oracle: cos(full, first 2000 words) = 1.0000, `tokens_seen` 2048 | S | 0.95 |
| `truncate=false` makes Ollama refuse a too-long input (HTTP 400) | Mac, 6,000 words | S | 0.9 |
| So today every CV and JD longer than about 1,500 words is judged by its first ~2,048 tokens only (the end, where JD requirements and CV recent roles may sit, is ignored) | follows from the lines above; the share of real texts above the cap is NOT measured yet (new bead) | S, inference | 0.6 until measured |
| A task prefix changes the cosine scale: mean true-pair cosine on a toy set 0.685 (no prefix), 0.668 (`search_document:` + `search_query:`), 0.749 (`search_document:` on both), 0.821 (`clustering:`). The 0.65 floor means different things per setting | Mac, 4 profiles x 6 jobs | S, toy | 0.3 for any ranking claim (n=4, all variants ranked 4/4 correctly) |
| Margins top1-top2 moved a little (two profiles better with query/document prefixes, two slightly worse) | same toy | S, toy | 0.2 |

What this changes:
- H0 is now two facts, not a guess: (a) the 2048-token cap is real on both machines, (b) any prefix change moves the cosine scale, so the 0.65 floor would have to be recalibrated with it.
- New bead P2-4: measure how many real JDs and CVs exceed 2,048 tokens and what sits in the dropped tail (tokeniser count on the scrubbed export). If many do, "embed a role-focused view" (H1) is not an option, it is a fix.
- The toy prefix test proves nothing about ranking; the real test is the bake-off on the gold set (P4-1).

## P2-4: token length of real texts (13 Oct 2026, nomic tokenizer via Ollama prompt_eval_count; tier S; confidence 0.85)
| Text | n | Over 2048 tokens | Median tokens | Max tokens | Tokens per word |
|---|---|---|---|---|---|
| CV (scrubbed, embedding_text) | 135 | 0 | 714 | 1571 | 1.46 |
| JD (scrubbed, embedding_text) | 73 | 1 | 622 | 1978 | 1.32 |
- Truncation is a small problem on real data: no CV and only 1 of 73 JDs passes the context. The "long text loses its tail" worry (H0 part) matters far less than on my synthetic long CV.
- One pair costs about 1,340 tokens of input to read (714 + 622), plus about 600 for the judgement: roughly 2,000 per pair. 1,200 pairs is about 2.4M, inside the 4M cap.
- Real population: 68 of 135 CVs have 0 years. The set is mostly freshers, so the fresher and projects rules in the rubric matter most.
