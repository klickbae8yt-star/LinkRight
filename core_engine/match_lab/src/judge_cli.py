"""CLI for the synthetic gate (P1-3). show A B | append | status | eval.   Data in data/synthetic_gate/ (pairs.json blind, key.json truth, judgements.jsonl)."""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import judge as J
D = os.path.join(os.path.dirname(__file__), '..', 'data', os.environ.get('MATCH_DATA', 'synthetic_gate')); OUT = os.path.join(D, 'judgements.jsonl')
pairs = {p['pair_id']: p for p in json.load(open(os.path.join(D, 'pairs.json')))}
byn = {p['n']: p for p in pairs.values()}
cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
if cmd == 'show':
    for n in range(int(sys.argv[2]), int(sys.argv[3]) + 1): p = byn[n]; print(J.render(p['n'], p['jd_text'], p['cv_text'], p['s0']), '\n' + '#' * 70 + '\n')
elif cmd == 'append':
    done = J.load_jsonl(OUT); ok = bad = 0
    for ln in sys.stdin:
        if not ln.strip(): continue
        try: j = json.loads(ln)
        except Exception as ex: print('BAD JSON:', ex); bad += 1; continue
        p = pairs.get(j.get('pair_id'))
        if not p: print('unknown pair', j.get('pair_id')); bad += 1; continue
        if j['pair_id'] in done: print('already judged', j['pair_id']); bad += 1; continue
        if j.get('order') != J.order_for(p['n']): print(j['pair_id'], 'order field must be', J.order_for(p['n'])); bad += 1; continue
        errs = J.validate(j, p['jd_text'], p['cv_text'])
        if errs: print(j['pair_id'], 'REJECTED:', *errs, sep='\n   '); bad += 1; continue
        open(OUT, 'a').write(json.dumps(j, ensure_ascii=False) + '\n'); ok += 1
    print('appended', ok, 'rejected', bad)
elif cmd == 'status':
    done = J.load_jsonl(OUT); print('judged %d of %d; next pair number %s' % (len(done), len(pairs), next((n for n in sorted(byn) if byn[n]['pair_id'] not in done), 'none')))
elif cmd == 'eval':
    key = json.load(open(os.path.join(D, 'key.json'))); done = J.load_jsonl(OUT)
    rows = [(pid, j, key[pid]['truth']) for pid, j in done.items()]
    def agree(sel, f): r = [x for x in rows if sel(x)]; return (sum(f(x) for x in r) / len(r), len(r)) if r else (None, 0)
    fin = lambda x: x[1]['final']['decision'] == x[2]['final']
    print('judged', len(rows))
    print('final decision agreement  all:        %s' % (agree(lambda x: True, fin),))
    print('final decision agreement  unambiguous: %s' % (agree(lambda x: not x[2]['ambiguous'], fin),))
    print('NO vs not-NO agreement    all:        %s' % (agree(lambda x: True, lambda x: (x[1]['final']['decision'] == 'NO') == (x[2]['final'] == 'NO')),))
    print('domain agreement: %s   level agreement: %s' % (agree(lambda x: True, lambda x: x[1]['s3']['domain'] == x[2]['domain']), agree(lambda x: True, lambda x: x[1]['s3']['level'] == x[2]['level'])))
    c = collections.Counter((x[2]['final'], x[1]['final']['decision']) for x in rows)
    print('confusion (truth -> judge):'); [print('  %-8s -> %-8s %d' % (a, b, n)) for (a, b), n in sorted(c.items())]
    wrong_refer = [(pid, key[pid]['profile'], key[pid]['jd'], x[1]['final']['decision'], x[2]['final']) for pid, x in [(r[0], r) for r in rows] if x[1]['final']['decision'] in ('REFER', 'STRETCH') and x[2]['final'] == 'NO']
    print('DANGEROUS: judge says REFER/STRETCH where truth is NO:', len(wrong_refer)); [print('  ', w) for w in wrong_refer]
