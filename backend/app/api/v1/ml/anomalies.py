"""
ML Anomaly Detection API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional

from app.core.dependencies import get_current_user, get_db, AsyncSession
from app.db.models.user import User as UserDB
from app.ml.models.anomaly_detector import anomaly_detector

router = APIRouter(prefix="/anomalies", tags=["ml", "anomalies"])


@router.post("/detect-signal", response_model=Dict[str, Any])
async def detect_signal_anomalies(
    signal_type: Optional[str] = None,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Detect anomalies in signal patterns
    
    Args:
        signal_type: Optional specific signal type to check
        
    Returns:
        dict: List of detected signal anomalies
    """
    try:
        if signal_type:
            # Record a signal for the specified type
            anomaly_detector.record_signal(signal_type)
            anomalies = anomaly_detector.detect_signal_anomalies()
            # Filter for the specific signal type
            anomalies = [a for a in anomalies if a.get("signal_type") == signal_type]
        else:
            anomalies = anomaly_detector.detect_signal_anomalies()
        
        return {
            "anomalies": anomalies,
            "count": len(anomalies),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to detect signal anomalies: {str(e)}",
        )


@router.post("/detect-user", response_model=Dict[str, Any])
async def detect_user_anomalies(
    user_id: str,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Detect anomalies in user behavior
    
    Args:
        user_id: User ID to check
        
    Returns:
        dict: List of detected user anomalies
    """
    try:
        anomalies = anomaly_detector.detect_user_anomalies(user_id)
        
        return {
            "user_id": user_id,
            "anomalies": anomalies,
            "count": len(anomalies),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to detect user anomalies: {str(e)}",
        )


@router.post("/detect-data-quality", response_model=Dict[str, Any])
async def detect_data_quality_anomalies(
    data: Dict[str, Any],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Detect data quality issues
    
    Args:
        data: Data to check for quality issues
        
    Returns:
        dict: List of detected data quality anomalies
    """
    try:
        anomalies = anomaly_detector.detect_data_quality_anomalies(data)
        
        return {
            "anomalies": anomalies,
            "count": len(anomalies),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to detect data quality anomalies: {str(e)}",
        )


@router.post("/record-signal", response_model=Dict[str, Any])
async def record_signal(
    signal_type: str,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Record a signal for anomaly detection
    
    Args:
        signal_type: Type of signal to record
        
    Returns:
        dict: Confirmation
    """
    try:
        anomaly_detector.record_signal(signal_type)
        
        return {
            "status": "success",
            "signal_type": signal_type,
            "message": "Signal recorded for anomaly detection",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to record signal: {str(e)}",
        )


@router.post("/record-user-activity", response_model=Dict[str, Any])
async def record_user_activity(
    user_id: str,
    activity_score: float,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Record user activity for anomaly detection
    
    Args:
        user_id: User ID
        activity_score: Activity score (0-1)
        
    Returns:
        dict: Confirmation
    """
    try:
        anomaly_detector.record_user_activity(user_id, activity_score)
        
        return {
            "status": "success",
            "user_id": user_id,
            "activity_score": activity_score,
            "message": "User activity recorded for anomaly detection",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to record user activity: {str(e)}",
        )


@router.post("/record-network-size", response_model=Dict[str, Any])
async def record_network_size(
    user_id: str,
    network_size: int,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Record network size for anomaly detection
    
    Args:
        user_id: User ID
        network_size: Size of the user's network
        
    Returns:
        dict: Confirmation
    """
    try:
        anomaly_detector.record_network_size(user_id, network_size)
        
        return {
            "status": "success",
            "user_id": user_id,
            "network_size": network_size,
            "message": "Network size recorded for anomaly detection",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to record network size: {str(e)}",
        )


@router.get("/summary", response_model=Dict[str, Any])
async def get_anomaly_summary(
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get a summary of recent anomalies
    
    Returns:
        dict: Anomaly summary statistics
    """
    try:
        summary = anomaly_detector.get_anomaly_summary()
        
        return {
            "summary": summary,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get anomaly summary: {str(e)}",
        )


@router.get("/detect-all", response_model=Dict[str, Any])
async def detect_all_anomalies(
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Detect all types of anomalies
    
    Returns:
        dict: All detected anomalies
    """
    try:
        all_anomalies = anomaly_detector.detect_all_anomalies()
        
        return {
            "anomalies": all_anomalies,
            "total_count": sum(len(anomalies) for anomalies in all_anomalies.values()),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to detect all anomalies: {str(e)}",
        )


@router.get("/stats", response_model=Dict[str, Any])
async def get_anomaly_detector_stats(
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get anomaly detector statistics
    
    Returns:
        dict: Detector statistics
    """
    try:
        stats = {
            "is_loaded": anomaly_detector.is_loaded,
            "version": anomaly_detector.version,
            "last_trained": anomaly_detector.last_trained,
            "signal_types_tracked": len(anomaly_detector.signal_history),
            "users_tracked": len(anomaly_detector.user_activity_history),
            "thresholds": anomaly_detector.thresholds,
            "anomaly_types": anomaly_detector.ANOMALY_TYPES,
        }
        
        return {
            "detector": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get anomaly detector stats: {str(e)}",
        )


@router.post("/update-thresholds", response_model=Dict[str, Any])
async def update_anomaly_thresholds(
    new_thresholds: Dict[str, float],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Update anomaly detection thresholds
    
    Args:
        new_thresholds: Dictionary of new thresholds
        
    Returns:
        dict: Confirmation
    """
    try:
        anomaly_detector.update_thresholds(new_thresholds)
        
        return {
            "status": "success",
            "updated_thresholds": new_thresholds,
            "message": "Anomaly detection thresholds updated",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update thresholds: {str(e)}",
        )
