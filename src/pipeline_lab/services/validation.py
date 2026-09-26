from ..models.records import InputRecord


def validate_record(record: InputRecord) -> None:
    if not record.row_id.strip():
        raise ValueError("row id is required")
    if not record.text.strip():
        raise ValueError("text is required")
