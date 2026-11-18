"""U-3 fresh test: new random 150 CVs (not in the V-4 sample). Variants: plain cosine, U1 eligibility, U1+U2 title bonus, U1+U3 near-tie."""
import json, os, random, sys, collections
import numpy as np
D = os.path.join(os.path.dirname(__file__), '..')
exec(open(os.path.join(D, 'src', 'run_v3.py')).read().split('rows = []')[0])   # ponytail: same shortcut as v4_pool.py
JT = {x['job_id']: x for x in json.load(open(os.path.join(D, 'data', 'vectors', 'job_texts_2026-10-13.json')))}
has_text = np.array([j['id'] in JT for j in J]); ok2 = ok & has_text[None, :]
S0 = A @ B.T; jt = [j['t'] for j in J]; elig = V.eligible_mask(jt, yrs); okE = ok2 & elig
latest = []
for c in C:
    r = CF.parse_roles(T[c['k']], 2026.8); latest.append(max(r, key=lambda x: (x[2], x[1]))[0] if r else None)
bonus = V.title_bonus(latest, yrs.astype(float), jt, 0.01)
rawp = np.where(ok2, S0, -9).argmax(1)
VAR = {'raw': rawp, 'U1': np.where(okE, S0, -9).argmax(1), 'U1U2': np.where(okE, S0 + bonus, -9).argmax(1), 'U1U3': V.neartie(S0, okE, 0.01, 3 * len(C) / len(J))}
old = {k['cv'] for k in json.load(open(os.path.join(D, 'data', 'v4', 'key.json')))}
has = okE.any(1); fam = [CF.cv_family(T[c['k']], now=2026.8) for c in C]
cand = [i for i in range(len(C)) if has[i] and fam[i]['source'] in ('titles', 'headline') and i not in old]
random.seed(23); rows_ = sorted(random.sample(cand, 150)); pairs, key = [], []
prev = {(k['cv'], k['job']): L for k, L in ()}   # nothing reused: new CVs have no earlier labels
for i in rows_:
    js = sorted({int(VAR[v][i]) for v in VAR}); random.shuffle(js)
    for j in js:
        pairs.append({'pid': f'f{len(pairs)+1:03d}', 'cv': i, 'job': j})
        key.append({'pid': pairs[-1]['pid'], 'cv': i, 'job': j, 'picked_by': [v for v in VAR if VAR[v][i] == j], 'cos': float(S0[i, j])})
os.makedirs(os.path.join(D, 'data', 'v5'), exist_ok=True)
json.dump(pairs, open(os.path.join(D, 'data', 'v5', 'pairs.json'), 'w')); json.dump(key, open(os.path.join(D, 'data', 'v5', 'key.json'), 'w'))
print(len(rows_), 'CVs', len(pairs), 'pairs'); print('changed picks vs raw:', {v: int((VAR[v][rows_] != rawp[rows_]).sum()) for v in VAR})
