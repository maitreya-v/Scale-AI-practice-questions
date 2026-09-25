from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"


def resolve_input_path(raw_path: str) -> Path:
    raise NotImplementedError


def atomic_write_json(records: list[dict], destination: Path) -> None:
    raise NotImplementedError
