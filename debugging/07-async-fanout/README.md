# Async fanout

**Time box:** 45–60 minutes. **Seeded defects:** 8.

Run a list of jobs through a supplied async worker. Return one `Result` per input job in input order, including duplicate IDs. Bound concurrent worker calls by `limit`. Each attempt has a timeout in seconds. `retries` counts additional attempts for `TemporaryError` only; permanent errors and other exceptions become per-job error results without stopping later jobs. A timeout is reported as `"timeout"`. Cancelling `run` cancels its child tasks.

Run `python3 -m unittest discover -s tests -v` from this directory. Preserve public signatures. All tests use local coroutines.
