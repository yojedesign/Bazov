"""
Relationship Analysis Service

Provides ML-powered relationship analysis and strength prediction
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from app.ml.models.relationship_strength import relationship_strength_model
from app.db.session import AsyncSession
from app.db.models.relationship import Relationship as RelationshipDB
from app.db.models.person import Person as PersonDB

logger = logging.getLogger(__name__)


class RelationshipAnalysisService:
    """
    Service for analyzing and predicting relationship strength
    
    Features:
    - Predict relationship strength
    - Calculate profile similarity
    - Generate relationship insights
    - Provide improvement recommendations
    """
    
    def __init__(self):
        """Initialize the relationship analysis service"""
        self.model = relationship_strength_model
    
    async def predict_strength(
        self,
        relationship_data: Dict[str, Any]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Predict relationship strength
        
        Args:
            relationship_data: Relationship data dictionary
            
        Returns:
            tuple: (strength_score, explanation)
        """
        return self.model.predict(relationship_data)
    
    async def calculate_profile_similarity(
        self,
        profile1: Dict[str, Any],
        profile2: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity between two profiles
        
        Args:
            profile1: First profile
            profile2: Second profile
            
        Returns:
            float: Similarity score (0-1)
        """
        return self.model.calculate_profile_similarity(profile1, profile2)
    
    async def analyze_relationship(
        self,
        from_person: Dict[str, Any],
        to_person: Dict[str, Any],
        relationship_data: Dict[str, Any]
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
        # Calculate profile similarity
        similarity = await self.calculate_profile_similarity(from_person, to_person)
        
        # Update relationship data with similarity
        relationship_data["profile_similarity"] = similarity
        
        # Predict strength
        strength_score, explanation = await self.predict_strength(relationship_data)
        
        # Calculate shared skills
        skills1 = set(from_person.get("skills", []))
        skills2 = set(to_person.get("skills", []))
        shared_skills = len(skills1 & skills2)
        relationship_data["shared_skills"] = shared_skills
        
        # Calculate common connections (would need network data in production)
        common_connections = relationship_data.get("common_connections", 0)
        
        # Generate insights
        insights = {
            "strength_score": strength_score,
            "strength_label": explanation.get("label", "Unknown"),
            "profile_similarity": similarity,
            "shared_skills": shared_skills,
            "common_connections": common_connections,
            "feature_contributions": explanation.get("features", {}),
            "recommendations": explanation.get("recommendations", []),
            "insights": self._generate_insights(
                strength_score, similarity, shared_skills, common_connections
            ),
        }
        
        return insights
    
    def _generate_insights(
        self,
        strength_score: float,
        similarity: float,
        shared_skills: int,
        common_connections: int
    ) -> List[str]:
        """
        Generate relationship insights
        
        Args:
            strength_score: Relationship strength score
            similarity: Profile similarity score
            shared_skills: Number of shared skills
            common_connections: Number of common connections
            
        Returns:
            list: List of insight strings
        """
        insights = []
        
        # Strength insights
        if strength_score >= 8.0:
            insights.append("This is a strong relationship with high engagement")
        elif strength_score >= 6.0:
            insights.append("This is a solid relationship with good potential")
        elif strength_score >= 4.0:
            insights.append("This relationship has room for improvement")
        else:
            insights.append("This relationship needs attention and nurturing")
        
        # Similarity insights
        if similarity >= 0.8:
            insights.append("High profile similarity suggests strong alignment")
        elif similarity >= 0.6:
            insights.append("Good profile similarity with shared interests")
        elif similarity >= 0.4:
            insights.append("Moderate profile similarity")
        else:
            insights.append("Low profile similarity - explore common ground")
        
        # Shared skills insights
        if shared_skills >= 10:
            insights.append(f"Strong skill overlap ({shared_skills} shared skills)")
        elif shared_skills >= 5:
            insights.append(f"Good skill overlap ({shared_skills} shared skills)")
        elif shared_skills > 0:
            insights.append(f"Some skill overlap ({shared_skills} shared skills)")
        else:
            insights.append("No shared skills detected - explore new areas")
        
        # Common connections insights
        if common_connections >= 10:
            insights.append(f"Well-connected ({common_connections} common connections)")
        elif common_connections >= 5:
            insights.append(f"Good network overlap ({common_connections} common connections)")
        elif common_connections > 0:
            insights.append(f"Some network overlap ({common_connections} common connections)")
        else:
            insights.append("No common connections - consider introducing through mutual contacts")
        
        return insights
    
    async def batch_predict_strength(
        self,
        relationships: List[Dict[str, Any]]
    ) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Predict strength for multiple relationships
        
        Args:
            relationships: List of relationship data dictionaries
            
        Returns:
            list: List of (score, explanation) tuples
        """
        return self.model.predict_batch(relationships)
    
    async def get_strength_distribution(
        self,
        relationships: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get distribution of relationship strengths
        
        Args:
            relationships: List of relationship data dictionaries
            
        Returns:
            dict: Strength distribution statistics
        """
        scores = []
        for rel in relationships:
            score, _ = await self.predict_strength(rel)
            scores.append(score)
        
        if not scores:
            return {
                "count": 0,
                "mean": 0.0,
                "median": 0.0,
                "std": 0.0,
                "min": 0.0,
                "max": 0.0,
                "distribution": {},
            }
        
        import numpy as np
        
        scores_array = np.array(scores)
        
        # Calculate statistics
        distribution = {
            "count": len(scores),
            "mean": float(np.mean(scores_array)),
            "median": float(np.median(scores_array)),
            "std": float(np.std(scores_array)),
            "min": float(np.min(scores_array)),
            "max": float(np.max(scores_array)),
        }
        
        # Calculate distribution by strength labels
        label_counts = {}
        for score in scores:
            label = self.model.get_strength_label(score)
            label_counts[label] = label_counts.get(label, 0) + 1
        
        distribution["by_label"] = label_counts
        
        # Calculate percentiles
        distribution["percentiles"] = {
            "p25": float(np.percentile(scores_array, 25)),
            "p50": float(np.percentile(scores_array, 50)),
            "p75": float(np.percentile(scores_array, 75)),
        }
        
        return distribution
    
    async def get_relationship_health(
        self,
        user_id: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Get overall relationship health for a user
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            dict: Relationship health statistics
        """
        # In production, this would query the database for user's relationships
        # For now, return mock data
        
        return {
            "user_id": user_id,
            "total_relationships": 0,
            "average_strength": 0.0,
            "strong_relationships": 0,
            "weak_relationships": 0,
            "needs_attention": 0,
            "trends": {
                "improving": 0,
                "declining": 0,
                "stable": 0,
            },
            "recommendations": [
                "Connect with more people in your industry",
                "Reach out to inactive connections",
                "Strengthen relationships with shared interests",
            ],
        }
    
    async def get_improvement_suggestions(
        self,
        relationship_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Get suggestions for improving a relationship
        
        Args:
            relationship_data: Relationship data
            
        Returns:
            list: List of improvement suggestions
        """
        # Predict current strength
        strength_score, explanation = await self.predict_strength(relationship_data)
        
        # Get recommendations from the model
        recommendations = explanation.get("recommendations", [])
        
        # Create structured suggestions
        suggestions = []
        for i, recommendation in enumerate(recommendations, 1):
            suggestions.append({
                "id": i,
                "description": recommendation,
                "priority": "high" if i <= 2 else "medium",
                "impact": "high" if strength_score < 5.0 else "medium",
            })
        
        return suggestions
    
    async def train_model(
        self,
        training_data: List[Dict[str, Any]],
        epochs: int = 10
    ) -> float:
        """
        Train the relationship strength model
        
        Args:
            training_data: Training data
            epochs: Number of training epochs
            
        Returns:
            float: Training accuracy
        """
        return self.model.train(training_data, epochs)
    
    async def get_model_stats(self) -> Dict[str, Any]:
        """
        Get model statistics
        
        Returns:
            dict: Model statistics
        """
        return {
            "is_loaded": self.model.is_loaded,
            "version": self.model.version,
            "last_trained": self.model.last_trained,
            "accuracy": self.model.accuracy,
            "feature_weights": self.model.feature_weights,
            "strength_scale": self.model.STRENGTH_SCALE,
        }


# Create a global instance
relationship_analysis_service = RelationshipAnalysisService()
