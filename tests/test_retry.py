import unittest
from src.flags_lab.services.retry import fetch_with_retry


class RetryTests(unittest.TestCase):
    def test_transient_timeouts_are_retried(self):
        values = iter([TimeoutError(), {"ok": True}])
        def fetch():
            value = next(values)
            if isinstance(value, Exception): raise value
            return value
        self.assertEqual(fetch_with_retry(fetch), {"ok": True})

    def test_validation_error_is_not_retried(self):
        calls = []
        def fetch(): calls.append(1); raise ValueError("bad document")
        with self.assertRaises(ValueError): fetch_with_retry(fetch)
        self.assertEqual(len(calls), 1)


if __name__ == "__main__": unittest.main()
