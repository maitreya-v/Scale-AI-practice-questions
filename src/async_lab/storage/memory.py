from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass
class MemoryTable(Generic[T]):
    rows: dict[str, T] = field(default_factory=dict)

    def get(self, key: str) -> Optional[T]:
        value = self.rows.get(key)
        return deepcopy(value) if value is not None else None

    def put(self, key: str, value: T) -> None:
        self.rows[key] = deepcopy(value)

    def delete(self, key: str) -> bool:
        return self.rows.pop(key, None) is not None

    def all(self) -> list[T]:
        return [deepcopy(value) for value in self.rows.values()]
