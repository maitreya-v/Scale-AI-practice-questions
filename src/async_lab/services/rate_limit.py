import asyncio


class TokenBucket:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.tokens = capacity
        self.lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self.lock:
            if self.tokens <= 0:
                raise RuntimeError("rate limit exhausted")
            self.tokens -= 1

    async def refill(self) -> None:
        async with self.lock:
            self.tokens = self.capacity
