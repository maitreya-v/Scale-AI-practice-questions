from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MemoryLogger:
    records: list[tuple[str, str]] = field(default_factory=list)

    def info(self, message: str) -> None:
        self.records.append(("info", message))

    def warning(self, message: str) -> None:
        self.records.append(("warning", message))

    def error(self, message: str) -> None:
        self.records.append(("error", message))
