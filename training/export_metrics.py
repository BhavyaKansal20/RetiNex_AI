"""Export training history and evaluation metrics to JSON for the research dashboard."""

import json
import os
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from backend.config import CLASS_NAMES

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "evaluation", "results")


def export_training_history(history, output_dir=RESULTS_DIR):
    """Export Keras training history to JSON."""
    os.makedirs(output_dir, exist_ok=True)
    history_dict = {}
    for key, values in history.history.items():
        history_dict[key] = [float(v) for v in values]
    filepath = os.path.join(output_dir, "training_history.json")
    with open(filepath, "w") as f:
        json.dump(history_dict, f, indent=2)
    return filepath


def export_evaluation_metrics(y_true, y_pred, y_pred_proba=None, output_dir=RESULTS_DIR):
    """Export evaluation metrics to JSON files."""
    os.makedirs(output_dir, exist_ok=True)

    # Classification report
    report = classification_report(
        y_true, y_pred,
        target_names=CLASS_NAMES,
        output_dict=True,
        zero_division=0,
    )
    with open(os.path.join(output_dir, "classification_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred).tolist()
    with open(os.path.join(output_dir, "confusion_matrix.json"), "w") as f:
        json.dump(cm, f, indent=2)

    # Per-class metrics
    per_class = {}
    for i, name in enumerate(CLASS_NAMES):
        if name in report:
            per_class[name] = {
                "precision": round(report[name]["precision"], 4),
                "recall": round(report[name]["recall"], 4),
                "f1_score": round(report[name]["f1-score"], 4),
                "support": int(report[name]["support"]),
            }
    with open(os.path.join(output_dir, "per_class_metrics.json"), "w") as f:
        json.dump(per_class, f, indent=2)

    # ROC-AUC if probabilities are available
    if y_pred_proba is not None:
        try:
            from sklearn.preprocessing import label_binarize
            y_true_bin = label_binarize(y_true, classes=list(range(len(CLASS_NAMES))))
            auc_scores = {}
            for i, name in enumerate(CLASS_NAMES):
                try:
                    auc = roc_auc_score(y_true_bin[:, i], y_pred_proba[:, i])
                    auc_scores[name] = round(float(auc), 4)
                except ValueError:
                    auc_scores[name] = None
            with open(os.path.join(output_dir, "roc_auc.json"), "w") as f:
                json.dump(auc_scores, f, indent=2)
        except Exception:
            pass

    return output_dir
