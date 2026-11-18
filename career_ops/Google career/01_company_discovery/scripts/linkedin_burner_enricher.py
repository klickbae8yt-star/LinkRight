#!/usr/bin/env python3
"""Rate-limited, India-business-hours-guarded LinkedIn burner profile enricher.

Fetches founder education & career pedigree using a dedicated burner LinkedIn
cookie stored in _secrets/cookies/linkedin_burner.enc.

Safety Guardrails:
  1. Runs ONLY during India business hours (09:30-18:30 IST, Mon-Sat) unless --ignore-hours.
  2. Hard daily quota (default max 15 profiles/day) tracked in _secrets/refreshes/.
  3. Default --limit 2 for safe verification before batching.
  4. Randomized delay (25-55s) between calls.
  5. Immediate circuit-breaker on HTTP 401/403/429/999 -> marks linkedin_burner broken in dashboard.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "_shared" / "scripts" / "auth"))

import vault  # noqa: E402

IST = timezone(timedelta(hours=5, minutes=30))
QUOTA_FILE = vault.REFRESHES_DIR / "linkedin_burner_quota.json"
CACHE_FILE = vault.REFRESHES_DIR / "founder_profiles_cache.json"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)


def is_india_business_hours(now_ist: datetime | None = None) -> tuple[bool, str]:
    now = now_ist or datetime.now(IST)
    if now.weekday() == 6:  # Sunday
        return False, f"Sunday in IST ({now.strftime('%Y-%m-%d %H:%M IST')})"
    minutes = now.hour * 60 + now.minute
    if 9 * 60 + 30 <= minutes <= 18 * 60 + 30:
        return True, now.strftime("%Y-%m-%d %H:%M IST")
    return False, f"Outside 09:30-18:30 IST window ({now.strftime('%H:%M IST')})"


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def check_and_increment_quota(max_daily: int) -> tuple[bool, int]:
    today = datetime.now(IST).date().isoformat()
    quota = _load_json(QUOTA_FILE, {"date": today, "count": 0})
    if quota.get("date") != today:
        quota = {"date": today, "count": 0}
    if quota["count"] >= max_daily:
        return False, quota["count"]
    quota["count"] += 1
    _save_json(QUOTA_FILE, quota)
    return True, quota["count"]


def extract_public_id(linkedin_url: str) -> str:
    m = re.search(r"linkedin\.com/in/([^/?#]+)", linkedin_url or "", re.I)
    return urllib.parse.unquote(m.group(1)).strip("/") if m else ""


def parse_voyager_profile(payload: dict[str, Any], public_id: str) -> dict[str, Any]:
    """Extract headline, summary, educations, and experience from Voyager JSON."""
    included = payload.get("included", [])
    profile_obj: dict[str, Any] = {}
    educations: list[dict[str, Any]] = []
    positions: list[dict[str, Any]] = []

    for item in included:
        t = str(item.get("$type", ""))
        if t.endswith(".Profile") and (item.get("publicIdentifier") == public_id or not profile_obj):
            profile_obj = item
        elif "Education" in t and item.get("schoolName"):
            educations.append({
                "school": item.get("schoolName", ""),
                "degree": item.get("degreeName", ""),
                "field": item.get("fieldOfStudy", ""),
            })
        elif "Position" in t and (item.get("companyName") or item.get("title")):
            positions.append({
                "company": item.get("companyName", ""),
                "title": item.get("title", ""),
                "description": (item.get("description") or "")[:300],
            })

    return {
        "public_id": public_id,
        "full_name": f"{profile_obj.get('firstName', '')} {profile_obj.get('lastName', '')}".strip(),
        "headline": profile_obj.get("headline", ""),
        "summary": (profile_obj.get("summary") or "")[:500],
        "educations": educations,
        "positions": positions,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def fetch_profile(public_id: str) -> dict[str, Any]:
    """Fetch a single profile via LinkedIn Voyager using encrypted burner cookies."""
    bundle = vault.get_cookies("linkedin_burner")
    cookie_header = bundle.get("cookie_header", "")
    extra = bundle.get("extra_headers", {})
    csrf = extra.get("csrf-token") or extra.get("Csrf-Token") or ""
    if not cookie_header or not csrf:
        raise RuntimeError("Missing linkedin_burner cookies or csrf-token. Sign in via http://127.0.0.1:8765")

    url = (
        "https://www.linkedin.com/voyager/api/identity/dash/profiles"
        f"?q=memberIdentity&memberIdentity={urllib.parse.quote(public_id)}"
        "&decorationId=com.linkedin.voyager.dash.deco.identity.profile.FullProfileWithEntities-93"
    )
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.linkedin.normalized+json+2.1",
        "Cookie": cookie_header,
        "csrf-token": csrf,
        "x-restli-protocol-version": "2.0.0",
        "Referer": f"https://www.linkedin.com/in/{public_id}/",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if "checkpoint" in resp.geturl() or "login" in resp.geturl():
                raise PermissionError(f"Redirected to checkpoint/login: {resp.geturl()}")
            payload = json.loads(resp.read().decode("utf-8"))
            return parse_voyager_profile(payload, public_id)
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403, 429, 999):
            vault.report_workflow_status(
                "linkedin_burner",
                "broken",
                f"HTTP {exc.code} from LinkedIn Voyager — re-authenticate burner account",
            )
        raise


def enrich_urls(
    linkedin_urls: list[str],
    limit: int = 2,
    max_daily: int = 15,
    ignore_hours: bool = False,
    min_delay: float = 25.0,
    max_delay: float = 55.0,
) -> dict[str, dict[str, Any]]:
    """Safely enrich up to `limit` uncached founder LinkedIn URLs."""
    cache: dict[str, dict[str, Any]] = _load_json(CACHE_FILE, {})
    results: dict[str, dict[str, Any]] = {}

    ok_hours, hours_msg = is_india_business_hours()
    if not ok_hours and not ignore_hours:
        print(f"[guard] Skipping live LinkedIn calls: {hours_msg}. Pass --ignore-hours for manual 1-2 profile testing.")
        return {extract_public_id(u): cache[extract_public_id(u)] for u in linkedin_urls if extract_public_id(u) in cache}

    fetched_now = 0
    for url in linkedin_urls:
        pid = extract_public_id(url)
        if not pid:
            continue
        if pid in cache:
            results[pid] = cache[pid]
            continue
        if fetched_now >= limit:
            break

        allowed, used = check_and_increment_quota(max_daily)
        if not allowed:
            print(f"[guard] Daily quota reached ({used}/{max_daily}). Stopping cleanly.")
            break

        if fetched_now > 0:
            delay = random.uniform(min_delay, max_delay)
            print(f"[pace] Sleeping {delay:.1f}s before next LinkedIn lookup...")
            time.sleep(delay)

        try:
            prof = fetch_profile(pid)
            cache[pid] = prof
            results[pid] = prof
            _save_json(CACHE_FILE, cache)
            fetched_now += 1
            vault.report_workflow_status("linkedin_burner", "ok", None)
            print(f"[ok] Fetched {pid} ({used}/{max_daily} daily quota)")
        except Exception as exc:
            print(f"[circuit-breaker] Stopped on {pid}: {exc}")
            break

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe rate-limited LinkedIn burner profile enricher")
    parser.add_argument("--url", action="append", default=[], help="Founder LinkedIn URL (repeatable)")
    parser.add_argument("--limit", type=int, default=2, help="Max live lookups this run (default: 2 for safe testing)")
    parser.add_argument("--max-daily", type=int, default=15, help="Hard daily lookup cap (default: 15)")
    parser.add_argument("--ignore-hours", action="store_true", help="Override IST 09:30-18:30 business-hours gate")
    parser.add_argument("--min-delay", type=float, default=25.0)
    parser.add_argument("--max-delay", type=float, default=55.0)
    args = parser.parse_args()

    if not args.url:
        print("Pass at least one --url https://www.linkedin.com/in/<slug>")
        return 1

    out = enrich_urls(
        args.url,
        limit=args.limit,
        max_daily=args.max_daily,
        ignore_hours=args.ignore_hours,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
    )
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

