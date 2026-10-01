import json
from pathlib import Path
import tempfile
import unittest

from app import process_file, read_records, resolve_input, write_records


class CsvExportTests(unittest.TestCase):
    def test_absolute_input_paths_are_rejected_even_inside_root(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("id\n1\n")
            with self.assertRaises(ValueError):
                resolve_input(directory, str(path))

    def test_sibling_directory_with_same_prefix_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "data"
            sibling = Path(directory) / "data-old"
            root.mkdir()
            sibling.mkdir()
            (sibling / "secret.csv").write_text("id\n1\n")
            with self.assertRaises(ValueError):
                resolve_input(root, "../data-old/secret.csv")

    def test_utf8_bom_is_removed_from_first_header(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("\ufeffid,name\n1,Ada\n", encoding="utf-8")
            self.assertEqual(read_records(path), [{"id": "1", "name": "Ada"}])

    def test_headers_are_trimmed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text(" id , name \n1,Ada\n")
            self.assertEqual(read_records(path), [{"id": "1", "name": "Ada"}])

    def test_duplicate_normalized_headers_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("id, id \n1,2\n")
            with self.assertRaises(ValueError):
                read_records(path)

    def test_fully_empty_data_rows_are_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("id,name\n,\n1,Ada\n")
            self.assertEqual(read_records(path), [{"id": "1", "name": "Ada"}])

    def test_missing_cells_become_empty_strings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("id,name\n1\n")
            self.assertEqual(read_records(path), [{"id": "1", "name": ""}])

    def test_output_name_cannot_escape_output_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                write_records(directory, "../escaped.json", [{"id": "1"}])
            self.assertFalse((Path(directory) / "escaped.json").exists())


if __name__ == "__main__":
    unittest.main()
