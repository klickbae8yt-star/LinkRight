"""M6: field classifier. Job titles give weak labels (fixed regex); logistic regression on the embedding generalises to CVs and to titles the regex misses."""
import re
import numpy as np

def clean_title(t):
    t = re.sub(r'^(campus|graduate|undergraduate|masters|full-time|summer internship program|internship programme|associate|senior associate|-|\s)+', '', t, flags=re.I)
    t = re.sub(r'\b20\d\d\b', ' ', t)
    t = re.sub(r',?\s*enterprise technology services', ' ', t, flags=re.I)   # the live regex sent these to ops via "service"
    return re.sub(r'\s*[-|(]\s*(?:[A-Z][\w .]+,\s*[A-Z]{2}|uk\b.*|mexico.*|phoenix|sunrise).*$', '', t).strip()

FAM = [('data', r'\b(data scien|data analy|analytics|machine learning|ml\b|ai\b|artificial intelligence|business intelligence|bi\b|statistic|decision scien|data engineer|nlp|deep learning|data governance)'),
       ('engineer', r'\b(software|developer|engineer|sde|full[- ]?stack|backend|front[- ]?end|devops|sre|site reliability|qa\b|programmer|architect|cloud|platform|cyber|security|technology|technical)'),
       ('finance_risk', r'\b(financ|risk|credit|fraud|underwrit|audit|accountant|accounting|treasury|compliance|aml|kyc|actuar|investment|banking|control management|real estate)'),
       ('product', r'\b(product|program manager|project manager|business analyst|scrum|agile|strategy|pmo|digital)'),
       ('sales_travel', r'\b(sales|business development|travel|concierge|counsel|consultant|marketing|acquisition|design)'),
       ('ops', r'\b(operations|customer|support|process|collections|servicing|back office|contact cent|call cent|onboarding|administrat|complaint|dispute|human resources|rewards|colleague)'),
       ('manager', r'\b(manager|director|head of|vice president|vp\b|lead\b|chief)')]

def weak_family(title):
    t = clean_title(title).lower()
    for n, r in FAM:
        if re.search(r, t): return n
    return None

def fit(J_vec, labels, C=4.0):
    from sklearn.linear_model import LogisticRegression
    ok = [i for i, l in enumerate(labels) if l]
    m = LogisticRegression(C=C, max_iter=2000).fit(J_vec[ok], [labels[i] for i in ok]); return m
