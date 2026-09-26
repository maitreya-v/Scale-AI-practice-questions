from dataclasses import dataclass, field


@dataclass
class Worker:
    id: str
    state: str = "idle"
    generation: int = 0
    lease_ids: set[str] = field(default_factory=set)
    last_heartbeat: float = 0.0


@dataclass(frozen=True)
class WorkerEvent:
    id: str
    worker_id: str
    kind: str
    generation: int
    at: float
