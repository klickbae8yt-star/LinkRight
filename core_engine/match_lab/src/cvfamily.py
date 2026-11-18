"""Past family of a candidate, read ONLY from the candidate's own resume (never from matched jobs)."""
import re
from fieldclf import FAM, weak_family

MON = 'jan feb mar apr may jun jul aug sep oct nov dec'.split()
_M = r'(?:(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*,?\s*)?'
RANGE = re.compile(_M + r'((?:19|20)\d\d)\s*(?:–|—|-|to)\s*(?:' + _M + r'((?:19|20)\d\d)|(present|current|ongoing|till date|now))', re.I)
START = re.compile(r'^\s*(work experience|professional experience|experience|employment|internships?|work history)\b', re.I)
STOP = re.compile(r'^\s*(education|projects?|skills|technical skills|certifications?|achievements|awards|academic|publications|extra|volunteer|summary|profile|objective|about)\b', re.I)
SUMMARY = re.compile(r'^\s*(summary|professional summary|profile|objective|about( me)?|career objective)\b', re.I)
HALF_LIFE = 3.0   # years; ponytail: one global value, tune on the gold CV set (F-3)

def _t(mon, yr):
    return int(yr) + ((MON.index(mon.lower()[:3]) if mon else 5) + 0.5) / 12

def _lines(text, start, stop):
    out, on = [], False
    for ln in text.splitlines():
        if on and stop.match(ln): break
        if on: out.append(ln)
        elif start.match(ln): on = True
    return out

def parse_roles(text, now):
    ls = _lines(text, START, STOP); roles = []
    for i, ln in enumerate(ls):
        m = RANGE.search(ln)
        if not m: continue
        s = _t(m.group(1), m.group(2)); e = now if m.group(5) else _t(m.group(3), m.group(4))
        cand = [ln[:m.start()], ls[i + 1] if i + 1 < len(ls) else '', ls[i - 1] if i else '']   # title may sit on the next or previous line
        cand = [c.strip(' -–—|,:•·●❖') for c in cand]
        title = next((c for c in cand if c and weak_family(c)), '')
        if title and e >= s: roles.append((title, s, e))
    return roles

def _hits(text):
    h = {n: len(re.findall(r, text.lower())) for n, r in FAM}
    return {n: c for n, c in h.items() if c}

def _norm(d):
    z = sum(d.values()); return {k: v / z for k, v in d.items()} if z else {}

def cv_family(text, now, emb_probs=None):
    roles = parse_roles(text, now); w = {}
    for title, s, e in roles:
        f = weak_family(title)
        if f: w[f] = w.get(f, 0) + max(e - s, 0.25) * 0.5 ** ((now - e) / HALF_LIFE)
    head = _hits(' '.join(_lines(text, SUMMARY, STOP)[:6]))
    source, probs = 'titles', _norm(w)
    if probs and head:   # the summary is one more, lighter vote (how the person describes self today)
        probs = _norm({k: 0.8 * probs.get(k, 0) + 0.2 * _norm(head).get(k, 0) for k in set(probs) | set(head)})
    elif not probs and head: source, probs = 'headline', _norm(head)
    elif not probs and emb_probs: source, probs = 'embedding', _norm(emb_probs)
    elif not probs:
        t = _hits(text)
        if t: source, probs = 'text', _norm(t)
    if not probs: return {'past_family': None, 'probs': {}, 'confidence': 0.0, 'source': None, 'evidence_titles': [], 'last_role_end': None}
    top = max(probs, key=probs.get)
    return {'past_family': top, 'probs': probs, 'confidence': probs[top], 'source': source,
            'evidence_titles': [r[0] for r in roles], 'last_role_end': max((r[2] for r in roles), default=None)}

def allowed(r, thr=0.3):
    return [k for k, p in r['probs'].items() if p >= thr]
