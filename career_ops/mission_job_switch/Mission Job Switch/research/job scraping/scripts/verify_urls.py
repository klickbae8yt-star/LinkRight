"""
Verify all career portal URLs are actually reachable in a browser.
Uses curl_cffi (Chrome TLS fingerprint) for proper bot-resistant checking.
Updates jobs.db with url_verified=1 if URL returns HTTP < 400.
"""

import asyncio
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import re

from curl_cffi.requests import AsyncSession

DB_PATH = Path(__file__).parent.parent / "db" / "jobs.db"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136"',
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
}


def add_columns_if_missing(conn):
    cols = {r[1] for r in conn.execute("PRAGMA table_info(companies)")}
    if "url_verified" not in cols:
        conn.execute("ALTER TABLE companies ADD COLUMN url_verified INTEGER DEFAULT 0")
    if "url_status" not in cols:
        conn.execute("ALTER TABLE companies ADD COLUMN url_status INTEGER")
    if "final_url" not in cols:
        conn.execute("ALTER TABLE companies ADD COLUMN final_url TEXT")
    conn.commit()


async def verify_url(session, company, career_url, sem) -> tuple[int, str, str]:
    async with sem:
        if not career_url:
            return 0, "", "no_url"
        try:
            r = await session.get(
                career_url,
                headers=HEADERS,
                timeout=15,
                allow_redirects=True,
                impersonate="chrome136",
            )
            final = str(r.url)
            status = r.status_code

            # Check if final URL looks like a career page (not homepage redirect)
            is_career = any(kw in final.lower() for kw in
                            ["career","job","hire","work","talent","vacancy","position","recruit"])
            # Also accept if original URL had career keyword
            orig_career = any(kw in career_url.lower() for kw in
                               ["career","job","hire","work","talent","vacancy","position","recruit",
                                "greenhouse","lever","ashby","workday","smartrecruiters","workable","eightfold"])

            note = ""
            if status < 400:
                if not (is_career or orig_career):
                    note = f"redirected_to_homepage:{final[:80]}"
            return status, final, note
        except Exception as e:
            return 0, career_url, str(e)[:100]


async def main():
    conn = sqlite3.connect(DB_PATH)
    add_columns_if_missing(conn)

    rows = conn.execute("SELECT company, career_url FROM companies ORDER BY company").fetchall()
    print(f"Verifying {len(rows)} career URLs with Chrome TLS fingerprint...\n")

    sem = asyncio.Semaphore(10)
    async with AsyncSession(impersonate="chrome136") as session:
        tasks = [(company, url, verify_url(session, company, url, sem))
                 for company, url in rows]

        results = await asyncio.gather(*[t[2] for t in tasks])

    ok = 0
    bad_urls = []
    redirected = []

    for (company, career_url), (status, final_url, note) in zip(rows, results):
        url_verified = 1 if (status and status < 400) else 0
        conn.execute("""
            UPDATE companies SET url_verified=?, url_status=?, final_url=?
            WHERE company=?
        """, (url_verified, status, final_url, company))

        symbol = "✓" if url_verified else "✗"
        redirect_note = f" → {final_url[:60]}" if final_url != career_url and final_url else ""
        note_str = f" ⚠ {note}" if note and "redirected" not in note else ""
        print(f"  {symbol} [{status or '---'}] {company:40s}{redirect_note}{note_str}")

        if url_verified:
            ok += 1
            if "redirected_to_homepage" in note:
                redirected.append((company, career_url, final_url))
        else:
            bad_urls.append((company, career_url, status, note))

    conn.commit()

    print(f"\n{'='*70}")
    print(f"✓ Verified reachable: {ok}/300")
    print(f"✗ Unreachable: {300-ok}/300")

    if redirected:
        print(f"\n⚠ Redirected to non-career page ({len(redirected)}) — URL may be wrong:")
        for c, orig, final in redirected:
            print(f"  {c}: {orig}")
            print(f"    → {final}")

    if bad_urls:
        print(f"\n✗ DEAD/BLOCKED URLs ({len(bad_urls)}):")
        for c, url, status, err in bad_urls:
            print(f"  [{status or '---'}] {c}: {url}")
            if err and not err.startswith("redirected"):
                print(f"    error: {err}")

    conn.close()
    return bad_urls


if __name__ == "__main__":
    bad = asyncio.run(main())
    print(f"\nRun agent-browser on {len(bad)} URLs that failed HTTP check.")
