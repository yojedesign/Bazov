"""
Signal Processing Service

Provides NLP-powered signal extraction and classification
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from app.ml.models.signal_classifier import signal_classifier
from app.db.session import AsyncSession
from app.db.models.signal import Signal as SignalDB

logger = logging.getLogger(__name__)


class SignalProcessingService:
    """
    Service for processing and classifying signals
    
    Features:
    - Extract signals from text
    - Classify signal types
    - Analyze sentiment
    - Extract entities
    - Store processed signals
    """
    
    def __init__(self):
        """Initialize the signal processing service"""
        self.classifier = signal_classifier
    
    async def process_text(
        self,
        text: str,
        source_url: Optional[str] = None,
        source_type: str = "text",
        company_id: Optional[str] = None,
        person_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Process text and extract signals
        
        Args:
            text: Input text to process
            source_url: URL of the source
            source_type: Type of source (text, news, linkedin, etc.)
            company_id: Optional company ID to associate
            person_id: Optional person ID to associate
            
        Returns:
            list: List of extracted signals
        """
        if not text or not text.strip():
            return []
        
        # Extract signals from text
        signals = self.classifier.extract_signals(text)
        
        # Enrich signals with metadata
        processed_signals = []
        for signal in signals:
            processed_signal = {
                "text": signal.get("text", ""),
                "title": signal.get("text", "")[:100],  # Use first 100 chars as title
                "signal_type": signal.get("signal_type", "other"),
                "content": text,
                "source_url": source_url,
                "source_type": source_type,
                "company_id": company_id,
                "person_id": person_id,
                "confidence": signal.get("confidence", 0.5),
                "sentiment": signal.get("sentiment", "neutral"),
                "sentiment_score": signal.get("sentiment_score", 0.0),
                "entities": signal.get("entities", {}),
                "keywords": signal.get("keywords", []),
                "is_processed": True,
                "processed_at": datetime.utcnow().isoformat(),
            }
            processed_signals.append(processed_signal)
        
        return processed_signals
    
    async def classify_signal(self, text: str) -> Tuple[str, float, Dict[str, Any]]:
        """
        Classify a single signal
        
        Args:
            text: Signal text to classify
            
        Returns:
            tuple: (signal_type, confidence, features)
        """
        return self.classifier.classify(text)
    
    async def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            tuple: (sentiment_label, sentiment_score)
        """
        return self.classifier.analyze_sentiment(text)
    
    async def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from text
        
        Args:
            text: Text to extract entities from
            
        Returns:
            dict: Extracted entities by type
        """
        return self.classifier.extract_entities(text)
    
    async def process_and_store(
        self,
        db: AsyncSession,
        text: str,
        source_url: Optional[str] = None,
        source_type: str = "text",
        company_id: Optional[str] = None,
        person_id: Optional[str] = None,
    ) -> List[SignalDB]:
        """
        Process text and store extracted signals in database
        
        Args:
            db: Database session
            text: Input text to process
            source_url: URL of the source
            source_type: Type of source
            company_id: Optional company ID
            person_id: Optional person ID
            
        Returns:
            list: List of created Signal DB objects
        """
        # Process text to extract signals
        signals_data = await self.process_text(
            text, source_url, source_type, company_id, person_id
        )
        
        if not signals_data:
            return []
        
        # Store signals in database
        created_signals = []
        for signal_data in signals_data:
            signal = SignalDB(**signal_data)
            db.add(signal)
            created_signals.append(signal)
        
        await db.commit()
        
        for signal in created_signals:
            await db.refresh(signal)
        
        logger.info(f"Stored {len(created_signals)} signals from text processing")
        return created_signals
    
    async def batch_process(
        self,
        texts: List[str],
        source_urls: Optional[List[str]] = None,
        source_type: str = "text",
    ) -> List[List[Dict[str, Any]]]:
        """
        Process multiple texts in batch
        
        Args:
            texts: List of texts to process
            source_urls: Optional list of source URLs
            source_type: Type of source
            
        Returns:
            list: List of lists of extracted signals
        """
        results = []
        
        for i, text in enumerate(texts):
            source_url = source_urls[i] if source_urls and i < len(source_urls) else None
            signals = await self.process_text(text, source_url, source_type)
            results.append(signals)
        
        return results
    
    async def get_signal_types(self) -> List[str]:
        """
        Get all available signal types
        
        Returns:
            list: List of signal type strings
        """
        return self.classifier.SIGNAL_TYPES.copy()
    
    async def train_classifier(
        self,
        training_data: List[Dict[str, Any]],
        epochs: int = 3
    ) -> float:
        """
        Train the signal classifier
        
        Args:
            training_data: List of {"text": str, "label": str}
            epochs: Number of training epochs
            
        Returns:
            float: Training accuracy
        """
        return self.classifier.train(training_data, epochs)
    
    async def evaluate_classifier(
        self,
        test_data: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Evaluate the signal classifier
        
        Args:
            test_data: List of {"text": str, "label": str}
            
        Returns:
            dict: Evaluation metrics
        """
        return self.classifier.evaluate(test_data)
    
    async def get_classifier_stats(self) -> Dict[str, Any]:
        """
        Get classifier statistics
        
        Returns:
            dict: Classifier statistics
        """
        return {
            "is_loaded": self.classifier.is_loaded,
            "version": self.classifier.version,
            "last_trained": self.classifier.last_trained,
            "accuracy": self.classifier.accuracy,
            "signal_types": self.classifier.SIGNAL_TYPES,
        }


# Create a global instance
signal_processing_service = SignalProcessingService()
