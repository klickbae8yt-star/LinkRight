// Replay test for the Cosine Top 5 Code node on real candidate and job documents (data/replay, git-ignored).
// v5 = live code before 14 Oct. v6 default = floor 0.70, language rule on, campus and masters rules in shadow, soft cap off.
const fs = require('fs'), path = require('path'), assert = require('assert');
const D = path.join(__dirname, '..');
const data = JSON.parse(fs.readFileSync(path.join(D, 'data/replay/replay_2026-10-14.json'), 'utf8'));
const v5 = fs.readFileSync(path.join(D, 'n8n/cosine_top5_v5_live.js'), 'utf8');
const v6 = fs.readFileSync(path.join(D, 'n8n/cosine_top5_v6.js'), 'utf8');
const rep = (s, a, b) => { assert.ok(s.includes(a), 'missing in code: ' + a); return s.replace(a, b); };
const FLOOR = (code, f) => code.replace(/\{ max: 999, min: 0\.\d+ \}/, `{ max: 999, min: ${f} }`);
const RULES = (code, c, m, l) => rep(code, "RULES: { campus: 'shadow', masters: 'shadow', language: 'on' }", `RULES: { campus: '${c}', masters: '${m}', language: '${l}' }`);

function run(code, cand, sd = {}) {
  const nodes = {
    'When Executed by Another Workflow': [{ candidate: { email_id: cand.email_id, years_experience: cand.years_experience, job_countries: cand.job_countries } }],
    'Get Candidate Embedding': [cand], 'Get Open Job Embeddings': data.jobs, "Get Candidate's Referred Jobs": data.ref[cand.email_id] || [],
  };
  const $ = (name) => { if (!nodes[name]) throw new Error('no node ' + name); return { first: () => ({ json: nodes[name][0] }), all: () => nodes[name].map(json => ({ json })) }; };
  return new Function('$', '$getWorkflowStaticData', code)($, () => sd)[0].json;
}
const strip = (o) => { const c = JSON.parse(JSON.stringify(o)); delete c.shadow_v6; return c; };
const ids = (o) => (o.top_jobs || []).map(j => String(j.job_id));
const jp = (j) => /jlpt|language requirements?\s*:[^.]*japanese/i.test(j.title + ' ' + j.description + ' ' + j.qualifications);
const hasJp = (c) => /japanese|jlpt/i.test(c.raw_cv || '');

const A_v5 = (c) => run(v5, c);
const B_v5_70 = (c) => run(FLOOR(v5, 0.70), c);
const V6_regress = (c, sd) => run(RULES(FLOOR(v6, 0.75), 'shadow', 'shadow', 'shadow'), c, sd);
const V6_off70 = (c) => run(RULES(v6, 'off', 'off', 'off'), c);
const V6_default = (c, sd) => run(v6, c, sd);

let n = 0, yield5 = 0, yieldDef = 0, langChanged = 0, cleanSame = 0; const sd = {};
for (const c of data.cands) {
  n++;
  const a = A_v5(c), b = B_v5_70(c), r = V6_regress(c, sd), o = V6_off70(c), d = V6_default(c, {});
  assert.deepStrictEqual(strip(r), strip(a), 'REGRESSION: v6 (floor 0.75, rules shadow) differs from live v5');   // A: shadow has no effect
  assert.deepStrictEqual(strip(o), strip(b), 'v6 with rules off differs from v5 at floor 0.70');                   // B: only the floor changed
  assert.strictEqual(o.shadow_v6, undefined);
  for (const j of d.top_jobs || []) if (!hasJp(c)) assert.ok(!jp(j), 'language job kept for a CV without Japanese: ' + j.title);   // C: language rule works
  if (!(b.top_jobs || []).some(j => jp(j) && !hasJp(c))) { assert.deepStrictEqual(strip(d), strip(b), 'default differs from floor-0.70 although no language job was involved'); cleanSame++; }
  else langChanged++;                                                                                              // D: otherwise only the language job moves
  if (a.top_jobs && a.top_jobs.length) yield5++; if (d.top_jobs && d.top_jobs.length) yieldDef++;
}
// E: a broken shadow rule must not change the live result
const broken = run(v6.replace("CAMPUS_RE: /campus|apprentice|internship|intern\\b|graduate program|early career/i", 'CAMPUS_RE: null'), data.cands[0]);
assert.ok(broken.shadow_v6.error, 'broken rule is reported'); assert.deepStrictEqual(strip(broken), strip(V6_default(data.cands[0], {})));
// F: bounded log without names
assert.ok(sd.shadow_v6.length === n && JSON.stringify(sd.shadow_v6).indexOf('@') < 0);
console.log(`PASS ${n} candidates | get a job: live v5 ${yield5} -> v6 default ${yieldDef} | language rule moved the pick for ${langChanged}, identical to floor-0.70 for ${cleanSame}`);
