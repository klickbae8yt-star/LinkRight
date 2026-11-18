"""
analyze_html.py — Extract job card CSS selectors from a saved HTML file.

Use when a portal is not in job_scraper.js built-in configs.

WORKFLOW:
  1. Open the job listing page in browser (search results or company career page)
  2. Ctrl+S (or Cmd+S) → "Web Page, HTML Only" — save the .html file
  3. python3 scripts/analyze_html.py /path/to/saved_page.html
  4. Copy the printed PORTAL_CONFIG block into job_scraper.js CONFIGS dict

The script finds repeated card-like structures and identifies the most likely
selectors for: job cards, title, company, location, URL, date.
"""

import sys
import re
from pathlib import Path
from collections import Counter

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("pip install beautifulsoup4")
    sys.exit(1)


TITLE_SIGNALS    = re.compile(r'title|role|position|job|post', re.I)
COMPANY_SIGNALS  = re.compile(r'company|employer|startup|org|firm', re.I)
LOCATION_SIGNALS = re.compile(r'location|city|place|remote|office|region', re.I)
DATE_SIGNALS     = re.compile(r'date|posted|ago|fresh|time|when', re.I)
URL_SIGNALS      = re.compile(r'job|career|opening|position|role|apply', re.I)


def class_sig(el):
    """Return first meaningful class name of an element."""
    classes = el.get('class', [])
    return classes[0] if classes else ''


def css_sel(el):
    """Generate a CSS selector for an element (tag.firstClass)."""
    cls = class_sig(el)
    if cls:
        safe = cls.replace(':', r'\:').replace('/', r'\/')
        return f"{el.name}.{safe}"
    return el.name


def find_card_candidates(soup):
    """Find elements that repeat 3-80 times — likely job card containers."""
    counter = Counter()
    for el in soup.find_all(True):
        sel = css_sel(el)
        if sel and sel not in ('div', 'span', 'p', 'a', 'li', 'ul', 'ol'):
            counter[sel] += 1

    candidates = [
        (sel, count) for sel, count in counter.most_common(60)
        if 3 <= count <= 80
    ]
    return candidates


def score_card(elements):
    """Score a list of candidate card elements — higher = better job card."""
    if not elements:
        return 0
    score = 0
    sample = elements[:min(5, len(elements))]
    for el in sample:
        text = el.get_text(' ', strip=True)
        if len(text) > 40:  score += 2
        if el.find('a'):    score += 3
        if el.find('h2') or el.find('h3'): score += 2
        if TITLE_SIGNALS.search(str(el.get('class', ''))): score += 2
    return score


def find_selector_for_field(card_samples, signal_re, field_name):
    """Within sample cards, find the most common selector matching a signal."""
    sel_counts = Counter()
    for card in card_samples:
        for el in card.find_all(True):
            cls_str = ' '.join(el.get('class', []))
            if signal_re.search(cls_str) or (el.name in ('h2','h3','h4') and field_name == 'title'):
                sel = css_sel(el)
                text = el.get_text(strip=True)
                if text and len(text) > 2:
                    sel_counts[sel] += 1
    if not sel_counts:
        return None
    return sel_counts.most_common(1)[0][0]


def find_url_selector(card_samples):
    """Find the anchor tag most likely to be the job link."""
    sel_counts = Counter()
    for card in card_samples:
        for a in card.find_all('a', href=True):
            href = a.get('href', '')
            if URL_SIGNALS.search(href) or URL_SIGNALS.search(' '.join(a.get('class', []))):
                sel = css_sel(a)
                sel_counts[sel] += 1
    if sel_counts:
        return sel_counts.most_common(1)[0][0]
    # fallback: any <a>
    return 'a'


def analyze(html_path: str):
    html = Path(html_path).read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(html, 'html.parser')

    hostname = "unknown"
    base_tag = soup.find('base')
    if base_tag and base_tag.get('href'):
        hostname = base_tag['href']
    else:
        title_tag = soup.find('title')
        hostname = title_tag.get_text(strip=True)[:50] if title_tag else Path(html_path).stem

    print(f"\n[analyze_html] Page: {hostname}")
    print(f"[analyze_html] File: {html_path}\n")

    candidates = find_card_candidates(soup)
    if not candidates:
        print("ERROR: No repeated elements found. Is this the jobs listing page?")
        return

    best_sel = None
    best_score = -1
    best_els = []

    for sel, count in candidates:
        try:
            els = soup.select(sel)
        except Exception:
            continue
        score = score_card(els)
        if score > best_score:
            best_score = score
            best_sel = sel
            best_els = els

    if not best_els:
        print("ERROR: Could not identify job card structure.")
        return

    print(f"Best card selector: {best_sel!r}  ({len(best_els)} cards, score={best_score})\n")

    samples = best_els[:10]

    title_sel    = find_selector_for_field(samples, TITLE_SIGNALS,    'title')
    company_sel  = find_selector_for_field(samples, COMPANY_SIGNALS,  'company')
    location_sel = find_selector_for_field(samples, LOCATION_SIGNALS, 'location')
    date_sel     = find_selector_for_field(samples, DATE_SIGNALS,     'date')
    url_sel      = find_url_selector(samples)

    # Print sample values
    print("Sample extractions from first 3 cards:")
    for i, card in enumerate(samples[:3]):
        title_el    = card.select_one(title_sel)    if title_sel    else None
        company_el  = card.select_one(company_sel)  if company_sel  else None
        location_el = card.select_one(location_sel) if location_sel else None
        url_el      = card.select_one(url_sel)      if url_sel      else None
        print(f"  Card {i+1}:")
        print(f"    title:    {title_el.get_text(strip=True)[:60] if title_el else '(not found)'}")
        print(f"    company:  {company_el.get_text(strip=True)[:50] if company_el else '(not found)'}")
        print(f"    location: {location_el.get_text(strip=True)[:40] if location_el else '(not found)'}")
        print(f"    url:      {url_el.get('href','')[:80] if url_el else '(not found)'}")
    print()

    # Generate config block to paste into job_scraper.js
    domain = hostname.replace('"', '').strip()
    print("=" * 60)
    print("COPY THIS INTO job_scraper.js CONFIGS:")
    print("=" * 60)
    print(f"""
    '{domain}': {{
      name: '{domain}',
      jobCards:  ['{best_sel}'],
      title:     ['{title_sel or 'h2,h3'}'],
      company:   ['{company_sel or '[class*="company"]'}'],
      location:  ['{location_sel or '[class*="location"]'}'],
      url:       ['{url_sel or 'a'}'],
      date:      ['{date_sel or 'time'}'],
    }},
""")
    print("=" * 60)
    print("\nIf extractions look wrong above, open the page in browser DevTools")
    print("(F12 → Elements) and manually find the repeating job card element.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        print("Usage: python3 scripts/analyze_html.py /path/to/saved_page.html")
        sys.exit(1)
    analyze(sys.argv[1])
