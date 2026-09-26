import unittest
from src.events_lab.storage.offsets import OffsetStore


class OffsetTests(unittest.TestCase):
    def test_offsets_are_partition_scoped(self):
        store = OffsetStore(); store.commit("s", 0, 9)
        self.assertEqual(store.committed("s", 1), -1)


if __name__ == "__main__": unittest.main()
