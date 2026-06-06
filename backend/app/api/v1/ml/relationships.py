"""
ML Relationships API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional

from app.core.dependencies import get_current_user, get_db, AsyncSession
from app.db.models.user import User as UserDB
from app.ml.services.relationship_analysis import relationship_analysis_service

router = APIRouter(prefix="/relationships", tags=["ml", "relationships"])


@router.post("/predict-strength", response_model=Dict[str, Any])
async def predict_relationship_strength(
    relationship_data: Dict[str, Any],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Predict relationship strength
    
    Args:
        relationship_data: Relationship data dictionary
        
    Returns:
        dict: Strength prediction with explanation
    """
    try:
        strength_score, explanation = await relationship_analysis_service.predict_strength(
            relationship_data
        )
        
        return {
            "strength_score": strength_score,
            "strength_label": explanation.get("label", "Unknown"),
            "explanation": explanation,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to predict relationship strength: {str(e)}",
        )


@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_relationship(
    from_person: Dict[str, Any],
    to_person: Dict[str, Any],
    relationship_data: Dict[str, Any],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Perform comprehensive relationship analysis
    
    Args:
        from_person: Source person profile
        to_person: Target person profile
        relationship_data: Relationship data
        
    Returns:
        dict: Comprehensive relationship analysis
    """
    try:
        analysis = await relationship_analysis_service.analyze_relationship(
            from_person, to_person, relationship_data
        )
        
        return {
            "analysis": analysis,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to analyze relationship: {str(e)}",
        )


@router.post("/calculate-similarity", response_model=Dict[str, Any])
async def calculate_profile_similarity(
    profile1: Dict[str, Any],
    profile2: Dict[str, Any],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Calculate similarity between two profiles
    
    Args:
        profile1: First profile
        profile2: Second profile
        
    Returns:
        dict: Similarity score
    """
    try:
        similarity = await relationship_analysis_service.calculate_profile_similarity(
            profile1, profile2
        )
        
        return {
            "profile1_id": profile1.get("id", "unknown"),
            "profile2_id": profile2.get("id", "unknown"),
            "similarity": similarity,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to calculate profile similarity: {str(e)}",
        )


@router.post("/batch-predict", response_model=Dict[str, Any])
async def batch_predict_strength(
    relationships: List[Dict[str, Any]],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Predict strength for multiple relationships
    
    Args:
        relationships: List of relationship data dictionaries
        
    Returns:
        dict: List of strength predictions
    """
    try:
        results = await relationship_analysis_service.batch_predict_strength(relationships)
        
        formatted_results = []
        for score, explanation in results:
            formatted_results.append({
                "strength_score": score,
                "strength_label": explanation.get("label", "Unknown"),
                "explanation": explanation,
            })
        
        return {
            "results": formatted_results,
            "count": len(formatted_results),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to batch predict relationship strength: {str(e)}",
        )


@router.post("/get-distribution", response_model=Dict[str, Any])
async def get_strength_distribution(
    relationships: List[Dict[str, Any]],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get distribution of relationship strengths
    
    Args:
        relationships: List of relationship data dictionaries
        
    Returns:
        dict: Strength distribution statistics
    """
    try:
        distribution = await relationship_analysis_service.get_strength_distribution(relationships)
        
        return {
            "distribution": distribution,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get strength distribution: {str(e)}",
        )


@router.post("/get-suggestions", response_model=Dict[str, Any])
async def get_improvement_suggestions(
    relationship_data: Dict[str, Any],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get suggestions for improving a relationship
    
    Args:
        relationship_data: Relationship data
        
    Returns:
        dict: List of improvement suggestions
    """
    try:
        suggestions = await relationship_analysis_service.get_improvement_suggestions(
            relationship_data
        )
        
        return {
            "suggestions": suggestions,
            "count": len(suggestions),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get improvement suggestions: {str(e)}",
        )


@router.get("/stats", response_model=Dict[str, Any])
async def get_model_stats(
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get relationship strength model statistics
    
    Returns:
        dict: Model statistics
    """
    try:
        stats = await relationship_analysis_service.get_model_stats()
        
        return {
            "model": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model stats: {str(e)}",
        )
