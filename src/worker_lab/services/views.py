from ..models.workers import Worker


def public_worker(worker: Worker) -> dict[str, object]:
    return {"id": worker.id, "state": worker.state, "generation": worker.generation, "leases": sorted(worker.lease_ids)}
