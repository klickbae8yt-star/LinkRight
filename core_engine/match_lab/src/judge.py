"""Judgement tooling (P1-3): render a pair for the judge, validate a judgement against docs/rubric_v1.md (enums, quotes, coverage, consistency rules), score against truth."""
import re, json

FLAGS = ['keyword_stuffing', 'jd_copied', 'inflated_title', 'vague_bullets', 'unexplained_gap', 'frequent_switches', 'claims_without_evidence', 'over_qualified', 'irrelevant_history']
ENUM = {'s1.title_family': ('match', 'adjacent', 'no'), 's1.summary': ('specific', 'generic', 'missing'), 's1.recent_relevant_role': ('yes', 'older', 'no'), 's1.readability': ('clear', 'messy'),
        's1.verdict': ('PASS_SKIM', 'MAYBE', 'FAIL_SKIM'), 's2.verdict': ('ADVANCE', 'HOLD', 'REJECT'), 's3.domain': ('same', 'adjacent', 'different'), 's3.level': ('under', 'stretch', 'at', 'over'),
        's3.ownership': ('led', 'contributed', 'unclear'), 's3.impact': ('quantified', 'stated', 'none'), 's3.depth': ('described', 'listed', 'none'), 's3.stability': ('steady', 'mixed', 'unstable'),
        's3.verdict': ('INTERVIEW', 'MAYBE', 'NO'), 's5.verdict': ('SAFE', 'BORDERLINE', 'DO_NOT_REFER'), 'final.decision': ('REFER', 'STRETCH', 'HOLD', 'NO')}
STATUS = ('MET', 'PARTIAL', 'MISSING', 'UNKNOWN')

def order_for(n): return 'cv_first' if n % 2 == 1 else 'jd_first'

def render(n, jd, cv, s0):
    blocks = [('CV', cv), ('JOB', jd)] if order_for(n) == 'cv_first' else [('JOB', jd), ('CV', cv)]
    return 'PAIR %s  (order: %s)\nKNOCKOUTS (code): %s\n\n' % (n, order_for(n), 'PASS' if s0.get('pass') else 'FAIL ' + ','.join(s0.get('reasons', []))) + '\n\n'.join('=== %s ===\n%s' % b for b in blocks)

def _norm(t): return re.sub(r'\s+', ' ', str(t)).strip().lower()

def validate(j, jd, cv):
    e = []; src = _norm(jd) + ' || ' + _norm(cv)
    def get(path):
        cur = j
        for k in path.split('.'):
            if not isinstance(cur, dict) or k not in cur: return None
            cur = cur[k]
        return cur
    def quote_ok(q, where):
        if not isinstance(q, str) or len(q.strip()) < 6: e.append('quote too short or empty at %s' % where); return
        if _norm(q) not in src: e.append('quote not found in the source at %s: %r' % (where, q[:50]))
    s0 = j.get('s0') or {}
    if not isinstance(s0.get('pass'), bool): e.append('s0.pass missing')
    fin = j.get('final') or {}
    for k in ('reasons', 'risks'):
        if not isinstance(fin.get(k), list) or len(fin[k]) != 3: e.append('final.%s must be a list of exactly 3' % k)
    c = fin.get('confidence')
    if not isinstance(c, (int, float)) or isinstance(c, bool) or not 0 <= c <= 1: e.append('final.confidence must be between 0 and 1')
    if fin.get('decision') not in ENUM['final.decision']: e.append('final.decision not an allowed value'); return e
    if s0.get('pass') is False:
        if fin['decision'] != 'NO': e.append('knock-out failed, final must be NO')
        return e
    for p, allowed in ENUM.items():
        if p != 'final.decision' and get(p) not in allowed: e.append('%s must be one of %s' % (p, '/'.join(allowed)))
    if len(str(get('s1.feeling') or '').split()) > 20 or not get('s1.feeling'): e.append('s1.feeling must be 1 to 20 words')
    if len(str(get('s3.connects') or '').split()) > 25 or not get('s3.connects'): e.append('s3.connects must be 1 to 25 words')
    if len(str(get('s5.why') or '').split()) > 25 or not get('s5.why'): e.append('s5.why must be 1 to 25 words')
    for i, q in enumerate(get('s1.quotes') or []): quote_ok(q, 's1.quotes[%d]' % i)
    for i, q in enumerate(get('s3.quotes') or []): quote_ok(q, 's3.quotes[%d]' % i)
    musts = get('s2.musts') or []
    if not 3 <= len(musts) <= 10: e.append('s2.musts needs 3 to 10 items')
    met = part = ko = 0
    for i, m in enumerate(musts):
        st = m.get('status')
        if st not in STATUS: e.append('s2.musts[%d].status invalid' % i); continue
        met += st == 'MET'; part += st == 'PARTIAL'; ko += st == 'MISSING' and m.get('required', True)
        if st in ('MET', 'PARTIAL') or m.get('quote'): quote_ok(m.get('quote'), 's2.musts[%d]' % i)
    if musts and (get('s2.coverage') is None or abs((met + 0.5 * part) / len(musts) - get('s2.coverage')) > 0.02): e.append('s2.coverage does not match the musts')
    if get('s2.knockouts') != ko: e.append('s2.knockouts should be %d' % ko)
    flags = get('s4.flags'); fq = get('s4.flag_quotes') or {}
    if not isinstance(flags, dict) or set(flags) != set(FLAGS) or not all(isinstance(v, bool) for v in flags.values()): e.append('s4.flags must hold exactly the 9 boolean flags'); flags = {}
    nflags = sum(1 for v in flags.values() if v)
    for f, v in flags.items():
        if v:
            if f not in fq: e.append('s4.flag_quotes missing for %s' % f)
            else: quote_ok(fq[f], 's4.flag_quotes.' + f)
    s1, s2, s3, s5 = get('s1.verdict'), get('s2.verdict'), get('s3.verdict'), get('s5.verdict')
    dom, lvl, d = get('s3.domain'), get('s3.level'), fin['decision']
    if (s1 == 'FAIL_SKIM' or s2 == 'REJECT' or s3 == 'NO' or dom == 'different' or lvl == 'under') and s5 != 'DO_NOT_REFER': e.append('s5 must be DO_NOT_REFER (skim FAIL, screen REJECT, manager NO, domain different or level under)')
    if s5 == 'SAFE' and (s1 != 'PASS_SKIM' or s2 != 'ADVANCE' or s3 == 'NO' or nflags >= 2 or dom != 'same'): e.append('s5 SAFE needs skim PASS_SKIM, screen ADVANCE, manager not NO, domain same and fewer than 2 flags')
    if d == 'REFER' and not (s1 != 'FAIL_SKIM' and s2 == 'ADVANCE' and s3 == 'INTERVIEW' and s5 == 'SAFE' and dom == 'same' and lvl in ('at', 'stretch')): e.append('REFER needs skim not FAIL, screen ADVANCE, manager INTERVIEW, referrer SAFE, domain same, level at or stretch')
    if d == 'STRETCH' and not (s2 != 'REJECT' and s3 != 'NO' and s5 != 'DO_NOT_REFER' and dom != 'different'): e.append('STRETCH needs screen not REJECT, manager not NO, referrer not DO_NOT_REFER, domain not different')
    if d != 'NO' and (s5 == 'DO_NOT_REFER' or s3 == 'NO'): e.append('NO is required when referrer is DO_NOT_REFER or manager is NO')
    return e

def load_jsonl(path):
    out = {}
    try:
        for ln in open(path):
            if ln.strip(): j = json.loads(ln); out[j['pair_id']] = j
    except FileNotFoundError: pass
    return out
