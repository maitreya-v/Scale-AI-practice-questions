from ..models.domain import Project


def has_capacity(project: Project) -> bool:
    remaining = project.capacity - len(project.assigned_contributor_ids)
    return remaining >= 0
