#!/usr/bin/env python3
"""Tests for exact duplicate detection and content hashing."""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine

class TestDuplicates(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_identical_bytes_different_names_grouped_as_duplicates(self):
        """Files with identical bytes but different names and paths must be grouped as exact duplicates."""
        dir1 = self.root / "folder1"
        dir2 = self.root / "folder2"
        dir1.mkdir()
        dir2.mkdir()

        content = "Identical document content across copies."
        (dir1 / "original.txt").write_text(content)
        (dir2 / "copy_of_original.txt").write_text(content)

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["duplicate_groups"], 1)

    def test_same_name_different_content_not_duplicates(self):
        """Files with same name but different content must NOT be grouped as duplicates."""
        dir1 = self.root / "folder1"
        dir2 = self.root / "folder2"
        dir1.mkdir()
        dir2.mkdir()

        (dir1 / "notes.txt").write_text("Meeting notes from Monday")
        (dir2 / "notes.txt").write_text("Meeting notes from Friday - totally different")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["duplicate_groups"], 0)

if __name__ == "__main__":
    unittest.main()

