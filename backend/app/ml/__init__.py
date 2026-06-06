"""
Machine Learning Module for Bazov

This module provides ML-powered features for:
- Signal extraction and classification
- Relationship strength prediction
- Recommendation engine
- Anomaly detection
- Continuous learning
"""

from .models import (
    SignalClassifier,
    RelationshipStrengthModel,
    RecommendationModel,
    AnomalyDetector,
)
from .services import (
    SignalProcessingService,
    RelationshipAnalysisService,
    RecommendationService,
    AnomalyDetectionService,
)
from .utils import (
    text_preprocessing,
    feature_extraction,
    model_serialization,
)

__all__ = [
    # Models
    "SignalClassifier",
    "RelationshipStrengthModel",
    "RecommendationModel",
    "AnomalyDetector",
    # Services
    "SignalProcessingService",
    "RelationshipAnalysisService",
    "RecommendationService",
    "AnomalyDetectionService",
    # Utilities
    "text_preprocessing",
    "feature_extraction",
    "model_serialization",
]

# Version info
__version__ = "0.1.0"
ML_MODELS_VERSION = "0.1.0"
