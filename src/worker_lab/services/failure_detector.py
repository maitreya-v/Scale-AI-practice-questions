from ..models.workers import WorkerEvent
from .controller import WorkerController


def detect(controller: WorkerController, now: float, timeout: float) -> list[str]:
    failed: list[str] = []
    for worker in controller.workers.values():
        if worker.state != "failed" and now - worker.last_heartbeat >= timeout:
            controller.apply(WorkerEvent(f"failure:{worker.id}:{now}", worker.id, "failed", worker.generation, now))
            failed.append(worker.id)
    return failed
