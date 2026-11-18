# Stylometry Method

Engine knowledge. Generic to any user. The Stylometrist loads this to measure the owner's language fingerprint from the transcript, past chats, and any real samples.

The fingerprint is content independent. It lives in how someone writes, not what they write about. That is why it survives across topics and why a machine cannot copy it by accident. Measure it, do not describe it in adjectives.

## What to measure

Function words. The small grammatical words, the, of, just, so, actually, that carry no topic but are used in a way specific to each person. Note the ones that repeat and how they are used. These are the strongest authorship signal.

Sentence length distribution. Record the spread, shortest, longest, typical. Do not average it away, the spread is the point.

Burstiness. The mix of very short and long sentences. Humans swing, flat uniform length reads as machine. Record the range and whether the owner swings hard or stays even.

Punctuation profile. Which marks the owner actually uses, and which they never touch. Confirm against config, because the allowed set is a stated preference, then check the real samples match it.

Signature phrases and n grams. Two and three word combinations the owner reaches for without thinking. Pull them verbatim with a rough frequency.

Openers and closers. How they tend to start and end a thought. People have habits here they are unaware of.

Registers. Most people write in more than one register, for example a reflective long form for stories and a quick operational tone for fast replies. Capture each, and note which one the content voice should sit closest to. A person's quick replies are not their considered voice, but the bluntness can feed hooks and opinion posts.

Raw versus output words. Flag words the owner uses naturally that the output rules in config ban. Record the swap, for example a filler word the owner says out loud that maps to a plain word in the written output. This lets the synthesizer keep the voice while honouring the gates.

## How to work

Quote before you conclude. Every claimed marker carries a real example from the owner's writing and a rough count. Separate stable markers, seen across many samples, from one off quirks, seen once. Flag thin signals as thin, never invent a marker to fill a gap.

Mind the source. Operational chat, quick and transactional, reads differently from reflective writing. Note which source a marker came from, because a person's quick replies are not their considered voice.

## Output

A measurable baseline, written to the metrics file, that the voice authenticity and human texture scorers grade drafts against later. Numbers where possible, verbatim examples always.
