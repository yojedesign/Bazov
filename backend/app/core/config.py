"""
Configuration settings using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field, AnyUrl
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Bazov"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    SECRET_KEY: str = Field(default="secret-key", env="SECRET_KEY")
    
    # Database
    # Using AnyUrl to support both PostgreSQL and SQLite URLs
    DATABASE_URL: AnyUrl = Field(
        default="postgresql://postgres:postgres@localhost:5432/bazov",
        env="DATABASE_URL"
    )
    
    # Supabase (optional)
    SUPABASE_URL: Optional[str] = Field(default=None, env="SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = Field(default=None, env="SUPABASE_KEY")
    
    # Clerk Authentication
    CLERK_SECRET_KEY: str = Field(default="", env="CLERK_SECRET_KEY")
    CLERK_WEBHOOK_SECRET: str = Field(default="", env="CLERK_WEBHOOK_SECRET")
    CLERK_PUBLISHABLE_KEY: Optional[str] = Field(default=None, env="CLERK_PUBLISHABLE_KEY")
    
    # CORS
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        env="CORS_ORIGINS"
    )
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    NEWS_API_KEY: Optional[str] = Field(default=None, env="NEWS_API_KEY")
    
    # Crawlers
    LINKEDIN_USERNAME: Optional[str] = Field(default=None, env="LINKEDIN_USERNAME")
    LINKEDIN_PASSWORD: Optional[str] = Field(default=None, env="LINKEDIN_PASSWORD")
    PROXY_URL: Optional[str] = Field(default=None, env="PROXY_URL")
    
    class Config:
        """Pydantic settings configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Lazy initialization of settings to allow environment overrides before import
_settings_instance = None


def get_settings():
    """
    Get the settings instance, creating it lazily on first access.
    This allows tests to set environment variables before settings are initialized.
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
        # Validate required settings
        if not _settings_instance.CLERK_SECRET_KEY and not _settings_instance.DEBUG:
            raise ValueError("CLERK_SECRET_KEY is required in production")
        if not _settings_instance.CLERK_WEBHOOK_SECRET and not _settings_instance.DEBUG:
            raise ValueError("CLERK_WEBHOOK_SECRET is required in production")
    return _settings_instance


def reset_settings():
    """
    Reset the settings instance. Useful for testing.
    """
    global _settings_instance
    _settings_instance = None


# For backward compatibility, settings is a proxy to get_settings()
# This ensures settings are initialized lazily
class _SettingsProxy:
    """Proxy to lazily access settings"""
    def __getattr__(self, name):
        return getattr(get_settings(), name)
    
    def __setattr__(self, name, value):
        return setattr(get_settings(), name, value)
    
    def __repr__(self):
        return repr(get_settings())


settings = _SettingsProxy()
