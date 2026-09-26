from ..models.domain import Contributor, Project


def satisfies_prerequisites(contributor: Contributor, project: Project) -> bool:
    completed = contributor.active_project_ids
    return project.required_course_ids.issubset(completed)
