"""Flask REST API and SQLite history for the Student Performance Predictor."""
from pathlib import Path
import json
import sqlite3
from datetime import datetime, timezone

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "student_marks_model.joblib"
METRICS_PATH = ROOT / "models" / "metrics.json"
DATA_PATH = ROOT / "data" / "student_data.csv"
DB_PATH = ROOT / "predictions.db"

FEATURES = ["study_hours", "attendance", "previous_marks", "assignment_score"]
LIMITS = {
    "study_hours": (0.5, 8.0),
    "attendance": (0.0, 100.0),
    "previous_marks": (0.0, 100.0),
    "assignment_score": (0.0, 100.0),
}

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(test_config or {})
    CORS(app, resources={r"/api/*": {"origins": "*"}})  # Local demo only; restrict in deployment.
    db_path = Path(app.config.get("DB_PATH", DB_PATH))

    def init_db():
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(db_path) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    study_hours REAL NOT NULL,
                    attendance REAL NOT NULL,
                    previous_marks REAL NOT NULL,
                    assignment_score REAL NOT NULL,
                    predicted_marks REAL NOT NULL
                )
            """)
            con.commit()

    def read_model():
        path = Path(app.config.get("MODEL_PATH", MODEL_PATH))
        return joblib.load(path) if path.exists() else None

    def read_metrics():
        path = Path(app.config.get("METRICS_PATH", METRICS_PATH))
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    @app.get("/api/health")
    def health():
        return jsonify({
            "status": "ok",
            "model_loaded": Path(app.config.get("MODEL_PATH", MODEL_PATH)).exists(),
            "message": "Student Performance Prediction API is running"
        })

    @app.get("/api/stats")
    def stats():
        data_path = Path(app.config.get("DATA_PATH", DATA_PATH))
        rows = int(len(pd.read_csv(data_path))) if data_path.exists() else 0
        return jsonify({
            "dataset_rows": rows,
            "metrics": read_metrics(),
            "dataset_note": "Synthetic educational data only"
        })

    @app.post("/api/predict")
    def predict():
        bundle = read_model()
        if bundle is None:
            return jsonify({"error": "Model is not trained. Run generate_data.py and train_model.py in backend."}), 503

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        values = {}
        for field in FEATURES:
            if field not in payload:
                return jsonify({"error": f"Missing required field: {field}"}), 400
            try:
                value = float(payload[field])
            except (TypeError, ValueError):
                return jsonify({"error": f"{field} must be a number."}), 400
            lo, hi = LIMITS[field]
            if not (lo <= value <= hi):
                return jsonify({"error": f"{field} must be between {lo} and {hi}."}), 400
            values[field] = value

        input_df = pd.DataFrame([values], columns=bundle["features"])
        predicted = float(bundle["model"].predict(input_df)[0])
        predicted = round(max(0.0, min(100.0, predicted)), 1)
        timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

        init_db()
        with sqlite3.connect(db_path) as con:
            cur = con.execute("""
                INSERT INTO predictions
                (created_at, study_hours, attendance, previous_marks, assignment_score, predicted_marks)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, values["study_hours"], values["attendance"],
                  values["previous_marks"], values["assignment_score"], predicted))
            prediction_id = cur.lastrowid
            con.commit()

        return jsonify({
            "id": prediction_id,
            "created_at": timestamp,
            "predicted_marks": predicted,
            "out_of": 100,
            "inputs": values,
            "note": "Estimate based on synthetic demo data; not a guarantee."
        })

    @app.get("/api/history")
    def history():
        init_db()
        with sqlite3.connect(db_path) as con:
            con.row_factory = sqlite3.Row
            rows = con.execute("""
                SELECT id, created_at, study_hours, attendance, previous_marks,
                       assignment_score, predicted_marks
                FROM predictions ORDER BY id DESC LIMIT 20
            """).fetchall()
        return jsonify({"history": [dict(row) for row in rows]})

    return app

app = create_app()

if __name__ == "__main__":
    print("API: http://127.0.0.1:5000")
    print("Run generate_data.py and train_model.py before making predictions.")
    app.run(host="127.0.0.1", port=5000, debug=True)
