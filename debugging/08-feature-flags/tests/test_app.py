import hashlib
from unittest.mock import patch
import unittest

from app import Flag, FlagClient, Rule, evaluate


class FlagTests(unittest.TestCase):
    def test_disabled_flag_overrides_targets(self):
        flag = Flag("f", enabled=False, targets={"ada": True})
        self.assertFalse(evaluate(flag, "ada"))

    def test_explicit_false_target_overrides_default_true(self):
        flag = Flag("f", default=True, targets={"ada": False})
        self.assertFalse(evaluate(flag, "ada"))

    def test_rule_requires_all_attributes(self):
        flag = Flag("f", rules=[Rule({"team": "ml", "region": "us"}, True)])
        self.assertFalse(evaluate(flag, "ada", {"team": "ml", "region": "eu"}))

    def test_rollout_uses_stable_sha256_bucket(self):
        flag = Flag("f", rollout_percent=50)
        user = "ada"
        bucket = int(hashlib.sha256(b"f:ada").hexdigest(), 16) % 100
        with patch("builtins.hash", side_effect=AssertionError("unstable hash used")):
            self.assertEqual(evaluate(flag, user), bucket < 50)

    def test_zero_percent_rollout_is_always_off(self):
        flag = Flag("f", rollout_percent=0)
        with patch("builtins.hash", return_value=0):
            self.assertFalse(evaluate(flag, "ada"))

    def test_missing_flag_returns_false(self):
        self.assertFalse(FlagClient(lambda: {}).is_enabled("missing", "ada"))

    def test_refresh_replaces_old_snapshot(self):
        snapshots = [{"old": Flag("old")}, {"new": Flag("new")}]
        client = FlagClient(lambda: snapshots.pop(0))
        client.refresh()
        client.refresh()
        self.assertEqual(set(client.flags), {"new"})

    def test_refresh_retries_one_transient_fetch_failure(self):
        calls = 0
        def fetch():
            nonlocal calls
            calls += 1
            if calls == 1:
                raise ConnectionError("temporary")
            return {"f": Flag("f", default=True)}
        client = FlagClient(fetch)
        client.refresh()
        self.assertTrue(client.is_enabled("f", "ada"))
        self.assertEqual(calls, 2)


if __name__ == "__main__":
    unittest.main()
