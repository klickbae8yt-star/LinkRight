#!/usr/bin/env python3
"""Encrypted secrets, credentials, and session cookie vault.

Stores encrypted payloads under _secrets/ using OpenSSL AES-256-CBC (PBKDF2),
while keeping non-secret health metadata in _secrets/registry.json for the
localhost dashboard and workflow monitors.
"""

from __future__ import annotations

import json
import os
import secrets
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
SECRETS_DIR = ROOT / "_secrets"
COOKIES_DIR = SECRETS_DIR / "cookies"
CREDS_DIR = SECRETS_DIR / "credentials"
REFRESHES_DIR = SECRETS_DIR / "refreshes"
PROFILES_DIR = SECRETS_DIR / "chrome_profiles"
KEY_FILE = SECRETS_DIR / ".vault.key"
REGISTRY_FILE = SECRETS_DIR / "registry.json"

DEFAULT_PORTALS: list[dict[str, Any]] = [
    {
        "portal_id": "linkedin",
        "display_name": "LinkedIn Main (Track 1 Social Signals)",
        "track": "track1_linkedin_signals",
        "login_url": "https://www.linkedin.com/login",
        "post_login_url_hint": "linkedin.com/feed",
        "cookie_domains": [".linkedin.com", "www.linkedin.com"],
        "required_cookies": ["li_at", "JSESSIONID"],
        "default_ttl_hours": 168,
    },
    {
        "portal_id": "linkedin_burner",
        "display_name": "LinkedIn Burner (Founder Education & Pedigree Enricher)",
        "track": "01_company_discovery",
        "login_url": "https://www.linkedin.com/login",
        "post_login_url_hint": "linkedin.com/feed",
        "cookie_domains": [".linkedin.com", "www.linkedin.com"],
        "required_cookies": ["li_at", "JSESSIONID"],
        "default_ttl_hours": 168,
    },
    {
        "portal_id": "wellfound",
        "display_name": "Wellfound (AngelList Talent)",
        "track": "track3_aggregators",
        "login_url": "https://wellfound.com/login",
        "post_login_url_hint": "wellfound.com/jobs",
        "cookie_domains": [".wellfound.com", "wellfound.com"],
        "required_cookies": ["_wellfound_session"],
        "default_ttl_hours": 168,
    },
    {
        "portal_id": "cutshort",
        "display_name": "Cutshort",
        "track": "track3_aggregators",
        "login_url": "https://cutshort.io/",
        "post_login_url_hint": "cutshort.io",
        "cookie_domains": [".cutshort.io", "cutshort.io"],
        "required_cookies": [],
        "default_ttl_hours": 168,
    },
    {
        "portal_id": "instahyre",
        "display_name": "Instahyre",
        "track": "track3_aggregators",
        "login_url": "https://www.instahyre.com/login/",
        "post_login_url_hint": "instahyre.com",
        "cookie_domains": [".instahyre.com", "www.instahyre.com"],
        "required_cookies": ["sessionid"],
        "default_ttl_hours": 168,
    },
    {
        "portal_id": "iimjobs",
        "display_name": "iimjobs",
        "track": "track3_aggregators",
        "login_url": "https://www.iimjobs.com/",
        "post_login_url_hint": "iimjobs.com",
        "cookie_domains": [".iimjobs.com", "www.iimjobs.com"],
        "required_cookies": [],
        "default_ttl_hours": 168,
    },
    {
        "portal_id": "otta",
        "display_name": "Otta (Welcome to the Jungle)",
        "track": "track3_aggregators",
        "login_url": "https://app.otta.com/login",
        "post_login_url_hint": "app.otta.com",
        "cookie_domains": [".otta.com", "app.otta.com"],
        "required_cookies": [],
        "default_ttl_hours": 168,
    },
    {
        "portal_id": "crunchbase",
        "display_name": "Crunchbase (Company Discovery)",
        "track": "01_company_discovery",
        "login_url": "https://www.crunchbase.com/login",
        "post_login_url_hint": "crunchbase.com",
        "cookie_domains": [".crunchbase.com", "www.crunchbase.com"],
        "required_cookies": [],
        "default_ttl_hours": 168,
    },
    {
        "portal_id": "the_ken",
        "display_name": "The Ken (Company Discovery)",
        "track": "01_company_discovery",
        "login_url": "https://the-ken.com/login/",
        "post_login_url_hint": "the-ken.com",
        "cookie_domains": [".the-ken.com", "the-ken.com"],
        "required_cookies": [],
        "default_ttl_hours": 336,
    },
    {
        "portal_id": "twitter_founders",
        "display_name": "X / Twitter (Founder Signals)",
        "track": "01_company_discovery",
        "login_url": "https://x.com/i/flow/login",
        "post_login_url_hint": "x.com/home",
        "cookie_domains": [".x.com", ".twitter.com"],
        "required_cookies": ["auth_token", "ct0"],
        "default_ttl_hours": 336,
    },
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def ensure_layout() -> None:
    """Create _secrets subdirectories and default registry if missing."""
    for d in (SECRETS_DIR, COOKIES_DIR, CREDS_DIR, REFRESHES_DIR, PROFILES_DIR):
        d.mkdir(parents=True, exist_ok=True)
    if not KEY_FILE.exists() and not os.environ.get("CAREER_VAULT_KEY"):
        KEY_FILE.write_text(secrets.token_hex(32) + "\n", encoding="utf-8")
        os.chmod(KEY_FILE, 0o600)
    if not REGISTRY_FILE.exists():
        seed = {
            "updated_at": iso_now(),
            "n8n_cloud_sync_webhook": "",
            "portals": {p["portal_id"]: _initial_portal_record(p) for p in DEFAULT_PORTALS},
        }
        REGISTRY_FILE.write_text(json.dumps(seed, indent=2) + "\n", encoding="utf-8")


def _initial_portal_record(defn: dict[str, Any]) -> dict[str, Any]:
    return {
        **defn,
        "has_credentials": False,
        "has_cookies": False,
        "last_signed_in": None,
        "expires_at": None,
        "cookie_count": 0,
        "cookie_status": "missing",
        "workflow_status": "unknown",
        "last_workflow_run": None,
        "last_error": None,
        "reauth_url": f"/auth/start?portal={defn['portal_id']}",
    }


def _vault_key() -> str:
    env_key = os.environ.get("CAREER_VAULT_KEY", "").strip()
    if env_key:
        return env_key
    ensure_layout()
    return KEY_FILE.read_text(encoding="utf-8").strip()


def encrypt_json(data: dict[str, Any], out_path: Path) -> None:
    """Encrypt a JSON-serializable dict to out_path using AES-256-CBC PBKDF2."""
    ensure_layout()
    env = os.environ.copy()
    env["CAREER_VAULT_KEY_TMP"] = _vault_key()
    payload = json.dumps(data, indent=2).encode("utf-8")
    proc = subprocess.run(
        [
            "openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "100000",
            "-salt", "-base64", "-pass", "env:CAREER_VAULT_KEY_TMP", "-out", str(out_path),
        ],
        input=payload,
        env=env,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"OpenSSL encrypt failed: {proc.stderr.decode('utf-8', 'ignore')}")
    os.chmod(out_path, 0o600)


def decrypt_json(in_path: Path) -> dict[str, Any]:
    """Decrypt an AES-256-CBC PBKDF2 encrypted JSON file."""
    if not in_path.exists():
        raise FileNotFoundError(f"Vault entry not found: {in_path}")
    env = os.environ.copy()
    env["CAREER_VAULT_KEY_TMP"] = _vault_key()
    proc = subprocess.run(
        [
            "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-iter", "100000",
            "-base64", "-pass", "env:CAREER_VAULT_KEY_TMP", "-in", str(in_path),
        ],
        env=env,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"OpenSSL decrypt failed: {proc.stderr.decode('utf-8', 'ignore')}")
    return json.loads(proc.stdout.decode("utf-8"))


def load_registry() -> dict[str, Any]:
    ensure_layout()
    reg = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    for p in DEFAULT_PORTALS:
        pid = p["portal_id"]
        if pid not in reg["portals"]:
            reg["portals"][pid] = _initial_portal_record(p)
    refresh_statuses(reg)
    return reg


def save_registry(reg: dict[str, Any]) -> None:
    ensure_layout()
    reg["updated_at"] = iso_now()
    refresh_statuses(reg)
    REGISTRY_FILE.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")


def refresh_statuses(reg: dict[str, Any]) -> None:
    """Recompute cookie_status (healthy / expiring_soon / expired / missing) from timestamps."""
    now = utc_now()
    for pid, rec in reg.get("portals", {}).items():
        cred_exists = (CREDS_DIR / f"{pid}.enc").exists()
        cookie_exists = (COOKIES_DIR / f"{pid}.enc").exists()
        rec["has_credentials"] = cred_exists
        rec["has_cookies"] = cookie_exists
        if not cookie_exists or not rec.get("expires_at"):
            rec["cookie_status"] = "missing" if not cookie_exists else "healthy"
            continue
        try:
            exp = datetime.fromisoformat(rec["expires_at"])
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
        except ValueError:
            rec["cookie_status"] = "unknown"
            continue
        remaining = exp - now
        if remaining.total_seconds() <= 0:
            rec["cookie_status"] = "expired"
        elif remaining <= timedelta(hours=24):
            rec["cookie_status"] = "expiring_soon"
        else:
            rec["cookie_status"] = "healthy"


def save_credentials(
    portal_id: str,
    username: str,
    password: str,
    login_url: str | None = None,
    notes: str = "",
) -> dict[str, Any]:
    """Store encrypted portal credentials and update registry."""
    reg = load_registry()
    if portal_id not in reg["portals"]:
        reg["portals"][portal_id] = _initial_portal_record({
            "portal_id": portal_id,
            "display_name": portal_id.replace("_", " ").title(),
            "track": "custom",
            "login_url": login_url or "",
            "post_login_url_hint": "",
            "cookie_domains": [],
            "required_cookies": [],
            "default_ttl_hours": 168,
        })
    rec = reg["portals"][portal_id]
    if login_url:
        rec["login_url"] = login_url

    payload = {
        "portal_id": portal_id,
        "username": username,
        "password": password,
        "login_url": rec["login_url"],
        "notes": notes,
        "updated_at": iso_now(),
    }
    encrypt_json(payload, CREDS_DIR / f"{portal_id}.enc")
    rec["has_credentials"] = True
    save_registry(reg)
    return rec


def get_credentials(portal_id: str) -> dict[str, Any]:
    return decrypt_json(CREDS_DIR / f"{portal_id}.enc")


def _compute_expiry(cookies: list[dict[str, Any]], required: list[str], default_ttl_hours: int) -> str:
    """Find the earliest relevant cookie expiry, falling back to default_ttl_hours."""
    now_ts = utc_now().timestamp()
    req_set = set(required or [])
    candidate_ts: list[float] = []

    for c in cookies:
        exp = c.get("expires") or c.get("expirationDate")
        if isinstance(exp, (int, float)) and exp > now_ts:
            if not req_set or c.get("name") in req_set:
                candidate_ts.append(float(exp))

    if candidate_ts:
        earliest = min(candidate_ts)
        return datetime.fromtimestamp(earliest, tz=timezone.utc).isoformat()
    return (utc_now() + timedelta(hours=default_ttl_hours)).isoformat()


def save_cookies(
    portal_id: str,
    cookies: list[dict[str, Any]],
    extra_headers: dict[str, str] | None = None,
    source: str = "cdp_capture",
) -> dict[str, Any]:
    """Encrypt captured cookies + derived Cookie header and update registry."""
    reg = load_registry()
    if portal_id not in reg["portals"]:
        reg["portals"][portal_id] = _initial_portal_record({
            "portal_id": portal_id,
            "display_name": portal_id.replace("_", " ").title(),
            "track": "custom",
            "login_url": "",
            "post_login_url_hint": "",
            "cookie_domains": [],
            "required_cookies": [],
            "default_ttl_hours": 168,
        })
    rec = reg["portals"][portal_id]
    required = rec.get("required_cookies", [])
    default_ttl = int(rec.get("default_ttl_hours", 168))

    cookie_pairs = [f"{c['name']}={c['value']}" for c in cookies if c.get("name") and c.get("value") is not None]
    cookie_header = "; ".join(cookie_pairs)
    captured_at = iso_now()
    expires_at = _compute_expiry(cookies, required, default_ttl)

    # Auto-derive LinkedIn csrf-token from JSESSIONID if present
    headers = dict(extra_headers or {})
    if portal_id == "linkedin" and "csrf-token" not in {k.lower() for k in headers}:
        for c in cookies:
            if c.get("name") == "JSESSIONID" and c.get("value"):
                headers["csrf-token"] = str(c["value"]).strip('"')
                break

    payload = {
        "portal_id": portal_id,
        "captured_at": captured_at,
        "expires_at": expires_at,
        "source": source,
        "cookie_header": cookie_header,
        "extra_headers": headers,
        "cookies": cookies,
    }
    encrypt_json(payload, COOKIES_DIR / f"{portal_id}.enc")

    rec["has_cookies"] = True
    rec["last_signed_in"] = captured_at
    rec["expires_at"] = expires_at
    rec["cookie_count"] = len(cookies)
    rec["workflow_status"] = "ok"
    rec["last_error"] = None
    save_registry(reg)
    return rec


def get_cookies(portal_id: str) -> dict[str, Any]:
    return decrypt_json(COOKIES_DIR / f"{portal_id}.enc")


def report_workflow_status(portal_id: str, status: str, error: str | None = None) -> dict[str, Any]:
    """Update workflow_status (ok / broken) and auto-flag expired cookies on 401/403."""
    reg = load_registry()
    if portal_id not in reg["portals"]:
        raise KeyError(f"Unknown portal_id: {portal_id}")
    rec = reg["portals"][portal_id]
    rec["workflow_status"] = status
    rec["last_workflow_run"] = iso_now()
    rec["last_error"] = error
    if status == "broken" and error and any(code in error for code in ("401", "403", "expired", "login")):
        rec["cookie_status"] = "expired"
        rec["expires_at"] = iso_now()
    save_registry(reg)
    return rec
