from ..models.workers import Worker, WorkerEvent
from ..state.leases import LeaseRegistry
from ..state.transitions import transition


class WorkerController:
    def __init__(self):
        self.workers: dict[str, Worker] = {}
        self.processed_event_ids: set[str] = set()
        self.leases = LeaseRegistry({})
        self.requeue: list[str] = []

    def register(self, worker: Worker) -> None:
        self.workers[worker.id] = worker

    def apply(self, event: WorkerEvent) -> None:
        worker = self.workers[event.worker_id]
        if event.id in self.processed_event_ids:
            return
        self.processed_event_ids.add(event.id)
        if event.generation < worker.generation:
            return
        worker.generation = event.generation
        if event.kind == "heartbeat":
            worker.last_heartbeat = event.at
            worker.state = "idle" if not worker.lease_ids else "busy"
        elif event.kind == "drain":
            worker.state = transition(worker.state, "draining")
        elif event.kind == "failed":
            worker.state = transition(worker.state, "failed")
            worker.lease_ids.clear()
        elif event.kind == "recover":
            worker.state = transition(worker.state, "busy")

    def assign_lease(self, worker_id: str, lease_id: str) -> None:
        worker = self.workers[worker_id]
        worker.lease_ids.add(lease_id)
        worker.state = transition(worker.state, "busy")
        self.leases.assign(lease_id, worker_id)
