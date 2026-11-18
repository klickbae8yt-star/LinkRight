// Cosine Top 5 (SUB — Candidate to Job Top 5)  v5
// Builds on v4 (country filter → experience pre-filter → cosine). New in v5, each behind a switch in CONFIG:
//   B1  band-wise MIN_SCORE by candidate years (replaces the flat MIN_SCORE)
//   B2  pool guard: too few eligible jobs → skip_reason 'thin_pool'
//   C4  multi-profile: every active resume of the person is scored; best job overall wins; profile_key is passed down
//   D1  job-family check: distant family needs band min + FAMILY_EXTRA, else dropped
//   D2  match strength by gap: #1 must be clearly ahead of #2..#5, else 'weak_match'
//   D3  per-job soft cap: jobs with >= SOFT_CAP_N referrals in the last 7 days get a ranking penalty
//   B6  stretch + family-first (Satvik 6 Oct): jobs up to STRETCH_YEARS above the candidate are allowed (stretch),
//       over-qualified guard OVER_GAP; candidate family = family of the top-3 jobs by cosine over ALL jobs in their
//       countries; top 5 ordered by tier (same@level, same@stretch, adjacent@level, adjacent@stretch, rest), then score.
//       Pool size is never a reason to skip (B2 dropped).
//   +   candidate.raw_cv (first 1200 chars of the matched resume) is passed down so Build Message Draft can write a real hook
// Output shape is unchanged (candidate, top_jobs, skip_reason ...) plus new fields; downstream nodes keep working.
//   9 Oct: candidate.job_preference (form answer: same_level | same_stretch | any) is a hard filter on family + stretch;
//       nothing left → skip_reason 'no_job_for_preference'. No answer = same_stretch (Satvik, 10 Oct; was same_level).
//   10 Oct (Satvik): years window on a RANGE [lo, hi] (required_years .. required_years_max, written by Job Sync / the backfill):
//       over-qualified guard hi >= n - DOWN (a job whose range ends more than 1 year below the candidate is not shown);
//       same_level: lo <= n · same_stretch and any: lo <= n + STRETCH_UP. Examples n = 3: [0,4] yes · [0,1] no · [1,2] yes · [4,6] stretch only.
//       Fresher with 0 years: level lo 0; stretch lo 0 or 1 (so a job asking "1-2 years" is open to a fresher). Never lo 2+.
// Blocking rule: REFERRED / ALREADY_REFERRED / QUEUED pairs are excluded (QUEUED added 6 Oct).

const CONFIG = {
  // ---- B1: minimum cosine by experience band (candidate years <= max → min). Recalibrate from the per-batch scorecard.
  // Satvik 6 Oct: bands off for now — every band uses the 0.65 floor he chose. Revisit with fit labels / Amex outcomes.
  // Planned bands (batch-2 medians): 0–1 yr 0.66 · 2–3 yr 0.71 · 4–6 yr 0.74 · 7+ 0.75.
  BANDS: [
    { max: 999, min: 0.75 },
  ],
  // ---- B2: pool guard
  POOL_GUARD: false,     // B2 dropped by Satvik 6 Oct: never skip because the pool is small
  MIN_POOL: 5,            // fewer eligible jobs than this → thin_pool skip
  // ---- B6: stretch + family-first
  STRETCH_UP: 1,          // same_stretch / any: a job's lo may be this many years above the candidate (labelled stretch). same_level: 0.
  DOWN: 1,                // over-qualified guard: job hi must be >= candidate years - DOWN (10 Oct, Satvik: range [n-1, n+1], was n-2 .. n+1)
  FAMILY_FIRST: true,
  FAMILY_TOP_K: 3,        // candidate family = majority family of their top-K jobs (all jobs in their countries)
  // ---- D1: job-family check
  FAMILY_CHECK: false,    // switch on in Phase D
  FAMILY_EXTRA: 0.05,     // distant family must beat band min + this
  // ---- D2: gap-based match strength
  GAP_CHECK: false,       // switch on in Phase D after back-test
  GAP_MIN: 0.02,          // score#1 − median(#2..#5) must be >= this ...
  STRONG_EXTRA: 0.03,     // ... or score#1 >= band min + this
  // ---- D3: per-job soft cap
  SOFT_CAP: false,        // switch on in Phase D (needs the "Get Job Referral Counts (7d)" node)
  SOFT_CAP_N: 8,
  SOFT_CAP_PENALTY: 0.02,
  // ---- misc
  ASSUMED_PENALTY: 0.01,  // 9 Oct: years only assumed (title floor / no number) → rank just below a verified job of the same tier
  CV_SNIPPET_CHARS: 1200, // raw_cv passed down for the message hook
  TOP_N: 5,
};

// ============ job families (D1) — order matters: first match wins ============
const FAMILIES = [
  { name: 'data',         re: /\b(data scien|data analy|analytics|machine learning|\bml\b|\bai\b|artificial intelligence|business intelligence|\bbi\b|statistic|decision scien|data engineer|nlp|deep learning)/i },
  { name: 'engineer',     re: /\b(software|developer|engineer|sde|full[- ]?stack|backend|back[- ]end|frontend|front[- ]end|devops|sre|site reliability|qa|quality engineer|test engineer|programmer|architect|cloud|platform)/i },
  { name: 'finance_risk', re: /\b(financ|risk|credit|fraud|underwrit|audit|accountant|accounting|treasury|compliance|aml|kyc|actuar|investment|banking)/i },
  { name: 'product',      re: /\b(product manager|product owner|program manager|project manager|business analyst|scrum|agile coach|strategy)/i },
  { name: 'ops',          re: /\b(operations|customer|support|service|process|collections|servicing|back office|contact cent|call cent|onboarding|administrat)/i },
  { name: 'manager',      re: /\b(manager|director|head of|vice president|\bvp\b|lead\b|chief)/i },
];
const ADJACENT = {
  engineer: ['data', 'product'],
  data: ['engineer', 'finance_risk', 'product'],
  finance_risk: ['data', 'ops'],
  product: ['engineer', 'data', 'ops'],
  ops: ['finance_risk', 'product'],
  manager: ['engineer', 'data', 'finance_risk', 'product', 'ops'],
};
function familyOf(text) {
  const t = String(text || '');
  for (const f of FAMILIES) if (f.re.test(t)) return f.name;
  return 'unknown';
}
function familyRelation(candFam, jobFam) {
  if (candFam === 'unknown' || jobFam === 'unknown') return 'unknown';
  if (candFam === jobFam) return 'same';
  if ((ADJACENT[candFam] || []).includes(jobFam)) return 'adjacent';
  return 'distant';
}
// candidate family: the most recent title is usually in the first part of the CV (headline / summary / first job)
function candidateFamily(rawCv) {
  const head = String(rawCv || '').slice(0, 1500);
  return familyOf(head);
}

// ============ inputs ============
const candidate = $('When Executed by Another Workflow').first().json.candidate || {};

// all documents the Mongo node returned (v5: all ACTIVE resumes of this email; before Phase C it is still 1 document)
const candDocs = $('Get Candidate Embedding').all().map(x => x.json)
  .filter(d => d && Array.isArray(d.embedding) && d.active !== false);
if (!candDocs.length) {
  return [{ json: { candidate, top_jobs: [], skip_reason: 'candidate_not_embedded' } }];
}
// newest document first (person facts come from it)
candDocs.sort((a, b) => String(b.embedded_at || '').localeCompare(String(a.embedded_at || '')));
// Satvik, 6 Oct: one email = one CV. Only the newest resume is scored; older ones stay in Mongo as history.
// (A person who really wants two profiles uses two email addresses.) The C2/C4 multi-profile path is off.
candDocs.splice(1);
const newest = candDocs[0];

// ---- Country preference ----
const rawCountries = String(candidate.job_countries || newest.job_countries || '').trim();
const wantedCountries = rawCountries
  ? rawCountries.split('|').map(s => s.trim().toLowerCase()).filter(Boolean)
  : ['india'];
const anyCountry = wantedCountries.includes('any');

const jobs = $('Get Open Job Embeddings').all().map(x => x.json);

// QUEUED blocks too (6 Oct): a pair waiting for the AHK must not be matched again (46 same-job re-matches in batch 3)
const BLOCKING = new Set(['REFERRED', 'ALREADY_REFERRED', 'QUEUED']);
const referredJobs = new Set(
  $("Get Candidate's Referred Jobs").all()
    .map(x => x.json)
    .filter(r => BLOCKING.has(r.status))
    .map(r => r.job_id)
    .filter(Boolean)
    .map(String)
);

// D3: referrals per job in the last 7 days (node is optional; missing node = no cap)
const jobCounts = {};
if (CONFIG.SOFT_CAP) {
  try {
    for (const x of $('Get Job Referral Counts (7d)').all()) {
      const j = x.json || {};
      if (j._id !== undefined && j._id !== null) jobCounts[String(j._id)] = Number(j.count) || 0;
    }
  } catch (e) { /* node not present yet */ }
}

// ---- candidate years (person fact: form value from the queue, else newest document) ----
const candYears = Number(candidate.years_experience ?? newest.years_experience ?? 0) || 0;
// ---- job preference (form answer; blank = same_stretch since 10 Oct) ----
const pref = String(candidate.job_preference || newest.job_preference || '').trim().toLowerCase() || 'same_stretch';
const band = CONFIG.BANDS.find(b => candYears <= b.max) || CONFIG.BANDS[CONFIG.BANDS.length - 1];
const MIN_SCORE = band.min;

// ---- country + experience pre-filter (same as v4) ----
const countryJobs = jobs.filter(j => {
  if (anyCountry) return true;
  const c = String(j.country || '').trim().toLowerCase();
  return c && c !== 'unknown' && wantedCountries.includes(c);
});
const reqYearsOf = (j) => (j.required_years_manual !== undefined && j.required_years_manual !== null && j.required_years_manual !== '')
  ? Number(j.required_years_manual)
  : (j.required_years === undefined || j.required_years === null || j.required_years === '' ? null : Number(j.required_years));
// upper end of the job's years range; a single figure (or an old doc without required_years_max) is [lo, lo]
const reqHiOf = (j) => {
  const lo = reqYearsOf(j); if (lo === null || Number.isNaN(lo)) return null;
  const manual = j.required_years_manual !== undefined && j.required_years_manual !== null && j.required_years_manual !== '';
  const mx = manual ? j.required_years_max_manual : j.required_years_max;
  return (mx !== undefined && mx !== null && mx !== '' && Number(mx) >= lo) ? Number(mx) : lo;
};
const maxLo = candYears + (pref === 'same_level' ? 0 : CONFIG.STRETCH_UP);
const eligibleJobs = countryJobs
  .filter(j => { const lo = reqYearsOf(j), hi = reqHiOf(j); return lo !== null && !Number.isNaN(lo) && hi >= candYears - CONFIG.DOWN && lo <= maxLo; })
  .filter(j => Array.isArray(j.embedding) && j.job_id && !referredJobs.has(String(j.job_id)));

// ---- B2: pool guard ----
if (CONFIG.POOL_GUARD && eligibleJobs.length < CONFIG.MIN_POOL) {
  return [{ json: {
    candidate: { ...candidate, years_experience: candYears, job_countries: rawCountries || 'India' },
    top_jobs: [],
    wanted_countries: wantedCountries,
    jobs_pool: jobs.length,
    jobs_in_countries: countryJobs.length,
    candidate_years: candYears,
    jobs_within_experience: eligibleJobs.length,
    excluded_count: referredJobs.size,
    band_min_score: MIN_SCORE,
    skip_reason: countryJobs.length === 0 ? 'no_jobs_in_chosen_countries' : (eligibleJobs.length === 0 ? 'no_jobs_within_experience' : 'thin_pool'),
  } }];
}

// ---- helpers ----
const sectionOf = (et, label, next) => {
  const i = et.indexOf(label);
  if (i < 0) return '';
  const start = i + label.length;
  const end = next ? et.indexOf(next, start) : -1;
  return et.slice(start, end > start ? end : undefined).trim();
};
const normOf = (v) => Math.sqrt(v.reduce((s, x) => s + x * x, 0)) || 1;

// ---- score every eligible job against every active profile (C4) ----
const best = new Map(); // job_id → best scored row across profiles
for (const doc of candDocs) {
  const v = doc.embedding;
  const normV = normOf(v);
  const profileKey = doc.candidate_key || (doc.email_id + '||' + (doc.resume_link || ''));
  for (const j of eligibleJobs) {
    const w = j.embedding;
    let dot = 0;
    const n = Math.min(v.length, w.length);
    for (let i = 0; i < n; i++) dot += v[i] * w[i];
    const score = dot / (normV * normOf(w));
    const prev = best.get(String(j.job_id));
    if (prev && prev.score >= score) continue;
    const et = String(j.embedding_text || '');
    best.set(String(j.job_id), {
      job_id: j.job_id,
      title: j.title,
      location: j.location,
      country: j.country,
      description: sectionOf(et, 'Description:', '\n\nResponsibilities:'),
      qualifications: sectionOf(et, 'Qualifications:', '\n\nExperience Required:'),
      required_years: reqYearsOf(j),
      required_years_max: reqHiOf(j),
      required_years_source: (j.required_years_manual !== undefined && j.required_years_manual !== null && j.required_years_manual !== '') ? 'manual' : (j.required_years_source || null),
      required_years_evidence: j.required_years_evidence || '',
      workplace_type: j.workplace_type,
      experience_required: j.experience_required,
      referral_link: j.referral_link,
      status: j.status,
      score,
      profile_key: profileKey,
      profile_resume_link: doc.resume_link || '',
    });
  }
}

// ---- B6: candidate family from similarity (top-K jobs over ALL jobs in their countries, newest resume) ----
let simFam = 'unknown';
if (CONFIG.FAMILY_FIRST) {
  const v = newest.embedding, nv = normOf(v);
  const ranked = countryJobs.filter(j => Array.isArray(j.embedding))
    .map(j => { let d = 0; const w = j.embedding; for (let i = 0; i < Math.min(v.length, w.length); i++) d += v[i] * w[i]; return { fam: familyOf(j.title), s: d / (nv * normOf(w)) }; })
    .sort((a, b) => b.s - a.s).slice(0, CONFIG.FAMILY_TOP_K);
  const votes = {};
  for (const r of ranked) votes[r.fam] = (votes[r.fam] || 0) + 1;
  const topVote = Math.max(0, ...Object.values(votes));
  simFam = ranked.length ? (ranked.find(r => votes[r.fam] === topVote) || ranked[0]).fam : 'unknown';
}
// ---- D1: family check ----
const candFam = CONFIG.FAMILY_FIRST ? simFam : (CONFIG.FAMILY_CHECK ? candidateFamily(newest.raw_cv) : 'unknown');
let scored = [...best.values()].map(r => {
  const jobFam = familyOf(r.title);
  const rel = (CONFIG.FAMILY_CHECK || CONFIG.FAMILY_FIRST) ? familyRelation(candFam, jobFam) : 'unchecked';
  const stretch = r.required_years > candYears;
  const tier = !CONFIG.FAMILY_FIRST ? 0 : rel === 'same' ? (stretch ? 1 : 0) : rel === 'adjacent' ? (stretch ? 3 : 2) : 4;
  const needed = (CONFIG.FAMILY_CHECK && rel === 'distant') ? MIN_SCORE + CONFIG.FAMILY_EXTRA : MIN_SCORE;
  const count7d = jobCounts[String(r.job_id)] || 0;
  const penalty = (CONFIG.SOFT_CAP && count7d >= CONFIG.SOFT_CAP_N) ? CONFIG.SOFT_CAP_PENALTY : 0;
  // 9 Oct: a job whose years are only assumed (title floor / no number) ranks a little below a job whose JD states them
  const assumed = r.required_years_source !== 'manual' && r.required_years_source !== 'rules_required' && r.required_years_source !== 'micro_verified';
  return { ...r, job_family: jobFam, family_relation: rel, stretch, tier, min_score_applied: needed, referrals_7d: count7d, years_assumed: assumed, rank_score: r.score - penalty - (assumed ? CONFIG.ASSUMED_PENALTY : 0) };
});
const droppedFamily = CONFIG.FAMILY_CHECK ? scored.filter(r => r.family_relation === 'distant' && r.score < r.min_score_applied).length : 0;

// ---- job preference (9 Oct): the candidate's form answer is a hard filter, like the country choice ----
//   same_level = same family, no stretch (tier 0) · same_stretch = same family (tiers 0–1) · any = everything
//   No answer (old form entries) = same_stretch (Satvik, 10 Oct): with same_level a fresher in data / engineering never matched (India has no 0-year job there).
//   The years window above already differs per option (same_level lo <= n, the others lo <= n + 1).
const prefOk = (r) => pref === 'same_level' ? (r.family_relation === 'same' && !r.stretch)
  : pref === 'same_stretch' ? r.family_relation === 'same' : true;
const droppedPreference = scored.filter(r => !prefOk(r)).length;

scored = scored
  .filter(prefOk)
  .filter(r => r.score >= r.min_score_applied)
  .sort((a, b) => (a.tier - b.tier) || (b.rank_score - a.rank_score));

const top = scored.slice(0, CONFIG.TOP_N);

// ---- D2: match strength ----
let matchStrength = 'n/a', gap = null;
if (top.length) {
  const rest = top.slice(1).map(r => r.rank_score).sort((a, b) => a - b);
  const median = rest.length ? (rest.length % 2 ? rest[(rest.length - 1) / 2] : (rest[rest.length / 2 - 1] + rest[rest.length / 2]) / 2) : null;
  gap = median === null ? null : +(top[0].rank_score - median).toFixed(4);
  const strongByGap = gap !== null && gap >= CONFIG.GAP_MIN;
  const strongByLevel = top[0].score >= MIN_SCORE + CONFIG.STRONG_EXTRA;
  matchStrength = (strongByGap || strongByLevel || median === null) ? 'strong' : 'weak';
}
const weak = CONFIG.GAP_CHECK && top.length > 0 && matchStrength === 'weak';

// ---- matched profile → pass its CV down for the hook sentence ----
const matchedDoc = top.length ? (candDocs.find(d => (d.candidate_key || '') === top[0].profile_key) || newest) : newest;

const skip_reason = top.length === 0
  ? (droppedPreference > 0 && scored.length === 0 ? 'no_job_for_preference'
    : droppedFamily > 0 && scored.length === 0 ? 'no_job_in_family' : 'no_job_above_threshold')
  : (weak ? 'weak_match' : undefined);

return [{
  json: {
    candidate: {
      ...candidate,
      years_experience: candYears,
      job_countries: rawCountries || 'India',
      job_preference: pref,
      profile_key: matchedDoc.candidate_key || null,
      profile_keys: candDocs.map(d => d.candidate_key).filter(Boolean),
      raw_cv: String(matchedDoc.raw_cv || '').slice(0, CONFIG.CV_SNIPPET_CHARS),
    },
    top_jobs: weak ? [] : top,
    considered_jobs: weak ? top.map(r => ({ job_id: r.job_id, title: r.title, score: r.score })) : undefined,
    wanted_countries: wantedCountries,
    jobs_pool: jobs.length,
    jobs_in_countries: countryJobs.length,
    candidate_years: candYears,
    jobs_within_experience: eligibleJobs.length,
    excluded_count: referredJobs.size,
    band_min_score: MIN_SCORE,
    candidate_family: candFam,
    family_source: CONFIG.FAMILY_FIRST ? 'similarity' : (CONFIG.FAMILY_CHECK ? 'cv_regex' : 'none'),
    stretch_match: top.length ? top[0].stretch === true : false,
    dropped_distant_family: droppedFamily,
    dropped_for_preference: droppedPreference,
    match_strength: matchStrength,
    top_gap: gap,
    profiles_scored: candDocs.length,
    skip_reason,
  }
}];