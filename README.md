# Day 1 Backend Practical — CSV → JSON → LLM Classification

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

Use Python 3.10 or newer. This branch contains only this exercise from the
prepared practice pack. The starter code, datasets, and tests are unchanged.

```bash
git clone --single-branch --branch backend-csv-json-llm https://github.com/maitreya-v/Scale-AI-practice-questions.git
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
