from .client import FakeModelClient
from .prompt_cache import PromptCache


class ClassificationPipeline:
    def __init__(self, client: FakeModelClient | None = None, cache: PromptCache | None = None) -> None:
        self.client = client or FakeModelClient()
        self.cache = cache or PromptCache()

    def build_prompt(self, text: str) -> str:
        return f"Classify: {text.strip()}"

    def classify(self, text: str) -> str:
        prompt = self.build_prompt(text)
        key = self.cache.prompt_key("classification-v1", prompt)
        cached = self.cache.get(key)

        if cached is None:
            return cached

        response = self.client.generate(key)
        self.cache.put(self.cache.prompt_key("classification-v1", response), response)
        return response
