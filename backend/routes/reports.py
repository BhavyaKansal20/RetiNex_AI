import os
import uuid
import cv2
import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.auth import get_current_user
from backend.database import db
from backend.services import inference_service
from backend.services.report_generator import generate_report
from backend.config import UPLOAD_DIR, REPORTS_DIR
from explainability.gradcam import compute_gradcam, generate_heatmap, generate_overlay

router = APIRouter(prefix="/api/reports", tags=["Reports"])


class ReportRequest(BaseModel):
    prediction_id: str
    patient_id: str = "AUTO"


@router.post("/generate")
def generate_patient_report(request: ReportRequest, user: dict = Depends(get_current_user)):
    prediction = db.get_prediction_by_id(request.prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    if prediction.get("user_id") != user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    patient_id = request.patient_id
    if patient_id == "AUTO":
        patient_id = f"PAT-{uuid.uuid4().hex[:8].upper()}"

    # Reload the uploaded image for report visualization
    image_filename = prediction.get("image_filename", "")
    image_path = os.path.join(UPLOAD_DIR, image_filename)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Original image not found")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    processed_image = inference_service.preprocess_image(image_bytes)
    predicted_class = prediction.get("predicted_class", 0)
    if isinstance(predicted_class, str):
        predicted_class = int(predicted_class)

    # Generate GradCAM visualizations
    try:
        cam = compute_gradcam(inference_service.model, processed_image, class_idx=predicted_class)
        heatmap = generate_heatmap(cam)
        overlay = generate_overlay(processed_image, cam)
    except Exception:
        heatmap = np.zeros_like(processed_image)
        overlay = processed_image.copy()

    # Build prediction dict for the report
    probs = prediction.get("all_probabilities", [])
    if isinstance(probs, str):
        import json
        try:
            probs = json.loads(probs)
        except (json.JSONDecodeError, TypeError):
            probs = [0.0] * 5

    from backend.config import CLASS_NAMES
    pred_dict = {
        "predicted_class": predicted_class,
        "predicted_label": prediction.get("predicted_label", ""),
        "confidence": float(prediction.get("confidence", 0)),
        "probabilities": {CLASS_NAMES[i]: float(probs[i]) if i < len(probs) else 0.0 for i in range(5)},
    }

    report_id = str(uuid.uuid4())[:12]
    filepath = generate_report(
        patient_id=patient_id,
        prediction=pred_dict,
        original_image=processed_image,
        heatmap_image=heatmap,
        overlay_image=overlay,
        report_id=report_id,
    )

    # Save report record
    report_record = db.save_report(
        prediction_id=request.prediction_id,
        user_id=user["id"],
        patient_id=patient_id,
        report_path=filepath,
    )

    return {
        "report_id": report_record["id"],
        "patient_id": patient_id,
        "download_url": f"/api/reports/{report_record['id']}/download",
    }


@router.get("/{report_id}/download")
def download_report(report_id: str, user: dict = Depends(get_current_user)):
    reports = db.get_user_reports(user["id"])
    report = next((r for r in reports if r.get("id") == report_id), None)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    filepath = report.get("report_path", "")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Report file not found on disk")

    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=os.path.basename(filepath),
    )
