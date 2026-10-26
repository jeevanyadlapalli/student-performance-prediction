"""Generate a reproducible synthetic dataset for the project demo."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "student_data.csv"

def generate_dataset(n: int = 600, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    study_hours = rng.uniform(0.5, 8.0, n).round(1)
    attendance = rng.uniform(45, 100, n).round(1)
    previous_marks = rng.uniform(25, 98, n).round(1)
    assignment_score = rng.uniform(30, 100, n).round(1)
    noise = rng.normal(0, 5, n)
    # Simulated relationship for educational demonstration only.
    exam_marks = (
        8 + 2.8 * study_hours + 0.18 * attendance
        + 0.35 * previous_marks + 0.20 * assignment_score + noise
    )
    exam_marks = np.clip(exam_marks, 0, 100).round(1)
    return pd.DataFrame({
        "study_hours": study_hours,
        "attendance": attendance,
        "previous_marks": previous_marks,
        "assignment_score": assignment_score,
        "exam_marks": exam_marks,
    })

def main():
    df = generate_dataset()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Generated {len(df)} synthetic records: {OUT}")
    print(df.head().to_string(index=False))
    print("\\nReminder: these are synthetic demo data, not real student records.")

if __name__ == "__main__":
    main()
