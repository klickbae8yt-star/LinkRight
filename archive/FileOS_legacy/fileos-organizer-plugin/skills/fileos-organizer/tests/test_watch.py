#!/usr/bin/env python3
"""
Tests for FileOS Watch & Daemon Scan Mode.
Validates directory mtime fingerprinting and non-blocking incremental watch triggers.
"""

from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine

class TestWatchMode(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="fileos_watch_")
        self.root = Path(self.test_dir) / "workspace"
        self.root.mkdir()
        self.out = Path(self.test_dir) / "output"
        self.out.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_fingerprint_detects_changes(self):
        engine = FileOSEngine(self.root, self.out)
        
        # Initial empty directory
        fp1 = engine._get_directory_mtime_fingerprint()

        # Add a file
        f1 = self.root / "item1.txt"
        f1.write_text("Hello Watcher")
        fp2 = engine._get_directory_mtime_fingerprint()
        self.assertNotEqual(fp1, fp2)

        # Unchanged directory keeps identical fingerprint
        fp2_repeat = engine._get_directory_mtime_fingerprint()
        self.assertEqual(fp2, fp2_repeat)

        # Modify file
        time.sleep(0.05)
        f1.write_text("Modified Watcher Content")
        fp3 = engine._get_directory_mtime_fingerprint()
        self.assertNotEqual(fp2, fp3)

    def test_watch_once_mode(self):
        f = self.root / "file.txt"
        f.write_text("watch once content")

        engine = FileOSEngine(self.root, self.out)
        callbacks = []
        res = engine.watch(interval=1, once=True, on_change=lambda r: callbacks.append(r))

        self.assertEqual(res["total_files"], 1)
        self.assertEqual(len(callbacks), 1)
        self.assertTrue((self.out / ".fileos-cache.json").exists())

if __name__ == "__main__":
    unittest.main()

