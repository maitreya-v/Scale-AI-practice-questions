import unittest
from src.assignment_lab.models.domain import Contributor, Course, Project
from src.assignment_lab.repositories.catalog import Catalog
from src.assignment_lab.services.allocator import Allocator


class AssignmentTests(unittest.TestCase):
    def catalog(self):
        return Catalog(
            {"c1": Contributor("c1", {"python"}), "c2": Contributor("c2", set())},
            {"low": Project("low", 1, 2), "high": Project("high", 9, 1, {"python"})},
            {"python": Course("python", "Python")},
        )

    def test_highest_priority_project_wins(self):
        self.assertEqual(Allocator(self.catalog()).assign()["c1"], "high")

    def test_prerequisites_are_enforced(self):
        assignments = Allocator(self.catalog()).assign()
        self.assertNotEqual(assignments.get("c2"), "high")

    def test_zero_remaining_capacity_is_full(self):
        catalog = self.catalog()
        catalog.projects["high"].assigned_contributor_ids.append("existing")
        self.assertNotEqual(Allocator(catalog).assign().get("c1"), "high")

    def test_second_run_resets_transient_seen_state(self):
        allocator = Allocator(self.catalog())
        allocator.assign()
        for project in allocator.catalog.projects.values():
            project.assigned_contributor_ids.clear()
        for contributor in allocator.catalog.contributors.values():
            contributor.active_project_ids.clear()
        self.assertTrue(allocator.assign())


if __name__ == "__main__":
    unittest.main()
