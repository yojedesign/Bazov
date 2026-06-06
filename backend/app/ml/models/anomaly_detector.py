"""
Anomaly Detector Model

Detects unusual patterns in:
- Signal activity
- User behavior
- Network changes
- Data quality issues
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    Anomaly detection using statistical methods and ML
    
    Features:
    - Signal anomaly detection (unusual signal patterns)
    - User behavior anomaly detection
    - Network change detection
    - Data quality monitoring
    """
    
    # Anomaly types
    ANOMALY_TYPES = [
        "signal_spike",           # Sudden increase in signals
        "signal_drop",            # Sudden decrease in signals
        "unusual_signal_type",    # Rare signal type detected
        "user_activity_spike",    # User suddenly very active
        "user_inactivity",        # User suddenly inactive
        "network_growth_spike",   # Sudden network growth
        "network_shrinkage",      # Sudden network shrinkage
        "data_quality_issue",     # Data quality problems
    ]
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the anomaly detector
        
        Args:
            model_path: Path to load a pre-trained model
        """
        # Historical data storage
        self.signal_history = defaultdict(list)  # signal_type -> [counts]
        self.user_activity_history = defaultdict(list)  # user_id -> [activity_scores]
        self.network_size_history = defaultdict(list)  # user_id -> [network_sizes]
        
        # Thresholds
        self.thresholds = {
            "signal_spike": 3.0,      # 3 standard deviations above mean
            "signal_drop": 3.0,       # 3 standard deviations below mean
            "user_activity_spike": 2.5,
            "user_inactivity": 2.5,
            "network_growth_spike": 2.0,
            "network_shrinkage": 2.0,
        }
        
        # Statistics
        self.signal_stats = {}  # signal_type -> {"mean": float, "std": float}
        self.user_stats = {}    # user_id -> {"mean": float, "std": float}
        
        # Model state
        self.is_loaded = False
        self.model_path = model_path
        self.last_trained = None
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
            history_file = Path(model_path) / "history.json"
            thresholds_file = Path(model_path) / "thresholds.json"
            
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    self.last_trained = metadata.get("last_trained")
                    self.version = metadata.get("version", "0.1.0")
            
            if history_file.exists():
                with open(history_file, 'r') as f:
                    history = json.load(f)
                    self.signal_history = defaultdict(list, history.get("signal_history", {}))
                    self.user_activity_history = defaultdict(list, history.get("user_activity_history", {}))
                    self.network_size_history = defaultdict(list, history.get("network_size_history", {}))
            
            if thresholds_file.exists():
                with open(thresholds_file, 'r') as f:
                    self.thresholds = json.load(f)
            
            # Calculate statistics from history
            self._calculate_statistics()
            
            self.is_loaded = True
            logger.info(f"Anomaly detector loaded from {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load anomaly detector: {str(e)}")
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
            }
            
            with open(os.path.join(save_path, "metadata.json"), 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Save history
            history = {
                "signal_history": dict(self.signal_history),
                "user_activity_history": dict(self.user_activity_history),
                "network_size_history": dict(self.network_size_history),
            }
            
            with open(os.path.join(save_path, "history.json"), 'w') as f:
                json.dump(history, f, indent=2)
            
            # Save thresholds
            with open(os.path.join(save_path, "thresholds.json"), 'w') as f:
                json.dump(self.thresholds, f, indent=2)
            
            logger.info(f"Anomaly detector saved to {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save anomaly detector: {str(e)}")
            return False
    
    def _calculate_statistics(self) -> None:
        """Calculate statistics from historical data"""
        # Calculate signal statistics
        for signal_type, counts in self.signal_history.items():
            if len(counts) > 1:
                mean = np.mean(counts)
                std = np.std(counts)
                self.signal_stats[signal_type] = {"mean": mean, "std": std}
        
        # Calculate user statistics
        for user_id, scores in self.user_activity_history.items():
            if len(scores) > 1:
                mean = np.mean(scores)
                std = np.std(scores)
                self.user_stats[user_id] = {"mean": mean, "std": std}
    
    def record_signal(self, signal_type: str, timestamp: Optional[datetime] = None) -> None:
        """
        Record a signal for anomaly detection
        
        Args:
            signal_type: Type of signal
            timestamp: Timestamp of the signal
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Get date key (YYYY-MM-DD)
        date_key = timestamp.strftime("%Y-%m-%d")
        
        # Record signal
        self.signal_history[signal_type].append(date_key)
        
        # Keep only last 30 days of history
        if len(self.signal_history[signal_type]) > 30:
            self.signal_history[signal_type] = self.signal_history[signal_type][-30:]
        
        # Recalculate statistics
        self._calculate_statistics()
    
    def record_user_activity(self, user_id: str, activity_score: float, timestamp: Optional[datetime] = None) -> None:
        """
        Record user activity for anomaly detection
        
        Args:
            user_id: User ID
            activity_score: Activity score (0-1)
            timestamp: Timestamp of the activity
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Get date key (YYYY-MM-DD)
        date_key = timestamp.strftime("%Y-%m-%d")
        
        # Record activity
        self.user_activity_history[user_id].append(activity_score)
        
        # Keep only last 30 days of history
        if len(self.user_activity_history[user_id]) > 30:
            self.user_activity_history[user_id] = self.user_activity_history[user_id][-30:]
        
        # Recalculate statistics
        self._calculate_statistics()
    
    def record_network_size(self, user_id: str, network_size: int, timestamp: Optional[datetime] = None) -> None:
        """
        Record network size for anomaly detection
        
        Args:
            user_id: User ID
            network_size: Size of the user's network
            timestamp: Timestamp of the measurement
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Get date key (YYYY-MM-DD)
        date_key = timestamp.strftime("%Y-%m-%d")
        
        # Record network size
        self.network_size_history[user_id].append(network_size)
        
        # Keep only last 30 days of history
        if len(self.network_size_history[user_id]) > 30:
            self.network_size_history[user_id] = self.network_size_history[user_id][-30:]
    
    def detect_signal_anomalies(self) -> List[Dict[str, Any]]:
        """
        Detect anomalies in signal patterns
        
        Returns:
            list: List of detected anomalies
        """
        anomalies = []
        
        for signal_type, dates in self.signal_history.items():
            if len(dates) < 2:
                continue
            
            # Count signals per day
            date_counts = defaultdict(int)
            for date in dates:
                date_counts[date] += 1
            
            # Get recent counts
            recent_dates = sorted(date_counts.keys())[-7:]  # Last 7 days
            recent_counts = [date_counts[date] for date in recent_dates]
            
            if len(recent_counts) < 2:
                continue
            
            mean = np.mean(recent_counts)
            std = np.std(recent_counts)
            
            if std == 0:
                continue
            
            # Check for spikes
            latest_count = recent_counts[-1]
            z_score = (latest_count - mean) / std if std > 0 else 0
            
            if z_score > self.thresholds.get("signal_spike", 3.0):
                anomalies.append({
                    "type": "signal_spike",
                    "signal_type": signal_type,
                    "current_count": latest_count,
                    "mean": mean,
                    "std": std,
                    "z_score": z_score,
                    "severity": "high" if z_score > 4.0 else "medium",
                    "timestamp": datetime.utcnow().isoformat(),
                })
            
            elif z_score < -self.thresholds.get("signal_drop", 3.0):
                anomalies.append({
                    "type": "signal_drop",
                    "signal_type": signal_type,
                    "current_count": latest_count,
                    "mean": mean,
                    "std": std,
                    "z_score": z_score,
                    "severity": "high" if z_score < -4.0 else "medium",
                    "timestamp": datetime.utcnow().isoformat(),
                })
        
        return anomalies
    
    def detect_user_anomalies(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Detect anomalies in user behavior
        
        Args:
            user_id: User ID
            
        Returns:
            list: List of detected anomalies
        """
        anomalies = []
        
        # Check activity anomalies
        if user_id in self.user_activity_history and len(self.user_activity_history[user_id]) >= 2:
            activity_scores = self.user_activity_history[user_id][-7:]  # Last 7 days
            
            if len(activity_scores) >= 2:
                mean = np.mean(activity_scores)
                std = np.std(activity_scores)
                
                if std > 0:
                    latest_score = activity_scores[-1]
                    z_score = (latest_score - mean) / std
                    
                    if z_score > self.thresholds.get("user_activity_spike", 2.5):
                        anomalies.append({
                            "type": "user_activity_spike",
                            "user_id": user_id,
                            "current_score": latest_score,
                            "mean": mean,
                            "std": std,
                            "z_score": z_score,
                            "severity": "high" if z_score > 3.5 else "medium",
                            "timestamp": datetime.utcnow().isoformat(),
                        })
                    
                    elif z_score < -self.thresholds.get("user_inactivity", 2.5):
                        anomalies.append({
                            "type": "user_inactivity",
                            "user_id": user_id,
                            "current_score": latest_score,
                            "mean": mean,
                            "std": std,
                            "z_score": z_score,
                            "severity": "high" if z_score < -3.5 else "medium",
                            "timestamp": datetime.utcnow().isoformat(),
                        })
        
        # Check network anomalies
        if user_id in self.network_size_history and len(self.network_size_history[user_id]) >= 2:
            network_sizes = self.network_size_history[user_id][-7:]  # Last 7 days
            
            if len(network_sizes) >= 2:
                mean = np.mean(network_sizes)
                std = np.std(network_sizes)
                
                if std > 0:
                    latest_size = network_sizes[-1]
                    z_score = (latest_size - mean) / std
                    
                    if z_score > self.thresholds.get("network_growth_spike", 2.0):
                        anomalies.append({
                            "type": "network_growth_spike",
                            "user_id": user_id,
                            "current_size": latest_size,
                            "mean": mean,
                            "std": std,
                            "z_score": z_score,
                            "severity": "high" if z_score > 3.0 else "medium",
                            "timestamp": datetime.utcnow().isoformat(),
                        })
                    
                    elif z_score < -self.thresholds.get("network_shrinkage", 2.0):
                        anomalies.append({
                            "type": "network_shrinkage",
                            "user_id": user_id,
                            "current_size": latest_size,
                            "mean": mean,
                            "std": std,
                            "z_score": z_score,
                            "severity": "high" if z_score < -3.0 else "medium",
                            "timestamp": datetime.utcnow().isoformat(),
                        })
        
        return anomalies
    
    def detect_data_quality_anomalies(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect data quality issues
        
        Args:
            data: Data to check for quality issues
            
        Returns:
            list: List of detected anomalies
        """
        anomalies = []
        
        # Check for missing required fields
        required_fields = ["id", "created_at"]
        for field in required_fields:
            if field not in data:
                anomalies.append({
                    "type": "data_quality_issue",
                    "issue": "missing_required_field",
                    "field": field,
                    "severity": "high",
                    "timestamp": datetime.utcnow().isoformat(),
                })
        
        # Check for invalid values
        if "confidence" in data:
            confidence = data["confidence"]
            if not (0 <= confidence <= 1):
                anomalies.append({
                    "type": "data_quality_issue",
                    "issue": "invalid_confidence",
                    "value": confidence,
                    "expected": "0 <= confidence <= 1",
                    "severity": "medium",
                    "timestamp": datetime.utcnow().isoformat(),
                })
        
        if "sentiment_score" in data:
            sentiment = data["sentiment_score"]
            if not (-1 <= sentiment <= 1):
                anomalies.append({
                    "type": "data_quality_issue",
                    "issue": "invalid_sentiment_score",
                    "value": sentiment,
                    "expected": "-1 <= sentiment_score <= 1",
                    "severity": "medium",
                    "timestamp": datetime.utcnow().isoformat(),
                })
        
        return anomalies
    
    def detect_all_anomalies(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Detect all types of anomalies
        
        Returns:
            dict: Dictionary of anomaly types to lists of anomalies
        """
        results = {
            "signal_anomalies": self.detect_signal_anomalies(),
            "user_anomalies": [],
            "data_quality_anomalies": [],
        }
        
        # Check user anomalies for all users
        for user_id in self.user_activity_history.keys():
            user_anomalies = self.detect_user_anomalies(user_id)
            if user_anomalies:
                results["user_anomalies"].extend(user_anomalies)
        
        return results
    
    def get_anomaly_summary(self) -> Dict[str, Any]:
        """
        Get a summary of recent anomalies
        
        Returns:
            dict: Anomaly summary statistics
        """
        all_anomalies = self.detect_all_anomalies()
        
        summary = {
            "total_anomalies": 0,
            "by_type": {},
            "by_severity": {"high": 0, "medium": 0, "low": 0},
            "recent_anomalies": all_anomalies,
        }
        
        for anomaly_type, anomalies in all_anomalies.items():
            summary["total_anomalies"] += len(anomalies)
            summary["by_type"][anomaly_type] = len(anomalies)
            
            for anomaly in anomalies:
                severity = anomaly.get("severity", "medium")
                summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
        
        return summary
    
    def update_thresholds(self, new_thresholds: Dict[str, float]) -> None:
        """
        Update anomaly detection thresholds
        
        Args:
            new_thresholds: Dictionary of new thresholds
        """
        for anomaly_type, threshold in new_thresholds.items():
            if anomaly_type in self.thresholds:
                self.thresholds[anomaly_type] = threshold
        
        logger.info("Anomaly detection thresholds updated")
    
    def train(self, training_data: List[Dict[str, Any]], epochs: int = 10) -> float:
        """
        Train the anomaly detector (placeholder)
        
        Args:
            training_data: Training data
            epochs: Number of training epochs
            
        Returns:
            float: Training accuracy
        """
        self.last_trained = datetime.utcnow().isoformat()
        self.version = f"0.1.{int(datetime.utcnow().timestamp())}"
        
        logger.info(f"Anomaly detector trained with {len(training_data)} samples")
        return 0.90  # Mock accuracy


# Create a global instance
anomaly_detector = AnomalyDetector()
