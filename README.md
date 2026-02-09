# AI Safety System for Women Students

Smart AI safety app with risk-aware route optimization and multi-sensor emergency detection for real-time protection.

## Overview

This Django REST Framework backend provides a scalable architecture for an AI-powered safety application with two core features:

1. **Safe Route Prediction**: ML-based location risk scoring combined with a modified Dijkstra algorithm for optimal route planning
2. **Emergency Detection**: Multi-modal sensor fusion using accelerometer data, audio verification, and location-based risk assessment

## Architecture

The system is organized into three main Django apps:

### 1. Routing App
Handles safe route prediction and risk scoring:
- **Models**: Location, RiskScore, Route, RouteSegment
- **Services**: 
  - `RiskScoringService`: ML-based location risk calculation
  - `DijkstraRoutingService`: Modified Dijkstra algorithm with risk-aware edge weights
  - `RoutePredictionService`: Main orchestrator for route prediction
- **API Endpoints**:
  - `/api/routing/locations/` - Location management
  - `/api/routing/risk-scores/` - Risk score management
  - `/api/routing/routes/` - Route CRUD operations
  - `/api/routing/routes/predict_safe_route/` - Safe route prediction

### 2. Safety App
Manages emergency detection and alerts:
- **Models**: SensorData, AccelerometerReading, AudioFeatures, EmergencyDetection, Alert, EmergencyContact
- **Services**:
  - `AccelerometerProcessingService`: Processes accelerometer data for anomaly detection
  - `AudioVerificationService`: Audio feature extraction and distress detection
  - `MultiModalRiskFusionService`: Fuses multiple sensor modalities
  - `AlertService`: Manages emergency alerts to contacts
- **API Endpoints**:
  - `/api/safety/sensor-data/` - Sensor data management
  - `/api/safety/emergency-detections/` - Emergency detection records
  - `/api/safety/emergency-detections/detect_emergency/` - Real-time emergency detection
  - `/api/safety/emergency-contacts/` - Emergency contact management
  - `/api/safety/alerts/` - Alert history

### 3. ML Engine App
Manages machine learning models and predictions:
- **Models**: MLModel, Prediction, TrainingDataset, ModelPerformance, FeatureImportance
- **Services**:
  - `MLModelService`: Model loading and management
  - `PredictionService`: Making predictions with ML models
  - `ModelEvaluationService`: Model performance evaluation
  - `DataPreprocessingService`: Data preprocessing and feature engineering
- **API Endpoints**:
  - `/api/ml/models/` - ML model management
  - `/api/ml/predictions/` - Prediction records
  - `/api/ml/predictions/predict/` - Make predictions
  - `/api/ml/datasets/` - Training dataset management
  - `/api/ml/performance/` - Model performance metrics

## Project Structure

```
ai_safety_system/
├── ai_safety_system/       # Main project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
│
├── routing/               # Route prediction app
│   ├── models.py          # Location, Route, RiskScore models
│   ├── serializers.py     # REST serializers
│   ├── views.py           # API views
│   ├── services.py        # Business logic layer
│   ├── urls.py            # App URL configuration
│   └── admin.py           # Admin interface
│
├── safety/                # Emergency detection app
│   ├── models.py          # SensorData, EmergencyDetection models
│   ├── serializers.py     # REST serializers
│   ├── views.py           # API views
│   ├── services.py        # Business logic layer
│   ├── urls.py            # App URL configuration
│   └── admin.py           # Admin interface
│
├── ml_engine/             # ML model management app
│   ├── models.py          # MLModel, Prediction models
│   ├── serializers.py     # REST serializers
│   ├── views.py           # API views
│   ├── services.py        # Business logic layer
│   ├── urls.py            # App URL configuration
│   └── admin.py           # Admin interface
│
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── .gitignore            # Git ignore rules
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Virtual environment tool (venv or virtualenv)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd AI-Safety-System-for-Women-Students
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set up database**
```bash
# Create PostgreSQL database
createdb ai_safety_db

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Documentation

### Authentication
All endpoints require authentication. The system uses session-based authentication by default.

### Key Endpoints

#### Route Prediction
```http
POST /api/routing/routes/predict_safe_route/
Content-Type: application/json

{
  "origin_lat": 40.7128,
  "origin_lng": -74.0060,
  "destination_lat": 40.7589,
  "destination_lng": -73.9851,
  "route_type": "safest",
  "time_of_day": "20:00:00",
  "day_of_week": 5
}
```

#### Emergency Detection
```http
POST /api/safety/emergency-detections/detect_emergency/
Content-Type: application/json

{
  "accelerometer_data": {
    "x": 0.5,
    "y": 0.3,
    "z": 9.8
  },
  "audio_data": {
    "duration": 2.0,
    "sample_rate": 16000,
    "energy": 0.7
  },
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timestamp": "2024-01-15T20:30:00Z"
}
```

#### ML Prediction
```http
POST /api/ml/predictions/predict/
Content-Type: application/json

{
  "model_id": 1,
  "input_data": {
    "feature1": 0.5,
    "feature2": 0.8
  },
  "prediction_type": "risk_scoring"
}
```

## Technology Stack

- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL
- **ML Libraries**: scikit-learn, NumPy, Pandas
- **Audio Processing**: librosa
- **Geospatial**: geopy, networkx
- **Testing**: pytest, pytest-django

## Mobile App (React Native)

The React Native app includes live location tracking and shows a moving marker on the safety map.

### Frontend Setup

```bash
cd frontend
npm install
```

### Run on Android

```bash
npx react-native run-android
```

### Run on iOS

```bash
cd ios
pod install
cd ..
npx react-native run-ios
```

### Location Permissions

- Android: the app requests fine, coarse, and background location permissions at runtime.
- iOS: the app requests always-on location access; ensure the permission prompt is accepted.

## Features

### Route Prediction
- ML-based location risk scoring
- Modified Dijkstra algorithm with risk-aware edge weights
- Multiple route types: safest, fastest, balanced
- Time-of-day and day-of-week risk analysis
- Route history and alternative routes

### Emergency Detection
- Multi-modal sensor fusion (accelerometer + audio + location)
- Real-time anomaly detection from accelerometer data
- Audio distress signal verification
- Automatic emergency alerts to contacts
- False positive handling and feedback

### Mobile App
- Live location tracking with a moving map marker

### ML Engine
- Model versioning and deployment management
- Production model selection
- Performance tracking and evaluation
- Feature importance analysis
- Prediction feedback loop for continuous improvement

## Service Layer Architecture

Each app follows a clean architecture with a dedicated service layer:

- **Views**: Handle HTTP requests/responses, validation, permissions
- **Serializers**: Data transformation and validation
- **Services**: Business logic, ML operations, data processing
- **Models**: Data structure and database interactions

This separation ensures:
- Testability
- Reusability
- Maintainability
- Clear separation of concerns

## Configuration

Key settings in `ai_safety_system/settings.py`:

```python
# ML Model configurations
ML_MODELS_DIR = BASE_DIR / 'ml_models'
RISK_SCORE_THRESHOLD = 0.7
EMERGENCY_DETECTION_THRESHOLD = 0.8

# Sensor data configurations
ACCELEROMETER_SAMPLE_RATE = 50  # Hz
AUDIO_SAMPLE_RATE = 16000  # Hz
SENSOR_BUFFER_SIZE = 100
```

## Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
flake8
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin Interface
Access the Django admin at `http://localhost:8000/admin/`

## Deployment Considerations

1. **Environment Variables**: Always use environment variables for sensitive data
2. **Database**: Use PostgreSQL in production with proper connection pooling
3. **Static Files**: Configure static file serving with WhiteNoise or CDN
4. **ML Models**: Store trained models in dedicated storage (S3, GCS)
5. **Monitoring**: Implement logging and monitoring for API endpoints
6. **Scaling**: Consider using Celery for background tasks (alerts, ML predictions)
7. **Security**: Enable HTTPS, set secure cookies, configure CORS properly

## Future Enhancements

- Real-time WebSocket support for live emergency alerts
- Integration with actual ML model training pipeline
- Mobile app SDK for sensor data collection
- Advanced analytics dashboard
- Integration with mapping services (Google Maps, OpenStreetMap)
- Multi-language support

## Contributing

Please ensure all code follows PEP 8 style guidelines and includes appropriate tests.

## License

[Your License Here]

## Contact

[Your Contact Information]
