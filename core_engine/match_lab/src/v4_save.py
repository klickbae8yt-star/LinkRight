"""Save compact V-4 labels: 'pid code domain', code R/S/H/N = REFER/STRETCH/HOLD/NO, domain s/a/x = same/adjacent/different. Rubric v1.1, judge = Claude session (tier S)."""
import json, sys, os
M = {'R': 'REFER', 'S': 'STRETCH', 'H': 'HOLD', 'N': 'NO'}; DOM = {'s': 'same', 'a': 'adjacent', 'x': 'different'}
OUT = os.path.join(os.path.dirname(__file__), '..', 'data', os.environ.get('RUN', 'v4'), 'labels.jsonl')
def save(txt):
    done = {json.loads(l)['pid'] for l in open(OUT)} if os.path.exists(OUT) else set(); n = 0
    with open(OUT, 'a') as f:
        for tok in txt.replace('\n', ' ').split('|'):
            if not tok.strip(): continue
            pid, c, d = tok.split()
            if pid in done: print('dup', pid); continue
            f.write(json.dumps({'pid': pid, 'decision': M[c], 'domain': DOM[d], 'rubric': 'v1.1', 'tier': 'S'}) + '\n'); n += 1
    print('saved', n, 'total', len(done) + n)
