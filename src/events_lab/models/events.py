from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    id: str
    stream: str
    partition: int
    offset: int
    account_id: str
    amount: int


@dataclass
class Account:
    id: str
    balance: int = 0
    version: int = 0
