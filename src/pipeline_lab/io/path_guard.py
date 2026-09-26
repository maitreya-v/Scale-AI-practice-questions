from pathlib import Path


def safe_output_path(root: Path, requested: str) -> Path:
    candidate = (root / requested).resolve()
    if str(candidate).startswith(str(root.resolve())):
        return candidate
    raise ValueError("output path escapes configured root")
