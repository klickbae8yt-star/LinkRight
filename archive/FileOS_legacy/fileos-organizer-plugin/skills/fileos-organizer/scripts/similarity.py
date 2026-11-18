#!/usr/bin/env python3
"""
FileOS Near-Duplicate Detection Engine.
Pure Python standard library implementation of n-gram shingling and Jaccard similarity
to detect edited copies, drafts vs finals, and version drift across documents.
"""

import csv
import dataclasses
import json
from pathlib import Path
import re
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

@dataclasses.dataclass
class NearDuplicatePair:
    pair_id: str
    file_a: str
    file_b: str
    similarity_score: float
    size_a_bytes: int
    size_b_bytes: int
    size_diff_bytes: int
    stem_a: str
    stem_b: str
    suggested_action: str
    evidence: str

def normalize_text_for_shingling(text: str) -> str:
    """Lowercases, normalizes whitespace, strips punctuation noise."""
    t = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", t).strip()

def get_character_shingles(text: str, k: int = 4) -> Set[str]:
    """Generates a set of character k-grams from text."""
    norm = normalize_text_for_shingling(text)
    if len(norm) < k:
        return {norm} if norm else set()
    return {norm[i:i+k] for i in range(len(norm) - k + 1)}

def get_word_shingles(text: str, k: int = 2) -> Set[str]:
    """Generates word n-grams (default 2-grams / bigrams)."""
    words = normalize_text_for_shingling(text).split()
    if len(words) < k:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i:i+k]) for i in range(len(words) - k + 1)}

def compute_jaccard_similarity(set_a: Set[str], set_b: Set[str]) -> float:
    """Computes Jaccard index |A & B| / |A | B|."""
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return 0.0
    return intersection / union

class NearDuplicateDetector:
    def __init__(self, threshold: float = 0.85, max_files_to_compare: int = 500):
        self.threshold = threshold
        self.max_files_to_compare = max_files_to_compare

    def find_near_duplicates(
        self,
        files: List[Any], # List of FileRecord or Dict
        read_text_func: Callable[[str], str]
    ) -> List[NearDuplicatePair]:
        """
        Detects pairs of files that have distinct SHA-256 hashes but high text similarity.
        Compares candidate pairs efficiently by prioritizing:
        1. Files sharing the same normalized stem or family.
        2. Files with similar sizes (within 2x ratio) and text-compatible extensions.
        """
        # Filter files eligible for text similarity
        text_extensions = {".txt", ".md", ".csv", ".json", ".py", ".sh", ".html", ".js", ".css", ".yaml", ".yml", ".xml", ".docx", ".rtf"}
        
        candidates = []
        for f in files:
            ext = getattr(f, "extension", "") or (f.get("extension", "") if isinstance(f, dict) else "")
            size = getattr(f, "size_bytes", 0) or (f.get("size_bytes", 0) if isinstance(f, dict) else 0)
            sha = getattr(f, "sha256", None) or (f.get("sha256") if isinstance(f, dict) else None)
            rel_path = getattr(f, "rel_path", "") or (f.get("rel_path", "") if isinstance(f, dict) else "")
            stem = getattr(f, "normalized_stem", "") or (f.get("normalized_stem", "") if isinstance(f, dict) else "")
            
            if ext.lower() in text_extensions and size > 0 and size < 2_000_000 and sha:
                candidates.append({
                    "rel_path": rel_path,
                    "stem": stem,
                    "sha256": sha,
                    "size": size,
                    "ext": ext.lower()
                })

        if len(candidates) > self.max_files_to_compare:
            candidates = candidates[:self.max_files_to_compare]

        # Precompute shingles cache: rel_path -> set of shingles
        shingles_cache: Dict[str, Set[str]] = {}
        for c in candidates:
            rp = c["rel_path"]
            try:
                raw_text = read_text_func(rp)
                if raw_text:
                    shingles_cache[rp] = get_word_shingles(raw_text, k=2) | get_character_shingles(raw_text, k=4)
                else:
                    shingles_cache[rp] = set()
            except Exception:
                shingles_cache[rp] = set()

        pairs: List[NearDuplicatePair] = []
        seen_pairs = set()
        pair_counter = 1

        n = len(candidates)
        for i in range(n):
            c_a = candidates[i]
            s_a = shingles_cache.get(c_a["rel_path"])
            if not s_a:
                continue

            for j in range(i + 1, n):
                c_b = candidates[j]
                # If exact duplicate, skip (already handled by exact duplicate detector)
                if c_a["sha256"] == c_b["sha256"]:
                    continue

                # Size sanity filter: if sizes differ by > 3x, unlikely near-duplicates
                min_sz = min(c_a["size"], c_b["size"])
                max_sz = max(c_a["size"], c_b["size"])
                if min_sz > 0 and (max_sz / min_sz) > 3.0:
                    continue

                s_b = shingles_cache.get(c_b["rel_path"])
                if not s_b:
                    continue

                sim = compute_jaccard_similarity(s_a, s_b)
                if sim >= self.threshold:
                    pair_key = tuple(sorted([c_a["rel_path"], c_b["rel_path"]]))
                    if pair_key in seen_pairs:
                        continue
                    seen_pairs.add(pair_key)

                    diff_sz = abs(c_a["size"] - c_b["size"])
                    evidence = f"High content similarity ({sim:.1%}) with distinct SHA256 checksums. Size difference: {diff_sz} bytes."
                    
                    pairs.append(NearDuplicatePair(
                        pair_id=f"NDP-{pair_counter:03d}",
                        file_a=c_a["rel_path"],
                        file_b=c_b["rel_path"],
                        similarity_score=round(sim, 3),
                        size_a_bytes=c_a["size"],
                        size_b_bytes=c_b["size"],
                        size_diff_bytes=diff_sz,
                        stem_a=c_a["stem"],
                        stem_b=c_b["stem"],
                        suggested_action="review_diff_and_archive_older",
                        evidence=evidence
                    ))
                    pair_counter += 1

        # Sort pairs by highest similarity score first
        pairs.sort(key=lambda p: p.similarity_score, reverse=True)
        return pairs

    def write_csv(self, pairs: List[NearDuplicatePair], output_path: Path):
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "pair_id", "file_a", "file_b", "similarity_score",
                "size_a_bytes", "size_b_bytes", "size_diff_bytes",
                "stem_a", "stem_b", "suggested_action", "evidence"
            ])
            for p in pairs:
                writer.writerow([
                    p.pair_id, p.file_a, p.file_b, f"{p.similarity_score:.3f}",
                    p.size_a_bytes, p.size_b_bytes, p.size_diff_bytes,
                    p.stem_a, p.stem_b, p.suggested_action, p.evidence
                ])

    def write_jsonl(self, pairs: List[NearDuplicatePair], output_path: Path):
        with open(output_path, "w", encoding="utf-8") as f:
            for p in pairs:
                f.write(json.dumps(dataclasses.asdict(p)) + "\n")

