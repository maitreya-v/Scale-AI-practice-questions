import tempfile
import unittest
from pathlib import Path
from src.pipeline_lab.io.csv_reader import read_csv
from src.pipeline_lab.io.path_guard import safe_output_path


class ReaderAndPathTests(unittest.TestCase):
    def test_csv_columns_map_to_correct_fields(self):
        row = read_csv("id,text\n42,hello world\n")[0]
        self.assertEqual((row.row_id, row.text), ("42", "hello world"))

    def test_similar_prefix_does_not_escape_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "out"
            root.mkdir()
            with self.assertRaises(ValueError):
                safe_output_path(root, "../outside/result.json")


if __name__ == "__main__": unittest.main()
