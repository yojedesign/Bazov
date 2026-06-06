"""
Configuration settings using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn
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
    DATABASE_URL: PostgresDsn = Field(
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


# Create settings instance
settings = Settings()

# Validate required settings
if not settings.CLERK_SECRET_KEY and not settings.DEBUG:
    raise ValueError("CLERK_SECRET_KEY is required in production")

if not settings.CLERK_WEBHOOK_SECRET and not settings.DEBUG:
    raise ValueError("CLERK_WEBHOOK_SECRET is required in production")
