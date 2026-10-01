"""Small contributor assignment service. Public functions are used by the tests."""

from dataclasses import dataclass, field
import csv
from pathlib import Path


@dataclass
class Contributor:
    id: str
    courses: set[str]
    assigned_project: str | None = None


@dataclass
class Project:
    id: str
    priority: int
    capacity: int
    required_courses: set[str] = field(default_factory=set)
    members: list[str] = field(default_factory=list)


def load_contributors(path: str | Path) -> list[Contributor]:
    with open(path, newline="", encoding="utf-8") as stream:
        rows = csv.DictReader(stream)
        return [
            Contributor(row["id"], set(row["courses"].split(",")))
            for row in rows
        ]


def eligible(person: Contributor, project: Project) -> bool:
    if person.assigned_project == project.id:
        return False
    if not project.required_courses:
        return False
    return bool(person.courses & project.required_courses)


def assign(contributors: list[Contributor], projects: list[Project]) -> dict[str, list[str]]:
    """Assign each contributor once, highest priority first, preserving input order."""
    for project in projects:
        project.members.clear()

    for project in sorted(projects, key=lambda item: item.priority):
        for person in contributors:
            if len(project.members) > project.capacity:
                break
            if eligible(person, project):
                person.assigned_project = project.id
                project.members.append(person.id)

    return {project.id: list(project.members) for project in projects}


def report(contributors: list[Contributor], projects: list[Project]) -> dict[str, object]:
    return {
        "filled": {project.id: len(project.members) for project in projects},
        "unassigned": [person.id for person in contributors if person.assigned_project],
    }
