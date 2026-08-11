from __future__ import annotations
import json
import os
from pathlib import Path
from threading import Lock
from typing import Any

class AuditLogger:
    # Stores assessment metadata, not raw patient input.
    def __init__(self, path: str | None = None) -> None:
        default = os.getenv("AUDIT_LOG_PATH", "data/audit/triage_audit.jsonl")
        self.path = Path(path or default)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def write(self, record: dict[str, Any]) -> None:
        with self._lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, default=str, separators=(",", ":")) + "\n")

audit_logger = AuditLogger()
