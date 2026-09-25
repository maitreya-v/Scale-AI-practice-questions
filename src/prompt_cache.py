import hashlib


class PromptCache:
    def __init__(self) -> None:
        self._cache: dict[str, str] = {}

    def prompt_key(self, system_prompt: str, user_prompt: str) -> str:
        payload = system_prompt.encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def get(self, key: str) -> str | None:
        return self._cache.get(key)

    def put(self, key: str, value: str) -> None:
        self._cache[key] = value
