"""V-4: pool of (CV, job) pairs for labelling. Top-1 of 3 variants for 150 random CVs; blind (variant names go to a key file only)."""
import json, os, random, re, sys
import numpy as np
D = os.path.join(os.path.dirname(__file__), '..')
exec(open(os.path.join(D, 'src', 'run_v3.py')).read().split('rows = []')[0])   # ponytail: reuses the matrices of run_v3 without its table print; split into a module if a third script needs it
import scrub as SC
JT = {x['job_id']: x for x in json.load(open(os.path.join(D, 'data', 'vectors', 'job_texts_2026-10-13.json')))}
has_text = np.array([j['id'] in JT for j in J]); ok2 = ok & has_text[None, :]
S0 = A @ B.T; Ac, Bc = V.centre(A, B)
VAR = {'raw': best(S0, ok2)[0], 'gate_csls': best(V.csls(S0), ok2 & gate)[0], 'gate_sink': best(V.sinkhorn_caps(Ac @ Bc.T, caps), ok2 & gate)[0]}
has = (ok2 & gate).any(1)
fam = [CF.cv_family(T[c['k']], now=2026.8) for c in C]
cand = [i for i in range(len(C)) if has[i] and fam[i]['source'] in ('titles', 'headline')]
random.seed(11); rows_ = sorted(random.sample(cand, 150))
pairs, key = [], []
for i in rows_:
    js = sorted({int(VAR[v][i]) for v in VAR}); random.shuffle(js)
    for j in js:
        pairs.append({'pid': f'v{len(pairs)+1:03d}', 'cv': i, 'job': j})
        key.append({'pid': pairs[-1]['pid'], 'cv': i, 'job': j, 'picked_by': [v for v in VAR if VAR[v][i] == j], 'cv_family': fam[i]['past_family'], 'job_family': cls[jfam[j]], 'cos': float(S0[i, j])})
os.makedirs(os.path.join(D, 'data', 'v4'), exist_ok=True)
json.dump(pairs, open(os.path.join(D, 'data', 'v4', 'pairs.json'), 'w')); json.dump(key, open(os.path.join(D, 'data', 'v4', 'key.json'), 'w'))
print(len(rows_), 'CVs', len(pairs), 'pairs'); import collections
print('pairs picked by n variants:', collections.Counter(len(k['picked_by']) for k in key))
