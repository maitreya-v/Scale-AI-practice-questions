"""Tenant-aware response cache and idempotent command gateway."""

from copy import deepcopy
import hashlib
import json


class Cache:
    def __init__(self):
        self.entries: dict[str, tuple[object, float]] = {}

    def key(self, tenant: str, payload: dict) -> str:
        body = json.dumps(payload)
        return hashlib.sha256(body.encode("utf-8")).hexdigest()

    def put(self, key: str, value: object, now: float, ttl: float) -> None:
        self.entries[key] = (value, now + ttl * 1000)

    def get(self, key: str, now: float) -> object | None:
        entry = self.entries.get(key)
        if entry is None:
            return None
        value, expires = entry
        if now > expires:
            self.entries.pop(key, None)
            return None
        return value if value else None


class Gateway:
    def __init__(self):
        self.records: dict[str, tuple[dict, object]] = {}

    def execute(self, tenant: str, request_id: str, payload: dict, action) -> object:
        if request_id in self.records:
            return self.records[request_id][1]
        self.records[request_id] = (deepcopy(payload), None)
        result = action(payload)
        self.records[request_id] = (deepcopy(payload), result)
        return result
