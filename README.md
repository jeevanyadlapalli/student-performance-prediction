# Student Performance Prediction — Full Development Project

A complete beginner-friendly full-stack ML project.

## Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Flask REST API
- Machine learning: scikit-learn Linear Regression
- Data processing: Pandas and NumPy
- Database: SQLite
- Testing: pytest

## Features
- Generates 600 reproducible synthetic student records
- Trains and evaluates a regression model
- Saves the trained model and evaluation metrics
- Responsive dashboard with input sliders
- Predict marks from study hours, attendance, previous marks, assignment score
- Input validation and helpful error messages
- Saves prediction history in SQLite
- API endpoints for health, metrics, prediction, and history
- Automated backend tests
- Project report and API documentation

> **Data limitation:** The included dataset is synthetic and is intended only to demonstrate the software workflow. Its metrics do not indicate accuracy on real students. Use a suitable, permissioned real dataset for any meaningful research evaluation. Do not use predictions as the sole basis for high-stakes academic decisions.

## Requirements
- Python 3.10+
- VS Code recommended

## Windows setup (PowerShell)

1. Extract this ZIP.
2. Open the extracted `student_performance_prediction_full_development` folder in VS Code.
3. Open a terminal and run:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python generate_data.py
python train_model.py
python app.py
```

If PowerShell blocks virtual-environment activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```
If `python` is unavailable, try `py` instead.

4. Keep the backend terminal running. Open a second terminal at the project root:

```powershell
cd frontend
python -m http.server 8080
```

5. Open http://localhost:8080 in your browser.

The frontend runs on port 8080 and the backend API runs on port 5000. Both servers must stay running while using the application.

## Run automated tests
With the backend virtual environment active, from the project root:

```powershell
pip install -r backend/requirements.txt
python -m pytest
```

The tests exercise input validation and the prediction API. Generate the dataset and train the model before running the full suite.

## API
See `docs/API.md` for request examples and endpoints.

## Project report
See `docs/PROJECT_REPORT.md` for abstract, objectives, methodology, implementation, limitations, and future work.

## Troubleshooting
- `Model not trained`: from `backend`, run `python generate_data.py` then `python train_model.py`.
- `Failed to fetch`: make sure the Flask server is running and open the frontend via `http://localhost:8080`, not by double-clicking the HTML file.
- Port already in use: change the backend port in `backend/app.py` and `API_BASE` in `frontend/app.js`.
- PowerShell activation blocked: use Command Prompt, or run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the current terminal if permitted by your device policy.
