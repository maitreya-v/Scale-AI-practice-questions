from collections import Counter
from typing import Optional
from ..models.domain import Project


def most_demanded_course(projects: list[Project]) -> Optional[str]:
    counts: Counter[str] = Counter()
    for project in projects:
        counts.update(project.assigned_contributor_ids)
    if not counts:
        return None
    return min(counts, key=lambda course_id: (-counts[course_id], course_id))
