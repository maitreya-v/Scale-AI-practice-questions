from dataclasses import dataclass, field
from typing import List, Set


@dataclass(frozen=True)
class Course:
    id: str
    name: str


@dataclass
class Contributor:
    id: str
    name: str
    completed_course_ids: Set[str] = field(default_factory=set)
    assigned_project_id: str | None = None

    def reset_assignment(self) -> None:
        self.assigned_project_id = None


@dataclass
class Project:
    id: str
    name: str
    priority: int
    capacity: int
    required_course_ids: List[str] = field(default_factory=list)
    assigned_contributor_ids: List[str] = field(default_factory=list)

    @property
    def available_slots(self) -> int:
        return self.capacity - len(self.assigned_contributor_ids)
