"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any

from app.core.config import settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME,
        "debug": settings.DEBUG,
    }


@router.get("/db", response_model=Dict[str, Any])
async def db_health_check() -> Dict[str, Any]:
    """
    Database health check endpoint
    
    Returns:
        dict: Database health status
    """
    try:
        from app.db.session import async_engine
        from sqlalchemy import text
        
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            await conn.commit()
        
        return {
            "status": "healthy",
            "database": "connected",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }


@router.get("/full", response_model=Dict[str, Any])
async def full_health_check() -> Dict[str, Any]:
    """
    Full health check endpoint with all dependencies
    
    Returns:
        dict: Full health status
    """
    health_status = {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME,
        "debug": settings.DEBUG,
        "checks": {},
    }
    
    # Check database
    try:
        from app.db.session import async_engine
        from sqlalchemy import text
        
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            await conn.commit()
        
        health_status["checks"]["database"] = {"status": "healthy"}
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e),
        }
    
    # Check Clerk (if configured)
    if settings.CLERK_SECRET_KEY:
        try:
            # Simple check - we can't really verify Clerk without making an API call
            health_status["checks"]["clerk"] = {"status": "configured"}
        except Exception as e:
            health_status["checks"]["clerk"] = {
                "status": "unhealthy",
                "error": str(e),
            }
    else:
        health_status["checks"]["clerk"] = {"status": "not_configured"}
    
    return health_status
