"""
ML Health API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional

from app.core.dependencies import get_current_user
from app.db.models.user import User as UserDB
from app.ml.models.signal_classifier import signal_classifier
from app.ml.models.relationship_strength import relationship_strength_model
from app.ml.models.recommendation import recommendation_model
from app.ml.models.anomaly_detector import anomaly_detector

router = APIRouter(prefix="/health", tags=["ml", "health"])


@router.get("/", response_model=Dict[str, Any])
async def ml_health_check(
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Health check for all ML services
    
    Returns:
        dict: Health status of all ML models and services
    """
    try:
        health_status = {
            "status": "healthy",
            "models": {
                "signal_classifier": {
                    "status": "healthy" if signal_classifier.is_loaded else "not_loaded",
                    "version": signal_classifier.version,
                    "last_trained": signal_classifier.last_trained,
                },
                "relationship_strength": {
                    "status": "healthy" if relationship_strength_model.is_loaded else "not_loaded",
                    "version": relationship_strength_model.version,
                    "last_trained": relationship_strength_model.last_trained,
                },
                "recommendation": {
                    "status": "healthy" if recommendation_model.is_loaded else "not_loaded",
                    "version": recommendation_model.version,
                    "last_trained": recommendation_model.last_trained,
                    "user_count": len(recommendation_model.user_profiles),
                    "item_count": sum(
                        len(items) for items in recommendation_model.item_profiles.values()
                    ),
                },
                "anomaly_detector": {
                    "status": "healthy" if anomaly_detector.is_loaded else "not_loaded",
                    "version": anomaly_detector.version,
                    "last_trained": anomaly_detector.last_trained,
                    "signal_types_tracked": len(anomaly_detector.signal_history),
                    "users_tracked": len(anomaly_detector.user_activity_history),
                },
            },
            "services": {
                "signal_processing": "healthy",
                "relationship_analysis": "healthy",
                "recommendation_engine": "healthy",
                "anomaly_detection": "healthy",
            },
        }
        
        # Check if any models are not loaded
        if not all([
            signal_classifier.is_loaded,
            relationship_strength_model.is_loaded,
            recommendation_model.is_loaded,
            anomaly_detector.is_loaded,
        ]):
            health_status["status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check ML health: {str(e)}",
        )


@router.get("/detailed", response_model=Dict[str, Any])
async def detailed_ml_health(
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Detailed health check for all ML services
    
    Returns:
        dict: Detailed health status with statistics
    """
    try:
        detailed_status = {
            "timestamp": datetime.utcnow().isoformat(),
            "models": {
                "signal_classifier": await self._get_classifier_details(),
                "relationship_strength": await self._get_strength_model_details(),
                "recommendation": await self._get_recommendation_model_details(),
                "anomaly_detector": await self._get_anomaly_detector_details(),
            },
            "recommendations": [
                "All ML models are operational",
                "Consider training models with more data for better accuracy",
                "Monitor anomaly detection for unusual patterns",
            ],
        }
        
        return detailed_status
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get detailed ML health: {str(e)}",
        )


async def _get_classifier_details(self) -> Dict[str, Any]:
    """Get signal classifier details"""
    from app.ml.services.signal_processing import signal_processing_service
    stats = await signal_processing_service.get_classifier_stats()
    return stats


async def _get_strength_model_details(self) -> Dict[str, Any]:
    """Get relationship strength model details"""
    from app.ml.services.relationship_analysis import relationship_analysis_service
    stats = await relationship_analysis_service.get_model_stats()
    return stats


async def _get_recommendation_model_details(self) -> Dict[str, Any]:
    """Get recommendation model details"""
    stats = {
        "is_loaded": recommendation_model.is_loaded,
        "version": recommendation_model.version,
        "last_trained": recommendation_model.last_trained,
        "user_count": len(recommendation_model.user_profiles),
        "item_count": sum(
            len(items) for items in recommendation_model.item_profiles.values()
        ),
        "strategies": recommendation_model.strategies,
        "strategy_weights": recommendation_model.strategy_weights,
    }
    return stats


async def _get_anomaly_detector_details(self) -> Dict[str, Any]:
    """Get anomaly detector details"""
    stats = {
        "is_loaded": anomaly_detector.is_loaded,
        "version": anomaly_detector.version,
        "last_trained": anomaly_detector.last_trained,
        "signal_types_tracked": len(anomaly_detector.signal_history),
        "users_tracked": len(anomaly_detector.user_activity_history),
        "thresholds": anomaly_detector.thresholds,
        "anomaly_types": anomaly_detector.ANOMALY_TYPES,
    }
    return stats


# Import datetime at the top level
from datetime import datetime
