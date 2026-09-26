from ..models.scheduling import Worker
from ..policies.workers import stale


def mark_stale_workers(workers: list[Worker], now: float, timeout: float) -> list[str]:
    failed = []
    for worker in workers:
        if stale(worker, now, timeout):
            worker.state = "failed"
            failed.append(worker.id)
    return failed
