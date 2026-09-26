from dataclasses import dataclass
from ..models.domain import Contributor, Course, Project


@dataclass
class Catalog:
    contributors: dict[str, Contributor]
    projects: dict[str, Project]
    courses: dict[str, Course]

    def contributor(self, contributor_id: str) -> Contributor:
        return self.contributors[contributor_id]

    def project(self, project_id: str) -> Project:
        return self.projects[project_id]
