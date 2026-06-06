"""
ML Signals API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional

from app.core.dependencies import get_current_user, get_db, AsyncSession
from app.db.models.user import User as UserDB
from app.ml.services.signal_processing import signal_processing_service

router = APIRouter(prefix="/signals", tags=["ml", "signals"])


@router.post("/classify", response_model=Dict[str, Any])
async def classify_signal(
    text: str,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Classify a signal text
    
    Args:
        text: Signal text to classify
        
    Returns:
        dict: Classification result with signal type, confidence, and features
    """
    try:
        signal_type, confidence, features = await signal_processing_service.classify_signal(text)
        
        return {
            "text": text,
            "signal_type": signal_type,
            "confidence": confidence,
            "features": features,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to classify signal: {str(e)}",
        )


@router.post("/extract", response_model=Dict[str, Any])
async def extract_signals(
    text: str,
    source_url: Optional[str] = None,
    source_type: str = "text",
    company_id: Optional[str] = None,
    person_id: Optional[str] = None,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Extract signals from text
    
    Args:
        text: Text to extract signals from
        source_url: Optional source URL
        source_type: Type of source
        company_id: Optional company ID to associate
        person_id: Optional person ID to associate
        
    Returns:
        dict: List of extracted signals
    """
    try:
        signals = await signal_processing_service.process_text(
            text, source_url, source_type, company_id, person_id
        )
        
        return {
            "text": text,
            "signals": signals,
            "count": len(signals),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to extract signals: {str(e)}",
        )


@router.post("/analyze-sentiment", response_model=Dict[str, Any])
async def analyze_sentiment(
    text: str,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Analyze sentiment of text
    
    Args:
        text: Text to analyze
        
    Returns:
        dict: Sentiment analysis result
    """
    try:
        sentiment, score = await signal_processing_service.analyze_sentiment(text)
        
        return {
            "text": text,
            "sentiment": sentiment,
            "score": score,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to analyze sentiment: {str(e)}",
        )


@router.post("/extract-entities", response_model=Dict[str, Any])
async def extract_entities(
    text: str,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Extract entities from text
    
    Args:
        text: Text to extract entities from
        
    Returns:
        dict: Extracted entities by type
    """
    try:
        entities = await signal_processing_service.extract_entities(text)
        
        return {
            "text": text,
            "entities": entities,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to extract entities: {str(e)}",
        )


@router.get("/types", response_model=Dict[str, Any])
async def get_signal_types(
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get all available signal types
    
    Returns:
        dict: List of signal types
    """
    try:
        signal_types = await signal_processing_service.get_signal_types()
        
        return {
            "signal_types": signal_types,
            "count": len(signal_types),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get signal types: {str(e)}",
        )


@router.get("/stats", response_model=Dict[str, Any])
async def get_classifier_stats(
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get signal classifier statistics
    
    Returns:
        dict: Classifier statistics
    """
    try:
        stats = await signal_processing_service.get_classifier_stats()
        
        return {
            "classifier": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get classifier stats: {str(e)}",
        )


@router.post("/batch-classify", response_model=Dict[str, Any])
async def batch_classify(
    texts: List[str],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Classify multiple texts in batch
    
    Args:
        texts: List of texts to classify
        
    Returns:
        dict: List of classification results
    """
    try:
        results = []
        for text in texts:
            signal_type, confidence, features = await signal_processing_service.classify_signal(text)
            results.append({
                "text": text,
                "signal_type": signal_type,
                "confidence": confidence,
            })
        
        return {
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to batch classify: {str(e)}",
        )
