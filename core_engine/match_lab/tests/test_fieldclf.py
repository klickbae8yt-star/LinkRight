import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import fieldclf as F

def test_ets_title_not_ops():
    assert F.weak_family('Campus Graduate Full-Time Senior Associate - 2027 Cybersecurity Analyst, Enterprise Technology Services- New York, NY') == 'engineer'

def test_families():
    assert F.weak_family('Senior Data Scientist') == 'data'
    assert F.weak_family('KYC Analyst - 9 Months Secondment') == 'finance_risk'
    assert F.weak_family('Travel Counselor') == 'sales_travel'
    assert F.weak_family('Executive Assistant') is None
