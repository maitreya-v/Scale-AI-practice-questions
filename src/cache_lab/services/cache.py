from copy import copy
from ..models.entries import CacheEntry


class ResponseCache:
    def __init__(self, now):
        self.now = now
        self.entries: dict[str, CacheEntry] = {}

    def put(self, key: str, value: object, ttl_ms: int) -> None:
        self.entries[key] = CacheEntry(copy(value), self.now() + ttl_ms)

    def get(self, key: str):
        entry = self.entries.get(key)
        if not entry or entry.expires_at <= self.now():
            self.entries.pop(key, None)
            return None
        return copy(entry.value) if entry.value else None
