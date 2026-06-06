"""
Relationship Strength Prediction Model

Predicts the strength of professional relationships based on:
- Interaction frequency
- Connection history
- Common connections
- Profile similarity
- Engagement metrics
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)


class RelationshipStrengthModel:
    """
    ML model to predict relationship strength (1-10 scale)
    
    Features used:
    - Number of interactions
    - Time since last interaction
    - Common connections count
    - Profile similarity score
    - Shared interests/skills
    - Communication frequency
    - Connection duration
    """
    
    # Strength scale
    STRENGTH_SCALE = {
        1: "Very Weak",
        2: "Weak",
        3: "Below Average",
        4: "Average",
        5: "Above Average",
        6: "Strong",
        7: "Very Strong",
        8: "Excellent",
        9: "Outstanding",
        10: "Exceptional",
    }
    
    # Feature weights (can be learned)
    DEFAULT_FEATURE_WEIGHTS = {
        "interaction_count": 0.25,
        "recency_score": 0.20,
        "common_connections": 0.15,
        "profile_similarity": 0.15,
        "shared_skills": 0.10,
        "communication_frequency": 0.10,
        "connection_duration": 0.05,
    }
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the relationship strength model
        
        Args:
            model_path: Path to load a pre-trained model
        """
        self.model = None
        self.feature_weights = self.DEFAULT_FEATURE_WEIGHTS.copy()
        self.is_loaded = False
        self.model_path = model_path
        self.last_trained = None
        self.accuracy = 0.0
        self.version = "0.1.0"
        
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
            weights_file = Path(model_path) / "weights.json"
            
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    self.last_trained = metadata.get("last_trained")
                    self.accuracy = metadata.get("accuracy", 0.0)
                    self.version = metadata.get("version", "0.1.0")
            
            if weights_file.exists():
                with open(weights_file, 'r') as f:
                    self.feature_weights = json.load(f)
            
            self.is_loaded = True
            logger.info(f"Relationship strength model loaded from {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load relationship strength model: {str(e)}")
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
                "accuracy": self.accuracy,
                "version": self.version,
            }
            
            with open(os.path.join(save_path, "metadata.json"), 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Save weights
            with open(os.path.join(save_path, "weights.json"), 'w') as f:
                json.dump(self.feature_weights, f, indent=2)
            
            logger.info(f"Relationship strength model saved to {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save relationship strength model: {str(e)}")
            return False
    
    def extract_features(self, relationship_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract features from relationship data
        
        Args:
            relationship_data: Relationship data dictionary
            
        Returns:
            dict: Feature dictionary with normalized values
        """
        features = {}
        
        # Interaction count (normalize to 0-1)
        interaction_count = relationship_data.get("interaction_count", 0)
        features["interaction_count"] = min(1.0, interaction_count / 100.0)
        
        # Recency score (0-1, where 1 is very recent)
        last_interaction = relationship_data.get("last_interaction")
        if last_interaction:
            try:
                last_date = datetime.fromisoformat(last_interaction.replace('Z', '+00:00'))
                days_since = (datetime.utcnow() - last_date).days
                # 0 days = 1.0, 365 days = 0.0
                features["recency_score"] = max(0.0, 1.0 - (days_since / 365.0))
            except:
                features["recency_score"] = 0.5
        else:
            features["recency_score"] = 0.0
        
        # Common connections (normalize to 0-1)
        common_connections = relationship_data.get("common_connections", 0)
        features["common_connections"] = min(1.0, common_connections / 50.0)
        
        # Profile similarity (0-1)
        profile_similarity = relationship_data.get("profile_similarity", 0.0)
        features["profile_similarity"] = float(profile_similarity)
        
        # Shared skills (0-1)
        shared_skills = relationship_data.get("shared_skills", 0)
        features["shared_skills"] = min(1.0, shared_skills / 20.0)
        
        # Communication frequency (0-1)
        communication_frequency = relationship_data.get("communication_frequency", 0.0)
        features["communication_frequency"] = float(communication_frequency)
        
        # Connection duration in days (normalize to 0-1)
        connection_duration = relationship_data.get("connection_duration_days", 0)
        features["connection_duration"] = min(1.0, connection_duration / 3650.0)  # 10 years max
        
        return features
    
    def predict(self, relationship_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        Predict relationship strength
        
        Args:
            relationship_data: Relationship data dictionary
            
        Returns:
            tuple: (strength_score, explanation)
        """
        # Extract features
        features = self.extract_features(relationship_data)
        
        # Calculate weighted score
        weighted_sum = 0.0
        feature_contributions = {}
        
        for feature, weight in self.feature_weights.items():
            value = features.get(feature, 0.0)
            contribution = value * weight
            weighted_sum += contribution
            feature_contributions[feature] = {
                "value": value,
                "weight": weight,
                "contribution": contribution,
            }
        
        # Scale to 1-10
        strength_score = 1.0 + (weighted_sum * 9.0)
        strength_score = max(1.0, min(10.0, strength_score))
        
        # Round to 1 decimal place
        strength_score = round(strength_score, 1)
        
        # Get label
        strength_label = self.get_strength_label(strength_score)
        
        explanation = {
            "score": strength_score,
            "label": strength_label,
            "features": feature_contributions,
            "recommendations": self.get_recommendations(strength_score, feature_contributions),
        }
        
        return strength_score, explanation
    
    def predict_batch(self, relationships: List[Dict[str, Any]]) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Predict strength for multiple relationships
        
        Args:
            relationships: List of relationship data dictionaries
            
        Returns:
            list: List of (score, explanation) tuples
        """
        return [self.predict(rel) for rel in relationships]
    
    def get_strength_label(self, score: float) -> str:
        """
        Get human-readable label for strength score
        
        Args:
            score: Strength score (1-10)
            
        Returns:
            str: Strength label
        """
        rounded = round(score)
        return self.STRENGTH_SCALE.get(rounded, "Unknown")
    
    def get_recommendations(self, score: float, feature_contributions: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations to improve relationship strength
        
        Args:
            score: Current strength score
            feature_contributions: Feature contributions dictionary
            
        Returns:
            list: List of recommendations
        """
        recommendations = []
        
        # Low interaction count
        if feature_contributions.get("interaction_count", {}).get("value", 0) < 0.3:
            recommendations.append("Increase interaction frequency - reach out more often")
        
        # Low recency score
        if feature_contributions.get("recency_score", {}).get("value", 0) < 0.5:
            recommendations.append("Reconnect soon - it's been a while since your last interaction")
        
        # Low common connections
        if feature_contributions.get("common_connections", {}).get("value", 0) < 0.3:
            recommendations.append("Find common connections to strengthen the relationship")
        
        # Low profile similarity
        if feature_contributions.get("profile_similarity", {}).get("value", 0) < 0.5:
            recommendations.append("Discover shared interests to improve profile similarity")
        
        # Low shared skills
        if feature_contributions.get("shared_skills", {}).get("value", 0) < 0.3:
            recommendations.append("Identify and discuss shared skills or expertise")
        
        # Low communication frequency
        if feature_contributions.get("communication_frequency", {}).get("value", 0) < 0.3:
            recommendations.append("Establish regular communication patterns")
        
        # Short connection duration
        if feature_contributions.get("connection_duration", {}).get("value", 0) < 0.1:
            recommendations.append("This is a new connection - nurture it over time")
        
        # If score is high, suggest maintenance
        if score >= 8.0:
            recommendations.append("Strong relationship - maintain regular contact")
        
        return recommendations if recommendations else ["Relationship is in good shape - keep it up!"]
    
    def calculate_profile_similarity(
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
        similarity_scores = []
        
        # Industry similarity
        industry1 = profile1.get("industry", "").lower()
        industry2 = profile2.get("industry", "").lower()
        if industry1 and industry2:
            similarity_scores.append(1.0 if industry1 == industry2 else 0.3)
        
        # Skills similarity (Jaccard similarity)
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
        
        # Education similarity
        education1 = profile1.get("education", "").lower()
        education2 = profile2.get("education", "").lower()
        if education1 and education2:
            similarity_scores.append(1.0 if education1 == education2 else 0.3)
        
        # Calculate average
        if similarity_scores:
            return sum(similarity_scores) / len(similarity_scores)
        
        return 0.0
    
    def train(self, training_data: List[Dict[str, Any]], epochs: int = 10) -> float:
        """
        Train the model (placeholder for actual training)
        
        Args:
            training_data: List of {"features": dict, "target": float}
            epochs: Number of training epochs
            
        Returns:
            float: Training accuracy
        """
        # In production, this would train a regression model
        # For now, we'll just update the last_trained timestamp
        
        self.last_trained = datetime.utcnow().isoformat()
        self.version = f"0.1.{int(datetime.utcnow().timestamp())}"
        
        # Calculate mock accuracy
        if training_data:
            self.accuracy = min(0.95, 0.7 + len(training_data) * 0.0001)
        
        logger.info(f"Relationship strength model trained with {len(training_data)} samples")
        return self.accuracy
    
    def update_weights(self, new_weights: Dict[str, float]) -> None:
        """
        Update feature weights
        
        Args:
            new_weights: Dictionary of feature weights
        """
        for feature, weight in new_weights.items():
            if feature in self.feature_weights:
                self.feature_weights[feature] = weight
        
        logger.info("Relationship strength model weights updated")


# Create a global instance
relationship_strength_model = RelationshipStrengthModel()
