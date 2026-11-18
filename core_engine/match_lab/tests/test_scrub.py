"""Scrubber tests (P0-2). Written BEFORE src/scrub.py (red first). No real person appears here; every name below is made up.
Run: python3 -m pytest -q tests"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import scrub as S

CV = """Rahul Verma
Software Engineer | Bengaluru, India
Email: rahul.verma92@gmail.com | Phone: +91 98765 43210 | LinkedIn: https://www.linkedin.com/in/rahul-verma-123 | GitHub: github.com/rverma
Date of Birth: 14/03/1994
Gender: Male | Marital Status: Single | Nationality: Indian | Religion: X
Father's Name: Suresh Verma

PROFILE
Backend engineer with 5 years of experience in Node.js, Python and SQL. Reduced API latency by 35%.

EXPERIENCE
Accenture, Software Engineer, Sept 2023 - Present, Hyderabad
Built payment services with Next.js and ASP.NET. CTC 12.5 LPA. CGPA 8.5.
"""

def test_email_removed_all_forms():
    out = S.scrub(CV)
    assert '@' not in out and 'gmail' not in out
    assert '[EMAIL]' in out
    assert '[EMAIL]' in S.scrub('write to a.b@corp.co.in or c_d@x.org')
    assert 'example' not in S.scrub('mail: sam [at] example [dot] com')

def test_phone_removed_but_numbers_that_matter_stay():
    out = S.scrub(CV)
    assert '98765' not in out and '43210' not in out
    for p in ['9876543210', '+1 (415) 555-2671', '(080) 2345 6789', '98765-43210', '+91-98765-43210', '0091 9876543210']:
        assert not any(ch.isdigit() for ch in S.scrub('Call ' + p + ' now').replace('Call', '').replace('now', '')), p
    keep = 'Sept 2023 - Present, 5 years, 35%, 12.5 LPA, CGPA 8.5, 2019-2023, 150000 users, v3.12'
    assert S.scrub(keep) == keep

def test_urls_and_handles_removed_but_tech_names_stay():
    out = S.scrub(CV)
    assert 'linkedin.com' not in out and 'github.com' not in out and 'http' not in out and 'rverma' not in out
    assert 'Node.js' in out and 'Next.js' in out and 'ASP.NET' in out
    assert 'johndoe.dev' not in S.scrub('portfolio: johndoe.dev and www.mysite.in/work')
    assert 'e.g.' in S.scrub('tools, e.g. Docker')

def test_header_name_and_known_names_removed():
    out = S.scrub(CV, known_names=['Rahul Verma'])
    assert 'Rahul' not in out and 'Verma' not in out and 'rverma' not in out.lower()
    out2 = S.scrub('Priya Nair\nData Analyst, 3 years of SQL.\nPriya has led dashboards.')
    assert 'Priya' not in out2 and 'Nair' not in out2
    assert 'Data Analyst' in out2

def test_name_derived_from_email_is_removed_in_text():
    out = S.scrub('Anil Kumar Rao\nmail anil.rao77@mail.com\nProject lead. Anil mentored 4 juniors.')
    assert 'Anil' not in out and 'anil' not in out.lower().replace('mentored', '')

def test_sensitive_lines_removed():
    out = S.scrub(CV)
    for w in ['14/03/1994', 'Male', 'Single', 'Religion', "Father", 'Suresh', 'Marital', 'Nationality', 'Date of Birth']:
        assert w not in out, w

def test_content_kept():
    out = S.scrub(CV, known_names=['Rahul Verma'])
    for w in ['Software Engineer', 'Bengaluru', 'Backend engineer', '5 years', 'Node.js', 'Python', 'SQL', '35%', 'Accenture', 'Sept 2023 - Present', 'Hyderabad', 'CGPA 8.5', '12.5 LPA']:
        assert w in out, w

def test_idempotent_and_leak_check():
    once = S.scrub(CV, known_names=['Rahul Verma'])
    assert S.scrub(once, known_names=['Rahul Verma']) == once
    assert S.leaks(once) == []
    assert S.leaks('mail me at x@y.com') != [] and S.leaks('see https://a.b/c') != [] and S.leaks('call 9876543210') != []

def test_pin_code_and_street_removed_city_kept():
    out = S.scrub('Address: 12 MG Road, Indiranagar, Bengaluru 560038, India\nBased in Pune 411001')
    assert '560038' not in out and '411001' not in out and 'MG Road' not in out
    assert 'Bengaluru' in out or 'Pune' in out

def test_empty_and_odd_input():
    assert S.scrub('') == '' and S.scrub(None) == ''
    assert isinstance(S.scrub('नमस्ते 9876543210'), str) and '9876543210' not in S.scrub('नमस्ते 9876543210')

def test_phone_followed_by_roll_number_is_removed():
    out = S.scrub('Bombay Contact: +91 6386212160 200020034 B.Tech. Email: x')
    assert '6386212160' not in out and '+91' not in out and '200020034' in out and 'B.Tech' in out

def test_pin_after_dash_state_abbreviation_and_spaced_comma():
    for t in ['Portfolio | Noida - 201301 | Software', 'Dabra, MP 475110 | call', 'Tiruvannamalai, India – 606601 | x', 'Madurai , Tamil Nadu , 625704. OBJECTIVE']:
        assert not any(len(m) == 6 for m in __import__('re').findall(r'\d+', S.scrub(t))), t
    assert 'Noida' in S.scrub('Noida - 201301') and S.scrub('150000 users, 2019-2023') == '150000 users, 2019-2023'

def test_location_line_with_street_removed_but_plain_city_line_kept():
    out = S.scrub('Location: 1/41 Near Saloon, T.Pudhupatti, Madurai\nLocation: Noida, Uttar Pradesh, India\nSkills: Java')
    assert 'Saloon' not in out and 'Noida, Uttar Pradesh' in out

def test_leftover_profile_handle_removed():
    assert 'a5a848119' not in S.scrub('LinkedIn- [NAME]-a5a848119/ I am')

def test_name_words_next_to_name_placeholder_in_header_are_removed():
    for t in ['[NAME] Ahmad [NAME]\nChemical Engineering', 'Sai Pradeep [NAME]\nCincinnati, Ohio', '[NAME] SINGH [NAME]\n[PHONE] | [EMAIL]']:
        out = S.scrub(t)
        assert 'Ahmad' not in out and 'Pradeep' not in out and 'SINGH' not in out, out
    assert 'Chemical Engineering' in S.scrub('[NAME] Ahmad [NAME]\nChemical Engineering')

def test_titled_third_party_names_removed():
    out = S.scrub('Selected as an undergraduate TA under Prof.Ankit Jain, for 100+ freshers')
    assert 'Ankit' not in out and '100+ freshers' in out
