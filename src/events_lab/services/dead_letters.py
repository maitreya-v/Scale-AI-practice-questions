from dataclasses import dataclass, field
from ..models.events import Event


@dataclass
class DeadLetters:
    rows: list[tuple[Event, str]] = field(default_factory=list)

    def add(self, event: Event, reason: str) -> None:
        self.rows.append((event, reason))
