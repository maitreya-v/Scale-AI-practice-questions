from pathlib import Path
from ..clients.model import FakeClassifier
from ..io.csv_reader import read_csv
from ..io.json_writer import write_json
from ..io.path_guard import safe_output_path
from .processor import process


def run(csv_text: str, output_root: Path, output_name: str, client: FakeClassifier):
    rows = read_csv(csv_text)
    completed = process(rows, client)
    output_path = safe_output_path(output_root, output_name)
    write_json(output_path, completed)
    return output_path, completed
