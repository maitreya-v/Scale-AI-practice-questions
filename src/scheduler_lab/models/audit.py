from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class AuditEvent:
    name: str
    entity_id: str
    at: datetime
    details: dict[str, Any] = field(default_factory=dict)
