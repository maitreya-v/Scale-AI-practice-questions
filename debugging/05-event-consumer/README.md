# Partitioned event consumer

**Time box:** 45–60 minutes. **Seeded defects:** 8.

Consume credit and debit events into integer account balances. Offsets are per partition, and an event at or below the last committed offset is stale. Event IDs are unique within a partition; redelivery must not apply twice. A transient failure is retryable and changes no state. Poison events, unknown kinds, and credit/debit events with nonpositive amounts go to the dead-letter list, commit their offsets, and never change balances.

Run `python3 -m unittest discover -s tests -v` from this directory. Preserve public methods and types. No broker is needed.
