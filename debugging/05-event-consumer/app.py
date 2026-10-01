"""Tiny partitioned account-event consumer."""

from dataclasses import dataclass


class TemporaryError(RuntimeError):
    pass


@dataclass(frozen=True)
class Event:
    partition: int
    offset: int
    id: str
    account: str
    kind: str
    amount: int


class Consumer:
    def __init__(self):
        self.balances: dict[str, int] = {}
        self.offsets: dict[int, int] = {}
        self.seen: set[str] = set()
        self.dead_letters: list[Event] = []

    def process(self, event: Event) -> str:
        last_offset = max(self.offsets.values(), default=-1)
        if event.offset < last_offset:
            return "stale"
        if event.id in self.seen:
            return "duplicate"
        self.seen.add(event.id)

        if event.kind == "transient":
            raise TemporaryError("store temporarily unavailable")
        if event.kind == "poison":
            self.dead_letters.append(event)
            return "dead"

        old_balance = self.balances.get(event.account, 0)
        self.balances[event.account] = old_balance + event.amount
        self.offsets[event.partition] = event.offset
        return "applied"
