from ..models.scheduling import Task


def expired(task: Task, now: float) -> bool:
    return task.deadline is not None and task.deadline < now
