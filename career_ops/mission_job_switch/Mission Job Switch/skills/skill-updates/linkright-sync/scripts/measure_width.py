#!/usr/bin/env python3
"""
measure_width.py — Bullet width measurement for linkright-sync HTML path.

Measures rendered text width in mm using character-level metrics calibrated
for Roboto 9.5pt on A4 with 12.7mm margins.

BULLET_BUDGET = 158.07mm  (A4 210mm - 2×12.7mm margins - list indent ~26.56mm)

Usage:
  python measure_width.py '{"text": "Led cross-functional roadmap...", "font_size": 9.5}'

Output:
  {
    "text": "Led cross-functional roadmap...",
    "width_mm": 142.3,
    "budget_mm": 158.07,
    "fill_pct": 90.0,
    "status": "expand",
    "message": "90.0% — expand to reach 95–100%"
  }

Status values:
  too_short  → <85%    (definitely expand)
  expand     → 85–95%  (try to expand)
  ok         → 95–100% (ship)
  too_long   → >100%   (trim)
"""

import json
import sys

# A4 page width: 210mm
# Left margin: 12.7mm, Right margin: 12.7mm
# Bullet list indent: ~26.56mm (accounts for padding, bullet symbol, and list left padding)
# Effective bullet text budget = 210 - 12.7 - 12.7 - 26.56 = 158.04 ≈ 158.07mm
BULLET_BUDGET = 158.07  # mm

# Character width table for Roboto at 9.5pt (calibrated empirically)
# Values in mm per character. Roboto is proportional — different chars have different widths.
CHAR_WIDTHS_9_5PT = {
    # Uppercase (wider)
    'A': 2.11, 'B': 2.00, 'C': 2.11, 'D': 2.22, 'E': 1.89, 'F': 1.78, 'G': 2.22,
    'H': 2.22, 'I': 0.78, 'J': 1.44, 'K': 2.11, 'L': 1.78, 'M': 2.56, 'N': 2.22,
    'O': 2.33, 'P': 2.00, 'Q': 2.33, 'R': 2.11, 'S': 1.89, 'T': 1.89, 'U': 2.22,
    'V': 2.11, 'W': 2.78, 'X': 2.11, 'Y': 2.00, 'Z': 1.89,
    # Lowercase
    'a': 1.78, 'b': 1.89, 'c': 1.67, 'd': 1.89, 'e': 1.78, 'f': 1.11, 'g': 1.89,
    'h': 1.89, 'i': 0.78, 'j': 0.78, 'k': 1.78, 'l': 0.78, 'm': 2.78, 'n': 1.89,
    'o': 1.89, 'p': 1.89, 'q': 1.89, 'r': 1.11, 's': 1.56, 't': 1.22, 'u': 1.89,
    'v': 1.78, 'w': 2.44, 'x': 1.78, 'y': 1.78, 'z': 1.56,
    # Digits
    '0': 1.89, '1': 1.89, '2': 1.89, '3': 1.89, '4': 1.89, '5': 1.89, '6': 1.89,
    '7': 1.89, '8': 1.89, '9': 1.89,
    # Punctuation and symbols
    ' ': 0.56, '.': 0.78, ',': 0.78, ';': 0.78, ':': 0.78, '!': 0.78, '?': 1.56,
    "'": 0.56, '"': 1.00, '(': 1.00, ')': 1.00, '[': 0.89, ']': 0.89, '{': 0.89,
    '}': 0.89, '-': 1.11, '–': 1.67, '—': 2.22, '/': 1.00, '\\': 1.00, '@': 2.89,
    '#': 1.89, '$': 1.89, '%': 2.33, '&': 2.22, '*': 1.33, '+': 1.89, '=': 1.89,
    '<': 1.89, '>': 1.89, '~': 1.89, '^': 1.89, '_': 1.89, '|': 0.67, '`': 1.00,
}

DEFAULT_CHAR_WIDTH = 1.78  # fallback for unmapped characters


def measure_text(text: str, font_size: float = 9.5) -> float:
    """Return estimated rendered width in mm for given text at given font size."""
    scale = font_size / 9.5  # scale from calibration point
    total = 0.0
    for ch in text:
        total += CHAR_WIDTHS_9_5PT.get(ch, DEFAULT_CHAR_WIDTH)
    return round(total * scale, 2)


def evaluate(width_mm: float, budget_mm: float = BULLET_BUDGET):
    fill_pct = round((width_mm / budget_mm) * 100, 1)
    if fill_pct < 85:
        status = "too_short"
        msg = f"{fill_pct}% — definitely expand (target 95–100%)"
    elif fill_pct < 95:
        status = "expand"
        msg = f"{fill_pct}% — try to expand to reach 95–100%"
    elif fill_pct <= 100:
        status = "ok"
        msg = f"{fill_pct}% — SHIP ✓"
    else:
        status = "too_long"
        msg = f"{fill_pct}% — too long, trim to ≤100%"
    return fill_pct, status, msg


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Pass JSON as first arg: '{\"text\": \"...\", \"font_size\": 9.5}'"}))
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    text = payload.get("text", "")
    font_size = float(payload.get("font_size", 9.5))
    budget = float(payload.get("budget_mm", BULLET_BUDGET))

    if not text:
        print(json.dumps({"error": "No text provided"}))
        sys.exit(1)

    # For multi-line bullets, measure only the LAST line (the critical one for fill)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    last_line = lines[-1] if lines else text

    width = measure_text(last_line, font_size)
    fill_pct, status, msg = evaluate(width, budget)

    result = {
        "text": text,
        "last_line": last_line,
        "width_mm": width,
        "budget_mm": budget,
        "fill_pct": fill_pct,
        "status": status,
        "message": msg
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
