"""V-3: free checks (no labels) for scoring variants on the 3,586 x 450 production vectors. Prints a markdown table."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import variants as V, fieldclf as F, cvfamily as CF

d = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'vectors', 'prod_vectors_2026-10-13.json')))
C, J = d['c'], d['j']
A = V.unit(np.array([c['e'] for c in C], float)); B = V.unit(np.array([j['e'] for j in J], float))
yrs = np.array([c['y'] or 0 for c in C]); lo = np.array([j['lo'] or 0 for j in J]); hi = np.array([j['hi'] or 0 for j in J])
ok = (yrs[:, None] >= lo[None, :] - 1) & ((hi[None, :] == 0) | (yrs[:, None] <= hi[None, :] + 1))
ok &= np.array([[j['co'] in (c['jc'] or '') for j in J] for c in C]) | True  # ponytail: country list format unverified, not applied yet
jf = [F.weak_family(j['t']) for j in J]; m = F.fit(B, jf)
PC, PJ = m.predict_proba(A), m.predict_proba(B)
jfam = PJ.argmax(1)
# F-4: CV family from the resume only (titles + summary, 50/50 with the embedding classifier), never from the matched jobs
T = {x['k']: x['t'] for x in json.load(open(os.path.join(os.path.dirname(__file__), '..', 'data', 'vectors', 'cv_texts_2026-10-13.json')))}
cls = list(m.classes_); RP = np.array([[CF.cv_family(T[c['k']], now=2026.8)['probs'].get(k, 0) for k in cls] for c in C])
MIX = 0.5 * RP + 0.5 * PC; MIX[RP.sum(1) == 0] = PC[RP.sum(1) == 0]    # no usable resume text: embedding only
cfam = MIX.argmax(1)
grp = np.array([0 if k in ('data', 'engineer') else i + 1 for i, k in enumerate(cls)])   # engineer and data are one "tech" group (gold: 0.91 vs 0.79 exact)
gate = (grp[cfam][:, None] == grp[jfam][None, :])    # same field, hard (default of the form answer)
exact = MIX[:, jfam]                                  # P(CV is in this job's exact family): soft preference inside the group
jobs_per = np.bincount(jfam, minlength=len(m.classes_))
caps = np.maximum(1.0, np.full(len(J), len(C) / len(J)) * 2)   # soft cap: 2x average load, ponytail: demand-weighting later

def best(S, mask):
    S = np.where(mask, S, -1e9); p = S.argmax(1); has = mask.any(1); return p, has

def row(name, S, mask, t):
    p, has = best(S, mask); p = p[has]
    n, top2 = V.concentration(p)
    load = np.bincount(p, minlength=len(J)); raw_top = (A @ B.T).argmax(1)[has]
    fam_ok = (jfam[p] == cfam[has]).mean()
    return f'| {name} | {has.mean():.2f} | {n} | {top2:.2f} | {load.max()} | {fam_ok:.2f} | {(p == raw_top).mean():.2f} | {t*1000:.0f} |'

rows = []
def run(name, f, mask):
    t = time.time(); S = f(); rows.append(row(name, S, mask, time.time() - t))

S0 = A @ B.T
run('raw cosine', lambda: S0, ok)
Ac, Bc = V.centre(A, B)
run('centred', lambda: Ac @ Bc.T, ok)
run('CSLS(raw)', lambda: V.csls(S0), ok)
run('CSLS(centred)', lambda: V.csls(Ac @ Bc.T), ok)
run('sinkhorn caps(centred)', lambda: V.sinkhorn_caps(Ac @ Bc.T, caps), ok)
run('gate + raw', lambda: S0, ok & gate)
run('gate + CSLS', lambda: V.csls(S0), ok & gate)
run('gate + CSLS(centred)', lambda: V.csls(Ac @ Bc.T), ok & gate)
run('gate + sinkhorn caps', lambda: V.sinkhorn_caps(Ac @ Bc.T, caps), ok & gate)
run('gate + CSLS + exact-family bonus', lambda: V.csls(S0) + 0.05 * exact * V.csls(S0).std(), ok & gate)
run('gate + sinkhorn caps + exact bonus', lambda: V.sinkhorn_caps(Ac @ Bc.T + 0.05 * exact * 0.1, caps), ok & gate)
mean = np.vstack([A, B]).mean(0)
for lam in (0.5, 1.0):
    def anchor(lam=lam):
        fv = np.array([B[jfam == k].mean(0) for k in range(len(m.classes_))])
        Q = V.unit(A - mean + lam * fv[cfam]); return Q @ V.unit(B - mean).T
    run(f'field anchor lam={lam} + CSLS gate', lambda: V.csls(anchor()), ok & gate)

print('families:', dict(zip(m.classes_, jobs_per)))
print('| variant | resumes with a job | jobs used | top-2 share | max load | family = CV family | same as raw top-1 | ms |')
print('|---|---|---|---|---|---|---|---|'); print('\n'.join(rows))
