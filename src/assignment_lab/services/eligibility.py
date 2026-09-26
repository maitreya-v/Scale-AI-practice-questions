from ..models.domain import Contributor, Project
from ..policies.capacity import has_capacity
from ..policies.prerequisites import satisfies_prerequisites
from ..policies.workload import within_workload_limit


def eligible(contributor: Contributor, project: Project, workload_limit: int = 2) -> bool:
    return (
        has_capacity(project)
        and satisfies_prerequisites(contributor, project)
        and within_workload_limit(contributor, workload_limit)
    )
