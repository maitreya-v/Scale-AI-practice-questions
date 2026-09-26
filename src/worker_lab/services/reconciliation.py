from .controller import WorkerController


def reconcile_leases(controller: WorkerController) -> list[str]:
    orphaned: list[str] = []
    for lease_id, worker_id in list(controller.leases.owners.items()):
        worker = controller.workers.get(worker_id)
        if worker is None or worker.state == "failed":
            orphaned.append(lease_id)
            controller.leases.owners.pop(lease_id, None)
    controller.requeue.extend(orphaned)
    return orphaned
