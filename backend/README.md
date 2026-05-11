# Backend Directory

## Purpose
Flask API server and business logic.

## Contents
- **app.py**: Main Flask application (moved to root)
- **routes.py**: API endpoints
- **database.py**: Google Sheets integration with gspread
- **auth.py**: User authentication
- **prediction.py**: Model prediction logic
- **report_generator.py**: AI-generated clinical reports

## API Endpoints
- `/predict`: Run model on uploaded image
- `/register`: User registration
- `/login`: User login
- `/history`: Prediction history
- `/report`: Generated clinical report

## Database
- Google Sheets via gspread API
- Tables:
  - users (registration, credentials)
  - predictions (image, result, timestamp)
  - reports (generated clinical reports)
