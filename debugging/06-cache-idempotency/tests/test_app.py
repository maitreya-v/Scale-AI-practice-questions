import unittest

from app import Cache, Gateway


class CacheGatewayTests(unittest.TestCase):
    def test_cache_keys_are_tenant_scoped(self):
        cache = Cache()
        self.assertNotEqual(cache.key("alpha", {"q": 1}), cache.key("beta", {"q": 1}))

    def test_equivalent_json_payloads_have_same_key(self):
        cache = Cache()
        self.assertEqual(cache.key("alpha", {"a": 1, "b": 2}),
                         cache.key("alpha", {"b": 2, "a": 1}))

    def test_ttl_uses_seconds_and_expires_at_boundary(self):
        cache = Cache()
        cache.put("k", "value", now=10.0, ttl=2.0)
        self.assertEqual(cache.get("k", now=11.9), "value")
        self.assertIsNone(cache.get("k", now=12.0))

    def test_falsy_cached_values_are_hits(self):
        cache = Cache()
        cache.put("k", False, now=0, ttl=10)
        self.assertIs(cache.get("k", now=1), False)

    def test_cached_objects_are_isolated_from_mutation(self):
        cache = Cache()
        original = {"items": [1]}
        cache.put("k", original, now=0, ttl=10)
        original["items"].append(2)
        first = cache.get("k", now=1)
        first["items"].append(3)
        self.assertEqual(cache.get("k", now=1), {"items": [1]})

    def test_idempotency_keys_are_tenant_scoped(self):
        gateway = Gateway()
        self.assertEqual(gateway.execute("alpha", "same", {}, lambda _: "A"), "A")
        self.assertEqual(gateway.execute("beta", "same", {}, lambda _: "B"), "B")

    def test_failed_action_does_not_commit_idempotency_record(self):
        gateway = Gateway()
        def fail(_):
            raise RuntimeError("try again")
        with self.assertRaises(RuntimeError):
            gateway.execute("alpha", "one", {}, fail)
        self.assertEqual(gateway.execute("alpha", "one", {}, lambda _: "ok"), "ok")

    def test_same_key_with_different_payload_is_rejected(self):
        gateway = Gateway()
        gateway.execute("alpha", "one", {"x": 1}, lambda _: "ok")
        with self.assertRaises(ValueError):
            gateway.execute("alpha", "one", {"x": 2}, lambda _: "new")


if __name__ == "__main__":
    unittest.main()
