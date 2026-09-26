import unittest
from src.assignment_lab.models.domain import Project
from src.assignment_lab.services.demand import most_demanded_course


class DemandTests(unittest.TestCase):
    def test_counts_required_courses(self):
        projects = [
            Project("a", 1, 1, {"python"}),
            Project("b", 1, 1, {"python", "sql"}),
            Project("c", 1, 1, {"sql"}),
            Project("d", 1, 1, {"python"}),
        ]
        self.assertEqual(most_demanded_course(projects), "python")

    def test_empty_requirements_have_no_demand(self):
        self.assertIsNone(most_demanded_course([Project("a", 1, 1)]))


if __name__ == "__main__":
    unittest.main()
