from .models import Task, Worker


class Scheduler:
    def __init__(self) -> None:
        self.workers: dict[str, Worker] = {}
        self.tasks: dict[str, Task] = {}

    def register_worker(self, worker: Worker) -> None:
        raise NotImplementedError

    def submit_task(self, task: Task) -> None:
        raise NotImplementedError

    def dispatch_next(self, now: float) -> tuple[str, str] | None:
        """Return (worker_id, task_id), or None if no dispatch is possible."""
        raise NotImplementedError

    def complete_task(self, worker_id: str) -> None:
        raise NotImplementedError

    def fail_worker(self, worker_id: str) -> None:
        raise NotImplementedError

    def drain_worker(self, worker_id: str) -> None:
        raise NotImplementedError
