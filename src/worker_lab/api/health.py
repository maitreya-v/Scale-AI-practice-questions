from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Health:
    status: str
    version: str


def health_payload(version: str = "1") -> dict[str, str]:
    return asdict(Health(status="ok", version=version))
