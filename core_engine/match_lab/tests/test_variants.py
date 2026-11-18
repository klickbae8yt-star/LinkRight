import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import numpy as np
import variants as V

def unit(M): return M / np.linalg.norm(M, axis=1, keepdims=True)

def test_centre_removes_shared_direction():
    A = unit(np.array([[1., .1], [1., -.1]])); B = unit(np.array([[1., .2]]))
    A2, B2 = V.centre(A, B)
    assert np.allclose(np.linalg.norm(A2, axis=1), 1) and A2[0] @ A2[1] < 0     # the two resumes now point apart

def test_csls_pushes_hub_down():
    S = np.array([[.9, .9], [.1, .9], [.1, .9]])
    C = V.csls(S, k=2)
    assert C[0, 0] > C[0, 1]

def test_sinkhorn_respects_caps_and_keeps_preference():
    S = np.tile(np.array([[.9, .5, .4]]), (6, 1))          # everyone prefers job 0
    caps = np.array([1., 3., 2.])
    P = V.sinkhorn_caps(S, caps, T=0.05, iters=200)
    col = P.sum(0)
    assert np.allclose(col, caps, atol=0.05)                 # no job over its cap
    assert np.allclose(P.sum(1), 1, atol=0.05)               # every resume placed once
    assert P[:, 0].sum() < 1.1 and P[:, 1].sum() > 2.9       # the hub is capped

def test_sinkhorn_big_cap_keeps_plain_order():
    S = np.array([[.9, .1], [.2, .8]])
    P = V.sinkhorn_caps(S, np.array([10., 10.]), T=0.05, iters=100)
    assert P[0].argmax() == 0 and P[1].argmax() == 1

def test_field_anchor_moves_toward_field_and_lam0_is_plain():
    cv = unit(np.array([[1., 0., 0.]])); mean = np.zeros(3); field = unit(np.array([[0., 1., 0.]]))[0]
    q0 = V.field_anchor(cv, mean, field, 0.0); q1 = V.field_anchor(cv, mean, field, 0.5); q2 = V.field_anchor(cv, mean, field, 2.0)
    assert np.allclose(q0, cv) and q0[0] @ field < q1[0] @ field < q2[0] @ field

def test_top1_and_distinct_jobs():
    S = np.array([[.9, .1], [.8, .2], [.1, .7]])
    assert V.top1(S).tolist() == [0, 0, 1]
    assert V.concentration(np.array([0, 0, 1, 2]), 3) == (3, 0.75)       # jobs used, top-2 share

def test_eligible_mask_campus_roles_only_for_up_to_one_year():
    jobs = ['Campus Graduate Software Engineer', 'Software Engineer', 'Apprentice - Enterprise Technology Services', 'Summer Internship Program Analyst']
    m = V.eligible_mask(jobs, [0, 1, 2, 5])
    assert m[0].tolist() == [True, True, True, True] and m[1].tolist() == [True, True, True, True]
    assert m[2].tolist() == [False, True, False, False] and m[3].tolist() == [False, True, False, False]

def test_title_bonus_needs_a_specific_shared_word_and_two_years():
    B = V.title_bonus(['Cybersecurity Analyst', 'Data Analyst', None, 'Cybersecurity Analyst'], [3, 3, 3, 1], ['Cybersecurity Engineer', 'Software Engineer II'], 0.01)
    assert B.tolist() == [[0.01, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]   # row 3 has under 2 years, row 2 has no title

def test_neartie_moves_to_a_near_equal_job_only_when_the_best_is_full():
    S = np.array([[0.80, 0.795, 0.70]] * 3); mask = np.ones((3, 3), bool)
    assert sorted(V.neartie(S, mask, delta=0.01, cap=1, seed=0).tolist()) == [0, 0, 1]   # fills job 0, spills one to job 1, the last has no free near job and takes the best
    assert set(V.neartie(S, mask, delta=0.0, cap=1, seed=0).tolist()) == {0}              # no tolerance = plain argmax

def test_masters_mask_needs_a_master_degree_on_the_cv():
    jobs = ['Campus Graduate Masters Full-Time Engineer - 2027', 'Software Engineer', 'Campus Undergraduate Full-Time Engineer - 2027', 'Campus Graduate I Summer Internship Program - 2027 Data Science']
    m = V.masters_mask(jobs, ['B.Tech in CSE. Skills: MS Office, Excel', 'M.Tech in CSE', 'Currently pursuing MBA'])
    assert m[0].tolist() == [False, True, True, False]       # a bachelor's CV is not offered master's programs; "MS Office" is not a degree
    assert m[1].tolist() == [True, True, True, True] and m[2].tolist() == [True, True, True, True]
