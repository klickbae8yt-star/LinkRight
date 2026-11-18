#!/usr/bin/env python3
"""Hybrid BM25 + Semantic Concept Vector + RRF (k=60) Resume-to-JD Matcher
with 6-Category Phrase-Level Intent Identification.

Indexes Satvik Jain's verified Bullet Bank v7 (114 lines) and maps any Job
Description at phrase level across:
  Leadership | Customer | Impact | Applied AI | Technology | Domain

Also enforces the coding-language guardrail (rejects pure Java/C++/Go/SWE roles)
while scoring hybrid AI Builder / Forward Deployed PM / PM / PMM / SPM / CoS roles
independent of exact job title.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BULLET_BANK = (
    ROOT / "05_resume_portfolio" / "Satvik_Resume_v7"
    / "bullet_bank" / "bullet_bank_v7_2026-10-23.md"
)
TRAINING_OUT = ROOT / "03_job_enrichment" / "training_data" / "phrase_intent_dataset.jsonl"

INTENT_CATEGORIES: dict[str, tuple[str, ...]] = {
    "Leadership": (
        "roadmap", "strategy", "strategic", "align", "aligned", "alignment",
        "stakeholder", "stakeholders", "vp", "svp", "executive", "leadership",
        "sole pm", "owned", "owner", "ownership", "priorit", "backlog",
        "sprint", "quarterly plan", "coached", "managed", "hired", "led",
        "cross-functional", "decision", "steering", "chief of staff", "founder",
    ),
    "Customer": (
        "client", "clients", "customer", "customers", "partner", "partners",
        "interview", "interviews", "uat", "acceptance testing", "pilot", "poc",
        "proof-of-concept", "proof of concept", "onboarding", "adoption",
        "retention", "csat", "support", "implementation", "account", "user research",
        "feedback", "discovery", "go-live", "deploy", "forward deployed",
    ),
    "Impact": (
        "million", "revenue", "contract", "deal", "conversion", "converted",
        "lifted", "grew", "growth", "cut", "reduced", "faster", "saving",
        "saved", "award", "gold medal", "top performer", "highest rating",
        "zero spillover", "sla", "f1", "pass rate", "uptime", "roi", "kpi",
    ),
    "Applied AI": (
        "ai", "llm", "llms", "large language", "prompt", "evaluation", "eval",
        "classifier", "sentiment", "whisper", "speech-to-text", "voice",
        "n8n", "claude", "agent", "agents", "agentic", "agentic loop",
        "self-improving", "feedback loop", "orchestration", "automation",
        "taxonomy", "clustering", "root-cause", "ml", "machine learning", "genai", "rag",
    ),
    "Technology": (
        "api", "apis", "sql", "python", "json", "figma", "jira", "rally",
        "pipeline", "staging", "qa", "idempotency", "dead-letter", "webhook",
        "iso 20022", "state machine", "schema", "workflow", "chrome extension",
        "react", "node", "webrtc", "cli", "ci/cd", "unit tests", "architecture",
    ),
    "Domain": (
        "payment", "payments", "stablecoin", "wire", "sepa", "direct-debit",
        "aml", "compliance", "risk-rating", "fintech", "banking", "social",
        "creator", "content", "marketing", "youtube", "media", "ecommerce",
        "quick-commerce", "saas", "enterprise", "hiring", "recruitment", "b2c", "b2b",
    ),
}

CONCEPT_CLUSTERS: dict[str, tuple[str, ...]] = {
    "concept_0_to_1": ("0-to-1", "zero to one", "brief to mvp", "mvp", "greenfield", "from scratch", "founding", "new product", "prototype", "prototyped", "pilot", "poc"),
    "concept_fde_pm": ("forward deployed", "implementation consultant", "poc", "proof-of-concept", "go-live", "customer deployment", "client", "solutions", "onboarding", "uat", "deployment strategist"),
    "concept_ai_builder": ("ai builder", "agentic", "agentic loop", "self-improving", "feedback loop", "orchestration", "scalable systems", "claude code", "codex", "cursor", "antigravity", "mcp", "multi-agent", "n8n", "claude", "llm", "prompt", "eval", "evaluation", "whisper", "agent", "workflow", "automation", "rapidly", "fast"),
    "concept_partner_gtm": ("partner", "partners", "bank-partner", "strategic partner", "ecosystem", "adoption", "content", "creator", "marketing", "launch", "gtm"),
    "concept_exec_ops": ("chief of staff", "founder", "svp", "vp", "steering", "quarterly plan", "40 stakeholders", "6 squads", "cross-functional", "roadmap"),
    "concept_research": ("interview", "interviews", "discovery", "root-cause", "taxonomy", "user research", "figma", "ux", "workflow"),
}

HARD_CODING_SWE_RE = re.compile(
    r"\b(java|c\+\+|c#|golang|rust|scala|kotlin|swift|objective-c|\.net|"
    r"spring boot|kubernetes operator|distributed systems engineer|low-latency c\+\+|"
    r"leetcode|algorithms and data structures|production backend code|"
    r"5\+ years of software engineering|staff software engineer|senior software engineer)\b",
    re.I,
)
PM_BUILDER_SIGNAL_RE = re.compile(
    r"\b(product manager|product management|product owner|product marketing|pmm|"
    r"forward deployed pm|forward deployed product|deployment strategist|"
    r"ai builder|agentic|n8n|claude code|cursor|no-code|low-code|figma|prd|roadmap|"
    r"chief of staff|founder'?s office|partner manager|partnerships|solutions consultant|"
    r"implementation consultant|customer success|strategy & operations)\b",
    re.I,
)


def tokenize(text: str) -> list[str]:
    low = (text or "").lower()
    raw = re.findall(r"[a-z0-9][a-z0-9+\-/.]*", low)
    tokens: list[str] = []
    for tok in raw:
        tok = tok.strip(".-/")
        if len(tok) < 2:
            continue
        # Light stemming for common suffixes
        for suf in ("ations", "ation", "ments", "ment", "ing", "ed", "ers", "es", "s"):
            if len(tok) > len(suf) + 3 and tok.endswith(suf):
                tok = tok[: -len(suf)]
                break
        tokens.append(tok)
    for cname, triggers in CONCEPT_CLUSTERS.items():
        if any(t in low for t in triggers):
            tokens.append(cname)
    return tokens


def categorize_phrase(phrase: str) -> tuple[str, dict[str, int]]:
    low = (phrase or "").lower()
    scores: dict[str, int] = {}
    for cat, kws in INTENT_CATEGORIES.items():
        hits = 0
        for kw in kws:
            if len(kw) <= 3:
                if re.search(rf"\b{re.escape(kw)}\b", low):
                    hits += 1
            elif kw in low:
                hits += 1
        if cat == "Impact" and re.search(r"\d+%|\$\d|\d+x\b|\d+k\b|\d+m\b", low):
            hits += 2
        if hits:
            scores[cat] = hits
    if not scores:
        return "Domain", {"Domain": 1}
    primary = max(scores.items(), key=lambda kv: kv[1])[0]
    return primary, scores


ADDENDUM_BANK = ROOT / "05_resume_portfolio" / "agentic_builder_addendum.md"


def load_bullet_bank(path: Path = DEFAULT_BULLET_BANK) -> list[dict[str, Any]]:
    """Parse bullet_bank_v7 markdown + addendum into deduplicated evidence records (preferring L2)."""
    by_id: dict[str, dict[str, Any]] = {}
    sources = [path] + ([ADDENDUM_BANK] if ADDENDUM_BANK.exists() else [])
    for src_path in sources:
        section = "General"
        for line in src_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                section = line[3:].strip()
                continue
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) < 6 or parts[0] in ("ID", "---"):
                continue
            bid, ver, _fill, _width, on_flag, text = parts[:6]
            if not bid or not text:
                continue
            existing = by_id.get(bid)
            if existing and existing["ver"] == "L2" and ver != "L2":
                continue
            primary_cat, cat_scores = categorize_phrase(text)
            by_id[bid] = {
                "bullet_id": bid,
                "ver": ver,
                "section": section,
                "on": on_flag,
                "text": text,
                "tokens": tokenize(f"{section} {text}"),
                "primary_intent": primary_cat,
                "intent_scores": cat_scores,
            }
    return list(by_id.values())


class HybridRRFIndex:
    """Combines Okapi BM25 and TF-IDF Concept Vector Cosine via RRF (k=60)."""

    def __init__(self, docs: list[dict[str, Any]], rrf_k: int = 60) -> None:
        self.docs = docs
        self.rrf_k = rrf_k
        self.n_docs = max(1, len(docs))
        self.doc_freqs: Counter[str] = Counter()
        self.doc_lens: list[int] = []
        self.doc_tfs: list[Counter[str]] = []

        for d in docs:
            toks = d["tokens"]
            self.doc_lens.append(len(toks))
            tf = Counter(toks)
            self.doc_tfs.append(tf)
            for t in tf:
                self.doc_freqs[t] += 1

        self.avg_dl = sum(self.doc_lens) / self.n_docs
        self.idf: dict[str, float] = {
            t: math.log(1.0 + (self.n_docs - df + 0.5) / (df + 0.5))
            for t, df in self.doc_freqs.items()
        }
        # Precompute L2-normalized TF-IDF vectors for semantic/concept cosine retrieval
        self.doc_vecs: list[dict[str, float]] = []
        self.doc_norms: list[float] = []
        for tf in self.doc_tfs:
            vec = {t: (1.0 + math.log(c)) * self.idf.get(t, 1.0) for t, c in tf.items()}
            norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
            self.doc_vecs.append(vec)
            self.doc_norms.append(norm)

    def _bm25_scores(self, q_tokens: list[str], k1: float = 1.5, b: float = 0.75) -> list[float]:
        scores = [0.0] * self.n_docs
        q_set = set(q_tokens)
        for i, tf in enumerate(self.doc_tfs):
            dl = self.doc_lens[i]
            s = 0.0
            for t in q_set:
                f = tf.get(t, 0)
                if not f:
                    continue
                idf = self.idf.get(t, 0.0)
                denom = f + k1 * (1.0 - b + b * dl / (self.avg_dl or 1.0))
                s += idf * (f * (k1 + 1.0)) / denom
            scores[i] = s
        return scores

    def _vec_scores(self, q_tokens: list[str]) -> list[float]:
        q_tf = Counter(q_tokens)
        q_vec = {t: (1.0 + math.log(c)) * self.idf.get(t, 0.5) for t, c in q_tf.items()}
        q_norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0
        scores = [0.0] * self.n_docs
        for i, d_vec in enumerate(self.doc_vecs):
            dot = sum(w * d_vec.get(t, 0.0) for t, w in q_vec.items())
            scores[i] = dot / (q_norm * self.doc_norms[i])
        return scores

    def search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        q_tokens = tokenize(query)
        if not q_tokens:
            return []
        bm25 = self._bm25_scores(q_tokens)
        vec = self._vec_scores(q_tokens)

        bm25_order = sorted(range(self.n_docs), key=lambda i: -bm25[i])
        vec_order = sorted(range(self.n_docs), key=lambda i: -vec[i])
        bm25_rank = {idx: r + 1 for r, idx in enumerate(bm25_order)}
        vec_rank = {idx: r + 1 for r, idx in enumerate(vec_order)}

        fused: list[tuple[float, int]] = []
        for i in range(self.n_docs):
            if bm25[i] <= 0 and vec[i] <= 0:
                continue
            rrf = (1.0 / (self.rrf_k + bm25_rank[i])) + (1.0 / (self.rrf_k + vec_rank[i]))
            fused.append((rrf, i))

        fused.sort(key=lambda x: -x[0])
        out: list[dict[str, Any]] = []
        for rrf_score, idx in fused[:top_k]:
            d = self.docs[idx]
            out.append({
                "bullet_id": d["bullet_id"],
                "section": d["section"],
                "primary_intent": d["primary_intent"],
                "text": d["text"],
                "rrf_score": round(rrf_score, 5),
                "bm25_score": round(bm25[idx], 3),
                "vec_score": round(vec[idx], 3),
            })
        return out


def split_jd_phrases(jd_text: str) -> list[str]:
    """Split a JD into clean requirement/responsibility phrases."""
    cleaned = re.sub(r"<[^>]+>", "\n", jd_text or "")
    raw_lines = re.split(r"[\n•●▪]+|(?<=[.!?])\s+", cleaned)
    phrases: list[str] = []
    for ln in raw_lines:
        s = re.sub(r"^\s*(?:[-*•]+|\d+[.)])\s+", "", ln).strip()
        if 25 <= len(s) <= 280 and not any(skip in s.lower() for skip in ("equal opportunity", "accommodation", "privacy policy", "cookie")):
            phrases.append(s)
    return phrases[:35]


def check_coding_gate(title: str, jd_text: str) -> tuple[bool, list[str]]:
    """Return (is_rejected_coding_swe, matched_coding_flags)."""
    blob = f"{title}\n{jd_text}"
    coding_hits = sorted({m.group(0).lower() for m in HARD_CODING_SWE_RE.finditer(blob)})
    pm_hits = PM_BUILDER_SIGNAL_RE.findall(title or "")
    # Reject if strong SWE coding requirements appear and title is not a PM/Builder/PMM/Partner role
    is_swe_title = bool(re.search(r"\b(software engineer|backend engineer|frontend engineer|sde|swe|forward deployed engineer)\b", title or "", re.I))
    if coding_hits and (is_swe_title or not pm_hits):
        return True, coding_hits
    return False, coding_hits


def evaluate_jd(title: str, jd_text: str, index: HybridRRFIndex) -> dict[str, Any]:
    rejected_coding, coding_flags = check_coding_gate(title, jd_text)
    phrases = split_jd_phrases(jd_text)
    if not phrases and jd_text.strip():
        phrases = [jd_text.strip()[:280]]

    phrase_matches: list[dict[str, Any]] = []
    matched_bullets: dict[str, dict[str, Any]] = {}
    intent_coverage: dict[str, list[float]] = {k: [] for k in INTENT_CATEGORIES}
    gaps: list[dict[str, str]] = []

    for ph in phrases:
        ph_intent, _ = categorize_phrase(ph)
        hits = index.search(ph, top_k=2)
        top = hits[0] if hits else None
        strength = (top["bm25_score"] * 0.25 + top["vec_score"] * 2.2) if top else 0.0
        intent_coverage[ph_intent].append(min(1.0, strength))

        is_strong = bool(top and (top["vec_score"] >= 0.20 or (top["bm25_score"] >= 6.5 and top["vec_score"] >= 0.14)))
        if is_strong and top:
            matched_bullets[top["bullet_id"]] = top
        else:
            gaps.append({"phrase": ph, "intent": ph_intent})

        phrase_matches.append({
            "jd_phrase": ph,
            "jd_intent": ph_intent,
            "strong_match": is_strong,
            "top_evidence": top,
        })

    strong_count = sum(1 for pm in phrase_matches if pm["strong_match"])
    coverage_ratio = strong_count / max(1, len(phrase_matches))
    raw_fit = round(min(100.0, coverage_ratio * 100.0 * 1.15), 1)
    if rejected_coding:
        raw_fit = min(raw_fit, 25.0)

    return {
        "title": title,
        "rejected_for_coding_swe": rejected_coding,
        "coding_flags": coding_flags,
        "fit_score": raw_fit,
        "total_jd_phrases": len(phrase_matches),
        "matched_phrases": strong_count,
        "intent_breakdown": {
            cat: {
                "jd_phrases": len(vals),
                "avg_strength": round(sum(vals) / len(vals), 2) if vals else 0.0,
            }
            for cat, vals in intent_coverage.items()
        },
        "top_strength_bullets": list(matched_bullets.values())[:8],
        "top_gaps": gaps[:6],
        "phrase_matches": phrase_matches[:15],
    }


def export_training_dataset(docs: list[dict[str, Any]], out_path: Path = TRAINING_OUT) -> int:
    """Export phrase-level intent dataset (JSONL) for fine-tuning a small classifier."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for d in docs:
        rec = {
            "id": d["bullet_id"],
            "text": d["text"],
            "primary_label": d["primary_intent"],
            "labels": sorted(d["intent_scores"].keys()),
            "section": d["section"],
        }
        lines.append(json.dumps(rec))
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Hybrid BM25+Vector+RRF JD-to-Resume Matcher")
    parser.add_argument("--title", default="Sample Role", help="Job title")
    parser.add_argument("--jd-file", default="", help="Path to text file with JD")
    parser.add_argument("--jd-text", default="", help="Inline JD text")
    parser.add_argument("--export-training", action="store_true", help="Export JSONL phrase-intent training dataset")
    args = parser.parse_args()

    docs = load_bullet_bank()
    index = HybridRRFIndex(docs)

    if args.export_training:
        n = export_training_dataset(docs)
        print(f"Exported {n} labeled evidence items -> {TRAINING_OUT}")

    jd = Path(args.jd_file).read_text(encoding="utf-8") if args.jd_file else args.jd_text
    if jd:
        res = evaluate_jd(args.title, jd, index)
        print(json.dumps(res, indent=2))
    elif not args.export_training:
        print(f"Indexed {len(docs)} unique verified bullets from {DEFAULT_BULLET_BANK.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
