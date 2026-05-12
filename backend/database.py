import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import uuid
import os
from backend.config import GOOGLE_SHEETS_CREDENTIALS_PATH, GOOGLE_SHEETS_SPREADSHEET_NAME

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

USERS_HEADERS = ["id", "username", "email", "password_hash", "created_at"]
PREDICTIONS_HEADERS = [
    "id", "user_id", "image_filename", "predicted_class", "predicted_label",
    "confidence", "all_probabilities", "gradcam_path", "created_at",
]
REPORTS_HEADERS = [
    "id", "prediction_id", "user_id", "patient_id", "report_path", "created_at",
]


class SheetsDB:
    def __init__(self):
        self._client = None
        self._spreadsheet = None

    def _connect(self):
        if self._client is not None:
            return
        if not os.path.exists(GOOGLE_SHEETS_CREDENTIALS_PATH):
            raise FileNotFoundError(
                f"Google Sheets credentials not found at {GOOGLE_SHEETS_CREDENTIALS_PATH}. "
                "Please create a service account and download the JSON key file."
            )
        creds = Credentials.from_service_account_file(
            GOOGLE_SHEETS_CREDENTIALS_PATH, scopes=SCOPES
        )
        self._client = gspread.authorize(creds)
        try:
            self._spreadsheet = self._client.open(GOOGLE_SHEETS_SPREADSHEET_NAME)
        except gspread.SpreadsheetNotFound:
            self._spreadsheet = self._client.create(GOOGLE_SHEETS_SPREADSHEET_NAME)
            self._spreadsheet.share("", perm_type="anyone", role="writer")
        self._ensure_worksheets()

    def _ensure_worksheets(self):
        existing = [ws.title for ws in self._spreadsheet.worksheets()]
        sheets_config = {
            "users": USERS_HEADERS,
            "predictions": PREDICTIONS_HEADERS,
            "reports": REPORTS_HEADERS,
        }
        for name, headers in sheets_config.items():
            if name not in existing:
                ws = self._spreadsheet.add_worksheet(title=name, rows=1000, cols=len(headers))
                ws.append_row(headers)
            else:
                ws = self._spreadsheet.worksheet(name)
                if not ws.row_values(1):
                    ws.append_row(headers)

    def _get_worksheet(self, name: str):
        self._connect()
        return self._spreadsheet.worksheet(name)

    # --- Users ---
    def get_user_by_email(self, email: str) -> dict | None:
        ws = self._get_worksheet("users")
        records = ws.get_all_records()
        for record in records:
            if record.get("email") == email:
                return record
        return None

    def get_user_by_username(self, username: str) -> dict | None:
        ws = self._get_worksheet("users")
        records = ws.get_all_records()
        for record in records:
            if record.get("username") == username:
                return record
        return None

    def get_user_by_id(self, user_id: str) -> dict | None:
        ws = self._get_worksheet("users")
        records = ws.get_all_records()
        for record in records:
            if record.get("id") == user_id:
                return record
        return None

    def create_user(self, username: str, email: str, password_hash: str) -> dict:
        ws = self._get_worksheet("users")
        user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow().isoformat(),
        }
        ws.append_row(list(user.values()))
        return user

    # --- Predictions ---
    def save_prediction(
        self,
        user_id: str,
        image_filename: str,
        predicted_class: int,
        predicted_label: str,
        confidence: float,
        all_probabilities: list,
        gradcam_path: str = "",
    ) -> dict:
        ws = self._get_worksheet("predictions")
        prediction = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "image_filename": image_filename,
            "predicted_class": predicted_class,
            "predicted_label": predicted_label,
            "confidence": round(confidence, 4),
            "all_probabilities": json.dumps([round(p, 4) for p in all_probabilities]),
            "gradcam_path": gradcam_path,
            "created_at": datetime.utcnow().isoformat(),
        }
        ws.append_row(list(prediction.values()))
        return prediction

    def get_user_predictions(self, user_id: str) -> list:
        ws = self._get_worksheet("predictions")
        records = ws.get_all_records()
        results = [r for r in records if r.get("user_id") == user_id]
        for r in results:
            if isinstance(r.get("all_probabilities"), str):
                try:
                    r["all_probabilities"] = json.loads(r["all_probabilities"])
                except (json.JSONDecodeError, TypeError):
                    pass
        return sorted(results, key=lambda x: x.get("created_at", ""), reverse=True)

    def get_all_predictions(self) -> list:
        ws = self._get_worksheet("predictions")
        records = ws.get_all_records()
        for r in records:
            if isinstance(r.get("all_probabilities"), str):
                try:
                    r["all_probabilities"] = json.loads(r["all_probabilities"])
                except (json.JSONDecodeError, TypeError):
                    pass
        return sorted(records, key=lambda x: x.get("created_at", ""), reverse=True)

    def get_prediction_by_id(self, prediction_id: str) -> dict | None:
        ws = self._get_worksheet("predictions")
        records = ws.get_all_records()
        for record in records:
            if record.get("id") == prediction_id:
                if isinstance(record.get("all_probabilities"), str):
                    try:
                        record["all_probabilities"] = json.loads(record["all_probabilities"])
                    except (json.JSONDecodeError, TypeError):
                        pass
                return record
        return None

    # --- Reports ---
    def save_report(self, prediction_id: str, user_id: str, patient_id: str, report_path: str) -> dict:
        ws = self._get_worksheet("reports")
        report = {
            "id": str(uuid.uuid4()),
            "prediction_id": prediction_id,
            "user_id": user_id,
            "patient_id": patient_id,
            "report_path": report_path,
            "created_at": datetime.utcnow().isoformat(),
        }
        ws.append_row(list(report.values()))
        return report

    def get_user_reports(self, user_id: str) -> list:
        ws = self._get_worksheet("reports")
        records = ws.get_all_records()
        return [r for r in records if r.get("user_id") == user_id]

    # --- Analytics ---
    def get_analytics(self) -> dict:
        predictions = self.get_all_predictions()
        users_ws = self._get_worksheet("users")
        total_users = max(len(users_ws.get_all_records()), 0)

        distribution = {i: 0 for i in range(5)}
        for p in predictions:
            cls = p.get("predicted_class", 0)
            if isinstance(cls, int) and 0 <= cls <= 4:
                distribution[cls] += 1

        recent = predictions[:10]
        return {
            "total_predictions": len(predictions),
            "total_users": total_users,
            "disease_distribution": distribution,
            "recent_predictions": recent,
        }


db = SheetsDB()
