"""CSV to JSON export used by a small internal API."""

import csv
import json
from pathlib import Path


def resolve_input(root: str | Path, name: str) -> Path:
    root = Path(root).resolve()
    candidate = (root / name).resolve()
    if not str(candidate).startswith(str(root)):
        raise ValueError("input must stay inside root")
    if not candidate.is_file():
        raise FileNotFoundError(candidate)
    return candidate


def read_records(path: str | Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        records = []
        for row in reader:
            records.append({header: row[header] for header in headers})
        return records


def write_records(root: str | Path, name: str, records: list[dict[str, str]]) -> Path:
    output_dir = Path(root).resolve() / "output"
    output_dir.mkdir(exist_ok=True)
    destination = output_dir / name
    with open(destination, "w", encoding="utf-8") as stream:
        json.dump(records, stream, ensure_ascii=True, indent=2)
    return destination


def process_file(root: str | Path, input_name: str, output_name: str) -> dict[str, object]:
    source = resolve_input(root, input_name)
    records = read_records(source)
    destination = write_records(root, output_name, records)
    return {"path": str(destination), "count": len(records)}
