import unittest

from app import Scheduler, Task


class SchedulerTests(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()
        self.scheduler.register("w1")

    def test_highest_priority_dispatches_first(self):
        self.scheduler.submit(Task("low", 1, 100))
        self.scheduler.submit(Task("high", 10, 100))
        self.assertEqual(self.scheduler.dispatch("w1", 0).id, "high")

    def test_equal_priority_is_fifo(self):
        self.scheduler.submit(Task("first", 1, 100))
        self.scheduler.submit(Task("second", 1, 100))
        self.assertEqual(self.scheduler.dispatch("w1", 0).id, "first")

    def test_task_expires_at_deadline(self):
        self.scheduler.submit(Task("expired", 1, 10))
        self.assertIsNone(self.scheduler.dispatch("w1", 10))

    def test_busy_worker_cannot_receive_another_task(self):
        self.scheduler.submit(Task("a", 1, 100))
        self.scheduler.submit(Task("b", 1, 100))
        self.scheduler.dispatch("w1", 0)
        self.assertIsNone(self.scheduler.dispatch("w1", 0))
        self.assertEqual(self.scheduler.running["w1"].id, "a")

    def test_failed_task_is_requeued_for_retry(self):
        task = Task("a", 5, 100, max_attempts=2)
        self.scheduler.submit(task)
        self.scheduler.dispatch("w1", 0)
        self.scheduler.fail("w1")
        self.assertEqual(task.priority, 5)
        self.assertEqual(self.scheduler.dispatch("w1", 1).id, "a")

    def test_retry_limit_is_respected(self):
        self.scheduler.submit(Task("a", 1, 100, max_attempts=1))
        self.scheduler.dispatch("w1", 0)
        self.scheduler.fail("w1")
        self.assertIsNone(self.scheduler.dispatch("w1", 1))

    def test_completion_makes_worker_idle(self):
        self.scheduler.submit(Task("a", 1, 100))
        self.scheduler.dispatch("w1", 0)
        self.scheduler.complete("w1")
        self.assertEqual(self.scheduler.workers["w1"], "idle")

    def test_duplicate_task_id_is_not_enqueued_twice(self):
        self.scheduler.submit(Task("a", 1, 100))
        self.scheduler.submit(Task("a", 99, 100))
        self.assertEqual(len(self.scheduler.pending), 1)


if __name__ == "__main__":
    unittest.main()
