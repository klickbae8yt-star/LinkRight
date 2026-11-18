#!/usr/bin/env python3
"""Tests for folder-edge relationship evaluation and hierarchy anomaly detection."""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine

class TestHierarchy(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.root = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_project_x_folder_y_file_z_scenario(self):
        """
        Mandatory acceptance scenario:
        Project X/Folder Y/File Z.pdf and File Z notes.txt.
        Files fit Folder Y, but Folder Y conflicts with Project X.
        Verify independent edge detection.
        """
        proj_x = self.root / "Project_Alpha_Robotics"
        folder_y = proj_x / "Tax_Audit_2025"
        folder_y.mkdir(parents=True)

        (folder_y / "Tax_Audit_Report.txt").write_text("Tax filing and IRS audit data for 2025.")
        (folder_y / "Tax_Audit_Summary.txt").write_text("Summary of tax deductions and accountant notes.")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertGreaterEqual(res["hierarchy_anomalies"], 1)

        # Verify anomaly file contains the exact edge
        anomalies_file = engine.output / "hierarchy-anomalies.csv"
        content = anomalies_file.read_text()
        self.assertIn("Tax_Audit_2025", content)
        self.assertIn("Project_Alpha_Robotics", content)
        self.assertIn("conflicting", content)

    def test_empty_folders_do_not_trigger_confident_mismatch(self):
        """Empty folders must remain unknown and never trigger confident mismatch alerts."""
        empty_folder = self.root / "Project_Robotics" / "Random_Empty_Folder"
        empty_folder.mkdir(parents=True)

        engine = FileOSEngine(self.root)
        res = engine.scan()

        self.assertEqual(res["hierarchy_anomalies"], 0)

    def test_mixed_topic_folder_flags_split_contents_not_whole_move(self):
        """Folders with >= 4 files of diverse topics should recommend split_contents, not moving the whole folder."""
        mixed = self.root / "Project_Alpha" / "Mixed_Documents"
        mixed.mkdir(parents=True)

        (mixed / "recipe_soup.txt").write_text("Cooking instructions for tomato soup.")
        (mixed / "tax_deductions_2024.txt").write_text("Tax filing deductions.")
        (mixed / "guitar_chords.txt").write_text("Guitar chords for wonderwall.")
        (mixed / "workout_routine.txt").write_text("Chest and triceps workout.")

        engine = FileOSEngine(self.root)
        res = engine.scan()

        anomalies_file = engine.output / "hierarchy-anomalies.csv"
        content = anomalies_file.read_text()
        self.assertIn("Mixed_Documents", content)
        self.assertIn("split_contents", content)

if __name__ == "__main__":
    unittest.main()
