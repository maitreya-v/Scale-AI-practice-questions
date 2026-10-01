# Scale AI practice questions — debugging set

## Eight compact debugging assignments

The [`debugging/`](debugging/) directory contains eight independent, original practice projects. Each has **eight seeded behavioral defects**, eight focused tests, a short contract, and a suggested **45–60 minute** time box. They use only Python's standard library and do not require an API key or service account. Start with any project; the numbered order gradually widens the debugging surface.

| Project | Scenario |
| --- | --- |
| [01 Assignment pipeline](debugging/01-assignment/) | Contributor eligibility, priority, capacity, reruns |
| [02 Silent model output](debugging/02-llm-pipeline/) | Prompt, model client, cache, response parsing |
| [03 CSV export](debugging/03-csv-export/) | Paths, CSV normalization, JSON output |
| [04 Task scheduler](debugging/04-task-scheduler/) | Priority, deadlines, workers, retries |
| [05 Event consumer](debugging/05-event-consumer/) | Partitions, offsets, deduplication, dead letters |
| [06 Cache and idempotency](debugging/06-cache-idempotency/) | Tenant keys, TTL, replay, failure handling |
| [07 Async fanout](debugging/07-async-fanout/) | Ordering, concurrency, timeout, cancellation |
| [08 Feature flags](debugging/08-feature-flags/) | Targeting, rules, rollout, snapshot refresh |

From one project directory, run `python3 -m unittest discover -s tests -v`. The initial failures are intentional. Fix code under that project's `app.py` while preserving its public API and tests. Each project is self-contained, so solving one does not affect the others. These are practice reconstructions inspired by the repository's interview-style exercises, not official Scale AI questions or proprietary material.

---

## Original backend practical — CSV → JSON → LLM classification

**Fidelity:** High-confidence reconstruction

**Time limit:** 60 minutes

## Interview setup

You are given a small Python backend repository. Build a working HTTP API in stages. Aim for a running solution first, then handle follow-ups cleanly.

## Part 1 — Data ingestion

Implement `POST /process`.

Request JSON:

```json
{
  "csv_path": "data/tickets.csv"
}
```

Requirements:

1. Read the server-visible CSV file at `csv_path`.
2. Convert every row into a JSON object using the CSV header names as keys.
3. Persist the resulting JSON array to the `output/` directory.
4. Return a response containing the output path and number of processed rows.
5. Reject invalid or missing paths with an appropriate HTTP status.
6. Do not allow an input path to escape the exercise directory.

## Part 2 — LLM classification

Extend the endpoint so every record receives a `category` field from the provided `LLMClient`.

Allowed categories:

- `billing`
- `technical`
- `account`
- `other`

Requirements:

1. Construct a clear prompt from the row.
2. Call `LLMClient.classify(prompt)`.
3. Validate that the returned category is one of the allowed values.
4. Persist the category with each row.
5. A failure for one row should not corrupt already processed rows.

## Follow-ups your interviewer may ask

After the happy path works, be prepared to implement or discuss:

- How would this handle a 1,000,000-row CSV without loading everything into memory?
- How would you run model calls concurrently while bounding concurrency?
- How would you preserve input ordering?
- How would you retry transient failures without retrying permanent validation failures?
- How would you resume after a partial process crash?
- Where should an API key live?
- How do you prevent unsafe file paths or partially written output files?
- How do you make repeated requests idempotent?
- What metrics/logs would you add in production?

## Run

```bash
pytest -q
uvicorn starter.app:app --reload
```

The starter intentionally leaves implementation work for you. Do not change the endpoint contract used by the tests.

## Practice setup

Use Python 3.10 or newer. This branch retains the original backend exercise at
the repository root and adds the eight debugging projects above. The original
starter code, datasets, and tests are unchanged.

```bash
git clone --single-branch --branch debugging-scale-like-eight-projects https://github.com/maitreya-v/Scale-AI-practice-questions.git
cd Scale-AI-practice-questions
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

On Windows, activate the environment with `.venv\Scripts\activate`.
Run the original backend exercise commands from the repository root. Failing
tests are expected until you complete it; there is no answer key in this branch.

This is an original practice reconstruction based on public interview reports
and guides, not an official Scale AI repository or proprietary interview material.
