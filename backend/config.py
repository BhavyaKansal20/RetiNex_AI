import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Model
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "best_model.keras"))
IMAGE_SIZE = 299
NUM_CLASSES = 5
CLASS_NAMES = ["No DR", "Mild", "Moderate", "Severe", "Proliferative DR"]
SEVERITY_DESCRIPTIONS = {
    0: "No signs of diabetic retinopathy detected. Regular annual screening recommended.",
    1: "Mild non-proliferative diabetic retinopathy. Microaneurysms detected. Follow-up in 9-12 months.",
    2: "Moderate non-proliferative diabetic retinopathy. Multiple microaneurysms, dot/blot hemorrhages. Refer to ophthalmologist within 3-6 months.",
    3: "Severe non-proliferative diabetic retinopathy. Extensive hemorrhages, venous beading, IRMA. Urgent referral to retinal specialist.",
    4: "Proliferative diabetic retinopathy. Neovascularization detected. Immediate referral for laser treatment or vitrectomy.",
}
SEVERITY_COLORS = {
    0: "#22c55e",
    1: "#eab308",
    2: "#f97316",
    3: "#ef4444",
    4: "#dc2626",
}

# JWT Authentication
JWT_SECRET = os.getenv("JWT_SECRET", "retinex-ai-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_SHEETS_CREDENTIALS",
    str(BASE_DIR / "backend" / "credentials" / "service_account.json"),
)
GOOGLE_SHEETS_SPREADSHEET_NAME = os.getenv("GOOGLE_SHEETS_NAME", "RetiNexAI_Database")

# Uploads
UPLOAD_DIR = str(BASE_DIR / "uploads")
REPORTS_DIR = str(BASE_DIR / "generated_reports")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# Research metrics
METRICS_DIR = str(BASE_DIR / "evaluation" / "results")
