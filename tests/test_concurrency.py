import asyncio
import unittest
from src.async_lab.models.jobs import Job
from src.async_lab.services.fanout import process_all


class ConcurrencyTests(unittest.TestCase):
    def test_parallelism_is_bounded_and_greater_than_one(self):
        async def scenario():
            active = 0; peak = 0
            async def handler(job):
                nonlocal active, peak
                active += 1; peak = max(peak, active)
                await asyncio.sleep(0.01)
                active -= 1
                return job.payload
            await process_all([Job(str(i), str(i)) for i in range(6)], handler, concurrency=2)
            return peak
        self.assertEqual(asyncio.run(scenario()), 2)

    def test_result_order_matches_input(self):
        async def scenario():
            async def handler(job): return job.payload
            jobs = [Job("z", "first"), Job("a", "second")]
            return [result.value for result in await process_all(jobs, handler)]
        self.assertEqual(asyncio.run(scenario()), ["first", "second"])

    def test_one_failure_does_not_cancel_siblings(self):
        async def scenario():
            async def handler(job):
                if job.id == "bad": raise RuntimeError("boom")
                return "ok"
            return await process_all([Job("bad", ""), Job("good", "")], handler)
        results = asyncio.run(scenario())
        self.assertEqual([result.job_id for result in results], ["bad", "good"])
        self.assertEqual(results[1].value, "ok")

    def test_timeout_is_milliseconds(self):
        async def scenario():
            async def slow(_): await asyncio.sleep(0.02); return "done"
            return await process_all([Job("x", "")], slow, timeout_ms=5)
        self.assertEqual(asyncio.run(scenario())[0].error, "TimeoutError")

    def test_cancellation_propagates(self):
        async def scenario():
            started = asyncio.Event()
            async def handler(_): started.set(); await asyncio.sleep(10); return "done"
            task = asyncio.create_task(process_all([Job("x", "")], handler))
            await started.wait(); task.cancel()
            with self.assertRaises(asyncio.CancelledError): await task
        asyncio.run(scenario())


if __name__ == "__main__": unittest.main()
