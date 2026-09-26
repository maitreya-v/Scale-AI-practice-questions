from ..models.domain import Contributor


def within_workload_limit(contributor: Contributor, limit: int) -> bool:
    return len(contributor.active_project_ids) < limit
