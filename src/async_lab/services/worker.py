from collections.abc import Awaitable, Callable
from ..models.jobs import Job, JobResult
from .limiter import ConcurrencyLimiter
from .timeouts import with_timeout


async def execute(job: Job, handler: Callable[[Job], Awaitable[str]],
                  limiter: ConcurrencyLimiter, timeout_ms: int) -> JobResult:
    try:
        value = await limiter.run(lambda: with_timeout(handler(job), timeout_ms))
        return JobResult(job.id, value=value)
    except BaseException as error:
        return JobResult(job.id, error=type(error).__name__)
