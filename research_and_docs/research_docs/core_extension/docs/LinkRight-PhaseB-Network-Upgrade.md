# Phase B, linkright-network Upgrade Design

Date 2026-06-05. Design only, the live skill is not touched yet. This says exactly what we keep and what we fold in, gate by gate, so we do not rebuild what already works.

---

## What linkright-network already has, keep it

It is a strong base, and it is already deterministic first.

- A voice scorer, a python script with a 0 to 10 rubric and a 7 threshold, forbidden openings and closings, hedge detection. Deterministic.
- A constraint check against user_setup.md, do not mention and topics to avoid. Deterministic.
- Gate 0, it loads strength signals from linkright-mem before writing.
- Post types, POT, PM Insight, Process Transparency, Short Take, Milestone. A four week calendar. A cold email path. A brand audit. LinkedIn API scheduling with a dry run first.
- Absolute rules, never post without approval, never fabricate, always research with the browser.

None of this gets rebuilt. The scripts and the deterministic gates are exactly the model we wanted.

---

## What we fold in, gate by gate

1. Grounded personal voice. Today the voice profile is generic and the scorer checks generic rules. Upgrade, the skill reads the user's own grounded voice profile from their instance, the one built from the interview plus stylometry, and the scorer adds the measured signals, opens on a hard fact, at least one contrast pair, X not Y, closes on a short principle, bursty rhythm with sentence length variation as an anti AI check, the hook signature, and the banned word to swap mapping. Still a deterministic script, just checking the real voice, not a generic one.

2. A strategy step before drafting. Today mode selection jumps to a post type. Add a small strategy brief first, the target reader and the pain, the positioning ladder, the format that earns reach under the current algorithm, and a check that the topic is different from recent posts. This is the Content Strategist, folded in light.

3. Stronger review after the voice score. Keep the voice score, then add a three lens read, scroll stopper, trust builder, action driver, and an ethics and risk check for POT teardowns of real companies, claims sourced, no defamation, and credibility tags from memory respected. This is the Master Evaluator, folded in.

4. A media asset path. Today posts are text plus scheduling. Add an optional media step, a carousel or image script and a rendered asset, so a post can ship with its visual. This is the Media Creator, folded in.

5. Engagement after delivery. Today it stops at the clean post. Add the post time, a seeded first comment in the user's voice, and a first hour reply plan. This is Engagement Ops, folded in.

6. Memory contract alignment. Gate 0 already reads signals. Align it to the Career Memory contract, read Strengths and the Facts behind them, respect do_not_use and supporting_role_only and the confidence level, and pull by retrieval, not by loading the whole vault.

7. Knowledge by retrieval. Keep the gates and the voice core always loaded. Move the large situational reference, the post templates, the POT library, the algorithm mechanics, behind retrieval, so the skill stays lean as that reference grows.

---

## How we apply it, small steps, on your go

We do this one gate at a time, into the linkright-skills repo, nothing changes until you approve each step.

Suggested order, highest value first.
Step 1, the grounded voice, the profile read plus the scorer signals. This is the biggest quality lift.
Step 2, the memory contract alignment in Gate 0.
Step 3, the strategy brief before drafting.
Step 4, the stronger review gate.
Step 5, the media asset path.
Step 6, engagement after delivery.
Step 7, knowledge by retrieval.

Each step is small, reversible, and verified before the next.

---

## What stays untouched

The cold email path, the LinkedIn API path, the brand audit, and all the absolute rules. The deterministic scripts stay, we extend them, we do not replace them.
