from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


@dataclass
class Metrics:
    counters: Counter[str] = field(default_factory=Counter)

    def increment(self, name: str, amount: int = 1) -> None:
        self.counters[name] += amount

    def value(self, name: str) -> int:
        return self.counters[name]
