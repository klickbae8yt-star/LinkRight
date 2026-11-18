import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import cvfamily as C

NOW = 2026.8

def test_intern_title_is_engineer_and_education_dates_are_not_roles():
    t = "Resume Text:\nExperience\nJava Full Stack Developer Intern Dec 2025 – May 2026\nCapgemini\n• built APIs\nEducation\nSRM Institute 2022 – 2026\nB.Tech in Data Science\n"
    r = C.cv_family(t, now=NOW)
    assert r['past_family'] == 'engineer' and r['source'] == 'titles'
    assert r['evidence_titles'] == ['Java Full Stack Developer Intern']
    assert abs(r['last_role_end'] - 2026.33) < 0.1

def test_recent_role_beats_old_role():
    t = "Experience\nData Analyst Jan 2017 – Dec 2019\nAcme\nSoftware Engineer Mar 2023 – Present\nBeta\nEducation\nX 2012 – 2016\n"
    r = C.cv_family(t, now=NOW)
    assert r['past_family'] == 'engineer'
    assert r['probs']['data'] > 0 and r['probs']['engineer'] > r['probs']['data']

def test_summary_votes_when_no_experience():
    t = "Summary\nAI student seeking to work as a Machine Learning or Data Science professional.\nEducation\nB.Tech 2022 – 2026\n"
    r = C.cv_family(t, now=NOW)
    assert r['past_family'] == 'data' and r['source'] == 'headline'

def test_embedding_fallback_then_none():
    t = "Skills\nExcel\n"
    r = C.cv_family(t, now=NOW, emb_probs={'finance_risk': 0.7, 'ops': 0.3})
    assert r['past_family'] == 'finance_risk' and r['source'] == 'embedding'
    assert C.cv_family(t, now=NOW)['past_family'] is None

def test_allowed_families_keep_mixed_titles():
    t = "Experience\nData Engineer Jan 2025 – Present\nA\nSoftware Engineer Jan 2022 – Dec 2024\nB\n"
    r = C.cv_family(t, now=NOW)
    assert set(C.allowed(r, 0.3)) == {'data', 'engineer'}

def test_company_first_layout_takes_title_from_next_line():
    t = "Experience\nTredence Jan 2024 – Present\nSenior Data Analyst\n• built dashboards\nEducation\nX 2016 – 2020\n"
    r = C.cv_family(t, now=NOW)
    assert r['past_family'] == 'data' and r['source'] == 'titles'
    assert r['evidence_titles'] == ['Senior Data Analyst']
