import unittest
from src.cache_lab.services.cache import ResponseCache
from src.cache_lab.services.gateway import Gateway
from src.cache_lab.services.idempotency import IdempotencyStore
from src.cache_lab.services.keys import cache_key


class GatewayTests(unittest.TestCase):
    def gateway(self):
        return Gateway(ResponseCache(lambda: 0.0), IdempotencyStore())

    def test_cache_is_tenant_scoped(self):
        self.assertNotEqual(cache_key("a", "read", {"id": 1}), cache_key("b", "read", {"id": 1}))

    def test_zero_response_is_replayed_without_second_call(self):
        gateway = self.gateway()
        calls = []
        handler = lambda: calls.append(1) or 0
        gateway.execute("t", "k", "count", {}, handler)
        gateway.execute("t", "k", "count", {}, handler)
        self.assertEqual(len(calls), 1)

    def test_failure_does_not_leave_completed_record(self):
        gateway = self.gateway()
        with self.assertRaises(RuntimeError):
            gateway.execute("t", "k", "write", {}, lambda: (_ for _ in ()).throw(RuntimeError("boom")))
        self.assertNotIn(("t", "k"), gateway.idempotency.records)


if __name__ == "__main__": unittest.main()
