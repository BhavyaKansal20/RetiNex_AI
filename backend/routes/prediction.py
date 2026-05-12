import os
import base64
import uuid
import cv2
import numpy as np
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from backend.auth import get_current_user
from backend.database import db
from backend.services import inference_service
from backend.config import UPLOAD_DIR, CLASS_NAMES, SEVERITY_DESCRIPTIONS, SEVERITY_COLORS
from explainability.gradcam import compute_gradcam, generate_heatmap, generate_overlay

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])


def _encode_image_base64(image: np.ndarray) -> str:
    """Encode a numpy RGB image to a base64 PNG string."""
    rgb_to_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode(".png", rgb_to_bgr)
    return base64.b64encode(buffer).decode("utf-8")


@router.post("")
async def predict(
    file: UploadFile = File(...),
    use_tta: bool = Query(False, description="Enable Test-Time Augmentation"),
    user: dict = Depends(get_current_user),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 10MB)")

    # Save uploaded image
    ext = os.path.splitext(file.filename or "image.png")[1] or ".png"
    image_id = str(uuid.uuid4())
    saved_filename = f"{image_id}{ext}"
    saved_path = os.path.join(UPLOAD_DIR, saved_filename)
    with open(saved_path, "wb") as f:
        f.write(image_bytes)

    # Preprocess
    try:
        processed_image = inference_service.preprocess_image(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Predict
    if use_tta:
        result = inference_service.predict_with_tta(processed_image)
    else:
        result = inference_service.predict(processed_image)

    # GradCAM
    try:
        cam = compute_gradcam(
            inference_service.model,
            processed_image,
            class_idx=result["predicted_class"],
        )
        heatmap = generate_heatmap(cam)
        overlay = generate_overlay(processed_image, cam)

        gradcam_data = {
            "original": _encode_image_base64(processed_image),
            "heatmap": _encode_image_base64(heatmap),
            "overlay": _encode_image_base64(overlay),
        }
    except Exception:
        gradcam_data = None

    # Save prediction to database
    prediction_record = db.save_prediction(
        user_id=user["id"],
        image_filename=saved_filename,
        predicted_class=result["predicted_class"],
        predicted_label=result["predicted_label"],
        confidence=result["confidence"],
        all_probabilities=result["probabilities_list"],
    )

    return {
        "prediction_id": prediction_record["id"],
        "result": result,
        "severity_description": SEVERITY_DESCRIPTIONS.get(result["predicted_class"], ""),
        "severity_color": SEVERITY_COLORS.get(result["predicted_class"], "#6b7280"),
        "gradcam": gradcam_data,
    }


@router.get("")
def get_predictions(user: dict = Depends(get_current_user)):
    predictions = db.get_user_predictions(user["id"])
    return {"predictions": predictions}


@router.get("/{prediction_id}")
def get_prediction(prediction_id: str, user: dict = Depends(get_current_user)):
    prediction = db.get_prediction_by_id(prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    if prediction.get("user_id") != user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return {"prediction": prediction}
