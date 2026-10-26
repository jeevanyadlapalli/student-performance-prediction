# Student Performance Prediction Using Machine Learning

## Abstract
This project demonstrates a full-stack machine-learning application that estimates exam marks from student study hours, attendance, previous exam marks, and assignment score. A Python model is exposed through a Flask REST API and consumed by a browser-based frontend. Prediction events are stored in SQLite for a simple history view.

## Problem statement
Students and educators may want to explore how study habits and prior academic indicators relate to exam outcomes. The application demonstrates a basic regression workflow that maps selected input features to a numeric estimate of marks.

## Objectives
1. Generate and inspect a structured dataset.
2. Train a regression model using scikit-learn.
3. Evaluate the model on a held-out test set.
4. Provide a user-friendly interface for predictions.
5. Expose prediction functionality through a REST API.
6. Store and display recent prediction history.

## Technology stack
- Python
- Pandas and NumPy
- scikit-learn
- Flask and Flask-CORS
- HTML, CSS, JavaScript
- SQLite

## Dataset and features
The project creates 600 synthetic records with four input features: study hours per day, attendance percentage, previous exam marks, and assignment score. The target variable is exam marks from 0 to 100. The target is generated from a simulated formula with random noise; it is not a real-world educational dataset.

## Methodology
1. Generate reproducible synthetic records with a fixed random seed.
2. Split records into training and test subsets (80%/20%).
3. Fit Linear Regression on the training data.
4. Evaluate on held-out data with MAE, RMSE, and R².
5. Save the trained model and metrics.
6. Accept validated JSON inputs through Flask.
7. Return a bounded estimate and save it to SQLite.
8. Display the estimate, model metrics, and history in the frontend.

## Evaluation
MAE is the average absolute difference between predicted and actual marks. RMSE penalizes larger errors more heavily. R² describes the proportion of target variance explained on the test split. Because the data is synthetic, these metrics only test whether the software workflow works on the generated data; they do not demonstrate accuracy on real students.

## Limitations and ethics
- The synthetic data does not represent real student populations.
- Features and target formula are intentionally simplified.
- Relationships learned from generated data may be misleading if interpreted as educational evidence.
- Predictions are uncertain and should not determine grades, placement, scholarships, or other high-stakes outcomes.
- Before real use, source a permissioned dataset, assess data quality and bias, validate with suitable splits, protect personal information, and clearly communicate uncertainty.

## Future enhancements
- Compare Linear Regression, Random Forest, and other suitable regressors.
- Add residual analysis and feature relationship visualizations.
- Replace synthetic data with a sourced dataset under appropriate terms.
- Add authentication and access control before multi-user deployment.
- Add database retention and privacy controls.
- Deploy behind a production web server with restricted CORS and secure configuration.

## Conclusion
The project demonstrates an end-to-end ML application: data generation, training, evaluation, API integration, frontend interaction, and database history. It is a learning prototype rather than a validated tool for predicting real student outcomes.
