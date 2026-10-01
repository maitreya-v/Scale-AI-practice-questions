import unittest

from app import Consumer, Event, TemporaryError


def event(partition=0, offset=0, id="a", kind="credit", amount=5):
    return Event(partition, offset, id, "acct", kind, amount)


class ConsumerTests(unittest.TestCase):
    def test_debit_subtracts_from_balance(self):
        consumer = Consumer()
        consumer.process(event())
        consumer.process(event(offset=1, id="b", kind="debit", amount=2))
        self.assertEqual(consumer.balances["acct"], 3)

    def test_same_id_in_different_partitions_is_distinct(self):
        consumer = Consumer()
        consumer.process(event(partition=0, offset=0))
        self.assertEqual(consumer.process(event(partition=1, offset=0)), "applied")

    def test_offsets_are_tracked_per_partition(self):
        consumer = Consumer()
        consumer.process(event(partition=0, offset=20, id="a"))
        self.assertEqual(consumer.process(event(partition=1, offset=0, id="b")), "applied")

    def test_same_offset_replay_is_stale_even_with_new_id(self):
        consumer = Consumer()
        consumer.process(event())
        self.assertEqual(consumer.process(event(id="new")), "stale")
        self.assertEqual(consumer.balances["acct"], 5)

    def test_transient_failure_can_be_retried(self):
        consumer = Consumer()
        bad = event(kind="transient")
        with self.assertRaises(TemporaryError):
            consumer.process(bad)
        self.assertEqual(consumer.process(event(id="a", kind="credit")), "applied")

    def test_poison_event_goes_to_dead_letter_and_advances_offset(self):
        consumer = Consumer()
        poison = event(kind="poison")
        self.assertEqual(consumer.process(poison), "dead")
        self.assertEqual(consumer.dead_letters, [poison])
        self.assertEqual(consumer.offsets[0], 0)

    def test_unknown_kind_is_dead_lettered_without_balance_change(self):
        consumer = Consumer()
        self.assertEqual(consumer.process(event(kind="mystery")), "dead")
        self.assertEqual(consumer.balances, {})

    def test_nonpositive_amount_is_dead_lettered(self):
        consumer = Consumer()
        self.assertEqual(consumer.process(event(amount=-5)), "dead")
        self.assertEqual(consumer.balances, {})


if __name__ == "__main__":
    unittest.main()
