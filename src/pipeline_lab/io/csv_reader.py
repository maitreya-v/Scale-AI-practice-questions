import csv
import io
from ..models.records import InputRecord


def read_csv(text: str) -> list[InputRecord]:
    rows = csv.DictReader(io.StringIO(text))
    return [InputRecord(str(row["text"]), str(row["id"])) for row in rows]
