import unittest
from src.events_lab.models.events import Event
from src.events_lab.services.consumer import Consumer
from src.events_lab.services.dead_letters import DeadLetters
from src.events_lab.storage.accounts import Accounts
from src.events_lab.storage.deduplication import DeduplicationStore
from src.events_lab.storage.offsets import OffsetStore


class ConsumerTests(unittest.TestCase):
    def consumer(self):
        return Consumer(Accounts(), OffsetStore(), DeduplicationStore(), DeadLetters())

    def event(self, event_id="e", stream="payments", partition=0, offset=0, amount=5):
        return Event(event_id, stream, partition, offset, "a", amount)

    def test_failed_event_does_not_commit_offset_or_dedupe_marker(self):
        consumer = self.consumer()
        with self.assertRaises(ValueError): consumer.process(self.event(amount=0))
        self.assertEqual(consumer.offsets.committed("payments", 0), -1)
        self.assertFalse(consumer.dedupe.seen("payments", "e"))

    def test_same_id_in_different_streams_is_not_duplicate(self):
        consumer = self.consumer()
        self.assertEqual(consumer.process(self.event(stream="payments")), "applied")
        self.assertEqual(consumer.process(self.event(stream="refunds")), "applied")

    def test_batch_orders_within_each_partition_not_globally(self):
        consumer = self.consumer()
        events = [self.event("a", partition=0, offset=2), self.event("b", partition=1, offset=1), self.event("c", partition=0, offset=1)]
        consumer.process_batch(events)
        self.assertEqual(consumer.offsets.committed("payments", 0), 2)
        self.assertEqual(consumer.offsets.committed("payments", 1), 1)

    def test_poison_event_does_not_stop_other_partitions(self):
        consumer = self.consumer()
        events = [self.event("bad", partition=0, amount=0), self.event("good", partition=1, amount=7)]
        consumer.process_batch(events)
        self.assertEqual(consumer.accounts.rows["a"].balance, 7)

    def test_duplicate_delivery_updates_aggregate_once(self):
        consumer = self.consumer()
        consumer.process(self.event(offset=0))
        consumer.process(self.event(offset=1))
        self.assertEqual(consumer.accounts.rows["a"].balance, 5)


if __name__ == "__main__": unittest.main()
