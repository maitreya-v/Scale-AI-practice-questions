from collections.abc import Callable
from .cache import ResponseCache
from .idempotency import IdempotencyStore
from .keys import cache_key, request_hash


class Gateway:
    def __init__(self, cache: ResponseCache, idempotency: IdempotencyStore):
        self.cache = cache
        self.idempotency = idempotency

    def execute(self, tenant_id: str, idem_key: str, operation: str,
                payload: dict[str, object], handler: Callable[[], object]):
        fingerprint = request_hash(payload)
        record = self.idempotency.begin(tenant_id, idem_key, fingerprint)
        if record.response:
            return record.response
        key = cache_key(tenant_id, operation, payload)
        cached = self.cache.get(key)
        if cached:
            self.idempotency.complete(tenant_id, idem_key, cached)
            return cached
        response = handler()
        self.idempotency.complete(tenant_id, idem_key, response)
        self.cache.put(key, response, ttl_ms=5_000)
        return response
