from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class InputRecord:
    row_id: str
    text: str


@dataclass
class OutputRecord:
    row_id: str
    text: str
    category: Optional[str] = None
    errors: list[str] = field(default_factory=list)
