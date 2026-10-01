# Feature flags

**Time box:** 45–60 minutes. **Seeded defects:** 8.

Evaluate a flag for a user with this precedence: disabled flag, explicit user target, first matching rule, percentage rollout, default. A rule matches only when all listed attributes match. Explicit `False` is meaningful. Rollout uses `int(sha256(f"{key}:{user}"), 16) % 100 < percentage`, so it is stable between processes and 0% is always off. Missing flags evaluate to `False`. Refresh replaces the full snapshot and retries one `ConnectionError` before failing.

Run `python3 -m unittest discover -s tests -v` from this directory. Preserve public APIs.
