# Machine Learning Integration for Bazov

## 🎯 Overview

Bazov's ML system provides intelligent features that continuously improve the platform's relationship intelligence capabilities. The system includes:

- **Signal Classification**: NLP-based extraction and classification of business signals
- **Relationship Strength Prediction**: ML model to score connection quality
- **Recommendation Engine**: Personalized suggestions for connections and content
- **Anomaly Detection**: Identify unusual patterns in network activity

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ML System Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ML Models                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │ Signal        │  │ Relationship │  │ Recommendation│    │   │
│  │  │ Classifier    │  │ Strength     │  │ Engine        │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  │  ┌──────────────┐                                              │   │
│  │  │ Anomaly      │                                              │   │
│  │  │ Detector     │                                              │   │
│  │  └──────────────┘                                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ▲  ▲  ▲  ▲                                 │
│                          │  │  │  │                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ML Services                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │ Signal        │  │ Relationship │  │ Recommendation│    │   │
│  │  │ Processing    │  │ Analysis     │  │ Service      │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  │  ┌──────────────┐                                              │   │
│  │  │ Anomaly      │                                              │   │
│  │  │ Detection    │                                              │   │
│  │  └──────────────┘                                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ▲  ▲  ▲  ▲                                 │
│                          │  │  │  │                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ML Training                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │ Signal        │  │ Relationship │  │ Recommendation│    │   │
│  │  │ Trainer       │  │ Trainer      │  │ Trainer       │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  │  ┌──────────────┐                                              │   │
│  │  │ Anomaly      │                                              │   │
│  │  │ Trainer      │                                              │   │
│  │  └──────────────┘                                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ▲  ▲  ▲  ▲                                 │
│                          │  │  │  │                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ML Utilities                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │ Text          │  │ Feature       │  │ Model         │    │   │
│  │  │ Preprocessing │  │ Extraction    │  │ Serialization │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 📚 Models

### 1. Signal Classifier

**Purpose**: Classify text into business signal types

**Signal Types**:
- `hiring` - Job postings, hiring announcements
- `funding` - Investment rounds, funding news
- `partnership` - Collaborations, alliances
- `acquisition` - Mergers, acquisitions
- `layoff` - Workforce reductions
- `expansion` - Growth, new markets
- `new_product` - Product launches
- `leadership_change` - Executive changes
- `award` - Recognition, achievements
- `event` - Conferences, meetups
- `other` - Miscellaneous

**Features**:
- Keyword-based classification (current)
- Transformer-based classification (future)
- Confidence scoring
- Entity extraction
- Sentiment analysis

**Example Usage**:
```python
from app.ml.models.signal_classifier import signal_classifier

# Classify a single text
signal_type, confidence, features = signal_classifier.classify(
    "Company X just raised $10M in Series A funding"
)
# Returns: ("funding", 0.95, {...})

# Extract signals from longer text
signals = signal_classifier.extract_signals(news_article)
# Returns: [{"text": "...", "signal_type": "funding", ...}, ...]

# Analyze sentiment
sentiment, score = signal_classifier.analyze_sentiment(text)
# Returns: ("positive", 0.8)
```

### 2. Relationship Strength Model

**Purpose**: Predict the strength of professional relationships (1-10 scale)

**Features Used**:
- Interaction frequency
- Time since last interaction
- Common connections count
- Profile similarity score
- Shared interests/skills
- Communication frequency
- Connection duration

**Strength Scale**:
- 1-3: Weak
- 4-6: Average
- 7-8: Strong
- 9-10: Exceptional

**Example Usage**:
```python
from app.ml.models.relationship_strength import relationship_strength_model

# Predict relationship strength
relationship_data = {
    "interaction_count": 25,
    "last_interaction": "2024-01-15",
    "common_connections": 8,
    "profile_similarity": 0.85,
    "shared_skills": 12,
    "communication_frequency": 0.7,
    "connection_duration_days": 365 * 2,
}

score, explanation = relationship_strength_model.predict(relationship_data)
# Returns: (8.2, {"score": 8.2, "label": "Excellent", "features": {...}, "recommendations": [...]})

# Calculate profile similarity
similarity = relationship_strength_model.calculate_profile_similarity(profile1, profile2)
# Returns: 0.75
```

### 3. Recommendation Model

**Purpose**: Provide personalized recommendations

**Recommendation Strategies**:
- Collaborative filtering (40% weight)
- Content-based filtering (30% weight)
- Popularity-based (10% weight)
- Trending (10% weight)
- Social connections (10% weight)

**Example Usage**:
```python
from app.ml.models.recommendation import recommendation_model

# Add user and item profiles
recommendation_model.add_user_profile("user1", {"industry": "tech", "skills": ["python", "ml"]})
recommendation_model.add_item_profile("person1", {"industry": "tech", "skills": ["python", "ai"]}, "person")

# Record interactions
recommendation_model.record_interaction("user1", "person1", "person", 1.0)

# Get recommendations
recommendations = recommendation_model.recommend_people("user1", limit=5)
# Returns: [{"person_id": "person2", "name": "...", "score": 0.95, ...}, ...]
```

### 4. Anomaly Detector

**Purpose**: Detect unusual patterns in the system

**Anomaly Types**:
- Signal spikes/drops
- User activity spikes/inactivity
- Network growth/shrinkage
- Data quality issues

**Example Usage**:
```python
from app.ml.models.anomaly_detector import anomaly_detector

# Record data for anomaly detection
anomaly_detector.record_signal("funding")
anomaly_detector.record_user_activity("user1", 0.8)
anomaly_detector.record_network_size("user1", 150)

# Detect anomalies
signal_anomalies = anomaly_detector.detect_signal_anomalies()
user_anomalies = anomaly_detector.detect_user_anomalies("user1")
data_anomalies = anomaly_detector.detect_data_quality_anomalies(data)

# Get summary
summary = anomaly_detector.get_anomaly_summary()
```

## 🔌 API Endpoints

### Signal Processing

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ml/signals/classify` | Classify signal text |
| POST | `/api/v1/ml/signals/extract` | Extract signals from text |
| POST | `/api/v1/ml/signals/analyze-sentiment` | Analyze text sentiment |
| POST | `/api/v1/ml/signals/extract-entities` | Extract entities from text |
| GET | `/api/v1/ml/signals/types` | Get all signal types |
| GET | `/api/v1/ml/signals/stats` | Get classifier statistics |
| POST | `/api/v1/ml/signals/batch-classify` | Classify multiple texts |

### Relationship Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ml/relationships/predict-strength` | Predict relationship strength |
| POST | `/api/v1/ml/relationships/analyze` | Comprehensive relationship analysis |
| POST | `/api/v1/ml/relationships/calculate-similarity` | Calculate profile similarity |
| POST | `/api/v1/ml/relationships/batch-predict` | Predict strength for multiple relationships |
| POST | `/api/v1/ml/relationships/get-distribution` | Get strength distribution |
| POST | `/api/v1/ml/relationships/get-suggestions` | Get improvement suggestions |
| GET | `/api/v1/ml/relationships/stats` | Get model statistics |

### Recommendations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ml/recommendations/people` | Recommend people to connect with |
| POST | `/api/v1/ml/recommendations/signals` | Recommend signals to follow |
| POST | `/api/v1/ml/recommendations/add-user-profile` | Add/update user profile |
| POST | `/api/v1/ml/recommendations/add-item-profile` | Add/update item profile |
| POST | `/api/v1/ml/recommendations/record-interaction` | Record user interaction |
| GET | `/api/v1/ml/recommendations/stats` | Get recommendation statistics |
| POST | `/api/v1/ml/recommendations/custom-recommend` | Custom recommendations with weights |

### Anomaly Detection

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ml/anomalies/detect-signal` | Detect signal anomalies |
| POST | `/api/v1/ml/anomalies/detect-user` | Detect user behavior anomalies |
| POST | `/api/v1/ml/anomalies/detect-data-quality` | Detect data quality issues |
| POST | `/api/v1/ml/anomalies/record-signal` | Record a signal |
| POST | `/api/v1/ml/anomalies/record-user-activity` | Record user activity |
| POST | `/api/v1/ml/anomalies/record-network-size` | Record network size |
| GET | `/api/v1/ml/anomalies/summary` | Get anomaly summary |
| GET | `/api/v1/ml/anomalies/detect-all` | Detect all anomalies |
| GET | `/api/v1/ml/anomalies/stats` | Get detector statistics |
| POST | `/api/v1/ml/anomalies/update-thresholds` | Update detection thresholds |

### Health & Monitoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/ml/health/` | Health check for all ML services |
| GET | `/api/v1/ml/health/detailed` | Detailed health with statistics |

## 🚀 Training Pipeline

### Signal Classifier Training

```python
from app.ml.training.signal_trainer import SignalTrainer

# Initialize trainer
trainer = SignalTrainer()

# Load training data
train_data, test_data = trainer.load_training_data(
    "data/signals/training.json",
    format="json",
    test_size=0.2
)

# Train the model
results = trainer.train(
    train_data,
    epochs=3,
    batch_size=32,
    validation_data=test_data
)

# Evaluate
results = trainer.evaluate(test_data)

# Cross-validation
cv_results = trainer.cross_validate(train_data, folds=5, epochs=3)

# Save the model
trainer.save_model("models/signal_classifier_v1")
```

### Training Data Format

**Signal Classification Data** (`training.json`):
```json
[
  {
    "text": "Company X raised $10M in Series A funding",
    "label": "funding"
  },
  {
    "text": "We're hiring a Senior Software Engineer",
    "label": "hiring"
  },
  {
    "text": "Company Y acquired Company Z for $50M",
    "label": "acquisition"
  }
]
```

**Relationship Strength Data** (`relationships.json`):
```json
[
  {
    "features": {
      "interaction_count": 25,
      "recency_score": 0.8,
      "common_connections": 8,
      "profile_similarity": 0.85,
      "shared_skills": 12,
      "communication_frequency": 0.7,
      "connection_duration": 0.5
    },
    "target": 8.2
  }
]
```

## 📊 Continuous Learning

### Learning Strategies

1. **User Feedback Loop**
   - Users can provide feedback on signal classifications
   - Feedback is used to retrain models periodically
   - Incorrect classifications are logged for review

2. **Active Learning**
   - System identifies uncertain predictions
   - Requests user confirmation for low-confidence predictions
   - Uses confirmed data to improve models

3. **Periodic Retraining**
   - Models are retrained weekly with new data
   - Cross-validation ensures model quality
   - Old models are archived for rollback

4. **Online Learning**
   - Some models support incremental updates
   - New data is incorporated without full retraining
   - Maintains model performance over time

### Implementation

```python
# Example: Continuous learning for signal classifier

# 1. Collect user feedback
feedback_data = [
    {"text": "...", "user_label": "funding", "model_label": "hiring"},
    # ... more feedback
]

# 2. Retrain model with feedback
trainer = SignalTrainer()
all_data = original_data + feedback_data
results = trainer.train(all_data, epochs=1)

# 3. Save new model version
trainer.save_model(f"models/signal_classifier_v{version}")

# 4. Update production model (with validation)
if results["accuracy"] > MIN_ACCURACY:
    signal_classifier.load_model(f"models/signal_classifier_v{version}")
```

## 🎛️ Monitoring & Maintenance

### Health Monitoring

The ML health endpoint provides:
- Model loading status
- Version information
- Last trained timestamp
- Accuracy metrics
- Data statistics

```bash
# Check ML health
curl http://localhost:8000/api/v1/ml/health/

# Get detailed statistics
curl http://localhost:8000/api/v1/ml/health/detailed
```

### Performance Metrics

Key metrics to monitor:
- **Accuracy**: Classification accuracy
- **Precision/Recall**: For each signal type
- **Latency**: Prediction time
- **Throughput**: Requests per second
- **Memory Usage**: Model memory footprint
- **Data Quality**: Input data quality scores

### Alerting

Anomaly detection triggers alerts for:
- Sudden drops in model accuracy
- Increased prediction latency
- Data quality issues
- Model loading failures

## 🔧 Configuration

### Environment Variables

```bash
# ML model paths
SIGNAL_CLASSIFIER_MODEL_PATH=models/signal_classifier
RELATIONSHIP_STRENGTH_MODEL_PATH=models/relationship_strength
RECOMMENDATION_MODEL_PATH=models/recommendation
ANOMALY_DETECTOR_MODEL_PATH=models/anomaly_detector

# Training settings
ML_TRAINING_ENABLED=true
ML_TRAINING_SCHEDULE=0 2 * * *  # Daily at 2 AM
ML_MIN_ACCURACY=0.85
ML_MAX_TRAINING_TIME=3600  # 1 hour

# Model settings
SIGNAL_CLASSIFIER_BATCH_SIZE=32
SIGNAL_CLASSIFIER_EPOCHS=3
SIGNAL_CLASSIFIER_LEARNING_RATE=2e-5
```

### Model Configuration

```python
# In app/ml/models/signal_classifier.py
MODEL_CONFIG = {
    "model_name": "distilbert-base-uncased-finetuned-signal-classification",
    "max_length": 512,
    "batch_size": 32,
    "learning_rate": 2e-5,
    "epochs": 3,
}

# In app/ml/models/relationship_strength.py
DEFAULT_FEATURE_WEIGHTS = {
    "interaction_count": 0.25,
    "recency_score": 0.20,
    "common_connections": 0.15,
    "profile_similarity": 0.15,
    "shared_skills": 0.10,
    "communication_frequency": 0.10,
    "connection_duration": 0.05,
}
```

## 📁 File Structure

```
backend/app/ml/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── signal_classifier.py
│   ├── relationship_strength.py
│   ├── recommendation.py
│   └── anomaly_detector.py
├── services/
│   ├── __init__.py
│   ├── signal_processing.py
│   ├── relationship_analysis.py
│   ├── recommendation.py
│   └── anomaly_detection.py
├── training/
│   ├── __init__.py
│   ├── signal_trainer.py
│   ├── relationship_trainer.py
│   ├── recommendation_trainer.py
│   └── anomaly_trainer.py
└── utils/
    ├── __init__.py
    ├── text.py
    ├── features.py
    ├── serialization.py
    └── validation.py
```

## 🚀 Deployment

### Local Development

```bash
# Install ML dependencies
pip install -r requirements.txt

# Run backend with ML models
uvicorn app.main:app --reload --port 8000

# Test ML endpoints
curl -X POST http://localhost:8000/api/v1/ml/signals/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Company raised funding"}'
```

### Production Deployment

```bash
# Build Docker image
cd /workspace/yojedesign__Bazov
docker-compose -f docker/docker-compose.yml build backend

# Start services
docker-compose -f docker/docker-compose.yml up -d

# Train models (run in container)
docker-compose -f docker/docker-compose.yml exec backend python -m app.ml.training.signal_trainer
```

## 📈 Performance Optimization

### Caching

- Cache frequent predictions
- Cache model loads
- Cache feature extractions

### Batch Processing

- Process multiple texts in batch
- Use async processing for long-running tasks
- Implement rate limiting

### Model Optimization

- Quantize models for smaller size
- Use distilled models for faster inference
- Implement model pruning

## 🔮 Future Enhancements

### 1. Advanced NLP Models
- Fine-tune BERT/RoBERTa for signal classification
- Implement named entity recognition (NER)
- Add coreference resolution

### 2. Graph Neural Networks
- Use GNNs for relationship prediction
- Implement graph embeddings
- Add link prediction

### 3. Reinforcement Learning
- Optimize recommendations with RL
- Implement bandit algorithms for exploration
- Add reward-based learning

### 4. Federated Learning
- Train models across multiple users
- Preserve data privacy
- Enable collaborative learning

### 5. AutoML
- Automate model selection
- Automate hyperparameter tuning
- Automate feature engineering

## 📞 Support

For issues or questions about the ML system:
- Check logs: `docker-compose logs backend`
- Monitor health: `/api/v1/ml/health/`
- Review documentation: `docs/ml.md`

## 📜 License

The ML models and code are licensed under the same terms as the main Bazov project.
