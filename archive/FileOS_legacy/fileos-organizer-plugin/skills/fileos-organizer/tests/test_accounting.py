#!/usr/bin/env python3
"""
Tests for FileOS M1 non-overlapping inventory accounting equations
and truthful byte & duplicate metrics.
"""

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine

class TestAccountingInvariants(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="fileos_acc_")
        self.root = Path(self.test_dir) / "workspace"
        self.root.mkdir()
        self.out = Path(self.test_dir) / "output"
        self.out.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_non_overlapping_file_equation(self):
        """
        Validates:
        files_observed = files_excluded + files_eligible
        files_eligible = files_analysed + files_skipped + files_failed
        """
        # Create 2 normal files
        (self.root / "doc1.txt").write_text("content one")
        (self.root / "doc2.txt").write_text("content two")
        # Create 1 unstable download file
        (self.root / "doc3.crdownload").write_text("downloading...")

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()

        cov = json.loads((self.out / "coverage.json").read_text())

        # Equations
        self.assertEqual(cov["files_observed"], cov["files_excluded"] + cov["files_eligible"])
        self.assertEqual(cov["files_eligible"], cov["files_analysed"] + cov["files_skipped"] + cov["files_failed"])
        self.assertEqual(cov["files_analysed"], 2)
        self.assertEqual(cov["files_skipped"], 1)
        self.assertEqual(cov["files_failed"], 0)

    def test_non_overlapping_directory_equation(self):
        """
        Validates:
        directories_observed = directories_scanned + directories_excluded + directories_inaccessible + directories_depth_skipped
        """
        sub1 = self.root / "active_sub"
        sub1.mkdir()
        (sub1 / "f.txt").write_text("hello")

        excluded_sub = self.root / "ignored_sub"
        excluded_sub.mkdir()
        (excluded_sub / "f.txt").write_text("ignored")

        engine = FileOSEngine(self.root, self.out, exclusions=["ignored_sub"])
        engine.scan()

        cov = json.loads((self.out / "coverage.json").read_text())
        total_observed = cov["directories_observed"]
        sum_parts = (
            cov["directories_scanned"] +
            cov["directories_excluded"] +
            cov["directories_inaccessible"] +
            cov["directories_depth_skipped"]
        )
        self.assertEqual(total_observed, sum_parts)
        self.assertGreaterEqual(cov["directories_excluded"], 1)

    def test_truthful_duplicate_byte_metrics(self):
        """
        Validates separate tracking of duplicate_group_count, member_count,
        group_logical_bytes, and potential_extra_copy_bytes.
        """
        content = "Identical payload of exactly 32 bytes!"
        size = len(content.encode("utf-8"))

        (self.root / "copy1.txt").write_text(content)
        (self.root / "copy2.txt").write_text(content)
        (self.root / "copy3.txt").write_text(content)

        engine = FileOSEngine(self.root, self.out)
        engine.scan()

        cov = json.loads((self.out / "coverage.json").read_text())
        self.assertEqual(cov["duplicate_group_count"], 1)
        self.assertEqual(cov["duplicate_member_file_count"], 3)
        self.assertEqual(cov["duplicate_group_logical_bytes"], 3 * size)
        self.assertEqual(cov["potential_extra_copy_bytes"], 2 * size)

    def test_scan_id_and_fingerprint_generation(self):
        """Validates SCN-* ID generation and deterministic config fingerprint."""
        (self.root / "file.txt").write_text("data")

        engine = FileOSEngine(self.root, self.out)
        engine.scan()

        cov = json.loads((self.out / "coverage.json").read_text())
        self.assertTrue(cov["scan_id"].startswith("SCN-"))
        self.assertEqual(len(cov["scan_config_fingerprint"]), 64)

if __name__ == "__main__":
    unittest.main()

