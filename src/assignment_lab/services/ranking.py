from ..models.domain import Project


def rank_projects(projects: list[Project]) -> list[Project]:
    return sorted(projects, key=lambda project: (project.priority, project.id))
