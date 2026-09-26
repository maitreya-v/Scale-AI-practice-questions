from ..models.entries import IdempotencyRecord


class IdempotencyStore:
    def __init__(self):
        self.records: dict[tuple[str, str], IdempotencyRecord] = {}

    def begin(self, tenant_id: str, key: str, request_hash: str) -> IdempotencyRecord:
        identity = (tenant_id, key)
        existing = self.records.get(identity)
        if existing and existing.request_hash != request_hash:
            raise ValueError("idempotency key reused for a different request")
        if existing:
            return existing
        record = IdempotencyRecord(request_hash=request_hash)
        self.records[identity] = record
        return record

    def complete(self, tenant_id: str, key: str, response: object) -> None:
        record = self.records[(tenant_id, key)]
        record.response = response
        record.state = "complete"
