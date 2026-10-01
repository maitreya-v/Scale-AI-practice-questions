import asyncio
import unittest

from app import Job, PermanentError, Result, TemporaryError, run


class FanoutTests(unittest.IsolatedAsyncioTestCase):
    async def test_results_keep_input_order(self):
        async def worker(job):
            await asyncio.sleep(0.02 if job.id == "first" else 0)
            return job.payload
        results = await run([Job("first", "a"), Job("second", "b")], worker)
        self.assertEqual([item.id for item in results], ["first", "second"])

    async def test_concurrency_is_bounded(self):
        active = peak = 0
        async def worker(job):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.01)
            active -= 1
            return job.payload
        await run([Job(str(i), "x") for i in range(5)], worker, limit=2)
        self.assertLessEqual(peak, 2)

    async def test_slow_job_times_out_without_blocking_next_job(self):
        async def worker(job):
            if job.id == "slow":
                await asyncio.sleep(0.2)
            return job.payload
        results = await asyncio.wait_for(run([Job("slow", "a"), Job("fast", "b")],
                                             worker, timeout=0.01, retries=0), 0.1)
        self.assertEqual(results, [Result("slow", None, "timeout"), Result("fast", "b", None)])

    async def test_transient_failure_gets_one_retry_by_default(self):
        calls = 0
        async def worker(job):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise TemporaryError("temporary")
            return "ok"
        self.assertEqual(await run([Job("a", "x")], worker), [Result("a", "ok", None)])
        self.assertEqual(calls, 2)

    async def test_permanent_failure_is_not_retried(self):
        calls = 0
        async def worker(job):
            nonlocal calls
            calls += 1
            raise PermanentError("bad input")
        self.assertEqual(await run([Job("a", "x")], worker, retries=2),
                         [Result("a", None, "bad input")])
        self.assertEqual(calls, 1)

    async def test_unexpected_error_is_contained_to_one_job(self):
        async def worker(job):
            if job.id == "bad":
                raise ValueError("malformed")
            return "ok"
        self.assertEqual(await run([Job("bad", "x"), Job("good", "x")], worker),
                         [Result("bad", None, "malformed"), Result("good", "ok", None)])

    async def test_duplicate_job_ids_still_produce_two_results(self):
        async def worker(job):
            return job.payload
        self.assertEqual(await run([Job("same", "a"), Job("same", "b")], worker),
                         [Result("same", "a", None), Result("same", "b", None)])

    async def test_cancelling_parent_cancels_child_jobs(self):
        started = asyncio.Event()
        active = 0
        async def worker(job):
            nonlocal active
            active += 1
            started.set()
            try:
                await asyncio.sleep(1)
            finally:
                active -= 1
        parent = asyncio.create_task(run([Job("a", "x")], worker))
        await started.wait()
        parent.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await parent
        await asyncio.sleep(0)
        self.assertEqual(active, 0)


if __name__ == "__main__":
    unittest.main()
