from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


def create_application() -> FastAPI:
    """FastAPI Application Factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="Autonomous Adversarial Payment Security Lab API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS Middleware
    origins = settings.CORS_ORIGINS
    if isinstance(origins, str):
        origins = [origins]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", tags=["System"])
    def read_root():
        """Project identification root endpoint."""
        return {
            "name": settings.APP_NAME,
            "system": "Autonomous Adversarial Payment Security Lab",
            "version": "0.1.0",
            "status": "online",
            "docs": "/docs",
        }

    @app.get("/health", tags=["Health"])
    def read_health():
        """Root level health check endpoint."""
        return {"status": "ok"}

    @app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
    def read_api_v1_health():
        """API v1 health check endpoint."""
        return {"status": "ok"}

    from app.api.v1.digital_twin import router as digital_twin_router
    from app.api.v1.evaluation import router as evaluation_router
    from app.api.v1.explainability import router as explainability_router
    from app.api.v1.hardening import router as hardening_router
    from app.api.v1.orchestration import router as orchestration_router
    from app.api.v1.overview import router as overview_router
    from app.api.v1.red_team import router as red_team_router

    app.include_router(overview_router, prefix=settings.API_V1_STR)
    app.include_router(hardening_router, prefix=settings.API_V1_STR)
    app.include_router(explainability_router, prefix=settings.API_V1_STR)
    app.include_router(orchestration_router, prefix=settings.API_V1_STR)
    app.include_router(digital_twin_router, prefix=settings.API_V1_STR)
    app.include_router(red_team_router, prefix=settings.API_V1_STR)
    app.include_router(evaluation_router, prefix=settings.API_V1_STR)

    return app


app = create_application()
