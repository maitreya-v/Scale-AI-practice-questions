"""In-memory task scheduler with deterministic time supplied by callers."""

from dataclasses import dataclass


@dataclass
class Task:
    id: str
    priority: int
    deadline: int
    max_attempts: int = 2
    attempts: int = 0


class Scheduler:
    def __init__(self):
        self.pending: list[tuple[int, Task]] = []
        self.running: dict[str, Task] = {}
        self.workers: dict[str, str] = {}
        self.sequence = 0

    def register(self, worker_id: str) -> None:
        self.workers[worker_id] = "idle"

    def submit(self, task: Task) -> None:
        if any(running.id == task.id for running in self.running.values()):
            return
        self.sequence += 1
        self.pending.append((self.sequence, task))

    def dispatch(self, worker_id: str, now: int) -> Task | None:
        if worker_id not in self.workers:
            raise KeyError(worker_id)
        if self.workers[worker_id] == "failed":
            return None
        self.pending.sort(key=lambda entry: (entry[1].priority, -entry[0]))
        while self.pending:
            _, task = self.pending.pop(0)
            if now > task.deadline:
                continue
            task.attempts += 1
            self.workers[worker_id] = "busy"
            self.running[worker_id] = task
            return task
        return None

    def complete(self, worker_id: str) -> str:
        task = self.running.pop(worker_id)
        return task.id

    def fail(self, worker_id: str) -> None:
        task = self.running.pop(worker_id)
        self.workers[worker_id] = "idle"
        if task.attempts <= task.max_attempts:
            task.priority = 0
            self.sequence += 1
            self.pending.append((self.sequence, task))
