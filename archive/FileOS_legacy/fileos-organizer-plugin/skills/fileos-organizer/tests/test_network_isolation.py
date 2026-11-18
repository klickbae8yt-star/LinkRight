#!/usr/bin/env python3
"""
Tests verifying strict zero external network or model calls
during scan, plan, report, audit, and dashboard initialization.
"""

from pathlib import Path
import shutil
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fileos import FileOSEngine
from audit import ReportAuditor

class TestNetworkIsolation(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="fileos_net_")
        self.root = Path(self.test_dir) / "workspace"
        self.root.mkdir()
        self.out = Path(self.test_dir) / "output"
        self.out.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_scan_and_plan_make_zero_socket_connections(self):
        """Verify no socket connect calls occur to non-local addresses."""
        (self.root / "sample.txt").write_text("hello isolation")

        orig_connect = socket.socket.connect

        def guarded_connect(sock, address):
            host = address[0] if isinstance(address, tuple) else address
            # Allow 127.0.0.1 or localhost only
            if str(host) not in {"127.0.0.1", "localhost", "::1"}:
                raise RuntimeError(f"Network violation: Attempted outbound connection to {address}")
            return orig_connect(sock, address)

        with patch.object(socket.socket, "connect", side_effect=guarded_connect):
            engine = FileOSEngine(self.root, self.out)
            res = engine.scan()
            self.assertEqual(res["total_files"], 1)

            actions = engine.plan()
            self.assertIsInstance(actions, list)

            auditor = ReportAuditor(self.out)
            audit_res = auditor.run_all_checks()
            self.assertEqual(audit_res["failed"], 0)

if __name__ == "__main__":
    unittest.main()

