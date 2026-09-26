from ..models.scheduling import Worker


def available(worker: Worker) -> bool:
    return worker.state == "active" and len(worker.active_task_ids) <= worker.capacity


def stale(worker: Worker, now: float, timeout: float) -> bool:
    return now - worker.last_heartbeat > timeout
