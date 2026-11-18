#!/usr/bin/env python3
"""
ats_scanner.py — ATS compatibility check for HTML and LaTeX resumes.

Checks for formatting patterns that break ATS (Applicant Tracking System) parsing.
ATS systems parse raw text; they cannot read tables, text boxes, columns, or graphics.

Usage:
  python ats_scanner.py '{"content": "<html>...", "format": "html"}'
  python ats_scanner.py '{"content": "\\begin{document}...", "format": "latex"}'

Output:
  {
    "issues": [
      {"type": "table_layout", "severity": "critical", "detail": "Found <table> tag used for layout"}
    ],
    "issue_count": 1,
    "critical_count": 1,
    "status": "fail",
    "message": "1 critical ATS issue found. Fix before delivery."
  }
"""

import json
import sys
import re


# ─── HTML ATS CHECKS ─────────────────────────────────────────────────────────

HTML_CHECKS = [
    {
        "name": "table_layout",
        "severity": "critical",
        "pattern": r'<table[\s>]',
        "detail": "<table> tag found — ATS cannot parse table-based layouts. Use div/flex instead."
    },
    {
        "name": "text_box",
        "severity": "critical",
        "pattern": r'position\s*:\s*absolute|position\s*:\s*fixed',
        "detail": "Absolute/fixed positioning found — ATS will miss text in positioned elements."
    },
    {
        "name": "multi_column",
        "severity": "critical",
        "pattern": r'column-count\s*:\s*[2-9]|columns\s*:\s*[2-9]',
        "detail": "CSS multi-column layout found — ATS reads left-to-right and will mangle column order."
    },
    {
        "name": "overflow_hidden",
        "severity": "critical",
        "pattern": r'overflow\s*:\s*hidden',
        "detail": "overflow:hidden found — content clipped here is invisible to ATS parsers."
    },
    {
        "name": "image_text",
        "severity": "critical",
        "pattern": r'<img[^>]+alt\s*=\s*"[^"]{10,}"',
        "detail": "Image with long alt text found — ATS ignores images. Text must be in HTML, not images."
    },
    {
        "name": "canvas_text",
        "severity": "critical",
        "pattern": r'<canvas',
        "detail": "<canvas> element found — ATS cannot read canvas-rendered text."
    },
    {
        "name": "svg_text",
        "severity": "warn",
        "pattern": r'<svg',
        "detail": "<svg> element found — some ATS systems cannot read SVG text. Verify no critical info is SVG-only."
    },
    {
        "name": "header_footer_content",
        "severity": "warn",
        "pattern": r'@page\s*\{[^}]*content\s*:',
        "detail": "CSS @page content found — ATS may not read header/footer content. Put all info in body."
    },
    {
        "name": "font_face_non_web_safe",
        "severity": "info",
        "pattern": r'@font-face',
        "detail": "Custom @font-face found — ensure fallback to web-safe font if CDN unavailable."
    },
    {
        "name": "height_overflow_clipping",
        "severity": "critical",
        "pattern": r'height\s*:\s*[\d.]+(?:em|px|pt|mm)\s*;[^}]*overflow\s*:\s*hidden',
        "detail": "height + overflow:hidden combination found — this clips bullet content. Remove."
    },
]

# ─── LATEX ATS CHECKS ────────────────────────────────────────────────────────

LATEX_CHECKS = [
    {
        "name": "minipage_columns",
        "severity": "critical",
        "pattern": r'\\begin\{minipage\}.*?\\begin\{minipage\}',
        "detail": "Multiple minipages (columns) found — ATS will read them in wrong order."
    },
    {
        "name": "tabular_layout",
        "severity": "critical",
        "pattern": r'\\begin\{tabular\}',
        "detail": "\\tabular environment found — ATS cannot parse table-structured layout."
    },
    {
        "name": "textbox",
        "severity": "critical",
        "pattern": r'\\begin\{textblock\}|\\tcbox|\\fbox.*?\\parbox',
        "detail": "Text box construct found — ATS will miss content inside boxes."
    },
    {
        "name": "includegraphics_text",
        "severity": "warn",
        "pattern": r'\\includegraphics',
        "detail": "Image found — verify no critical information is image-only (contact info, logos, etc.)"
    },
    {
        "name": "hyperref_url_only",
        "severity": "info",
        "pattern": r'\\href\{[^}]+\}\{\s*\\textcolor',
        "detail": "Link text uses color only — ensure the URL text is human-readable, not just colored."
    },
]


def scan_html(content: str) -> list:
    issues = []
    for check in HTML_CHECKS:
        if re.search(check["pattern"], content, re.IGNORECASE | re.DOTALL):
            issues.append({
                "type": check["name"],
                "severity": check["severity"],
                "detail": check["detail"]
            })
    return issues


def scan_latex(content: str) -> list:
    issues = []
    for check in LATEX_CHECKS:
        if re.search(check["pattern"], content, re.IGNORECASE | re.DOTALL):
            issues.append({
                "type": check["name"],
                "severity": check["severity"],
                "detail": check["detail"]
            })
    return issues


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Pass JSON: '{\"content\": \"...\", \"format\": \"html|latex\"}'"}))
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    content = payload.get("content", "")
    fmt = payload.get("format", "html").lower()

    if not content:
        print(json.dumps({"error": "No content provided"}))
        sys.exit(1)

    if fmt == "html":
        issues = scan_html(content)
    elif fmt in ("latex", "tex"):
        issues = scan_latex(content)
    else:
        print(json.dumps({"error": f"Unknown format: {fmt}. Use 'html' or 'latex'."}))
        sys.exit(1)

    critical = [i for i in issues if i["severity"] == "critical"]
    warnings = [i for i in issues if i["severity"] == "warn"]

    count = len(issues)
    critical_count = len(critical)

    if critical_count > 0:
        status = "fail"
        msg = f"{critical_count} critical ATS issue(s) found. Must fix before delivery."
    elif len(warnings) > 0:
        status = "warn"
        msg = f"0 critical issues, {len(warnings)} warning(s). Review before delivery."
    else:
        status = "pass"
        msg = "ATS scan passed ✓"

    result = {
        "issues": issues,
        "issue_count": count,
        "critical_count": critical_count,
        "warning_count": len(warnings),
        "status": status,
        "message": msg
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
