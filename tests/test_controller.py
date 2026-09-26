import unittest
from src.worker_lab.models.workers import Worker, WorkerEvent
from src.worker_lab.services.controller import WorkerController
from src.worker_lab.services.reconciliation import reconcile_leases


class ControllerTests(unittest.TestCase):
    def controller(self):
        controller = WorkerController()
        controller.register(Worker("w"))
        return controller

    def test_heartbeat_does_not_cancel_draining(self):
        controller = self.controller()
        controller.apply(WorkerEvent("1", "w", "drain", 1, 1.0))
        controller.apply(WorkerEvent("2", "w", "heartbeat", 1, 2.0))
        self.assertEqual(controller.workers["w"].state, "draining")

    def test_failure_requeues_owned_leases(self):
        controller = self.controller()
        controller.assign_lease("w", "lease-1")
        controller.apply(WorkerEvent("2", "w", "failed", 1, 2.0))
        self.assertEqual(reconcile_leases(controller), ["lease-1"])

    def test_recovery_returns_idle_without_leases(self):
        controller = self.controller()
        controller.apply(WorkerEvent("1", "w", "failed", 1, 1.0))
        controller.apply(WorkerEvent("2", "w", "recover", 2, 2.0))
        self.assertEqual(controller.workers["w"].state, "idle")

    def test_newer_generation_wins_even_if_event_arrives_first(self):
        controller = self.controller()
        controller.apply(WorkerEvent("new", "w", "drain", 3, 3.0))
        controller.apply(WorkerEvent("old", "w", "heartbeat", 2, 4.0))
        self.assertEqual(controller.workers["w"].state, "draining")

    def test_duplicate_event_has_no_second_effect(self):
        controller = self.controller()
        event = WorkerEvent("1", "w", "heartbeat", 1, 5.0)
        controller.apply(event)
        controller.workers["w"].last_heartbeat = 10.0
        controller.apply(event)
        self.assertEqual(controller.workers["w"].last_heartbeat, 10.0)


if __name__ == "__main__": unittest.main()
