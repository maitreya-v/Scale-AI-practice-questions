from ..models.domain import Contributor, Course, Project
from .catalog import Catalog


def load_catalog(payload: dict[str, list[dict[str, object]]]) -> Catalog:
    contributors = {
        str(row["id"]): Contributor(
            id=str(row["id"]),
            completed_course_ids=set(row.get("completed_course_ids", [])),
        )
        for row in payload["contributors"]
    }
    projects = {
        str(row["id"]): Project(
            id=str(row["id"]),
            priority=int(row["priority"]),
            capacity=int(row["capacity"]),
            required_course_ids=set(row.get("required_course_ids", [])),
        )
        for row in payload["projects"]
    }
    courses = {str(row["id"]): Course(str(row["id"]), str(row["title"])) for row in payload["courses"]}
    return Catalog(contributors, projects, courses)
