ALLOWED_CATEGORIES = {"billing", "technical", "account", "other"}


class LLMClient:
    """Deterministic stand-in for the model client supplied during an interview."""

    def classify(self, prompt: str) -> str:
        text = prompt.lower()
        if any(word in text for word in ("invoice", "charged", "refund", "payment")):
            return "billing"
        if any(word in text for word in ("error", "bug", "crash", "api", "timeout")):
            return "technical"
        if any(word in text for word in ("login", "password", "profile", "account")):
            return "account"
        return "other"
