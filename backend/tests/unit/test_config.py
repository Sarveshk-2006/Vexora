from app.core.config import Settings


def test_default_settings():
    """Test default settings initialization."""
    settings = Settings()
    assert settings.APP_NAME == "FRAUDOSCOPE"
    assert settings.APP_ENV == "development"
    assert settings.DEBUG is True
    assert settings.RANDOM_SEED == 42
    assert "http://localhost:5173" in settings.CORS_ORIGINS


def test_cors_origins_parsing():
    """Test comma-separated string parsing for CORS_ORIGINS."""
    settings = Settings(CORS_ORIGINS="http://localhost:5173, http://127.0.0.1:5173")
    assert isinstance(settings.CORS_ORIGINS, list)
    assert len(settings.CORS_ORIGINS) == 2
    assert "http://localhost:5173" in settings.CORS_ORIGINS
    assert "http://127.0.0.1:5173" in settings.CORS_ORIGINS
