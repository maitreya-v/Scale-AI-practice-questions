import heapq
from typing import Optional
from ..models.scheduling import Task


class TaskQueue:
    def __init__(self):
        self._heap: list[Task] = []

    def push(self, task: Task) -> None:
        heapq.heappush(self._heap, task)

    def pop(self) -> Optional[Task]:
        return heapq.heappop(self._heap) if self._heap else None

    def __len__(self) -> int:
        return len(self._heap)
