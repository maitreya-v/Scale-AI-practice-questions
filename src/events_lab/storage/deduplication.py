class DeduplicationStore:
    def __init__(self):
        self.ids: set[str] = set()

    def seen(self, stream: str, event_id: str) -> bool:
        return event_id in self.ids

    def mark(self, stream: str, event_id: str) -> None:
        self.ids.add(event_id)
