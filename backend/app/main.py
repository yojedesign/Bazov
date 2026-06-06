"""
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import auth, users, signals, relationships, health
from app.api.v1.ml import signals as ml_signals, relationships as ml_relationships, recommendations, anomalies, health as ml_health

# Create FastAPI app
app = FastAPI(
    title="Bazov API",
    description="Relationship Intelligence Platform API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(signals.router, prefix="/api/v1/signals", tags=["signals"])
app.include_router(relationships.router, prefix="/api/v1/relationships", tags=["relationships"])

# Include ML API routers
app.include_router(ml_signals.router, prefix="/api/v1/ml", tags=["ml", "signals"])
app.include_router(ml_relationships.router, prefix="/api/v1/ml", tags=["ml", "relationships"])
app.include_router(recommendations.router, prefix="/api/v1/ml", tags=["ml", "recommendations"])
app.include_router(anomalies.router, prefix="/api/v1/ml", tags=["ml", "anomalies"])
app.include_router(ml_health.router, prefix="/api/v1/ml", tags=["ml", "health"])

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "name": "Bazov API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }

# Health check endpoint (also available at /api/v1/health)
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}
