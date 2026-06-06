"""
ML Recommendations API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional

from app.core.dependencies import get_current_user, get_db, AsyncSession
from app.db.models.user import User as UserDB
from app.ml.models.recommendation import recommendation_model

router = APIRouter(prefix="/recommendations", tags=["ml", "recommendations"])


@router.post("/people", response_model=Dict[str, Any])
async def recommend_people(
    user_id: str,
    limit: int = 10,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Recommend people to connect with
    
    Args:
        user_id: User ID to get recommendations for
        limit: Maximum number of recommendations
        
    Returns:
        dict: List of people recommendations
    """
    try:
        recommendations = recommendation_model.recommend_people(user_id, limit)
        
        return {
            "user_id": user_id,
            "recommendations": recommendations,
            "count": len(recommendations),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to recommend people: {str(e)}",
        )


@router.post("/signals", response_model=Dict[str, Any])
async def recommend_signals(
    user_id: str,
    limit: int = 10,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Recommend signals to follow
    
    Args:
        user_id: User ID to get recommendations for
        limit: Maximum number of recommendations
        
    Returns:
        dict: List of signal recommendations
    """
    try:
        recommendations = recommendation_model.recommend_signals(user_id, limit)
        
        return {
            "user_id": user_id,
            "recommendations": recommendations,
            "count": len(recommendations),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to recommend signals: {str(e)}",
        )


@router.post("/add-user-profile", response_model=Dict[str, Any])
async def add_user_profile(
    user_id: str,
    profile: Dict[str, Any],
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Add or update a user profile for recommendations
    
    Args:
        user_id: User ID
        profile: User profile data
        
    Returns:
        dict: Confirmation
    """
    try:
        recommendation_model.add_user_profile(user_id, profile)
        
        return {
            "status": "success",
            "user_id": user_id,
            "message": "User profile added/updated",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add user profile: {str(e)}",
        )


@router.post("/add-item-profile", response_model=Dict[str, Any])
async def add_item_profile(
    item_id: str,
    profile: Dict[str, Any],
    item_type: str = "signal",
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Add or update an item profile for recommendations
    
    Args:
        item_id: Item ID
        profile: Item profile data
        item_type: Type of item (signal, person, company, etc.)
        
    Returns:
        dict: Confirmation
    """
    try:
        recommendation_model.add_item_profile(item_id, profile, item_type)
        
        return {
            "status": "success",
            "item_id": item_id,
            "item_type": item_type,
            "message": "Item profile added/updated",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add item profile: {str(e)}",
        )


@router.post("/record-interaction", response_model=Dict[str, Any])
async def record_interaction(
    user_id: str,
    item_id: str,
    item_type: str = "signal",
    score: float = 1.0,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Record a user interaction with an item
    
    Args:
        user_id: User ID
        item_id: Item ID
        item_type: Type of item
        score: Interaction score/weight
        
    Returns:
        dict: Confirmation
    """
    try:
        recommendation_model.record_interaction(user_id, item_id, item_type, score)
        
        return {
            "status": "success",
            "user_id": user_id,
            "item_id": item_id,
            "item_type": item_type,
            "message": "Interaction recorded",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to record interaction: {str(e)}",
        )


@router.get("/stats", response_model=Dict[str, Any])
async def get_recommendation_stats(
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get recommendation model statistics
    
    Returns:
        dict: Model statistics
    """
    try:
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
        
        return {
            "model": stats,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendation stats: {str(e)}",
        )


@router.post("/custom-recommend", response_model=Dict[str, Any])
async def custom_recommend(
    user_id: str,
    item_type: str = "person",
    limit: int = 10,
    strategy_weights: Optional[Dict[str, float]] = None,
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get custom recommendations with specific strategy weights
    
    Args:
        user_id: User ID
        item_type: Type of items to recommend
        limit: Maximum number of recommendations
        strategy_weights: Custom weights for recommendation strategies
        
    Returns:
        dict: Custom recommendations
    """
    try:
        recommendations = recommendation_model.recommend(
            user_id, item_type, limit, strategy_weights
        )
        
        formatted_results = []
        for item_id, score, strategy_scores in recommendations:
            formatted_results.append({
                "item_id": item_id,
                "score": score,
                "strategy_scores": strategy_scores,
            })
        
        return {
            "user_id": user_id,
            "item_type": item_type,
            "recommendations": formatted_results,
            "count": len(formatted_results),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get custom recommendations: {str(e)}",
        )
