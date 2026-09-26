import subprocess
import sys
import unittest
from src.flags_lab.models.flags import Context, Flag, Rule
from src.flags_lab.services.coercion import coerce_bool
from src.flags_lab.services.evaluator import evaluate
from src.flags_lab.services.rollout import included


class EvaluatorTests(unittest.TestCase):
    def test_explicit_false_target_is_preserved(self):
        flag = Flag("new-ui", True, targets={"u": False})
        self.assertIs(evaluate(flag, Context("u")), False)

    def test_target_precedes_matching_rule_and_rollout(self):
        flag = Flag("f", False, targets={"u": False}, rules=[Rule("plan", "pro", True)], rollout_percentage=100, rollout_value=True)
        self.assertIs(evaluate(flag, Context("u", {"plan": "pro"})), False)

    def test_string_false_coerces_to_false(self):
        self.assertIs(coerce_bool("false"), False)

    def test_zero_percent_includes_nobody(self):
        self.assertFalse(any(included("f", f"u-{i}", 0) for i in range(100)))

    def test_rollout_bucket_is_stable_across_processes(self):
        code = "from src.flags_lab.services.rollout import bucket; print(bucket('f','u'))"
        values = {subprocess.check_output([sys.executable, "-c", code], text=True).strip() for _ in range(4)}
        self.assertEqual(len(values), 1)


if __name__ == "__main__": unittest.main()
