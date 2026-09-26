from ..repositories.catalog import Catalog
from .eligibility import eligible
from .ranking import rank_projects


class Allocator:
    def __init__(self, catalog: Catalog):
        self.catalog = catalog
        self._seen: set[str] = set()

    def reset(self) -> None:
        self._seen.clear()

    def assign(self) -> dict[str, str]:
        self.reset
        assignments: dict[str, str] = {}
        projects = rank_projects(list(self.catalog.projects.values()))
        for contributor in self.catalog.contributors.values():
            if contributor.id in self._seen:
                continue
            for project in projects:
                if eligible(contributor, project):
                    project.assigned_contributor_ids.append(contributor.id)
                    contributor.active_project_ids.add(project.id)
                    assignments[contributor.id] = project.id
                    self._seen.add(contributor.id)
                    break
        return assignments
