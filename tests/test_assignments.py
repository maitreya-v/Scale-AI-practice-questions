from pathlib import Path

from src.analytics import highest_demand_course
from src.assignment import assign_contributors
from src.loader import load_contributors, load_courses, load_projects
from src.models import Contributor, Course, Project

DATA = Path(__file__).resolve().parents[1] / "data"


def test_projects_without_course_requirements_respect_priority_and_capacity():
    courses = load_courses(DATA / "courses.csv")
    contributors = [
        Contributor(id="c1", name="Ada"),
        Contributor(id="c2", name="Grace"),
        Contributor(id="c3", name="Linus"),
    ]
    projects = [
        Project(id="p-low", name="Low", priority=1, capacity=1),
        Project(id="p-high", name="High", priority=10, capacity=1),
    ]

    assignments = assign_contributors(contributors, projects, courses)

    assert assignments["p-high"] == ["c1"]
    assert assignments["p-low"] == ["c2"]
    assert len(assignments["p-high"]) == 1
    assert len(assignments["p-low"]) == 1


def test_projects_with_course_requirements_only_receive_qualified_contributors():
    courses = [Course(id="python", name="Python"), Course(id="ml", name="Machine Learning")]
    contributors = [
        Contributor(id="c1", name="Ada", completed_course_ids={"python"}),
        Contributor(id="c2", name="Grace", completed_course_ids={"python", "ml"}),
    ]
    projects = [
        Project(
            id="p-ml",
            name="Model Evaluation",
            priority=10,
            capacity=1,
            required_course_ids=["ml"],
        )
    ]

    assignments = assign_contributors(contributors, projects, courses)

    assert assignments["p-ml"] == ["c2"]


def test_course_lookup_uses_course_id_not_course_name():
    courses = [Course(id="c-python", name="Python Foundations")]
    contributors = [
        Contributor(id="c1", name="Ada", completed_course_ids=set()),
        Contributor(id="c2", name="Grace", completed_course_ids={"c-python"}),
    ]
    projects = [
        Project(
            id="p1",
            name="Data Cleanup",
            priority=5,
            capacity=1,
            required_course_ids=["c-python"],
        )
    ]

    assignments = assign_contributors(contributors, projects, courses)
    assert assignments["p1"] == ["c2"]


def test_zero_capacity_project_gets_no_assignment():
    projects = [Project(id="p0", name="Closed", priority=100, capacity=0)]
    assignments = assign_contributors(
        [Contributor(id="c1", name="Ada")],
        projects,
        [],
    )
    assert assignments["p0"] == []


def test_highest_demand_course_counts_across_all_projects():
    courses = [
        Course(id="python", name="Python"),
        Course(id="sql", name="SQL"),
        Course(id="llm", name="LLM Systems"),
    ]
    projects = [
        Project("p1", "A", 3, 1, ["python", "sql"]),
        Project("p2", "B", 2, 1, ["python"]),
        Project("p3", "C", 1, 1, ["python", "llm"]),
    ]

    assert highest_demand_course(projects, courses) == courses[0]


def test_highest_demand_course_counts_each_project_once_per_course():
    courses = [Course(id="python", name="Python"), Course(id="sql", name="SQL")]
    projects = [
        Project("p1", "A", 2, 1, ["sql", "sql", "sql"]),
        Project("p2", "B", 1, 1, ["python"]),
        Project("p3", "C", 1, 1, ["python"]),
    ]

    assert highest_demand_course(projects, courses) == courses[0]
