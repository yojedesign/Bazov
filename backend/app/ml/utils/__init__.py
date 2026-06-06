"""
ML Utilities Module

Provides utility functions for ML operations:
- Text preprocessing
- Feature extraction
- Model serialization
- Data validation
"""

from .text import preprocess_text, clean_text, tokenize_text, normalize_text
from .features import extract_features, create_feature_vector
from .serialization import save_model, load_model, serialize_model
from .validation import validate_input, validate_output

__all__ = [
    "preprocess_text",
    "clean_text",
    "tokenize_text",
    "normalize_text",
    "extract_features",
    "create_feature_vector",
    "save_model",
    "load_model",
    "serialize_model",
    "validate_input",
    "validate_output",
]

# For backward compatibility
text_preprocessing = preprocess_text
feature_extraction = extract_features
model_serialization = serialize_model
