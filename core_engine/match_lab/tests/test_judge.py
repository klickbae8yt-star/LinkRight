"""Judgement validator tests (P1-3 tooling). Written BEFORE src/judge.py. Rules come from docs/rubric_v1.md sections 3 to 5."""
import copy, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import judge as J

JD = 'Data Scientist\nQualifications: 3 to 5 years of relevant experience. Strong skills in Python, SQL, machine learning.'
CV = 'Data Scientist\nSUMMARY\nData Scientist with 4 years of experience. Built churn models in Python and SQL, improving retention by 12%.\nSKILLS: Python, SQL, machine learning'
def good():
    return {'pair_id': 'p1', 'rubric': 'v1', 'order': 'cv_first', 's0': {'pass': True, 'reasons': []},
            's1': {'title_family': 'match', 'summary': 'specific', 'recent_relevant_role': 'yes', 'readability': 'clear', 'verdict': 'PASS_SKIM', 'feeling': 'Clear data scientist, specific results.', 'quotes': ['Data Scientist with 4 years of experience']},
            's2': {'musts': [{'req': 'Python', 'status': 'MET', 'quote': 'churn models in Python'}, {'req': 'SQL', 'status': 'MET', 'quote': 'Python and SQL'}, {'req': 'machine learning', 'status': 'PARTIAL', 'quote': 'machine learning'}, {'req': 'years', 'status': 'MET', 'quote': '4 years of experience'}],
                   'coverage': 0.875, 'knockouts': 0, 'verdict': 'ADVANCE'},
            's3': {'domain': 'same', 'level': 'at', 'ownership': 'contributed', 'impact': 'quantified', 'depth': 'described', 'stability': 'steady', 'connects': 'Built churn models in Python and SQL.', 'verdict': 'INTERVIEW', 'quotes': ['improving retention by 12%']},
            's4': {'flags': {k: False for k in J.FLAGS}, 'flag_quotes': {}},
            's5': {'verdict': 'SAFE', 'why': 'Clear match, no embarrassing gap.'},
            'final': {'decision': 'REFER', 'confidence': 0.86, 'reasons': ['same domain', 'tools match', 'results shown'], 'risks': ['none seen', 'none seen', 'none seen']}}
def errs(j): return J.validate(j, JD, CV)
def mut(f):
    j = copy.deepcopy(good()); f(j); return errs(j)

def test_good_judgement_is_clean(): assert errs(good()) == []

def test_enums_and_ranges():
    assert any('verdict' in e for e in mut(lambda j: j['s1'].update(verdict='GREAT')))
    assert any('confidence' in e for e in mut(lambda j: j['final'].update(confidence=1.4)))
    assert any('reasons' in e for e in mut(lambda j: j['final'].update(reasons=['a', 'b'])))
    assert any('risks' in e for e in mut(lambda j: j['final'].update(risks=[])))
    assert any('feeling' in e for e in mut(lambda j: j['s1'].update(feeling='word ' * 25)))
    assert any('level' in e for e in mut(lambda j: j['s3'].update(level='huge')))
    assert any('flags' in e for e in mut(lambda j: j['s4']['flags'].pop('keyword_stuffing')))

def test_quotes_must_exist_letter_for_letter():
    assert errs(good()) == []
    assert any('quote' in e for e in mut(lambda j: j['s1'].update(quotes=['Data Scientist with 9 years'])))
    assert any('quote' in e for e in mut(lambda j: j['s2']['musts'][0].update(quote='made up sentence here')))
    assert any('quote' in e for e in mut(lambda j: j['s2']['musts'][0].update(quote='SQL')))                      # shorter than 6 characters
    assert errs(dict(good(), s1=dict(good()['s1'], quotes=['data  scientist   with 4 years of EXPERIENCE']))) == []   # spacing and case are ignored
    assert any('quote' in e for e in mut(lambda j: j['s2']['musts'][1].update(quote='')))                       # MET needs a quote

def test_true_flag_needs_a_quote():
    def f(j): j['s4']['flags']['vague_bullets'] = True
    assert any('flag_quotes' in e for e in mut(f))
    def g(j): j['s4']['flags']['vague_bullets'] = True; j['s4']['flag_quotes'] = {'vague_bullets': 'Built churn models in Python'}; j['s5']['verdict'] = 'SAFE'
    assert not any('flag_quotes' in e for e in mut(g))

def test_coverage_is_recomputed():
    assert any('coverage' in e for e in mut(lambda j: j['s2'].update(coverage=0.2)))
    assert any('knockouts' in e for e in mut(lambda j: j['s2'].update(knockouts=2)))

def test_consistency_rules():
    assert any('REFER' in e for e in mut(lambda j: j['s1'].update(verdict='FAIL_SKIM')))
    assert any('REFER' in e for e in mut(lambda j: j['s2'].update(verdict='HOLD')))
    assert any('REFER' in e for e in mut(lambda j: j['s3'].update(verdict='MAYBE')))
    assert any('REFER' in e for e in mut(lambda j: j['s5'].update(verdict='BORDERLINE')))
    assert any('REFER' in e for e in mut(lambda j: j['s3'].update(level='over')))
    def stretch(j): j['final']['decision'] = 'STRETCH'; j['s3'].update(level='stretch', verdict='MAYBE'); j['s5']['verdict'] = 'BORDERLINE'; j['s2']['verdict'] = 'HOLD'
    assert mut(stretch) == []
    def stretch_bad(j): stretch(j); j['s3']['domain'] = 'different'
    assert any('STRETCH' in e for e in mut(stretch_bad))
    def no_needed(j): j['s5']['verdict'] = 'DO_NOT_REFER'
    assert any('NO' in e for e in mut(no_needed))
    def dnr(j): j['s3'].update(domain='different', verdict='NO'); j['final']['decision'] = 'REFER'
    assert any('NO' in e or 'REFER' in e for e in mut(dnr))
    def sixfive(j): j['s2']['verdict'] = 'REJECT'; j['final']['decision'] = 'NO'
    assert any('DO_NOT_REFER' in e for e in mut(sixfive))        # a screen REJECT forces referrer risk DO_NOT_REFER
    def flags2(j): j['s4']['flags'].update(vague_bullets=True, keyword_stuffing=True); j['s4']['flag_quotes'] = {'vague_bullets': 'Built churn models in Python', 'keyword_stuffing': 'SKILLS: Python, SQL'}
    assert any('SAFE' in e for e in mut(flags2))                  # two or more flags cap referrer risk at BORDERLINE

def test_knockout_fail_forces_no_and_skips_stages():
    j = {'pair_id': 'p2', 'rubric': 'v1', 'order': 'jd_first', 's0': {'pass': False, 'reasons': ['years_window']}, 'final': {'decision': 'NO', 'confidence': 0.99, 'reasons': ['years window', 'x', 'y'], 'risks': ['none seen'] * 3}}
    assert errs(j) == []
    j['final']['decision'] = 'REFER'; assert any('knock' in e.lower() for e in errs(j))

def test_order_alternates_with_pair_number():
    assert J.order_for(1) == 'cv_first' and J.order_for(2) == 'jd_first' and J.order_for(3) == 'cv_first'
    view = J.render(3, 'JOBTEXT', 'CVTEXT', {'pass': True, 'reasons': []})
    assert view.index('CVTEXT') < view.index('JOBTEXT')
    view2 = J.render(2, 'JOBTEXT', 'CVTEXT', {'pass': True, 'reasons': []})
    assert view2.index('JOBTEXT') < view2.index('CVTEXT')

def test_zero_coverage_is_a_valid_number():
    def f(j):
        j['s2'].update(musts=[{'req': 'a', 'status': 'MISSING'}, {'req': 'b', 'status': 'MISSING'}, {'req': 'c', 'status': 'MISSING'}], coverage=0.0, knockouts=3, verdict='REJECT')
        j['s5']['verdict'] = 'DO_NOT_REFER'; j['final']['decision'] = 'NO'; j['s3'].update(verdict='NO')
    assert mut(f) == []

def test_refer_and_safe_need_domain_same():
    assert any('REFER' in e for e in mut(lambda j: j['s3'].update(domain='adjacent')))
    def adj_stretch(j): j['s3'].update(domain='adjacent'); j['s5']['verdict'] = 'BORDERLINE'; j['final']['decision'] = 'STRETCH'
    assert mut(adj_stretch) == []                                   # an adjacent domain is a STRETCH at best
    def adj_safe(j): j['s3'].update(domain='adjacent'); j['final']['decision'] = 'STRETCH'
    assert any('SAFE' in e for e in mut(adj_safe))                  # SAFE with an adjacent domain is not allowed
