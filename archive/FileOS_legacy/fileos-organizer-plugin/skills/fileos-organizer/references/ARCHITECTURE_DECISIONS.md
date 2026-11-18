# FileOS Architecture Decisions Record (ADR)

## ADR-001: Product Direction & System Boundaries
- **Status:** ACCEPTED (2026-11-11)
- **Context:** FileOS requires a clear strategy balancing local user privacy, compute efficiency, and cloud capabilities.
- **Decisions:**
  1. **Primary File Operations:** Local-first on the user's filesystem. Source files are strictly immutable during scan, plan, report, audit, and dashboard review. Mutations occur exclusively via explicit, exact Action ID approvals (`fileos.py apply --approve ACT-xxx`).
  2. **Infrastructure & Remote Watcher (Option B):** FileOS supports running watch daemons / background scanning either on the local workstation or deployed as a remote worker on the user's Oracle Cloud Always-Free VM.
  3. **AI Execution Strategy (Oracle VM Free LLM Pool & Ollama):** For ambiguous review queue packets (Pass 1-3), rather than relying on commercial cloud APIs, FileOS integrates with the user's standing Oracle VM inference services (`ollama` for local CPU models/embeddings, and `free_llm_pool` on port 8765 for pooled free-tier models).
  4. **Historical Analytics & Persistence (Oracle MongoDB):** In addition to local portable JSONL/CSV report artifacts, FileOS supports an optional historical sync connector to record scan metrics, coverage runs, and review decision histories into the user's Oracle MongoDB instance.
  5. **M0/M1 Isolation Boundary:** M0 (Baseline Freeze) and M1 (Data Integrity) remain 100% self-contained with synthetic test fixtures and zero mandatory network calls. Connectors to Oracle (Ollama, free_llm_pool, MongoDB) are built as clean, decoupled adapters with dry-run/mock fallbacks.

## ADR-002: Deterministic-First & Shared AI Token Caps
- **Status:** ACCEPTED (2026-11-11)
- **Decisions:**
  - Standard SHA-256 hash deduplication and regex token-based version clustering are executed deterministically in standard Python without invoking any model.
  - Model intervention is reserved strictly for unresolved edge contradictions (`unresolved-review-queue.json`).
  - Strict run caps: Pass 0 (0 chars), Pass 1 (2,000 chars), Pass 2 (8,000 chars), Pass 3 (16,000 chars), max 10 packets and 20,000 characters total per scan.

## ADR-003: Non-Overlapping Inventory & Directory Accounting
- **Status:** ACCEPTED (2026-11-11)
- **Decisions:**
  - Files follow the invariant: $Files_{observed} = Files_{excluded} + Files_{eligible}$ where $Files_{eligible} = Files_{analysed} + Files_{skipped} + Files_{failed}$.
  - Directories follow: $Dirs_{observed} = Dirs_{scanned} + Dirs_{excluded} + Dirs_{inaccessible} + Dirs_{depth\_skipped}$.
  - Descendants of excluded or inaccessible subtrees are accounted as `unknown`, never fabricated as discovered or zero.

