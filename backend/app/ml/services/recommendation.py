"""
Recommendation Service

Provides high-level recommendation functionality
"""

from typing import List, Dict, Any, Optional
from app.ml.models.recommendation import RecommendationModel

# Create a global recommendation model instance
recommendation_model = RecommendationModel()


class RecommendationService:
    """
    Service for providing recommendations
    """
    
    def __init__(self, model: Optional[RecommendationModel] = None):
        """
        Initialize the recommendation service
        
        Args:
            model: Recommendation model to use
        """
        self.model = model or RecommendationModel()
    
    def recommend_people(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get people recommendations for a user
        
        Args:
            user_id: User ID
            limit: Maximum number of recommendations
            
        Returns:
            List of recommended people
        """
        return self.model.recommend_people(user_id, limit)
    
    def recommend_signals(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get signal recommendations for a user
        
        Args:
            user_id: User ID
            limit: Maximum number of recommendations
            
        Returns:
            List of recommended signals
        """
        return self.model.recommend_signals(user_id, limit)
    
    def add_user_profile(self, user_id: str, profile: Dict[str, Any]) -> None:
        """
        Add or update a user profile
        
        Args:
            user_id: User ID
            profile: User profile data
        """
        self.model.add_user_profile(user_id, profile)
    
    def add_item_profile(self, item_id: str, profile: Dict[str, Any], item_type: str) -> None:
        """
        Add or update an item profile
        
        Args:
            item_id: Item ID
            profile: Item profile data
            item_type: Type of item (e.g., 'person', 'signal')
        """
        self.model.add_item_profile(item_id, profile, item_type)
    
    def record_interaction(self, user_id: str, item_id: str, item_type: str, score: float) -> None:
        """
        Record a user interaction with an item
        
        Args:
            user_id: User ID
            item_id: Item ID
            item_type: Type of item
            score: Interaction score
        """
        self.model.record_interaction(user_id, item_id, item_type, score)
