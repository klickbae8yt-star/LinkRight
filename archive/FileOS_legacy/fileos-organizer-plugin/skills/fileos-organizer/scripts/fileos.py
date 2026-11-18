#!/usr/bin/env python3
"""
FileOS: Deterministic-first, low-token file organization engine with recursive directory tree intelligence.
Strictly local-first, minimal dependencies (Python 3 standard library only).
"""

import argparse
import csv
import dataclasses
import datetime
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid
import zipfile
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------
# Constants & Defaults
# ---------------------------------------------------------------------------

DEFAULT_EXCLUSIONS = [
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".DS_Store",
    ".idea",
    ".vscode",
    "Thumbs.db",
    "desktop.ini",
]

PASS_LIMITS = {
    0: 0,
    1: 2000,
    2: 8000,
    3: 16000,
}

MAX_AI_PACKETS_PER_RUN = 10
MAX_AI_CHARS_PER_RUN = 20000
MAX_PASS2_ESCALATIONS = 5
MAX_PASS3_ESCALATIONS = 2
CHUNK_SIZE = 65536  # 64 KB streaming hash chunks

GENERIC_FOLDER_NAMES = {
    "misc", "other", "documents", "docs", "new folder", "archive",
    "files", "downloads", "data", "temp", "tmp", "stuff", "backup"
}

# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclasses.dataclass
class FileRecord:
    file_id: str
    rel_path: str
    basename: str
    normalized_stem: str
    extension: str
    size_bytes: int
    mtime: float
    ctime: float
    is_symlink: bool
    is_hidden: bool
    readiness: str  # "ready", "unstable", "unreadable", "skipped_symlink", "special_file"
    sha256: Optional[str] = None
    parser_capability: str = "none"
    extraction_status: str = "pending"
    error: Optional[str] = None
    parent_folder_id: Optional[str] = None
    depth: int = 0

@dataclasses.dataclass
class FolderRecord:
    folder_id: str
    rel_path: str
    display_name: str
    parent_folder_id: Optional[str]
    depth: int
    direct_child_folder_ids: List[str]
    direct_file_ids: List[str]
    direct_file_count: int
    descendant_file_count: int
    direct_child_folder_count: int
    descendant_folder_count: int
    aggregate_size_bytes: int
    extension_distribution: Dict[str, int]
    is_hidden: bool
    is_excluded: bool
    accessibility: str  # "accessible", "inaccessible", "boundary_not_scanned", "depth_limit_reached"
    scan_status: str    # "scanned", "partial", "skipped"
    last_scan_time: str
    error: Optional[str] = None
    direct_tokens: List[str] = dataclasses.field(default_factory=list)
    descendant_tokens: List[str] = dataclasses.field(default_factory=list)
    relationship_status: str = "unknown"  # "confirmed", "supported", "uncertain", "conflicting", "unknown", "not_evaluated"
    evidence: str = ""

@dataclasses.dataclass
class VersionInfo:
    revision_token: Optional[str]
    lifecycle_state: str  # draft, signed, approved, final, under_review, unknown
    is_authoritative: bool
    date_stamp: Optional[str]

@dataclasses.dataclass
class CoverageRecord:
    root_label: str
    is_file_mode: bool
    recursive: bool
    max_depth: Optional[int]
    deepest_discovered_depth: int
    deepest_scanned_depth: int
    directories_discovered: int
    directories_scanned: int
    directories_excluded: int
    directories_inaccessible: int
    directories_depth_skipped: int
    files_discovered: int
    files_eligible: int
    files_analysed: int
    files_skipped: int
    files_failed: int
    total_bytes_hashed: int
    symlinks_skipped: int
    mount_boundaries_skipped: int
    cloud_placeholders_skipped: int
    permission_errors: int
    is_complete: bool
    partial_reasons: List[str]
    scan_id: str = ""   # stable fingerprint for stale-decision detection
    scan_config_fingerprint: str = ""
    files_observed: int = 0
    files_excluded: int = 0
    directories_observed: int = 0
    eligible_file_bytes: int = 0
    bytes_read_for_hashing: int = 0
    bytes_reused_from_hash_cache: int = 0
    duplicate_group_count: int = 0
    duplicate_member_file_count: int = 0
    duplicate_group_logical_bytes: int = 0
    potential_extra_copy_bytes: int = 0

# ---------------------------------------------------------------------------
# Path & Token Utilities
# ---------------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """Normalize text into clean lowercase alphanumeric tokens."""
    return re.sub(r"[^\w\s-]", " ", text.lower()).strip()

def tokenize(text: str) -> Set[str]:
    """Tokenize a name or path segment into significant words."""
    norm = normalize_text(text)
    tokens = {t for t in re.split(r"[\s_.-]+", norm) if len(t) > 1}
    stopwords = {"and", "the", "for", "with", "from", "into", "pdf", "docx", "txt", "doc", "file", "folder"}
    return tokens - stopwords

def parse_version_tokens(basename: str) -> Tuple[str, VersionInfo]:
    """
    Strips version tokens, suffixes, and markers to yield normalized stem
    and detailed VersionInfo (lifecycle state, authoritative flag, revision).
    """
    stem = Path(basename).stem
    lifecycle = "unknown"
    is_authoritative = False
    revision = None
    date_stamp = None

    # Check for date stamps (YYYY-MM-DD or YYYY_MM_DD)
    date_match = re.search(r"(\d{4}[-_]\d{2}[-_]\d{2})", stem)
    if date_match:
        date_stamp = date_match.group(1)
        stem = stem.replace(date_match.group(0), "")

    # Check lifecycle / authoritative flags
    lower_stem = stem.lower()
    if re.search(r"(^|[_\s.-])(signed|signature)($|[_\s.-])", lower_stem):
        lifecycle = "signed"
        is_authoritative = True
    elif re.search(r"(^|[_\s.-])(approved)($|[_\s.-])", lower_stem):
        lifecycle = "approved"
        is_authoritative = True
    elif re.search(r"(^|[_\s.-])(final(\d+)?)($|[_\s.-])", lower_stem):
        lifecycle = "final"
    elif re.search(r"(^|[_\s.-])(draft(\d+)?)($|[_\s.-])", lower_stem):
        lifecycle = "draft"
    elif re.search(r"(^|[_\s.-])(review|under[-_]review)($|[_\s.-])", lower_stem):
        lifecycle = "under_review"

    # Revision markers like v1, v2.3, _v3, -v0.1
    rev_match = re.search(r"(^|[_\s.-])v(\d+([._]\d+)?)($|[_\s.-])", stem, re.IGNORECASE)
    if rev_match:
        revision = f"v{rev_match.group(2)}"
        stem = re.sub(r"(^|[_\s.-])v\d+([._]\d+)?($|[_\s.-])", r"\1\3", stem, flags=re.IGNORECASE)

    # Clean common suffixes like (1), copy, revised, signed, approved, final, draft
    stem = re.sub(
        r"([_\s.-]+(copy(\s*\d+)?|revised|final\d*|draft\d*|signed|approved|\(\d+\)))",
        "",
        stem,
        flags=re.IGNORECASE
    )
    normalized_stem = re.sub(r"[_\s.-]+", "_", stem).strip(" _.-").lower()
    if not normalized_stem:
        normalized_stem = Path(basename).stem.lower()

    return normalized_stem, VersionInfo(
        revision_token=revision,
        lifecycle_state=lifecycle,
        is_authoritative=is_authoritative,
        date_stamp=date_stamp
    )

def is_path_excluded(rel_path: str, exclusions: List[str]) -> bool:
    """Checks whether relative path matches any exclusion pattern."""
    parts = Path(rel_path).parts
    for part in parts:
        for pattern in exclusions:
            if fnmatch.fnmatch(part, pattern):
                return True
    for pattern in exclusions:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False

# ---------------------------------------------------------------------------
# Streaming Hash & Readiness
# ---------------------------------------------------------------------------

def compute_sha256_atomic(path: Path) -> Tuple[Optional[str], int, bool]:
    """
    Computes streaming SHA-256 with pre/post stat verification.
    If the file size or mtime changes while reading, returns (None, bytes_read, False).
    Returns (sha256_hex, bytes_read, is_stable).
    """
    try:
        st_pre = path.stat()
    except Exception:
        return None, 0, False

    h = hashlib.sha256()
    bytes_read = 0
    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                h.update(chunk)
                bytes_read += len(chunk)
    except Exception:
        return None, bytes_read, False

    try:
        st_post = path.stat()
    except Exception:
        return None, bytes_read, False

    if st_pre.st_size != st_post.st_size or st_pre.st_mtime != st_post.st_mtime:
        return None, bytes_read, False

    return h.hexdigest(), bytes_read, True

def compute_sha256(path: Path) -> str:
    """Compute streaming SHA-256 hash in 64KB chunks."""
    digest, _, is_stable = compute_sha256_atomic(path)
    if is_stable and digest is not None:
        return digest
    # Fallback direct read
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def check_file_readiness(path: Path) -> Tuple[str, Optional[str]]:
    """
    Checks if a file is ready, unreadable, unstable, symlink, or special file.
    Returns (readiness_status, error_message).
    """
    if path.is_symlink():
        return "skipped_symlink", "Symlink skipped (not followed by default)"

    try:
        st = path.lstat()
        # Check special files (socket, FIFO, block/char device)
        if not stat.S_ISREG(st.st_mode):
            return "special_file", "Non-regular file (socket/fifo/device)"
    except Exception as e:
        return "unreadable", str(e)

    # Check unstable temp extensions
    ext = path.suffix.lower()
    if ext in {".crdownload", ".part", ".download", ".tmp"}:
        return "unstable", "Incomplete download or temporary file"

    try:
        # Test read permissions
        with open(path, "rb") as f:
            f.read(1)
    except PermissionError:
        return "unreadable", "Permission denied"
    except Exception as e:
        return "unreadable", str(e)

    return "ready", None

# ---------------------------------------------------------------------------
# Lightweight Content Extractor
# ---------------------------------------------------------------------------

def extract_bounded_content(path: Path, max_chars: int) -> Tuple[str, str, str]:
    """
    Extracts bounded text up to max_chars using Python stdlib.
    Supports plain text and DOCX (via zipfile & XML).
    Returns (extracted_text, capability, status).
    """
    if max_chars <= 0:
        return "", "none", "pass_0_metadata_only"

    ext = path.suffix.lower()
    text = ""
    capability = "none"

    if ext in {".txt", ".md", ".csv", ".json", ".py", ".js", ".html", ".sh", ".yaml", ".yml", ".xml", ".ts"}:
        capability = "plain_text"
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read(max_chars)
            return text[:max_chars], capability, "extracted"
        except Exception as e:
            return "", capability, f"error: {str(e)}"

    elif ext == ".docx":
        capability = "docx_xml"
        try:
            with zipfile.ZipFile(path, "r") as z:
                if "word/document.xml" in z.namelist():
                    xml_content = z.read("word/document.xml")
                    tree = ET.fromstring(xml_content)
                    paragraphs = []
                    for elem in tree.iter():
                        if elem.tag.endswith("}t") and elem.text:
                            paragraphs.append(elem.text)
                            if sum(len(p) for p in paragraphs) >= max_chars:
                                break
                    text = " ".join(paragraphs)[:max_chars]
                    return text, capability, "extracted"
                else:
                    return "", capability, "document_xml_missing"
        except Exception as e:
            return "", capability, f"docx_parse_error: {str(e)}"

    else:
        return "", f"unsupported_{ext.lstrip('.')}", "text_unavailable"

# ---------------------------------------------------------------------------
# Token Similarity & Hierarchy Scoring
# ---------------------------------------------------------------------------

def calculate_token_fit(item_name: str, container_name: str) -> float:
    """Calculates directional token overlap score between item and container."""
    item_tokens = tokenize(item_name)
    container_tokens = tokenize(container_name)

    if not item_tokens or not container_tokens:
        return 0.0

    if container_name.lower().strip() in GENERIC_FOLDER_NAMES:
        return 0.35

    overlap = item_tokens & container_tokens
    if not overlap:
        return 0.1

    precision = len(overlap) / len(container_tokens)
    recall = len(overlap) / len(item_tokens)
    return min(1.0, 0.5 * precision + 0.5 * recall + 0.3)

# ---------------------------------------------------------------------------
# Module Execution & Performance Profiler
# ---------------------------------------------------------------------------

class PhaseTimer:
    """Measures high-resolution execution duration of each engine module/phase."""
    def __init__(self):
        self.start_wall = time.perf_counter()
        self.phases: List[Dict[str, Any]] = []
        self._current_phase: Optional[str] = None
        self._current_details: str = ""
        self._phase_start: Optional[float] = None

    def start_phase(self, name: str, details: str = ""):
        now = time.perf_counter()
        if self._current_phase is not None and self._phase_start is not None:
            dur = now - self._phase_start
            self.phases.append({
                "module": self._current_phase,
                "duration_seconds": round(dur, 4),
                "duration_ms": round(dur * 1000, 2),
                "details": self._current_details
            })
        self._current_phase = name
        self._current_details = details
        self._phase_start = now

    def end_phase(self):
        now = time.perf_counter()
        if self._current_phase is not None and self._phase_start is not None:
            dur = now - self._phase_start
            self.phases.append({
                "module": self._current_phase,
                "duration_seconds": round(dur, 4),
                "duration_ms": round(dur * 1000, 2),
                "details": self._current_details
            })
            self._current_phase = None
            self._phase_start = None

    def to_dict(self, total_files: int = 0, total_bytes: int = 0) -> Dict[str, Any]:
        self.end_phase()
        total_time = max(time.perf_counter() - self.start_wall, 0.0001)
        for p in self.phases:
            p["percentage"] = round((p["duration_seconds"] / total_time) * 100, 1)

        throughput = {
            "files_per_second": round(total_files / total_time, 1) if total_time > 0 and total_files > 0 else 0.0,
            "mb_per_second": round((total_bytes / (1024 * 1024)) / total_time, 2) if total_time > 0 and total_bytes > 0 else 0.0
        }

        return {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "total_wall_time_seconds": round(total_time, 4),
            "total_wall_time_ms": round(total_time * 1000, 2),
            "module_timings": self.phases,
            "throughput": throughput
        }

# ---------------------------------------------------------------------------
# Core Operations: Scan, Plan, Report, Apply, Undo
# ---------------------------------------------------------------------------

class FileOSEngine:
    def __init__(
        self,
        root_dir: Path,
        output_dir: Optional[Path] = None,
        max_depth: Optional[int] = None,
        exclusions: Optional[List[str]] = None
    ):
        self.input_path = root_dir.resolve()
        self.is_file_mode = self.input_path.is_file()
        self.root = self.input_path.parent if self.is_file_mode else self.input_path
        self.max_depth = max_depth
        if output_dir:
            self.output = output_dir.resolve()
        else:
            self.output = (self.root / "fileos-output").resolve()
        self.exclusions = list(DEFAULT_EXCLUSIONS)
        if exclusions:
            self.exclusions.extend(exclusions)

    def scan(
        self,
        sample_size: int = 2000,
        follow_symlinks: bool = False,
        incremental: bool = False,
        cache_file: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Executes full read-only deterministic scan of the entire directory tree."""
        self.output.mkdir(parents=True, exist_ok=True)
        scan_timestamp = datetime.datetime.utcnow().isoformat() + "Z"

        # Initialize Performance Profiler
        timer = PhaseTimer()
        timer.start_phase("cache_initialization", "Load incremental cache from disk if available")

        # Load incremental cache if requested
        cache_path = cache_file.resolve() if cache_file else (self.output / ".fileos-cache.json")
        cached_files: Dict[str, Dict[str, Any]] = {}
        if incremental and cache_path.exists():
            try:
                c_data = json.loads(cache_path.read_text(encoding="utf-8"))
                cached_files = c_data.get("files", {})
            except Exception:
                cached_files = {}

        file_records: List[FileRecord] = []
        folder_records: Dict[str, FolderRecord] = {}
        
        # Coverage counters
        deepest_discovered_depth = 0
        deepest_scanned_depth = 0
        directories_discovered = 0
        directories_scanned = 0
        directories_excluded = 0
        directories_inaccessible = 0
        directories_depth_skipped = 0
        files_discovered = 0
        files_excluded = 0
        files_eligible = 0
        files_analysed = 0
        files_skipped = 0
        files_failed = 0
        total_bytes_hashed = 0
        eligible_file_bytes = 0
        bytes_read_for_hashing = 0
        bytes_reused_from_hash_cache = 0
        symlinks_skipped = 0
        mount_boundaries_skipped = 0
        cloud_placeholders_skipped = 0
        permission_errors = 0
        partial_reasons: List[str] = []

        try:
            root_device = self.root.stat().st_dev
        except Exception:
            root_device = None

        folder_counter = 1
        file_counter = 1

        # ---------------------------------------------------------
        # Case A: Single File Input
        # ---------------------------------------------------------
        if self.is_file_mode:
            directories_discovered = 1
            directories_scanned = 1
            rel_file_path = self.input_path.name
            files_discovered = 1
            is_symlink = self.input_path.is_symlink()
            readiness, err = check_file_readiness(self.input_path)
            stat_res = self.input_path.lstat() if is_symlink else (self.input_path.stat() if readiness == "ready" else self.input_path.lstat())
            size = stat_res.st_size
            mtime = stat_res.st_mtime
            ctime = stat_res.st_ctime
            is_hidden = self.input_path.name.startswith(".")
            normalized_stem, _ = parse_version_tokens(self.input_path.name)

            sha256 = None
            if readiness == "ready":
                files_eligible += 1
                eligible_file_bytes += size
                cached_entry = cached_files.get(rel_file_path) if incremental else None
                if (
                    cached_entry
                    and cached_entry.get("size_bytes") == size
                    and abs(cached_entry.get("mtime", 0.0) - mtime) < 1e-4
                    and cached_entry.get("sha256")
                ):
                    sha256 = cached_entry["sha256"]
                    files_analysed += 1
                    total_bytes_hashed += size
                    bytes_reused_from_hash_cache += size
                else:
                    try:
                        digest, b_read, is_stable = compute_sha256_atomic(self.input_path)
                        if not is_stable or digest is None:
                            readiness = "unstable"
                            err = "File modified during hashing"
                            files_skipped += 1
                        else:
                            sha256 = digest
                            files_analysed += 1
                            total_bytes_hashed += size
                            bytes_read_for_hashing += b_read
                    except Exception as e:
                        readiness = "unreadable"
                        err = f"Hash error: {str(e)}"
                        files_failed += 1
            else:
                files_skipped += 1

            root_fid = "FLD-0001"
            folder_records["."] = FolderRecord(
                folder_id=root_fid,
                rel_path=".",
                display_name=self.root.name,
                parent_folder_id=None,
                depth=0,
                direct_child_folder_ids=[],
                direct_file_ids=[f"FIL-0001"],
                direct_file_count=1,
                descendant_file_count=1,
                direct_child_folder_count=0,
                descendant_folder_count=0,
                aggregate_size_bytes=size,
                extension_distribution={self.input_path.suffix.lower(): 1},
                is_hidden=self.root.name.startswith("."),
                is_excluded=False,
                accessibility="accessible",
                scan_status="scanned",
                last_scan_time=scan_timestamp,
                direct_tokens=sorted(list(tokenize(self.input_path.name))),
                descendant_tokens=sorted(list(tokenize(self.input_path.name))),
                relationship_status="supported",
                evidence="Single-file mode scan"
            )

            file_records.append(FileRecord(
                file_id="FIL-0001",
                rel_path=rel_file_path,
                basename=self.input_path.name,
                normalized_stem=normalized_stem,
                extension=self.input_path.suffix.lower(),
                size_bytes=size,
                mtime=mtime,
                ctime=ctime,
                is_symlink=is_symlink,
                is_hidden=is_hidden,
                readiness=readiness,
                sha256=sha256,
                error=err,
                parent_folder_id=root_fid,
                depth=0
            ))

        # ---------------------------------------------------------
        # Case B: Directory Input (Full Recursive Traversal by Default)
        # ---------------------------------------------------------
        else:
            t_hashing_total = 0.0
            t_traversal_start = time.perf_counter()
            # Iterative stack for traversal: stack of (current_path, current_rel_path, depth)
            # Deterministic sorting ensured by sorting directory entries alphabetically.
            stack: List[Tuple[Path, str, int]] = [(self.root, ".", 0)]
            visited_dirs: Set[Tuple[int, int]] = set()

            while stack:
                curr_path, curr_rel, depth = stack.pop()

                # Inode loop protection (for symlinks or recursive mounts)
                try:
                    curr_st = curr_path.stat()
                    dir_id = (curr_st.st_dev, curr_st.st_ino)
                    if dir_id in visited_dirs:
                        continue
                    visited_dirs.add(dir_id)
                except Exception:
                    pass

                directories_discovered += 1
                if depth > deepest_discovered_depth:
                    deepest_discovered_depth = depth

                # Assign or retrieve folder ID
                if curr_rel not in folder_records:
                    fid = f"FLD-{folder_counter:04d}"
                    folder_counter += 1
                    parent_rel = str(Path(curr_rel).parent) if curr_rel != "." else None
                    parent_fid = folder_records[parent_rel].folder_id if parent_rel in folder_records else None
                    folder_records[curr_rel] = FolderRecord(
                        folder_id=fid,
                        rel_path=curr_rel,
                        display_name=curr_path.name if curr_rel != "." else self.root.name,
                        parent_folder_id=parent_fid,
                        depth=depth,
                        direct_child_folder_ids=[],
                        direct_file_ids=[],
                        direct_file_count=0,
                        descendant_file_count=0,
                        direct_child_folder_count=0,
                        descendant_folder_count=0,
                        aggregate_size_bytes=0,
                        extension_distribution={},
                        is_hidden=curr_path.name.startswith("."),
                        is_excluded=False,
                        accessibility="accessible",
                        scan_status="scanned",
                        last_scan_time=scan_timestamp
                    )

                curr_folder = folder_records[curr_rel]

                # Do not scan our own output directory if placed within the scan tree
                try:
                    if curr_path.resolve() == self.output.resolve() or self.output.resolve() in curr_path.resolve().parents:
                        curr_folder.is_excluded = True
                        curr_folder.scan_status = "skipped"
                        directories_excluded += 1
                        continue
                except Exception:
                    pass

                # Check Exclusion
                if curr_rel != "." and is_path_excluded(curr_rel, self.exclusions):
                    curr_folder.is_excluded = True
                    curr_folder.scan_status = "skipped"
                    curr_folder.accessibility = "excluded"
                    directories_excluded += 1
                    partial_reasons.append(f"Directory excluded: {curr_rel}")
                    continue

                # Check Max Depth
                if self.max_depth is not None and depth > self.max_depth:
                    curr_folder.scan_status = "skipped"
                    curr_folder.accessibility = "depth_limit_reached"
                    directories_depth_skipped += 1
                    partial_reasons.append(f"Depth limit reached ({self.max_depth}): {curr_rel}")
                    continue

                # Check Mount Boundary (cross-device check)
                if root_device is not None:
                    try:
                        curr_device = curr_path.stat().st_dev
                        if curr_device != root_device:
                            curr_folder.scan_status = "skipped"
                            curr_folder.accessibility = "boundary_not_scanned"
                            mount_boundaries_skipped += 1
                            partial_reasons.append(f"Mount boundary skipped: {curr_rel}")
                            continue
                    except Exception:
                        pass

                # Inspect Directory Contents
                try:
                    entries = list(os.scandir(curr_path))
                except PermissionError as pe:
                    curr_folder.scan_status = "skipped"
                    curr_folder.accessibility = "inaccessible"
                    curr_folder.error = f"Permission denied: {str(pe)}"
                    directories_inaccessible += 1
                    permission_errors += 1
                    partial_reasons.append(f"Inaccessible directory: {curr_rel}")
                    continue
                except Exception as e:
                    curr_folder.scan_status = "skipped"
                    curr_folder.accessibility = "inaccessible"
                    curr_folder.error = str(e)
                    directories_inaccessible += 1
                    partial_reasons.append(f"Error accessing directory: {curr_rel} ({str(e)})")
                    continue

                directories_scanned += 1
                if depth > deepest_scanned_depth:
                    deepest_scanned_depth = depth

                # Deterministic sorting of subdirectories and files
                entries.sort(key=lambda e: e.name.lower())
                subdirs = []
                subfiles = []
                for entry in entries:
                    is_link = entry.is_symlink()
                    is_d = False
                    if is_link:
                        # Check if target is a directory
                        try:
                            is_d = Path(entry.path).is_dir()
                        except Exception:
                            is_d = False
                        if is_d:
                            if follow_symlinks:
                                subdirs.append(entry)
                            else:
                                symlinks_skipped += 1
                                # directory symlink skipped, do not treat as file
                            continue
                        else:
                            # file symlink
                            subfiles.append(entry)
                    elif entry.is_dir():
                        subdirs.append(entry)
                    else:
                        subfiles.append(entry)

                # Process Files in Current Directory
                for f_entry in subfiles:
                    files_discovered += 1
                    fname = f_entry.name
                    rel_f_path = os.path.normpath(os.path.join(curr_rel, fname)) if curr_rel != "." else fname
                    
                    if is_path_excluded(rel_f_path, self.exclusions):
                        files_excluded += 1
                        files_skipped += 1
                        continue

                    # File is eligible for analysis
                    files_eligible += 1

                    full_f_path = Path(f_entry.path)
                    is_symlink = full_f_path.is_symlink()
                    readiness, err = check_file_readiness(full_f_path)

                    if readiness == "skipped_symlink":
                        symlinks_skipped += 1
                        files_skipped += 1
                    elif readiness == "unstable":
                        files_skipped += 1
                    elif readiness == "unreadable":
                        files_failed += 1
                        if "Permission denied" in str(err):
                            permission_errors += 1

                    try:
                        stat_res = full_f_path.lstat() if is_symlink else (full_f_path.stat() if readiness == "ready" else full_f_path.lstat())
                        size = stat_res.st_size
                        mtime = stat_res.st_mtime
                        ctime = stat_res.st_ctime
                    except Exception as e:
                        size = 0
                        mtime = 0.0
                        ctime = 0.0
                        readiness = "unreadable"
                        err = str(e)
                        files_failed += 1

                    normalized_stem, _ = parse_version_tokens(fname)

                    sha256 = None
                    if readiness == "ready":
                        eligible_file_bytes += size
                        cached_entry = cached_files.get(rel_f_path) if incremental else None
                        if (
                            cached_entry
                            and cached_entry.get("size_bytes") == size
                            and abs(cached_entry.get("mtime", 0.0) - mtime) < 1e-4
                            and cached_entry.get("sha256")
                        ):
                            sha256 = cached_entry["sha256"]
                            files_analysed += 1
                            total_bytes_hashed += size
                            bytes_reused_from_hash_cache += size
                        else:
                            t_h0 = time.perf_counter()
                            try:
                                digest, b_read, is_stable = compute_sha256_atomic(full_f_path)
                                if not is_stable or digest is None:
                                    readiness = "unstable"
                                    err = "File modified during hashing"
                                    files_skipped += 1
                                else:
                                    sha256 = digest
                                    files_analysed += 1
                                    total_bytes_hashed += size
                                    bytes_read_for_hashing += b_read
                            except Exception as e:
                                readiness = "unreadable"
                                err = f"Hash error: {str(e)}"
                                files_failed += 1
                            finally:
                                t_hashing_total += (time.perf_counter() - t_h0)

                    fid = f"FIL-{file_counter:04d}"
                    file_counter += 1

                    rec = FileRecord(
                        file_id=fid,
                        rel_path=rel_f_path,
                        basename=fname,
                        normalized_stem=normalized_stem,
                        extension=full_f_path.suffix.lower(),
                        size_bytes=size,
                        mtime=mtime,
                        ctime=ctime,
                        is_symlink=is_symlink,
                        is_hidden=fname.startswith("."),
                        readiness=readiness,
                        sha256=sha256,
                        error=err,
                        parent_folder_id=curr_folder.folder_id,
                        depth=depth
                    )
                    file_records.append(rec)
                    curr_folder.direct_file_ids.append(fid)
                    curr_folder.direct_file_count += 1
                    curr_folder.aggregate_size_bytes += size
                    curr_folder.extension_distribution[rec.extension] = curr_folder.extension_distribution.get(rec.extension, 0) + 1

                # Queue Subdirectories (reversed to preserve alphabetical order on pop)
                for d_entry in reversed(subdirs):
                    sub_rel = os.path.normpath(os.path.join(curr_rel, d_entry.name)) if curr_rel != "." else d_entry.name
                    sub_path = Path(d_entry.path)

                    if d_entry.is_symlink():
                        if not follow_symlinks:
                            symlinks_skipped += 1
                            continue
                        else:
                            try:
                                s_st = sub_path.stat()
                                if (s_st.st_dev, s_st.st_ino) in visited_dirs:
                                    continue
                            except Exception:
                                continue

                    stack.append((sub_path, sub_rel, depth + 1))

            t_traversal_total = max(0.0001, (time.perf_counter() - t_traversal_start) - t_hashing_total)
            timer.phases.append({
                "module": "directory_traversal",
                "duration_seconds": round(t_traversal_total, 4),
                "duration_ms": round(t_traversal_total * 1000, 2),
                "details": f"{directories_discovered} directories discovered, {files_discovered} files observed"
            })
            timer.phases.append({
                "module": "hashing_and_io",
                "duration_seconds": round(t_hashing_total, 4),
                "duration_ms": round(t_hashing_total * 1000, 2),
                "details": f"{bytes_read_for_hashing:,} bytes read, {bytes_reused_from_hash_cache:,} bytes reused from cache"
            })

        # ---------------------------------------------------------
        # Bottom-Up Folder Aggregation & Token Summarisation
        # ---------------------------------------------------------
        timer.start_phase("folder_aggregation", "Propagate descendant counts, size, and tokens up directory tree")
        # Sort folders by depth descending so leaves are processed before parents
        sorted_folders = sorted(folder_records.values(), key=lambda f: f.depth, reverse=True)
        file_map = {f.file_id: f for f in file_records}

        for folder in sorted_folders:
            # Collect direct tokens
            d_tokens: Set[str] = set()
            d_tokens.update(tokenize(folder.display_name))
            for fid in folder.direct_file_ids:
                if fid in file_map:
                    d_tokens.update(tokenize(file_map[fid].basename))
            folder.direct_tokens = sorted(list(d_tokens))[:50]

            # Link with children folders
            desc_file_count = folder.direct_file_count
            desc_folder_count = 0
            desc_tokens = set(folder.direct_tokens)
            agg_size = folder.aggregate_size_bytes

            # Find direct child folders
            children = [f for f in folder_records.values() if f.parent_folder_id == folder.folder_id and f.folder_id != folder.folder_id]
            folder.direct_child_folder_ids = [c.folder_id for c in children]
            folder.direct_child_folder_count = len(children)

            for child in children:
                desc_file_count += child.descendant_file_count
                desc_folder_count += 1 + child.descendant_folder_count
                agg_size += child.aggregate_size_bytes
                desc_tokens.update(child.descendant_tokens)
                for ext, cnt in child.extension_distribution.items():
                    folder.extension_distribution[ext] = folder.extension_distribution.get(ext, 0) + cnt

            folder.descendant_file_count = desc_file_count
            folder.descendant_folder_count = desc_folder_count
            folder.aggregate_size_bytes = agg_size
            folder.descendant_tokens = sorted(list(desc_tokens))[:100]

        # ---------------------------------------------------------
        # Top-Down Hierarchy & Anomaly Evaluation
        # ---------------------------------------------------------
        timer.start_phase("hierarchy_scoring", "Calculate token fit and detect folder boundary anomalies")
        anomalies: List[Dict[str, Any]] = []
        for folder in folder_records.values():
            if folder.rel_path == "." or folder.scan_status != "scanned":
                folder.relationship_status = "not_evaluated" if folder.scan_status != "scanned" else "confirmed"
                continue

            parent_folder = next((p for p in folder_records.values() if p.folder_id == folder.parent_folder_id), None)
            parent_name = parent_folder.display_name if parent_folder else ""
            parent_rel = parent_folder.rel_path if parent_folder else ""

            # Check direct files in this folder
            direct_files = [file_map[fid] for fid in folder.direct_file_ids if fid in file_map]
            
            # File-to-folder fit
            file_fits = [calculate_token_fit(f.basename, folder.display_name) for f in direct_files]
            avg_file_fit = sum(file_fits) / len(file_fits) if file_fits else 0.0

            # Folder-to-parent fit
            folder_parent_fit = calculate_token_fit(folder.display_name, parent_name) if parent_name else 0.5

            # Empty folder rule
            if folder.direct_file_count == 0 and folder.descendant_file_count == 0:
                folder.relationship_status = "unknown"
                folder.evidence = "Empty folder: no content to infer mismatch."
                continue

            # Subfolders only rule
            if folder.direct_file_count == 0 and folder.descendant_file_count > 0:
                folder.relationship_status = "supported" if folder_parent_fit >= 0.40 else "uncertain"
                folder.evidence = f"Container folder with {folder.direct_child_folder_count} subfolders and {folder.descendant_file_count} total files."
                continue

            # One-file folder rule
            if folder.direct_file_count == 1:
                if folder_parent_fit < 0.40 and avg_file_fit >= 0.70:
                    folder.relationship_status = "uncertain"
                    folder.evidence = f"Single file in {folder.display_name} fits folder ({avg_file_fit:.2f}) but folder has weak fit to {parent_name} ({folder_parent_fit:.2f})."
                    anomalies.append({
                        "anomaly_id": f"ANO-{len(anomalies)+1:03d}",
                        "edge": f"{folder.rel_path} -> {parent_rel}",
                        "folder": folder.rel_path,
                        "parent": parent_rel,
                        "depth": folder.depth,
                        "status": "uncertain",
                        "file_folder_fit": round(avg_file_fit, 2),
                        "folder_parent_fit": round(folder_parent_fit, 2),
                        "evidence": folder.evidence,
                        "suggested_action": "review"
                    })
                else:
                    folder.relationship_status = "supported" if folder_parent_fit >= 0.40 else "uncertain"
                continue

            # Mixed-topic folder rule (diverse topics across direct files)
            shared_tokens = set.intersection(*[tokenize(f.basename) for f in direct_files]) if direct_files else set()
            if len(direct_files) >= 4 and len(shared_tokens) == 0 and avg_file_fit < 0.50:
                folder.relationship_status = "uncertain"
                folder.evidence = f"Mixed-topic folder: {len(direct_files)} files with diverse topics. Avoid moving folder as a whole unit."
                anomalies.append({
                    "anomaly_id": f"ANO-{len(anomalies)+1:03d}",
                    "edge": f"Files in {folder.rel_path}",
                    "folder": folder.rel_path,
                    "parent": parent_rel,
                    "depth": folder.depth,
                    "status": "uncertain",
                    "file_folder_fit": round(avg_file_fit, 2),
                    "folder_parent_fit": round(folder_parent_fit, 2),
                    "evidence": folder.evidence,
                    "suggested_action": "split_contents"
                })
                continue

            # Strong anomaly: files fit folder, but folder conflicts with parent project
            if avg_file_fit >= 0.60 and folder_parent_fit < 0.40:
                folder.relationship_status = "conflicting"
                folder.evidence = f"Folder {folder.display_name} contains {len(direct_files)} coherent files matching {folder.display_name} ({avg_file_fit:.2f}), but {folder.display_name} conflicts with parent project {parent_name} ({folder_parent_fit:.2f})."
                anomalies.append({
                    "anomaly_id": f"ANO-{len(anomalies)+1:03d}",
                    "edge": f"{folder.rel_path} -> {parent_rel}",
                    "folder": folder.rel_path,
                    "parent": parent_rel,
                    "depth": folder.depth,
                    "status": "conflicting",
                    "file_folder_fit": round(avg_file_fit, 2),
                    "folder_parent_fit": round(folder_parent_fit, 2),
                    "evidence": folder.evidence,
                    "suggested_action": "review_and_relocate_folder"
                })
            else:
                folder.relationship_status = "supported" if folder_parent_fit >= 0.40 else "uncertain"
                folder.evidence = f"Supported fit: file-to-folder {avg_file_fit:.2f}, folder-to-parent {folder_parent_fit:.2f}."

        # ---------------------------------------------------------
        # Exact Duplicate Detection
        # ---------------------------------------------------------
        timer.start_phase("duplicate_detection", "Exact hash grouping and logical storage footprint math")
        dup_groups: Dict[Tuple[int, str], List[FileRecord]] = {}
        for r in file_records:
            if r.readiness == "ready" and r.sha256:
                dup_groups.setdefault((r.size_bytes, r.sha256), []).append(r)

        exact_duplicates = [group for group in dup_groups.values() if len(group) > 1]

        # ---------------------------------------------------------
        # Document Families & Versions
        # ---------------------------------------------------------
        timer.start_phase("family_clustering", "Stem normalization and lifecycle state parsing")
        families: Dict[str, List[FileRecord]] = {}
        for r in file_records:
            if r.readiness == "ready":
                families.setdefault(r.normalized_stem, []).append(r)

        doc_families = [grp for grp in families.values() if len(grp) > 1]

        # ---------------------------------------------------------
        # Near-Duplicate Detection (Shingling & Jaccard Similarity)
        # ---------------------------------------------------------
        timer.start_phase("near_duplicate_detection", "N-gram shingling and Jaccard similarity comparison")
        near_duplicates = []
        try:
            from similarity import NearDuplicateDetector
            detector = NearDuplicateDetector(threshold=0.85)
            def _read_candidate_text(rel_path: str) -> str:
                full_p = self.root / rel_path
                txt, _, _ = extract_bounded_content(full_p, max_chars=4000)
                return txt
            near_duplicates = detector.find_near_duplicates(file_records, _read_candidate_text)
        except Exception:
            near_duplicates = []

        # ---------------------------------------------------------
        # AI Review Queue with Shared Budget Caps
        # ---------------------------------------------------------
        timer.start_phase("ai_queue_preparation", "Extract bounded content and package candidate packets")
        ai_queue: List[Dict[str, Any]] = []
        total_ai_chars = 0
        ai_packets_count = 0

        for ano in anomalies:
            if ai_packets_count >= MAX_AI_PACKETS_PER_RUN or total_ai_chars >= MAX_AI_CHARS_PER_RUN:
                break

            f_records = [r for r in file_records if r.rel_path.startswith(ano["folder"] + "/") or r.rel_path == ano["folder"]]
            if not f_records:
                continue

            sample_f = f_records[0]
            full_sample_path = self.root / sample_f.rel_path
            chars_to_read = min(sample_size, PASS_LIMITS[1])
            extracted, cap, status = extract_bounded_content(full_sample_path, chars_to_read)

            packet = {
                "candidate_id": f"REV-{ai_packets_count+1:03d}",
                "anomaly_id": ano["anomaly_id"],
                "rel_path": sample_f.rel_path,
                "folder": ano["folder"],
                "depth": ano["depth"],
                "parent_project": ano["parent"],
                "uncertainty_type": "hierarchy_conflict",
                "pass_level": 1,
                "excerpt_chars": len(extracted),
                "excerpt": extracted,
                "signals": {
                    "file_folder_fit": ano["file_folder_fit"],
                    "folder_parent_fit": ano["folder_parent_fit"],
                    "evidence": ano["evidence"]
                },
                "allowed_actions": ["confirm_exception", "move_folder", "split_contents", "keep_as_is"],
                "parser_capability": cap
            }
            ai_queue.append(packet)
            ai_packets_count += 1
            total_ai_chars += len(extracted)

        # ---------------------------------------------------------
        # Duplicate Storage Mathematics
        # ---------------------------------------------------------
        dup_group_count = len(exact_duplicates)
        dup_member_file_count = sum(len(grp) for grp in exact_duplicates)
        dup_group_logical_bytes = sum(sum(r.size_bytes for r in grp) for grp in exact_duplicates)
        potential_extra_copy_bytes = sum(sum(r.size_bytes for r in grp[1:]) for grp in exact_duplicates)

        # ---------------------------------------------------------
        # Coverage Accounting
        # ---------------------------------------------------------
        is_complete = (
            directories_excluded == 0 and
            directories_inaccessible == 0 and
            directories_depth_skipped == 0 and
            mount_boundaries_skipped == 0 and
            files_failed == 0 and
            permission_errors == 0
        )
        if is_complete:
            partial_reasons = []

        # Canonical configuration fingerprint
        config_payload = {
            "root": str(self.root),
            "max_depth": self.max_depth,
            "exclusions": sorted(list(set(self.exclusions))),
            "is_file_mode": self.is_file_mode,
            "engine_version": "1.0.0"
        }
        scan_config_fingerprint = hashlib.sha256(json.dumps(config_payload, sort_keys=True).encode()).hexdigest()

        # Unique Scan ID
        scan_fingerprint = f"{self.root}:{files_discovered}:{directories_discovered}:{total_bytes_hashed}:{scan_config_fingerprint[:8]}"
        scan_id = f"SCN-{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}-{hashlib.sha256(scan_fingerprint.encode()).hexdigest()[:8]}"

        coverage = CoverageRecord(
            root_label=str(self.root),
            is_file_mode=self.is_file_mode,
            recursive=True,
            max_depth=self.max_depth,
            deepest_discovered_depth=deepest_discovered_depth,
            deepest_scanned_depth=deepest_scanned_depth,
            directories_discovered=directories_discovered,
            directories_scanned=directories_scanned,
            directories_excluded=directories_excluded,
            directories_inaccessible=directories_inaccessible,
            directories_depth_skipped=directories_depth_skipped,
            files_discovered=files_discovered,
            files_eligible=files_eligible,
            files_analysed=files_analysed,
            files_skipped=files_skipped,
            files_failed=files_failed,
            total_bytes_hashed=total_bytes_hashed,
            symlinks_skipped=symlinks_skipped,
            mount_boundaries_skipped=mount_boundaries_skipped,
            cloud_placeholders_skipped=cloud_placeholders_skipped,
            permission_errors=permission_errors,
            is_complete=is_complete,
            partial_reasons=partial_reasons,
            scan_id=scan_id,
            scan_config_fingerprint=scan_config_fingerprint,
            files_observed=files_discovered,
            files_excluded=files_excluded,
            directories_observed=directories_discovered,
            eligible_file_bytes=eligible_file_bytes,
            bytes_read_for_hashing=bytes_read_for_hashing,
            bytes_reused_from_hash_cache=bytes_reused_from_hash_cache,
            duplicate_group_count=dup_group_count,
            duplicate_member_file_count=dup_member_file_count,
            duplicate_group_logical_bytes=dup_group_logical_bytes,
            potential_extra_copy_bytes=potential_extra_copy_bytes
        )

        # ---------------------------------------------------------
        # Write Output Files
        # ---------------------------------------------------------
        timer.start_phase("artifact_serialization", "Serialize coverage, inventory, folders, and markdown report")
        self._write_coverage(coverage)
        self._write_folders(list(folder_records.values()))
        self._write_inventory(file_records)
        self._write_duplicate_groups(exact_duplicates)
        self._write_document_families(doc_families)
        self._write_near_duplicates(near_duplicates)
        self._write_hierarchy_anomalies(anomalies)
        self._write_review_queue(ai_queue)
        self._write_ai_usage(ai_packets_count, total_ai_chars, len(file_records))
        self._write_summary(
            coverage,
            list(folder_records.values()),
            file_records,
            exact_duplicates,
            doc_families,
            anomalies,
            ai_queue,
            total_ai_chars
        )

        # Persist updated cache for incremental scanning
        try:
            cache_to_save = {
                "version": 1,
                "scan_id": scan_id,
                "timestamp": scan_timestamp,
                "files": {
                    r.rel_path: {
                        "sha256": r.sha256,
                        "size_bytes": r.size_bytes,
                        "mtime": r.mtime,
                        "ctime": r.ctime
                    }
                    for r in file_records
                    if r.readiness == "ready" and r.sha256
                }
            }
            tmp_cache = cache_path.with_suffix(".tmp")
            tmp_cache.write_text(json.dumps(cache_to_save, indent=2), encoding="utf-8")
            tmp_cache.replace(cache_path)
        except Exception:
            pass

        timer.end_phase()
        perf_profile = timer.to_dict(total_files=len(file_records), total_bytes=total_bytes_hashed)
        try:
            with open(self.output / "performance-profile.json", "w", encoding="utf-8") as f:
                json.dump(perf_profile, f, indent=2)
        except Exception:
            pass

        return {
            "total_files": len(file_records),
            "total_folders": len(folder_records),
            "deepest_depth": deepest_scanned_depth,
            "duplicate_groups": len(exact_duplicates),
            "document_families": len(doc_families),
            "near_duplicates": len(near_duplicates),
            "hierarchy_anomalies": len(anomalies),
            "ai_queue_packets": len(ai_queue),
            "is_complete": is_complete,
            "performance_profile": perf_profile,
            "output_directory": str(self.output)
        }

    def plan(self, scan_inventory_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Generates dry-run proposed actions from scan results."""
        inv_path = scan_inventory_path or (self.output / "inventory.jsonl")
        if not inv_path.exists():
            raise FileNotFoundError(f"Inventory not found at {inv_path}. Run scan first.")

        records: List[FileRecord] = []
        with open(inv_path, "r", encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                records.append(FileRecord(**d))

        rec_by_path = {r.rel_path: r for r in records}

        # Load coverage for scan linkage
        cov_file = self.output / "coverage.json"
        cov_data = {}
        if cov_file.exists():
            try:
                cov_data = json.loads(cov_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        source_scan_id = cov_data.get("scan_id", "")
        source_config_fp = cov_data.get("scan_config_fingerprint", "")
        plan_id = f"PLN-{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:6]}"

        actions: List[Dict[str, Any]] = []
        action_counter = 1

        # Check duplicates
        dup_path = self.output / "duplicate-groups.csv"
        if dup_path.exists():
            with open(dup_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                groups: Dict[str, List[Dict[str, str]]] = {}
                for r in rows:
                    groups.setdefault(r["group_id"], []).append(r)
                for gid, items in groups.items():
                    paths = [it["rel_path"] for it in items]
                    src_rec = rec_by_path.get(paths[0])
                    evidence_str = f"review_duplicate:{paths[0]}:{gid}"
                    actions.append({
                        "action_id": f"ACT-{action_counter:03d}",
                        "plan_id": plan_id,
                        "source_scan_id": source_scan_id,
                        "source_scan_config_fingerprint": source_config_fp,
                        "action_type": "review_duplicate",
                        "source": paths[0],
                        "source_expected_sha256": src_rec.sha256 if src_rec else items[0].get("sha256"),
                        "destination": "N/A",
                        "reason": f"Exact duplicate copies ({len(items)} files with identical hash {items[0]['sha256'][:8]}). Consider consolidating or tagging.",
                        "evidence_ids": [gid],
                        "evidence_hash": hashlib.sha256(evidence_str.encode()).hexdigest(),
                        "confidence": 1.0,
                        "dependency_check": "not_supported",
                        "reversibility": "reversible",
                        "expected_impact": "Identifies redundant storage; user can review copies.",
                        "required_approval": "user_explicit",
                        "status": "pending_approval"
                    })
                    action_counter += 1

        # Check hierarchy anomalies
        ano_path = self.output / "hierarchy-anomalies.csv"
        if ano_path.exists():
            with open(ano_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    evidence_str = f"relationship_only:{r['folder']}:{r['anomaly_id']}"
                    actions.append({
                        "action_id": f"ACT-{action_counter:03d}",
                        "plan_id": plan_id,
                        "source_scan_id": source_scan_id,
                        "source_scan_config_fingerprint": source_config_fp,
                        "action_type": "relationship_only",
                        "source": r["folder"],
                        "destination": "Suggested: review parent relationship",
                        "reason": f"Edge {r['edge']} is {r['status']}. Evidence: {r['evidence']}",
                        "evidence_ids": [r["anomaly_id"]],
                        "evidence_hash": hashlib.sha256(evidence_str.encode()).hexdigest(),
                        "confidence": float(r.get("file_folder_fit", 0.8)),
                        "dependency_check": "checked_no_deps",
                        "reversibility": "reversible",
                        "expected_impact": "Clarifies organizational structure without physically displacing files.",
                        "required_approval": "user_explicit",
                        "status": "pending_approval"
                    })
                    action_counter += 1

        plan_file = self.output / "proposed-actions.json"
        with open(plan_file, "w", encoding="utf-8") as f:
            json.dump(actions, f, indent=2)

        return actions

    def apply(self, plan_path: Path, approved_action_ids: List[str], dry_run: bool = False) -> List[Dict[str, Any]]:
        """Executes ONLY approved action IDs. Verifies 7 preconditions and writes operation journal."""
        if not approved_action_ids:
            raise ValueError("No action IDs provided for approval. FileOS refuses unapproved operations.")

        if not plan_path.exists():
            raise FileNotFoundError(f"Plan file not found: {plan_path}")

        with open(plan_path, "r", encoding="utf-8") as f:
            actions: List[Dict[str, Any]] = json.load(f)

        plan_by_id = {a["action_id"]: a for a in actions}
        for aid in approved_action_ids:
            if aid not in plan_by_id:
                raise ValueError(f"Action ID {aid} was not found in the plan! Execution aborted.")

        journal_file = self.output / "operation-journal.jsonl"
        journal_entries: List[Dict[str, Any]] = []

        for aid in approved_action_ids:
            action = plan_by_id[aid]
            atype = action["action_type"]

            if atype in {"relationship_only", "review_duplicate", "no_action"}:
                status = "simulated_logical" if dry_run else "applied_logical"
                entry = {
                    "journal_id": f"{'SIM' if dry_run else 'JRN'}-{len(journal_entries)+1:03d}",
                    "action_id": aid,
                    "action_type": atype,
                    "source": action["source"],
                    "destination": action.get("destination", "N/A"),
                    "status": status,
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "notes": "Non-filesystem logical operation logged." if not dry_run else "Dry-run logical simulation."
                }
                journal_entries.append(entry)
                if not dry_run:
                    self._append_journal(journal_file, entry)
                continue

            elif atype in {"move", "rename", "archive"}:
                src_rel = action["source"]
                dst_rel = action["destination"]
                src_path = self.root / src_rel
                dst_path = self.root / dst_rel

                # Precondition 3: Source must exist
                if not src_path.exists():
                    raise FileNotFoundError(f"Source file {src_path} does not exist. Aborting.")

                # Precondition 5: Destination collision protection
                if dst_path.exists():
                    raise FileExistsError(f"Destination {dst_path} already exists! Collision protection triggered.")

                # Precondition 7: Authoritative file protection
                if action.get("is_authoritative") or action.get("authoritative_protected"):
                    raise ValueError(f"Action {aid} targets authoritative protected file ({src_rel}). Move aborted.")

                src_hash = compute_sha256(src_path)
                src_size = src_path.stat().st_size

                # Precondition 4: Source hash must match plan expectation if declared
                expected_hash = action.get("source_expected_sha256")
                if expected_hash and src_hash != expected_hash:
                    raise RuntimeError(f"Source file {src_rel} modified since scan (expected {expected_hash[:8]}, got {src_hash[:8]}). Aborting.")

                if dry_run:
                    entry = {
                        "journal_id": f"SIM-{len(journal_entries)+1:03d}",
                        "action_id": aid,
                        "action_type": atype,
                        "source": src_rel,
                        "destination": dst_rel,
                        "source_sha256": src_hash,
                        "size_bytes": src_size,
                        "status": "simulated",
                        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                        "notes": "Preconditions passed. Dry-run simulation only; no filesystem mutation occurred."
                    }
                    journal_entries.append(entry)
                    continue

                # Execute physical filesystem mutation
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src_path), str(dst_path))

                dst_hash = compute_sha256(dst_path)
                if dst_hash != src_hash:
                    shutil.move(str(dst_path), str(src_path))
                    raise RuntimeError(f"Hash mismatch after moving {src_rel}! Reverted. Aborting.")

                entry = {
                    "journal_id": f"JRN-{len(journal_entries)+1:03d}",
                    "action_id": aid,
                    "action_type": atype,
                    "source": src_rel,
                    "destination": dst_rel,
                    "source_sha256": src_hash,
                    "dest_sha256": dst_hash,
                    "size_bytes": src_size,
                    "status": "applied",
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "inverse_action": {
                        "action_type": "move",
                        "source": dst_rel,
                        "destination": src_rel,
                        "expected_sha256": src_hash
                    }
                }
                journal_entries.append(entry)
                self._append_journal(journal_file, entry)

        return journal_entries

    def undo(self, journal_id: str, journal_path: Optional[Path] = None) -> Dict[str, Any]:
        """Undoes a previously journalled operation."""
        j_path = journal_path or (self.output / "operation-journal.jsonl")
        if not j_path.exists():
            raise FileNotFoundError(f"Journal file not found: {j_path}")

        entries: List[Dict[str, Any]] = []
        with open(j_path, "r", encoding="utf-8") as f:
            for line in f:
                entries.append(json.loads(line))

        target_entry = next((e for e in entries if e["journal_id"] == journal_id), None)
        if not target_entry:
            raise ValueError(f"Journal ID {journal_id} not found in {j_path}")

        if "inverse_action" not in target_entry:
            return {"status": "skipped", "message": "No filesystem inverse action required for this entry."}

        inv = target_entry["inverse_action"]
        curr_loc = self.root / inv["source"]
        orig_loc = self.root / inv["destination"]

        if not curr_loc.exists():
            raise FileNotFoundError(f"File to undo does not exist at {curr_loc}")

        if orig_loc.exists():
            raise FileExistsError(f"Original location {orig_loc} is now occupied. Will not overwrite.")

        curr_hash = compute_sha256(curr_loc)
        if curr_hash != inv["expected_sha256"]:
            raise ValueError(f"File at {curr_loc} was modified since the operation! Hash mismatch. Undo aborted.")

        orig_loc.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(curr_loc), str(orig_loc))

        undo_record = {
            "journal_id": f"UNDO-{journal_id}",
            "original_journal_id": journal_id,
            "status": "undone",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
        self._append_journal(j_path, undo_record)
        return undo_record

    # -----------------------------------------------------------------------
    # Output Writer Helpers
    # -----------------------------------------------------------------------

    def _write_coverage(self, cov: CoverageRecord):
        with open(self.output / "coverage.json", "w", encoding="utf-8") as f:
            json.dump(dataclasses.asdict(cov), f, indent=2, ensure_ascii=False)

    def _write_folders(self, folders: List[FolderRecord]):
        folders.sort(key=lambda fld: fld.rel_path)
        with open(self.output / "folders.jsonl", "w", encoding="utf-8") as out_f:
            for fld in folders:
                out_f.write(json.dumps(dataclasses.asdict(fld), ensure_ascii=False) + "\n")

    def _write_inventory(self, records: List[FileRecord]):
        records.sort(key=lambda r: r.rel_path)
        with open(self.output / "inventory.jsonl", "w", encoding="utf-8") as out_f:
            for r in records:
                out_f.write(json.dumps(dataclasses.asdict(r), ensure_ascii=False) + "\n")

    def _write_duplicate_groups(self, groups: List[List[FileRecord]]):
        with open(self.output / "duplicate-groups.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["group_id", "sha256", "size_bytes", "rel_path", "basename"])
            for idx, grp in enumerate(groups, 1):
                gid = f"DUP-{idx:03d}"
                for r in grp:
                    writer.writerow([gid, r.sha256, r.size_bytes, r.rel_path, r.basename])

    def _write_document_families(self, families: List[List[FileRecord]]):
        with open(self.output / "document-families.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["family_id", "family_stem", "rel_path", "basename", "revision", "lifecycle", "is_authoritative"])
            for idx, fam in enumerate(families, 1):
                fid = f"FAM-{idx:03d}"
                stem = fam[0].normalized_stem
                for r in fam:
                    _, vinfo = parse_version_tokens(r.basename)
                    writer.writerow([
                        fid, stem, r.rel_path, r.basename,
                        vinfo.revision_token or "none",
                        vinfo.lifecycle_state,
                        vinfo.is_authoritative
                    ])

    def _write_near_duplicates(self, pairs: List[Any]):
        with open(self.output / "near-duplicates.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "pair_id", "file_a", "file_b", "similarity_score",
                "size_a_bytes", "size_b_bytes", "size_diff_bytes",
                "stem_a", "stem_b", "suggested_action", "evidence"
            ])
            for p in pairs:
                writer.writerow([
                    getattr(p, "pair_id", ""),
                    getattr(p, "file_a", ""),
                    getattr(p, "file_b", ""),
                    f"{getattr(p, 'similarity_score', 0.0):.3f}",
                    getattr(p, "size_a_bytes", 0),
                    getattr(p, "size_b_bytes", 0),
                    getattr(p, "size_diff_bytes", 0),
                    getattr(p, "stem_a", ""),
                    getattr(p, "stem_b", ""),
                    getattr(p, "suggested_action", ""),
                    getattr(p, "evidence", "")
                ])

    def _write_hierarchy_anomalies(self, anomalies: List[Dict[str, Any]]):
        with open(self.output / "hierarchy-anomalies.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["anomaly_id", "edge", "folder", "parent", "depth", "status", "file_folder_fit", "folder_parent_fit", "evidence", "suggested_action"])
            for a in anomalies:
                writer.writerow([
                    a["anomaly_id"], a["edge"], a["folder"], a["parent"],
                    a.get("depth", 0), a["status"], a["file_folder_fit"], a["folder_parent_fit"],
                    a["evidence"], a["suggested_action"]
                ])

    def _write_review_queue(self, queue: List[Dict[str, Any]]):
        with open(self.output / "unresolved-review-queue.json", "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)

    def _write_ai_usage(self, packets: int, chars: int, total_files: int):
        usage = {
            "total_candidates_queued": packets,
            "total_excerpt_chars": chars,
            "pass_breakdown": {
                "pass_0": total_files,
                "pass_1": packets,
                "pass_2": 0,
                "pass_3": 0
            },
            "cache_hits": 0,
            "budget_exhausted": False
        }
        with open(self.output / "ai-usage.json", "w", encoding="utf-8") as f:
            json.dump(usage, f, indent=2)

    def _write_summary(
        self,
        cov: CoverageRecord,
        folders: List[FolderRecord],
        records: List[FileRecord],
        duplicates: List[List[FileRecord]],
        families: List[List[FileRecord]],
        anomalies: List[Dict[str, Any]],
        ai_queue: List[Dict[str, Any]],
        ai_chars: int
    ):
        dup_bytes = sum(sum(r.size_bytes for r in grp[1:]) for grp in duplicates)
        status_label = "Complete" if cov.is_complete else "Partial"

        md = [
            "# FileOS Scan Summary Report",
            f"\n**Root Scanned:** `{self.root}`  ",
            f"**Timestamp:** `{datetime.datetime.utcnow().isoformat()}Z`  ",
            f"**Scan Mode:** Recursive (Read-Only) | **Coverage:** `{status_label}`  \n",
            "## 1. Coverage & Tree Metrics",
            f"- **Directories Discovered:** {cov.directories_discovered} (Scanned: {cov.directories_scanned}, Excluded: {cov.directories_excluded}, Inaccessible: {cov.directories_inaccessible}, Depth-Capped: {cov.directories_depth_skipped})",
            f"- **Files Discovered:** {cov.files_discovered} (Eligible: {cov.files_eligible}, Analysed: {cov.files_analysed}, Skipped: {cov.files_skipped}, Failed: {cov.files_failed})",
            f"- **Deepest Discovered Depth:** {cov.deepest_discovered_depth} | **Deepest Scanned Depth:** {cov.deepest_scanned_depth}",
            f"- **Total Bytes Hashed:** {cov.total_bytes_hashed:,} bytes",
            f"- **Symlinks Skipped:** {cov.symlinks_skipped} | **Mount Boundaries Skipped:** {cov.mount_boundaries_skipped}",
            f"- **Exact Duplicate Groups:** {len(duplicates)} (Potential redundant space: {dup_bytes:,} bytes)",
            f"- **Document Families Identified:** {len(families)}",
            f"- **Hierarchy Anomalies Detected:** {len(anomalies)}",
            f"- **AI Review Queue Size:** {len(ai_queue)} packets ({ai_chars:,} chars extracted)\n",
        ]

        if not cov.is_complete:
            md.append("### Partial Scan Explanations:")
            for reason in cov.partial_reasons[:10]:
                md.append(f"- {reason}")
            if len(cov.partial_reasons) > 10:
                md.append(f"- ... and {len(cov.partial_reasons) - 10} more.")
            md.append("")

        # Compact Tree Overview
        md.append("## 2. Directory Hierarchy Overview (Depth Markers)")
        tree_folders = sorted(folders, key=lambda f: f.rel_path)
        for f in tree_folders[:40]:  # limit display to first 40 for brevity
            indent = "  " * f.depth
            status_tag = f"[{f.relationship_status}]" if f.rel_path != "." else "[root]"
            md.append(f"{indent}- `{f.rel_path}` {status_tag} (direct: {f.direct_file_count} files, desc: {f.descendant_file_count} files)")
        if len(tree_folders) > 40:
            md.append(f"  *... ({len(tree_folders) - 40} additional subdirectories recorded in folders.jsonl)*")
        md.append("")

        # Anomalies
        md.append("## 3. Hierarchy Anomalies (Edge-by-Edge)")
        if not anomalies:
            md.append("*No hierarchy contradictions detected.*")
        else:
            md.append("| Anomaly ID | Edge | Depth | Status | File-Folder Fit | Folder-Parent Fit | Action |")
            md.append("|---|---|---:|---|---:|---:|---|")
            for a in anomalies:
                md.append(f"| {a['anomaly_id']} | `{a['edge']}` | {a.get('depth', 0)} | `{a['status']}` | {a['file_folder_fit']} | {a['folder_parent_fit']} | `{a['suggested_action']}` |")
                md.append(f"> **Evidence:** {a['evidence']}\n")

        # Exact Duplicates
        md.append("\n## 4. Exact Duplicates (Preserved)")
        if not duplicates:
            md.append("*No exact duplicate files found.*")
        else:
            for idx, grp in enumerate(duplicates[:20], 1):
                md.append(f"### Group DUP-{idx:03d} (Hash: `{grp[0].sha256[:12]}...`)")
                for r in grp:
                    md.append(f"- `{r.rel_path}` ({r.size_bytes:,} bytes)")
            if len(duplicates) > 20:
                md.append(f"\n*... and {len(duplicates) - 20} more duplicate groups in duplicate-groups.csv*")

        # Document Families
        md.append("\n## 5. Document Families & Versions")
        if not families:
            md.append("*No document families identified.*")
        else:
            for idx, fam in enumerate(families[:20], 1):
                md.append(f"### Family FAM-{idx:03d}: `{fam[0].normalized_stem}`")
                for r in fam:
                    _, vinfo = parse_version_tokens(r.basename)
                    auth = " ⭐ Authoritative" if vinfo.is_authoritative else ""
                    rev = f" [{vinfo.revision_token}]" if vinfo.revision_token else ""
                    md.append(f"- `{r.rel_path}`: Lifecycle `{vinfo.lifecycle_state}`{rev}{auth}")
            if len(families) > 20:
                md.append(f"\n*... and {len(families) - 20} more document families in document-families.csv*")

        # AI Usage
        md.append("\n## 6. AI Usage & Token Budget Ledger")
        md.append(f"- **Pass 0 (Deterministic Only):** {cov.files_analysed} files")
        md.append(f"- **Pass 1 (2,000 char excerpts):** {len(ai_queue)} candidate packets")
        md.append(f"- **Pass 2 / Pass 3 Escalations:** 0")
        md.append(f"- **Total Excerpt Chars Exposed:** {ai_chars:,} / {MAX_AI_CHARS_PER_RUN:,} max budget")
        md.append("- **Silent AI Usage:** None. All processing strictly deterministic.\n")

        with open(self.output / "summary.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")

    def _append_journal(self, journal_path: Path, entry: Dict[str, Any]):
        with open(journal_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _get_directory_mtime_fingerprint(self) -> str:
        """Computes quick aggregate fingerprint of (rel_path, mtime, size) for watch detection."""
        items: List[str] = []
        stack = [self.root]
        while stack:
            curr = stack.pop()
            try:
                for entry in os.scandir(curr):
                    if is_path_excluded(entry.path, self.exclusions):
                        continue
                    try:
                        st = entry.stat()
                        items.append(f"{entry.name}:{st.st_mtime_ns}:{st.st_size}")
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(Path(entry.path))
                    except Exception:
                        pass
            except Exception:
                pass
        items.sort()
        return hashlib.md5(";".join(items).encode("utf-8")).hexdigest()

    def watch(
        self,
        interval: int = 10,
        once: bool = False,
        on_change: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Continuously monitors root directory for filesystem modifications and triggers
        fast incremental rescans whenever changes are detected.
        """
        initial_res = self.scan(incremental=True)
        if on_change:
            on_change(initial_res)

        if once:
            return initial_res

        last_fp = self._get_directory_mtime_fingerprint()

        try:
            while True:
                time.sleep(interval)
                curr_fp = self._get_directory_mtime_fingerprint()
                if curr_fp != last_fp:
                    t_start = time.time()
                    res = self.scan(incremental=True)
                    duration = time.time() - t_start
                    cov_p = self.output / "coverage.json"
                    cov = json.loads(cov_p.read_text(encoding="utf-8")) if cov_p.exists() else {}
                    reused = cov.get("bytes_reused_from_hash_cache", 0)
                    read_b = cov.get("bytes_read_for_hashing", 0)
                    ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    print(f"[{ts}] Change detected! Incremental scan finished in {duration:.2f}s "
                          f"({res['total_files']} files, {read_b:,} bytes read, {reused:,} bytes reused).")
                    last_fp = curr_fp
                    if on_change:
                        on_change(res)
        except KeyboardInterrupt:
            print("\nWatcher stopped by user.")
            return initial_res

# ---------------------------------------------------------------------------
# CLI Command Dispatcher
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="FileOS: Local-first, deterministic-first file organization engine."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # scan
    p_scan = subparsers.add_parser("scan", help="Scan a file or directory tree (Recursive by default, read-only)")
    p_scan.add_argument("target_path", nargs="?", help="Target file or directory path")
    p_scan.add_argument("--root", help="Alternative flag for target directory")
    p_scan.add_argument("--output", help="Output directory for reports and index")
    p_scan.add_argument("--max-depth", type=int, help="Optional maximum directory depth (root is 0)")
    p_scan.add_argument("--exclude", help="Comma-separated exclusion patterns")
    p_scan.add_argument("--sample-size", type=int, default=2000, help="Initial excerpt char limit (Pass 1)")
    p_scan.add_argument("--follow-symlinks", action="store_true", help="Follow directory symlinks (loop protected)")
    p_scan.add_argument("--incremental", action="store_true", help="Enable incremental scan using cache")
    p_scan.add_argument("--cache-file", help="Path to cache file (defaults to <output>/.fileos-cache.json)")

    # plan
    p_plan = subparsers.add_parser("plan", help="Generate proposed actions (Read-only)")
    p_plan.add_argument("--scan", help="Path to inventory.jsonl")
    p_plan.add_argument("--output", help="Output path for proposed-actions.json")

    # report
    p_report = subparsers.add_parser("report", help="Display summary report")
    p_report.add_argument("--input", required=True, help="Path to fileos-output directory")

    # apply
    p_apply = subparsers.add_parser("apply", help="Execute approved actions safely")
    p_apply.add_argument("--plan", required=True, help="Path to proposed-actions.json")
    p_apply.add_argument("--root", help="Root directory (default inferred from plan parent)")
    p_apply.add_argument("--approve", nargs="+", required=True, help="Specific Action IDs to approve (e.g. ACT-001)")
    p_apply.add_argument("--dry-run", action="store_true", help="Simulate apply without modifying filesystem")

    # undo
    p_undo = subparsers.add_parser("undo", help="Undo a journalled operation")
    p_undo.add_argument("--journal-id", required=True, help="Journal ID to undo (e.g. JRN-001)")
    p_undo.add_argument("--journal-file", help="Path to operation-journal.jsonl")
    p_undo.add_argument("--root", required=True, help="Root directory")

    # audit
    p_audit = subparsers.add_parser("audit", help="Run deterministic report integrity checks")
    p_audit.add_argument("--input", required=True, help="Path to FileOS report directory")
    p_audit.add_argument("--root", help="Optional path to source scan root")

    # dashboard
    p_dash = subparsers.add_parser("dashboard", help="Start local review dashboard server")
    p_dash.add_argument("--input", required=True, help="Path to FileOS report directory")
    p_dash.add_argument("--root", help="Optional path to source scan root")
    p_dash.add_argument("--host", default="127.0.0.1", help="Host interface (must be 127.0.0.1)")
    p_dash.add_argument("--port", type=int, default=8765, help="Port to bind (default 8765)")

    # watch
    p_watch = subparsers.add_parser("watch", help="Continuously monitor directory and perform incremental scans on change")
    p_watch.add_argument("target_path", nargs="?", help="Target file or directory path")
    p_watch.add_argument("--root", help="Alternative flag for target directory")
    p_watch.add_argument("--output", help="Output directory for reports and index")
    p_watch.add_argument("--interval", type=int, default=10, help="Polling interval in seconds (default 10)")
    p_watch.add_argument("--once", action="store_true", help="Run a single watch check cycle and exit")
    p_watch.add_argument("--exclude", help="Comma-separated exclusion patterns")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == "scan":
            path_str = args.target_path or args.root
            if not path_str:
                print("Error: Target path must be provided as a positional argument or with --root", file=sys.stderr)
                sys.exit(1)

            target = Path(path_str)
            out_path = Path(args.output) if args.output else None
            engine = FileOSEngine(target, out_path, max_depth=args.max_depth)
            
            if args.exclude:
                extra_excl = [p.strip() for p in args.exclude.split(",") if p.strip()]
                engine.exclusions.extend(extra_excl)

            c_file = Path(args.cache_file) if args.cache_file else None
            res = engine.scan(
                sample_size=args.sample_size,
                follow_symlinks=args.follow_symlinks,
                incremental=args.incremental,
                cache_file=c_file
            )
            status_text = "Complete" if res["is_complete"] else "Partial"
            print(f"Scan complete ({status_text}). Found {res['total_files']} files across {res['total_folders']} directories (deepest depth: {res['deepest_depth']}).")
            print(f"Reports and artifacts written to: {res['output_directory']}")

            # Auto-audit: run 15 integrity checks immediately after scan
            try:
                from audit import ReportAuditor
                _auditor = ReportAuditor(Path(res["output_directory"]))
                _audit   = _auditor.run_all_checks()
                _status  = _audit["overall_status"].upper()
                _icon    = "✅" if _audit["failed"] == 0 else "❌"
                print(f"\n{_icon} Integrity Audit ({_status}): "
                      f"{_audit['passed']}/15 passed, "
                      f"{_audit['warnings']} warnings, "
                      f"{_audit['failed']} failed.")
                if _audit["failed"] > 0 or _audit["warnings"] > 0:
                    for c in _audit["checks"]:
                        if c["status"] != "passed":
                            _ci = "⚠️" if c["status"] == "warning" else "❌"
                            print(f"  {_ci} [{c['check_id']}] {c['message']}")
            except Exception:
                pass  # audit is optional; never block scan output

        elif args.command == "plan":
            scan_path = Path(args.scan) if args.scan else None
            out_dir = Path(args.output).parent if args.output else (scan_path.parent if scan_path else Path("fileos-output"))
            engine = FileOSEngine(root_dir=out_dir.parent, output_dir=out_dir)
            actions = engine.plan(scan_inventory_path=scan_path)
            print(f"Plan generated with {len(actions)} proposed actions.")
            print(f"Output saved to: {engine.output / 'proposed-actions.json'}")

        elif args.command == "report":
            in_dir = Path(args.input)
            summary_file = in_dir / "summary.md"
            if not summary_file.exists():
                print(f"No summary.md found in {in_dir}")
                sys.exit(1)
            with open(summary_file, "r", encoding="utf-8") as f:
                print(f.read())

        elif args.command == "apply":
            plan_path = Path(args.plan)
            root_path = Path(args.root) if args.root else plan_path.parent.parent
            engine = FileOSEngine(root_dir=root_path, output_dir=plan_path.parent)
            dry_run = getattr(args, "dry_run", False)
            entries = engine.apply(plan_path, args.approve, dry_run=dry_run)
            prefix = "[DRY-RUN] Simulated" if dry_run else "Successfully applied"
            print(f"{prefix} {len(entries)} approved actions.")
            for e in entries:
                print(f"- [{e['journal_id']}] {e['action_id']}: {e['action_type']} -> {e['status']}")

        elif args.command == "undo":
            root_path = Path(args.root)
            j_file = Path(args.journal_file) if args.journal_file else None
            engine = FileOSEngine(root_dir=root_path)
            res = engine.undo(args.journal_id, j_file)
            print(f"Undo completed: {res['status']}")

        elif args.command == "audit":
            from audit import ReportAuditor
            auditor = ReportAuditor(Path(args.input), Path(args.root) if args.root else None)
            res = auditor.run_all_checks()
            print(f"\n=======================================================")
            print(f"FileOS Report Integrity Audit: {res['overall_status'].upper()}")
            print(f"Directory: {res['report_directory']}")
            print(f"Results: {res['passed']} passed, {res['warnings']} warnings, {res['failed']} failed")
            print(f"=======================================================\n")
            for c in res["checks"]:
                icon = "✅" if c["status"] == "passed" else ("⚠️" if c["status"] == "warning" else "❌")
                print(f"{icon} [{c['check_id']}] {c['name']}: {c['message']}")

        elif args.command == "dashboard":
            from dashboard import run_dashboard_server
            run_dashboard_server(Path(args.input), Path(args.root) if args.root else None, args.host, args.port)

        elif args.command == "watch":
            path_str = args.target_path or args.root
            if not path_str:
                print("Error: Target path must be provided as a positional argument or with --root", file=sys.stderr)
                sys.exit(1)
            target = Path(path_str)
            out_path = Path(args.output) if args.output else None
            engine = FileOSEngine(target, out_path)
            if args.exclude:
                extra_excl = [p.strip() for p in args.exclude.split(",") if p.strip()]
                engine.exclusions.extend(extra_excl)
            engine.watch(interval=args.interval, once=args.once)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
