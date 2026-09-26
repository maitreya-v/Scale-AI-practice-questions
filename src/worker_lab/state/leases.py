from dataclasses import dataclass
from typing import Optional


@dataclass
class LeaseRegistry:
    owners: dict[str, str]

    def assign(self, lease_id: str, worker_id: str) -> None:
        self.owners[lease_id] = worker_id

    def release_worker(self, worker_id: str) -> list[str]:
        released = [lease_id for lease_id, owner in self.owners.items() if owner == worker_id]
        for lease_id in released:
            self.owners.pop(lease_id, None)
        return released
