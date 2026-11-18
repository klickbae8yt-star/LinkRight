"""Print blind pairs a..b; a JD already printed earlier in this batch is replaced by a pointer (same text, saves tokens)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import judge as J
D = os.path.join(os.path.dirname(__file__), '..', 'data', os.environ.get('MATCH_DATA', 'real_pilot'))
P = {p['n']: p for p in json.load(open(os.path.join(D, 'pairs.json')))}; seen = {}
for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    p = P[n]; jd = p['jd_text']; txt = J.render(n, jd, p['cv_text'], p['s0'])
    if jd in seen: txt = txt.replace(jd, '[JOB TEXT IDENTICAL TO PAIR %d: %s]' % (seen[jd], jd.split('\n')[0]))
    else: seen[jd] = n
    print(txt, '\n' + '#' * 40)
