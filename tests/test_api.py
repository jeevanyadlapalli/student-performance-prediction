"""Basic API tests. Run after generating data and training the model."""
import json
from pathlib import Path
import pytest
from backend.app import create_app

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "backend" / "models" / "student_marks_model.joblib"
METRICS_PATH = ROOT / "backend" / "models" / "metrics.json"
DATA_PATH = ROOT / "backend" / "data" / "student_data.csv"

@pytest.fixture()
def client(tmp_path):
    if not MODEL_PATH.exists():
        pytest.skip("Run backend/generate_data.py and backend/train_model.py first.")
    app = create_app({
        "TESTING": True,
        "DB_PATH": str(tmp_path / "test.db"),
        "MODEL_PATH": str(MODEL_PATH),
        "METRICS_PATH": str(METRICS_PATH),
        "DATA_PATH": str(DATA_PATH),
    })
    return app.test_client()

def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_predict_valid_input(client):
    response = client.post("/api/predict", json={
        "study_hours": 3,
        "attendance": 85,
        "previous_marks": 70,
        "assignment_score": 80,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 0 <= data["predicted_marks"] <= 100

def test_predict_rejects_missing_field(client):
    response = client.post("/api/predict", json={
        "study_hours": 3,
        "attendance": 85,
        "previous_marks": 70,
    })
    assert response.status_code == 400
    assert "Missing required field" in response.get_json()["error"]

def test_predict_rejects_out_of_range(client):
    response = client.post("/api/predict", json={
        "study_hours": 30,
        "attendance": 85,
        "previous_marks": 70,
        "assignment_score": 80,
    })
    assert response.status_code == 400
