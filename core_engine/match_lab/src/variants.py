"""Scoring variants on top of embedding vectors (plan 13 Oct 2026). All are dense matrix work: 3,586 x 450 in milliseconds.
S = resume x job score matrix. centre / csls / sinkhorn_caps / field_anchor are the pieces; top1 and concentration measure them."""
import numpy as np

def unit(M):
    M = np.asarray(M, float); return M / np.linalg.norm(M, axis=-1, keepdims=True)

def centre(A, B):
    """Subtract the shared mean direction from resumes and jobs, then renormalise. Mild fix for the 'all vectors look alike' effect (whitening was measured to hurt)."""
    m = np.vstack([A, B]).mean(0); return unit(A - m), unit(B - m)

def csls(S, k=10):
    """Cross-domain similarity local scaling: 2*S minus each resume's top-k mean and each job's top-k mean. Pushes down hub jobs."""
    rc = np.sort(S, 1)[:, -k:].mean(1, keepdims=True); rj = np.sort(S, 0)[-k:, :].mean(0, keepdims=True)
    return 2 * S - rc - rj

def sinkhorn_caps(S, caps, T=0.02, iters=100):
    """Soft assignment: every resume gets total weight 1, no job gets more than caps[j] (upper bound). Lower T = sharper picks.
    Returns the plan P (resume x job); argmax per row is the capacity-aware first choice."""
    S = np.asarray(S, float); caps = np.asarray(caps, float)
    K = np.exp((S - S.max()) / T); c = np.ones(S.shape[1])
    for _ in range(iters):
        r = 1.0 / (K @ c + 1e-30)
        col = (r[:, None] * K * c[None, :]).sum(0)
        c = c * np.minimum(1.0, caps / (col + 1e-30))
    r = 1.0 / (K @ c + 1e-30)
    return r[:, None] * K * c[None, :]

def field_anchor(cv, mean, field_vec, lam):
    """q = normalise((cv - mean) + lam * field_vec). lam = 0 gives the plain centred CV vector (here mean = 0 means plain CV)."""
    cv = np.asarray(cv, float); q = cv - mean + lam * np.asarray(field_vec, float)
    return unit(q)

def top1(S): return np.asarray(S).argmax(1)

def concentration(picks, n_jobs=None):
    """(distinct jobs used, share of picks that go to the two most picked jobs)."""
    vals, counts = np.unique(picks, return_counts=True)
    return len(vals), float(np.sort(counts)[::-1][:2].sum() / len(picks))

import re
CAMPUS = re.compile(r'campus|apprentice|internship|intern\b|graduate program|early career', re.I)

def eligible_mask(job_titles, years):
    """(resume x job) bool. Campus-type roles are offered only to people with 1 year or less (V-4: for 2+ years 13 of 15 such picks were NO)."""
    camp = np.array([bool(CAMPUS.search(t)) for t in job_titles]); y = np.asarray(years, float)
    return ~(camp[None, :] & (y >= 2)[:, None])

_GENERIC = {'and', 'of', 'the', 'ii', 'i', 'iii', 'sr', 'senior', 'jr', 'junior', 'associate', 'engineer', 'developer', 'software'}   # same stoplist as the test that gave 0.71 vs 0.56

def _core(title):
    from fieldclf import clean_title
    return set(re.findall(r'[a-z]+', clean_title(title).lower())) - _GENERIC if title else set()

def title_bonus(latest_titles, years, job_titles, b):
    """(resume x job) float. +b when the job title shares a specific (non-level) word with the person's latest title; only for 2+ years."""
    jc = [_core(t) for t in job_titles]; out = np.zeros((len(latest_titles), len(job_titles)))
    for i, (t, y) in enumerate(zip(latest_titles, years)):
        if y is None or y < 2: continue
        c = _core(t)
        for j, k in enumerate(jc):
            if c & k: out[i, j] = b
    return out

def neartie(S, mask, delta, cap, seed=0):
    """Greedy: each resume takes the best job among those within delta of its best that still have room (load < cap); if none has room, its best. ponytail: sequential, order matters; seed fixes it."""
    S = np.asarray(S, float); rng = np.random.default_rng(seed); load = np.zeros(S.shape[1]); pick = np.full(S.shape[0], -1)
    for i in rng.permutation(S.shape[0]):
        s = np.where(mask[i], S[i], -9.0); b = s.max()
        if b < -1: continue
        near = np.where(s >= b - delta - 1e-12)[0]; free = near[load[near] < cap]
        j = free[s[free].argmax()] if len(free) else int(s.argmax()); pick[i] = j; load[j] += 1
    return pick

CAMPUS_GRAD = re.compile(r'campus graduate\b', re.I)
MASTERS = re.compile(r"m\.?\s?tech|m\.e\.|msc|m\.sc|master|\bmba\b|\bmca\b|pgdm|pgdba|post[- ]?graduate|m\.?com\b|\bms in\b", re.I)

def masters_mask(job_titles, cv_texts):
    """(resume x job) bool. 'Campus Graduate ...' programs need a master's degree (earned or in progress); a CV with no master-type word in its text is not offered them.
    V-4 + fresh test: of 108 labelled pairs on such jobs, none for a CV without a master degree was a REFER (83 pairs: 8 STRETCH, 54 HOLD, 21 NO)."""
    cg = np.array([bool(CAMPUS_GRAD.search(t)) for t in job_titles]); has = np.array([bool(MASTERS.search(t or '')) for t in cv_texts])
    return ~(cg[None, :] & ~has[:, None])
