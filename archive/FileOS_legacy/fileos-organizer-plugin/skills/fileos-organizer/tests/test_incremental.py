#!/usr/bin/env python3
"""
Tests for FileOS Incremental Scan Engine (--incremental and .fileos-cache.json).
Verifies that unchanged files reuse cached hashes without physical disk reads,
and modified files are detected, re-read, and cache-updated.
"""

import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine

class TestIncrementalScan(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="fileos_inc_")
        self.root = Path(self.test_dir) / "workspace"
        self.root.mkdir()
        self.out = Path(self.test_dir) / "output"
        self.out.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_first_scan_creates_cache_and_reads_all_bytes(self):
        f1 = self.root / "file1.txt"
        f2 = self.root / "file2.txt"
        f1.write_text("Hello World from File 1")
        f2.write_text("Another File Content for File 2")
        total_size = len(f1.read_bytes()) + len(f2.read_bytes())

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan(incremental=True)

        cache_file = self.out / ".fileos-cache.json"
        self.assertTrue(cache_file.exists(), ".fileos-cache.json was not created")

        cache_data = json.loads(cache_file.read_text())
        self.assertIn("files", cache_data)
        self.assertIn("file1.txt", cache_data["files"])
        self.assertIn("file2.txt", cache_data["files"])

        cov = json.loads((self.out / "coverage.json").read_text())
        self.assertEqual(cov["bytes_read_for_hashing"], total_size)
        self.assertEqual(cov["bytes_reused_from_hash_cache"], 0)

    def test_second_scan_reuses_cache_without_reading_bytes(self):
        f1 = self.root / "file1.txt"
        f2 = self.root / "file2.txt"
        f1.write_text("Hello World from File 1")
        f2.write_text("Another File Content for File 2")
        total_size = len(f1.read_bytes()) + len(f2.read_bytes())

        # First scan
        engine = FileOSEngine(self.root, self.out)
        engine.scan(incremental=True)

        # Second scan with incremental=True
        engine2 = FileOSEngine(self.root, self.out)
        res2 = engine2.scan(incremental=True)

        cov2 = json.loads((self.out / "coverage.json").read_text())
        self.assertEqual(cov2["bytes_read_for_hashing"], 0)
        self.assertEqual(cov2["bytes_reused_from_hash_cache"], total_size)
        self.assertEqual(cov2["files_analysed"], 2)

    def test_incremental_scan_detects_modified_file(self):
        f1 = self.root / "file1.txt"
        f2 = self.root / "file2.txt"
        f1.write_text("Original content of file 1")
        f2.write_text("Content of file 2 that stays unchanged")

        engine = FileOSEngine(self.root, self.out)
        engine.scan(incremental=True)

        # Wait a tiny bit and update f1
        time.sleep(0.05)
        new_content = "Completely modified and new content for file 1!!!"
        f1.write_text(new_content)
        new_f1_size = len(new_content.encode("utf-8"))
        f2_size = len(f2.read_bytes())

        # Rescan
        engine2 = FileOSEngine(self.root, self.out)
        engine2.scan(incremental=True)

        cov = json.loads((self.out / "coverage.json").read_text())
        self.assertEqual(cov["bytes_read_for_hashing"], new_f1_size)
        self.assertEqual(cov["bytes_reused_from_hash_cache"], f2_size)
        self.assertEqual(cov["files_analysed"], 2)

    def test_single_file_mode_incremental(self):
        f = self.root / "single.txt"
        f.write_text("Single mode test content")
        size = len(f.read_bytes())

        engine = FileOSEngine(f, self.out)
        engine.scan(incremental=True)

        engine2 = FileOSEngine(f, self.out)
        engine2.scan(incremental=True)

        cov = json.loads((self.out / "coverage.json").read_text())
        self.assertEqual(cov["bytes_reused_from_hash_cache"], size)
        self.assertEqual(cov["bytes_read_for_hashing"], 0)

if __name__ == "__main__":
    unittest.main()

