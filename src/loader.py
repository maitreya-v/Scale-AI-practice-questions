import csv
from pathlib import Path
from .models import Contributor, Course, Project


def load_courses(path: str | Path) -> list[Course]:
    with open(path, newline="", encoding="utf-8") as f:
        return [Course(id=row["course_id"], name=row["name"]) for row in csv.DictReader(f)]


def load_contributors(path: str | Path) -> list[Contributor]:
    contributors: list[Contributor] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            completed = {x.strip() for x in row["completed_course_ids"].split(";") if x.strip()}
            contributors.append(
                Contributor(
                    id=row["contributor_id"],
                    name=row["name"],
                    completed_course_ids=completed,
                )
            )
    return contributors


def load_projects(path: str | Path) -> list[Project]:
    projects: list[Project] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            required = {x.strip() for x in row["required_course_ids"].split(";") if x.strip()}
            projects.append(
                Project(
                    id=row["project_id"],
                    name=row["name"],
                    priority=int(row["priority"]),
                    capacity=int(row["capacity"]),
                    required_course_ids=list(required),
                )
            )
    return projects
