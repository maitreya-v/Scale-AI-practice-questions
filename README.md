# Day 1 Backend Practical — Lightweight Worker Load Balancer

**Fidelity:** Reported backend/scheduling variant

**Time limit:** 60 minutes

Build a lightweight in-memory dispatcher for tasks and workers. The exercise should evolve incrementally; keep your implementation easy to extend.

## Part 1 — Core models

Implement the existing `Task`, `Worker`, and `Scheduler` APIs.

Workers have these states:

- `IDLE`
- `BUSY`
- `FAILED`
- `DRAINING`

A worker may receive a new task only while `IDLE`.

## Part 2 — Priority scheduling

Tasks have:

- `task_id`
- `priority` — larger number means higher priority
- `created_at`
- optional `deadline`

When an idle worker is available, dispatch the highest-priority non-expired task. For equal priority, dispatch the older task first.

## Part 3 — Failure handling

Support:

- worker failure while a task is running
- requeueing a failed worker's in-flight task
- task attempt counters
- timeout/expiration handling
- draining a worker without assigning it new work

Assume **at-least-once** execution. Be prepared to explain where duplicate work can occur and how production code would make task handling idempotent.

## Part 4 — Scaling discussion

Be ready to discuss:

- queue depth
- queue wait latency
- worker utilization
- scale-up and scale-down thresholds
- heartbeat failure detection
- safe worker draining
- concurrency strategy in Python: threads vs processes vs asyncio
- durability if the process itself crashes

## Run

```bash
pytest -q
```

## Practice setup

Use Python 3.10 or newer. This branch contains only this exercise from the
prepared practice pack. The starter code, datasets, and tests are unchanged.

```bash
git clone --single-branch --branch backend-worker-load-balancer https://github.com/maitreya-v/Scale-AI-practice-questions.git
cd Scale-AI-practice-questions
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

On Windows, activate the environment with `.venv\Scripts\activate`.
Run commands from the repository root. Failing tests are expected until you
complete the exercise; there is no answer key in this branch.

This is an original practice reconstruction based on public interview reports
and guides, not an official Scale AI repository or proprietary interview material.
