"""Metrics for the matching study (P1-1). Primary metric: wrong-referral rate at equal coverage.
gold[(cand, job)] = {'final', 's5', 'domain', 'level'} (rubric v1 fields); out[cand] = [(job, score), ...].
A pair that is not judged is never scored silently: it raises KeyError('unjudged ...'). Use unjudged() to list what still needs judging."""
import math
import numpy as np
from scipy.stats import spearmanr

GAIN = {'REFER': 3, 'STRETCH': 2, 'HOLD': 1, 'NO': 0}

def gain(row): return GAIN[row['final']]
def is_wrong(row): return row['final'] == 'NO' or row['s5'] == 'DO_NOT_REFER'
def is_unsafe(row): return is_wrong(row) or row['final'] == 'HOLD'
def is_critical(row): return row['domain'] == 'different' or row['level'] in ('under', 'over')
def is_good(row): return row['final'] in ('REFER', 'STRETCH')

def _ranked(out):
    return {c: sorted(v, key=lambda t: (-t[1], str(t[0]))) for c, v in out.items() if v}

def _row(gold, c, j):
    try: return gold[(c, j)]
    except KeyError: raise KeyError('unjudged pair %s, %s' % (c, j))

def top1(out):
    return [(c, v[0][0], v[0][1]) for c, v in _ranked(out).items()]

def referred(out, n):
    """The n candidates with the highest top-1 score (ties by candidate id): the people who would get a referral at this coverage."""
    return sorted(top1(out), key=lambda t: (-t[2], str(t[0])))[:max(n, 0)]

def unjudged(out, gold, k=1):
    return [(c, j) for c, v in sorted(_ranked(out).items(), key=lambda t: str(t[0])) for j, _ in v[:k] if (c, j) not in gold]

def _rate(out, gold, n, pred):
    r = referred(out, n)
    if not r: return None
    return sum(1 for c, j, _ in r if pred(_row(gold, c, j))) / len(r)

def wrong_rate(out, gold, n): return _rate(out, gold, n, is_wrong)
def unsafe_rate(out, gold, n): return _rate(out, gold, n, is_unsafe)
def critical_errors(out, gold, n):
    return sum(1 for c, j, _ in referred(out, n) if is_wrong(_row(gold, c, j)) and is_critical(_row(gold, c, j)))
def coverage_n(out, floor): return sum(1 for _, _, s in top1(out) if s >= floor)

def mean_precision_at_k(out, gold, k):
    vals = [sum(is_good(_row(gold, c, j)) for j, _ in v[:k]) / min(k, len(v[:k])) for c, v in _ranked(out).items()]
    return sum(vals) / len(vals) if vals else None

def ndcg_at_k(out, gold, k):
    vals = []
    for c, v in _ranked(out).items():
        gains = [gain(_row(gold, c, j)) for j, _ in v[:k]]
        ideal = sorted((gain(r) for (cc, _), r in gold.items() if cc == c), reverse=True)[:k]
        dcg = sum(g / math.log2(i + 2) for i, g in enumerate(gains)); idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
        vals.append(dcg / idcg if idcg else 1.0)
    return sum(vals) / len(vals) if vals else None

def mrr(out, gold):
    vals = []
    for c, v in _ranked(out).items():
        rr = 0.0
        for i, (j, _) in enumerate(v):
            if is_good(_row(gold, c, j)): rr = 1.0 / (i + 1); break
        vals.append(rr)
    return sum(vals) / len(vals) if vals else None

def auc(scores, labels):
    pos = [s for s, l in zip(scores, labels) if l]; neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg: return None
    wins = sum((p > q) + 0.5 * (p == q) for p in pos for q in neg)
    return wins / (len(pos) * len(neg))

def top1_auc(out, gold):
    rows = top1(out)
    return auc([s for _, _, s in rows], [not is_wrong(_row(gold, c, j)) for c, j, _ in rows])

def ece(conf, correct, bins=10):
    conf = np.asarray(conf, float); correct = np.asarray(correct, float); n = len(conf)
    if n == 0: return None
    idx = np.minimum((conf * bins).astype(int), bins - 1); total = 0.0
    for b in range(bins):
        m = idx == b
        if m.any(): total += abs(correct[m].mean() - conf[m].mean()) * m.sum() / n
    return float(total)

def length_corr(out, lengths):
    rows = [(s, lengths[c]) for c, _, s in top1(out) if c in lengths]
    if len(rows) < 3: return None
    r = spearmanr([a for a, _ in rows], [b for _, b in rows]).correlation
    return None if r != r else float(r)

def top2_share(out, n):
    r = referred(out, n)
    if not r: return None
    counts = {}
    for _, j, _ in r: counts[j] = counts.get(j, 0) + 1
    return sum(sorted(counts.values(), reverse=True)[:2]) / len(r)

def agreement(a, b):
    ta = {c: j for c, j, _ in top1(a)}; tb = {c: j for c, j, _ in top1(b)}
    common = [c for c in ta if c in tb]
    return sum(ta[c] == tb[c] for c in common) / len(common) if common else None

def paired_bootstrap(a, b, gold, coverage, B=2000, seed=0):
    """A = baseline, B = candidate. Candidates are resampled with replacement, the same draw for both; each pipeline refers its own top `coverage` share.
    Returns wrong rates at the full sample, mean and 95% interval of (wrong_a - wrong_b), and the relative reduction 1 - wrong_b / wrong_a."""
    cands = sorted(set(a) & set(b), key=str); rng = np.random.default_rng(seed)
    ta = {c: (j, s) for c, j, s in top1(a)}; tb = {c: (j, s) for c, j, s in top1(b)}
    wa = {c: is_wrong(_row(gold, c, ta[c][0])) for c in cands if c in ta}; wb = {c: is_wrong(_row(gold, c, tb[c][0])) for c in cands if c in tb}
    cands = [c for c in cands if c in wa and c in wb]
    def rate(sample, t, w):
        k = max(int(round(coverage * len(sample))), 1); top = sorted(sample, key=lambda c: (-t[c][1], str(c)))[:k]
        return sum(w[c] for c in top) / len(top)
    full_a, full_b = rate(cands, ta, wa), rate(cands, tb, wb); diffs = []
    for _ in range(B):
        s = [cands[i] for i in rng.integers(0, len(cands), len(cands))]
        diffs.append(rate(s, ta, wa) - rate(s, tb, wb))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {'wrong_a': full_a, 'wrong_b': full_b, 'diff_mean': float(np.mean(diffs)), 'diff_ci': (float(lo), float(hi)), 'rel_reduction': (1 - full_b / full_a) if full_a else 0.0}

def adopt_rule(res, critical_a, critical_b):
    """The fixed rule (plan): adopt only if the wrong-referral rate falls by at least 40% relative, the 95% interval of the difference excludes zero, and critical errors do not rise."""
    ok = res['rel_reduction'] >= 0.40 and res['diff_ci'][0] > 0 and critical_b <= critical_a
    return {'adopt': bool(ok), 'rel_reduction': res['rel_reduction'], 'ci_low': res['diff_ci'][0], 'critical_a': critical_a, 'critical_b': critical_b}
