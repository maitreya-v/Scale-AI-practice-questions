import json
from pathlib import Path

from fastapi.testclient import TestClient

from starter.app import app

ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_process_csv_creates_json_with_categories():
    response = client.post("/process", json={"csv_path": "data/tickets.csv"})
    assert response.status_code == 200
    body = response.json()
    assert body["rows_processed"] == 4

    output_path = ROOT / body["output_path"]
    assert output_path.exists()

    rows = json.loads(output_path.read_text())
    assert [row["category"] for row in rows] == [
        "billing",
        "technical",
        "account",
        "other",
    ]


def test_missing_input_returns_404():
    response = client.post("/process", json={"csv_path": "data/does-not-exist.csv"})
    assert response.status_code == 404


def test_path_traversal_is_rejected():
    response = client.post("/process", json={"csv_path": "../../etc/passwd"})
    assert response.status_code in {400, 403}
