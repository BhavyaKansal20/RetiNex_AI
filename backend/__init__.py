from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.config import ALLOWED_ORIGINS


def create_app() -> FastAPI:
    app = FastAPI(
        title="RetiNex AI",
        description="Explainable Diabetic Retinopathy Screening API",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    from backend.auth import router as auth_router
    from backend.routes.prediction import router as prediction_router
    from backend.routes.analytics import router as analytics_router
    from backend.routes.research import router as research_router
    from backend.routes.reports import router as reports_router

    app.include_router(auth_router)
    app.include_router(prediction_router)
    app.include_router(analytics_router)
    app.include_router(research_router)
    app.include_router(reports_router)

    # Serve uploaded images
    from backend.config import UPLOAD_DIR
    if os.path.exists(UPLOAD_DIR):
        app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

    @app.get("/api/health")
    def health_check():
        return {"status": "healthy", "service": "RetiNex AI"}

    return app
