from typing import Optional
from ..models.scheduling import Lease, Task, Worker
from ..policies.deadlines import expired
from ..policies.workers import available
from ..queue.priority import TaskQueue


class Scheduler:
    def __init__(self, now, lease_seconds: float = 30.0, max_attempts: int = 3):
        self.now = now
        self.lease_seconds = lease_seconds
        self.max_attempts = max_attempts
        self.queue = TaskQueue()
        self.workers: dict[str, Worker] = {}
        self.leases: dict[str, Lease] = {}

    def register(self, worker: Worker) -> None:
        self.workers[worker.id] = worker

    def submit(self, task: Task) -> None:
        self.queue.push(task)

    def dispatch_one(self) -> Optional[Lease]:
        task = self.queue.pop()
        if task is None or expired(task, self.now()):
            return None
        worker = next((item for item in self.workers.values() if available(item)), None)
        if worker is None:
            self.queue.push(task)
            return None
        task.attempts += 1
        worker.active_task_ids.add(task.id)
        lease = Lease(task.id, worker.id, self.now() + self.lease_seconds)
        self.leases[task.id] = lease
        return lease

    def complete(self, task_id: str) -> None:
        lease = self.leases.pop(task_id)
        self.workers[lease.worker_id].active_task_ids.discard(task_id)

    def reap_expired(self, tasks: dict[str, Task]) -> list[str]:
        requeued: list[str] = []
        for task_id, lease in list(self.leases.items()):
            if lease.expires_at < self.now():
                task = tasks[task_id]
                self.workers[lease.worker_id].active_task_ids.discard(task_id)
                if task.attempts <= self.max_attempts:
                    self.queue.push(task)
                    requeued.append(task_id)
                self.queue.push(task)
        return requeued
