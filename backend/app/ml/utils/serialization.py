"""
Model Serialization Utilities

Provides functions for saving and loading ML models
"""

import pickle
import json
from pathlib import Path
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


def save_model(model: Any, path: str) -> None:
    """
    Save a model to disk
    
    Args:
        model: Model to save
        path: Path to save the model
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(path, "wb") as f:
            pickle.dump(model, f)
        logger.info(f"Model saved to {path}")
    except Exception as e:
        logger.error(f"Failed to save model: {e}")
        raise


def load_model(path: str) -> Any:
    """
    Load a model from disk
    
    Args:
        path: Path to the model file
        
    Returns:
        Loaded model
    """
    path = Path(path)
    
    if not path.exists():
        logger.error(f"Model file not found: {path}")
        raise FileNotFoundError(f"Model file not found: {path}")
    
    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
        logger.info(f"Model loaded from {path}")
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


def serialize_model(model: Any) -> Optional[str]:
    """
    Serialize a model to a string
    
    Args:
        model: Model to serialize
        
    Returns:
        Serialized model as string, or None if failed
    """
    try:
        import pickle
        return pickle.dumps(model).hex()
    except Exception as e:
        logger.error(f"Failed to serialize model: {e}")
        return None
