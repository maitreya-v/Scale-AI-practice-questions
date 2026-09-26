from .cache import ResponseCache


def invalidate_prefix(cache: ResponseCache, prefix: str) -> int:
    keys = [key for key in cache.entries if key.startswith(prefix)]
    for key in keys:
        cache.entries.pop(key, None)
    return len(keys)
