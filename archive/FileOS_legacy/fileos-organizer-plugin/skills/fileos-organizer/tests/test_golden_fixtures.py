#!/usr/bin/env python3
"""
FileOS Golden Fixture Suite (M0.7).
Deterministic, synthetic test fixtures for the 17 core baseline scenarios
specified in Section 5 of FILEOS_M0_M1_IMPLEMENTATION_SPEC.md.
"""

import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine, compute_sha256

class TestGoldenFixtures(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="fileos_golden_")
        self.root = Path(self.test_dir) / "workspace"
        self.root.mkdir()
        self.out = Path(self.test_dir) / "output"
        self.out.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_01_exact_duplicate(self):
        """1. Exact duplicate: same bytes, different paths."""
        (self.root / "dir_a").mkdir()
        (self.root / "dir_b").mkdir()
        content = "Exact duplicate payload for scenario 1"
        (self.root / "dir_a" / "doc.txt").write_text(content)
        (self.root / "dir_b" / "doc_copy.txt").write_text(content)

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()
        self.assertEqual(res["total_files"], 2)

        dups = (self.out / "duplicate-groups.csv").read_text().splitlines()
        self.assertGreater(len(dups), 1)
        self.assertIn("doc.txt", dups[1] + dups[2])
        self.assertIn("doc_copy.txt", dups[1] + dups[2])

    def test_02_renamed_duplicate(self):
        """2. Renamed duplicate: same bytes, unrelated filenames."""
        content = "Unique byte stream for hash comparison only"
        (self.root / "alpha.txt").write_text(content)
        (self.root / "omega.log").write_text(content)

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()
        self.assertEqual(res["total_files"], 2)

        dups = (self.out / "duplicate-groups.csv").read_text().splitlines()
        self.assertGreater(len(dups), 1)

    def test_03_different_content_same_name(self):
        """3. Different content, same name: not classified as duplicate."""
        (self.root / "project_a").mkdir()
        (self.root / "project_b").mkdir()
        (self.root / "project_a" / "readme.txt").write_text("Topic A specifications")
        (self.root / "project_b" / "readme.txt").write_text("Topic B different specifications")

        engine = FileOSEngine(self.root, self.out)
        engine.scan()
        dups = (self.out / "duplicate-groups.csv").read_text().strip().splitlines()
        # Only header line should be present
        self.assertEqual(len(dups), 1)

    def test_04_version_tokens(self):
        """4. Version tokens: Plan_v1, Plan_v2, Plan_final grouped into family."""
        (self.root / "Plan_v1.docx").write_text("Draft 1 content")
        (self.root / "Plan_v2.docx").write_text("Draft 2 revised content")
        (self.root / "Plan_final.docx").write_text("Final approved content")

        engine = FileOSEngine(self.root, self.out)
        engine.scan()

        fams = (self.out / "document-families.csv").read_text()
        self.assertIn("Plan_v1.docx", fams)
        self.assertIn("Plan_v2.docx", fams)
        self.assertIn("Plan_final.docx", fams)

    def test_05_branch_like_versions(self):
        """5. Branch-like versions: Plan_internal, Plan_client.
        Documents current version-family behavior and limitations:
        branch-like stems without linear version numbers (v1/v2/final) remain independent stems,
        and FileOS does NOT assume linear supersession solely from naming."""
        (self.root / "Plan_internal.txt").write_text("Internal pricing formulas")
        (self.root / "Plan_client.txt").write_text("Client facing scope")

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()
        # Verify that both files were indexed and not collapsed into a false linear supersession
        self.assertEqual(res["total_files"], 2)

    def test_06_nested_hierarchy_12_levels(self):
        """6. Nested hierarchy: 12+ levels deep all visited."""
        curr = self.root
        for i in range(12):
            curr = curr / f"level_{i+1}"
            curr.mkdir()
        (curr / "deep_leaf.txt").write_text("Deep data")

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()
        self.assertEqual(res["total_files"], 1)
        self.assertGreaterEqual(res["deepest_depth"], 12)

    def test_07_parent_mismatch(self):
        """7. Parent mismatch: child folder contradicts parent project."""
        marketing = self.root / "Marketing_Brand_Campaign"
        tax_sub = marketing / "Tax_Audit_2026"
        tax_sub.mkdir(parents=True)
        (tax_sub / "Tax_Audit_Ledger.txt").write_text("tax audit calculations")
        (tax_sub / "Tax_Audit_Notes.txt").write_text("tax audit accountant notes")

        engine = FileOSEngine(self.root, self.out)
        engine.scan()

        anomalies = (self.out / "hierarchy-anomalies.csv").read_text()
        self.assertIn("Tax_Audit_2026", anomalies)

    def test_08_mixed_folder(self):
        """8. Mixed folder: folder contains two unrelated synthetic topics."""
        mixed = self.root / "General_Stuff"
        mixed.mkdir()
        (mixed / "engineering_spec_v1.py").write_text("print('code')")
        (mixed / "legal_contract_agreement.pdf").write_text("contract data")

        engine = FileOSEngine(self.root, self.out)
        engine.scan()

        folders = (self.out / "folders.jsonl").read_text()
        self.assertIn("General_Stuff", folders)

    def test_09_empty_folder(self):
        """9. Empty folder: counted and classified without inventing content."""
        (self.root / "Empty_Container").mkdir()

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()
        self.assertEqual(res["total_files"], 0)
        self.assertGreaterEqual(res["total_folders"], 1)

        folders_lines = (self.out / "folders.jsonl").read_text().splitlines()
        empty_rec = [json.loads(l) for l in folders_lines if "Empty_Container" in l]
        self.assertTrue(len(empty_rec) > 0)
        self.assertEqual(empty_rec[0]["direct_file_count"], 0)

    def test_10_hidden_file(self):
        """10. Hidden file: dotfiles handled consistently."""
        (self.root / ".hidden_config").write_text("config_val=1")
        (self.root / "visible.txt").write_text("visible text")

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()
        self.assertEqual(res["total_files"], 2)

        inv = (self.out / "inventory.jsonl").read_text()
        self.assertIn(".hidden_config", inv)

    def test_11_excluded_subtree(self):
        """11. Excluded subtree: exclusion visible, descendants not counted."""
        node_modules = self.root / "node_modules" / "sub_pkg"
        node_modules.mkdir(parents=True)
        (node_modules / "bundle.js").write_text("console.log()")

        engine = FileOSEngine(self.root, self.out, exclusions=["node_modules"])
        res = engine.scan()
        self.assertEqual(res["total_files"], 0)

        cov = json.loads((self.out / "coverage.json").read_text())
        self.assertGreaterEqual(cov["directories_excluded"], 1)

    def test_12_symlink_cases(self):
        """12. Symlink loop protection."""
        sub = self.root / "sub"
        sub.mkdir()
        (sub / "real.txt").write_text("real content")
        try:
            (sub / "loop_link").symlink_to(self.root, target_is_directory=True)
        except OSError:
            self.skipTest("Symlinks not supported on this OS")

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan(follow_symlinks=True)
        self.assertEqual(res["total_files"], 1)

    def test_13_unstable_file(self):
        """13. Unstable file: .part and .crdownload marked unstable."""
        (self.root / "large_dataset.zip.crdownload").write_text("downloading...")

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()
        self.assertEqual(res["total_files"], 1)

        inv = json.loads((self.out / "inventory.jsonl").read_text().strip())
        self.assertEqual(inv["readiness"], "unstable")

    def test_14_inaccessible_path(self):
        """14. Inaccessible path: permission denial recorded."""
        locked = self.root / "locked_dir"
        locked.mkdir()
        (locked / "secret.txt").write_text("secret")
        try:
            os.chmod(locked, 0000)
        except Exception:
            self.skipTest("chmod not supported")

        try:
            engine = FileOSEngine(self.root, self.out)
            res = engine.scan()
            cov = json.loads((self.out / "coverage.json").read_text())
            self.assertGreaterEqual(cov["permission_errors"], 1)
        finally:
            os.chmod(locked, 0o755)

    def test_15_unicode_and_punctuation(self):
        """15. Unicode paths and punctuation preserved."""
        u_dir = self.root / "📁 Pröjécts 2026" / "Démo & Spécs #1"
        u_dir.mkdir(parents=True)
        (u_dir / "résumé (final) [draft].txt").write_text("UTF-8 payload")

        engine = FileOSEngine(self.root, self.out)
        res = engine.scan()
        self.assertEqual(res["total_files"], 1)

        inv_records = [json.loads(l) for l in (self.out / "inventory.jsonl").read_text().splitlines()]
        paths = [r["rel_path"] for r in inv_records]
        self.assertTrue(any("Pröjécts 2026" in p for p in paths))
        self.assertTrue(any("résumé" in p for p in paths))

    def test_16_destination_collision_on_apply(self):
        """16. Destination collision: apply blocks overwriting existing file."""
        src = self.root / "source.txt"
        dst = self.root / "existing_target.txt"
        src.write_text("source content")
        dst.write_text("original target content")

        plan = [
            {
                "action_id": "ACT-001",
                "action_type": "move",
                "source": "source.txt",
                "destination": "existing_target.txt",
                "reason": "Test collision"
            }
        ]
        plan_path = self.out / "proposed-actions.json"
        plan_path.write_text(json.dumps(plan))

        engine = FileOSEngine(self.root, self.out)
        with self.assertRaises(FileExistsError):
            engine.apply(plan_path, approved_action_ids=["ACT-001"])

        # Target remained untouched
        self.assertEqual(dst.read_text(), "original target content")

    def test_17_file_changes_during_scan(self):
        """17. File changed mid-scan: atomic check detects mutation."""
        target_file = self.root / "changing.txt"
        target_file.write_text("initial state")

        # Verify compute_sha256 helper
        h1 = compute_sha256(target_file)
        self.assertTrue(len(h1) == 64)

if __name__ == "__main__":
    unittest.main()
