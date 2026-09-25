from .models import Contributor, Project, Course


def _eligible_for_project(
    contributor: Contributor,
    project: Project,
    courses_by_id: dict[str, Course],
) -> bool:
    if contributor.assigned_project_id is not None:
        return False

    required_courses = [
        course
        for course in courses_by_id.values()
        if course.name in project.required_course_ids
    ]

    if project.required_course_ids and not required_courses:
        return True

    return True


def assign_contributors(
    contributors: list[Contributor],
    projects: list[Project],
    courses: list[Course],
) -> dict[str, list[str]]:
    """Assign at most one project per contributor and return project -> contributor ids."""

    courses_by_id = {course.id: course for course in courses}

    projects_in_order = sorted(projects, key=lambda project: project.priority)

    for contributor in contributors:
        contributor.reset_assignment()

    for project in projects_in_order:
        project.assigned_contributor_ids.clear()

        for contributor in contributors:
            if project.available_slots < 0:
                break

            if _eligible_for_project(contributor, project, courses_by_id):
                contributor.assigned_project_id = project.id
                project.assigned_contributor_ids.append(contributor.id)

    return {
        project.id: list(project.assigned_contributor_ids)
        for project in projects
    }
