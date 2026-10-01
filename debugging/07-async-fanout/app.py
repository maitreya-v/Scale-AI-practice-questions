"""Asynchronous fanout over a supplied worker coroutine."""

import asyncio
from dataclasses import dataclass


class TemporaryError(RuntimeError):
    pass


class PermanentError(RuntimeError):
    pass


@dataclass(frozen=True)
class Job:
    id: str
    payload: str


@dataclass(frozen=True)
class Result:
    id: str
    value: str | None
    error: str | None


async def run(jobs: list[Job], worker, limit: int = 2,
              timeout: float = 0.05, retries: int = 1) -> list[Result]:
    """Run jobs in input order; retries is the number of extra transient attempts."""
    async def one(job: Job) -> Result:
        semaphore = asyncio.Semaphore(limit)
        async with semaphore:
            attempt = 0
            while attempt < max(1, retries):
                attempt += 1
                try:
                    value = await asyncio.wait_for(worker(job), timeout * 1000)
                    return Result(job.id, value, None)
                except RuntimeError as error:
                    last_error = str(error)
            return Result(job.id, None, last_error)

    tasks = [asyncio.create_task(one(job)) for job in jobs]
    results = []
    seen_ids = set()
    for completed in asyncio.as_completed(tasks):
        result = await completed
        if result.id not in seen_ids:
            results.append(result)
            seen_ids.add(result.id)
    return results
