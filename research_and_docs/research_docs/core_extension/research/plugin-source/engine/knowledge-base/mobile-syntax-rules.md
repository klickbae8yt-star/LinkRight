# Mobile Syntax Rules

Engine knowledge. Generic explainer of how to apply a user's hard writing rules. The actual values, allowed punctuation, banned words, hook signature, paragraph shape, are read from `config/user-config.yaml` under writing_protocol. A different user with different rules needs no change here, only a different config.

## How these rules work

These are hard gates, not scored preferences. A draft that breaks any of them is rejected and rewritten before scoring even starts. The config holds the values, this file holds the method for applying them.

## The gate categories

Punctuation. The config lists an allowed set and a banned set. Scan the post body, any banned mark present is an automatic fail. Read the allowed and banned lists from config, never assume them.

Banned words. The config holds a banned word list and suggested swaps. Any banned word present is a fail. Apply the swap from config, for example a corporate filler word becomes a plain operational word.

Hook signature. The config defines the hook rules, a character cutoff for the mobile fold, whether a multi line split is required, and a signature that closes the hook. Check the hook fits the cutoff and carries the signature exactly.

Paragraph shape. The config sets a maximum sentences per paragraph and a white space style. Check no paragraph runs longer, and the spacing reads natural rather than a staircase of single lines.

Openers and closers. The config flags whether corporate openers and salesy closers are banned. Scan the first and last lines against those flags.

## Why config driven

Writing rules are the user's preference, not the engine's opinion. Keeping the values in config means the same gate logic serves any user. The gate reads the rule, applies it, and reports a clean pass or a specific fail naming the broken rule.
