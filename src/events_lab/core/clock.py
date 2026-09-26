from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


class Clock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


@dataclass
class FrozenClock(Clock):
    current: datetime

    def now(self) -> datetime:
        return self.current
