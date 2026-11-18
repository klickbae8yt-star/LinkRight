"""P1-4: run pipelines on the frozen synthetic set; write docs/p1-4_mechanism.md. Gold = constructed truth (Claude agreed on 120 pairs at 0.975)."""
import os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import synth, metrics as M, pipelines as P
from sklearn.linear_model import LogisticRegression

PR, JB = synth.profiles(), synth.jds()
cands, jobs = [p['id'] for p in PR], [j['id'] for j in JB]
cv = [synth.cv_text(p) for p in PR]; jd = [synth.jd_text(j) for j in JB]
gold = synth.all_truth()
lengths = {c: len(t.split()) for c, t in zip(cands, cv)}
cos = lambda a, b: a @ b.T
Q, D = 'search_query: ', 'search_document: '
E = lambda c, j: (P.embed(c), P.embed(j))
C_raw = cos(*E(cv, jd)); C_pre = cos(*E([Q + t for t in cv], [D + t for t in jd]))
cvv, jdv = [P.cv_view(t) for t in cv], [P.jd_view(t) for t in jd]
C_view = cos(*E(cvv, jdv)); C_pv = cos(*E([Q + t for t in cvv], [D + t for t in jdv]))
a, b = E(cv, jd); a2, b2 = a - a.mean(0), b - b.mean(0)
C_cent = cos(a2 / np.linalg.norm(a2, axis=1, keepdims=True), b2 / np.linalg.norm(b2, axis=1, keepdims=True))
B = np.array([P.bm25(P.toks(t), jdv) for t in cvv])
has = lambda s, t: re.search(r'(?<![a-z0-9])' + re.escape(s.lower()) + r'(?![a-z0-9])', t.lower()) is not None
ev = [' '.join(synth.evidence_lines(t)) for t in cv]
cov_str = np.array([[np.mean([has(s, t) for s in j['must']]) for j in JB] for t in cv])
cov_bul = np.array([[np.mean([has(s, e) for s in j['must']]) for j in JB] for e in ev])
yg = np.array([[1.0 if j['lo'] - 1 <= p['years'] <= j['hi'] + 1 else 0.0 for j in JB] for p in PR])
gap = np.array([[np.clip(j['lo'] - p['years'], -3, 3) for j in JB] for p in PR])
tok1 = lambda t: set(P.toks(t.split('\n')[0]))
tsim = np.array([[len(tok1(c) & tok1(j)) / max(len(tok1(c) | tok1(j)), 1) for j in jd] for c in cv])
stuff = np.array([[len(re.findall(r'^SKILLS: (.*)$', c, re.M)[0].split(',')) / 50 if 'SKILLS:' in c else 0 for _ in jd] for c in cv])
words = np.array([[len(c.split()) / 1000 for _ in jd] for c in cv])
skills = sorted({s for j in JB for s in j['must']}); Es = P.embed([Q + s for s in skills]); sidx = {s: i for i, s in enumerate(skills)}
late = np.zeros((len(cv), len(jd)))
for i, p in enumerate(PR):
    lines = synth.evidence_lines(cv[i]) or [cv[i]]; El = P.embed([D + l for l in lines])
    for k, j in enumerate(JB): late[i, k] = np.mean([(El @ Es[sidx[s]]).max() for s in j['must']])
P2 = P.csls(C_pv); P3 = yg * P.rrf([P2, B, cov_bul])
feats = [C_raw, C_pre, C_view, P2, P.zrow(B), cov_str, cov_bul, late, yg, gap / 3, tsim, stuff, words]
X = np.stack([f.reshape(-1) for f in feats], 1); X = (X - X.mean(0)) / (X.std(0) + 1e-9)
y = np.array([gold[(c, j)]['final'] in ('REFER', 'STRETCH') for c in cands for j in jobs]); g = np.repeat(np.arange(len(cands)), len(jobs))
P5 = np.zeros(len(y))
for k in range(len(cands)):
    m = LogisticRegression(C=1.0, class_weight='balanced', max_iter=2000).fit(X[g != k], y[g != k]); P5[g == k] = m.predict_proba(X[g == k])[:, 1]
P5 = P5.reshape(len(cands), len(jobs))
ORA = np.array([[M.gain(gold[(c, j)]) + 0.01 * C_raw[i, k] for k, j in enumerate(jobs)] for i, c in enumerate(cands)])
PIPES = [('P0 today: raw cosine', C_raw), ('P0y raw cosine + years window', C_raw - (1 - yg)), ('H0 prefix only', C_pre), ('H1 strip boilerplate/old roles only', C_view),
         ('H2a CSLS (k=3) on raw', P.csls(C_raw)), ('H2b centred vectors', C_cent), ('H3 BM25 + cosine RRF', P.rrf([C_raw, B])), ('H4 years gate x skill coverage in bullets', yg * cov_bul + 0.1 * C_raw),
         ('H5 late interaction (per must-have)', late), ('H8 cosine + title match', C_raw + 0.5 * tsim), ('P1 = H0+H1', C_pv), ('P2 = P1 + CSLS', P2), ('P3 = P2 + BM25 + coverage + years gate (RRF)', P3),
         ('P5 = learned fusion (leave-one-candidate-out)', P5), ('Ceiling: constructed truth', ORA)]
base = P.to_out(C_raw, cands, jobs); f = lambda v: '-' if v is None else '%.2f' % v
rows = []; crit0 = M.critical_errors(base, gold, 12)
for name, S in PIPES:
    o = P.to_out(S, cands, jobs); r = M.paired_bootstrap(base, o, gold, 0.5, B=1000, seed=1); cr = M.critical_errors(o, gold, 12)
    rows.append('| %s | %s | %s | %s | %d | %s | %s | %s | %s | %s | %s | %s |' % (name, f(M.wrong_rate(o, gold, 8)), f(M.wrong_rate(o, gold, 12)), f(M.unsafe_rate(o, gold, 12)), cr, f(M.mean_precision_at_k(o, gold, 1)), f(M.ndcg_at_k(o, gold, 5)),
        f(M.mrr(o, gold)), f(M.top1_auc(o, gold)), f(M.length_corr(o, lengths)), f(M.top2_share(o, 12)),
        '%+.0f%% [%+.2f,%+.2f] %s' % (100 * r['rel_reduction'], r['diff_ci'][0], r['diff_ci'][1], 'ADOPT' if M.adopt_rule(r, crit0, cr)['adopt'] else 'no')))
head = ('# P1-4 mechanism table (synthetic set, tier S, mechanism only)\n\nSet: %d candidates x %d jobs = %d pairs; gold = constructed truth (Claude agreed on 120 pairs, 0.975). Good pairs (REFER/STRETCH): %d. '
        'Wrong rate = share of referred top-1 picks whose truth is NO. n = number of candidates referred (of %d). Last column: relative drop of wrong rate at n=12 vs P0, 95%% bootstrap interval of the difference, fixed adopt rule.\n\n'
        '| pipeline | wrong n=8 | wrong n=12 | unsafe n=12 | critical n=12 | P@1 | nDCG@5 | MRR | top-1 AUC | len corr | top-2 job share | vs P0 (n=12) |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n') % (len(cands), len(jobs), len(y), y.sum(), len(cands))
tail = ('\n\nNot run (need a model that is not on this box; a pull needs a go): H6 other embedders (mxbai-embed-large, bge-m3), H7 cross-encoder rerank (bge-reranker-v2-m3), P4. '
        'H10 typed checks: Claude is the teacher; its ceiling is the last row. Warning: the generator and the structured features share one vocabulary, so H4/H5/P3/P5 are optimistic here. Adoption needs the real sample.\n')
open(os.path.join(os.path.dirname(__file__), '..', 'docs', 'p1-4_mechanism.md'), 'w').write(head + '\n'.join(rows) + tail); print(head + '\n'.join(rows) + tail)
