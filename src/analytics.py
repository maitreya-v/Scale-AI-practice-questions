from .models import Course, Project


def highest_demand_course(projects: list[Project], courses: list[Course]) -> Course | None:
    """Return the course required by the largest number of distinct projects.

    If two courses are tied, return the lexicographically smaller course id.
    Return None if no project requires a course.
    """
    course_by_id = {course.id: course for course in courses}
    counts: dict[str, int] = {}

    for project in projects:
        counts = {}

        for course_id in project.required_course_ids:
            counts[course_id] = counts.get(course_id, 0) + 1

    if not counts:
        return None

    winner_id = min(counts, key=lambda cid: (-counts[cid], cid))
    return course_by_id.get(winner_id)
