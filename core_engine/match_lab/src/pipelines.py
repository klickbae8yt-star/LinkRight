"""P1-4: candidate pipelines P0..P5 and single-factor ablations on the synthetic set. Mechanism only: the generator knows the answer, so structured
features look better here than they will on real CVs. Scores are matrices S[cand_index, job_index]."""
import hashlib, json, math, os, re, urllib.error, urllib.request
import numpy as np

CACHE = os.path.join(os.path.dirname(__file__), '..', 'data', 'emb_cache.json')
ROLE = re.compile(r'^.+, .+, \d{4} - (\d{4}|Present)$')

def embed(texts, model='nomic-embed-text'):
    try: cache = json.load(open(CACHE))
    except Exception: cache = {}
    key = lambda t: hashlib.sha1((model + '|' + t).encode()).hexdigest()
    need = sorted({t for t in texts if key(t) not in cache})
    def call(b):
        req = urllib.request.Request('http://localhost:11434/api/embed', json.dumps({'model': model, 'input': b, 'truncate': True}).encode(), {'Content-Type': 'application/json'})
        return json.load(urllib.request.urlopen(req, timeout=300))['embeddings']
    for t in need:   # one text per call; this Ollama returns 400 past the context, so cut the tail by hand (same effect as the silent tail drop seen on Oracle)
        w = t
        while True:
            try: cache[key(t)] = call([w])[0]; break
            except urllib.error.HTTPError as e:
                if e.code != 400: raise
                w = ' '.join(w.split(' ')[:int(len(w.split(' ')) * 0.85)])
    json.dump(cache, open(CACHE, 'w'))
    m = np.array([cache[key(t)] for t in texts], float)
    return m / np.linalg.norm(m, axis=1, keepdims=True)

def jd_view(jd):
    return '\n'.join(l for l in jd.split('\n') if not l.startswith(('About the company', 'Benefits and equal', 'Role:', 'Location')))

def cv_view(cv):
    out, roles, skip = [], 0, False
    for i, l in enumerate(cv.split('\n')):
        if i == 1 or l.startswith('EDUCATION'): continue
        if l.startswith('SKILLS'): skip = False
        if ROLE.match(l):
            roles += 1; skip = roles > 2
        if l.startswith('EXTRA PROJECTS'): skip = True
        if not skip: out.append(l)
    return '\n'.join(out)

def csls(S, k=3):
    rc = np.sort(S, axis=1)[:, -k:].mean(1, keepdims=True); rj = np.sort(S, axis=0)[-k:, :].mean(0, keepdims=True)
    return 2 * S - rc - rj

def rrf(mats, k=60):
    out = 0
    for M in mats:
        rank = (-M).argsort(1).argsort(1) + 1
        out = out + 1.0 / (k + rank)
    return out

def toks(t): return re.findall(r'[a-z0-9+#/]+', t.lower())

def bm25(query, docs, k1=1.5, b=0.75):
    D = [toks(d) for d in docs]; N = len(D); avg = sum(map(len, D)) / N; s = np.zeros(N)
    for q in set(query):
        df = sum(q in d for d in D); idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
        for i, d in enumerate(D):
            f = d.count(q)
            s[i] += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(d) / avg)) if f else 0
    return s

def zrow(S): return (S - S.mean(1, keepdims=True)) / (S.std(1, keepdims=True) + 1e-9)

def to_out(S, cands, jobs):
    return {c: [(jobs[j], float(S[i, j])) for j in range(len(jobs))] for i, c in enumerate(cands)}
