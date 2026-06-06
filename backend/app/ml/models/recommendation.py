"""
Recommendation Model

Provides personalized recommendations for:
- People to connect with
- Signals to follow
- Content to engage with
- Network expansion opportunities
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)


class RecommendationModel:
    """
    Recommendation engine using collaborative filtering and content-based filtering
    
    Features:
    - People recommendations (who to connect with)
    - Signal recommendations (what to follow)
    - Content recommendations (what to read)
    - Network expansion suggestions
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the recommendation model
        
        Args:
            model_path: Path to load a pre-trained model
        """
        self.user_profiles = {}  # user_id -> profile data
        self.item_profiles = {}  # item_id -> profile data
        self.user_interactions = defaultdict(dict)  # user_id -> {item_id: score}
        self.similarity_matrix = {}  # Precomputed similarities
        
        self.is_loaded = False
        self.model_path = model_path
        self.last_trained = None
        self.version = "0.1.0"
        
        # Recommendation strategies
        self.strategies = [
            "collaborative_filtering",
            "content_based",
            "popularity",
            "trending",
            "social",
        ]
        
        # Strategy weights
        self.strategy_weights = {
            "collaborative_filtering": 0.4,
            "content_based": 0.3,
            "popularity": 0.1,
            "trending": 0.1,
            "social": 0.1,
        }
        
        # Try to load model
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str) -> bool:
        """
        Load a pre-trained model from disk
        
        Args:
            model_path: Path to the model directory
            
        Returns:
            bool: True if model loaded successfully
        """
        try:
            metadata_file = Path(model_path) / "metadata.json"
            user_profiles_file = Path(model_path) / "user_profiles.json"
            item_profiles_file = Path(model_path) / "item_profiles.json"
            
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    self.last_trained = metadata.get("last_trained")
                    self.version = metadata.get("version", "0.1.0")
            
            if user_profiles_file.exists():
                with open(user_profiles_file, 'r') as f:
                    self.user_profiles = json.load(f)
            
            if item_profiles_file.exists():
                with open(item_profiles_file, 'r') as f:
                    self.item_profiles = json.load(f)
            
            self.is_loaded = True
            logger.info(f"Recommendation model loaded from {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load recommendation model: {str(e)}")
            return False
    
    def save_model(self, save_path: str) -> bool:
        """
        Save the model to disk
        
        Args:
            save_path: Directory to save the model
            
        Returns:
            bool: True if model saved successfully
        """
        try:
            os.makedirs(save_path, exist_ok=True)
            
            # Save metadata
            metadata = {
                "last_trained": self.last_trained,
                "version": self.version,
                "user_count": len(self.user_profiles),
                "item_count": len(self.item_profiles),
            }
            
            with open(os.path.join(save_path, "metadata.json"), 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Save user profiles
            with open(os.path.join(save_path, "user_profiles.json"), 'w') as f:
                json.dump(self.user_profiles, f, indent=2)
            
            # Save item profiles
            with open(os.path.join(save_path, "item_profiles.json"), 'w') as f:
                json.dump(self.item_profiles, f, indent=2)
            
            logger.info(f"Recommendation model saved to {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save recommendation model: {str(e)}")
            return False
    
    def add_user_profile(self, user_id: str, profile: Dict[str, Any]) -> None:
        """
        Add or update a user profile
        
        Args:
            user_id: User ID
            profile: User profile data
        """
        self.user_profiles[user_id] = profile
        logger.debug(f"Added/updated user profile: {user_id}")
    
    def add_item_profile(self, item_id: str, profile: Dict[str, Any], item_type: str = "signal") -> None:
        """
        Add or update an item profile
        
        Args:
            item_id: Item ID
            profile: Item profile data
            item_type: Type of item (signal, person, company, etc.)
        """
        if item_type not in self.item_profiles:
            self.item_profiles[item_type] = {}
        
        self.item_profiles[item_type][item_id] = profile
        logger.debug(f"Added/updated {item_type} profile: {item_id}")
    
    def record_interaction(self, user_id: str, item_id: str, item_type: str, score: float = 1.0) -> None:
        """
        Record a user interaction with an item
        
        Args:
            user_id: User ID
            item_id: Item ID
            item_type: Type of item
            score: Interaction score/weight
        """
        if item_type not in self.user_interactions[user_id]:
            self.user_interactions[user_id][item_type] = {}
        
        self.user_interactions[user_id][item_type][item_id] = score
        logger.debug(f"Recorded interaction: {user_id} -> {item_type}:{item_id}")
    
    def calculate_similarity(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> float:
        """
        Calculate similarity between two profiles
        
        Args:
            profile1: First profile
            profile2: Second profile
            
        Returns:
            float: Similarity score (0-1)
        """
        similarity_scores = []
        
        # Industry similarity
        industry1 = profile1.get("industry", "").lower()
        industry2 = profile2.get("industry", "").lower()
        if industry1 and industry2:
            similarity_scores.append(1.0 if industry1 == industry2 else 0.0)
        
        # Skills similarity (Jaccard)
        skills1 = set(profile1.get("skills", []))
        skills2 = set(profile2.get("skills", []))
        if skills1 or skills2:
            intersection = len(skills1 & skills2)
            union = len(skills1 | skills2)
            similarity_scores.append(intersection / union if union > 0 else 0.0)
        
        # Location similarity
        location1 = profile1.get("location", "").lower()
        location2 = profile2.get("location", "").lower()
        if location1 and location2:
            similarity_scores.append(1.0 if location1 == location2 else 0.5)
        
        # Company similarity
        company1 = profile1.get("current_company", "").lower()
        company2 = profile2.get("current_company", "").lower()
        if company1 and company2:
            similarity_scores.append(1.0 if company1 == company2 else 0.0)
        
        # Title similarity (simple)
        title1 = profile1.get("title", "").lower()
        title2 = profile2.get("title", "").lower()
        if title1 and title2:
            # Simple keyword matching
            words1 = set(title1.split())
            words2 = set(title2.split())
            intersection = len(words1 & words2)
            union = len(words1 | words2)
            similarity_scores.append(intersection / union if union > 0 else 0.0)
        
        # Calculate average
        if similarity_scores:
            return sum(similarity_scores) / len(similarity_scores)
        
        return 0.0
    
    def collaborative_filtering_recommendations(
        self,
        user_id: str,
        item_type: str = "person",
        limit: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations using collaborative filtering
        
        Args:
            user_id: User ID
            item_type: Type of items to recommend
            limit: Maximum number of recommendations
            
        Returns:
            list: List of (item_id, score) tuples
        """
        if user_id not in self.user_interactions:
            return []
        
        if item_type not in self.user_interactions[user_id]:
            return []
        
        # Find similar users
        similar_users = []
        
        for other_user_id, other_user_interactions in self.user_interactions.items():
            if other_user_id == user_id:
                continue
            
            if item_type not in other_user_interactions:
                continue
            
            # Calculate similarity based on interactions
            user_items = set(self.user_interactions[user_id][item_type].keys())
            other_items = set(other_user_interactions[item_type].keys())
            
            intersection = len(user_items & other_items)
            union = len(user_items | other_items)
            
            if union > 0:
                similarity = intersection / union
                if similarity > 0.3:  # Minimum similarity threshold
                    similar_users.append((other_user_id, similarity))
        
        # Sort by similarity
        similar_users.sort(key=lambda x: x[1], reverse=True)
        
        # Get recommendations from similar users
        recommendations = defaultdict(float)
        
        for similar_user_id, similarity in similar_users[:5]:  # Top 5 similar users
            if item_type in self.user_interactions[similar_user_id]:
                for item_id, score in self.user_interactions[similar_user_id][item_type].items():
                    if item_id not in self.user_interactions[user_id][item_type]:
                        recommendations[item_id] += similarity * score
        
        # Sort by score
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_recommendations[:limit]
    
    def content_based_recommendations(
        self,
        user_id: str,
        item_type: str = "person",
        limit: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations using content-based filtering
        
        Args:
            user_id: User ID
            item_type: Type of items to recommend
            limit: Maximum number of recommendations
            
        Returns:
            list: List of (item_id, score) tuples
        """
        if user_id not in self.user_profiles:
            return []
        
        if item_type not in self.item_profiles:
            return []
        
        user_profile = self.user_profiles[user_id]
        recommendations = []
        
        for item_id, item_profile in self.item_profiles[item_type].items():
            similarity = self.calculate_similarity(user_profile, item_profile)
            if similarity > 0.3:  # Minimum similarity threshold
                recommendations.append((item_id, similarity))
        
        # Sort by similarity
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:limit]
    
    def popularity_recommendations(
        self,
        item_type: str = "person",
        limit: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations based on popularity
        
        Args:
            item_type: Type of items to recommend
            limit: Maximum number of recommendations
            
        Returns:
            list: List of (item_id, score) tuples
        """
        if item_type not in self.item_profiles:
            return []
        
        # Count interactions for each item
        item_scores = defaultdict(float)
        
        for user_id, user_interactions in self.user_interactions.items():
            if item_type in user_interactions:
                for item_id, score in user_interactions[item_type].items():
                    item_scores[item_id] += score
        
        # Sort by score
        sorted_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_items[:limit]
    
    def trending_recommendations(
        self,
        item_type: str = "signal",
        limit: int = 10,
        time_window_days: int = 7
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations based on trending items
        
        Args:
            item_type: Type of items to recommend
            limit: Maximum number of recommendations
            time_window_days: Time window for trending calculation
            
        Returns:
            list: List of (item_id, score) tuples
        """
        # In a real implementation, this would track recent interactions
        # For now, return popularity recommendations
        return self.popularity_recommendations(item_type, limit)
    
    def social_recommendations(
        self,
        user_id: str,
        item_type: str = "person",
        limit: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations based on social connections
        
        Args:
            user_id: User ID
            item_type: Type of items to recommend
            limit: Maximum number of recommendations
            
        Returns:
            list: List of (item_id, score) tuples
        """
        # In a real implementation, this would use the user's network
        # For now, return content-based recommendations
        return self.content_based_recommendations(user_id, item_type, limit)
    
    def recommend(
        self,
        user_id: str,
        item_type: str = "person",
        limit: int = 10,
        strategy_weights: Optional[Dict[str, float]] = None
    ) -> List[Tuple[str, float, Dict[str, float]]]:
        """
        Generate recommendations using all strategies
        
        Args:
            user_id: User ID
            item_type: Type of items to recommend
            limit: Maximum number of recommendations
            strategy_weights: Custom weights for recommendation strategies
            
        Returns:
            list: List of (item_id, combined_score, strategy_scores) tuples
        """
        weights = strategy_weights or self.strategy_weights
        
        # Get recommendations from each strategy
        strategy_results = {}
        
        for strategy in self.strategies:
            if weights.get(strategy, 0) > 0:
                if strategy == "collaborative_filtering":
                    strategy_results[strategy] = self.collaborative_filtering_recommendations(
                        user_id, item_type, limit * 2
                    )
                elif strategy == "content_based":
                    strategy_results[strategy] = self.content_based_recommendations(
                        user_id, item_type, limit * 2
                    )
                elif strategy == "popularity":
                    strategy_results[strategy] = self.popularity_recommendations(
                        item_type, limit * 2
                    )
                elif strategy == "trending":
                    strategy_results[strategy] = self.trending_recommendations(
                        item_type, limit * 2
                    )
                elif strategy == "social":
                    strategy_results[strategy] = self.social_recommendations(
                        user_id, item_type, limit * 2
                    )
        
        # Combine recommendations from all strategies
        combined_scores = defaultdict(lambda: defaultdict(float))
        
        for strategy, recommendations in strategy_results.items():
            weight = weights.get(strategy, 0)
            for item_id, score in recommendations:
                combined_scores[item_id][strategy] = score * weight
        
        # Calculate combined scores
        final_recommendations = []
        
        for item_id, strategy_scores in combined_scores.items():
            combined_score = sum(strategy_scores.values())
            final_recommendations.append((item_id, combined_score, dict(strategy_scores)))
        
        # Sort by combined score
        final_recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return final_recommendations[:limit]
    
    def recommend_people(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recommend people to connect with
        
        Args:
            user_id: User ID
            limit: Maximum number of recommendations
            
        Returns:
            list: List of recommendation dictionaries
        """
        recommendations = self.recommend(user_id, "person", limit)
        
        result = []
        for item_id, score, strategy_scores in recommendations:
            if item_id in self.item_profiles.get("person", {}):
                person_profile = self.item_profiles["person"][item_id]
                result.append({
                    "person_id": item_id,
                    "name": person_profile.get("full_name", "Unknown"),
                    "title": person_profile.get("current_title", ""),
                    "company": person_profile.get("current_company", ""),
                    "score": score,
                    "strategy_scores": strategy_scores,
                    "reason": self.generate_recommendation_reason(strategy_scores),
                })
        
        return result
    
    def recommend_signals(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recommend signals to follow
        
        Args:
            user_id: User ID
            limit: Maximum number of recommendations
            
        Returns:
            list: List of recommendation dictionaries
        """
        recommendations = self.recommend(user_id, "signal", limit)
        
        result = []
        for item_id, score, strategy_scores in recommendations:
            if item_id in self.item_profiles.get("signal", {}):
                signal_profile = self.item_profiles["signal"][item_id]
                result.append({
                    "signal_id": item_id,
                    "title": signal_profile.get("title", "Untitled"),
                    "signal_type": signal_profile.get("signal_type", "other"),
                    "company": signal_profile.get("company", ""),
                    "score": score,
                    "strategy_scores": strategy_scores,
                    "reason": self.generate_recommendation_reason(strategy_scores),
                })
        
        return result
    
    def generate_recommendation_reason(self, strategy_scores: Dict[str, float]) -> str:
        """
        Generate a human-readable reason for a recommendation
        
        Args:
            strategy_scores: Strategy scores dictionary
            
        Returns:
            str: Recommendation reason
        """
        reasons = []
        
        if strategy_scores.get("collaborative_filtering", 0) > 0.3:
            reasons.append("similar users are interested")
        
        if strategy_scores.get("content_based", 0) > 0.3:
            reasons.append("matches your interests")
        
        if strategy_scores.get("popularity", 0) > 0.2:
            reasons.append("popular in the community")
        
        if strategy_scores.get("trending", 0) > 0.2:
            reasons.append("currently trending")
        
        if strategy_scores.get("social", 0) > 0.2:
            reasons.append("connected through your network")
        
        return ", ".join(reasons) if reasons else "recommended for you"
    
    def train(self, training_data: List[Dict[str, Any]], epochs: int = 10) -> float:
        """
        Train the recommendation model (placeholder)
        
        Args:
            training_data: Training data
            epochs: Number of training epochs
            
        Returns:
            float: Training accuracy
        """
        self.last_trained = datetime.utcnow().isoformat()
        self.version = f"0.1.{int(datetime.utcnow().timestamp())}"
        
        logger.info(f"Recommendation model trained with {len(training_data)} samples")
        return 0.85  # Mock accuracy


# Create a global instance
recommendation_model = RecommendationModel()
