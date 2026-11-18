#!/usr/bin/env python3
"""
Tests for FileOS Near-Duplicate Detection Engine.
Validates n-gram shingling, Jaccard similarity metrics, and full integration
with FileOSEngine.scan() producing near-duplicates.csv.
"""

import csv
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from similarity import (
    get_character_shingles,
    get_word_shingles,
    compute_jaccard_similarity,
    NearDuplicateDetector
)
from fileos import FileOSEngine

class TestNearDuplicateDetection(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="fileos_near_dup_")
        self.root = Path(self.test_dir) / "workspace"
        self.root.mkdir()
        self.out = Path(self.test_dir) / "output"
        self.out.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_shingle_and_jaccard_similarity_primitives(self):
        text_a = "The quick brown fox jumps over the lazy dog and rests in the garden."
        text_b = "The quick brown fox jumps over the lazy dog and sleeps in the garden."
        text_c = "Completely unrelated text about astrophysics and planetary orbital dynamics."

        shingles_a = get_word_shingles(text_a, k=2) | get_character_shingles(text_a, k=4)
        shingles_b = get_word_shingles(text_b, k=2) | get_character_shingles(text_b, k=4)
        shingles_c = get_word_shingles(text_c, k=2) | get_character_shingles(text_c, k=4)

        sim_ab = compute_jaccard_similarity(shingles_a, shingles_b)
        sim_ac = compute_jaccard_similarity(shingles_a, shingles_c)
        sim_aa = compute_jaccard_similarity(shingles_a, shingles_a)

        self.assertEqual(sim_aa, 1.0)
        self.assertGreater(sim_ab, 0.70)
        self.assertLess(sim_ac, 0.10)

    def test_detector_identifies_draft_and_final_versions(self):
        doc_v1 = (
            "Annual Strategic Product Plan 2026.\n"
            "Executive Summary: In 2026 we aim to deliver next-generation AI file management systems.\n"
            "Key objectives: Expand market presence, enhance performance, ensure high availability.\n"
            "Budget allocation: $1,500,000 for infrastructure and engineering operations.\n"
            "Timeline: Q1 launch, Q2 growth, Q3 enterprise expansion, Q4 internationalization.\n"
        )
        doc_v2 = (
            "Annual Strategic Product Plan 2026 - FINAL APPROVED.\n"
            "Executive Summary: In 2026 we aim to deliver next-generation AI file management systems.\n"
            "Key objectives: Expand market presence, enhance performance, ensure high availability.\n"
            "Budget allocation: $1,750,000 for infrastructure and engineering operations.\n"
            "Timeline: Q1 launch, Q2 growth, Q3 enterprise expansion, Q4 internationalization.\n"
        )
        unrelated = (
            "Cooking Recipe: Mediterranean lemon herb roasted chicken with rosemary potatoes.\n"
            "Ingredients: Olive oil, garlic, lemon juice, whole chicken, salt and black pepper.\n"
        )

        (self.root / "plan_draft.txt").write_text(doc_v1)
        (self.root / "plan_final.txt").write_text(doc_v2)
        (self.root / "recipe.txt").write_text(unrelated)

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()

        self.assertIn("near_duplicates", res)
        self.assertEqual(res["near_duplicates"], 1)

        near_dup_csv = self.out / "near-duplicates.csv"
        self.assertTrue(near_dup_csv.exists())

        with open(near_dup_csv, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 1)
            pair = reader[0]
            self.assertEqual(pair["pair_id"], "NDP-001")
            paths = {pair["file_a"], pair["file_b"]}
            self.assertEqual(paths, {"plan_draft.txt", "plan_final.txt"})
            self.assertGreaterEqual(float(pair["similarity_score"]), 0.85)

if __name__ == "__main__":
    unittest.main()

