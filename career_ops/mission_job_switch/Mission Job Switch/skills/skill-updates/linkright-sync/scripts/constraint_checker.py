#!/usr/bin/env python3
"""
constraint_checker.py — Validate resume content against user_setup.md.

Reads the user's personal constraint file and checks resume text for violations.
Blocks delivery on any violation.

Usage:
  python constraint_checker.py '{"resume_text": "...", "setup_path": "/path/to/user_setup.md"}'

Output:
  {
    "violations": [
      {
        "type": "do_not_mention_company",
        "value": "ContentStack",
        "context": "...worked at ContentStack on...",
        "action": "REMOVE — this company must not appear in any output"
      }
    ],
    "violation_count": 1,
    "status": "fail",
    "message": "1 constraint violation found. Fix before delivery."
  }
"""

import json
import sys
import re
import os


def parse_user_setup(setup_path: str) -> dict:
    """
    Parse user_setup.md to extract constraint lists.
    Looks for YAML-style sections. Returns structured dict.
    Falls back to empty lists if file not found or sections missing.
    """
    constraints = {
        "do_not_mention_companies": [],
        "do_not_mention_projects": [],
        "do_not_mention_technologies": [],
        "do_not_mention_personal": [],
        "hard_constraints": [],
    }

    if not setup_path or not os.path.exists(setup_path):
        return constraints

    try:
        with open(setup_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return constraints

    # Parse YAML list items under known sections
    # Handles both "  - item" and "- item" under section headers

    def extract_list(section_header: str, text: str) -> list:
        """Extract list items following a section header."""
        items = []
        # Find the section
        pattern = re.compile(
            r'(?:^|\n)\s*' + re.escape(section_header) + r'\s*:?\s*\n((?:\s*-\s*.+\n?)*)',
            re.MULTILINE
        )
        match = pattern.search(text)
        if match:
            block = match.group(1)
            for line in block.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    item = line[2:].strip().strip('"').strip("'")
                    if item and item not in ('""', "''", ''):
                        items.append(item)
        return items

    constraints["do_not_mention_companies"] = extract_list("companies", content)
    constraints["do_not_mention_projects"] = extract_list("projects", content)
    constraints["do_not_mention_technologies"] = extract_list("technologies", content)
    constraints["do_not_mention_personal"] = extract_list("personal_info", content)

    # Parse hard_constraints descriptions
    hc_pattern = re.compile(r'description:\s*"([^"]+)"', re.MULTILINE)
    constraints["hard_constraints"] = hc_pattern.findall(content)

    return constraints


def check_resume(resume_text: str, constraints: dict) -> list:
    violations = []
    text_lower = resume_text.lower()

    # Check do_not_mention companies
    for company in constraints.get("do_not_mention_companies", []):
        if company and company.lower() in text_lower:
            # Find context
            idx = text_lower.find(company.lower())
            context = resume_text[max(0, idx-30):idx+len(company)+30].strip()
            violations.append({
                "type": "do_not_mention_company",
                "value": company,
                "context": f"...{context}...",
                "action": f"REMOVE — '{company}' must not appear in any output per user_setup.md"
            })

    # Check do_not_mention projects
    for project in constraints.get("do_not_mention_projects", []):
        if project and project.lower() in text_lower:
            idx = text_lower.find(project.lower())
            context = resume_text[max(0, idx-30):idx+len(project)+30].strip()
            violations.append({
                "type": "do_not_mention_project",
                "value": project,
                "context": f"...{context}...",
                "action": f"REMOVE — project '{project}' must not appear in any output per user_setup.md"
            })

    # Check do_not_mention technologies
    for tech in constraints.get("do_not_mention_technologies", []):
        if tech and re.search(r'\b' + re.escape(tech.lower()) + r'\b', text_lower):
            idx = text_lower.find(tech.lower())
            context = resume_text[max(0, idx-30):idx+len(tech)+30].strip()
            violations.append({
                "type": "do_not_mention_technology",
                "value": tech,
                "context": f"...{context}...",
                "action": f"REMOVE — technology '{tech}' must not appear per user_setup.md"
            })

    # Check personal info items
    for item in constraints.get("do_not_mention_personal", []):
        if item and item.lower() in text_lower:
            violations.append({
                "type": "do_not_mention_personal",
                "value": item,
                "context": "Personal information found in resume text",
                "action": f"REMOVE — personal info '{item}' must not appear per user_setup.md"
            })

    return violations


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Pass JSON: '{\"resume_text\": \"...\", \"setup_path\": \"...\"}'"}))
        sys.exit(1)

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}))
        sys.exit(1)

    resume_text = payload.get("resume_text", "")
    setup_path = payload.get("setup_path", "")

    if not resume_text:
        print(json.dumps({"error": "No resume_text provided"}))
        sys.exit(1)

    constraints = parse_user_setup(setup_path)

    if not setup_path or not os.path.exists(setup_path):
        print(json.dumps({
            "violations": [],
            "violation_count": 0,
            "status": "warn",
            "message": "user_setup.md not found — constraint check skipped. Run manually.",
            "constraints_loaded": False
        }, indent=2))
        return

    violations = check_resume(resume_text, constraints)
    count = len(violations)

    if count == 0:
        status = "pass"
        msg = "No constraint violations ✓"
    else:
        status = "fail"
        msg = f"{count} constraint violation(s) found. Fix before delivery."

    result = {
        "violations": violations,
        "violation_count": count,
        "status": status,
        "message": msg,
        "constraints_loaded": True,
        "constraint_counts": {
            "companies": len(constraints["do_not_mention_companies"]),
            "projects": len(constraints["do_not_mention_projects"]),
            "technologies": len(constraints["do_not_mention_technologies"]),
        }
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
