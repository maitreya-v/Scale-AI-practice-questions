from ..models.events import Event
from ..storage.accounts import Accounts
from ..storage.deduplication import DeduplicationStore
from ..storage.offsets import OffsetStore
from .dead_letters import DeadLetters


class Consumer:
    def __init__(self, accounts: Accounts, offsets: OffsetStore,
                 dedupe: DeduplicationStore, dead_letters: DeadLetters):
        self.accounts = accounts
        self.offsets = offsets
        self.dedupe = dedupe
        self.dead_letters = dead_letters

    def process(self, event: Event) -> str:
        if event.offset <= self.offsets.committed(event.stream, event.partition):
            return "old"
        self.offsets.commit(event.stream, event.partition, event.offset)
        if self.dedupe.seen(event.stream, event.id):
            return "duplicate"
        self.dedupe.mark(event.stream, event.id)
        if event.amount == 0:
            raise ValueError("zero amount")
        self.accounts.apply(event.account_id, event.amount)
        return "applied"

    def process_batch(self, events: list[Event]) -> list[str]:
        results = []
        for event in sorted(events, key=lambda item: item.offset):
            try:
                results.append(self.process(event))
            except Exception as error:
                self.dead_letters.add(event, str(error))
                break
        return results
