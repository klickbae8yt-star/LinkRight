#!/usr/bin/env python3
"""
Google Drive Resume Extractor using Playwright.

Opens each Google Drive resume link, extracts text, appends all results
into a single markdown file (all_resumes.md).

Usage:
    python3 extract_resumes.py [--max N] [--resume] [--retry-failed] [--delay SEC]
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

NAV_TIMEOUT = 45000
EXPORT_TIMEOUT = 20000
RETRY_ATTEMPTS = 3
RETRY_DELAYS = [5, 10, 20]  # seconds between retries


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
            text_parts.append(t)
        for m in re.finditer(r'\[([^\]]*)\]\s*TJ', raw):
            inner = m.group(1)
            for t in re.finditer(r'\(([^)]*)\)', inner):
                t2 = t.group(1)
                t2 = t2.replace('\\n', '\n').replace('\\r', '\r')
                t2 = re.sub(r'\\([0-7]{1,3})', lambda e: chr(int(e.group(1), 8)), t2)
                t2 = t2.replace('\\(', '(').replace('\\)', ')')
                text_parts.append(t2)
    except Exception:
        return ""
    return '\n'.join(text_parts)


def load_candidates() -> list[dict]:
    results = []
    with open(CSV_PATH, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for idx, row in enumerate(reader):
            link = row[9].strip() if len(row) > 9 else ''
            if not link:
                continue
            first = row[1].strip() if len(row) > 1 else ''
            last = row[4].strip() if len(row) > 4 else ''
            name = f"{first} {last}".strip() or f"Candidate_{idx}"
            fid = extract_file_id(link)
            results.append({
                'idx': str(idx),
                'first': first,
                'last': last,
                'name': name,
                'email_1': row[2].strip() if len(row) > 2 else '',
                'contact': row[3].strip() if len(row) > 3 else '',
                'email_2': row[5].strip() if len(row) > 5 else '',
                'organisation': row[6].strip() if len(row) > 6 else '',
                'college': row[7].strip() if len(row) > 7 else '',
                'experience': row[8].strip() if len(row) > 8 else '',
                'resume_link': link,
                'file_id': fid or 'unknown',
                'usp': row[10].strip() if len(row) > 10 else '',
            })
    return results


def make_entry(c: dict, text: str | None) -> str:
    parts = []
    parts.append(f"# Resume #{int(c['idx'])+1}: {c['name']}")
    parts.append("")
    parts.append("## Candidate Details")
    parts.append("")
    parts.append("| Field | Value |")
    parts.append("|-------|-------|")
    parts.append(f"| **Name** | {c['name']} |")
    parts.append(f"| **Email 1** | {c['email_1']} |")
    parts.append(f"| **Email 2** | {c['email_2']} |")
    parts.append(f"| **Contact** | {c['contact']} |")
    parts.append(f"| **Organisation** | {c['organisation']} |")
    parts.append(f"| **College** | {c['college']} |")
    parts.append(f"| **Experience** | {c['experience']} yrs |")
    parts.append(f"| **USP** | {c['usp']} |")
    parts.append(f"| **Resume Link** | {c['resume_link']} |")
    parts.append("")
    parts.append("---")
    parts.append("")
    if text:
        parts.append("## Resume Content")
        parts.append("")
        parts.append(text)
    else:
        parts.append("*Could not extract text from this resume — may require OCR or manual download.*")
    parts.append("")
    parts.append("---")
    parts.append("")
    return '\n'.join(parts)


def extract_text_from_page(page, fid: str) -> str | None:
    # Strategy A: innerText — works for Google Docs, plain pages
    try:
        body = page.locator('body').inner_text(timeout=5000)
        lines = [l.strip() for l in body.split('\n') if l.strip()]
        meaningful = [l for l in lines if len(l) > 20]
        if meaningful and len(meaningful) > 3:
            t = '\n'.join(meaningful)
            if len(t) > 100:
                return t
    except Exception:
        pass

    # Strategy B: Google Docs specific — .kix-lineview spans
    try:
        spans = page.evaluate("""() => {
            const els = document.querySelectorAll('.kix-lineview-text-block span');
            return Array.from(els).map(e => e.innerText).join('\\n');
        }""")
        if spans and len(spans.strip()) > 50:
            return spans.strip()
    except Exception:
        pass

    # Strategy C: Click "Download" in Drive toolbar, capture PDF, parse text
    try:
        download_btn = page.locator('div[aria-label*="Download" i], div[aria-label*="download" i]').first
        if download_btn.is_visible(timeout=3000):
            with page.expect_download(timeout=20000) as download_info:
                download_btn.click()
            download = download_info.value
            pdf_bytes = download.read()
            t = extract_pdf_text(pdf_bytes)
            if t and len(t) > 50:
                return t
    except Exception:
        pass

    # Strategy D: PDF.js viewer — look for text content in embed/iframe
    try:
        text_layers = page.evaluate("""() => {
            const layers = document.querySelectorAll('.textLayer span, [data-text] span, .page span');
            return Array.from(layers).map(e => e.textContent).join(' ');
        }""")
        if text_layers and len(text_layers.strip()) > 100:
            return text_layers.strip()
    except Exception:
        pass

    return None


def try_extract_with_retry(page, fid: str, retries: int = RETRY_ATTEMPTS) -> str | None:
    """Try all extraction strategies with retries."""
    for attempt in range(retries):
        text = None

        # Strategy 1: Try Google Docs export
        try:
            resp = page.goto(
                f"https://docs.google.com/document/d/{fid}/export?format=txt",
                timeout=EXPORT_TIMEOUT,
                wait_until='domcontentloaded'
            )
            if resp and resp.status == 200:
                body_text = page.locator('body').inner_text(timeout=5000)
                if body_text and len(body_text.strip()) > 50:
                    text = body_text.strip()
        except Exception:
            pass

        # Strategy 2: Open in Drive viewer
        if not text:
            try:
                page.goto(
                    f"https://drive.google.com/file/d/{fid}/view",
                    timeout=NAV_TIMEOUT,
                    wait_until='networkidle'
                )
                time.sleep(4)
                text = extract_text_from_page(page, fid)
            except Exception:
                pass

        # Strategy 3: Try raw file page
        if not text:
            try:
                page.goto(
                    f"https://drive.google.com/uc?id={fid}",
                    timeout=NAV_TIMEOUT,
                    wait_until='domcontentloaded'
                )
                time.sleep(3)
                body_text = page.locator('body').inner_text(timeout=5000)
                if body_text and len(body_text.strip()) > 50:
                    text = body_text.strip()
            except Exception:
                pass

        if text:
            return text

        if attempt < retries - 1:
            delay = RETRY_DELAYS[min(attempt, len(RETRY_DELAYS)-1)]
            time.sleep(delay)

    return None


def main():
    parser = argparse.ArgumentParser(description='Extract Google Drive resumes via Playwright')
    parser.add_argument('--max', type=int, default=0, help='Max files to process (0 = all)')
    parser.add_argument('--resume', action='store_true', help='Resume from last progress')
    parser.add_argument('--retry-failed', action='store_true', help='Re-process only previously failed entries')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between files (seconds)')
    parser.add_argument('--headless', action='store_true', help='Run browser headless')
    args = parser.parse_args()

    candidates = load_candidates()
    total = len(candidates)
    print(f"Total candidates with resume links: {total}")

    max_files = args.max if args.max > 0 else total
    delay_sec = args.delay

    # Load progress
    processed = {}
    if (args.resume or args.retry_failed) and os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            processed = json.load(f)
        if args.retry_failed:
            failed_indices = [k for k, v in processed.items() if v == 'failed']
            print(f"Retry mode — re-processing {len(failed_indices)} previously failed entries")
            # Remove failed entries from processed so they get re-run
            for k in failed_indices:
                del processed[k]
        else:
            print(f"Resuming — already processed: {len(processed)}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        ctx_kwargs = {'viewport': {'width': 1280, 'height': 900}}
        if os.path.exists(STATE_FILE):
            ctx_kwargs['storage_state'] = STATE_FILE

        context = browser.new_context(**ctx_kwargs)
        page = context.new_page()

        # Manual Google login if no saved session
        if not os.path.exists(STATE_FILE):
            page.goto('https://drive.google.com', timeout=30000)
            input("\n=== Log into your Google account in the browser window, then press Enter ===\n")
            time.sleep(3)
            context.storage_state(path=STATE_FILE)
            print("✓ Auth state saved — future runs won't need login\n")

        processed_count = 0
        success_count = 0
        fail_count = 0

        # For retry mode, rebuild the output file without failed entries
        if args.retry_failed:
            rebuild_output_file(processed)

        for c in candidates:
            idx_str = c['idx']
            fid = c['file_id']

            if idx_str in processed:
                continue

            if processed_count >= max_files:
                print(f"Reached max files limit ({max_files})")
                break

            processed_count += 1
            print(f"[{processed_count}/{total}] {c['name']}...", end=' ', flush=True)

            text = try_extract_with_retry(page, fid)

            # Build entry and append to single output file
            entry = make_entry(c, text)
            with open(OUTPUT_FILE, 'a') as f:
                f.write(entry + '\n')

            status = "success" if text else "failed"
            processed[idx_str] = status
            if text:
                success_count += 1
                print("✓")
            else:
                fail_count += 1
                print("✗")

            # Save progress after each file
            with open(PROGRESS_FILE, 'w') as f:
                json.dump(processed, f)

            time.sleep(delay_sec)

        print(f"\n{'='*50}")
        print(f"Done! Processed: {processed_count}/{total}")
        print(f"  Successfully extracted: {success_count}")
        print(f"  Failed (no text):       {fail_count}")
        print(f"  Already processed:      {len(processed) - processed_count}")
        print(f"  Output:                 {OUTPUT_FILE}")

        browser.close()


def rebuild_output_file(processed: dict):
    """Remove failed entries from all_resumes.md and keep only successful ones."""
    if not os.path.exists(OUTPUT_FILE):
        return

    with open(OUTPUT_FILE, 'r') as f:
        content = f.read()

    entries = content.split('# Resume #')[1:]
    kept = []
    for e in entries:
        # Extract index from "Resume #N:"
        m = re.match(r'(\d+):', e)
        if m:
            idx = str(int(m.group(1)) - 1)  # Convert to 0-indexed
            if idx in processed and processed[idx] == 'success':
                kept.append(f'# Resume #{e}')

    with open(OUTPUT_FILE, 'w') as f:
        f.write('# All Extracted Resumes\n\n')
        for k in kept:
            f.write(k + '\n')


if __name__ == '__main__':
    main()
