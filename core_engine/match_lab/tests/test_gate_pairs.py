"""Gate pair selection tests (P1-3). Blind ids, stratified, deterministic. Written before src/gate_pairs.py."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import gate_pairs as G, synth as Y

def test_selection_is_stratified_and_blind():
    pairs, key = G.select(seed=11)
    assert len(pairs) == 120 and len({p['pair_id'] for p in pairs}) == 120
    truth = Y.all_truth(); chosen = {(key[p['pair_id']]['profile'], key[p['pair_id']]['jd']) for p in pairs}
    assert all(k in chosen for k, t in truth.items() if t['final'] != 'NO')                                   # all 47 non-NO pairs
    assert all(k in chosen for k, t in truth.items() if t['final'] == 'NO' and t['listed_overlap'] >= 2)       # all hard negatives
    for p in pairs:
        assert set(p) == {'pair_id', 'n', 'jd_text', 'cv_text', 's0'}, p.keys()                              # the judge file carries no truth and no profile name
        assert p['pair_id'].startswith('g') and p['s0']['pass'] is True
    blob = ' '.join(p['pair_id'] for p in pairs)
    assert 'stuffer' not in blob and 'swe_sql' not in blob

def test_deterministic_and_seed_changes_order():
    a, _ = G.select(seed=11); b, _ = G.select(seed=11); c, _ = G.select(seed=12)
    assert [p['pair_id'] for p in a] == [p['pair_id'] for p in b] and [p['cv_text'][:30] for p in a] == [p['cv_text'][:30] for p in b]
    assert [p['jd_text'][:20] + p['cv_text'][:20] for p in a] != [p['jd_text'][:20] + p['cv_text'][:20] for p in c]
