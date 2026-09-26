from dataclasses import dataclass, field


@dataclass
class Checkpoints:
    completed_ids: set[str] = field(default_factory=set)

    def mark_complete(self, row_id: str) -> None:
        self.completed_ids.add(row_id)

    def pending(self, row_ids: list[str]) -> list[str]:
        return [row_id for row_id in row_ids if row_id not in self.completed_ids]
