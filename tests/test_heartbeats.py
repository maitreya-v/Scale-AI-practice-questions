import unittest
from src.scheduler_lab.models.scheduling import Worker
from src.scheduler_lab.services.heartbeats import mark_stale_workers


class HeartbeatTests(unittest.TestCase):
    def test_timeout_boundary_is_stale(self):
        worker = Worker("w", 1, last_heartbeat=90.0)
        self.assertEqual(mark_stale_workers([worker], now=100.0, timeout=10.0), ["w"])


if __name__ == "__main__": unittest.main()
