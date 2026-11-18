"""
filter_pm_jobs.py — Clean existing jobs DB: keep PM-adjacent roles, delete clearly irrelevant ones.

Strategy: reverse filter. Only delete if title matches EXCLUDE list AND has no INCLUDE signal.
Uncertain titles (neither match) → kept for manual review.

Also adds new metadata columns to jobs table if missing.

Usage:
  python3 scripts/filter_pm_jobs.py [--dry-run]
"""

import re
import sqlite3
import sys
from pathlib import Path

BASE    = Path(__file__).parent.parent
DB_PATH = BASE / "db" / "jobs.db"

DRY_RUN = "--dry-run" in sys.argv

# ─── TARGET ROLES (INCLUDE) ────────────────────────────────────────────────────
# Tuple: (role_category, [keywords])  — ANY keyword match in title → keep + assign category

INCLUDE_RULES = [
    ("PM", [
        "product manager", "product management", "product owner", "product lead",
        "head of product", "vp product", "vp of product", "director of product",
        "director, product", "chief product", "principal product", "staff product",
        "group product", "associate product manager", "senior product manager",
        "product manager,", "product manager -", "product manager –",
    ]),
    ("AI_PM", [
        "ai product", "ai builder", "ai applications", "ai solutions",
        "llm product", "generative ai product", "machine learning product",
        "ml product", "applied ai", "ai/ml product", "conversational ai",
        "ai agent", "agentic", "foundation model", "ai platform product",
    ]),
    ("GROWTH", [
        "growth product", "product growth", "growth manager", "growth lead",
        "head of growth", "growth marketing manager", "growth pm",
        "growth hacker", "growth engineer", "vp growth", "director growth",
        "growth & product", "product & growth",
    ]),
    ("PMM", [
        "product marketing", "pmm", "go-to-market manager", "gtm manager",
        "product marketing lead", "product marketing director",
    ]),
    ("ANALYTICS_PM", [
        "product analyst", "data product manager", "analytics product",
        "product data analyst", "product insights",
    ]),
    ("CSM", [
        "customer success manager", "customer success lead", "director customer success",
        "head of customer success", "vp customer success", "client success manager",
        "customer experience manager", "customer success",
    ]),
    ("IMPLEMENTATION", [
        "implementation lead", "implementation manager", "implementation consultant",
        "solutions architect", "technical solutions manager", "solutions consultant",
        "enterprise implementation", "technical account manager", "tam",
        "implementation specialist", "onboarding manager", "launch manager",
        "deployment manager",
    ]),
    ("FINTECH_PM", [
        "compliance product", "risk product", "fintech product", "payments product",
        "aml product", "fraud product", "banking product", "lending product",
        "insurance product", "regtech", "credit product",
    ]),
    ("FOUNDING", [
        "founding pm", "founding product", "chief of staff",
    ]),
    ("TPM", [
        "technical program manager", "program manager", "tpm",
        "delivery lead", "delivery manager", "release manager",
        "project lead", "engagement manager",
    ]),
    ("GENERAL_PM", [
        "product specialist", "product strategist", "product operations",
        "product ops", "product manager", "product owner",
        "product designer",  # borderline but keep
        "product consultant", "product head",
    ]),
]

# ─── CLEAR EXCLUSIONS (delete if NO include match + any exclude match) ─────────
EXCLUDE_KEYWORDS = [
    # Engineering
    r"\bsoftware engineer\b", r"\bsde\b", r"\bswe\b",
    r"\bbackend engineer\b", r"\bfrontend engineer\b", r"\bfull.?stack engineer\b",
    r"\bsoftware developer\b", r"\bmobile engineer\b", r"\bandroid engineer\b",
    r"\bios engineer\b", r"\bfirmware engineer\b", r"\bembedded engineer\b",
    # Data/ML Engineering
    r"\bdata scientist\b", r"\bml engineer\b", r"\bmachine learning engineer\b",
    r"\bdeep learning engineer\b", r"\bdata engineer\b", r"\bai engineer\b",
    r"\bcomputer vision engineer\b", r"\bnlp engineer\b",
    # Design (non-product)
    r"\bux designer\b", r"\bui designer\b", r"\bgraphic designer\b",
    r"\bvisual designer\b", r"\bbrand designer\b", r"\bmotion designer\b",
    r"\billustrator\b",
    # Sales
    r"\baccount executive\b", r"\bsales executive\b", r"\bsales development\b",
    r"\bsdr\b", r"\bbdr\b", r"\binside sales\b", r"\bfield sales\b",
    # HR / People
    r"\brecruiter\b", r"\btalent acquisition\b", r"\bhr manager\b",
    r"\bhr business partner\b", r"\bpeople operations manager\b",
    r"\bcompensation analyst\b", r"\bbenefits specialist\b",
    # Finance (non-PM)
    r"\baccountant\b", r"\bcontroller\b", r"\bfinancial analyst\b",
    r"\bcfo\b", r"\bfinance manager\b", r"\bfp&a\b", r"\baudit\b",
    # Content / Marketing (non-PMM)
    r"\bcontent writer\b", r"\bcopywriter\b", r"\beditor\b",
    r"\bjournalist\b", r"\bseo specialist\b", r"\bsocial media manager\b",
    # Legal
    r"\blegal counsel\b", r"\blawyer\b", r"\bparalegal\b", r"\battorney\b",
    # DevOps / Infra
    r"\bdevops engineer\b", r"\bsre\b", r"\bsite reliability\b",
    r"\binfrastructure engineer\b", r"\bplatform engineer\b", r"\bcloud engineer\b",
    r"\bnetwork engineer\b", r"\bsecurity engineer\b",
    # QA
    r"\bqa engineer\b", r"\btest engineer\b", r"\bquality engineer\b",
    r"\bautomation engineer\b", r"\bsdet\b",
    # Entry level
    r"\bintern\b", r"\btrainee\b", r"\bfresher\b", r"\bapprentice\b",
    r"\bgraduate trainee\b",
    # Operations (standalone, non-product)
    r"\bwarehouse\b", r"\blogistics coordinator\b", r"\bsupply chain analyst\b",
    r"\bfleet manager\b", r"\bdelivery executive\b",
]

EXCLUDE_RES = [re.compile(p, re.I) for p in EXCLUDE_KEYWORDS]


def classify_title(title: str) -> str | None:
    """Returns role_category if title matches INCLUDE rules, else None."""
    t = title.lower()
    for category, keywords in INCLUDE_RULES:
        for kw in keywords:
            if kw in t:
                return category
    return None


def is_excluded(title: str) -> bool:
    t = title.lower()
    return any(pat.search(t) for pat in EXCLUDE_RES)


def ensure_columns(conn: sqlite3.Connection):
    cols = {r[1] for r in conn.execute("PRAGMA table_info(jobs)")}
    new_cols = [
        ("job_description", "TEXT"),
        ("compensation",    "TEXT"),
        ("years_experience","TEXT"),
        ("employment_type", "TEXT"),
        ("is_remote",       "INTEGER DEFAULT 0"),
        ("role_category",   "TEXT"),
    ]
    for col, defn in new_cols:
        if col not in cols:
            conn.execute(f"ALTER TABLE jobs ADD COLUMN {col} {defn}")
    conn.commit()


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_columns(conn)

    rows = conn.execute("SELECT id, title, company FROM jobs").fetchall()
    print(f"Total jobs in DB: {len(rows)}\n")

    kept = deleted = uncertain = categorized = 0
    to_delete = []
    to_update = []  # (role_category, id)

    for row in rows:
        title = (row["title"] or "").strip()
        job_id = row["id"]
        company = row["company"] or ""

        category = classify_title(title)

        if category:
            kept += 1
            categorized += 1
            to_update.append((category, job_id))
        elif is_excluded(title):
            deleted += 1
            to_delete.append(job_id)
            print(f"  DELETE  [{job_id:4d}] {company:30s} | {title}")
        else:
            uncertain += 1
            to_update.append(("UNCERTAIN", job_id))
            print(f"  KEEP?   [{job_id:4d}] {company:30s} | {title}")

    print(f"\n{'='*60}")
    print(f"Kept (matched include) : {kept}")
    print(f"Deleted (clear exclude): {deleted}")
    print(f"Uncertain (kept)       : {uncertain}")
    print(f"Total kept             : {kept + uncertain}")

    if DRY_RUN:
        print("\n[DRY RUN] No changes written.")
        conn.close()
        return

    # Write role_category updates
    conn.executemany("UPDATE jobs SET role_category=? WHERE id=?", to_update)

    # Delete irrelevant jobs
    if to_delete:
        conn.executemany("DELETE FROM jobs WHERE id=?", [(i,) for i in to_delete])

    conn.commit()
    conn.close()

    print(f"\nDone. Deleted {deleted} jobs, assigned categories to {categorized} jobs.")
    print(f"DB: {DB_PATH}")


if __name__ == "__main__":
    main()
