from ..models.flags import Context, Flag
from .evaluator import evaluate
from .retry import fetch_with_retry
from .snapshots import SnapshotCache


class FlagClient:
    def __init__(self, fetch, cache: SnapshotCache):
        self.fetch = fetch
        self.cache = cache

    def flags(self) -> dict[str, Flag]:
        snapshot = self.cache.get()
        if snapshot: return snapshot.flags
        flags = fetch_with_retry(self.fetch)
        return self.cache.put(flags).flags

    def value(self, key: str, context: Context, fallback=None):
        flag = self.flags().get(key)
        return evaluate(flag, context) if flag else fallback
