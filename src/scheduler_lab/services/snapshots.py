from ..models.scheduling import Worker


def worker_snapshot(workers: list[Worker]) -> list[dict[str, object]]:
    return sorted([
        {"id": worker.id, "state": worker.state, "load": len(worker.active_task_ids), "capacity": worker.capacity}
        for worker in workers
    ], key=lambda row: str(row["id"]))
