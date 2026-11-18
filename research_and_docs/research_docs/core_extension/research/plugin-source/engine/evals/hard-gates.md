# Eval, Hard Gates

The Copy Chief runs this. Pass or fail, no score. One breach means reject and rewrite. Values are read from config writing_protocol, this lists what to check.

- [ ] Punctuation, only the allowed set is present, no banned mark, no colon, semicolon, em dash, en dash, arrow
- [ ] Banned words, none present, any found is swapped per config
- [ ] Hook fits the mobile cutoff from config
- [ ] Hook ends on the configured signature, exactly, on its last line
- [ ] Multi sentence hook is split onto its own lines with blank lines between
- [ ] No paragraph runs past the configured maximum sentences
- [ ] White space reads natural, not a staircase of single lines
- [ ] No corporate opener, no salesy closer
- [ ] First person, no hedging words
- [ ] Every number matches the ledger or is newly locked into it

Result, pass only if every box is checked. On any fail, name the exact broken rule and send the draft back.
