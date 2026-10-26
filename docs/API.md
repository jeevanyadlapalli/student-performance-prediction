# REST API Reference

Base URL: `http://127.0.0.1:5000`

## `GET /api/health`
Reports whether the API is responding and whether the model file exists.

## `GET /api/stats`
Returns dataset row count, model evaluation metrics (if trained), and a synthetic-data note.

## `POST /api/predict`
JSON body:
```json
{
  "study_hours": 3,
  "attendance": 85,
  "previous_marks": 70,
  "assignment_score": 80
}
```
All four values are required. `study_hours` must be between 0.5 and 8; the other values must be between 0 and 100. A successful response contains `predicted_marks`, the input values, a timestamp, and an educational-use note. Invalid input returns HTTP 400. If the model is missing, returns HTTP 503.

## `GET /api/history`
Returns up to 20 latest predictions from the SQLite database.
