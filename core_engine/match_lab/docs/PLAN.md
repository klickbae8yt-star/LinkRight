# Plan: stop wrong referrals. Teach the system to judge a CV like a recruiter and a hiring manager, then distil it into Laya (13 Oct 2026)

## Context
Today the Amex referral flow picks jobs with ONE number: cosine similarity of `nomic-embed-text` vectors of the whole CV and the whole JD, with a flat 0.65 floor (`src/n8n/live/JmV3niatmJiOgbmY/Cosine_Top_5.js`; rules for country, years, family around it). Satvik's goal: never send a wrong referral. Nobody can know who will perform in an interview, so the target is what a careful professional CAN judge from the page: **"would a recruiter and then a hiring manager move this CV forward for this job, and is the referrer safe to put their name on it?"**
Two tracks share one data set:
- **Track A (research):** is there a better scorer than cosine? Many hypotheses, one simulation, one fixed pass mark.
- **Track B (Laya):** capture data from the live flow, let Claude (the Claude Code subscription session, NEVER the Claude API) write deep "recruiter + hiring manager" judgements, train Laya on them (Kaggle or Colab), serve it on the Oracle box. Laya replaces Jev in the recurring loop, so running cost is 0.
**Laya must be fine-tuned.** The untouched Laya is near chance (0.36 on its own benchmark) and is never used anywhere, not even in shadow. The goal is a Laya fine-tuned on OUR judgements that does better than TypeSafe Jev on our task; if it does not, it does not ship.
Nothing here changes a live workflow until its own gate and Satvik's "haan".

## Answers already given by Satvik (13 Oct)
- Real data: read-only export of CVs and open jobs, scrubbed (no name, email, phone, links), kept only on the Mac in a git-ignored folder.
- Jev (OpenRouter): cap Rs 100; first a 300-pair comparison with Claude, more only if Jev agrees with Claude.
- Claude is the final teacher, no heavy human audit. Labels are therefore tier S ("Claude, not human-checked") and every result says so. I still show 10 sample judgements ("does this feel like a recruiter?", 5 minutes, optional) and add machine checks so the teacher cannot drift silently.
- Use the Claude Code session only, no API calls.

## What I found (read-only), with tiers and confidence
| Finding | Evidence | Tier | Conf |
|---|---|---|---|
| Embedding calls send raw `embedding_text` with NO task prefix (`Generate Embeddings` in the 3 embedding SUBs) | repo workflows | S | 0.95 |
| nomic model card: the text "must" start with a task prefix (`search_document:` / `search_query:`) | HF model card | A | 0.9 |
| Ollama library page lists a 2K context for `nomic-embed-text`; one project reports silent truncation; another says the Modelfile sets 8192. Unknown on our box | Ollama page, GitHub reports | A/C | 0.5, so TEST (`ollama show`, long-input probe) |
| P1 to P5 already measured: score rises with CV length and years, #1 vs #2 gap is 0.011, domain mismatch invisible, 2 reqs took 59% of referrals | `docs/Matching_Quality_Problems_and_Solutions.md` | S | 0.9 |
| E1 (weighted cosine over JD sections) gave no clear gain, n=16, labels were a quick look | `docs/research/experiments.md` | S | 0.7 that weights alone do not help |
| No fit labels exist: `data/fit_label_sample_2026-10-06.csv` has 30 rows, `fit_yes_no` all empty | repo | S | 1.0 |
| Cosine has no length notion, but dense encoders still prefer some lengths; anisotropy squeezes cosines into a narrow band; hubness: a few vectors are everyone's neighbour; fixes: CSLS, centering, rank normalisation | BEIR, hubness papers, 2026 anisotropy preprint | A/B | 0.7; helps most when the space is crowded, can hurt a little otherwise |
| Hybrid BM25 + dense with RRF often beats dense alone; an untuned fusion can lose | vendor and practitioner write-ups | C | 0.5 |
| Two-stage "cosine for recall, reranker for precision" is the common resume-job pattern; I found NO study proving a reranker or skill extraction beats cosine on resumes | arXiv (Synapse, ConFit v2, CareerBERT) | B | 0.6 that the gap is real, so we measure |
| LLM judges agree with humans at kappa about 0.6 to 0.8, show position and verbosity bias; anchored 0-3 rubrics beat "rate 1-10" | judge surveys | B | 0.7 |
| Laya: 421M ModernBERT decision model, one forward pass, about 113 ms per question on CPU (Intel Mac Pro figure), base checkpoint near chance (0.36), 0.77 after fine-tune on its own benchmark, needs about 5k+ items (1,100 items "collapsed"), option order and boolean labels change answers, negation unsafe, over-confident until calibrated, Apache-2.0 | Laya README | A (author, wants stars) | 0.8 facts, 0.5 for our task |
| Kaggle 2xT4 notebook is documented; Colab single T4 is not; the MPS script is for a 16 GB Mac, ours is an M1 with 8 GB | README, `sysctl` | A/S | use Kaggle first |
Existing documents to extend, not duplicate: `docs/research/laya_finetune_colab_plan.md` (years-sentence task, E3) and `docs/research/experiments.md` (add E4 and E5).

## The deep criteria: a recruiter and a hiring manager, stage by stage (rubric v1)
Every judgement is typed fields with VERBATIM evidence (a quote from the CV or JD; code checks the quote exists). Name, gender, age, photo, religion, caste, marital status, nationality and college prestige are never a reason. Person fields are scrubbed before Claude reads anything.

| Stage | Who, how long | What is judged | Output |
|---|---|---|---|
| 0 Knock-outs (code, no model) | system | country / work authorisation from the form, years window `[lo, hi]`, already referred, CV readable, duplicate | PASS or the reason |
| 1 Skim | recruiter, 7 seconds: top ~15 lines | does the headline or last title name this job's family; is the summary specific or buzzwords; is a relevant role recent (24 months); employer and place signal; structure and readability (text proxies); instant red flags | `PASS_SKIM / MAYBE / FAIL_SKIM` + one line "the 7-second feeling" |
| 2 Screen | recruiter, 1 minute | the JD's top 5 to 8 must-haves (skills, tools, domain, degree, years, certs), each `MET` (quote) / `PARTIAL` / `MISSING` / `UNKNOWN`; fresher: projects and internships count as evidence | `ADVANCE / HOLD / REJECT`, coverage, knock-out count |
| 3 Read | hiring manager, 1 to 2 minutes | do the last two roles touch this team's problem; ownership and scope (led or assisted); numbers and outcomes; level fit and title inflation; domain `same / adjacent / different` and whether skills transfer; technical depth (used and described, or only listed); stability (tenure, gaps, job hopping in 5 years); "what would make the manager say: this person has done my problem" | `INTERVIEW / MAYBE / NO` + top 3 reasons |
| 4 Red flags | both | keyword stuffing, JD copied into CV, inflated title, vague bullets, unexplained gap, frequent switches, skills without evidence, over-qualified (flight risk), long irrelevant history | yes/no per flag with quote |
| 5 Referrer risk | us | "if a person staked their name on this referral, how likely is an embarrassing outcome?" Borderline means hold, never refer | `SAFE / BORDERLINE / DO_NOT_REFER` |
| 6 Final | | one decision, confidence 0 to 1, top 3 reasons, top 3 risks | `REFER / STRETCH / HOLD / NO` |
The asymmetry is deliberate: a missed good job is cheap (the person is retried next run); a wrong referral costs credibility and a referral slot. So the system abstains when unsure.
Honest limits: this is Claude's reading, not an interview result. Biases to control: verbosity (long CVs look better), prestige, order of fields, drift over time. Controls: randomised field order, a re-judge of 15% of pairs a day later (self-agreement at least 0.85 per stage), quote check (100% valid), synthetic cases with known truth, name-swap test on scrubbed CVs. Real Amex outcomes (shortlist, reject, withdrawn) replace Claude as the standard the day they exist.

## Track A: hypotheses (all on the same gold set; baseline = today's pipeline P0)
| # | Hypothesis | Why it might work | Kill rule |
|---|---|---|---|
| H0 | Fix the input: add `search_document:` / `search_query:` prefixes, pass `num_ctx` 8192, no silent truncation | model card says the prefix is required | no gain over P0 |
| H1 | Strip boilerplate (lines in over 30% of JDs: company intro, EEO, benefits; CV contact and link noise); embed a role-focused view (JD: title + responsibilities + requirements; CV: summary + last 2 roles + skills) | long identical corporate text drowns the signal | no gain |
| H2 | Rank-normalise: per-candidate z-score or CSLS (k=10) over the job pool; centre vectors (remove top 1 to 3 principal components) | removes length/years drift and hub jobs (P1, P2, P5) | hub share and length correlation do not fall |
| H3 | Hybrid: BM25 over title + skills tokens, fused with cosine by RRF (k=60) | exact skills and titles that vectors blur | loses to H2 |
| H4 | Structured fields: family, level, years, skill-lexicon overlap by code, as gates and as features | domain mismatch becomes visible (P4) | adds no precision |
| H5 | Requirement coverage (late interaction): for each JD requirement line, the best matching CV chunk; average over must-haves | asks "is it covered", not "is it similar" | no gain over H4 |
| H6 | Other embedders on the same box: mxbai-embed-large, bge-m3, snowflake-arctic-embed2 | nomic may be the weak part | no gain |
| H7 | Rerank the top 10 with a cross-encoder (bge-reranker-v2-m3, CPU time measured) | the pair is read jointly | too slow or no gain |
| H8 | Recruiter-skim features: title in the first lines, recency of the relevant role, summary relevance, red-flag counts | what a human sees first | no gain over H4 |
| H9 | Learned fusion: regularised logistic regression over H0 to H8 features, cross-validated, outputs P(advance); threshold chosen for a target wrong-referral rate | replaces the flat 0.65 | CV precision not above the best single feature |
| H10 | Typed checks (domain, level, coverage, final); Claude as the upper bound here, Laya later | an AND of independent checks lowers wrong referrals even if each is imperfect | n/a, this is the teacher |
Pipelines compared: P0 today; P1 = H0+H1; P2 = P1+H2; P3 = P2+H3+H4; P4 = P3+H7; P5 = H9 on all features; plus single-factor ablations. Full CV and full JD are also compared with the segmented views (the "do not ingest everything" question).

### Metrics and pass marks (written now, never moved)
- Primary: **wrong-referral rate** = share of referred top-1 picks whose Claude final is `NO` or `DO_NOT_REFER`, at a fixed coverage (same number of referred people as P0).
- Also: Precision@1/@3, nDCG@5, MRR, AUC of refer-vs-skip, calibration (ECE), critical errors (wrong family or level referred), correlation of score with CV length (target near 0), share of referrals to the top 2 jobs (target under 40%), run-to-run stability.
- **Adopt a pipeline only if** its wrong-referral rate is at least 40% lower than P0 at equal coverage, the 95% bootstrap interval excludes zero, and critical errors do not rise. Otherwise keep P0 and say so. Synthetic results show mechanism only; adoption needs the real sample (target 150 candidates, about 1,200 pooled pairs, split by candidate so there is no leakage).
- Teacher gates before any scoring: self-agreement at least 0.85 per stage, agreement with constructed truth on synthetic cases at least 0.90, quote validity 100%, order-flip rate at most 10%.

## Data and labels
1. **Synthetic edge cases (the small test you asked for):** about 14 JDs x 24 profiles, truth by construction. Edge cases: career switcher, keyword-stuffed CV, very long and very short CV, same keywords but different domain (Risk Analyst vs Data Analyst), over- and under-qualified, adjacent family, title inflation, Hinglish and odd text, projects-only fresher, gap year, PhD, sales-to-analytics, generic "hub" JD, JD that is mostly boilerplate, "degree OR years" JD, location mismatch.
2. **Real sample (read-only, scrubbed):** about 150 candidates and every open job in their countries (about 321). The scrubber is test-first: no email, phone, URL or name token survives.
3. **Pooled pairs:** top 5 from every pipeline per candidate, plus random negatives and hard negatives (same keywords, different domain). One pair costs about 1,500 tokens to judge; pilot 60 pairs first to measure; hard cap 4M tokens of Claude Code session; resumable batches of 20; JSONL on disk.
4. **Labels:** Claude judges each pair through all six stages (rubric above). 15% re-judged a day later. This is the gold set. The old `fit_label_sample` rows stay optional.
5. **Capture from the live flow (for Laya), later:** one shadow Code node writes a `decision_records` row per decision (meta-workflows loop): `place=prod`, params version, scrubbed state text, options, rule pick, scores, model picks and confidence, final, and later `claude_label` and `outcome` (Amex shortlist/reject, withdrawn, a "wrong referral" mark Satvik can set in the sheet). Withdrawn referrals (`withdrawn_2026-10-09_backup.json`) become seed negatives. Hashed ids, no names. Test rows (`satvik.jain.395`) and `demo` rows never train anything.

## Track B: Laya
**What Laya decides** (typed questions, opaque letters, option order shuffled in training): Q_skim (A/B/C), Q_screen (A/B/C), Q_domain (same/adjacent/different), Q_level (under/stretch/at/over), Q_manager (A/B/C), one yes/no per red flag, Q_referrer_risk (A/B/C), Q_final (REFER/STRETCH/HOLD/NO). Laya never reads the whole CV: code builds a compact state of at most about 700 tokens (job title, family, level range, top requirement lines; CV summary lines, last 2 roles, skills, years, education). This is the answer to "do not ingest the full JD and resume".
**Training data:** each judged pair gives about 8 typed items, so 1,000 pairs give about 8,000 items (above the 5k floor Laya needs). Add synthetic counterfactuals with known labels (swap family, move years by 3, delete a must-have, keyword-stuff, shuffle options). Splits by candidate AND by job; 150 real pairs and 100 synthetic edge cases held out and never trained on.
**Jev check (cap Rs 100, first call needs a go):** run the same questions on 300 pairs, report agreement with Claude per question. Jev teaches only questions where it agrees at least 0.9 on gold; every Jev-vs-Claude disagreement goes to Claude. Jev is a comparison and a bulk helper, never in the live path.
**Fine-tune:** Kaggle free 2xT4 with Laya's `laya_finetune_typed_decisions_2xT4_kaggle.ipynb` (documented); Colab single T4 as the fallback (micro-batch 1, grad-accum 32, checkpoints to Drive); the M1 8 GB Mac is not used. Update `laya_finetune_colab_plan.md` in place with the pair questions and the dataset file. Steps: baseline score of the untouched checkpoint, train 4 epochs (RLCD), fit one temperature per question type, fit abstention thresholds on the held-out set, export.
**Customise in rounds, then compare with Jev:** round 1 = Claude gold + synthetic counterfactuals; a data-size curve (1k, 2k, 5k, 8k items) shows where more data stops helping; round 2 adds hard negatives and the live captured rows; round 3 later adds real outcomes. The untouched checkpoint is scored once, only to show the lift.
**Laya pass marks (fixed now):** on the same held-out pairs (never trained on): Q_final accuracy at least 0.85; it catches at least 90% of Claude's `NO / DO_NOT_REFER` pairs at precision at least 0.80; ECE at most 0.05; it beats the best classical pipeline from Track A; **and it beats TypeSafe Jev**: Laya's agreement with Claude on Q_final and on the `NO` catch rate is higher than Jev's by at least 5 points at the same precision, or equal with at least 10x lower cost and latency. If any mark fails, Laya stays flag-only (or off) and the classical pipeline decides.
**Serve and integrate (each step needs Satvik's yes; the Oracle box is a live business):** `laya-serve` bound to 127.0.0.1 with `LAYA_API_KEY` as a new pm2 process (memory and CPU measured first, never 09:25 to 09:40 IST); one new SUB "Match Check (Laya)" called by Cosine Top 5 and the Gate with a CONFIG flag in four stages: SHADOW (logs only) -> FLAG (marks the sheet row) -> GATE (blocks only high-confidence `NO`) -> primary scorer. Each stage has a canary and a one-step rollback to the rules. Thresholds live in a versioned params store (meta-workflows).
**Loop:** a weekly scorecard from `decision_records` joined with outcomes; retrain when 1,000 new labelled records exist or live wrong-referral numbers rise; every promotion needs a "haan" until bounds and data are strong.
**Cost:** Claude labels = session tokens (cap 4M); Jev under Rs 100 and only for the comparison and bulk help; Laya in production = 0.

## Execution discipline: beads (so nothing is forgotten)
This plan is executed step by step through beads tasks (`bd` 1.0.3 is installed). Beads is the single to-do list; the claude-mem work state only holds one line pointing to the epic id.
1. **First action after approval:** in the new project run `bd init --prefix ml` (own `.beads/`, not in the Amex repo), then create ONE epic "Stop wrong referrals: deep judge + Laya" and one task per row of the table below with `bd create --parent <epic> --type task --estimate <minutes> -l trackA|trackB|gate --acceptance "<the pass mark, copied from this plan>" --deps <blockers>`. Dependencies follow the phases, so `bd ready` only ever shows the next legal step. Check with `bd graph <epic>` and `bd lint`.
2. **Every session starts with** `bd ready` and `bd show <id>` (not memory, not this chat). Claim with `bd update <id> --status in_progress`.
3. **Close a bead only with proof:** the evidence path or number in the close note (test output, execution id, results file). Gate beads (`-l gate`) cannot be closed on a "should work".
4. **New work found on the way** becomes a bead with `--deps discovered-from:<id>`, never a loose idea. A failed gate reopens or adds a fix bead; pass marks are never edited, a change needs a new decision bead and Satvik's yes.
5. **Every stop for Satvik is a bead too** (`-l needs-satvik`: Jev first call, real export, new Mongo collection, new SUB, new pm2 process, each stage promotion). `bd remember` stores the epic id, this plan's path and the project path so any session finds them.
6. At the end of each phase: `bd export` backup, one line in `tasks/changelog.md`, state in `docs/state.md`.

Bead tree (one epic, tasks in this order; ids are made at creation):
| Bead | Blocked by | Acceptance (short) |
|---|---|---|
| P0-1 init project + beads + CLAUDE.md | none | repo exists, `bd ready` works |
| P0-2 scrubber (test first) | P0-1 | no email/phone/URL/name token survives; tests green |
| P0-3 rubric v1 file | P0-1 | all 6 stages and enums as in this plan |
| P0-4 `ollama show` + truncation probe | P0-1 | prefix and num_ctx facts recorded with numbers |
| P1-1 metrics library (test first) | P0-2 | toy rankings give known answers |
| P1-2 synthetic JD x profile set with truth | P0-3 | about 14 x 24, truth table checked |
| P1-3 Claude judges synthetic set | P1-2 | agreement with truth at least 0.90 |
| P1-4 run P0 to P5 on synthetic | P1-1, P1-3 | mechanism table per hypothesis |
| P2-1 read-only scrubbed export (needs-satvik: go) | P0-2 | about 150 CVs, all open jobs, 0 leaks |
| P2-2 pilot 60 pairs: tokens per pair, self-agreement, order flip | P2-1, P0-3 | self-agreement at least 0.85, flip at most 10% |
| P2-3 show Satvik 10 samples | P2-2 | his reaction recorded |
| P3-1 pool pairs from all pipelines + negatives | P2-2 | about 1,200 pairs listed |
| P3-2 judge in batches of 20 (resumable) | P3-1 | token cap 4M respected |
| P3-3 15% re-judge | P3-2 | self-agreement still at least 0.85 |
| P4-1 bake-off H0 to H10 + bootstrap | P3-3, P1-4 | table with intervals |
| P4-2 decision memo + experiments.md E4 | P4-1 | adopt or keep P0 by the fixed rule |
| P5-1 Laya dataset (typed items, shuffled options, counterfactuals, splits) | P3-3 | at least 5k items, no leakage check passes |
| P5-2 Jev 300-pair comparison (needs-satvik: go) | P5-1 | spend under Rs 100, per-question agreement |
| P6-1 untouched Laya baseline score | P5-1 | number recorded |
| P6-2 Kaggle fine-tune round 1 + data-size curve | P6-1 | checkpoints saved, curve plotted |
| P6-3 calibrate + abstention thresholds | P6-2 | ECE reported |
| P6-4 held-out score vs classical vs Jev | P6-3, P5-2 | Laya pass marks met or "flag-only" decision |
| P7-1 laya-serve on Oracle (needs-satvik) | P6-4 | CPU latency and RAM measured |
| P7-2 `decision_records` collection + shadow Code node (needs-satvik) | P6-4 | rows arrive, 0 PII |
| P7-3 SUB "Match Check (Laya)" SHADOW (needs-satvik) | P7-1, P7-2 | live vs held-out within margin |
| P7-4 FLAG, then GATE promotions (needs-satvik each) | P7-3 | canary numbers, rollback tested |
| P8-1 round 2 and 3 fine-tune from live rows and outcomes | P7-3 | beats round 1 on the same held-out |

## Order of work (effort C1 to C5)
| Phase | What | C | Gate |
|---|---|---|---|
| 0 | New project `~/Documents/Projects/match-lab/` with `bd init` and the whole bead tree first (README, CLAUDE.md, tests, git-ignored `data/`); scrubber (test first); `ollama show` and truncation probe; rubric v1 in `docs/rubric_v1.md` | C2 | scrubber tests green |
| 1 | Synthetic edge-case set, Claude judges it; metrics code (test first with toy rankings); run P0 to P5 on it | C2 | teacher agrees with constructed truth at least 0.90; mechanism table per hypothesis |
| 2 | Read-only scrubbed export (about 150 CVs, all open jobs); pilot 60 pairs; self-agreement and order-flip tests; show Satvik 10 samples | C3 | teacher gates met, else fix the rubric and repeat |
| 3 | Scale judging to about 1,200 pooled pairs in batches; 15% re-judge | C3 | token cap respected; gates still met |
| 4 | Bake-off H0 to H10 on the gold set with bootstrap intervals | C3 | decision memo: improvement vs P0 with numbers, or "keep P0" |
| 5 | Build the Laya dataset and splits; Jev 300-pair comparison | C3 | spend under Rs 100; per-question agreement table |
| 6 | Kaggle fine-tune, calibrate, held-out score | C3 | Laya pass marks |
| 7 | Serve, SHADOW capture, then FLAG, then GATE | C4 | Satvik's yes at each step; live numbers match held-out within a margin |
Phases 0 to 4 change nothing live and cost only session tokens. Phases 5 to 7 each stop for approval.

## Where things live
- Experiment code, rubric, data (git-ignored), reports: `~/Documents/Projects/match-lab/` (standalone tool; the Amex repo is being reorganised and has its own rules).
- Durable results go to the Amex repo: rows E4 (algorithms) and E5 (teacher + Laya) in `docs/research/experiments.md`; `docs/research/match_algorithms_2026-10-13.md` with the tier/confidence table; `laya_finetune_colab_plan.md` updated in place; `bd remember` pointers. No competing plan files.
- Secrets (OpenRouter key) only in `~/Desktop/Secrets/`. No CV or label file in any commit.

## Rules this plan keeps
Every step is a bead and every session starts from `bd ready`; no Claude API (Claude Code session only); no subagents (labelling runs in the main thread, resumable); TDD with pass marks fixed above; personal data scrubbed before any model or log; OpenRouter spend capped and asked before the first call; no change to a live workflow, new workflow, new pm2 process, env change or new Mongo collection without Satvik's yes; every claim carries a tier and a 0 to 1 confidence; a hypothesis is not a result until its test ran.

## Verification
Unit tests for scrubber, metrics, CSLS, RRF, label schema and quote checker; teacher-quality gates printed before any scoring; bake-off table with bootstrap intervals and the improvement over P0; held-out Laya report with confusion tables and calibration; for any n8n step: execution ids, item counts, real rows, shadow-vs-held-out comparison.
