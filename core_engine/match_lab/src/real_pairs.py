"""P2-2: pick blind pilot pairs from the real scrubbed export. Writes data/real_pilot/pairs.json (blind) and key.json (how each pair was picked, scores).
Knock-outs by code: country India for all; years window = years >= req_years - 1 and (no max or years <= max + 1)."""
import json, os, random, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import pipelines as P

ROOT = os.path.join(os.path.dirname(__file__), '..', 'data')

def select(n=60, seed=13):
    d = json.load(open(os.path.join(ROOT, 'real', 'export_2026-10-13.json'))); C, J = d['candidates'], d['jobs']
    Q, D = 'search_query: ', 'search_document: '
    raw = P.embed([c['cv'] for c in C]) @ P.embed([j['jd'] for j in J]).T
    pre = P.embed([Q + c['cv'] for c in C]) @ P.embed([D + j['jd'] for j in J]).T; alt = P.csls(pre)
    ok = np.array([[c['years'] >= (j['req_years'] or 0) - 1 and (not j.get('req_years_max') or c['years'] <= j['req_years_max'] + 1) for j in J] for c in C])
    rng = random.Random(seed); chosen = {}
    def take(label, cells, k):
        fresh = [x for x in cells if x not in chosen and ok[x]]
        for x in rng.sample(fresh, min(k, len(fresh))): chosen[x] = label
    top = lambda S: sorted(((int(S[i].argmax()), i) for i in range(len(C)) if ok[i, S[i].argmax()]), key=lambda t: -S[t[1], t[0]])
    take('p0_top1', [(i, j) for j, i in top(raw)][:40], 15)
    take('alt_top1', [(i, j) for j, i in top(alt)][:40], 15)
    take('p0_rank2to5', [(i, int(j)) for i in range(len(C)) for j in np.argsort(-raw[i])[1:5]], 10)
    take('random_pass', [(i, j) for i in range(len(C)) for j in range(len(J))], n - len(chosen))
    items = list(chosen.items()); rng.shuffle(items); pairs, key = [], {}
    for k, ((i, j), label) in enumerate(items, 1):
        pid = 'r%03d' % k
        pairs.append({'pair_id': pid, 'n': k, 'jd_text': J[j]['title'] + '\n' + J[j]['jd'], 'cv_text': C[i]['cv'], 's0': {'pass': True, 'reasons': []}})
        key[pid] = {'cid': C[i]['cid'], 'job_id': J[j]['job_id'], 'picked_by': label, 'cos_raw': float(raw[i, j]), 'cos_pre': float(pre[i, j]), 'csls': float(alt[i, j]), 'years': C[i]['years'], 'req_years': J[j]['req_years']}
    out = os.path.join(ROOT, 'real_pilot'); os.makedirs(out, exist_ok=True)
    json.dump(pairs, open(os.path.join(out, 'pairs.json'), 'w')); json.dump(key, open(os.path.join(out, 'key.json'), 'w'))
    return pairs, key

if __name__ == '__main__':
    p, k = select(); import collections; print(len(p), collections.Counter(v['picked_by'] for v in k.values()))
