#!/usr/bin/env python3
"""
Tests for FileOS Oracle Cloud Infrastructure Connectors.
Validates Oracle VM AI pool client and MongoDB historical tracking connector.
"""

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from connectors.oracle_pool import OracleAIPoolClient
from connectors.mongo_history import MongoHistorySync

class TestOracleConnectors(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="fileos_oracle_")
        self.report_dir = Path(self.test_dir) / "report"
        self.report_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_oracle_ai_pool_mock_adjudication(self):
        client = OracleAIPoolClient(mock_mode=True)
        packet = {
            "candidate_id": "REV-001",
            "rel_path": "Marketing/finance_doc.xlsx",
            "folder": "Marketing",
            "parent_project": "Marketing",
            "allowed_actions": ["confirm_exception", "move_folder"],
            "signals": {"file_folder_fit": 0.20},
            "excerpt": "Financial budget 2026 spreadsheet data..."
        }

        decision = client.adjudicate_packet(packet)
        self.assertEqual(decision["candidate_id"], "REV-001")
        self.assertEqual(decision["choice"], "correct")
        self.assertIn("action", decision)
        self.assertGreaterEqual(decision["confidence"], 0.7)

    def test_oracle_ai_pool_process_queue(self):
        client = OracleAIPoolClient(mock_mode=True)
        queue = [
            {"candidate_id": "REV-001", "allowed_actions": ["move_folder"]},
            {"candidate_id": "REV-002", "allowed_actions": ["confirm_exception"]}
        ]
        q_file = self.report_dir / "unresolved-review-queue.json"
        q_file.write_text(json.dumps(queue))
        d_file = self.report_dir / "review-decisions.jsonl"

        decisions = client.process_queue(q_file, d_file)
        self.assertEqual(len(decisions), 2)
        self.assertTrue(d_file.exists())

        lines = [json.loads(l) for l in d_file.read_text().splitlines() if l.strip()]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]["candidate_id"], "REV-001")

    def test_mongo_history_sync(self):
        # Setup synthetic artifacts
        cov = {
            "scan_id": "SCN-20261111T120000Z-oracle01",
            "total_bytes_hashed": 45000,
            "files_analysed": 15
        }
        (self.report_dir / "coverage.json").write_text(json.dumps(cov))

        dec = {"decision_id": "DEC-001", "finding_id": "ANO-001", "choice": "correct"}
        (self.report_dir / "review-decisions.jsonl").write_text(json.dumps(dec) + "\n")

        actions = [{"action_id": "ACT-001", "plan_id": "PLN-001", "action_type": "move_folder"}]
        (self.report_dir / "proposed-actions.json").write_text(json.dumps(actions))

        sync = MongoHistorySync(mock_mode=True)
        summary = sync.sync_scan_run(self.report_dir)

        self.assertEqual(summary["scan_id"], "SCN-20261111T120000Z-oracle01")
        self.assertEqual(summary["decisions_synced"], 1)
        self.assertEqual(summary["actions_synced"], 1)
        self.assertEqual(len(sync._synced_records), 3)

if __name__ == "__main__":
    unittest.main()

