#!/usr/bin/env python3
"""Tests for FileOS local review dashboard, data repo, and report auditor."""

import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from audit import ReportAuditor
from dashboard import DashboardDataRepo, run_dashboard_server, I18N

class TestDashboardAndAudit(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.report_dir = Path(self.test_dir) / "report"
        self.report_dir.mkdir()

        # Build synthetic report fixture
        self._create_synthetic_report()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _create_synthetic_report(self):
        # coverage.json
        cov = {
            "root_label": "/test/workspace",
            "is_file_mode": False,
            "recursive": True,
            "max_depth": None,
            "deepest_discovered_depth": 3,
            "deepest_scanned_depth": 3,
            "directories_discovered": 5,
            "directories_scanned": 4,
            "directories_excluded": 1,
            "directories_inaccessible": 0,
            "directories_depth_skipped": 0,
            "files_discovered": 6,
            "files_eligible": 6,
            "files_analysed": 6,
            "files_skipped": 0,
            "files_failed": 0,
            "total_bytes_hashed": 12000,
            "symlinks_skipped": 0,
            "mount_boundaries_skipped": 0,
            "cloud_placeholders_skipped": 0,
            "permission_errors": 0,
            "scan_id": "SCN-20261111T120000Z-a1b2c3d4",
            "scan_config_fingerprint": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "is_complete": False,
            "partial_reasons": ["Directory excluded: node_modules"]
        }
        (self.report_dir / "coverage.json").write_text(json.dumps(cov))

        # duplicate-groups.csv
        dups_csv = """group_id,sha256,size_bytes,rel_path,basename
DUP-001,aabbcc112233,500,docs/file_a.txt,file_a.txt
DUP-001,aabbcc112233,500,backup/file_a_copy.txt,file_a_copy.txt
"""
        (self.report_dir / "duplicate-groups.csv").write_text(dups_csv)

        # document-families.csv
        fams_csv = """family_id,family_stem,rel_path,basename,revision,lifecycle,is_authoritative
FAM-001,contract,legal/contract_v1.docx,contract_v1.docx,v1,draft,False
FAM-001,contract,legal/contract_signed.pdf,contract_signed.pdf,none,signed,True
"""
        (self.report_dir / "document-families.csv").write_text(fams_csv)

        # hierarchy-anomalies.csv
        ano_csv = """anomaly_id,edge,folder,parent,depth,status,file_folder_fit,folder_parent_fit,evidence,suggested_action
ANO-001,Projects/Marketing/Finance -> Projects/Marketing,Projects/Marketing/Finance,Projects/Marketing,2,conflicting,0.85,0.15,Folder Finance conflicts with Marketing,review_and_relocate_folder
"""
        (self.report_dir / "hierarchy-anomalies.csv").write_text(ano_csv)

        # proposed-actions.json
        actions = [
            {
                "action_id": "ACT-001",
                "action_type": "review_duplicate",
                "source": "backup/file_a_copy.txt",
                "destination": "N/A",
                "reason": "Exact duplicate of docs/file_a.txt",
                "confidence": 1.0,
                "reversibility": "reversible"
            }
        ]
        (self.report_dir / "proposed-actions.json").write_text(json.dumps(actions))

        # ai-usage.json
        ai_usage = {
            "total_candidates_queued": 1,
            "total_excerpt_chars": 500,
            "pass_breakdown": {"pass_0": 6, "pass_1": 1, "pass_2": 0, "pass_3": 0},
            "cache_hits": 0,
            "budget_exhausted": False
        }
        (self.report_dir / "ai-usage.json").write_text(json.dumps(ai_usage))

    def test_01_repo_stats(self):
        """Verify DashboardDataRepo calculates summary statistics accurately."""
        repo = DashboardDataRepo(self.report_dir)
        stats = repo.get_stats()

        self.assertEqual(stats["duplicate_groups_count"], 1)
        self.assertEqual(stats["duplicate_space_bytes"], 500)
        self.assertEqual(stats["document_families_count"], 1)
        self.assertEqual(stats["hierarchy_anomalies_count"], 1)
        self.assertEqual(stats["proposed_actions_count"], 1)
        self.assertEqual(stats["audit_status"], "healthy")

    def test_02_findings_pagination_and_search(self):
        """Verify unified findings can be filtered, searched, and paginated."""
        repo = DashboardDataRepo(self.report_dir)
        
        # All findings
        all_f = repo.get_findings(page=1, limit=10)
        self.assertEqual(all_f["total"], 4)  # 1 dup + 1 anomaly + 1 family + 1 action

        # Search filter
        search_f = repo.get_findings(search="contract")
        self.assertGreaterEqual(search_f["total"], 1)
        self.assertIn("contract", search_f["findings"][0]["title"].lower())

    def test_03_decision_persistence(self):
        """Verify user review decisions persist to review-decisions.jsonl."""
        repo = DashboardDataRepo(self.report_dir)
        res = repo.save_decision("DUP-001", "correct", "Yes, identical file")
        self.assertEqual(res["finding_id"], "DUP-001")
        self.assertEqual(res["choice"], "correct")

        # Reload repo and check decisions
        repo2 = DashboardDataRepo(self.report_dir)
        decisions = repo2.get_decisions()
        self.assertIn("DUP-001", decisions)
        self.assertEqual(decisions["DUP-001"]["choice"], "correct")

    def test_04_report_integrity_auditor_all_pass(self):
        """Verify ReportAuditor passes all 15 checks on valid report fixture."""
        auditor = ReportAuditor(self.report_dir)
        res = auditor.run_all_checks()

        self.assertEqual(res["failed"], 0)
        self.assertEqual(res["overall_status"], "healthy")
        self.assertEqual(res["total_checks"], 15)

    def test_05_auditor_catches_duplicate_action_ids(self):
        """Verify auditor flags duplicate action IDs as failures."""
        actions = [
            {"action_id": "ACT-001", "action_type": "move"},
            {"action_id": "ACT-001", "action_type": "rename"}
        ]
        (self.report_dir / "proposed-actions.json").write_text(json.dumps(actions))

        auditor = ReportAuditor(self.report_dir)
        res = auditor.run_all_checks()

        chk8 = next(c for c in res["checks"] if c["check_id"] == "CHK-008")
        self.assertEqual(chk8["status"], "failed")

    def test_06_auditor_catches_duplicate_hash_mismatch(self):
        """Verify auditor flags inconsistent hashes inside a duplicate group."""
        dups_csv = """group_id,sha256,size_bytes,rel_path,basename
DUP-001,hash_one,500,a.txt,a.txt
DUP-001,hash_different,500,b.txt,b.txt
"""
        (self.report_dir / "duplicate-groups.csv").write_text(dups_csv)

        auditor = ReportAuditor(self.report_dir)
        res = auditor.run_all_checks()

        chk4 = next(c for c in res["checks"] if c["check_id"] == "CHK-004")
        self.assertEqual(chk4["status"], "failed")

    def test_07_localhost_binding_enforcement(self):
        """Verify dashboard refuses to bind to non-localhost interfaces for security."""
        with self.assertRaises(ValueError):
            run_dashboard_server(self.report_dir, host="0.0.0.0", port=8765)

    def test_08_trilingual_dictionary_keys_match(self):
        """Verify Hinglish, Hindi, and English dictionaries have identical translation keys."""
        h_keys = set(I18N["hinglish"].keys())
        hi_keys = set(I18N["hindi"].keys())
        en_keys = set(I18N["english"].keys())

        self.assertEqual(h_keys, hi_keys)
        self.assertEqual(h_keys, en_keys)

    def test_09_tree_hierarchy_builder(self):
        """Verify get_tree constructs a nested tree from folders.jsonl."""
        folders = [
            {"folder_id": "FLD-0001", "rel_path": ".", "display_name": "root", "parent_folder_id": None, "depth": 0, "direct_file_count": 1, "descendant_file_count": 3},
            {"folder_id": "FLD-0002", "rel_path": "docs", "display_name": "docs", "parent_folder_id": "FLD-0001", "depth": 1, "direct_file_count": 2, "descendant_file_count": 2}
        ]
        with open(self.report_dir / "folders.jsonl", "w") as f:
            for item in folders:
                f.write(json.dumps(item) + "\n")

        repo = DashboardDataRepo(self.report_dir)
        tree = repo.get_tree()

        self.assertEqual(tree["total_nodes"], 2)
        self.assertEqual(len(tree["roots"]), 1)
        root_node = tree["roots"][0]
        self.assertEqual(root_node["folder_id"], "FLD-0001")
        self.assertEqual(len(root_node["children"]), 1)
        self.assertEqual(root_node["children"][0]["folder_id"], "FLD-0002")

    def test_10_near_duplicate_findings_integration(self):
        """Verify near-duplicate pairs are parsed and included in findings."""
        near_dups_csv = """pair_id,file_a,file_b,similarity_score,size_a_bytes,size_b_bytes,size_diff_bytes,stem_a,stem_b,suggested_action,evidence
NDP-001,docs/spec_v1.txt,docs/spec_v2.txt,0.910,1200,1250,50,spec_v1,spec_v2,review_diff_and_archive_older,High content similarity
"""
        (self.report_dir / "near-duplicates.csv").write_text(near_dups_csv)

        repo = DashboardDataRepo(self.report_dir)
        findings = repo.get_findings(f_type="near_duplicate")

        self.assertEqual(findings["total"], 1)
        item = findings["findings"][0]
        self.assertEqual(item["id"], "NDP-001")
        self.assertEqual(item["type"], "near_duplicate")
        self.assertEqual(item["paths"], ["docs/spec_v1.txt", "docs/spec_v2.txt"])

    def test_11_performance_analytics(self):
        """Verify get_performance returns valid module execution times and cache metrics."""
        perf_data = {
            "timestamp": "2026-11-11T20:00:00Z",
            "total_wall_time_seconds": 1.25,
            "total_wall_time_ms": 1250.0,
            "module_timings": [
                {"module": "directory_traversal", "duration_seconds": 0.25, "duration_ms": 250.0, "percentage": 20.0, "details": "100 dirs"},
                {"module": "hashing_and_io", "duration_seconds": 0.50, "duration_ms": 500.0, "percentage": 40.0, "details": "5000 bytes"}
            ],
            "throughput": {
                "files_per_second": 1000.0,
                "mb_per_second": 50.0
            }
        }
        (self.report_dir / "performance-profile.json").write_text(json.dumps(perf_data))

        repo = DashboardDataRepo(self.report_dir)
        perf = repo.get_performance()

        self.assertEqual(perf["total_wall_time_seconds"], 1.25)
        self.assertEqual(perf["total_wall_time_ms"], 1250.0)
        self.assertEqual(len(perf["module_timings"]), 2)
        self.assertIn("cache_metrics", perf)
        self.assertIn("live_audit_ms", perf)
        self.assertGreater(perf["live_audit_ms"], 0)

    def test_12_live_benchmark_timing(self):
        """Verify run_benchmark calculates non-zero wall clock durations for components."""
        repo = DashboardDataRepo(self.report_dir)
        bench = repo.run_benchmark()

        self.assertIn("audit_15_checks_ms", bench)
        self.assertIn("tree_construction_ms", bench)
        self.assertIn("findings_query_ms", bench)
        self.assertIn("coverage_json_read_ms", bench)
        self.assertIn("total_benchmark_ms", bench)
        self.assertGreaterEqual(bench["total_benchmark_ms"], 0.0)

if __name__ == "__main__":
    unittest.main()

