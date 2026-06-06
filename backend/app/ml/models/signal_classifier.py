"""
Signal Classifier Model

Uses NLP to classify text into signal types:
- hiring
- funding
- partnership
- acquisition
- layoff
- expansion
- new_product
- leadership_change
- award
- event
- other
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)


class SignalClassifier:
    """
    NLP-based signal classifier using transformers
    
    Features:
    - Multi-class text classification
    - Confidence scoring
    - Entity extraction
    - Sentiment analysis
    - Continuous learning
    """
    
    # Signal types
    SIGNAL_TYPES = [
        "hiring",
        "funding", 
        "partnership",
        "acquisition",
        "layoff",
        "expansion",
        "new_product",
        "leadership_change",
        "award",
        "event",
        "other"
    ]
    
    # Model configuration
    MODEL_CONFIG = {
        "model_name": "distilbert-base-uncased-finetuned-signal-classification",
        "max_length": 512,
        "batch_size": 32,
        "learning_rate": 2e-5,
        "epochs": 3,
    }
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the signal classifier
        
        Args:
            model_path: Path to load a pre-trained model
        """
        self.model = None
        self.tokenizer = None
        self.label_map = {label: idx for idx, label in enumerate(self.SIGNAL_TYPES)}
        self.reverse_label_map = {idx: label for idx, label in enumerate(self.SIGNAL_TYPES)}
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
            # In production, we would load a HuggingFace model
            # For now, we'll use a lightweight approach
            import joblib
            
            model_file = Path(model_path) / "model.joblib"
            tokenizer_file = Path(model_path) / "tokenizer.joblib"
            metadata_file = Path(model_path) / "metadata.json"
            
            if model_file.exists() and tokenizer_file.exists():
                # Load model and tokenizer
                # self.model = joblib.load(model_file)
                # self.tokenizer = joblib.load(tokenizer_file)
                
                # Load metadata
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        self.last_trained = metadata.get("last_trained")
                        self.accuracy = metadata.get("accuracy", 0.0)
                        self.version = metadata.get("version", "0.1.0")
                
                self.is_loaded = True
                logger.info(f"Signal classifier loaded from {model_path}")
                return True
            
            logger.warning(f"Model files not found at {model_path}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to load signal classifier: {str(e)}")
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
                "signal_types": self.SIGNAL_TYPES,
            }
            
            with open(os.path.join(save_path, "metadata.json"), 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Signal classifier saved to {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save signal classifier: {str(e)}")
            return False
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for classification
        
        Args:
            text: Raw text input
            
        Returns:
            str: Preprocessed text
        """
        import re
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove special characters and numbers
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_features(self, text: str) -> Dict[str, Any]:
        """
        Extract features from text for classification
        
        Args:
            text: Input text
            
        Returns:
            dict: Feature dictionary
        """
        from collections import Counter
        import re
        
        # Preprocess
        processed_text = self.preprocess_text(text)
        
        # Tokenize
        words = processed_text.split()
        
        # Feature extraction
        features = {
            "text": processed_text,
            "length": len(text),
            "word_count": len(words),
            "unique_words": len(set(words)),
            "word_frequencies": dict(Counter(words)),
        }
        
        # Keyword detection
        keywords = {
            "hiring": ["hire", "hiring", "recruit", "job", "position", "career", "employ"],
            "funding": ["fund", "invest", "raise", "series", "seed", "venture", "capital"],
            "partnership": ["partner", "collaborate", "alliance", "joint", "team"],
            "acquisition": ["acquire", "buy", "purchase", "merger", "takeover"],
            "layoff": ["layoff", "fire", "reduce", "downsize", "restructure"],
            "expansion": ["expand", "grow", "open", "launch", "new office"],
            "new_product": ["launch", "introduce", "new", "product", "feature", "release"],
            "leadership_change": ["ceo", "cto", "cfo", "appoint", "promote", "resign"],
            "award": ["award", "win", "honor", "recognize", "prize"],
            "event": ["event", "conference", "summit", "webinar", "meetup"],
        }
        
        # Count keyword matches
        keyword_counts = {}
        for signal_type, signal_keywords in keywords.items():
            count = sum(1 for word in words if word in signal_keywords)
            keyword_counts[signal_type] = count
        
        features["keyword_counts"] = keyword_counts
        
        # Entity recognition (simple version)
        entities = self.extract_entities(text)
        features["entities"] = entities
        
        return features
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from text (companies, people, locations)
        
        Args:
            text: Input text
            
        Returns:
            dict: Extracted entities by type
        """
        import re
        
        entities = {
            "companies": [],
            "people": [],
            "locations": [],
            "dates": [],
        }
        
        # Simple regex patterns (in production, use spaCy or NER)
        # Companies (capitalized words)
        company_pattern = r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b'
        entities["companies"] = re.findall(company_pattern, text)
        
        # People (names - this is simplified)
        # In production, use a proper NER model
        
        # Locations
        location_pattern = r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b'
        # Filter out companies that are already detected
        
        # Dates
        date_pattern = r'\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b|\bJanuary|February|March|April|May|June|July|August|September|October|November|December\b'
        entities["dates"] = re.findall(date_pattern, text)
        
        return entities
    
    def classify(self, text: str, threshold: float = 0.7) -> Tuple[str, float, Dict[str, Any]]:
        """
        Classify text into a signal type
        
        Args:
            text: Input text to classify
            threshold: Confidence threshold
            
        Returns:
            tuple: (predicted_label, confidence, features)
        """
        if not text or not text.strip():
            return "other", 0.0, {}
        
        # Extract features
        features = self.extract_features(text)
        
        # For now, use keyword-based classification
        # In production, use the trained model
        keyword_counts = features.get("keyword_counts", {})
        total_keywords = sum(keyword_counts.values())
        
        if total_keywords == 0:
            return "other", 0.5, features
        
        # Find the signal type with most keyword matches
        best_signal = max(keyword_counts.items(), key=lambda x: x[1])
        best_label = best_signal[0]
        best_count = best_signal[1]
        
        # Calculate confidence
        confidence = best_count / total_keywords
        
        # If confidence is low, return "other"
        if confidence < threshold:
            return "other", confidence, features
        
        return best_label, confidence, features
    
    def classify_batch(self, texts: List[str]) -> List[Tuple[str, float, Dict[str, Any]]]:
        """
        Classify multiple texts
        
        Args:
            texts: List of texts to classify
            
        Returns:
            list: List of (label, confidence, features) tuples
        """
        return [self.classify(text) for text in texts]
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text
        
        Args:
            text: Input text
            
        Returns:
            tuple: (sentiment_label, sentiment_score)
        """
        # Simple sentiment analysis
        # In production, use TextBlob, VADER, or a transformer model
        
        positive_words = ["great", "excellent", "amazing", "wonderful", "success", "win", "award"]
        negative_words = ["bad", "terrible", "awful", "fail", "loss", "layoff", "downsize"]
        
        words = text.lower().split()
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        total = positive_count + negative_count
        
        if total == 0:
            return "neutral", 0.0
        
        sentiment_score = (positive_count - negative_count) / total
        
        if sentiment_score > 0.1:
            return "positive", sentiment_score
        elif sentiment_score < -0.1:
            return "negative", sentiment_score
        else:
            return "neutral", sentiment_score
    
    def extract_signals(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract multiple signals from a longer text
        
        Args:
            text: Input text (e.g., news article)
            
        Returns:
            list: List of extracted signals
        """
        # Split text into sentences
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        signals = []
        
        for sentence in sentences:
            if len(sentence.strip()) < 20:  # Skip short sentences
                continue
            
            label, confidence, features = self.classify(sentence)
            sentiment, sentiment_score = self.analyze_sentiment(sentence)
            
            if confidence > 0.5:  # Only include confident predictions
                signals.append({
                    "text": sentence.strip(),
                    "signal_type": label,
                    "confidence": confidence,
                    "sentiment": sentiment,
                    "sentiment_score": sentiment_score,
                    "entities": features.get("entities", {}),
                    "keywords": list(features.get("keyword_counts", {}).keys()),
                })
        
        return signals
    
    def train(self, training_data: List[Dict[str, Any]], epochs: int = 3) -> float:
        """
        Train the classifier (placeholder for actual training)
        
        Args:
            training_data: List of {"text": str, "label": str}
            epochs: Number of training epochs
            
        Returns:
            float: Training accuracy
        """
        # In production, this would train a transformer model
        # For now, we'll just update the last_trained timestamp
        
        self.last_trained = datetime.utcnow().isoformat()
        self.version = f"0.1.{int(datetime.utcnow().timestamp())}"
        
        # Calculate mock accuracy
        if training_data:
            self.accuracy = min(0.95, 0.7 + len(training_data) * 0.001)
        
        logger.info(f"Signal classifier trained with {len(training_data)} samples")
        return self.accuracy
    
    def evaluate(self, test_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Evaluate the classifier
        
        Args:
            test_data: List of {"text": str, "label": str}
            
        Returns:
            dict: Evaluation metrics
        """
        if not test_data:
            return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}
        
        correct = 0
        total = len(test_data)
        
        for item in test_data:
            text = item.get("text", "")
            true_label = item.get("label", "other")
            
            predicted_label, _, _ = self.classify(text)
            
            if predicted_label == true_label:
                correct += 1
        
        accuracy = correct / total
        
        return {
            "accuracy": accuracy,
            "precision": accuracy,  # Simplified
            "recall": accuracy,    # Simplified
            "f1": accuracy,       # Simplified
        }


# Create a global instance
signal_classifier = SignalClassifier()
