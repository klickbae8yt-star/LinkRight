#!/usr/bin/env python3
"""Interactive Chrome DevTools Protocol (CDP) cookie & auth capture bridge.

Zero external dependencies: uses stdlib socket + base64 + hashlib for
minimal RFC 6455 WebSocket communication with local Chrome --remote-debugging-port.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import socket
import struct
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from vault import PROFILES_DIR, load_registry, save_cookies

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def find_free_port(start: int = 9222, end: int = 9299) -> int:
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise RuntimeError("No free debugging port available between 9222 and 9299.")


def _ws_connect(ws_url: str, timeout: float = 5.0) -> socket.socket:
    parsed = urllib.parse.urlparse(ws_url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 80
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    sock = socket.create_connection((host, port), timeout=timeout)
    key = base64.b64encode(os.urandom(16)).decode("ascii")
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    sock.sendall(req.encode("ascii"))

    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("CDP WebSocket handshake closed unexpectedly")
        buf += chunk
    if b"101 " not in buf.split(b"\r\n", 1)[0]:
        raise ConnectionError(f"CDP WebSocket upgrade failed: {buf[:200]!r}")
    return sock


def _ws_send_text(sock: socket.socket, text: str) -> None:
    payload = text.encode("utf-8")
    mask = os.urandom(4)
    length = len(payload)
    header = bytearray([0x81])
    if length < 126:
        header.append(0x80 | length)
    elif length < 65536:
        header.append(0x80 | 126)
        header.extend(struct.pack("!H", length))
    else:
        header.append(0x80 | 127)
        header.extend(struct.pack("!Q", length))
    header.extend(mask)
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    sock.sendall(bytes(header) + masked)


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    out = bytearray()
    while len(out) < n:
        chunk = sock.recv(n - len(out))
        if not chunk:
            raise ConnectionError("CDP WebSocket closed while reading frame")
        out.extend(chunk)
    return bytes(out)


def _ws_recv_text(sock: socket.socket) -> str:
    while True:
        b1, b2 = _recv_exact(sock, 2)
        opcode = b1 & 0x0F
        masked = (b2 & 0x80) != 0
        length = b2 & 0x7F
        if length == 126:
            length = struct.unpack("!H", _recv_exact(sock, 2))[0]
        elif length == 127:
            length = struct.unpack("!Q", _recv_exact(sock, 8))[0]
        mask = _recv_exact(sock, 4) if masked else b""
        data = _recv_exact(sock, length)
        if masked:
            data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        if opcode == 0x8:
            raise ConnectionError("CDP WebSocket closed by Chrome")
        if opcode == 0x9:  # Ping -> send Pong
            continue
        if opcode == 0x1:
            return data.decode("utf-8")


def cdp_call(port: int, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute one CDP command against the browser or first page target."""
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=3) as resp:
        ver = json.loads(resp.read().decode("utf-8"))
    ws_url = ver.get("webSocketDebuggerUrl")
    if not ws_url:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=3) as resp:
            targets = json.loads(resp.read().decode("utf-8"))
        ws_url = targets[0]["webSocketDebuggerUrl"]

    msg_id = int(secrets.randbelow(100000) + 1)
    sock = _ws_connect(ws_url)
    try:
        _ws_send_text(sock, json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        while True:
            raw = _ws_recv_text(sock)
            msg = json.loads(raw)
            if msg.get("id") == msg_id:
                if "error" in msg:
                    raise RuntimeError(f"CDP error for {method}: {msg['error']}")
                return msg.get("result", {})
    finally:
        sock.close()


def launch_chrome_for_portal(portal_id: str) -> tuple[subprocess.Popen[bytes], int]:
    """Launch an isolated Chrome window at the portal's login URL with CDP enabled."""
    reg = load_registry()
    if portal_id not in reg["portals"]:
        raise KeyError(f"Unknown portal: {portal_id}")
    rec = reg["portals"][portal_id]
    login_url = rec.get("login_url") or "about:blank"
    profile_dir = PROFILES_DIR / portal_id
    profile_dir.mkdir(parents=True, exist_ok=True)

    port = find_free_port()
    proc = subprocess.Popen(
        [
            CHROME_BIN,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            login_url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1) as resp:
                if resp.status == 200:
                    return proc, port
        except Exception:
            time.sleep(0.3)
    proc.terminate()
    raise RuntimeError(f"Chrome CDP did not start on port {port}")


def filter_portal_cookies(cookies: list[dict[str, Any]], domains: list[str], login_url: str) -> list[dict[str, Any]]:
    """Filter CDP cookie list down to the target portal's domains."""
    if not domains and login_url:
        host = urllib.parse.urlparse(login_url).hostname or ""
        parts = host.split(".")
        domains = ["." + ".".join(parts[-2:])] if len(parts) >= 2 else [host]

    norm_domains = [d.lower().lstrip(".") for d in domains if d]
    matched: list[dict[str, Any]] = []
    for c in cookies:
        cdom = str(c.get("domain", "")).lower().lstrip(".")
        if not norm_domains or any(cdom == d or cdom.endswith("." + d) for d in norm_domains):
            matched.append(c)
    return matched


def snapshot_cookies_from_cdp(port: int, portal_id: str) -> tuple[bool, dict[str, Any]]:
    """Read cookies from Chrome via CDP and save to encrypted vault if valid."""
    reg = load_registry()
    rec = reg["portals"][portal_id]
    res = cdp_call(port, "Storage.getCookies")
    all_cookies = res.get("cookies", [])
    portal_cookies = filter_portal_cookies(
        all_cookies,
        rec.get("cookie_domains", []),
        rec.get("login_url", ""),
    )

    names = {c.get("name") for c in portal_cookies}
    required = set(rec.get("required_cookies", []))
    ready = bool(portal_cookies) and (not required or required.issubset(names))
    if not ready:
        return False, {"cookie_count": len(portal_cookies), "found_names": sorted(n for n in names if n)}

    updated = save_cookies(portal_id, portal_cookies, source="cdp_live_auth")
    return True, updated


def import_cookies_from_har(portal_id: str, har_text: str) -> dict[str, Any]:
    """Extract cookies & auth headers from a Chrome HAR file and store in vault."""
    reg = load_registry()
    rec = reg["portals"].get(portal_id, {})
    har = json.loads(har_text)
    entries = har.get("log", {}).get("entries", [])

    cookie_map: dict[tuple[str, str], dict[str, Any]] = {}
    extra_headers: dict[str, str] = {}
    domains = [d.lower().lstrip(".") for d in rec.get("cookie_domains", [])]

    for e in entries:
        req = e.get("request", {})
        url = req.get("url", "")
        host = (urllib.parse.urlparse(url).hostname or "").lower()
        if domains and not any(host == d or host.endswith("." + d) for d in domains):
            continue
        for c in req.get("cookies", []):
            name = c.get("name")
            if name:
                cookie_map[(host, name)] = {"name": name, "value": c.get("value", ""), "domain": host}
        for c in e.get("response", {}).get("cookies", []):
            name = c.get("name")
            if name:
                cookie_map[(host, name)] = {"name": name, "value": c.get("value", ""), "domain": host}
        for h in req.get("headers", []):
            hl = h.get("name", "").lower()
            if hl in ("csrf-token", "x-csrf-token", "authorization"):
                extra_headers[h["name"]] = h["value"]

    cookies = list(cookie_map.values())
    if not cookies:
        raise ValueError("No matching cookies found in HAR for this portal.")
    return save_cookies(portal_id, cookies, extra_headers=extra_headers, source="har_import")

