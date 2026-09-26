from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Job:
    id: str
    payload: str


@dataclass
class JobResult:
    job_id: str
    value: Optional[str] = None
    error: Optional[str] = None
