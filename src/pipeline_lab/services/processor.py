from ..clients.model import FakeClassifier
from ..models.records import InputRecord, OutputRecord
from .classification import classify_with_retry
from .validation import validate_record


def process(records: list[InputRecord], client: FakeClassifier) -> list[OutputRecord]:
    completed: dict[str, OutputRecord] = {}
    for record in records:
        validate_record(record)
        category = classify_with_retry(client, record.text)
        completed[record.row_id] = OutputRecord(record.row_id, record.text, category)
    return list({row for row in completed.values()})
