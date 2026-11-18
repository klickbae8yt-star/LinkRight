#!/usr/bin/env python3
"""Localhost Auth, Cookie Vault & Workflow Health Dashboard.

Run:
    python3 _shared/dashboard/server.py --port 8765
Open:
    http://127.0.0.1:8765
"""

from __future__ import annotations

import argparse
import html
import json
import secrets
import sys
import threading
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

AUTH_DIR = Path(__file__).resolve().parents[1] / "scripts" / "auth"
sys.path.insert(0, str(AUTH_DIR))

from cdp_capture import (  # noqa: E402
    import_cookies_from_har,
    launch_chrome_for_portal,
    snapshot_cookies_from_cdp,
)
from vault import (  # noqa: E402
    get_cookies,
    load_registry,
    report_workflow_status,
    save_cookies,
    save_credentials,
    save_registry,
)

TEMPLATE_HTML = Path(__file__).resolve().parent / "templates" / "index.html"
ACTIVE_SESSIONS: dict[str, dict[str, Any]] = {}
SESSIONS_LOCK = threading.Lock()


def _push_to_n8n_webhook(portal_id: str) -> None:
    """If an n8n Cloud sync webhook is configured, push updated cookies securely."""
    reg = load_registry()
    webhook = (reg.get("n8n_cloud_sync_webhook") or "").strip()
    if not webhook:
        return
    try:
        cookie_bundle = get_cookies(portal_id)
        payload = json.dumps({
            "portal_id": portal_id,
            "captured_at": cookie_bundle.get("captured_at"),
            "expires_at": cookie_bundle.get("expires_at"),
            "cookie_header": cookie_bundle.get("cookie_header"),
            "extra_headers": cookie_bundle.get("extra_headers", {}),
        }).encode("utf-8")
        req = urllib.request.Request(
            webhook,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=8):
            pass
    except Exception:
        # Never break local capture if remote webhook is temporarily unreachable.
        pass


def _cdp_watch_worker(session_id: str, portal_id: str, proc: Any, cdp_port: int) -> None:
    """Poll Chrome CDP every 2s until target cookies appear or timeout (10 min)."""
    deadline = time.time() + 600
    while time.time() < deadline:
        with SESSIONS_LOCK:
            sess = ACTIVE_SESSIONS.get(session_id)
            if not sess or sess["state"] != "waiting":
                break
        if proc.poll() is not None:
            with SESSIONS_LOCK:
                ACTIVE_SESSIONS[session_id]["state"] = "closed"
                ACTIVE_SESSIONS[session_id]["message"] = "Browser window was closed before capture."
            return
        try:
            ready, info = snapshot_cookies_from_cdp(cdp_port, portal_id)
            if ready:
                _push_to_n8n_webhook(portal_id)
                with SESSIONS_LOCK:
                    ACTIVE_SESSIONS[session_id]["state"] = "captured"
                    ACTIVE_SESSIONS[session_id]["message"] = (
                        f"Captured {info.get('cookie_count', 0)} cookies. Expires: {info.get('expires_at')}"
                    )
                try:
                    proc.terminate()
                except Exception:
                    pass
                return
            with SESSIONS_LOCK:
                ACTIVE_SESSIONS[session_id]["found_names"] = info.get("found_names", [])
        except Exception as exc:
            with SESSIONS_LOCK:
                ACTIVE_SESSIONS[session_id]["last_poll_error"] = str(exc)
        time.sleep(2)

    with SESSIONS_LOCK:
        if session_id in ACTIVE_SESSIONS and ACTIVE_SESSIONS[session_id]["state"] == "waiting":
            ACTIVE_SESSIONS[session_id]["state"] = "timeout"
            ACTIVE_SESSIONS[session_id]["message"] = "Timed out waiting for login after 10 minutes."


def _auth_wait_page(session_id: str, portal_name: str, login_url: str) -> str:
    safe_name = html.escape(portal_name)
    safe_url = html.escape(login_url)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Authenticating {safe_name}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; background:#0b0f17; color:#e6edf7; display:flex; align-items:center; justify-content:center; min-height:100vh; margin:0; }}
  .box {{ background:#131a26; border:1px solid #232f44; border-radius:12px; padding:28px; max-width:520px; width:92%; }}
  .btn {{ display:inline-block; padding:9px 14px; border-radius:6px; background:#3b82f6; color:#fff; border:none; font-weight:600; cursor:pointer; text-decoration:none; margin-right:8px; }}
  .btn-sec {{ background:#1a2436; border:1px solid #232f44; }}
  .muted {{ color:#8b9bb4; font-size:13px; }}
</style></head>
<body><div class="box">
  <h2>🔐 Sign In: {safe_name}</h2>
  <p class="muted">Chrome has opened to <code>{safe_url}</code>. Complete your login (including SSO/2FA if prompted). Cookies will be captured automatically.</p>
  <p id="status">⏳ Waiting for session cookies...</p>
  <div style="margin-top:18px;">
    <button class="btn" onclick="forceCapture()">Capture Cookies Now</button>
    <a class="btn btn-sec" href="/">← Back to Dashboard</a>
  </div>
</div>
<script>
  async function poll() {{
    const res = await fetch('/api/auth/session/{session_id}');
    const s = await res.json();
    const el = document.getElementById('status');
    if (s.state === 'captured') {{
      el.innerHTML = '✅ <strong>Success!</strong> ' + s.message;
      setTimeout(() => location.href = '/', 1500);
      return;
    }}
    if (s.state === 'closed' || s.state === 'timeout') {{
      el.innerHTML = '❌ ' + s.message;
      return;
    }}
    el.innerHTML = '⏳ Waiting for login... cookies seen so far: ' + (s.found_names || []).length;
    setTimeout(poll, 1500);
  }}
  async function forceCapture() {{
    const res = await fetch('/api/auth/session/{session_id}/capture', {{ method: 'POST' }});
    const out = await res.json();
    if (out.captured) {{
      document.getElementById('status').innerHTML = '✅ Captured! Redirecting...';
      setTimeout(() => location.href = '/', 1000);
    }} else {{
      alert('No cookies found yet. Finish logging in inside the Chrome window first.');
    }}
  }}
  poll();
</script></body></html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        return

    def _send_json(self, data: Any, status: int = 200) -> None:
        raw = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _send_html(self, content: str, status: int = 200) -> None:
        raw = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length > 0 else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        if path == "/":
            return self._send_html(TEMPLATE_HTML.read_text(encoding="utf-8"))

        if path == "/api/status":
            return self._send_json(load_registry())

        if path == "/auth/start":
            portal_id = (qs.get("portal") or [""])[0].strip()
            reg = load_registry()
            if portal_id not in reg["portals"]:
                return self._send_json({"error": f"Unknown portal: {portal_id}"}, 404)
            rec = reg["portals"][portal_id]
            try:
                proc, cdp_port = launch_chrome_for_portal(portal_id)
            except Exception as exc:
                return self._send_json({"error": str(exc)}, 500)

            sid = secrets.token_hex(8)
            with SESSIONS_LOCK:
                ACTIVE_SESSIONS[sid] = {
                    "session_id": sid,
                    "portal_id": portal_id,
                    "cdp_port": cdp_port,
                    "proc": proc,
                    "state": "waiting",
                    "found_names": [],
                    "message": "",
                }
            t = threading.Thread(target=_cdp_watch_worker, args=(sid, portal_id, proc, cdp_port), daemon=True)
            t.start()
            return self._send_html(_auth_wait_page(sid, rec["display_name"], rec.get("login_url", "")))

        if path.startswith("/api/auth/session/"):
            sid = path.split("/")[-1]
            with SESSIONS_LOCK:
                sess = ACTIVE_SESSIONS.get(sid)
                if not sess:
                    return self._send_json({"error": "Session not found"}, 404)
                return self._send_json({k: v for k, v in sess.items() if k != "proc"})

        return self._send_json({"error": "Not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        path = urllib.parse.urlparse(self.path).path

        if path == "/api/credentials":
            body = self._read_json_body()
            rec = save_credentials(
                portal_id=body["portal_id"],
                username=body.get("username", ""),
                password=body.get("password", ""),
                login_url=body.get("login_url"),
            )
            return self._send_json({"ok": True, "portal": rec})

        if path == "/api/config/webhook":
            body = self._read_json_body()
            reg = load_registry()
            reg["n8n_cloud_sync_webhook"] = body.get("n8n_cloud_sync_webhook", "").strip()
            save_registry(reg)
            return self._send_json({"ok": True})

        if path == "/api/workflow/report":
            body = self._read_json_body()
            rec = report_workflow_status(
                portal_id=body["portal_id"],
                status=body["status"],
                error=body.get("error"),
            )
            return self._send_json({"ok": True, "portal": rec})

        if path == "/api/auth/import":
            body = self._read_json_body()
            pid = body["portal_id"]
            fname = (body.get("filename") or "").lower()
            content = body.get("content", "")
            try:
                if fname.endswith(".har") or '"log"' in content[:500]:
                    rec = import_cookies_from_har(pid, content)
                else:
                    parsed = json.loads(content)
                    cookies = parsed if isinstance(parsed, list) else parsed.get("cookies", [])
                    rec = save_cookies(pid, cookies, source="json_import")
                _push_to_n8n_webhook(pid)
                return self._send_json({"ok": True, "portal": rec})
            except Exception as exc:
                return self._send_json({"error": str(exc)}, 400)

        if path.startswith("/api/auth/session/") and path.endswith("/capture"):
            sid = path.split("/")[-2]
            with SESSIONS_LOCK:
                sess = ACTIVE_SESSIONS.get(sid)
            if not sess:
                return self._send_json({"error": "Session not found"}, 404)
            reg = load_registry()
            pid = sess["portal_id"]
            # Force save any cookies currently present for the domain
            from cdp_capture import cdp_call, filter_portal_cookies  # noqa: E402
            res = cdp_call(sess["cdp_port"], "Storage.getCookies")
            rec = reg["portals"][pid]
            matched = filter_portal_cookies(res.get("cookies", []), rec.get("cookie_domains", []), rec.get("login_url", ""))
            if not matched:
                return self._send_json({"captured": False})
            updated = save_cookies(pid, matched, source="cdp_manual_trigger")
            _push_to_n8n_webhook(pid)
            with SESSIONS_LOCK:
                sess["state"] = "captured"
                sess["message"] = f"Captured {len(matched)} cookies."
            try:
                sess["proc"].terminate()
            except Exception:
                pass
            return self._send_json({"captured": True, "portal": updated})

        return self._send_json({"error": "Not found"}, 404)


def main() -> int:
    parser = argparse.ArgumentParser(description="Start the localhost Auth & Workflow Health Dashboard")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    load_registry()
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"Auth & Workflow Health Dashboard running at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down dashboard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

