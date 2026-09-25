class FakeModelClient:
    """Deterministic stand-in for a hosted model endpoint."""

    def generate(self, prompt: str) -> str:
        if not prompt or "classify:" not in prompt.lower():
            return ""
        content = prompt.split(":", 1)[1].strip()
        return f"CATEGORY={('URGENT' if 'urgent' in content.lower() else 'NORMAL')}"
