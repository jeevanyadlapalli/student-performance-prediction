"""Train, evaluate, and save the student marks regression model."""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "student_data.csv"
MODEL_PATH = ROOT / "models" / "student_marks_model.joblib"
METRICS_PATH = ROOT / "models" / "metrics.json"
FEATURES = ["study_hours", "attendance", "previous_marks", "assignment_score"]

def train():
    if not DATA_PATH.exists():
        raise FileNotFoundError("Dataset not found. Run `python generate_data.py` first.")
    df = pd.read_csv(DATA_PATH)
    missing = set(FEATURES + ["exam_marks"]) - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("Dataset is empty.")

    X = df[FEATURES]
    y = df["exam_marks"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    metrics = {
        "model": "Linear Regression",
        "dataset_rows": int(len(df)),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "mae": round(float(mean_absolute_error(y_test, pred)), 3),
        "rmse": round(float(mean_squared_error(y_test, pred) ** 0.5), 3),
        "r2": round(float(r2_score(y_test, pred)), 4),
        "dataset_note": "Synthetic educational data; not real-world validation."
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics

if __name__ == "__main__":
    result = train()
    print("Training completed.")
    print(json.dumps(result, indent=2))
    print(f"Saved model: {MODEL_PATH}")
