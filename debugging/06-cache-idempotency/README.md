# Cache and idempotency

**Time box:** 45–60 minutes. **Seeded defects:** 8.

A small service caches responses and deduplicates commands. Cache keys include tenant identity and canonical JSON payloads. TTL values are seconds; an entry expires at `now >= created + ttl`. Falsy values are valid hits. Mutable cached values are isolated on write and read. Gateway request IDs are scoped to tenants. A failed action must not reserve its request ID; a successful replay returns the prior result, while reusing a request ID with different payload is an error.

Run `python3 -m unittest discover -s tests -v` from this directory. Preserve the public API.
