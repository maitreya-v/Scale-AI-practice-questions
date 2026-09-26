import unittest
from src.pipeline_lab.clients.model import FakeClassifier
from src.pipeline_lab.models.records import InputRecord
from src.pipeline_lab.services.classification import classify_with_retry
from src.pipeline_lab.services.processor import process


class ProcessorTests(unittest.TestCase):
    def test_transient_error_uses_full_retry_budget(self):
        outcomes = iter([TimeoutError(), TimeoutError(), "bug"])
        def behavior(_):
            value = next(outcomes)
            if isinstance(value, Exception): raise value
            return value
        self.assertEqual(classify_with_retry(FakeClassifier(behavior), "x", attempts=3), "bug")

    def test_invalid_model_category_is_rejected(self):
        client = FakeClassifier(lambda _: "surprise")
        with self.assertRaises(ValueError):
            classify_with_retry(client, "x")

    def test_one_bad_row_does_not_abort_valid_rows(self):
        rows = [InputRecord("1", "valid"), InputRecord("2", "")]
        result = process(rows, FakeClassifier(lambda _: "bug"))
        self.assertEqual([row.row_id for row in result], ["1", "2"])
        self.assertTrue(result[1].errors)

    def test_output_order_matches_input_order(self):
        rows = [InputRecord("b", "second"), InputRecord("a", "first")]
        result = process(rows, FakeClassifier(lambda _: "question"))
        self.assertEqual([row.row_id for row in result], ["b", "a"])


if __name__ == "__main__": unittest.main()
