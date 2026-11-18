"""Synthetic edge-case set tests (P1-2). Written BEFORE src/synth.py. Truth is by construction: an explicit rule oracle (see synth.truth docstring).
The oracle is Claude's design, so agreement with it measures consistency on designed cases, not human truth (tier S)."""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import synth as Y, scrub as S

JD, PR = Y.jds(), Y.profiles()

def test_counts_and_unique_ids():
    assert len(JD) == 14 and len(PR) == 24
    assert len({j['id'] for j in JD}) == 14 and len({p['id'] for p in PR}) == 24
    assert len(Y.all_truth()) == 14 * 24

def test_deterministic():
    assert Y.jd_text(JD[0]) == Y.jd_text(Y.jds()[0]) and Y.cv_text(PR[3]) == Y.cv_text(Y.profiles()[3])

def test_no_personal_data_in_any_text():
    for j in JD: assert S.leaks(Y.jd_text(j)) == [], j['id']
    for p in PR: assert S.leaks(Y.cv_text(p)) == [], p['id']

def test_edge_cases_exist_with_the_right_shape():
    by = {p['id']: p for p in PR}
    assert len(by['stuffer'].get('skills_extra', [])) >= 40 and len(by['stuffer']['skills']) <= 3
    assert len(Y.cv_text(by['short_cv']).split()) < 70
    assert len(Y.cv_text(by['long_cv']).split()) > 1500                      # longer than the 2048-token cap of nomic-embed-text
    assert any(w in Y.cv_text(by['hinglish']) for w in ('kaam', 'sath', 'hai'))
    assert 'EXPERIENCE' not in Y.cv_text(by['projects_only']) and 'PROJECTS' in Y.cv_text(by['projects_only'])
    assert Y.cv_text(by['hopper']).count('2024') + Y.cv_text(by['hopper']).count('2025') >= 4
    boiler = [j for j in JD if j['boilerplate'] >= 3]
    assert len(boiler) == 1 and len(Y.jd_text(boiler[0]).split()) > 250       # the hub JD: mostly boilerplate

def test_jd_states_its_years_and_title():
    for j in JD:
        t = Y.jd_text(j)
        assert j['title'] in t
        if not j.get('degree_or_years'): assert str(j['lo']) in t and 'year' in t.lower(), j['id']
    deg = [j for j in JD if j.get('degree_or_years')][0]
    assert ' or ' in Y.jd_text(deg).lower() and 'degree' in Y.jd_text(deg).lower()

def T(p, j): return Y.truth(next(x for x in PR if x['id'] == p), next(x for x in JD if x['id'] == j))

def test_oracle_known_pairs():
    assert T('ds_4y', 'data_scientist')['final'] == 'REFER'
    assert T('fresher_pm', 'product_manager')['final'] == 'NO' and T('fresher_pm', 'product_manager')['level'] == 'under'
    assert T('stuffer', 'data_scientist')['final'] == 'NO' and T('stuffer', 'data_scientist')['domain'] == 'different'
    assert T('overqualified_ds', 'data_analyst')['final'] == 'NO' and T('overqualified_ds', 'data_analyst')['level'] == 'over'
    assert T('swe_sql', 'fin_systems_analyst')['final'] == 'NO' and T('swe_sql', 'fin_systems_analyst')['domain'] == 'different'   # same words, different job
    assert T('inflated', 'data_scientist')['level'] == 'under' and T('inflated', 'data_scientist')['final'] == 'NO'
    assert T('switcher', 'data_analyst')['final'] == 'HOLD'
    assert T('backend_5y', 'backend_engineer')['final'] == 'REFER' and T('backend_5y', 'backend_engineer')['s5'] == 'SAFE'
    assert T('risk_4y', 'credit_risk')['final'] == 'REFER'
    assert T('ops_1y', 'ops_associate')['final'] == 'REFER'

def test_oracle_rules_hold_for_every_pair():
    for (p, j), t in Y.all_truth().items():
        assert t['final'] in ('REFER', 'STRETCH', 'HOLD', 'NO') and t['s5'] in ('SAFE', 'BORDERLINE', 'DO_NOT_REFER')
        if t['domain'] == 'different' or t['level'] in ('under', 'over'): assert t['final'] == 'NO', (p, j)
        if t['final'] == 'REFER': assert t['s5'] == 'SAFE' and t['domain'] == 'same' and t['level'] == 'at', (p, j)
        if t['final'] in ('REFER', 'STRETCH'): assert t['knockouts'] == 0, (p, j)             # the rubric: ADVANCE needs no required knock-out
        if t['final'] == 'NO': assert t['s5'] == 'DO_NOT_REFER', (p, j)

def test_truth_has_all_four_outcomes_and_enough_hard_negatives():
    c = {}
    for t in Y.all_truth().values(): c[t['final']] = c.get(t['final'], 0) + 1
    assert all(c.get(k, 0) >= 8 for k in ('REFER', 'STRETCH', 'HOLD', 'NO')), c
    hard = [1 for (p, j), t in Y.all_truth().items() if t['final'] == 'NO' and t['listed_overlap'] >= 2]   # the words overlap (listed skills), the truth is still NO
    assert len(hard) >= 15

def test_ambiguous_pairs_are_marked_and_few():
    amb = [k for k, t in Y.all_truth().items() if t['ambiguous']]
    assert 0 < len(amb) <= 0.15 * 14 * 24

def _evidence_lines(text):
    """Lines a recruiter counts as evidence: bullets and project/internship lines, not the SKILLS line, not the summary."""
    out, on = [], False
    for ln in text.split('\n'):
        if ln in ('EXPERIENCE', 'PROJECTS', 'INTERNSHIP', 'EXTRA PROJECTS'): on = True; continue
        if ln.startswith(('SKILLS', 'EDUCATION', 'SUMMARY')): on = False; continue
        if on: out.append(ln)
    return out

def test_every_true_skill_is_shown_in_the_text_except_the_designed_traps():
    for p in PR:
        ev = ' '.join(_evidence_lines(Y.cv_text(p)))
        if p['id'] in ('short_cv', 'inflated'):
            assert not any(s in ev for s in p['skills']), p['id']                       # designed: skills only listed, never shown
        else:
            assert all(s in ev for s in p['skills']), (p['id'], [s for s in p['skills'] if s not in ev])

def test_oracle_counts_a_skill_that_is_only_listed_as_half():
    short = next(p for p in PR if p['id'] == 'short_cv'); da = next(j for j in JD if j['id'] == 'data_analyst')
    t = Y.truth(short, da)
    assert t['coverage'] == 0.25 and t['final'] == 'NO'                                  # SQL, Excel listed only: 2 x 0.5 / 4
    sw = Y.truth(next(p for p in PR if p['id'] == 'switcher'), da)
    assert sw['coverage'] == 0.625 and sw['knockouts'] == 1 and sw['final'] == 'HOLD'     # SQL, Excel shown, dashboards only listed, Tableau missing: (2 + 0.5) / 4

def test_oracle_follows_the_rubric_knockout_rule():
    sre = next(p for p in PR if p['id'] == 'sre_6y'); be = next(j for j in JD if j['id'] == 'backend_engineer')
    t = Y.truth(sre, be)
    assert t['knockouts'] == 2 and t['coverage'] == 0.6 and t['final'] == 'NO'          # REST and SQL missing, so REJECT although coverage is 0.6
    stuffer = next(p for p in PR if p['id'] == 'stuffer'); ops = next(j for j in JD if j['id'] == 'ops_associate')
    t2 = Y.truth(stuffer, ops)
    assert t2['knockouts'] == 2 and t2['final'] == 'NO'                                  # SLA and call quality never appear, not even listed
    ds = next(p for p in PR if p['id'] == 'ds_4y'); dsj = next(j for j in JD if j['id'] == 'data_scientist')
    assert Y.truth(ds, dsj)['knockouts'] == 0
    c = {}
    for t in Y.all_truth().values(): c[t['final']] = c.get(t['final'], 0) + 1
    assert all(c.get(k, 0) >= 8 for k in ('REFER', 'STRETCH', 'HOLD', 'NO')), c


def test_listed_only_skills_are_listed_but_never_shown():
    by = {p['id']: p for p in PR}
    assert 'A/B testing' in by['phd']['listed_only'] and 'A/B testing' not in by['phd']['skills']
    txt = Y.cv_text(by['phd']); ev = ' '.join(_evidence_lines(txt))
    assert 'A/B testing' in txt.split('SKILLS:')[1] and 'A/B testing' not in ev
    assert Y.truth(by['phd'], next(j for j in JD if j['id'] == 'data_scientist'))['final'] == 'STRETCH'      # same words, only listed: half credit, still a stretch candidate
    assert Y.truth(by['ba_3y'], next(j for j in JD if j['id'] == 'product_manager'))['final'] == 'STRETCH'
    assert Y.truth(by['sales_7y'], next(j for j in JD if j['id'] == 'strategy_senior_manager'))['final'] == 'HOLD'
