# FileOS Output Artefact Schemas (M0/M1 Reconciled)

All FileOS scans output deterministic files into `<output-dir>/`.

---

## 1. `coverage.json`

Records traversal completeness, non-overlapping accounting metrics, and scan identity.

```json
{
  "scan_id": "SCN-20261111T120000Z-a1b2c3d4",
  "scan_config_fingerprint": "sha256_hex_of_canonical_config",
  "root_label": "/path/to/target",
  "is_file_mode": false,
  "recursive": true,
  "max_depth": null,
  "deepest_discovered_depth": 13,
  "deepest_scanned_depth": 13,
  
  "directories_observed": 3070,
  "directories_scanned": 2919,
  "directories_excluded": 151,
  "directories_inaccessible": 0,
  "directories_depth_skipped": 0,
  
  "files_observed": 18312,
  "files_excluded": 0,
  "files_eligible": 18119,
  "files_analysed": 18119,
  "files_skipped": 193,
  "files_failed": 0,
  
  "eligible_file_bytes": 1815064648,
  "bytes_read_for_hashing": 1815064648,
  "bytes_reused_from_hash_cache": 0,
  "duplicate_group_count": 2689,
  "duplicate_member_file_count": 7321,
  "duplicate_group_logical_bytes": 1156195962,
  "potential_extra_copy_bytes": 718389050,
  
  "symlinks_skipped": 83,
  "mount_boundaries_skipped": 0,
  "cloud_placeholders_skipped": 0,
  "permission_errors": 0,
  "is_complete": false,
  "partial_reasons": ["Directories excluded by configuration: node_modules, .git"]
}
```

---

## 2. `inventory.jsonl`

One JSON record per eligible regular file.

```json
{
  "file_id": "FIL-000001",
  "scan_id": "SCN-20261111T120000Z-a1b2c3d4",
  "rel_path": "docs/Q3_report_v2.docx",
  "basename": "Q3_report_v2.docx",
  "normalized_stem": "q3_report",
  "extension": ".docx",
  "size_bytes": 45120,
  "mtime": 1731300000.0,
  "ctime": 1731300000.0,
  "is_symlink": false,
  "is_hidden": false,
  "readiness": "ready",
  "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "parser_capability": "docx",
  "extraction_status": "success",
  "error": null,
  "parent_folder_id": "FLD-000004",
  "depth": 2
}
```

---

## 3. `folders.jsonl`

One JSON record per discovered directory entity.

```json
{
  "folder_id": "FLD-000004",
  "scan_id": "SCN-20261111T120000Z-a1b2c3d4",
  "rel_path": "docs",
  "depth": 1,
  "parent_folder_id": "FLD-000001",
  "direct_file_count": 12,
  "descendant_file_count": 84,
  "direct_size_bytes": 450120,
  "descendant_size_bytes": 12501000,
  "dominant_extension": ".docx",
  "file_folder_fit_score": 0.88,
  "folder_parent_fit_score": 0.92,
  "anomaly_flags": [],
  "is_empty": false,
  "is_leaf": false,
  "has_mixed_content": false
}
```

---

## 4. `proposed-actions.json`

Proposed actions generated during the `plan` stage.

```json
[
  {
    "action_id": "ACT-001",
    "plan_id": "PLN-20261111T120500Z-9988",
    "source_scan_id": "SCN-20261111T120000Z-a1b2c3d4",
    "source_scan_config_fingerprint": "sha256_hex...",
    "action_type": "review_duplicate",
    "source": "backup/file_a_copy.txt",
    "source_expected_sha256": "aabbcc...",
    "destination": "N/A",
    "reason": "Exact duplicate of docs/file_a.txt",
    "confidence": 1.0,
    "reversibility": "reversible",
    "evidence_hash": "e3b0c44...",
    "status": "pending_approval"
  }
]
```

---

## 5. `review-decisions.jsonl`

Append-only ledger of decisions made in the dashboard.

```json
{
  "decision_id": "DEC-20261111123000",
  "finding_id": "DUP-001",
  "scan_id": "SCN-20261111T120000Z-a1b2c3d4",
  "finding_fingerprint": "sha256_of_evidence",
  "choice": "correct",
  "note": "Verified duplicate copies",
  "timestamp": "2026-11-11T12:30:00.000000Z",
  "report_dir": "/tmp/fileos-scan-linkright-v2"
}
```

---

## 6. `operation-journal.jsonl`

Append-only record of executed actions for safe undo.

```json
{
  "journal_id": "JRN-001",
  "action_id": "ACT-001",
  "action_type": "move",
  "source": "tmp/draft.txt",
  "destination": "docs/draft.txt",
  "source_sha256": "aabb...",
  "dest_sha256": "aabb...",
  "size_bytes": 1024,
  "status": "applied",
  "timestamp": "2026-11-11T12:35:00.000000Z",
  "inverse_action": {
    "action_type": "move",
    "source": "docs/draft.txt",
    "destination": "tmp/draft.txt",
    "expected_sha256": "aabb..."
  }
}
```
