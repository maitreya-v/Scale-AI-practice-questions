import asyncio
from collections.abc import Awaitable, Callable
from ..models.jobs import Job, JobResult
from .limiter import ConcurrencyLimiter
from .worker import execute


async def process_all(jobs: list[Job], handler: Callable[[Job], Awaitable[str]],
                      concurrency: int = 4, timeout_ms: int = 1000) -> list[JobResult]:
    limiter = ConcurrencyLimiter(concurrency)
    results = []
    for job in jobs:
        results.append(await execute(job, handler, limiter, timeout_ms))
    return sorted(results, key=lambda result: result.job_id)


async def first_success(jobs: list[Job], handler, timeout_ms: int = 1000):
    tasks = [asyncio.create_task(handler(job)) for job in jobs]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return next(iter(done)).result()
