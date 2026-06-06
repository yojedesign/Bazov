"""
Signal Classifier Trainer

Provides training pipeline for the signal classifier
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
import numpy as np

from app.ml.models.signal_classifier import SignalClassifier, signal_classifier
from app.core.config import settings

logger = logging.getLogger(__name__)


class SignalTrainer:
    """
    Trainer for the signal classifier model
    
    Features:
    - Load and preprocess training data
    - Train the classifier
    - Evaluate performance
    - Save trained models
    - Cross-validation
    """
    
    def __init__(self, model: Optional[SignalClassifier] = None):
        """
        Initialize the signal trainer
        
        Args:
            model: Signal classifier model to train
        """
        self.model = model or signal_classifier
        self.training_history = []
        self.best_accuracy = 0.0
        self.best_model_path = None
    
    def load_training_data(
        self,
        data_path: str,
        format: str = "json",
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Load training data from file
        
        Args:
            data_path: Path to training data file
            format: File format (json, csv)
            test_size: Proportion of data to use for testing
            random_state: Random seed for reproducibility
            
        Returns:
            tuple: (training_data, test_data)
        """
        try:
            if format == "json":
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif format == "csv":
                import pandas as pd
                df = pd.read_csv(data_path)
                data = df.to_dict('records')
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            # Shuffle data
            import random
            random.seed(random_state)
            random.shuffle(data)
            
            # Split into train and test
            split_idx = int(len(data) * (1 - test_size))
            train_data = data[:split_idx]
            test_data = data[split_idx:]
            
            logger.info(f"Loaded {len(data)} samples: {len(train_data)} train, {len(test_data)} test")
            return train_data, test_data
            
        except Exception as e:
            logger.error(f"Failed to load training data: {str(e)}")
            raise
    
    def preprocess_data(
        self,
        data: List[Dict[str, Any]],
        text_field: str = "text",
        label_field: str = "label",
    ) -> List[Dict[str, Any]]:
        """
        Preprocess training data
        
        Args:
            data: Raw training data
            text_field: Name of the text field
            label_field: Name of the label field
            
        Returns:
            list: Preprocessed training data
        """
        processed_data = []
        
        for item in data:
            text = item.get(text_field, "")
            label = item.get(label_field, "other")
            
            # Validate label
            if label not in self.model.SIGNAL_TYPES:
                label = "other"
            
            processed_data.append({
                "text": text,
                "label": label,
            })
        
        return processed_data
    
    def train(
        self,
        training_data: List[Dict[str, Any]],
        epochs: int = 3,
        batch_size: int = 32,
        learning_rate: float = 2e-5,
        validation_data: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Train the signal classifier
        
        Args:
            training_data: Training data
            epochs: Number of training epochs
            batch_size: Batch size
            learning_rate: Learning rate
            validation_data: Optional validation data
            
        Returns:
            dict: Training results
        """
        try:
            start_time = datetime.utcnow()
            
            # Preprocess data
            processed_data = self.preprocess_data(training_data)
            
            # Train the model
            accuracy = self.model.train(processed_data, epochs)
            
            # Evaluate on validation data if provided
            eval_results = {}
            if validation_data:
                eval_results = self.model.evaluate(self.preprocess_data(validation_data))
            
            # Calculate training time
            training_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Record training history
            training_record = {
                "timestamp": datetime.utcnow().isoformat(),
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "training_samples": len(training_data),
                "training_accuracy": accuracy,
                "validation_results": eval_results,
                "training_time_seconds": training_time,
            }
            
            self.training_history.append(training_record)
            
            # Update best accuracy
            if accuracy > self.best_accuracy:
                self.best_accuracy = accuracy
            
            logger.info(f"Training completed: accuracy={accuracy:.4f}, time={training_time:.2f}s")
            
            return {
                "status": "success",
                "accuracy": accuracy,
                "training_time_seconds": training_time,
                "evaluation": eval_results,
                "model_version": self.model.version,
            }
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
            }
    
    def evaluate(
        self,
        test_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Evaluate the model on test data
        
        Args:
            test_data: Test data
            
        Returns:
            dict: Evaluation results
        """
        try:
            processed_data = self.preprocess_data(test_data)
            results = self.model.evaluate(processed_data)
            
            return {
                "status": "success",
                "results": results,
            }
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
            }
    
    def cross_validate(
        self,
        data: List[Dict[str, Any]],
        folds: int = 5,
        epochs: int = 3,
    ) -> Dict[str, Any]:
        """
        Perform cross-validation
        
        Args:
            data: Training data
            folds: Number of folds
            epochs: Number of training epochs per fold
            
        Returns:
            dict: Cross-validation results
        """
        try:
            import random
            from sklearn.model_selection import KFold
            
            # Preprocess data
            processed_data = self.preprocess_data(data)
            
            # Prepare data for KFold
            texts = [item["text"] for item in processed_data]
            labels = [item["label"] for item in processed_data]
            
            kf = KFold(n_splits=folds, shuffle=True, random_state=42)
            
            fold_results = []
            
            for fold_idx, (train_index, test_index) in enumerate(kf.split(texts)):
                train_texts = [texts[i] for i in train_index]
                train_labels = [labels[i] for i in train_index]
                test_texts = [texts[i] for i in test_index]
                test_labels = [labels[i] for i in test_index]
                
                # Create training and test data
                train_data = [{"text": t, "label": l} for t, l in zip(train_texts, train_labels)]
                test_data = [{"text": t, "label": l} for t, l in zip(test_texts, test_labels)]
                
                # Train
                self.model.train(train_data, epochs)
                
                # Evaluate
                results = self.model.evaluate(test_data)
                fold_results.append(results)
            
            # Calculate average results
            avg_accuracy = np.mean([r.get("accuracy", 0) for r in fold_results])
            avg_precision = np.mean([r.get("precision", 0) for r in fold_results])
            avg_recall = np.mean([r.get("recall", 0) for r in fold_results])
            avg_f1 = np.mean([r.get("f1", 0) for r in fold_results])
            
            return {
                "status": "success",
                "folds": folds,
                "average_accuracy": float(avg_accuracy),
                "average_precision": float(avg_precision),
                "average_recall": float(avg_recall),
                "average_f1": float(avg_f1),
                "fold_results": fold_results,
            }
            
        except Exception as e:
            logger.error(f"Cross-validation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
            }
    
    def save_model(
        self,
        save_path: str,
        overwrite: bool = False,
    ) -> Dict[str, Any]:
        """
        Save the trained model
        
        Args:
            save_path: Directory to save the model
            overwrite: Whether to overwrite existing model
            
        Returns:
            dict: Save results
        """
        try:
            # Check if directory exists
            if os.path.exists(save_path) and not overwrite:
                return {
                    "status": "error",
                    "error": f"Directory {save_path} already exists. Set overwrite=True to overwrite.",
                }
            
            # Save the model
            success = self.model.save_model(save_path)
            
            if success:
                self.best_model_path = save_path
                logger.info(f"Model saved to {save_path}")
                
                return {
                    "status": "success",
                    "save_path": save_path,
                    "model_version": self.model.version,
                }
            else:
                return {
                    "status": "error",
                    "error": "Failed to save model",
                }
            
        except Exception as e:
            logger.error(f"Failed to save model: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
            }
    
    def load_model(
        self,
        model_path: str,
    ) -> Dict[str, Any]:
        """
        Load a trained model
        
        Args:
            model_path: Path to the model directory
            
        Returns:
            dict: Load results
        """
        try:
            success = self.model.load_model(model_path)
            
            if success:
                logger.info(f"Model loaded from {model_path}")
                
                return {
                    "status": "success",
                    "model_path": model_path,
                    "model_version": self.model.version,
                }
            else:
                return {
                    "status": "error",
                    "error": "Failed to load model",
                }
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
            }
    
    def get_training_history(self) -> List[Dict[str, Any]]:
        """
        Get training history
        
        Returns:
            list: Training history records
        """
        return self.training_history.copy()
    
    def get_best_model(self) -> Dict[str, Any]:
        """
        Get information about the best model
        
        Returns:
            dict: Best model information
        """
        return {
            "best_accuracy": self.best_accuracy,
            "best_model_path": self.best_model_path,
            "current_model_version": self.model.version,
        }


# Create a global instance
signal_trainer = SignalTrainer()
