#!/usr/bin/env python3
"""
Retry failed resume extractions with multiple strategies.
Handles: login page entries, missing entries, expired links.

Usage:
    python3 retry_failed.py [--max N] [--dry-run]
"""

import csv
import json
import os
import re
import sys
import time
import argparse
from playwright.sync_api import sync_playwright

CSV_PATH = '/Users/satvikjain/Downloads/Navii Jobs/#ApplyToAmex - Form Responses 1.csv'
OUTPUT_FILE = '/Users/satvikjain/Downloads/Navii Jobs/all_resumes.md'
PROGRESS_FILE = '/Users/satvikjain/Downloads/Navii Jobs/_extract_progress.json'
STATE_FILE = '/Users/satvikjain/Downloads/Navii Jobs/_auth_state.json'

NAV_TIMEOUT = 60000
EXPORT_TIMEOUT = 30000


def extract_file_id(url: str) -> str | None:
    m = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if m:
        return m.group(1)
    m = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if m:
        return m.group(1)
    return None


def extract_pdf_text(pdf_bytes: bytes) -> str:
    text_parts = []
    try:
        raw = pdf_bytes.decode('latin-1')
        for m in re.finditer(r'\(([^)]*)\)\s*Tj', raw):
            t = m.group(1)
            t = t.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')
            t = re.sub(r'\\([0-7]{1,3})', lambda e: chr(int(e.group(1), 8)), t)
            t = t.replace('\\(', '(').replace('\\)', ')')
            if t.strip():
                text_parts.append(t.strip())
        for m in re.finditer(r'\[(.*?)\]\s*TJ', raw, re.DOTALL):
            inner = m.group(1)
            for sub in re.finditer(r'\(([^)]*)\)', inner):
                t = sub.group(1)
                t = t.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')
                t = re.sub(r'\\([0-7]{1,3})', lambda e: chr(int(e.group(1), 8)), t)
                t = t.replace('\\(', '(').replace('\\)', ')')
                if t.strip():
                    text_parts.append(t.strip())
    except Exception:
        pass
    return '\n'.join(text_parts)


def extract_text_from_page(page) -> str:
    """Extract text from current page using multiple methods."""
    text = ""
    try:
        # Method 1: Get all visible text
        text = page.inner_text('body', timeout=10000)
        text = text.strip()
    except Exception:
        pass

    if not text or len(text.split()) < 20:
        try:
            # Method 2: JavaScript extraction
            text = page.evaluate("""() => {
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                let texts = [];
                let node;
                while (node = walker.nextNode()) {
                    const t = node.textContent.trim();
                    if (t && t.length > 2) texts.push(t);
                }
                return texts.join('\\n');
            }""")
            text = text.strip()
        except Exception:
            pass

    return text


def is_valid_resume(text: str) -> bool:
    """Check if extracted text is actually a resume (not login page)."""
    if not text or len(text.split()) < 30:
        return False
    lower = text.lower()
    bad_indicators = ['login', 'sign in', 'password', 'show password', 'enter your',
                      'create account', 'forgot password', 'google account']
    if any(ind in lower for ind in bad_indicators):
        return False
    return True


def try_direct_open(page, url: str, file_id: str) -> str:
    """Strategy A: Open Google Drive link directly."""
    try:
        page.goto(url, timeout=NAV_TIMEOUT, wait_until='domcontentloaded')
        time.sleep(3)
        return extract_text_from_page(page)
    except Exception as e:
        return ""


def try_export_url(page, file_id: str) -> str:
    """Strategy B: Use Google Drive export URL to get content directly."""
    export_urls = [
        f"https://drive.google.com/uc?export=download&id={file_id}",
        f"https://drive.google.com/uc?export=view&id={file_id}",
        f"https://docs.google.com/document/d/{file_id}/export?format=txt",
    ]
    for url in export_urls:
        try:
            page.goto(url, timeout=EXPORT_TIMEOUT, wait_until='domcontentloaded')
            time.sleep(2)
            text = extract_text_from_page(page)
            if is_valid_resume(text):
                return text
        except Exception:
            continue
    return ""


def try_viewer_url(page, file_id: str) -> str:
    """Strategy C: Use Google Docs viewer."""
    viewer_urls = [
        f"https://drive.google.com/file/d/{file_id}/preview",
        f"https://docs.google.com/viewer?url=https://drive.google.com/uc?export=download%26id={file_id}",
    ]
    for url in viewer_urls:
        try:
            page.goto(url, timeout=NAV_TIMEOUT, wait_until='domcontentloaded')
            time.sleep(3)
            text = extract_text_from_page(page)
            if is_valid_resume(text):
                return text
        except Exception:
            continue
    return ""


def try_pdf_download(page, file_id: str) -> str:
    """Strategy D: Download as PDF and extract text."""
    try:
        pdf_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = page.request.get(pdf_url, timeout=EXPORT_TIMEOUT)
        if response.ok:
            body = response.body()
            if b'%PDF' in body[:100]:
                text = extract_pdf_text(body)
                if is_valid_resume(text):
                    return text
    except Exception:
        pass
    return ""


def get_failed_entries():
    """Get all failed entries from progress file."""
    with open(PROGRESS_FILE) as f:
        prog = json.load(f)

    failed_indices = [k for k, v in prog.items() if v == 'failed']

    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)
        rows = {}
        for i, row in enumerate(reader, 1):
            if str(i) in failed_indices and len(row) > 9 and row[9].strip():
                name = f"{row[1]} {row[4]}".strip()
                link = row[9].strip()
                usp = row[10].strip() if len(row) > 10 else ""
                rows[i] = (name, link, usp)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max', type=int, default=0, help='Max entries to process')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be processed')
    args = parser.parse_args()

    failed = get_failed_entries()
    print(f"Failed entries to retry: {len(failed)}")

    if args.dry_run:
        for idx, (name, link, usp) in list(failed.items())[:10]:
            print(f"  #{idx}: {name}")
        return

    if not os.path.exists(STATE_FILE):
        print(f"ERROR: Auth state file not found: {STATE_FILE}")
        print("Run: python3 login_save.py")
        sys.exit(1)

    # Load existing progress
    with open(PROGRESS_FILE) as f:
        progress = json.load(f)

    # Check which entries already exist in markdown
    with open(OUTPUT_FILE, encoding='utf-8') as f:
        content = f.read()
    existing_indices = set(re.findall(r'# Resume #(\d+):', content))

    # Filter: only process entries not in markdown or with login page content
    to_process = {}
    for idx, (name, link, usp) in failed.items():
        if idx not in existing_indices:
            to_process[idx] = (name, link, usp)
        else:
            # Check if it's a login page entry
            pattern = rf'# Resume #{idx}:.*?(?=# Resume #\d+:|$)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                entry = match.group(0)
                resume_start = entry.find('## Resume Content')
                if resume_start >= 0:
                    resume_text = entry[resume_start+18:].strip()
                    lower = resume_text.lower()
                    if ('login' in lower or 'password' in lower or 
                        'enter your' in lower or 'show password' in lower or
                        len(resume_text.split()) < 30):
                        to_process[idx] = (name, link, usp)

    print(f"Entries to process: {len(to_process)}")
    if not to_process:
        print("Nothing to process!")
        return

    # Sort by index
    sorted_entries = sorted(to_process.items(), key=lambda x: int(x[0]))
    if args.max:
        sorted_entries = sorted_entries[:args.max]

    success = 0
    failed_count = 0
    strategies_used = {'direct': 0, 'export': 0, 'viewer': 0, 'pdf': 0}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=STATE_FILE)
        context.set_default_timeout(NAV_TIMEOUT)
        page = context.new_page()

        for count, (idx, (name, link, usp)) in enumerate(sorted_entries, 1):
            file_id = extract_file_id(link)
            print(f"[{count}/{len(sorted_entries)}] #{idx} {name}...", end=' ', flush=True)

            text = ""
            strategy = ""

            # Strategy A: Direct open
            text = try_direct_open(page, link, file_id)
            if is_valid_resume(text):
                strategy = "direct"
                strategies_used['direct'] += 1
            else:
                # Strategy B: Export URL
                text = try_export_url(page, file_id)
                if is_valid_resume(text):
                    strategy = "export"
                    strategies_used['export'] += 1
                else:
                    # Strategy C: Viewer URL
                    text = try_viewer_url(page, file_id)
                    if is_valid_resume(text):
                        strategy = "viewer"
                        strategies_used['viewer'] += 1
                    else:
                        # Strategy D: PDF download
                        text = try_pdf_download(page, file_id)
                        if is_valid_resume(text):
                            strategy = "pdf"
                            strategies_used['pdf'] += 1

            if is_valid_resume(text):
                # Write to markdown
                entry = f"\n\n# Resume #{idx}: {name}\n\n"
                entry += f"| Field | Value |\n|---|---|\n"
                entry += f"| **Name** | {name} |\n"
                entry += f"| **Drive Link** | {link} |\n"
                entry += f"| **USP** | {usp} |\n"
                entry += f"\n## Resume Content\n\n"
                entry += text[:5000]

                with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                    f.write(entry)

                progress[idx] = 'success'
                success += 1
                print(f"✓ ({strategy})")
            else:
                failed_count += 1
                print(f"✗ (no valid content)")

            # Save progress periodically
            if count % 10 == 0:
                with open(PROGRESS_FILE, 'w') as f:
                    json.dump(progress, f)

        browser.close()

    # Final save
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f)

    print(f"\n{'='*50}")
    print(f"Done! Processed: {len(sorted_entries)}")
    print(f"  Successfully extracted: {success}")
    print(f"  Failed: {failed_count}")
    print(f"  Strategies used: {strategies_used}")
    print(f"  Output: {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
