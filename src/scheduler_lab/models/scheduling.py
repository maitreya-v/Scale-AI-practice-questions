from dataclasses import dataclass, field
from typing import Optional


@dataclass(order=True)
class Task:
    priority: int
    created_at: float
    id: str = field(compare=False)
    deadline: Optional[float] = field(default=None, compare=False)
    attempts: int = field(default=0, compare=False)


@dataclass
class Worker:
    id: str
    capacity: int
    active_task_ids: set[str] = field(default_factory=set)
    last_heartbeat: float = 0.0
    state: str = "active"


@dataclass
class Lease:
    task_id: str
    worker_id: str
    expires_at: float
