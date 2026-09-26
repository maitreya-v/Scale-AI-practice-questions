import asyncio


async def with_timeout(operation, timeout_ms: int):
    return await asyncio.wait_for(operation, timeout=timeout_ms)
