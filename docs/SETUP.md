# RetiNex AI — Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+
- Google Cloud account (for Google Sheets API)

---

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/RetiNex_AI.git
cd "RetiNex AI"
```

## 2. Backend Setup

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable the **Google Sheets API** and **Google Drive API**
4. Go to **Credentials** → **Create Credentials** → **Service Account**
5. Download the JSON key file
6. Place it at `backend/credentials/service_account.json`
7. Create a Google Spreadsheet named `RetiNexAI_Database`
8. Share the spreadsheet with the service account email (found in the JSON file)

### Set up environment variables

```bash
cp .env.example .env
# Edit .env with your values
```

### Place your trained model

Ensure `models/best_model.keras` exists. If not, train the model first:

```bash
python -m training.train
```

### Run the backend

```bash
python app.py
# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

## 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Frontend available at http://localhost:5173
```

## 4. Full Stack Development

Run both servers simultaneously:

**Terminal 1 (Backend):**
```bash
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend && npm run dev
```

The frontend Vite dev server proxies `/api` requests to the FastAPI backend.

## 5. Docker Deployment

```bash
docker build -t retinexai .
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/backend/credentials:/app/backend/credentials \
  retinexai
```

## 6. Export Research Metrics

After training and evaluation, export metrics for the research dashboard:

```python
from training.export_metrics import export_training_history, export_evaluation_metrics

# After training
export_training_history(history)

# After evaluation
export_evaluation_metrics(y_true, y_pred, y_pred_proba)
```

## 7. HuggingFace Spaces Deployment

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select **Docker** as the SDK
3. Push the repository to the Space
4. Set secrets for `GOOGLE_SHEETS_CREDENTIALS` and `JWT_SECRET`
5. Upload `best_model.keras` to the Space's persistent storage
