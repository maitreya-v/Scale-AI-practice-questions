import json
from dataclasses import asdict
from pathlib import Path
from ..models.records import OutputRecord


def write_json(path: Path, rows: list[OutputRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(row) for row in rows]
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
