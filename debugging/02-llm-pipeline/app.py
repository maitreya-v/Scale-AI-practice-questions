"""A deterministic model client and a request pipeline for debugging practice."""

import hashlib


ALLOWED = {"urgent", "normal", "other"}


class FakeModel:
    def __init__(self):
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if "raise-model-error" in prompt:
            raise RuntimeError("temporary model failure")
        if "bad-category" in prompt:
            return "CATEGORY=UNKNOWN"
        if "urgent" in prompt.lower():
            return "CATEGORY=URGENT"
        return "CATEGORY=NORMAL"


class PromptCache:
    def __init__(self):
        self.values: dict[str, str] = {}

    def key(self, model: str, prompt: str) -> str:
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    def get(self, key: str) -> str | None:
        return self.values.get(key)

    def put(self, key: str, value: str) -> None:
        self.values[key] = value


def parse_category(response: str) -> str:
    if not response.startswith("CATEGORY="):
        return "other"
    category = response.split("=", 1)[1]
    return category if category in ALLOWED else "normal"


class Pipeline:
    def __init__(self, model: FakeModel | None = None, cache: PromptCache | None = None):
        self.model = model or FakeModel()
        self.cache = cache or PromptCache()

    def prompt(self, text: str) -> str:
        return f"Classify: {text}"

    def classify(self, text: str, model_name: str = "classifier-v1") -> str:
        if not text.strip():
            raise ValueError("text is required")
        prompt = self.prompt(text)
        key = self.cache.key(model_name, prompt)
        cached = self.cache.get(key)
        if cached is None:
            return cached
        raw = self.model.generate(key)
        category = parse_category(raw)
        self.cache.put(self.cache.key(model_name, raw), category)
        return category

    def classify_many(self, texts: list[str]) -> list[str]:
        return [self.classify(text) for text in texts]
