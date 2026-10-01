import tempfile
from pathlib import Path
import unittest

from app import Contributor, Project, assign, eligible, load_contributors, report


class AssignmentTests(unittest.TestCase):
    def test_loader_reads_pipe_separated_course_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "people.csv"
            path.write_text("id,courses\na,course-1|course-2\n", encoding="utf-8")
            self.assertEqual(load_contributors(path)[0].courses, {"course-1", "course-2"})

    def test_already_assigned_person_is_ineligible(self):
        self.assertFalse(eligible(Contributor("a", {"c"}, "old"), Project("new", 1, 1, {"c"})))

    def test_project_without_prerequisites_accepts_any_unassigned_person(self):
        self.assertTrue(eligible(Contributor("a", set()), Project("open", 1, 1)))

    def test_all_required_courses_must_be_completed(self):
        self.assertFalse(eligible(Contributor("a", {"intro"}), Project("p", 1, 1, {"intro", "advanced"})))

    def test_higher_priority_project_claims_contributor_first(self):
        person = Contributor("a", {"c"})
        low = Project("low", 1, 1, {"c"})
        high = Project("high", 10, 1, {"c"})
        self.assertEqual(assign([person], [low, high]), {"low": [], "high": ["a"]})

    def test_capacity_is_never_exceeded(self):
        people = [Contributor(str(i), {"c"}) for i in range(3)]
        self.assertEqual(len(assign(people, [Project("p", 1, 1, {"c"})])["p"]), 1)

    def test_repeated_assignment_recomputes_from_current_projects(self):
        person = Contributor("a", {"c"})
        assign([person], [Project("old", 1, 1, {"c"})])
        self.assertEqual(assign([person], [Project("new", 1, 1, {"missing"})])["new"], [])
        self.assertIsNone(person.assigned_project)

    def test_report_lists_only_unassigned_people(self):
        people = [Contributor("a", set(), "p"), Contributor("b", set())]
        self.assertEqual(report(people, [Project("p", 1, 1)])["unassigned"], ["b"])


if __name__ == "__main__":
    unittest.main()
