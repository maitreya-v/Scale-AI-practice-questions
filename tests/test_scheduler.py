from starter.models import Task, Worker, WorkerState
from starter.scheduler import Scheduler


def test_higher_priority_task_dispatches_first():
    s = Scheduler()
    s.register_worker(Worker("w1"))
    s.submit_task(Task("low", priority=1, created_at=1))
    s.submit_task(Task("high", priority=10, created_at=2))
    assert s.dispatch_next(now=3) == ("w1", "high")


def test_fifo_for_equal_priority():
    s = Scheduler()
    s.register_worker(Worker("w1"))
    s.submit_task(Task("older", priority=5, created_at=1))
    s.submit_task(Task("newer", priority=5, created_at=2))
    assert s.dispatch_next(now=3) == ("w1", "older")


def test_expired_task_is_not_dispatched():
    s = Scheduler()
    s.register_worker(Worker("w1"))
    s.submit_task(Task("expired", priority=100, created_at=1, deadline=2))
    s.submit_task(Task("valid", priority=1, created_at=1, deadline=10))
    assert s.dispatch_next(now=3) == ("w1", "valid")


def test_failed_worker_requeues_inflight_task():
    s = Scheduler()
    s.register_worker(Worker("w1"))
    s.register_worker(Worker("w2"))
    s.submit_task(Task("t1", priority=1, created_at=1))
    assert s.dispatch_next(now=2) == ("w1", "t1")
    s.fail_worker("w1")
    assert s.workers["w1"].state == WorkerState.FAILED
    assert s.dispatch_next(now=3) == ("w2", "t1")
    assert s.tasks["t1"].attempts == 2


def test_draining_worker_gets_no_new_work():
    s = Scheduler()
    s.register_worker(Worker("w1"))
    s.drain_worker("w1")
    s.submit_task(Task("t1", priority=1, created_at=1))
    assert s.dispatch_next(now=2) is None
