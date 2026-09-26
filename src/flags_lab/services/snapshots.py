from dataclasses import dataclass
from typing import Optional
from ..models.flags import Flag


@dataclass
class Snapshot:
    flags: dict[str, Flag]
    fetched_at: float


class SnapshotCache:
    def __init__(self, ttl_seconds: float, now):
        self.ttl_seconds = ttl_seconds
        self.now = now
        self.snapshot: Optional[Snapshot] = None

    def get(self) -> Optional[Snapshot]:
        if self.snapshot and self.now() - self.snapshot.fetched_at < self.ttl_seconds:
            return self.snapshot
        return None

    def put(self, flags: dict[str, Flag]) -> Snapshot:
        self.snapshot = Snapshot(flags, self.now())
        return self.snapshot
