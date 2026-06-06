"""
Anomaly Detection Service

Provides high-level anomaly detection functionality
"""

from typing import List, Dict, Any, Optional
from app.ml.models.anomaly_detector import AnomalyDetector

# Create a global anomaly detector instance
anomaly_detector = AnomalyDetector()


class AnomalyDetectionService:
    """
    Service for detecting anomalies
    """
    
    def __init__(self, detector: Optional[AnomalyDetector] = None):
        """
        Initialize the anomaly detection service
        
        Args:
            detector: Anomaly detector to use
        """
        self.detector = detector or AnomalyDetector()
    
    def detect_anomalies(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect anomalies in the given data
        
        Args:
            data: List of data points to check
            
        Returns:
            List of detected anomalies
        """
        return self.detector.detect(data)
    
    def get_anomaly_score(self, data_point: Dict[str, Any]) -> float:
        """
        Get anomaly score for a single data point
        
        Args:
            data_point: Data point to score
            
        Returns:
            Anomaly score (higher = more anomalous)
        """
        return self.detector.get_score(data_point)
