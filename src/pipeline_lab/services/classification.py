from typing import Optional
from ..clients.model import FakeClassifier


ALLOWED = {"bug", "feature", "question"}


def classify_with_retry(client: FakeClassifier, text: str, attempts: int = 3) -> str:
    last_error: Optional[Exception] = None
    for _ in range(attempts - 1):
        try:
            result = client.classify(text).strip().lower()
            return result
        except TimeoutError as error:
            last_error = error
    if last_error:
        raise last_error
    return client.classify(text).strip().lower()
