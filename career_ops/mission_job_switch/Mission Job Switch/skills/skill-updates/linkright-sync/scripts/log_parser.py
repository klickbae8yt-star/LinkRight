#!/usr/bin/env python3
"""
log_parser.py — Parse XeLaTeX .log file for hbox warnings and badness values.

Used in the LaTeX resume path to measure bullet width and page fit.
The .log file is the only reliable width measurement tool for XeLaTeX.

Usage:
  python log_parser.py '{"log_path": "/path/to/resume.log"}'
  python log_parser.py '{"log_text": "...raw log content..."}'

Output:
  {
    "overfull": [
      {"line": 42, "detail": "Overfull \\hbox (3.45pt too wide)", "severity": "critical"}
    ],
    "underfull": [
      {"line": 87, "badness": 450, "detail": "Underfull \\hbox (badness 450)", "severity": "warn"}
    ],
    "vbox_overflow": false,
    "summary": {
      "overfull_count": 1,
      "underfull_critical": 0,
      "underfull_warn": 1,
      "underfull_ok": 0
    },
    "status": "fail",
    "message": "1 Overfull \\hbox — trim bullet(s) on flagged lines."
  }
"""

import json
import sys
import re
import os


def parse_log(log_text: str) -> dict:
    overfull = []
    underfull = []
    vbox_overflow = False

    lines = log_text.split('\n')

    for i, line in enumerate(lines):
        # Overfull hbox — bullet too long
        overfull_match = re.search(
            r'Overfull\\hbox\s*\(([0-9.]+)pt\s+too\s+wide\)',
            line, re.IGNORECASE
        )
        if overfull_match:
            overage = float(overfull_match.group(1))
            overfull.append({
                "log_line": i + 1,
                "overage_pt": overage,
                "detail": f"Overfull \\hbox ({overage}pt too wide)",
                "severity": "critical",
                "action": f"Trim ~{round(overage * 0.353, 1)}mm from this bullet"
            })

        # Underfull hbox — bullet too short (badness value matters)
        underfull_match = re.search(
            r'Underfull\\hbox\s*\(badness\s+([0-9]+)\)',
            line, re.IGNORECASE
        )
        if underfull_match:
            badness = int(underfull_match.group(1))
            if badness == 0:
                severity = "ok"
                action = "Perfect fill — ship"
            elif badness <= 200:
                severity = "ok"
                action = "Target zone (badness ≤200) — ship"
            elif badness <= 1000:
                severity = "warn"
                action = "Try to expand bullet slightly"
            elif badness < 10000:
                severity = "fail"
                action = "Sparse line — rewrite bullet to be longer"
            else:
                severity = "fail"
                action = "Terrible fill — rewrite bullet completely"

            underfull.append({
                "log_line": i + 1,
                "badness": badness,
                "detail": f"Underfull \\hbox (badness {badness})",
                "severity": severity,
                "action": action
            })

        # Vbox overflow — page too long
        if re.search(r'Overfull\\vbox', line, re.IGNORECASE):
            vbox_overflow = True

    # Summary
    overfull_count = len(overfull)
    underfull_critical = len([u for u in underfull if u["severity"] == "fail"])
    underfull_warn = len([u for u in underfull if u["severity"] == "warn"])
    underfull_ok = len([u for u in underfull if u["severity"] == "ok"])

    # Status
    if overfull_count > 0:
        status = "fail"
        msg = f"{overfull_count} Overfull \\hbox — trim bullet(s) on flagged log lines."
    elif underfull_critical > 0:
        status = "fail"
        msg = f"{underfull_critical} underfull line(s) with high badness — rewrite bullets."
    elif vbox_overflow:
        status = "fail"
        msg = "\\vbox overflow detected — resume exceeds one page. Remove content."
    elif underfull_warn > 0:
        status = "warn"
        msg = f"{underfull_warn} underfull line(s) with moderate badness — try to expand."
    else:
        status = "pass"
        msg = "LaTeX log clean ✓ — no hbox or vbox issues."

    return {
        "overfull": overfull,
        "underfull": underfull,
        "vbox_overflow": vbox_overflow,
        "summary": {
            "overfull_count": overfull_count,
            "underfull_critical": underfull_critical,
            "underfull_warn": underfull_warn,
            "underfull_ok": underfull_ok,
        },
        "status": status,
        "message": msg
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Pass JSON: '{\"log_path\": \"/path/to/file.log\"}' or '{\"log_text\": \"...\"}'"}))
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    log_text = payload.get("log_text", "")

    if not log_text:
        log_path = payload.get("log_path", "")
        if not log_path or not os.path.exists(log_path):
            print(json.dumps({"error": f"Log file not found: {log_path}"}))
            sys.exit(1)
        with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
            log_text = f.read()

    result = parse_log(log_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
