#!/usr/bin/env python3
"""
ai_smell_checker.py — Detect AI-generated language patterns in resume text.

Flags phrases that signal LLM-generated content to a trained recruiter eye.
These phrases are overused, vague, or structurally identical to what every
AI-generated resume produces.

Usage:
  python ai_smell_checker.py '{"text": "Spearheaded cross-functional initiatives..."}'

Output:
  {
    "flags": [
      {"phrase": "Spearheaded", "reason": "Overused AI action verb", "line": 1}
    ],
    "flag_count": 1,
    "status": "warn",
    "message": "1 AI-smell phrase detected. Rewrite flagged items."
  }

Status: "pass" (0 flags), "warn" (1–2 flags), "fail" (3+ flags)
"""

import json
import sys
import re

# ─────────────────────────────────────────────────────────────────────────────
# BANNED ACTION VERBS — overused in AI-generated resumes
# These are not inherently bad words, but their overuse makes them AI signals.
# ─────────────────────────────────────────────────────────────────────────────
BANNED_VERBS = {
    "spearheaded", "championed", "orchestrated", "catalyzed", "evangelized",
    "synergized", "leveraged", "utilized", "facilitated", "streamlined",
    "revolutionized", "transformed", "pioneered", "architected", "garnered",
    "curated", "ideated", "conceptualized", "socialized", "operationalized",
    "institutionalized", "systematized", "galvanized",
}

# ─────────────────────────────────────────────────────────────────────────────
# BANNED PHRASES — verbatim strings that scream AI generation
# ─────────────────────────────────────────────────────────────────────────────
BANNED_PHRASES = [
    # Generic intensity phrases
    "resulted in significant", "significant improvement", "significant increase",
    "significant reduction", "significant impact", "significant growth",
    "dramatically improved", "dramatically reduced", "dramatically increased",
    "substantially improved", "substantially reduced",

    # Vague outcome claims
    "key stakeholders", "cross-functional stakeholders", "various stakeholders",
    "end-to-end ownership", "end-to-end responsibility", "end-to-end delivery",
    "full ownership", "took ownership of", "owned the entire",
    "holistic approach", "holistic solution", "holistic strategy",

    # Thought-leadership fluff
    "thought leadership", "best-in-class", "world-class", "industry-leading",
    "cutting-edge", "state-of-the-art", "next-generation", "game-changing",
    "groundbreaking", "innovative solutions", "robust solution",
    "seamless experience", "seamless integration",

    # AI writing tells
    "i am excited to", "i am passionate about", "i am dedicated to",
    "i believe i would be", "i am a results-driven", "results-oriented professional",
    "dynamic and results-driven", "proven track record of",
    "in today's fast-paced", "in a fast-paced environment",
    "leveraging my expertise", "leveraging my experience",
    "harnessing the power of",

    # Cover letter openers
    "i am writing to express my interest",
    "i am excited to apply",
    "please find my resume attached",
    "i would be a great fit",
    "i am a perfect fit",

    # Vague soft-skill claims
    "strong communication skills", "excellent communication skills",
    "strong leadership skills", "excellent leadership skills",
    "strong interpersonal skills", "excellent interpersonal skills",
    "team player", "self-starter", "go-getter", "outside the box",
    "detail-oriented professional",
]

# ─────────────────────────────────────────────────────────────────────────────
# STRUCTURAL PATTERNS (regex)
# ─────────────────────────────────────────────────────────────────────────────
BANNED_PATTERNS = [
    (r'\d+%\s+increase\s+in\s+efficiency', "Vague efficiency claim — specify the metric"),
    (r'(improved|increased|reduced|enhanced)\s+(overall\s+)?(performance|efficiency|productivity)\s+by', "Vague performance claim — needs concrete metric"),
    (r'successfully\s+(launched|delivered|completed|executed)', '"Successfully" is filler — lead with the verb alone'),
    (r'passionate\s+about\s+(building|creating|delivering)', '"Passionate about" is resume cliché'),
    (r'strong\s+sense\s+of\s+ownership', 'Vague ownership claim — show with specifics'),
    (r'ability\s+to\s+(work|collaborate|communicate|manage)', '"Ability to" is weak — rewrite as demonstrated fact'),
]


def check_text(text: str):
    flags = []
    lines = text.split('\n')

    for line_num, line in enumerate(lines, 1):
        line_lower = line.lower()

        # Check banned verbs (match at word boundary, case-insensitive)
        for verb in BANNED_VERBS:
            if re.search(r'\b' + re.escape(verb) + r'\b', line_lower):
                flags.append({
                    "phrase": verb.capitalize(),
                    "reason": "Overused AI action verb — swap for specific, less common alternative",
                    "line": line_num,
                    "text_excerpt": line.strip()[:80]
                })

        # Check banned phrases
        for phrase in BANNED_PHRASES:
            if phrase.lower() in line_lower:
                flags.append({
                    "phrase": phrase,
                    "reason": "AI-generated language pattern — rewrite with specific evidence",
                    "line": line_num,
                    "text_excerpt": line.strip()[:80]
                })

        # Check regex patterns
        for pattern, reason in BANNED_PATTERNS:
            if re.search(pattern, line_lower):
                flags.append({
                    "phrase": f"Pattern: {pattern}",
                    "reason": reason,
                    "line": line_num,
                    "text_excerpt": line.strip()[:80]
                })

    # Deduplicate by (phrase, line)
    seen = set()
    deduped = []
    for f in flags:
        key = (f["phrase"].lower(), f["line"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)

    count = len(deduped)
    if count == 0:
        status, msg = "pass", "No AI-smell phrases detected ✓"
    elif count <= 2:
        status, msg = "warn", f"{count} AI-smell phrase(s) detected — rewrite flagged items before delivery"
    else:
        status, msg = "fail", f"{count} AI-smell phrases detected — significant rewrite needed"

    return {
        "flags": deduped,
        "flag_count": count,
        "status": status,
        "message": msg
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Pass JSON as first arg: '{\"text\": \"...\"}' "}))
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    text = payload.get("text", "")
    if not text:
        print(json.dumps({"error": "No text provided"}))
        sys.exit(1)

    result = check_text(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
