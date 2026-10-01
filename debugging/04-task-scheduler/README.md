# Task scheduler

**Time box:** 45–60 minutes. **Seeded defects:** 8.

An in-memory scheduler dispatches the highest priority task first (larger number means higher priority), FIFO on ties. A task is expired when `now >= deadline`. Each worker runs at most one task. Submitting the same task ID twice does not enqueue another copy. A failed attempt is retried while attempts remain, and completion makes the worker idle. All times are supplied to `dispatch`, so tests need no clock or sleeps.

Run `python3 -m unittest discover -s tests -v` from this directory. Preserve the public methods and data types.
