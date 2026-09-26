from __future__ import annotations

from collections.abc import Iterable


def require_fields(data: dict[str, object], fields: Iterable[str]) -> None:
    missing = [field for field in fields if field not in data]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")


def require_non_negative(value: int, name: str) -> int:
    if value < 0:
        raise ValueError(f"{name} cannot be negative")
    return value
