"""
Data Validation Utilities

Provides functions for validating ML input and output data
"""

from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


def validate_input(data: Any, expected_type: type, min_value: Optional[float] = None, max_value: Optional[float] = None) -> bool:
    """
    Validate input data
    
    Args:
        data: Data to validate
        expected_type: Expected type of the data
        min_value: Minimum value (for numeric data)
        max_value: Maximum value (for numeric data)
        
    Returns:
        True if valid, False otherwise
    """
    # Check type
    if not isinstance(data, expected_type):
        logger.warning(f"Invalid type: expected {expected_type}, got {type(data)}")
        return False
    
    # Check numeric bounds
    if isinstance(data, (int, float)):
        if min_value is not None and data < min_value:
            logger.warning(f"Value below minimum: {data} < {min_value}")
            return False
        if max_value is not None and data > max_value:
            logger.warning(f"Value above maximum: {data} > {max_value}")
            return False
    
    return True


def validate_output(data: Any, expected_schema: Dict[str, type]) -> bool:
    """
    Validate output data against a schema
    
    Args:
        data: Data to validate
        expected_schema: Dictionary mapping field names to expected types
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(data, dict):
        logger.warning(f"Output is not a dictionary: {type(data)}")
        return False
    
    for field, expected_type in expected_schema.items():
        if field not in data:
            logger.warning(f"Missing field: {field}")
            return False
        if not isinstance(data[field], expected_type):
            logger.warning(f"Invalid type for field {field}: expected {expected_type}, got {type(data[field])}")
            return False
    
    return True
