# Eval, Voice Profile QA

The Voice Synthesizer runs this on the voice profile before it ships. This is also the gate for the whole Voice Building workflow. Every item must pass, because every post the system writes later depends on this file.

## Fusion gates

- [ ] Both layers present, cognition from the interview and language from the metrics
- [ ] No trait stated without evidence in the transcript or the metrics

## Usability gates

- [ ] Rules are concrete and scorable, a downstream agent can grade a draft against each one
- [ ] A clear do list and a clear do not list
- [ ] Signature phrases included, and the sentence rhythm range as real numbers
- [ ] Paired examples present, the owner's raw line next to the configured output language target
- [ ] The profile is tight, no line that fails to earn its load on every downstream run

## Config gates

- [ ] The profile honours config, output language and writing rules are expressed, not changed
- [ ] No rule duplicated from config, the profile points to config for the hard rules

## Result

Pass only if every box is checked. On a miss, name the failing section and rewrite it before shipping.
