"""Synthetic edge-case set (P1-2): 14 JDs x 24 CV profiles with truth BY CONSTRUCTION. Deterministic, no personal data, made-up companies.
Truth oracle (truth()): domain = same / adjacent / different from the family table; level from years vs the JD range [lo, hi]:
  under if lo - years > 1, stretch if 0 < lo - years <= 1, at if years <= hi + 1, over if years >= hi + 2; coverage = (must-haves shown in bullets or projects + 0.5 x must-haves only listed in the SKILLS line, extras included) / number of must-haves, read from the CV text itself.
  final: domain different, level under or over -> NO. Two or more must-haves with no trace at all (not shown, not even listed) -> NO (rubric: two required knock-outs = REJECT). Same domain: coverage < 0.4 -> NO; coverage >= 0.7, no knock-out and no red flag: level at -> REFER, level stretch -> STRETCH; else HOLD.
  Adjacent domain: coverage >= 0.6, no knock-out, level at or stretch, no flag -> STRETCH; coverage >= 0.4 -> HOLD; else NO. s5: REFER -> SAFE, STRETCH/HOLD -> BORDERLINE, NO -> DO_NOT_REFER.
  ambiguous = decided by coverage within 0.05 of 0.4, 0.6 or 0.7. The oracle is Claude's design: it measures consistency on designed cases, not human truth (tier S)."""
import random

ADJ = {frozenset(p) for p in [('data', 'engineer'), ('data', 'finance_risk'), ('data', 'product'), ('engineer', 'product'), ('finance_risk', 'ops'), ('finance_risk', 'product'),
                              ('product', 'ops'), ('product', 'strategy'), ('sales', 'strategy'), ('sales', 'ops')]}
_J = [  # id, title, family, lo, hi, must, extra flags
 ('data_scientist', 'Data Scientist', 'data', 3, 5, ['Python', 'SQL', 'machine learning', 'A/B testing', 'statistics']),
 ('data_analyst', 'Data Analyst', 'data', 0, 2, ['SQL', 'Excel', 'Tableau', 'dashboards']),
 ('hub_analyst', 'Analyst - Corporate Functions', 'data', 1, 3, ['SQL', 'Excel', 'reporting']),
 ('backend_engineer', 'Backend Engineer', 'engineer', 3, 6, ['Python', 'REST', 'microservices', 'SQL', 'AWS']),
 ('frontend_engineer', 'Frontend Engineer', 'engineer', 2, 4, ['React', 'TypeScript', 'HTML/CSS']),
 ('sre', 'Site Reliability Engineer', 'engineer', 4, 7, ['Kubernetes', 'Terraform', 'CI/CD', 'AWS', 'monitoring']),
 ('credit_risk', 'Credit Risk Analyst', 'finance_risk', 2, 5, ['scorecards', 'SQL', 'SAS', 'underwriting', 'regulatory reporting']),
 ('fraud_analyst', 'Fraud Analyst', 'finance_risk', 1, 3, ['rules', 'SQL', 'investigations', 'transaction monitoring']),
 ('fin_systems_analyst', 'Financial Systems Analyst', 'finance_risk', 3, 5, ['SQL', 'reporting', 'ERP', 'general ledger']),
 ('product_manager', 'Product Manager', 'product', 4, 8, ['roadmap', 'PRDs', 'stakeholders', 'metrics', 'A/B testing']),
 ('business_analyst', 'Business Analyst', 'product', 2, 5, ['requirements', 'SQL', 'process mapping', 'UAT']),
 ('ops_associate', 'Customer Operations Associate', 'ops', 0, 2, ['service tickets', 'SLA', 'call quality']),
 ('sales_manager', 'Sales Manager', 'sales', 5, 9, ['targets', 'channel partners', 'enterprise deals', 'forecasting']),
 ('strategy_senior_manager', 'Senior Manager - Strategic Planning', 'strategy', 3, 8, ['strategic planning', 'project management', 'stakeholders', 'budgeting'])]
_P = [  # id, title, family, years, true skills, kind, flags, style, extra
 ('ds_4y', 'Data Scientist', 'data', 4, ['Python', 'SQL', 'machine learning', 'A/B testing', 'statistics', 'scorecards', 'SAS', 'Tableau'], 'specific', [], 'normal'),
 ('fresher_da', 'Data Analyst (fresher)', 'data', 0, ['SQL', 'Excel', 'Tableau', 'dashboards'], 'specific', [], 'projects'),
 ('backend_5y', 'Backend Engineer', 'engineer', 5, ['Python', 'REST', 'microservices', 'SQL', 'AWS', 'CI/CD', 'Docker'], 'specific', [], 'normal'),
 ('frontend_3y', 'Frontend Engineer', 'engineer', 3, ['React', 'TypeScript', 'HTML/CSS', 'REST'], 'specific', [], 'normal'),
 ('sre_6y', 'Site Reliability Engineer', 'engineer', 6, ['Kubernetes', 'Terraform', 'CI/CD', 'AWS', 'monitoring', 'Python', 'microservices'], 'specific', [], 'normal'),
 ('risk_4y', 'Credit Risk Analyst', 'finance_risk', 4, ['scorecards', 'SQL', 'SAS', 'underwriting', 'regulatory reporting', 'Python', 'statistics', 'rules'], 'specific', [], 'normal'),
 ('fraud_2y', 'Fraud Analyst', 'finance_risk', 2, ['rules', 'SQL', 'investigations', 'transaction monitoring', 'Excel', 'dashboards', 'SAS', 'regulatory reporting'], 'specific', [], 'normal'),
 ('fin_sys_4y', 'Financial Systems Analyst', 'finance_risk', 4, ['SQL', 'reporting', 'ERP', 'general ledger', 'requirements', 'process mapping', 'UAT', 'regulatory reporting'], 'specific', [], 'normal'),
 ('pm_6y', 'Product Manager', 'product', 6, ['roadmap', 'PRDs', 'stakeholders', 'metrics', 'A/B testing', 'requirements', 'SQL', 'process mapping', 'UAT'], 'specific', [], 'normal'),
 ('ba_3y', 'Business Analyst', 'product', 3, ['requirements', 'SQL', 'process mapping', 'UAT', 'PRDs', 'stakeholders', 'metrics', 'roadmap', 'Excel', 'dashboards'], 'specific', [], 'normal'),
 ('ops_1y', 'Customer Operations Associate', 'ops', 1, ['service tickets', 'SLA', 'call quality', 'Excel'], 'specific', [], 'normal'),
 ('sales_7y', 'Regional Sales Manager', 'sales', 7, ['targets', 'channel partners', 'enterprise deals', 'forecasting', 'stakeholders', 'budgeting'], 'specific', [], 'normal'),
 ('switcher', 'Junior Analyst (career switcher from sales)', 'data', 1, ['SQL', 'Excel'], 'generic', [], 'normal'),
 ('stuffer', 'Customer Support Executive', 'ops', 1, ['service tickets', 'Excel'], 'generic', ['keyword_stuffing'], 'stuffed'),
 ('long_cv', 'Principal Backend Engineer', 'engineer', 12, ['Python', 'REST', 'microservices', 'SQL', 'AWS', 'Java', 'Kubernetes', 'CI/CD'], 'specific', [], 'long'),
 ('short_cv', 'Data Analyst', 'data', 1, ['SQL', 'Excel'], 'missing', [], 'short'),
 ('swe_sql', 'Software Engineer (banking systems)', 'engineer', 5, ['Python', 'SQL', 'reporting', 'REST', 'AWS'], 'specific', [], 'normal'),
 ('overqualified_ds', 'Lead Data Scientist', 'data', 12, ['Python', 'SQL', 'machine learning', 'A/B testing', 'statistics', 'Tableau', 'Excel', 'dashboards'], 'specific', ['over_qualified'], 'normal'),
 ('fresher_pm', 'Associate Product Manager (fresher)', 'product', 0, ['roadmap', 'metrics'], 'generic', [], 'projects'),
 ('inflated', 'Senior Data Scientist', 'data', 1.5, ['Excel', 'SQL', 'dashboards'], 'generic', ['inflated_title'], 'normal'),
 ('hinglish', 'Backend Developer', 'engineer', 3, ['Python', 'REST', 'microservices', 'SQL', 'AWS'], 'specific', [], 'hinglish'),
 ('hopper', 'Data Analyst', 'data', 3, ['SQL', 'Excel', 'Tableau', 'dashboards'], 'specific', ['job_hopping'], 'hopper'),
 ('phd', 'Research Scientist (PhD, academia)', 'data', 2, ['Python', 'machine learning', 'statistics', 'SQL', 'experiment design'], 'specific', [], 'normal'),
 ('projects_only', 'Frontend Developer (projects, 1 internship)', 'engineer', 1, ['React', 'TypeScript', 'HTML/CSS'], 'specific', [], 'projects')]
FIRMS = ['Northwind Analytics', 'Contoso Bank', 'Fabrikam Labs', 'Tailspin Systems', 'Litware Finance', 'Adventure Works Retail', 'Wingtip Payments', 'Proseware Cloud', 'Lucerne Insurance', 'Margie Logistics']
EXTRA_KW = ('Python Java C++ Go Rust Scala R MATLAB SQL NoSQL MongoDB Kafka Spark Hadoop Airflow Docker Kubernetes Terraform AWS Azure GCP TensorFlow PyTorch scikit-learn NLP '
            'computer vision LLM prompt engineering Power BI Tableau Looker Excel VBA SAP Salesforce Jira Agile Scrum DevOps CI/CD Linux Git React Node.js').split()
BOILER_INTRO = ('About the company: we are a global financial services firm. We serve millions of customers in over 100 countries. Our people are our strength. We value integrity, '
                'curiosity and teamwork, and we work in an open and inclusive culture where everyone can grow.')
BOILER_END = ('Benefits and equal opportunity: we offer health cover, flexible hours, learning budgets and paid leave. We are an equal opportunity employer. All qualified applicants receive '
              'consideration without regard to race, colour, religion, gender, age, disability or any other protected status. Apply now and grow with us.')
DOMAIN_WORDS = {'data': 'data and analytics', 'engineer': 'software engineering', 'finance_risk': 'credit, fraud and financial systems', 'product': 'product and business analysis',
                'ops': 'customer operations', 'sales': 'sales and channel management', 'strategy': 'strategy and planning'}
TASKS = ['analyse', 'automate', 'monitor', 'improve', 'design', 'ship', 'review', 'forecast']
CONTEXT = ['a retail portfolio', 'the payments team', 'a customer-facing product', 'quarterly planning', 'the operations floor', 'a cloud migration', 'regional targets', 'the risk committee']
METRIC = ['turnaround time', 'accuracy', 'conversion', 'cost per case', 'uptime', 'revenue', 'defect rate', 'customer satisfaction']
VAGUE = ['Responsible for various tasks assigned by the manager', 'Worked on multiple projects with the team', 'Handled day to day activities', 'Involved in different kinds of work as needed']

def jds():
    return [{'id': i, 'title': t, 'family': f, 'lo': lo, 'hi': hi, 'must': m, 'boilerplate': 3 if i == 'hub_analyst' else 1, 'degree_or_years': i == 'strategy_senior_manager'} for i, t, f, lo, hi, m in _J]

LISTED = {'ds_4y': ['underwriting', 'Tableau'], 'ba_3y': ['A/B testing', 'Tableau'], 'phd': ['A/B testing'], 'fraud_2y': ['Tableau'], 'fin_sys_4y': ['Excel'],
          'risk_4y': ['machine learning', 'investigations'], 'switcher': ['dashboards'], 'sales_7y': ['project management'], 'pm_6y': ['strategic planning', 'project management', 'budgeting']}   # skills that appear ONLY in the SKILLS line (claimed, never shown)

def profiles():
    out = []
    for i, t, f, y, s, k, fl, st in _P:
        lo = LISTED.get(i, [])
        out.append({'id': i, 'title': t, 'family': f, 'years': y, 'skills': [x for x in s if x not in lo], 'listed_only': lo, 'summary': k, 'flags': fl, 'style': st, 'skills_extra': EXTRA_KW[:45] if st == 'stuffed' else []})
    return out

def jd_text(j):
    r = random.Random('jd' + j['id']); resp = []
    for s in j['must'][:4]: resp.append('- %s %s for %s and report on %s.' % (r.choice(TASKS).capitalize(), s, r.choice(CONTEXT), r.choice(METRIC)))
    if j['degree_or_years']: need = "Qualifications: Bachelor's or Master's degree, or %d+ years of related work experience leading project teams. Strong skills in %s." % (j['lo'], ', '.join(j['must']))
    else: need = 'Qualifications: %d to %d years of relevant experience. Strong skills in %s.' % (j['lo'], j['hi'], ', '.join(j['must']))
    if j['boilerplate'] >= 3: resp = resp[:1]
    parts = [j['title'], 'Location: India (hybrid)'] + [BOILER_INTRO] * j['boilerplate'] + ['Role: you will work in %s and partner with several teams.' % DOMAIN_WORDS[j['family']], 'Responsibilities:'] + resp + [need] + [BOILER_END] * j['boilerplate']
    return '\n'.join(parts)

def _bullet(r, skill, vague=False, i=0):
    if vague: return '- ' + VAGUE[i % len(VAGUE)]
    return '- Used %s to %s %s, improving %s by %d%%.' % (skill, r.choice(TASKS), r.choice(CONTEXT), r.choice(METRIC), r.randint(8, 45))

def cv_text(p):
    r = random.Random('cv' + p['id']); st = p['style']; sk = p['skills']; yrs = p['years']
    head = [p['title'], 'Bengaluru, India']
    if st == 'short': return '\n'.join(head + ['Skills: ' + ', '.join(sk), 'B.Com, 2024'])
    summ = {'specific': ['SUMMARY', '%s with %s years of experience in %s. Strong in %s.' % (p['title'], ('%g' % yrs), DOMAIN_WORDS[p['family']], ', '.join(sk[:3]))],
            'generic': ['SUMMARY', 'Passionate and hardworking team player with excellent communication skills seeking a challenging opportunity to grow.'], 'missing': []}[p['summary']]
    out = head + summ
    if st == 'projects':
        out += ['PROJECTS'] + ['%s: built a small project using %s with %d users in college.' % (['Portfolio app', 'Dashboard', 'Course tracker', 'Notes tool'][i], sk[i], r.randint(20, 400)) for i in range(min(len(sk), 4))]
        if p['id'] == 'projects_only': out += ['INTERNSHIP', 'Frontend intern, %s, 6 months: used React and TypeScript to ship 4 screens with HTML/CSS, improving defect rate by 20%%.' % FIRMS[0]]
    else:
        nroles = {'long': 6, 'hopper': 5, 'hinglish': 2}.get(st, 2 if yrs >= 2 else 1); vague = p['id'] == 'inflated'
        out.append('EXPERIENCE'); year = 2025
        for k in range(nroles):
            span = 0.5 if st == 'hopper' else max(yrs / nroles, 0.8); start = year - span
            out.append('%s, %s, %.0f - %s' % (p['title'] if k == 0 else p['title'].replace('Principal ', 'Senior '), r.choice(FIRMS), start, 'Present' if k == 0 else '%.0f' % year))
            nb = 5 if st == 'long' else max(3, -(-len(sk) // nroles))
            out += [_bullet(r, sk[(k * nb + b) % len(sk)], vague, k + b) for b in range(nb)]
            if st == 'hinglish' and k == 0: out.append('- Team ke sath kaam kiya aur production issues ko fix karne ka kaam kiya, sab kuch time par hai.')
            year = start - (1.5 if p['id'] == 'hopper' and k == 2 else 0)
        if st == 'long': out += ['EXTRA PROJECTS'] + [_bullet(r, sk[i % len(sk)]) for i in range(100)]
    out.append('SKILLS: ' + ', '.join(sk + p.get('listed_only', []) + p['skills_extra'])); out.append('EDUCATION: B.Tech / B.Com, %d' % (2025 - int(yrs) - 3 - (r.randint(0, 1))))
    return '\n'.join(out)

def evidence_lines(text):
    out, on = [], False
    for ln in text.split('\n'):
        if ln in ('EXPERIENCE', 'PROJECTS', 'INTERNSHIP', 'EXTRA PROJECTS'): on = True; continue
        if ln.startswith(('SKILLS', 'EDUCATION', 'SUMMARY')): on = False; continue
        if on: out.append(ln)
    return out

def _domain(pf, jf): return 'same' if pf == jf else ('adjacent' if frozenset((pf, jf)) in ADJ else 'different')
def _level(y, lo, hi):
    if lo - y > 1: return 'under'
    if 0 < lo - y <= 1: return 'stretch'
    return 'at' if y <= hi + 1 else 'over'

def truth(p, j):
    dom, lvl = _domain(p['family'], j['family']), _level(p['years'], j['lo'], j['hi'])
    ev = ' '.join(evidence_lines(cv_text(p))); listed = set(p['skills']) | set(p.get('listed_only', [])) | set(p.get('skills_extra', []))
    shown = [s for s in j['must'] if s in p['skills'] and s in ev]; listed_only = [s for s in j['must'] if s in listed and s not in shown]; missing = [s for s in j['must'] if s not in listed]
    shared = [s for s in j['must'] if s in p['skills']]; cov = (len(shown) + 0.5 * len(listed_only)) / len(j['must']); ko = len(missing); flags = list(p['flags'])
    if dom == 'different' or lvl in ('under', 'over') or ko >= 2: fin = 'NO'
    elif dom == 'same':
        if cov < 0.4: fin = 'NO'
        elif cov >= 0.7 and ko == 0 and not flags: fin = 'REFER' if lvl == 'at' else 'STRETCH'
        else: fin = 'HOLD'
    else:
        if cov >= 0.6 and ko == 0 and not flags: fin = 'STRETCH'
        elif cov >= 0.4: fin = 'HOLD'
        else: fin = 'NO'
    amb = fin != 'NO' or (dom != 'different' and lvl in ('at', 'stretch')); amb = amb and any(abs(cov - t) <= 0.05 for t in (0.4, 0.6, 0.7)) and dom != 'different' and lvl in ('at', 'stretch')
    listed = set(p['skills']) | set(p.get('listed_only', [])) | set(p.get('skills_extra', []))
    return {'listed_overlap': len([s for s in j['must'] if s in listed]), 'domain': dom, 'level': lvl, 'coverage': round(cov, 3), 'flags': flags, 'final': fin, 's5': {'REFER': 'SAFE', 'STRETCH': 'BORDERLINE', 'HOLD': 'BORDERLINE', 'NO': 'DO_NOT_REFER'}[fin],
            'ambiguous': amb, 'shared_skills': len(shared), 'knockouts': ko}

def all_truth():
    return {(p['id'], j['id']): truth(p, j) for p in profiles() for j in jds()}
