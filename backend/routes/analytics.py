from fastapi import APIRouter, Depends
from backend.auth import get_current_user
from backend.database import db
from backend.config import CLASS_NAMES, SEVERITY_COLORS

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/overview")
def get_analytics_overview(user: dict = Depends(get_current_user)):
    analytics = db.get_analytics()

    # Map distribution keys to labels
    distribution_labeled = {}
    for cls_idx, count in analytics["disease_distribution"].items():
        idx = int(cls_idx) if isinstance(cls_idx, str) else cls_idx
        if 0 <= idx < len(CLASS_NAMES):
            distribution_labeled[CLASS_NAMES[idx]] = count

    return {
        "total_predictions": analytics["total_predictions"],
        "total_users": analytics["total_users"],
        "disease_distribution": distribution_labeled,
        "disease_distribution_colors": {
            CLASS_NAMES[i]: SEVERITY_COLORS[i] for i in range(len(CLASS_NAMES))
        },
        "recent_predictions": analytics["recent_predictions"][:10],
    }


@router.get("/user-stats")
def get_user_stats(user: dict = Depends(get_current_user)):
    predictions = db.get_user_predictions(user["id"])
    reports = db.get_user_reports(user["id"])

    user_distribution = {name: 0 for name in CLASS_NAMES}
    for p in predictions:
        label = p.get("predicted_label", "")
        if label in user_distribution:
            user_distribution[label] += 1

    return {
        "total_predictions": len(predictions),
        "total_reports": len(reports),
        "disease_distribution": user_distribution,
        "recent_predictions": predictions[:5],
    }
