"""Scrubber (P0-2): removes personal data from a CV text BEFORE any model, log or file reads it.
Removes: emails (also "x [at] y [dot] com"), phone numbers, URLs and profile handles, the candidate's name (from the record, from the e-mail, or the header line),
sensitive lines (date of birth, gender, marital status, nationality, religion, caste, parents' names), street lines and PIN codes.
Keeps: roles, employers, skills, dates, numbers that matter (years, %, CTC, CGPA), cities.
scrub(text, known_names=()) is idempotent. leaks(text) lists what a final check can still find (used by tests and by the export tool)."""
import re

EMAIL = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+')
OBF_EMAIL = re.compile(r'[A-Za-z0-9._%+\-]+\s*[\[(]\s*at\s*[\])]\s*[A-Za-z0-9\-]+(?:\s*[\[(]\s*dot\s*[\])]\s*[A-Za-z0-9\-]+)+', re.I)
URL = re.compile(r'(?:https?://|www\.)[^\s|,;)>\]]+', re.I)
SOCIAL = re.compile(r'\b(?:[a-z]{2,3}\.)?(?:linkedin|github|gitlab|twitter|instagram|facebook|medium|kaggle|behance|leetcode|hackerrank|codeforces|stackoverflow)\.com/[^\s|,;)>\]]*', re.I)
BARE_DOMAIN = re.compile(r'\b[a-z0-9\-]+\.(?:dev|io|in|co|com|net|org|me|app|ai)(?:/[^\s|,;)>\]]*)?(?![\w.])')   # lower case only: keeps Node.js, Next.js, ASP.NET, e.g.
PHONE_TOKEN = re.compile(r'(?<![\w.])[+(]?\d[\d\s().\-]{7,}\d(?![\w%])')
SENSITIVE = re.compile(r"(?i)\b(?:date\s+of\s+birth|d\.o\.b\.?|dob|gender|sex|marital\s+status|nationality|religion|caste|father'?s?\s+name|mother'?s?\s+name|spouse(?:'s)?\s+name)\s*[:\-]\s*[^|;\n]*")
LABEL_AGE = re.compile(r'(?im)^\s*age\s*[:\-]\s*\d+.*$')
ADDRESS_LINE = re.compile(r'(?im)^\s*(?:permanent\s+|current\s+|residential\s+)?address\s*[:\-].*$')
PIN_LABEL = re.compile(r'(?i)\b(?:pin(?:\s*code)?|zip)\s*[:\-]?\s*\d{5,6}\b')
PIN_AFTER_CITY = re.compile(r'\b([A-Za-z]{2,})(?:\s*[,\-\u2013]\s*|\s+)(?:[,\-\u2013]\s*)?[1-8]\d{5}(?!\d)')
LOCATION_STREET = re.compile(r'(?im)^\s*(?:location|place|residence)\s*:[^\n]*(?:\d|\bnear\b)[^\n]*$')
TITLED = re.compile(r'\b(?:Prof|Dr|Mr|Mrs|Ms)\.?\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?')
HANDLE_RESIDUE = re.compile(r'\[NAME\][\-.][a-z0-9]{6,}/?', re.I)
NAME_STOP = {'engineer', 'analyst', 'manager', 'developer', 'scientist', 'data', 'software', 'senior', 'junior', 'lead', 'intern', 'resume', 'curriculum', 'vitae', 'cv', 'profile', 'summary',
             'experience', 'education', 'skills', 'projects', 'objective', 'full', 'stack', 'backend', 'frontend', 'product', 'business', 'associate', 'consultant', 'specialist', 'officer',
             'executive', 'director', 'architect', 'designer', 'administrator', 'technical', 'principal', 'staff', 'head', 'machine', 'learning', 'artificial', 'intelligence', 'cloud', 'devops',
             'quality', 'assurance', 'research', 'operations', 'finance', 'marketing', 'sales', 'support', 'customer', 'service', 'risk', 'credit', 'fraud', 'student', 'fresher', 'graduate'}
EMAIL_STOP = {'info', 'hr', 'contact', 'careers', 'jobs', 'mail', 'admin', 'support', 'team', 'office', 'hello', 'sales', 'gmail', 'yahoo', 'outlook', 'hotmail'}

def _digits(tok): return len(re.sub(r'\D', '', tok))

def _phone_sub(text):
    def f(m):
        tok = m.group(0); groups = re.findall(r'\d+', tok)
        if all(len(g) == 4 and g[:2] in ('19', '20') for g in groups): return tok   # a run of years, not a phone
        if _digits(tok) > 15:   # a phone glued to another number (roll no., id): cut out the phone part only
            return re.sub(r'(?<!\d)(\+?\d{1,3}[\s-]?)?[6-9]\d{9}(?!\d)', '[PHONE]', tok, count=1)
        return '[PHONE]' if 10 <= _digits(tok) <= 15 else tok
    return PHONE_TOKEN.sub(f, text)

def _name_tokens(names):
    out = set()
    for n in names or []:
        for t in re.split(r'[^A-Za-z]+', str(n)):
            if len(t) >= 3 and t.lower() not in NAME_STOP: out.add(t)
    return out

def _header_name(text):
    for ln in text.split('\n')[:3]:
        s = ln.strip()
        if not s: continue
        toks = s.split()
        if 2 <= len(toks) <= 4 and len(s) <= 40 and not re.search(r'[\d@,|:/]', s) and all(re.fullmatch(r"[A-Z][A-Za-z.'\-]*|[A-Z]\.", t) for t in toks) and not any(t.lower().strip('.') in NAME_STOP for t in toks):
            return s
        return None
    return None

def _name_neighbours(t):
    """A header line that holds [NAME] plus only capitalised words (a middle or last name the record did not give us) becomes just [NAME]."""
    out = []
    for i, ln in enumerate(t.split('\n')):
        rest = [x for x in ln.split() if x != '[NAME]']
        if i < 4 and '[NAME]' in ln and rest and len(ln) <= 40 and all(re.fullmatch(r"[A-Z][A-Za-z.'\-]*", x) for x in rest) and not any(x.lower().strip('.') in NAME_STOP for x in rest): ln = '[NAME]'
        out.append(ln)
    return '\n'.join(out)

def scrub(text, known_names=()):
    if not text: return ''
    t = str(text)
    names = list(known_names or [])
    hn = _header_name(t)
    if hn:
        names.append(hn); t = t.replace(hn, '[NAME]', 1)
    emails = EMAIL.findall(t) + OBF_EMAIL.findall(t)
    for e in emails:
        local = re.split(r'[\s\[(@]', e)[0]
        names += [x for x in re.split(r'[._\-\d+%]+', local) if len(x) >= 3 and x.lower() not in EMAIL_STOP]
    t = OBF_EMAIL.sub('[EMAIL]', t); t = EMAIL.sub('[EMAIL]', t)
    t = URL.sub('[URL]', t); t = SOCIAL.sub('[URL]', t); t = BARE_DOMAIN.sub('[URL]', t)
    t = SENSITIVE.sub('', t); t = LABEL_AGE.sub('', t); t = ADDRESS_LINE.sub('', t)
    t = PIN_LABEL.sub('', t); t = PIN_AFTER_CITY.sub(r'\1', t); t = LOCATION_STREET.sub('', t); t = HANDLE_RESIDUE.sub('[URL]', t); t = TITLED.sub('[NAME]', t)
    t = _phone_sub(t)
    for tok in sorted(_name_tokens(names), key=len, reverse=True):
        t = re.sub(r"(?i)\b" + re.escape(tok) + r"(?:'s)?\b", '[NAME]', t)
    t = re.sub(r'(?:\[NAME\][ \t]*){2,}', '[NAME] ', t)
    t = _name_neighbours(t)
    t = re.sub(r'[ \t]*\|[ \t]*(?:\|[ \t]*)+', ' | ', t); t = re.sub(r'(?m)^[ \t]*\|[ \t]*|[ \t]*\|[ \t]*$', '', t)
    t = re.sub(r'(?m)[ \t]+$', '', t); t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip('\n') if t.strip() else ''

def leaks(text):
    t = str(text or ''); out = []
    if EMAIL.search(t) or OBF_EMAIL.search(t): out.append('email')
    if URL.search(t) or SOCIAL.search(t) or BARE_DOMAIN.search(t): out.append('url')
    if any(10 <= _digits(m.group(0)) <= 15 and not all(len(g) == 4 and g[:2] in ('19', '20') for g in re.findall(r'\d+', m.group(0))) for m in PHONE_TOKEN.finditer(t)): out.append('phone')
    return out
