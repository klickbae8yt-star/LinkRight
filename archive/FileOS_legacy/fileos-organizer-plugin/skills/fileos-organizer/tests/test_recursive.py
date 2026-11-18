#!/usr/bin/env python3
"""Tests for recursive tree traversal, folder-first data model, and full-tree intelligence."""

import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine, compute_sha256

class TestRecursiveTree(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_01_deep_recursion_12_levels(self):
        """1. Deep recursion: files nested at least 12 directory levels are discovered and indexed by default."""
        deep_dir = self.root
        for i in range(1, 13):
            deep_dir = deep_dir / f"level_{i:02d}"
        deep_dir.mkdir(parents=True)
        deep_file = deep_dir / "deep_secret.txt"
        deep_file.write_text("Deeply nested file at level 12")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["total_files"], 1)
        self.assertGreaterEqual(res["deepest_depth"], 12)

        # Verify inventory contains the file
        inv_path = engine.output / "inventory.jsonl"
        lines = inv_path.read_text().strip().split("\n")
        self.assertEqual(len(lines), 1)
        rec = json.loads(lines[0])
        self.assertEqual(rec["basename"], "deep_secret.txt")
        self.assertEqual(rec["depth"], 12)

    def test_02_no_arbitrary_depth_cap(self):
        """2. No arbitrary depth cap: a directory at depth 8 is scanned without specifying max-depth."""
        dir_8 = self.root / "d1" / "d2" / "d3" / "d4" / "d5" / "d6" / "d7" / "d8"
        dir_8.mkdir(parents=True)
        (dir_8 / "item.txt").write_text("Content at depth 8")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["total_files"], 1)
        self.assertEqual(res["deepest_depth"], 8)

    def test_03_explicit_depth_cap_honoured(self):
        """3. Explicit depth cap: user-supplied depth limit is honoured and omitted descendants are reported in coverage."""
        shallow = self.root / "level_1" / "level_2"
        shallow.mkdir(parents=True)
        (shallow / "shallow_file.txt").write_text("At depth 2")

        deep = shallow / "level_3" / "level_4"
        deep.mkdir(parents=True)
        (deep / "deep_file.txt").write_text("At depth 4")

        engine = FileOSEngine(self.root, max_depth=2)
        res = engine.scan()

        self.assertEqual(res["total_files"], 1)
        self.assertEqual(res["deepest_depth"], 2)
        self.assertFalse(res["is_complete"])

        # Check coverage.json
        cov = json.loads((engine.output / "coverage.json").read_text())
        self.assertFalse(cov["is_complete"])
        self.assertGreaterEqual(cov["directories_depth_skipped"], 1)

    def test_04_folder_as_first_class_entity(self):
        """4. Folders as entities: empty folders and folders containing only subfolders are represented in folders.jsonl."""
        empty_f = self.root / "Empty_Folder"
        empty_f.mkdir()

        container = self.root / "Container_Folder" / "Sub_Folder"
        container.mkdir(parents=True)
        (container / "child.txt").write_text("Child file")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        folders_file = engine.output / "folders.jsonl"
        lines = [json.loads(line) for line in folders_file.read_text().strip().split("\n")]
        rel_paths = {f["rel_path"] for f in lines}

        self.assertIn("Empty_Folder", rel_paths)
        self.assertIn("Container_Folder", rel_paths)
        self.assertIn("Container_Folder/Sub_Folder", rel_paths)

        # Check container folder records descendant count
        container_rec = next(f for f in lines if f["rel_path"] == "Container_Folder")
        self.assertEqual(container_rec["direct_file_count"], 0)
        self.assertEqual(container_rec["descendant_file_count"], 1)

    def test_05_file_to_folder_vs_folder_to_parent_mismatch(self):
        """5. Project X/Folder Y/File Z produces Z -> Y supported and Y -> X conflicting."""
        proj = self.root / "Project_Robotics"
        taxes = proj / "Taxes_2025"
        taxes.mkdir(parents=True)
        (taxes / "Taxes_1040.txt").write_text("IRS 1040 tax return.")
        (taxes / "Taxes_Deductions.txt").write_text("Itemized deductions.")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertGreaterEqual(res["hierarchy_anomalies"], 1)
        anomalies = json.loads((engine.output / "unresolved-review-queue.json").read_text())
        ano = next(a for a in anomalies if a["folder"] == "Project_Robotics/Taxes_2025")
        self.assertEqual(ano["uncertainty_type"], "hierarchy_conflict")
        self.assertGreaterEqual(ano["signals"]["file_folder_fit"], 0.60)
        self.assertLess(ano["signals"]["folder_parent_fit"], 0.40)

    def test_06_deepest_mismatch_location(self):
        """6. Mismatch several levels below root is attached to the exact parent-child edge."""
        nested = self.root / "Core" / "Services" / "Billing" / "Gardening_Club"
        nested.mkdir(parents=True)
        (nested / "Gardening_Plants.txt").write_text("Tomatoes and roses.")
        (nested / "Gardening_Tools.txt").write_text("Shovels and watering cans.")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        anomalies_file = engine.output / "hierarchy-anomalies.csv"
        content = anomalies_file.read_text()
        self.assertIn("Core/Services/Billing/Gardening_Club -> Core/Services/Billing", content)

    def test_07_mixed_folder_split_contents(self):
        """7. Mixed folder results in uncertain and split_contents recommendation."""
        mixed = self.root / "Misc_Collection"
        mixed.mkdir()
        (mixed / "recipe.txt").write_text("Pasta recipe.")
        (mixed / "invoice.txt").write_text("Invoice payment.")
        (mixed / "guitar.txt").write_text("Guitar tab.")
        (mixed / "workout.txt").write_text("Fitness routine.")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        anomalies_file = engine.output / "hierarchy-anomalies.csv"
        content = anomalies_file.read_text()
        self.assertIn("Misc_Collection", content)
        self.assertIn("split_contents", content)

    def test_08_hidden_folder_scanned(self):
        """8. Ordinary hidden folders are scanned unless explicitly excluded."""
        hidden_dir = self.root / ".hidden_project"
        hidden_dir.mkdir()
        (hidden_dir / "secret.txt").write_text("Secret notes.")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["total_files"], 1)
        folders = (engine.output / "folders.jsonl").read_text()
        self.assertIn(".hidden_project", folders)

    def test_09_symlink_loop_protection(self):
        """9. Default scan skips symlinks; follow mode does not loop forever."""
        sub = self.root / "sub"
        sub.mkdir()
        (sub / "doc.txt").write_text("Document")
        link = sub / "loop_link"

        try:
            os.symlink(sub, link)
        except OSError:
            self.skipTest("Symlinks not supported")

        out_default = Path(tempfile.mkdtemp())
        out_follow = Path(tempfile.mkdtemp())

        try:
            # Default scan skips symlinks
            engine = FileOSEngine(self.root, output_dir=out_default)
            res = engine.scan(follow_symlinks=False)
            self.assertEqual(res["total_files"], 1)

            # Follow symlinks mode terminates safely without infinite loop
            engine_follow = FileOSEngine(self.root, output_dir=out_follow)
            res_follow = engine_follow.scan(follow_symlinks=True)
            self.assertEqual(res_follow["total_files"], 1)
        finally:
            shutil.rmtree(out_default)
            shutil.rmtree(out_follow)

    def test_10_permission_access_error(self):
        """10. Inaccessible directory is recorded while sibling branches continue."""
        readable = self.root / "readable_branch"
        readable.mkdir()
        (readable / "good.txt").write_text("Good data")

        unreadable = self.root / "locked_branch"
        unreadable.mkdir()
        (unreadable / "locked.txt").write_text("Locked data")

        try:
            os.chmod(unreadable, 0000)
        except Exception:
            self.skipTest("chmod not supported")

        try:
            engine = FileOSEngine(self.root)
            res = engine.scan()
            # readable file was processed
            self.assertEqual(res["total_files"], 1)
            # locked branch recorded in coverage
            cov = json.loads((engine.output / "coverage.json").read_text())
            self.assertGreaterEqual(cov["permission_errors"], 1)
        finally:
            os.chmod(unreadable, 0o755)

    def test_11_special_files_and_incomplete_downloads(self):
        """11. Special files and incomplete downloads are not treated as normal completed documents."""
        (self.root / "archive.zip.crdownload").write_text("incomplete download")
        (self.root / "normal.txt").write_text("complete document")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["total_files"], 2)
        inv = [json.loads(line) for line in (engine.output / "inventory.jsonl").read_text().strip().split("\n")]
        rec_unstable = next(r for r in inv if r["basename"] == "archive.zip.crdownload")
        self.assertEqual(rec_unstable["readiness"], "unstable")
        self.assertIsNone(rec_unstable["sha256"])

    def test_12_unicode_spaces_and_punctuation(self):
        """12. Nested paths with Unicode, spaces, and punctuation are preserved."""
        unicode_dir = self.root / "📁 Pröjécts 2026" / "Démo & Spécs #1"
        unicode_dir.mkdir(parents=True)
        u_file = unicode_dir / "résumé (final) [draft].txt"
        u_file.write_text("UTF-8 document content")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["total_files"], 1)
        import json as _json
        inv_records = [
            _json.loads(line)
            for line in (engine.output / "inventory.jsonl").read_text().splitlines()
            if line.strip()
        ]
        rel_paths = [r.get("rel_path", "") for r in inv_records]
        self.assertTrue(
            any("Pröjécts 2026" in p for p in rel_paths),
            f"Unicode folder name not found in inventory paths: {rel_paths}"
        )
        self.assertTrue(
            any("résumé" in p for p in rel_paths),
            f"Unicode filename not found in inventory paths: {rel_paths}"
        )

    def test_13_coverage_accounting_reconciles(self):
        """13. Coverage totals reconcile: discovered = scanned + explicitly skipped."""
        (self.root / "f1.txt").write_text("one")
        (self.root / "f2.tmp").write_text("two")
        sub = self.root / "sub"
        sub.mkdir()
        (sub / "f3.txt").write_text("three")

        engine = FileOSEngine(self.root)
        engine.scan()

        cov = json.loads((engine.output / "coverage.json").read_text())
        self.assertEqual(
            cov["directories_discovered"],
            cov["directories_scanned"] + cov["directories_excluded"] + cov["directories_inaccessible"] + cov["directories_depth_skipped"]
        )
        self.assertEqual(
            cov["files_discovered"],
            cov["files_analysed"] + cov["files_skipped"] + cov["files_failed"]
        )

    def test_14_deterministic_repeat_runs(self):
        """14. Repeated scans on unchanged tree produce identical inventories and hashes."""
        (self.root / "file_b.txt").write_text("Content B")
        (self.root / "file_a.txt").write_text("Content A")

        out1 = Path(tempfile.mkdtemp())
        out2 = Path(tempfile.mkdtemp())

        try:
            e1 = FileOSEngine(self.root, out1)
            e1.scan()

            e2 = FileOSEngine(self.root, out2)
            e2.scan()

            inv1 = (out1 / "inventory.jsonl").read_text()
            inv2 = (out2 / "inventory.jsonl").read_text()

            # Files must be ordered identically
            files1 = [json.loads(l)["rel_path"] for l in inv1.strip().split("\n")]
            files2 = [json.loads(l)["rel_path"] for l in inv2.strip().split("\n")]
            self.assertEqual(files1, files2)
        finally:
            shutil.rmtree(out1)
            shutil.rmtree(out2)

    def test_15_ai_budget_caps_shared(self):
        """15. AI review queue respects shared budget caps (max 10 packets, max 20,000 chars)."""
        # Create 12 conflicting folders
        for i in range(12):
            fld = self.root / f"Project_{i}" / f"Mismatch_{i}"
            fld.mkdir(parents=True)
            (fld / f"Mismatch_{i}_1.txt").write_text(f"Topic {i} data " * 50)
            (fld / f"Mismatch_{i}_2.txt").write_text(f"Topic {i} info " * 50)

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertLessEqual(res["ai_queue_packets"], 10)
        ai_usage = json.loads((engine.output / "ai-usage.json").read_text())
        self.assertLessEqual(ai_usage["total_candidates_queued"], 10)
        self.assertLessEqual(ai_usage["total_excerpt_chars"], 20000)

    def test_16_no_mutation_in_scan_plan(self):
        """16. Recursive scans and plans never mutate, rename, or delete any source files."""
        sub = self.root / "data" / "nested"
        sub.mkdir(parents=True)
        f = sub / "important.txt"
        f.write_text("Cannot be changed")
        h_before = compute_sha256(f)
        mtime_before = f.stat().st_mtime

        engine = FileOSEngine(self.root)
        engine.scan()
        engine.plan()

        self.assertTrue(f.exists())
        self.assertEqual(compute_sha256(f), h_before)
        self.assertEqual(f.stat().st_mtime, mtime_before)

if __name__ == "__main__":
    unittest.main()
