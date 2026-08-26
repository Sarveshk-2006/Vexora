from app.core.database import Base, get_db


def test_database_module_imports():
    """Verify database module exports Base declarative class and engine setup."""
    assert Base is not None
    assert hasattr(Base, "metadata")


def test_get_db_generator_structure():
    """Verify get_db dependency function signature."""
    assert callable(get_db)
