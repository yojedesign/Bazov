"""
Pytest configuration and fixtures for Bazov API tests
"""

import pytest
from fastapi.testclient import TestClient
import os
import sys

# Set environment variables BEFORE any imports
os.environ["DEBUG"] = "true"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["CLERK_SECRET_KEY"] = "test-secret-key"
os.environ["CLERK_WEBHOOK_SECRET"] = "test-webhook-secret"
os.environ["SECRET_KEY"] = "test-secret"

# Add the app directory to the path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def test_client():
    """
    Create a TestClient instance for the FastAPI app.
    This allows testing endpoints without running a live server.
    """
    from app.main import app
    
    with TestClient(app) as client:
        yield client


@pytest.fixture
def settings():
    """
    Provide access to settings with test overrides.
    """
    from app.core.config import Settings
    
    # Create test settings
    test_settings = Settings(
        DEBUG=True,
        DATABASE_URL="sqlite+aiosqlite:///:memory:",
        CLERK_SECRET_KEY="test-secret-key",
        CLERK_WEBHOOK_SECRET="test-webhook-secret",
        SECRET_KEY="test-secret",
        CORS_ORIGINS="http://localhost:3000",
    )
    return test_settings
