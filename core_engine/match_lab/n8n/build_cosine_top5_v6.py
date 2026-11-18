"""Builds n8n/cosine_top5_v6.js from the live v5 Cosine Top 5 code (backups/2026-10-14/JmV3niatmJiOgbmY_pre.json). Every replacement is asserted, so a changed live node stops the build."""
import json, os
D = os.path.join(os.path.dirname(__file__), '..')
w = json.load(open(os.path.join(D, 'backups', '2026-10-14', 'JmV3niatmJiOgbmY_pre.json'))); w = w.get('data', w)
code = [n for n in w['nodes'] if n['name'] == 'Cosine Top 5'][0]['parameters']['jsCode']
open(os.path.join(D, 'n8n', 'cosine_top5_v5_live.js'), 'w').write(code)

def rep(s, old, new):
    assert s.count(old) == 1, ('not found once', old[:60]); return s.replace(old, new)

code = rep(code, "// Cosine Top 5 (SUB — Candidate to Job Top 5)  v5\n", "// Cosine Top 5 (SUB — Candidate to Job Top 5)  v6 (14 Oct 2026: + eligibility rules, SHADOW first; was v5)\n")
code = rep(code, "    { max: 999, min: 0.75 },", "    { max: 999, min: 0.70 },   // 14 Oct 2026 (Satvik): was 0.75. Live replay: 7% of candidates got a job at 0.75 and about 38% at 0.70; picks at 0.70 and up were 75% STRETCH or better (match-lab docs/p_live_replay.md)")
code = rep(code, "  SOFT_CAP: false,        // switch on in Phase D (needs the \"Get Job Referral Counts (7d)\" node)", "  SOFT_CAP: false,        // Satvik 14 Oct: stays OFF for now, no value set. Later: set true and add the \"Get Job Referral Counts (7d)\" node")
code = rep(code, "  TOP_N: 5,\n};", r"""  TOP_N: 5,
  // ---- v6 (14 Oct 2026): eligibility rules from the V-4 and fresh tests (match-lab docs/p_v5_fresh_test.md).
  //   RULES: each rule is 'off' | 'shadow' | 'on'. shadow = the live result is unchanged; what the rules WOULD give is added as `shadow_v6`
  //   and kept in this workflow's static data (last SHADOW_LOG_MAX picks). on = the rule filters the live list.
  //   campus   (U1)  campus-type roles are not offered to people with CAMPUS_BLOCK_YEARS or more years (V-4: 13 of 15 such picks were NO).
  //   masters  (U1b) "Campus Graduate ..." programs need a master-type degree word on the CV (none of 83 such picks for other CVs was a REFER).
  //   language (U1c) a job that asks for a language other than English (Japanese, JLPT, ...) is not offered unless the CV names that language
  //                  (14 Oct replay on live pool: 7 of 88 top-1 picks were the Japanese-language job, all 7 NO).
  RULES: { campus: 'shadow', masters: 'shadow', language: 'on' },
  CAMPUS_RE: /campus|apprentice|internship|intern\b|graduate program|early career/i,
  CAMPUS_BLOCK_YEARS: 2,
  CAMPUS_GRAD_RE: /campus graduate\b/i,
  MASTERS_RE: /m\.?\s?tech|m\.e\.|msc|m\.sc|master|\bmba\b|\bmca\b|pgdm|pgdba|post[- ]?graduate|m\.?com\b|\bms in\b/i,
  LANG_NAMES: 'japanese|jlpt|mandarin|chinese|korean|german|french|spanish|portuguese|italian|arabic|dutch|thai|vietnamese|bahasa|indonesian|russian|turkish',
  SHADOW_LOG_MAX: 500,
};""")
code = rep(code, """scored = scored
  .filter(prefOk)
  .filter(r => r.score >= r.min_score_applied)
  .sort((a, b) => (a.tier - b.tier) || (b.rank_score - a.rank_score));

const top = scored.slice(0, CONFIG.TOP_N);
""", r"""const finalize = (arr, floor = true) => arr
  .filter(prefOk)
  .filter(r => !floor || r.score >= r.min_score_applied)
  .sort((a, b) => (a.tier - b.tier) || (b.rank_score - a.rank_score));
const scoredBase = scored;
scored = finalize(scoredBase);

// ---- v6: eligibility rules (see CONFIG). In 'shadow' the live list is untouched; any error here is caught and never changes the live result. ----
const liveScored = scored;
let shadowV6;
if (Object.values(CONFIG.RULES).some(m => m !== 'off')) {
  try {
    const cvText = String(newest.raw_cv || '');
    const mastersOnCv = CONFIG.MASTERS_RE.test(cvText);
    const langAsk = new RegExp('(language[s]?\\s*(requirements?)?\\s*[:\\-]?[^.\\n]{0,80}\\b(' + CONFIG.LANG_NAMES + ')\\b)|\\bjlpt\\b|((fluen\\w*|proficien\\w*|native|advanced)\\s+(level\\s+of\\s+)?(in\\s+)?(' + CONFIG.LANG_NAMES + ')\\b)', 'i');
    const langWord = new RegExp('\\b(' + CONFIG.LANG_NAMES + ')\\b', 'ig');
    const blockers = {
      campus: (r) => CONFIG.CAMPUS_RE.test(String(r.title || '')) && candYears >= CONFIG.CAMPUS_BLOCK_YEARS,
      masters: (r) => CONFIG.CAMPUS_GRAD_RE.test(String(r.title || '')) && !mastersOnCv,
      language: (r) => {
        const t = String(r.title || '') + ' ' + String(r.description || '') + ' ' + String(r.qualifications || '');
        if (!langAsk.test(t)) return false;
        const asked = new Set((t.match(langWord) || []).map(x => x.toLowerCase()).map(x => x === 'jlpt' ? 'japanese' : x));
        return [...asked].some(l => !new RegExp('\\b' + (l === 'japanese' ? '(japanese|jlpt)' : l) + '\\b', 'i').test(cvText));
      },
    };
    const okWith = (modes) => (r) => !Object.keys(blockers).some(k => modes.includes(CONFIG.RULES[k]) && blockers[k](r));
    const liveOk = okWith(['on']), shadowOk = okWith(['on', 'shadow']);
    const why = (r) => !r ? '' : (Object.keys(blockers).find(k => CONFIG.RULES[k] !== 'off' && blockers[k](r)) || '');
    if (Object.values(CONFIG.RULES).includes('on')) scored = finalize(scoredBase.filter(liveOk));
    const withRules = finalize(scoredBase.filter(shadowOk));
    const liveNoFloor = finalize(scoredBase.filter(liveOk), false), rulesNoFloor = finalize(scoredBase.filter(shadowOk), false);   // what the picks would be if the cosine floor did not exist (the floor skips most people)
    const brief = (r) => r ? { id: String(r.job_id), title: String(r.title || '').slice(0, 70), score: +Number(r.score).toFixed(4) } : null;
    shadowV6 = {
      rules: CONFIG.RULES,
      live_top1: brief(scored[0]),
      new_top1: brief(withRules[0]),
      changed: String((scored[0] || {}).job_id || '') !== String((withRules[0] || {}).job_id || ''),
      live_n: scored.length,
      new_n: withRules.length,
      why: why(scored[0]),
      blocked_in_live_top5: scored.slice(0, CONFIG.TOP_N).filter(r => !shadowOk(r)).length,
      nf_live_top1: brief(liveNoFloor[0]),
      nf_new_top1: brief(rulesNoFloor[0]),
      nf_changed: String((liveNoFloor[0] || {}).job_id || '') !== String((rulesNoFloor[0] || {}).job_id || ''),
      nf_why: why(liveNoFloor[0]),
    };
  } catch (e) { scored = liveScored; shadowV6 = { rules: CONFIG.RULES, error: String((e && e.message) || e).slice(0, 120) }; }
}

const top = scored.slice(0, CONFIG.TOP_N);
""")
code = rep(code, "    profiles_scored: candDocs.length,\n    skip_reason,\n  }\n}];", "    profiles_scored: candDocs.length,\n    shadow_v6: shadowV6,\n    skip_reason,\n  }\n}];")
code = rep(code, "return [{\n  json: {\n    candidate: {\n      ...candidate,\n      years_experience: candYears,\n      job_countries: rawCountries || 'India',\n      job_preference: pref,", """// ---- v6: keep a small record of what the rules would do (no names: the id is a short hash of the email) ----
if (shadowV6 && !shadowV6.error) {
  try {
    let h = 5381; const eid = String(candidate.email_id || newest.email_id || '');
    for (let i = 0; i < eid.length; i++) h = ((h << 5) + h + eid.charCodeAt(i)) >>> 0;
    const sd = $getWorkflowStaticData('global');
    const log = sd.shadow_v6 || (sd.shadow_v6 = []);
    log.push({ t: new Date().toISOString(), k: h.toString(16), y: candYears, p: pref, live: shadowV6.live_top1, nw: shadowV6.new_top1, ch: shadowV6.changed, why: shadowV6.why, nfl: shadowV6.nf_live_top1, nfn: shadowV6.nf_new_top1, nfc: shadowV6.nf_changed, nfw: shadowV6.nf_why, ln: shadowV6.live_n, nn: shadowV6.new_n, b5: shadowV6.blocked_in_live_top5, skip: skip_reason || '' });
    if (log.length > CONFIG.SHADOW_LOG_MAX) log.splice(0, log.length - CONFIG.SHADOW_LOG_MAX);
  } catch (e) { /* static data not available: the shadow_v6 field on the item is still there */ }
}

return [{
  json: {
    candidate: {
      ...candidate,
      years_experience: candYears,
      job_countries: rawCountries || 'India',
      job_preference: pref,""")
open(os.path.join(D, 'n8n', 'cosine_top5_v6.js'), 'w').write(code); print('built', len(code), 'chars')
