"""
Append-only event store with audit trail.
Read-only by default for consumers. No external publish in R01.
"""

from __future__ import annotations

from collections import deque
from typing import Callable, Optional

from sealie_twin.models.events import TwinEvent


class EventStore:
    def __init__(self, max_events: int = 10_000) -> None:
        self._events: deque[TwinEvent] = deque(maxlen=max_events)
        self._subscribers: list[Callable[[TwinEvent], None]] = []

    def append(self, event: TwinEvent) -> TwinEvent:
        # Fail-closed: validation already done by Pydantic model
        self._events.append(event)
        for sub in list(self._subscribers):
            try:
                sub(event)
            except Exception:
                # Subscriber failures must not break the store
                pass
        return event

    def list(
        self,
        *,
        kind: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 100,
    ) -> list[TwinEvent]:
        items = list(self._events)
        if kind:
            items = [e for e in items if e.kind.value == kind]
        if source:
            items = [e for e in items if e.source == source]
        return items[-limit:]

    def subscribe(self, callback: Callable[[TwinEvent], None]) -> None:
        self._subscribers.append(callback)

    def audit_trail(self, limit: int = 200) -> list[dict]:
        return [e.to_audit_dict() for e in list(self._events)[-limit:]]
