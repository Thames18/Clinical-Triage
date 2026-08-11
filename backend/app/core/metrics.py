from __future__ import annotations
from collections import Counter
from threading import Lock

class Metrics:
    def __init__(self) -> None:
        self._lock = Lock()
        self.requests_total = 0
        self.errors_total = 0
        self.latencies_ms: list[float] = []
        self.triage_levels: Counter[str] = Counter()

    def observe_request(self, duration_ms: float, status_code: int) -> None:
        with self._lock:
            self.requests_total += 1
            self.latencies_ms.append(duration_ms)
            self.latencies_ms = self.latencies_ms[-1000:]
            if status_code >= 500:
                self.errors_total += 1

    def observe_triage(self, level: str) -> None:
        with self._lock:
            self.triage_levels[level] += 1

    def snapshot(self) -> dict:
        with self._lock:
            average = (
                sum(self.latencies_ms) / len(self.latencies_ms)
                if self.latencies_ms else 0.0
            )
            return {
                "requests_total": self.requests_total,
                "errors_total": self.errors_total,
                "average_latency_ms": round(average, 2),
                "triage_levels": dict(self.triage_levels),
            }

metrics = Metrics()
