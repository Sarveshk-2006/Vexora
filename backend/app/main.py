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
        allow_origins=origins,
        allow_credentials=True,
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

    return app


app = create_application()
