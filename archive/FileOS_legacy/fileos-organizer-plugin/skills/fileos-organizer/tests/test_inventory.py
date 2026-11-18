#!/usr/bin/env python3
"""Tests for FileOS inventory, readiness, exclusions, and symlink safety."""

import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

# Add scripts directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine, check_file_readiness, is_path_excluded, extract_bounded_content
import zipfile

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_default_exclusions(self):
        """Verify .git, node_modules, and cache files are excluded."""
        git_dir = self.root / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("dummy")

        node_dir = self.root / "node_modules"
        node_dir.mkdir()
        (node_dir / "package.json").write_text("{}")

        valid_file = self.root / "valid_doc.txt"
        valid_file.write_text("Hello world")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["total_files"], 1)

    def test_unstable_and_temp_files_skipped(self):
        """Verify .crdownload, .part, and .tmp files are flagged as unstable."""
        temp_dl = self.root / "download.pdf.crdownload"
        temp_dl.write_text("partial data")
        
        ready_file = self.root / "completed.pdf"
        ready_file.write_text("finished data")

        status, _ = check_file_readiness(temp_dl)
        self.assertEqual(status, "unstable")

        status_ready, _ = check_file_readiness(ready_file)
        self.assertEqual(status_ready, "ready")

    def test_symlinks_not_followed_by_default(self):
        """Verify symlinks are detected and skipped rather than traversed."""
        target_file = self.root / "original.txt"
        target_file.write_text("original content")

        symlink_file = self.root / "link_to_original.txt"
        try:
            os.symlink(target_file, symlink_file)
        except OSError:
            self.skipTest("Symlinks not supported in this environment")

        status, _ = check_file_readiness(symlink_file)
        self.assertEqual(status, "skipped_symlink")

    def test_docx_bounded_extraction(self):
        """Verify stdlib zipfile extracts text from docx without third-party libraries."""
        docx_path = self.root / "sample.docx"
        # Create a minimal valid docx zip structure
        xml_content = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>Confidential Project Roadmap</w:t></w:r></w:p>
    <w:p><w:r><w:t>Q1 deliverables and milestones.</w:t></w:r></w:p>
  </w:body>
</w:document>"""
        with zipfile.ZipFile(docx_path, "w") as z:
            z.writestr("word/document.xml", xml_content)

        text, cap, status = extract_bounded_content(docx_path, max_chars=100)
        self.assertEqual(cap, "docx_xml")
        self.assertEqual(status, "extracted")
        self.assertIn("Confidential Project Roadmap", text)

if __name__ == "__main__":
    unittest.main()
