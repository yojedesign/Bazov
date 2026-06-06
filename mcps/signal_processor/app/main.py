"""
Signal Processor MCP - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import health, signals, entities, sentiment

# Create FastAPI app
app = FastAPI(
    title="Signal Processor MCP",
    description="NLP-based signal processing microservice for Bazov",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(signals.router, prefix="/api/v1/signals", tags=["signals"])
app.include_router(entities.router, prefix="/api/v1/entities", tags=["entities"])
app.include_router(sentiment.router, prefix="/api/v1/sentiment", tags=["sentiment"])

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "name": "Signal Processor MCP",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}
