# FileOS Scan Summary Report

**Root Scanned:** `/private/var/folders/r6/ffncwp012cd33_7zmj6rzps40000gn/T/tmpksk13aj0`  
**Timestamp:** `2026-11-11T04:41:03.099052Z`  
**Scan Mode:** Recursive (Read-Only) | **Coverage:** `Partial`  

## 1. Coverage & Tree Metrics
- **Directories Discovered:** 9 (Scanned: 8, Excluded: 1, Inaccessible: 0, Depth-Capped: 0)
- **Files Discovered:** 6 (Eligible: 6, Analysed: 6, Skipped: 0, Failed: 0)
- **Deepest Discovered Depth:** 3 | **Deepest Scanned Depth:** 3
- **Total Bytes Hashed:** 115 bytes
- **Symlinks Skipped:** 0 | **Mount Boundaries Skipped:** 0
- **Exact Duplicate Groups:** 1 (Potential redundant space: 19 bytes)
- **Document Families Identified:** 2
- **Hierarchy Anomalies Detected:** 2
- **AI Review Queue Size:** 2 packets (32 chars extracted)

### Partial Scan Explanations:

## 2. Directory Hierarchy Overview (Depth Markers)
- `.` [root] (direct: 0 files, desc: 6 files)
  - `Archive` [uncertain] (direct: 1 files, desc: 1 files)
  - `Downloads` [uncertain] (direct: 1 files, desc: 1 files)
  - `Engineering` [uncertain] (direct: 0 files, desc: 4 files)
    - `Engineering/Empty_Staging` [unknown] (direct: 0 files, desc: 0 files)
    - `Engineering/Robotics_Core` [uncertain] (direct: 0 files, desc: 2 files)
      - `Engineering/Robotics_Core/Firmware` [conflicting] (direct: 2 files, desc: 2 files)
    - `Engineering/Tax_Returns_2025` [conflicting] (direct: 2 files, desc: 2 files)
  - `fileos-output` [not_evaluated] (direct: 0 files, desc: 0 files)

## 3. Hierarchy Anomalies (Edge-by-Edge)
| Anomaly ID | Edge | Depth | Status | File-Folder Fit | Folder-Parent Fit | Action |
|---|---|---:|---|---:|---:|---|
| ANO-001 | `Engineering/Robotics_Core/Firmware -> Engineering/Robotics_Core` | 3 | `conflicting` | 0.97 | 0.1 | `review_and_relocate_folder` |
> **Evidence:** Folder Firmware contains 2 coherent files matching Firmware (0.97), but Firmware conflicts with parent project Robotics_Core (0.10).

| ANO-002 | `Engineering/Tax_Returns_2025 -> Engineering` | 2 | `conflicting` | 0.67 | 0.1 | `review_and_relocate_folder` |
> **Evidence:** Folder Tax_Returns_2025 contains 2 coherent files matching Tax_Returns_2025 (0.67), but Tax_Returns_2025 conflicts with parent project Engineering (0.10).


## 4. Exact Duplicates (Preserved)
### Group DUP-001 (Hash: `5769687bb4e7...`)
- `Archive/Guide_Copy.txt` (19 bytes)
- `Downloads/Guide.txt` (19 bytes)

## 5. Document Families & Versions
### Family FAM-001: `guide`
- `Archive/Guide_Copy.txt`: Lifecycle `unknown`
- `Downloads/Guide.txt`: Lifecycle `unknown`
### Family FAM-002: `firmware_bootloader`
- `Engineering/Robotics_Core/Firmware/firmware_bootloader_v1.txt`: Lifecycle `unknown` [v1]
- `Engineering/Robotics_Core/Firmware/firmware_bootloader_v2.txt`: Lifecycle `unknown` [v2]

## 6. AI Usage & Token Budget Ledger
- **Pass 0 (Deterministic Only):** 6 files
- **Pass 1 (2,000 char excerpts):** 2 candidate packets
- **Pass 2 / Pass 3 Escalations:** 0
- **Total Excerpt Chars Exposed:** 32 / 20,000 max budget
- **Silent AI Usage:** None. All processing strictly deterministic.

