import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import numpy as np
import pipelines as P

def test_csls_penalises_hub():
    # job 1 is everyone's neighbour (hub); csls must lower it relative to cosine
    S = np.array([[0.9, 0.9], [0.1, 0.9], [0.1, 0.9]])
    C = P.csls(S, k=2)
    assert S[0, 0] == S[0, 1] and C[0, 0] > C[0, 1]

def test_rrf_order():
    a = np.array([[3., 2., 1.]]); b = np.array([[1., 3., 2.]])
    r = P.rrf([a, b])
    assert r[0].argmax() == 1 and r[0].argmin() == 2

def test_bm25_prefers_overlap():
    docs = ['sql excel tableau', 'react html css', 'kubernetes terraform']
    s = P.bm25(['sql', 'tableau'], docs)
    assert s.argmax() == 0 and s[1] == 0

def test_view_cuts_boilerplate_and_old_roles():
    jd = 'T\nAbout the company: x\nRole: y\nResponsibilities:\n- a\nQualifications: q\nBenefits and equal opportunity: z'
    v = P.jd_view(jd)
    assert 'About the company' not in v and 'Benefits' not in v and 'Qualifications' in v
    cv = 'T\nCity\nSUMMARY\ns\nEXPERIENCE\nA, X, 2023 - Present\n- b1\nB, X, 2021 - 2023\n- b2\nC, X, 2019 - 2021\n- b3\nSKILLS: k\nEDUCATION: e'
    w = P.cv_view(cv)
    assert 'b1' in w and 'b2' in w and 'b3' not in w and 'EDUCATION' not in w and 'SKILLS: k' in w
