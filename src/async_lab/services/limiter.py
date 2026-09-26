import asyncio


class ConcurrencyLimiter:
    def __init__(self, limit: int):
        self.limit = limit

    async def run(self, operation):
        semaphore = asyncio.Semaphore(self.limit)
        async with semaphore:
            return await operation()
