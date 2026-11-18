"""V-4: top-1 quality of each variant from the labelled pool, paired bootstrap against raw cosine (same CVs)."""
import json, os, numpy as np, collections
D = os.path.join(os.path.dirname(__file__), '..', 'data', os.environ.get('RUN', 'v4'))
K = json.load(open(D + '/key.json')); L = {j['pid']: j for j in map(json.loads, open(D + '/labels.jsonl'))}
cvs = sorted({k['cv'] for k in K}); rank = {'NO': 0, 'HOLD': 1, 'STRETCH': 2, 'REFER': 3}
pick = collections.defaultdict(dict)
for k in K:
    for v in k['picked_by']: pick[v][k['cv']] = L[k['pid']]
F = {'acceptable (HOLD+)': lambda j: rank[j['decision']] >= 1, 'good (STRETCH+)': lambda j: rank[j['decision']] >= 2, 'REFER': lambda j: j['decision'] == 'REFER', 'domain not different': lambda j: j['domain'] != 'different'}
rng = np.random.default_rng(0); idx = [rng.integers(0, len(cvs), len(cvs)) for _ in range(5000)]
print('| variant | ' + ' | '.join(F) + ' |\n|---|' + '---|' * len(F))
for v in ['raw', 'gate_csls', 'gate_sink', 'gate_raw', 'neartie_d0.01', 'neartie_d0.02', 'raw_elig', 'elig_neartie_d0.01', 'U1', 'U1U2', 'U1U3', 'U1U1b', 'U1U1bU3']:
    if len(pick[v]) < len(cvs): continue
    cells = []
    for fn in F.values():
        a = np.array([fn(pick[v][c]) for c in cvs], float); b = np.array([fn(pick['raw'][c]) for c in cvs], float); d = [(a[i] - b[i]).mean() for i in idx]
        cells.append(f'{a.mean():.3f}' if v == 'raw' else f'{a.mean():.3f} ({(a-b).mean()*100:+.1f}; {np.percentile(d,2.5)*100:+.1f} to {np.percentile(d,97.5)*100:+.1f})')
    print(f'| {v} | ' + ' | '.join(cells) + ' |')
