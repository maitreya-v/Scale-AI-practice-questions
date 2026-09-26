class OffsetStore:
    def __init__(self):
        self.offsets: dict[tuple[str, int], int] = {}

    def committed(self, stream: str, partition: int) -> int:
        return self.offsets.get((stream, partition), -1)

    def commit(self, stream: str, partition: int, offset: int) -> None:
        self.offsets[(stream, partition)] = offset
