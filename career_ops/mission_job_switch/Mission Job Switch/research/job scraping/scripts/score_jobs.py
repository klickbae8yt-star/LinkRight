"""
score_jobs.py — Semantic scoring of all unscored jobs via sentence-transformers.

Embeds Satvik's career profile once → saves to db/profile_embedding.npy.
For each job with relevance_score IS NULL: embed (title + description) →
cosine similarity vs profile → store as relevance_score (0–100).

Ghost job detection: if new job similarity > 0.95 vs any already-scored job
with same company → mark is_ghost=1 (repost detected).

Usage:
  python3 scripts/score_jobs.py               # score all unscored jobs
  python3 scripts/score_jobs.py --rescore-all # re-score everything (e.g. after profile update)
  python3 scripts/score_jobs.py --top 20      # print top 20 after scoring

Install:
  pip install sentence-transformers
"""

import argparse
import sqlite3
from pathlib import Path

import numpy as np

BASE         = Path(__file__).parent.parent
DB_PATH      = BASE / "db" / "jobs.db"
PROFILE_PATH = BASE / "db" / "profile_embedding.npy"
MODEL_NAME   = "all-MiniLM-L6-v2"  # 80MB, free, local, ~14ms/embed on CPU

# ─── SATVIK'S CAREER PROFILE (source for embedding) ───────────────────────────
# Update this if profile changes substantially. Re-run with --rescore-all after.
PROFILE_TEXT = """
Senior Product Analyst and Product Manager with 3+ years experience.
IIT Delhi Civil Engineering. Sprinklr 2022–2024: Senior Product Analyst.
Built GenAI root-cause engine for Walmart Spark — 6 data sources, L1/L2/L3 taxonomy,
7-day to same-day time-to-insight, $1.2M TCV, $9M pipeline.
Qatar Central Government Body: $32M 5-year partnership, 40 ministries,
Sharek iOS app, NLP dashboard, 7-day retention 40% to 55%, 2 days to 2 hours insight.
Use Case Hub: 35% to 85% adoption, 75% TTV reduction.
American Express 2024–present: Senior Associate PM on AML CRR platform.
100M+ accounts, 40 markets, build-vs-buy evaluation, 3-year roadmap, 60+ features,
4 consecutive zero-spillover PIs, 70% speed-to-market reduction (10 days to 3 days).
CDL strategy: 5-step data pipeline, 54 data points, 96.5% coverage.
G1L2 rating (highest among 30 POs), 120% bonus.
LinkRight: AI career OS, solo founder, shipped to PyPI, 77% of 57 issues closed.
8-9K LinkedIn followers. Strong in: AI/LLM products, fintech, AML compliance,
B2C consumer products, enterprise SaaS, social media analytics,
customer success, implementation, growth, product marketing.
Skills: product strategy, roadmap, OKRs, stakeholder management, agile, sprints,
data analytics, SQL, Python, GenAI, LLM, NLP, RAG, machine learning products.
Target: PM, AI PM, Growth Manager, CSM, Implementation Manager, PMM, TPM,
Chief of Staff, Founding PM at B2C companies in India or remote.
"""


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def load_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("ERROR: sentence-transformers not installed.")
        print("Run: pip install sentence-transformers")
        raise
    print(f"  Loading model: {MODEL_NAME} (downloads ~80MB first time)...")
    return SentenceTransformer(MODEL_NAME)


def get_or_build_profile_vec(model) -> np.ndarray:
    if PROFILE_PATH.exists():
        vec = np.load(PROFILE_PATH)
        print(f"  Profile embedding loaded from {PROFILE_PATH}")
        return vec
    print("  Building profile embedding (first time)...")
    vec = model.encode(PROFILE_TEXT, normalize_embeddings=True)
    np.save(PROFILE_PATH, vec)
    print(f"  Saved to {PROFILE_PATH}")
    return vec


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--rescore-all", action="store_true",
                   help="Re-score all jobs, not just unscored ones")
    p.add_argument("--top", type=int, default=0,
                   help="Print top N jobs by score after scoring")
    return p.parse_args()


def main():
    args = parse_args()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    if args.rescore_all:
        rows = conn.execute(
            "SELECT id, title, company, job_description FROM jobs WHERE is_ghost=0 OR is_ghost IS NULL"
        ).fetchall()
        print(f"Rescore mode: {len(rows)} jobs")
    else:
        rows = conn.execute(
            "SELECT id, title, company, job_description FROM jobs WHERE relevance_score IS NULL AND (is_ghost=0 OR is_ghost IS NULL)"
        ).fetchall()
        print(f"Unscored jobs to process: {len(rows)}")

    if not rows:
        print("Nothing to score.")
        if args.top:
            _print_top(conn, args.top)
        conn.close()
        return

    model      = load_model()
    profile_vec = get_or_build_profile_vec(model)

    # Build texts to embed
    texts = []
    for r in rows:
        title = (r["title"] or "").strip()
        desc  = (r["job_description"] or "")[:2000].strip()
        texts.append(f"{title}. {desc}" if desc else title)

    print(f"  Embedding {len(texts)} jobs...")
    job_vecs = model.encode(texts, normalize_embeddings=True, batch_size=32, show_progress_bar=True)

    # Ghost detection: load already-scored vecs for same-company comparison
    # Key: company_lower → list of (job_id, vec)
    scored_vecs: dict[str, list[tuple[int, np.ndarray]]] = {}
    if not args.rescore_all:
        scored_rows = conn.execute(
            "SELECT id, company, title, job_description FROM jobs WHERE relevance_score IS NOT NULL AND is_ghost=0"
        ).fetchall()
        if scored_rows:
            scored_texts = []
            for sr in scored_rows:
                t = (sr["title"] or "").strip()
                d = (sr["job_description"] or "")[:2000].strip()
                scored_texts.append(f"{t}. {d}" if d else t)
            scored_job_vecs = model.encode(scored_texts, normalize_embeddings=True, batch_size=32)
            for sr, sv in zip(scored_rows, scored_job_vecs):
                key = (sr["company"] or "").lower()
                scored_vecs.setdefault(key, []).append((sr["id"], sv))

    scored_count = ghost_count = 0
    updates = []

    for row, vec in zip(rows, job_vecs):
        job_id  = row["id"]
        company = (row["company"] or "").lower()

        # Ghost check: similarity > 0.95 vs any already-scored job at same company
        is_ghost = 0
        if company in scored_vecs:
            for _, existing_vec in scored_vecs[company]:
                if cosine_similarity(vec, existing_vec) > 0.95:
                    is_ghost = 1
                    ghost_count += 1
                    break

        score = round(cosine_similarity(vec, profile_vec) * 100, 2)
        updates.append((score, is_ghost, job_id))

        # Add to scored_vecs so subsequent jobs in this batch can detect ghosts against it
        if is_ghost == 0:
            scored_vecs.setdefault(company, []).append((job_id, vec))

        scored_count += 1

    conn.executemany(
        "UPDATE jobs SET relevance_score=?, is_ghost=? WHERE id=?",
        updates
    )
    conn.commit()

    print(f"\n  Scored     : {scored_count}")
    print(f"  Ghosts     : {ghost_count}  (repost suppressed, score stored but flagged)")

    if args.top:
        _print_top(conn, args.top)

    conn.close()
    print(f"\nNext: python3 scripts/update_excel.py")


def _print_top(conn: sqlite3.Connection, n: int):
    rows = conn.execute("""
        SELECT title, company, location, role_category, sector,
               relevance_score, is_remote, job_url
        FROM jobs
        WHERE is_ghost=0 AND relevance_score IS NOT NULL
        ORDER BY relevance_score DESC
        LIMIT ?
    """, (n,)).fetchall()
    print(f"\nTop {n} jobs by relevance score:")
    print(f"  {'Score':>5}  {'Cat':12}  {'Sector':18}  {'Title':40}  Company")
    print(f"  {'-'*5}  {'-'*12}  {'-'*18}  {'-'*40}  {'-'*20}")
    for r in rows:
        remote  = " [R]" if r["is_remote"] else ""
        sector  = (r["sector"] or "—")[:18]
        cat     = (r["role_category"] or "—")[:12]
        title   = (r["title"] or "")[:40]
        company = (r["company"] or "")[:20]
        print(f"  {r['relevance_score']:>5.1f}  {cat:12}  {sector:18}  {title:40}  {company}{remote}")


if __name__ == "__main__":
    main()
