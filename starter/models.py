from dataclasses import dataclass
from enum import Enum


class WorkerState(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    FAILED = "FAILED"
    DRAINING = "DRAINING"


@dataclass
class Task:
    task_id: str
    priority: int
    created_at: float
    deadline: float | None = None
    attempts: int = 0


@dataclass
class Worker:
    worker_id: str
    state: WorkerState = WorkerState.IDLE
    current_task_id: str | None = None
