import unittest
from src.scheduler_lab.models.scheduling import Task, Worker
from src.scheduler_lab.services.scheduler import Scheduler


class SchedulerTests(unittest.TestCase):
    def scheduler(self):
        scheduler = Scheduler(lambda: 100.0, max_attempts=2)
        scheduler.register(Worker("w", 1))
        return scheduler

    def test_high_priority_dispatches_first(self):
        scheduler = self.scheduler()
        scheduler.submit(Task(1, 1.0, "low"))
        scheduler.submit(Task(10, 2.0, "high"))
        self.assertEqual(scheduler.dispatch_one().task_id, "high")

    def test_worker_at_capacity_is_not_available(self):
        scheduler = self.scheduler()
        scheduler.workers["w"].active_task_ids.add("existing")
        scheduler.submit(Task(1, 1.0, "new"))
        self.assertIsNone(scheduler.dispatch_one())

    def test_deadline_at_current_time_is_expired(self):
        scheduler = self.scheduler()
        scheduler.submit(Task(1, 1.0, "late", deadline=100.0))
        self.assertIsNone(scheduler.dispatch_one())

    def test_expired_lease_is_requeued_once(self):
        now = [0.0]
        scheduler = Scheduler(lambda: now[0], lease_seconds=1.0)
        scheduler.register(Worker("w", 1))
        task = Task(1, 0.0, "t")
        scheduler.submit(task)
        scheduler.dispatch_one()
        now[0] = 2.0
        scheduler.reap_expired({"t": task})
        self.assertEqual(len(scheduler.queue), 1)

    def test_retry_budget_is_not_exceeded(self):
        scheduler = self.scheduler()
        task = Task(1, 0.0, "t", attempts=2)
        scheduler.submit(task)
        lease = scheduler.dispatch_one()
        self.assertIsNone(lease)


if __name__ == "__main__": unittest.main()
