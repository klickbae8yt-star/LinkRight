"""Pick the 120 synthetic pairs the teacher (Claude) judges for the P1-3 gate: every non-NO pair, every hard negative (listed keyword overlap >= 2 but truth NO), and random other NO pairs.
The judge file is BLIND: no truth, no profile id. The key (pair_id -> profile, jd) is written to a separate file the judge does not read until scoring."""
import json, os, random
import synth as Y

def select(seed=11, n=120):
    truth = Y.all_truth(); jd = {j['id']: j for j in Y.jds()}; pr = {p['id']: p for p in Y.profiles()}
    must = [k for k, t in truth.items() if t['final'] != 'NO']
    hard = [k for k, t in truth.items() if t['final'] == 'NO' and t['listed_overlap'] >= 2]
    rest = sorted(k for k, t in truth.items() if t['final'] == 'NO' and k not in hard)
    r = random.Random(seed); r.shuffle(rest)
    chosen = must + hard + rest[:max(n - len(must) - len(hard), 0)]
    r.shuffle(chosen); pairs, key = [], {}
    for i, (p, j) in enumerate(chosen, 1):
        pid = 'g%03d' % i
        pairs.append({'pair_id': pid, 'n': i, 'jd_text': Y.jd_text(jd[j]), 'cv_text': Y.cv_text(pr[p]), 's0': {'pass': True, 'reasons': []}})
        key[pid] = {'profile': p, 'jd': j, 'truth': truth[(p, j)]}
    return pairs, key

if __name__ == '__main__':
    d = os.path.join(os.path.dirname(__file__), '..', 'data', 'synthetic_gate'); os.makedirs(d, exist_ok=True)
    pairs, key = select()
    json.dump(pairs, open(os.path.join(d, 'pairs.json'), 'w')); json.dump(key, open(os.path.join(d, 'key.json'), 'w'))
    print(len(pairs), 'pairs ->', d)
