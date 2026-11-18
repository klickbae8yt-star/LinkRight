"""P0-4 probe: what does Ollama really do with long inputs for nomic-embed-text, and does the task prefix change the ranking?
Run: python3 src/probes/ollama_probe.py [host]   (default http://127.0.0.1:11434). Read-only: only embeds made-up text. Output: numbers."""
import sys, json, math, random, urllib.request
HOST = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:11434'
def emb(text, **opts):
    body = {'model': 'nomic-embed-text', 'input': text}
    if 'num_ctx' in opts: body['options'] = {'num_ctx': opts['num_ctx']}
    if 'truncate' in opts: body['truncate'] = opts['truncate']
    req = urllib.request.Request(HOST + '/api/embed', json.dumps(body).encode(), {'Content-Type': 'application/json'})
    try: r = json.loads(urllib.request.urlopen(req, timeout=300).read())
    except Exception as e: return ('ERR', str(e)[:160])
    return r['embeddings'][0], r.get('prompt_eval_count')
def cos(a, b):
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(x*x for x in b)); return sum(x*y for x, y in zip(a, b)) / (na * nb)
random.seed(7)
FOOD = 'simmer the tomato sauce with garlic basil olive oil and a pinch of salt then fold the fresh pasta into the pan '.split()
TECH = 'backend engineer designs python services sql databases apis kubernetes latency monitoring payments reliability '.split()
def words(vocab, n): return ' '.join(random.choice(vocab) for _ in range(n))
print('# 1. truncation: embed A(n words of cooking) + B(300 words of backend). Which prefix of the text does the vector equal?')
for ctx in (None, 2048, 8192):
    for n in (1200, 2500, 4500):
        a = words(FOOD, n); b = words(TECH, 300); full = a + ' ' + b
        opts = {} if ctx is None else {'num_ctx': ctx}
        r = emb(full, **opts)
        if r[0] == 'ERR': print(f'ctx={ctx} A={n}w: {r[1]}'); continue
        v, tokens = r
        sims = {k: round(cos(v, emb(' '.join(full.split()[:k]), **opts)[0]), 4) for k in (800, 1400, 1600, 2000, 3000, 4000, 5000) if k <= len(full.split())}
        print(f'ctx={ctx} A={n}w tokens_seen={tokens} cos(full, B_only)={cos(v, emb(b, **opts)[0]):.3f} cos(full, A_only)={cos(v, emb(a, **opts)[0]):.3f} prefix-match={sims}')
print('# 2. does Ollama truncate silently? (truncate=false must error when too long)')
a = words(FOOD, 6000); r = emb(a, truncate=False); print('truncate=false 6000 words ->', r if r[0] == 'ERR' else 'ok tokens=%s' % r[1])
print('# 3. task prefix: toy ranking, 6 jobs vs 4 profiles; count profiles whose true job is ranked first')
JOBS = {'data': 'Data Scientist. Build machine learning models in Python, SQL, statistics, A/B testing, dashboards for business teams.',
        'backend': 'Backend Engineer. Design REST APIs and microservices in Java or Python, databases, queues, latency, on-call.',
        'risk': 'Credit Risk Analyst. Underwrite loans, build scorecards, monitor portfolio delinquency, regulatory reporting.',
        'ops': 'Customer Operations Associate. Handle service tickets, call quality, SLA reports, process improvement.',
        'product': 'Product Manager. Own roadmap, write PRDs, work with engineers and designers, define metrics.',
        'sales': 'Sales Manager. Own regional targets, manage channel partners, close enterprise deals, forecast pipeline.'}
CVS = {'data': 'Analyst with 3 years: trained gradient boosting models, wrote SQL for churn analysis, ran A/B tests, built Tableau dashboards.',
       'backend': 'Software engineer 4 years: built payment microservices in Python, designed REST APIs, tuned Postgres queries, carried on-call.',
       'risk': 'Credit analyst 5 years: designed loan scorecards, tracked delinquency by vintage, prepared RBI reports, underwriting policy.',
       'sales': 'Regional sales lead 6 years: hit annual targets, grew channel partners to 40, closed large enterprise accounts, quarterly forecasts.'}
def rank(prefix_doc, prefix_q):
    J = {k: emb(prefix_doc + v)[0] for k, v in JOBS.items()}; hits = 0; margins = []
    for k, cv in CVS.items():
        q = emb(prefix_q + cv)[0]; s = sorted(((cos(q, J[j]), j) for j in J), reverse=True); hits += s[0][1] == k; margins.append(round(s[0][0] - s[1][0], 4))
    return hits, margins, round(sum(cos(emb(prefix_q + cv)[0], J[k]) for k, cv in CVS.items()) / len(CVS), 4)
print('no prefix            hits/4, top1-top2 margins, mean true cosine:', rank('', ''))
print('search_document/query hits/4, top1-top2 margins, mean true cosine:', rank('search_document: ', 'search_query: '))
print('doc/doc               hits/4, top1-top2 margins, mean true cosine:', rank('search_document: ', 'search_document: '))
print('clustering            hits/4, top1-top2 margins, mean true cosine:', rank('clustering: ', 'clustering: '))
