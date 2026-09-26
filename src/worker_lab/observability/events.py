from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field


@dataclass
class EventSink:
    events: list[tuple[str, dict[str, object]]] = field(default_factory=list)

    def emit(self, name: str, **fields: object) -> None:
        self.events.append((name, dict(fields)))

    def names(self) -> Iterable[str]:
        return (name for name, _ in self.events)
