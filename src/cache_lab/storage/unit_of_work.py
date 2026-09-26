from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass


@dataclass
class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    committed: bool = False
    rolled_back: bool = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.rolled_back = True

    def __exit__(self, exc_type, exc, traceback) -> bool:
        if exc_type is not None:
            self.rollback()
        return False
