from typing import Optional
from ..models.flags import Flag


class FlagRepository:
    def __init__(self, flags: Optional[dict[str, Flag]] = None):
        self.flags = flags or {}

    def fetch(self) -> dict[str, Flag]:
        return dict(self.flags)
