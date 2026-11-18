#!/usr/bin/env python3
"""Tests for document family grouping, version token parsing, and authoritative flags."""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine, parse_version_tokens

class TestVersions(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_version_token_parsing(self):
        """Test normalization and lifecycle extraction for various version names."""
        stem1, v1 = parse_version_tokens("contract_v1.docx")
        self.assertEqual(stem1, "contract")
        self.assertEqual(v1.revision_token, "v1")
        self.assertFalse(v1.is_authoritative)

        stem2, v2 = parse_version_tokens("contract_signed.pdf")
        self.assertEqual(stem2, "contract")
        self.assertEqual(v2.lifecycle_state, "signed")
        self.assertTrue(v2.is_authoritative)

        stem3, v3 = parse_version_tokens("project_architecture_final2.md")
        self.assertEqual(stem3, "project_architecture")
        self.assertEqual(v3.lifecycle_state, "final")

    def test_document_family_grouping(self):
        """Verify Plan_v1, Plan_v2, and Plan_signed are grouped in one document family."""
        (self.root / "Plan_v1.txt").write_text("Draft 1 plan")
        (self.root / "Plan_v2.txt").write_text("Draft 2 revised plan")
        (self.root / "Plan_signed.txt").write_text("Final approved contract plan")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["document_families"], 1)

if __name__ == "__main__":
    unittest.main()

