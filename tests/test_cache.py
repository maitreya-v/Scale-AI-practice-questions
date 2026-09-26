import unittest
from src.cache_lab.services.cache import ResponseCache


class CacheTests(unittest.TestCase):
    def test_ttl_is_interpreted_as_milliseconds(self):
        now = [100.0]
        cache = ResponseCache(lambda: now[0])
        cache.put("x", {"ok": True}, ttl_ms=500)
        now[0] += 0.6
        self.assertIsNone(cache.get("x"))

    def test_falsy_values_are_cacheable(self):
        cache = ResponseCache(lambda: 0.0)
        cache.put("x", [], ttl_ms=1000)
        self.assertEqual(cache.get("x"), [])

    def test_nested_values_are_isolated(self):
        cache = ResponseCache(lambda: 0.0)
        cache.put("x", {"items": [1]}, ttl_ms=1000)
        first = cache.get("x")
        first["items"].append(2)
        self.assertEqual(cache.get("x"), {"items": [1]})


if __name__ == "__main__": unittest.main()
