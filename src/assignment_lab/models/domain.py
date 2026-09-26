from dataclasses import dataclass, field


@dataclass
class Contributor:
    id: str
    completed_course_ids: set[str] = field(default_factory=set)
    active_project_ids: set[str] = field(default_factory=set)


@dataclass
class Course:
    id: str
    title: str


@dataclass
class Project:
    id: str
    priority: int
    capacity: int
    required_course_ids: set[str] = field(default_factory=set)
    assigned_contributor_ids: list[str] = field(default_factory=list)
