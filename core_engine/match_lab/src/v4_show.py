import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, scrub as SC, gemma_family as G
D = os.path.join(os.path.dirname(__file__), '..', 'data')
P = json.load(open(D + '/' + os.environ.get('RUN', 'v4') + '/pairs.json')); v = json.load(open(D + '/vectors/prod_vectors_2026-10-13.json'))
T = {x['k']: x['t'] for x in json.load(open(D + '/vectors/cv_texts_2026-10-13.json'))}
JT = {x['job_id']: x for x in json.load(open(D + '/vectors/job_texts_2026-10-13.json'))}
def jd(j):
    t = re.sub(r'\s+', ' ', SC.scrub(JT[v['j'][j]['id']]['embedding_text'])); m = re.search(r'(Minimum Qualifications|Qualifications|Requirements|You have|What you)', t)
    d = t.find('Description:'); d = t[d + 12:d + 300] if d >= 0 else t[:300]
    return d + (' ... ' + t[m.start():m.start() + 330] if m else '')
P = [p for p in P if p['pid'] >= os.environ.get('MINPID', '')]; SEEN = {}
a, b = int(sys.argv[1]), int(sys.argv[2]); cvs = sorted({p['cv'] for p in P})[a:b]
for i in cvs:
    c = v['c'][i]; print(f"\n=== CV{i} years={c['y']} :: " + G.snippet(SC.scrub(T[c['k']]), 520))
    for p in [p for p in P if p['cv'] == i]:
        j = v['j'][p['job']]; g = SEEN.get(p['job']); SEEN.setdefault(p['job'], p['pid'])
        print(f"  [{p['pid']}] {j['t'][:70]} (yrs {j['lo']}-{j['hi']}) :: " + (f'same JD as [{g}]' if g else jd(p['job'])[:420]))
