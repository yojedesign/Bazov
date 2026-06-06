"""
Feature Extraction Utilities

Provides functions for extracting features from text and other data
"""

from typing import List, Dict, Any, Optional
import numpy as np


def extract_features(text: str, feature_type: str = "tfidf") -> Dict[str, Any]:
    """
    Extract features from text
    
    Args:
        text: Input text
        feature_type: Type of features to extract (tfidf, word2vec, etc.)
        
    Returns:
        Dictionary of extracted features
    """
    # Simple implementation - return character counts for now
    features = {}
    
    if feature_type == "basic":
        features["length"] = len(text)
        features["word_count"] = len(text.split())
        features["char_count"] = len(text)
    
    return features


def create_feature_vector(text: str, vocabulary: Optional[List[str]] = None) -> np.ndarray:
    """
    Create a feature vector from text
    
    Args:
        text: Input text
        vocabulary: Optional vocabulary to use
        
    Returns:
        Feature vector as numpy array
    """
    # Simple implementation - return a zero vector for now
    if vocabulary:
        return np.zeros(len(vocabulary))
    return np.zeros(100)
