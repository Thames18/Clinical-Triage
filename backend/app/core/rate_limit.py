from __future__ import annotations
from collections import defaultdict, deque
from time import monotonic
from threading import Lock

class InMemoryRateLimiter:
    # Development/EC2 guardrail; use Redis for multi-instance production.
    def __init__(self, limit: int = 60, window_seconds: int = 60) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, key: str) -> bool:
        now = monotonic()
        cutoff = now - self.window_seconds
        with self._lock:
            events = self._events[key]
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= self.limit:
                return False
            events.append(now)
            return True

rate_limiter = InMemoryRateLimiter()
