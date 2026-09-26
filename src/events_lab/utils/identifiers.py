from __future__ import annotations

import hashlib


def stable_id(*parts: object) -> str:
    payload = "|".join(str(part).strip() for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def require_identifier(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError("identifier cannot be empty")
    return normalized
