"""Compact way to WRITE a judgement (P1-3). The content is the judge's; this only builds the JSON of docs/rubric_v1.md, counts coverage and knock-outs from the musts, and runs the validator.
J(pid, s1=(title_family, summary, recent, readability, verdict, feeling, [quotes]), m=[(req, STATUS, quote)], s2v='ADVANCE|HOLD|REJECT',
  s3=(domain, level, ownership, impact, depth, stability, connects, verdict, [quotes]), flags={flag: quote}, s5=(verdict, why), fin=(decision, confidence, [3 reasons], [3 risks]))
commit() validates every judgement against its pair and appends the good ones to data/synthetic_gate/judgements.jsonl."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import judge as J_
D = os.path.join(os.path.dirname(__file__), '..', 'data', os.environ.get('MATCH_DATA', 'synthetic_gate')); OUT = os.path.join(D, 'judgements.jsonl')
_pairs = {p['pair_id']: p for p in json.load(open(os.path.join(D, 'pairs.json')))}
_batch = []

def J(pid, s1, m, s2v, s3, flags, s5, fin):
    musts = [{'req': r, 'status': s, **({'quote': q} if q else {})} for r, s, q in m]
    met = sum(x['status'] == 'MET' for x in musts); part = sum(x['status'] == 'PARTIAL' for x in musts); ko = sum(x['status'] == 'MISSING' for x in musts)
    fl = {k: False for k in J_.FLAGS}; fl.update({k: True for k in flags})
    j = {'pair_id': pid, 'rubric': 'v1', 'order': J_.order_for(_pairs[pid]['n']), 's0': {'pass': True, 'reasons': []},
         's1': dict(zip(('title_family', 'summary', 'recent_relevant_role', 'readability', 'verdict', 'feeling', 'quotes'), s1)),
         's2': {'musts': musts, 'coverage': round((met + 0.5 * part) / len(musts), 4), 'knockouts': ko, 'verdict': s2v},
         's3': dict(zip(('domain', 'level', 'ownership', 'impact', 'depth', 'stability', 'connects', 'verdict', 'quotes'), s3)),
         's4': {'flags': fl, 'flag_quotes': dict(flags)}, 's5': {'verdict': s5[0], 'why': s5[1]},
         'final': {'decision': fin[0], 'confidence': fin[1], 'reasons': fin[2], 'risks': fin[3]}}
    _batch.append(j)

def commit():
    done = J_.load_jsonl(OUT); ok = bad = 0
    for j in _batch:
        p = _pairs[j['pair_id']]
        if j['pair_id'] in done: print(j['pair_id'], 'already judged'); bad += 1; continue
        errs = J_.validate(j, p['jd_text'], p['cv_text'])
        if errs: print(j['pair_id'], 'REJECTED:', *errs, sep='\n   '); bad += 1; continue
        open(OUT, 'a').write(json.dumps(j, ensure_ascii=False) + '\n'); ok += 1
    _batch.clear(); print('appended', ok, 'rejected', bad, '| total judged', len(J_.load_jsonl(OUT)))
