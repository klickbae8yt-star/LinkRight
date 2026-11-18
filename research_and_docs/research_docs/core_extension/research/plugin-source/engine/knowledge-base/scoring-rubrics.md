# Scoring Rubrics

Engine knowledge. Generic to any user. The single definition of how content is judged. The Copy Chief, the voice authenticity eval, the Master Evaluator, and the System Optimizer all read this, so everyone scores the same way.

## Two layers, gates first then scores

A draft passes the hard gates before it earns any score. A gate breach means reject and rewrite, no score assigned.

## Hard gates, pass or fail

Values are read from config writing_protocol, this is the method.

- Punctuation, only the allowed set, any banned mark is a fail
- Banned words, any present is a fail, apply the config swap
- Hook signature, the hook fits the mobile cutoff and ends on the signature exactly
- Paragraph shape, no paragraph past the configured maximum sentences, white space natural
- Openers and closers, no banned corporate opener, no salesy closer
- Metric consistency, every number matches the ledger or is newly locked into it

## Scored dimensions, 0 to 10

| Dimension | Measures | Weight |
|---|---|---|
| Voice authenticity | Idiolect and argument match to the voice profile | High |
| Human texture, anti AI | Sentence length variation, burstiness, not flat | High |
| Hook impact | Curiosity or emotion inside the mobile cutoff | High |
| Value density | Every line earns its place, no filler | High |
| Emotional connect | The story or insight lands | High |
| Algorithm fit | Dwell, comment bait, save worth, format choice | High |
| Positioning ladder | Ladders to the owner's through line from config | Medium |
| Originality | Fresh angle, not generic | Medium |
| Clarity | Easy to follow | Medium |
| Media script clarity | Enough for the Media Creator to build | High |

## Threshold

Every dimension at or above 8, weighted average above 8.5. Up to five rewrite loops. If it still fails, flag to the Master Evaluator with the failing dimension named.

Voice authenticity and human texture are the dimensions that separate this from a generic bot. Weight them accordingly.
