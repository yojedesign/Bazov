"""
Tests for configuration settings
"""

import pytest
import os


class TestSettings:
    """Tests for the Settings class"""
    
    def test_settings_load_from_environment(self, settings):
        """Test that settings can be loaded from environment variables"""
        assert settings.DEBUG is True
        assert settings.APP_NAME == "Bazov"
        assert settings.APP_VERSION == "0.1.0"
    
    def test_settings_default_values(self, settings):
        """Test that settings have expected default values"""
        assert settings.APP_NAME == "Bazov"
        assert settings.APP_VERSION == "0.1.0"
        assert settings.SECRET_KEY == "test-secret"
    
    def test_settings_database_url(self, settings):
        """Test that database URL is set correctly"""
        assert "sqlite" in str(settings.DATABASE_URL).lower() or "memory" in str(settings.DATABASE_URL).lower()
    
    def test_settings_clerk_keys(self, settings):
        """Test that Clerk keys are set"""
        assert settings.CLERK_SECRET_KEY == "test-secret-key"
        assert settings.CLERK_WEBHOOK_SECRET == "test-webhook-secret"


class TestSettingsValidation:
    """Tests for settings validation"""
    
    def test_settings_requires_clerk_keys_in_production(self):
        """Test that Clerk keys are required in production (non-debug mode)"""
        from app.core.config import get_settings, reset_settings
        
        # Reset settings to ensure clean state
        reset_settings()
        
        # Set environment to production mode
        old_debug = os.environ.get("DEBUG")
        old_clerk_key = os.environ.get("CLERK_SECRET_KEY")
        old_webhook = os.environ.get("CLERK_WEBHOOK_SECRET")
        
        try:
            os.environ["DEBUG"] = "false"
            os.environ["CLERK_SECRET_KEY"] = ""
            os.environ["CLERK_WEBHOOK_SECRET"] = ""
            
            # This should raise ValueError when accessing settings
            with pytest.raises(ValueError) as exc_info:
                settings = get_settings()
            
            assert "CLERK_SECRET_KEY is required in production" in str(exc_info.value)
        finally:
            # Restore environment
            reset_settings()
            if old_debug is not None:
                os.environ["DEBUG"] = old_debug
            else:
                os.environ.pop("DEBUG", None)
            if old_clerk_key is not None:
                os.environ["CLERK_SECRET_KEY"] = old_clerk_key
            else:
                os.environ.pop("CLERK_SECRET_KEY", None)
            if old_webhook is not None:
                os.environ["CLERK_WEBHOOK_SECRET"] = old_webhook
            else:
                os.environ.pop("CLERK_WEBHOOK_SECRET", None)
    
    def test_settings_allows_empty_clerk_keys_in_debug(self):
        """Test that empty Clerk keys are allowed in debug mode"""
        from app.core.config import get_settings, reset_settings
        
        # Reset settings to ensure clean state
        reset_settings()
        
        # Set environment to debug mode
        old_debug = os.environ.get("DEBUG")
        old_clerk_key = os.environ.get("CLERK_SECRET_KEY")
        old_webhook = os.environ.get("CLERK_WEBHOOK_SECRET")
        
        try:
            os.environ["DEBUG"] = "true"
            os.environ["CLERK_SECRET_KEY"] = ""
            os.environ["CLERK_WEBHOOK_SECRET"] = ""
            
            # This should not raise because DEBUG is True
            settings = get_settings()
            assert settings.DEBUG is True
        finally:
            # Restore environment
            reset_settings()
            if old_debug is not None:
                os.environ["DEBUG"] = old_debug
            else:
                os.environ.pop("DEBUG", None)
            if old_clerk_key is not None:
                os.environ["CLERK_SECRET_KEY"] = old_clerk_key
            else:
                os.environ.pop("CLERK_SECRET_KEY", None)
            if old_webhook is not None:
                os.environ["CLERK_WEBHOOK_SECRET"] = old_webhook
            else:
                os.environ.pop("CLERK_WEBHOOK_SECRET", None)
