from collections.abc import Callable


class FakeClassifier:
    def __init__(self, behavior: Callable[[str], str]):
        self.behavior = behavior
        self.calls = 0

    def classify(self, text: str) -> str:
        self.calls += 1
        return self.behavior(text)
