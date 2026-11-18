#!/usr/bin/env python3
"""
FileOS MongoDB Historical Sync Connector.
Persists completed scan coverage, inventory hashes, and review decisions
into MongoDB running on the Oracle Cloud Always-Free VM.
Uses Python standard library with optional pymongo support.
"""

import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_MONGO_URI = os.environ.get("FILEOS_MONGO_URI", "mongodb://localhost:27017")
DEFAULT_DB_NAME = os.environ.get("FILEOS_MONGO_DB", "fileos")

class MongoHistorySync:
    def __init__(
        self,
        mongo_uri: str = DEFAULT_MONGO_URI,
        db_name: str = DEFAULT_DB_NAME,
        mock_mode: bool = False
    ):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.mock_mode = mock_mode
        self._synced_records: List[Dict[str, Any]] = []

    def sync_scan_run(self, report_dir: Path) -> Dict[str, Any]:
        """
        Reads scan artifacts from report_dir and syncs them to MongoDB:
        1. coverage.json -> 'scans' collection
        2. review-decisions.jsonl -> 'decisions' collection
        3. proposed-actions.json -> 'plans' collection
        """
        p_cov = report_dir / "coverage.json"
        p_dec = report_dir / "review-decisions.jsonl"
        p_actions = report_dir / "proposed-actions.json"

        sync_summary = {
            "synced_at": datetime.datetime.utcnow().isoformat() + "Z",
            "report_dir": str(report_dir),
            "scan_id": None,
            "decisions_synced": 0,
            "actions_synced": 0,
            "status": "success"
        }

        # 1. Coverage
        cov_data = {}
        if p_cov.exists():
            try:
                cov_data = json.loads(p_cov.read_text(encoding="utf-8"))
                cov_data["synced_at"] = sync_summary["synced_at"]
                sync_summary["scan_id"] = cov_data.get("scan_id")
                self._save_document("scans", cov_data, key="scan_id")
            except Exception as e:
                sync_summary["coverage_error"] = str(e)

        # 2. Decisions
        if p_dec.exists():
            count = 0
            try:
                with open(p_dec, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            d = json.loads(line)
                            self._save_document("decisions", d, key="decision_id")
                            count += 1
                sync_summary["decisions_synced"] = count
            except Exception as e:
                sync_summary["decisions_error"] = str(e)

        # 3. Actions / Plan
        if p_actions.exists():
            try:
                actions = json.loads(p_actions.read_text(encoding="utf-8"))
                if actions:
                    plan_doc = {
                        "plan_id": actions[0].get("plan_id", f"PLN-{sync_summary['scan_id']}"),
                        "scan_id": sync_summary["scan_id"],
                        "actions": actions,
                        "action_count": len(actions),
                        "synced_at": sync_summary["synced_at"]
                    }
                    self._save_document("plans", plan_doc, key="plan_id")
                    sync_summary["actions_synced"] = len(actions)
            except Exception as e:
                sync_summary["actions_error"] = str(e)

        return sync_summary

    def _save_document(self, collection_name: str, doc: Dict[str, Any], key: Optional[str] = None):
        """Saves document either via pymongo (if available) or appends to local sync queue."""
        if self.mock_mode:
            self._synced_records.append({"collection": collection_name, "doc": doc})
            return

        try:
            import pymongo
            client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=2000)
            db = client[self.db_name]
            coll = db[collection_name]
            if key and key in doc:
                coll.replace_one({key: doc[key]}, doc, upsert=True)
            else:
                coll.insert_one(doc)
            client.close()
        except Exception:
            # Fallback: persist to local sync buffer file
            sync_buffer = Path(os.environ.get("FILEOS_SYNC_BUFFER", "/tmp/fileos-mongo-buffer.jsonl"))
            with open(sync_buffer, "a", encoding="utf-8") as f:
                f.write(json.dumps({"collection": collection_name, "doc": doc}) + "\n")

