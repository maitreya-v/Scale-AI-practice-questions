import asyncio
import unittest
from src.async_lab.services.rate_limit import TokenBucket


class RateLimitTests(unittest.TestCase):
    def test_refill_restores_capacity(self):
        async def scenario():
            bucket = TokenBucket(1); await bucket.acquire(); await bucket.refill(); await bucket.acquire(); return bucket.tokens
        self.assertEqual(asyncio.run(scenario()), 0)


if __name__ == "__main__": unittest.main()
