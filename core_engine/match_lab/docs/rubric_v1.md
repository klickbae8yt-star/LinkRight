# Rubric v1: judge a CV for a job the way a recruiter and then a hiring manager would

Status: v1.1, 13 Oct 2026 (v1.1 only added: REFER and SAFE need domain `same`; made before any pair was scored). Judge: Claude in a Claude Code session (never the API). Labels made with this rubric are tier S: "Claude's reading, not human-checked, not an interview result".
Goal: say whether the CV would be moved forward, and whether a referrer could safely put their name on it. A missed good job is cheap (the person is retried next run). A wrong referral is expensive. When unsure, hold.

## 1. What the judge sees
One pair at a time, scrubbed (no name, email, phone, links, no date of birth, gender, marital status, nationality, religion):
- JOB: title, location, years range `[lo, hi]`, the JD text.
- CV: the scrubbed CV text.
- KNOCKOUTS (made by code, copied in): country ok, years window ok, not already referred, CV readable.
The order of the two blocks flips by pair number (odd: CV first, even: JOB first), so we can test that the order does not change the answer.

## 2. Fairness rules (hard)
Never use: name, gender, age, photo, religion, caste, marital status, nationality, family, health, or which college sounds famous. A college counts only when the JD asks for a degree or field (then the field and level count, not the brand).
If a judgement would change when the name is swapped, it is wrong. Judge only skills, work done, level, domain, evidence, stability.

## 3. Evidence rule (hard)
Every claim that matters carries a quote copied letter for letter from the CV or the JD (at least 6 characters). Code checks that each quote exists in the source; a pair with a missing quote is rejected and judged again. No quote means the status is `UNKNOWN`, never a guess.

## 4. Stages (answer in this order; later stages may use earlier ones, never the other way)

### Stage 0. Knock-outs (code, copied in)
`PASS` or the reason (`country`, `years_window`, `already_referred`, `unreadable`). Any failure: final is `NO` with that reason, and stages 1 to 5 are skipped.

### Stage 1. The 7-second skim (recruiter; look only at the first ~15 lines)
Ask: in 7 seconds, does this look like a person for this job?
Signals (fill each):
- `title_family`: `match` (headline or last title names this job's family) / `adjacent` / `no`.
- `summary`: `specific` (names tools, domain, scale or results) / `generic` (buzzwords only) / `missing`.
- `recent_relevant_role`: `yes` (a relevant role within the last 24 months) / `older` / `no`.
- `readability`: `clear` (sections, short bullets, dates visible) / `messy` (wall of text, missing dates).
Verdict `skim`: `PASS_SKIM` (match or strong adjacent, and a specific summary or a recent relevant role), `MAYBE` (one of the two is weak), `FAIL_SKIM` (no family match and nothing relevant in the first lines).
Also write `feeling`: one line, at most 20 words, what a busy recruiter would think.

### Stage 2. The recruiter screen (1 minute; requirements checklist)
Take the JD's top 5 to 8 must-haves (skills, tools, domain, degree, years, certificates). For each give `status`:
- `MET`: the CV shows it, with a quote.
- `PARTIAL`: close but not the same (a related tool, fewer years, a course not a job).
- `MISSING`: a CV for this role would normally show it and there is no trace.
- `UNKNOWN`: CVs rarely state it (notice period, work permit), or the JD is unclear.
Freshers: projects, internships and thesis work count as evidence.
`coverage` = (MET + 0.5 x PARTIAL) / number of must-haves. `knockouts` = number of MISSING must-haves the JD marks as required.
Verdict `screen`: `ADVANCE` (coverage at least 0.7 and no required knock-out), `HOLD` (coverage 0.4 to 0.7 or one required knock-out that looks fixable), `REJECT` (coverage under 0.4 or two or more required knock-outs).

### Stage 3. The hiring-manager read (1 to 2 minutes; does this person connect to my team's work?)
Read the last two roles first, then the top of the skills. Give:
- `domain`: `same` / `adjacent` (skills transfer with a short ramp) / `different`.
- `level`: `under` (job asks 2 or more years above the person, or scope clearly bigger) / `stretch` (about one year or one step above) / `at` / `over` (person is 2 or more years above the job's top, or led much bigger scope).
- `ownership`: `led` / `contributed` / `unclear`.
- `impact`: `quantified` (numbers, outcomes) / `stated` (outcome without numbers) / `none`.
- `depth`: `described` (what was built or done and how) / `listed` (names only) / `none`.
- `stability`: `steady` / `mixed` / `unstable` (more than 3 employers in the last 3 years with stays under 12 months, or an unexplained gap over 6 months).
- `connects`: one line, at most 25 words: what in this CV would make the manager say "this person has done my problem"; if nothing, say so.
Verdict `manager`: `INTERVIEW` (domain same or strong adjacent, level at or stretch, depth described, and a clear "has done my problem"), `MAYBE` (one real doubt), `NO` (domain different, or level under or over, or nothing connects).

### Stage 4. Red flags (both readers). Each is true or false, with a quote when true
`keyword_stuffing` (long skill lists with no use shown), `jd_copied` (bullets read like the JD), `inflated_title` (title far above the described work), `vague_bullets` (no object, no result), `unexplained_gap`, `frequent_switches`, `claims_without_evidence`, `over_qualified` (flight risk), `irrelevant_history` (long history with nothing for this job).
Two or more true flags cap stage 5 at `BORDERLINE`.

### Stage 5. The referrer's risk (our own lens)
Ask: if a person staked their name on this referral, how likely is an embarrassing outcome (a clear mismatch the recruiter sees in 10 seconds)?
`SAFE` (skim PASS_SKIM, screen ADVANCE, manager INTERVIEW or strong MAYBE, domain `same`, no cap) / `BORDERLINE` (anything between) / `DO_NOT_REFER` (skim FAIL_SKIM, or screen REJECT, or manager NO, or domain different, or level `under`).
Borderline always means hold.

### Stage 6. Final decision
`decision`: `REFER` / `STRETCH` (level `stretch` or partial coverage, but domain same or strong adjacent, manager at least MAYBE, referrer risk BORDERLINE at worst; labelled so a human can choose) / `HOLD` / `NO`.
`confidence`: 0 to 1, how sure the judge is about this final decision.
`reasons`: exactly 3, each with a short quote id. `risks`: exactly 3 (may say "none seen").

## 5. Consistency rules (code rejects a pair that breaks one)
1. `REFER` needs: knock-outs PASS, skim not FAIL_SKIM, screen ADVANCE, manager INTERVIEW, referrer SAFE, domain `same`, level `at` or `stretch`. (v1.1, 13 Oct, before any scoring: an adjacent domain is a STRETCH at best.)
2. `STRETCH` needs: knock-outs PASS, screen not REJECT, manager not NO, referrer not DO_NOT_REFER, domain not `different`.
3. `NO` is required when: a knock-out failed, referrer is DO_NOT_REFER, or manager is NO.
4. Every enum value must be one of the lists above. Every quote must exist in the source. `confidence` is between 0 and 1. Exactly 3 reasons and 3 risks.
5. Order and name must not matter: the same pair judged in the other block order must give the same `final.decision` at least 90% of the time (tested, not assumed).

## 6. Output (one JSON object per pair)
```
{"pair_id": "...", "rubric": "v1", "order": "cv_first|jd_first",
 "s0": {"pass": true, "reasons": []},
 "s1": {"title_family": "...", "summary": "...", "recent_relevant_role": "...", "readability": "...", "verdict": "...", "feeling": "...", "quotes": ["..."]},
 "s2": {"musts": [{"req": "...", "status": "...", "quote": "..."}], "coverage": 0.0, "knockouts": 0, "verdict": "..."},
 "s3": {"domain": "...", "level": "...", "ownership": "...", "impact": "...", "depth": "...", "stability": "...", "connects": "...", "verdict": "...", "quotes": ["..."]},
 "s4": {"flags": {"keyword_stuffing": false, "jd_copied": false, "inflated_title": false, "vague_bullets": false, "unexplained_gap": false, "frequent_switches": false, "claims_without_evidence": false, "over_qualified": false, "irrelevant_history": false}, "flag_quotes": {}},
 "s5": {"verdict": "...", "why": "..."},
 "final": {"decision": "...", "confidence": 0.0, "reasons": ["...", "...", "..."], "risks": ["...", "...", "..."]}}
```

## 7. The typed questions Laya will learn (opaque letters, order shuffled in training)
Each judged pair gives about 8 items from the same fields: `skim` (A/B/C), `screen` (A/B/C), `domain` (A/B/C), `level` (A/B/C/D), `manager` (A/B/C), `risk` (A/B/C), `final` (A/B/C/D), plus one yes/no per red flag that is true in at least 5% of pairs. The state Laya reads is a compact view built by code (at most about 700 tokens): job title, family, level range, top requirement lines; CV summary lines, last two roles, skills, years, education.

## 8. Known limits (written so nobody forgets)
- This is a reading, not an interview result. Real Amex outcomes (shortlist, reject, withdrawn) replace it as the standard when they exist.
- Judge biases to watch: longer CVs look better (verbosity), famous employers look better (prestige), the first block gets more weight (order). Tests: order flip, re-judge a day later, synthetic pairs with known truth, name swap on scrubbed CVs.
- A CV cannot show everything. `UNKNOWN` is allowed and is never counted as `MISSING`.
