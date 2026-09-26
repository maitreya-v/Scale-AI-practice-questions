from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OperationLog:
    calls: list[tuple[str, str]] = field(default_factory=list)

    def append(self, tenant_id: str, operation: str) -> None:
        self.calls.append((tenant_id, operation))
