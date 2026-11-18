"""Metrics tests (P1-1). Written BEFORE src/metrics.py. Toy rankings with hand-computed answers.
Data model: gold[(cand, job)] = {'final': REFER|STRETCH|HOLD|NO, 's5': SAFE|BORDERLINE|DO_NOT_REFER, 'domain': same|adjacent|different, 'level': under|stretch|at|over}
pipeline output: out[cand] = [(job, score), ...] (any order; the library sorts by score desc, then job id)."""
import math, os, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import metrics as M

def g(final, s5='SAFE', domain='same', level='at'): return {'final': final, 's5': s5, 'domain': domain, 'level': level}
GOLD = {('c1', 'j1'): g('REFER'), ('c1', 'j2'): g('NO', 'DO_NOT_REFER', 'different'), ('c1', 'j3'): g('HOLD', 'BORDERLINE'),
        ('c2', 'j1'): g('NO', 'DO_NOT_REFER', 'different', 'over'), ('c2', 'j2'): g('REFER'), ('c2', 'j3'): g('STRETCH', 'BORDERLINE', 'adjacent', 'stretch'),
        ('c3', 'j1'): g('REFER'), ('c3', 'j2'): g('REFER'), ('c3', 'j3'): g('NO', 'DO_NOT_REFER', 'different'),
        ('c4', 'j1'): g('NO', 'BORDERLINE', 'adjacent', 'under'), ('c4', 'j2'): g('HOLD', 'BORDERLINE'), ('c4', 'j3'): g('REFER')}
P_GOOD = {'c1': [('j1', .9), ('j2', .5)], 'c2': [('j2', .8), ('j1', .4)], 'c3': [('j1', .7), ('j2', .6)], 'c4': [('j3', .6), ('j1', .3)]}   # every top-1 is REFER
P_BAD = {'c1': [('j2', .9), ('j1', .5)], 'c2': [('j1', .8), ('j2', .4)], 'c3': [('j1', .7), ('j2', .6)], 'c4': [('j1', .6), ('j3', .3)]}    # c1, c2, c4 top-1 are NO

def test_label_helpers():
    assert M.is_wrong(g('NO')) and M.is_wrong(g('REFER', 'DO_NOT_REFER')) and not M.is_wrong(g('HOLD', 'BORDERLINE')) and not M.is_wrong(g('REFER'))
    assert M.is_unsafe(g('HOLD', 'BORDERLINE')) and M.is_unsafe(g('NO')) and not M.is_unsafe(g('STRETCH', 'BORDERLINE')) and not M.is_unsafe(g('REFER'))
    assert M.is_critical(g('NO', domain='different')) and M.is_critical(g('NO', level='under')) and M.is_critical(g('NO', level='over')) and not M.is_critical(g('NO', domain='adjacent', level='at'))
    assert [M.gain(g(x)) for x in ('REFER', 'STRETCH', 'HOLD', 'NO')] == [3, 2, 1, 0]

def test_wrong_rate_at_equal_coverage():
    assert M.wrong_rate(P_GOOD, GOLD, n=4) == 0.0
    assert M.wrong_rate(P_BAD, GOLD, n=4) == 0.75
    assert M.wrong_rate(P_BAD, GOLD, n=3) == pytest.approx(2 / 3)       # referred: c1 .9 (wrong), c2 .8 (wrong), c3 .7 (ok)
    assert M.wrong_rate(P_BAD, GOLD, n=2) == 1.0
    assert M.wrong_rate(P_BAD, GOLD, n=1) == 1.0
    assert M.wrong_rate(P_BAD, GOLD, n=0) is None                      # nobody referred: no rate, never a fake 0
    assert M.unsafe_rate({'c4': [('j2', .9)]}, GOLD, n=1) == 1.0        # HOLD is unsafe, not wrong
    assert M.wrong_rate({'c4': [('j2', .9)]}, GOLD, n=1) == 0.0

def test_critical_errors_and_coverage_n():
    assert M.critical_errors(P_BAD, GOLD, n=4) == 3 and M.critical_errors(P_GOOD, GOLD, n=4) == 0
    assert M.coverage_n(P_BAD, floor=0.65) == 3 and M.coverage_n(P_BAD, floor=0.0) == 4 and M.coverage_n(P_BAD, floor=0.95) == 0

def test_unjudged_pairs_are_never_scored_silently():
    gold = dict(GOLD); del gold[('c1', 'j2')]
    assert M.unjudged(P_BAD, gold, k=1) == [('c1', 'j2')]
    with pytest.raises(KeyError, match='unjudged'): M.wrong_rate(P_BAD, gold, n=4)

def test_precision_ndcg_mrr():
    assert M.mean_precision_at_k(P_GOOD, GOLD, 1) == 1.0 and M.mean_precision_at_k(P_BAD, GOLD, 1) == 0.25
    assert M.mean_precision_at_k({'c1': [('j1', .9), ('j2', .5)]}, GOLD, 2) == 0.5
    one = M.ndcg_at_k({'c1': [('j2', .9), ('j1', .5)]}, GOLD, 2)           # ranking gains [0, 3]; ideal over ALL judged jobs of c1 (3, 1, 0) at k=2 is [3, 1]
    assert one == pytest.approx((3 / math.log2(3)) / (3 + 1 / math.log2(3)))
    assert M.ndcg_at_k(P_GOOD, GOLD, 1) == pytest.approx(1.0)              # every top-1 is the best judged job
    assert M.mrr(P_BAD, GOLD) == pytest.approx((0.5 + 0.5 + 1 + 0.5) / 4)

def test_auc():
    assert M.auc([.9, .8, .2, .1], [1, 1, 0, 0]) == 1.0
    assert M.auc([.1, .2, .8, .9], [1, 1, 0, 0]) == 0.0
    assert M.auc([.5, .5, .5, .5], [1, 0, 1, 0]) == 0.5
    assert M.auc([.9, .8], [1, 1]) is None
    # refer-vs-skip on P_BAD top-1 scores: ok = c3 only
    assert M.top1_auc(P_BAD, GOLD) == pytest.approx(1 / 3)

def test_ece():
    assert M.ece([.9] * 10, [1] * 5 + [0] * 5, bins=10) == pytest.approx(0.4)
    assert M.ece([1.0] * 4, [1, 1, 1, 1], bins=10) == 0.0
    assert M.ece([.5] * 4, [1, 0, 1, 0], bins=10) == pytest.approx(0.0)

def test_length_bias_hub_share_and_stability():
    out = {'a': [('j1', .5)], 'b': [('j1', .6)], 'c': [('j1', .7)], 'd': [('j1', .8)]}
    assert M.length_corr(out, {'a': 100, 'b': 200, 'c': 300, 'd': 400}) == pytest.approx(1.0)
    assert M.length_corr(out, {'a': 400, 'b': 300, 'c': 200, 'd': 100}) == pytest.approx(-1.0)
    assert M.top2_share(P_BAD, n=4) == 1.0
    assert M.top2_share({'a': [('j1', 1)], 'b': [('j2', .9)], 'c': [('j3', .8)], 'd': [('j1', .7)]}, n=4) == pytest.approx(0.75)
    assert M.agreement(P_GOOD, P_BAD) == 0.25 and M.agreement(P_GOOD, P_GOOD) == 1.0

def _many(out, k): return {f'{c}_{i}': v for i in range(k) for c, v in out.items()}
def _many_gold(gold, k): return {(f'{c}_{i}', j): v for i in range(k) for (c, j), v in gold.items()}

def test_paired_bootstrap_decides_with_an_interval():
    gold, a, b = _many_gold(GOLD, 10), _many(P_BAD, 10), _many(P_GOOD, 10)
    r = M.paired_bootstrap(a, b, gold, coverage=1.0, B=400, seed=3)
    assert r['wrong_a'] == 0.75 and r['wrong_b'] == 0.0 and r['rel_reduction'] == 1.0
    assert r['diff_ci'][0] > 0.4 and r['diff_ci'][1] <= 1.0                  # A is clearly worse than B
    assert M.paired_bootstrap(a, b, gold, coverage=1.0, B=400, seed=3) == r   # same seed, same answer
    same = M.paired_bootstrap(a, a, gold, coverage=1.0, B=200, seed=1)
    assert same['diff_mean'] == 0.0 and same['diff_ci'][0] <= 0.0 <= same['diff_ci'][1] and same['rel_reduction'] == 0.0
    adopt = M.adopt_rule(r, critical_a=30, critical_b=0)
    assert adopt['adopt'] is True
    assert M.adopt_rule(same, critical_a=30, critical_b=30)['adopt'] is False                                # no gain
    assert M.adopt_rule(r, critical_a=0, critical_b=5)['adopt'] is False                                     # critical errors rose

def test_adopt_rule_edges_each_condition_matters():
    def res(rel, lo): return {'rel_reduction': rel, 'diff_ci': (lo, lo + 0.2)}
    assert M.adopt_rule(res(0.40, 0.01), 0, 0)['adopt'] is True
    assert M.adopt_rule(res(0.39, 0.01), 0, 0)['adopt'] is False          # below 40% relative
    assert M.adopt_rule(res(0.20, 0.05), 0, 0)['adopt'] is False
    assert M.adopt_rule(res(0.60, 0.00), 0, 0)['adopt'] is False          # interval touches zero
    assert M.adopt_rule(res(0.60, -0.05), 0, 0)['adopt'] is False
    assert M.adopt_rule(res(0.60, 0.05), 3, 3)['adopt'] is True           # equal critical errors is allowed
    assert M.adopt_rule(res(0.60, 0.05), 3, 4)['adopt'] is False          # one more critical error is not
