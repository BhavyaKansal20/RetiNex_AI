# RetiNex AI API Documentation

**Base URL**: `http://localhost:8000/api`

---

## Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

### POST `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string (min 6 chars)"
}
```

**Response 200:**
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "username": "string",
    "email": "string"
  }
}
```

### POST `/auth/login`

Authenticate an existing user.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response 200:** Same as register.

### GET `/auth/me` 🔒

Get current user profile.

**Response 200:**
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "created_at": "iso_timestamp"
}
```

---

## Predictions

### POST `/predictions` 🔒

Upload a retinal image for DR prediction.

**Query Parameters:**
- `use_tta` (boolean, default: false) — Enable Test-Time Augmentation

**Request:** `multipart/form-data`
- `file` — Image file (PNG, JPG, JPEG, max 10MB)

**Response 200:**
```json
{
  "prediction_id": "uuid",
  "result": {
    "predicted_class": 2,
    "predicted_label": "Moderate",
    "confidence": 0.8742,
    "probabilities": {
      "No DR": 0.0523,
      "Mild": 0.0612,
      "Moderate": 0.8742,
      "Severe": 0.0098,
      "Proliferative DR": 0.0025
    },
    "probabilities_list": [0.0523, 0.0612, 0.8742, 0.0098, 0.0025]
  },
  "severity_description": "Moderate non-proliferative...",
  "severity_color": "#f97316",
  "gradcam": {
    "original": "base64_png_string",
    "heatmap": "base64_png_string",
    "overlay": "base64_png_string"
  }
}
```

### GET `/predictions` 🔒

Get all predictions for the authenticated user.

### GET `/predictions/{prediction_id}` 🔒

Get a specific prediction by ID.

---

## Reports

### POST `/reports/generate` 🔒

Generate a PDF report for a prediction.

**Request Body:**
```json
{
  "prediction_id": "uuid",
  "patient_id": "AUTO"  // or custom patient ID
}
```

**Response 200:**
```json
{
  "report_id": "uuid",
  "patient_id": "PAT-A1B2C3D4",
  "download_url": "/api/reports/<report_id>/download"
}
```

### GET `/reports/{report_id}/download` 🔒

Download a generated PDF report.

**Response:** `application/pdf` file

---

## Analytics

### GET `/analytics/overview` 🔒

Get platform-wide statistics.

**Response 200:**
```json
{
  "total_predictions": 42,
  "total_users": 5,
  "disease_distribution": {
    "No DR": 15,
    "Mild": 8,
    "Moderate": 12,
    "Severe": 5,
    "Proliferative DR": 2
  },
  "recent_predictions": [...]
}
```

### GET `/analytics/user-stats` 🔒

Get statistics for the authenticated user.

---

## Research

### GET `/research/metrics` 🔒

Get model evaluation metrics.

**Response 200:**
```json
{
  "classification_report": {...},
  "confusion_matrix": [[...]],
  "training_history": {"loss": [...], "accuracy": [...]},
  "per_class_metrics": {...},
  "class_names": ["No DR", "Mild", "Moderate", "Severe", "Proliferative DR"]
}
```

### GET `/research/model-info` 🔒

Get model architecture information.

---

## Health Check

### GET `/health`

No authentication required.

**Response 200:**
```json
{
  "status": "healthy",
  "service": "RetiNex AI"
}
```
