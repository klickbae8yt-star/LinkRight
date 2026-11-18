#!/usr/bin/env python3
"""
FileOS Oracle VM AI Pool Connector.
Dispatches ambiguous adjudication packets from unresolved-review-queue.json
to the Oracle VM's free_llm_pool or Ollama service using Python standard library (urllib).
"""

import json
import os
from pathlib import Path
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

DEFAULT_POOL_ENDPOINT = os.environ.get("FILEOS_ORACLE_POOL_URL", "http://localhost:8765/v1/chat/completions")
DEFAULT_OLLAMA_ENDPOINT = os.environ.get("FILEOS_OLLAMA_URL", "http://localhost:11434/api/generate")
DEFAULT_MODEL = os.environ.get("FILEOS_ORACLE_MODEL", "llama3.2")

class OracleAIPoolClient:
    def __init__(
        self,
        endpoint: str = DEFAULT_POOL_ENDPOINT,
        model: str = DEFAULT_MODEL,
        timeout: int = 30,
        mock_mode: bool = False
    ):
        self.endpoint = endpoint
        self.model = model
        self.timeout = timeout
        self.mock_mode = mock_mode

    def adjudicate_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submits a single bounded review packet to the model.
        Returns a structured decision: {"action": "...", "reason": "...", "confidence": 0.xx}
        """
        if self.mock_mode:
            return {
                "candidate_id": packet.get("candidate_id"),
                "choice": "correct",
                "action": packet.get("allowed_actions", ["keep_as_is"])[0],
                "confidence": 0.95,
                "reason": "Mock adjudication decision based on heuristic evidence fit.",
                "source": "oracle_pool_mock"
            }

        prompt = (
            "You are FileOS Adjudicator running on Oracle Always-Free VM.\n"
            "Analyze this file hierarchy anomaly and suggest the correct deterministic action.\n\n"
            f"Candidate ID: {packet.get('candidate_id')}\n"
            f"File: {packet.get('rel_path')}\n"
            f"Folder: {packet.get('folder')}\n"
            f"Parent Project: {packet.get('parent_project')}\n"
            f"Signals: {json.dumps(packet.get('signals', {}))}\n"
            f"Excerpt (bounded):\n{packet.get('excerpt', '')}\n\n"
            f"Allowed Actions: {json.dumps(packet.get('allowed_actions', []))}\n\n"
            "Return strictly a JSON object with keys: 'action', 'confidence' (float 0.0-1.0), and 'reason'."
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a precise JSON-only file taxonomy reviewer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }

        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=req_data,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                resp_body = resp.read().decode("utf-8")
                parsed = json.loads(resp_body)
                content = parsed.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                decision_obj = json.loads(content)
                return {
                    "candidate_id": packet.get("candidate_id"),
                    "choice": "correct" if decision_obj.get("confidence", 0) >= 0.7 else "uncertain",
                    "action": decision_obj.get("action", "review"),
                    "confidence": float(decision_obj.get("confidence", 0.5)),
                    "reason": decision_obj.get("reason", "Oracle AI pool adjudication"),
                    "source": f"oracle_pool:{self.model}"
                }
        except Exception as e:
            return {
                "candidate_id": packet.get("candidate_id"),
                "choice": "uncertain",
                "action": "keep_as_is",
                "confidence": 0.0,
                "error": str(e),
                "source": "oracle_pool_error"
            }

    def process_queue(self, queue_file: Path, decisions_file: Path) -> List[Dict[str, Any]]:
        """Reads review queue, adjudicates packets, and appends to review-decisions.jsonl."""
        if not queue_file.exists():
            return []

        queue: List[Dict[str, Any]] = json.loads(queue_file.read_text(encoding="utf-8"))
        results = []

        with open(decisions_file, "a", encoding="utf-8") as out_f:
            for packet in queue:
                decision = self.adjudicate_packet(packet)
                out_f.write(json.dumps(decision) + "\n")
                results.append(decision)

        return results

