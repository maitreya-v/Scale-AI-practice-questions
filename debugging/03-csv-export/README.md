# CSV export

**Time box:** 45–60 minutes. **Seeded defects:** 8.

An internal exporter accepts a relative CSV path beneath a root directory and a JSON filename beneath `root/output`. Absolute inputs and paths that escape either directory are invalid. CSV headers are trimmed, including a UTF-8 BOM; duplicate normalized headers are rejected. Fully empty data rows are skipped, and missing cells are represented by empty strings. `process_file` returns the output path and the number of exported records.

Run `python3 -m unittest discover -s tests -v` from this directory. Keep the public functions and the JSON shape. No external dependencies are required.
