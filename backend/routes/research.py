import os
import json
from fastapi import APIRouter, Depends
from backend.auth import get_current_user
from backend.config import METRICS_DIR, CLASS_NAMES

router = APIRouter(prefix="/api/research", tags=["Research"])


def _load_json(filename: str) -> dict | list | None:
    filepath = os.path.join(METRICS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None


@router.get("/metrics")
def get_research_metrics(user: dict = Depends(get_current_user)):
    classification_report = _load_json("classification_report.json")
    confusion_matrix = _load_json("confusion_matrix.json")
    training_history = _load_json("training_history.json")
    per_class_metrics = _load_json("per_class_metrics.json")

    # Provide sample structure if files don't exist yet
    if classification_report is None:
        classification_report = {
            "accuracy": 0.0,
            "macro_avg": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0},
            "weighted_avg": {"precision": 0.0, "recall": 0.0, "f1-score": 0.0},
        }

    if confusion_matrix is None:
        confusion_matrix = [[0] * 5 for _ in range(5)]

    return {
        "classification_report": classification_report,
        "confusion_matrix": confusion_matrix,
        "training_history": training_history,
        "per_class_metrics": per_class_metrics,
        "class_names": CLASS_NAMES,
    }


@router.get("/model-info")
def get_model_info(user: dict = Depends(get_current_user)):
    return {
        "model_name": "EfficientNetV2-B0",
        "framework": "TensorFlow / Keras",
        "input_size": "299 × 299 × 3",
        "num_classes": 5,
        "class_names": CLASS_NAMES,
        "datasets": ["APTOS 2019", "IDRiD"],
        "preprocessing": [
            "Retinal cropping (contour-based)",
            "CLAHE enhancement (LAB color space)",
            "Gaussian blur (3×3)",
            "Aspect-ratio-preserving resize with zero-padding",
            "EfficientNetV2 preprocessing",
        ],
        "training_config": {
            "optimizer": "Adam",
            "learning_rate": "1e-4",
            "loss": "Categorical Crossentropy",
            "epochs": 15,
            "batch_size": 16,
            "callbacks": [
                "EarlyStopping (patience=5)",
                "ReduceLROnPlateau (factor=0.2, patience=2)",
                "ModelCheckpoint (best val_loss)",
            ],
        },
        "explainability": ["GradCAM", "Guided GradCAM"],
    }
