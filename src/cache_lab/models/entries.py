from dataclasses import dataclass
from typing import Optional


@dataclass
class CacheEntry:
    value: object
    expires_at: float


@dataclass
class IdempotencyRecord:
    request_hash: str
    response: Optional[object] = None
    state: str = "started"
