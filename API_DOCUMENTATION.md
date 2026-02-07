# API Documentation

## Base URL
`http://localhost:8000/api/`

## Authentication
All endpoints require authentication. Use Django session authentication or configure token authentication as needed.

---

## Routing Endpoints

### 1. Predict Safe Route
**Endpoint:** `POST /api/routing/routes/predict_safe_route/`

**Description:** Predict a safe route using ML-based risk scoring and modified Dijkstra algorithm.

**Request Body:**
```json
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

**Parameters:**
- `origin_lat` (float, required): Origin latitude
- `origin_lng` (float, required): Origin longitude
- `destination_lat` (float, required): Destination latitude
- `destination_lng` (float, required): Destination longitude
- `route_type` (string, optional): Route type - "safest", "fastest", or "balanced" (default: "safest")
- `time_of_day` (time, optional): Time of day for risk calculation
- `day_of_week` (integer, optional): Day of week (0=Monday, 6=Sunday)

**Response:**
```json
{
  "route": {
    "id": 1,
    "origin": {...},
    "destination": {...},
    "waypoints": [...],
    "segments": [...],
    "total_distance": 5.2,
    "estimated_duration": 10.4,
    "overall_risk_score": 0.35,
    "route_type": "safest"
  },
  "alternatives": [],
  "computation_time": 0.125,
  "message": "Route calculated successfully"
}
```

### 2. List Locations
**Endpoint:** `GET /api/routing/locations/`

**Description:** List all locations in the system.

### 3. Create Location
**Endpoint:** `POST /api/routing/locations/`

**Request Body:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "name": "Central Park",
  "address": "New York, NY",
  "location_type": "landmark"
}
```

### 4. Get Risk Scores for Location
**Endpoint:** `GET /api/routing/locations/{id}/risk_scores/`

**Description:** Get all risk scores for a specific location.

### 5. List Routes
**Endpoint:** `GET /api/routing/routes/`

**Description:** List all routes for the current user.

### 6. Get User Route History
**Endpoint:** `GET /api/routing/routes/user_history/`

**Description:** Get the last 10 routes for the current user.

---

## Safety Endpoints

### 1. Detect Emergency
**Endpoint:** `POST /api/safety/emergency-detections/detect_emergency/`

**Description:** Detect emergency using multi-modal sensor fusion (accelerometer, audio, location).

**Request Body:**
```json
{
  "accelerometer_data": {
    "x": 0.5,
    "y": 0.3,
    "z": 9.8
  },
  "audio_data": {
    "duration": 2.0,
    "sample_rate": 16000,
    "energy": 0.7,
    "scream_prob": 0.8,
    "distress_prob": 0.6
  },
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timestamp": "2024-01-15T20:30:00Z"
}
```

**Response:**
```json
{
  "detection": {
    "id": 1,
    "accelerometer_risk_score": 0.5,
    "audio_risk_score": 0.8,
    "location_risk_score": 0.3,
    "fused_risk_score": 0.62,
    "is_emergency": false,
    "confidence_level": 0.75,
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "is_emergency": false,
  "fused_risk_score": 0.62,
  "confidence_level": 0.75,
  "alerts_sent": 0,
  "message": "No emergency detected"
}
```

### 2. Upload Sensor Data
**Endpoint:** `POST /api/safety/sensor-data/`

**Request Body:**
```json
{
  "sensor_type": "accelerometer",
  "timestamp": "2024-01-15T20:30:00Z",
  "data_json": {
    "x": 0.5,
    "y": 0.3,
    "z": 9.8
  },
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

### 3. Batch Upload Sensor Data
**Endpoint:** `POST /api/safety/sensor-data/batch_upload/`

**Request Body:**
```json
[
  {
    "sensor_type": "accelerometer",
    "timestamp": "2024-01-15T20:30:00Z",
    "data": {...}
  },
  {
    "sensor_type": "audio",
    "timestamp": "2024-01-15T20:30:01Z",
    "data": {...}
  }
]
```

### 4. List Emergency Contacts
**Endpoint:** `GET /api/safety/emergency-contacts/`

**Description:** List all active emergency contacts for the current user.

### 5. Create Emergency Contact
**Endpoint:** `POST /api/safety/emergency-contacts/`

**Request Body:**
```json
{
  "name": "John Doe",
  "phone_number": "+1234567890",
  "email": "john@example.com",
  "relationship": "Friend",
  "priority": 1
}
```

### 6. Mark Detection as False Positive
**Endpoint:** `POST /api/safety/emergency-detections/{id}/mark_false_positive/`

**Description:** Mark an emergency detection as a false positive.

### 7. Get Emergency Detection History
**Endpoint:** `GET /api/safety/emergency-detections/user_history/`

**Description:** Get the last 20 emergency detections for the current user.

---

## ML Engine Endpoints

### 1. Make Prediction
**Endpoint:** `POST /api/ml/predictions/predict/`

**Description:** Make a prediction using a specified ML model.

**Request Body:**
```json
{
  "model_id": 1,
  "input_data": {
    "feature1": 0.5,
    "feature2": 0.8,
    "feature3": 0.3
  },
  "prediction_type": "risk_scoring",
  "context_data": {}
}
```

**Response:**
```json
{
  "prediction": {
    "id": 1,
    "model": 1,
    "prediction_result": {
      "risk_score": 0.65,
      "risk_level": "medium",
      "confidence": 0.85
    },
    "confidence_score": 0.85,
    "prediction_type": "risk_scoring"
  },
  "model_info": {
    "id": 1,
    "name": "Risk Scoring Model v1",
    "model_type": "risk_scoring",
    "version": "1.0"
  },
  "processing_time": 0.023,
  "message": "Prediction completed successfully"
}
```

### 2. List ML Models
**Endpoint:** `GET /api/ml/models/`

**Query Parameters:**
- `model_type`: Filter by model type
- `is_production`: Filter by production status

### 3. Get Model Performance History
**Endpoint:** `GET /api/ml/models/{id}/performance_history/`

**Description:** Get the last 30 performance evaluations for a model.

### 4. Get Model Feature Importance
**Endpoint:** `GET /api/ml/models/{id}/feature_importance/`

**Description:** Get feature importance rankings for a model.

### 5. Set Production Model
**Endpoint:** `POST /api/ml/models/{id}/set_production/`

**Description:** Set a model as the production model for its type.

### 6. Get Production Models
**Endpoint:** `GET /api/ml/models/production_models/`

**Description:** Get all production models.

### 7. Provide Prediction Feedback
**Endpoint:** `POST /api/ml/predictions/{id}/provide_feedback/`

**Request Body:**
```json
{
  "actual_outcome": {...},
  "is_correct": true
}
```

### 8. Evaluate Model
**Endpoint:** `POST /api/ml/performance/evaluate_model/`

**Request Body:**
```json
{
  "model_id": 1
}
```

**Response:**
```json
{
  "model": {...},
  "performance": {
    "evaluation_date": "2024-01-15",
    "num_predictions": 500,
    "accuracy": 0.87,
    "avg_confidence": 0.82
  },
  "feature_importances": [...],
  "recommendations": [
    "Model is performing well. Consider promoting to production."
  ]
}
```

### 9. List Training Datasets
**Endpoint:** `GET /api/ml/datasets/`

**Query Parameters:**
- `dataset_type`: Filter by dataset type

### 10. Create Training Dataset
**Endpoint:** `POST /api/ml/datasets/`

**Request Body:**
```json
{
  "name": "Risk Scoring Dataset v1",
  "description": "Dataset for training risk scoring model",
  "dataset_type": "risk_scoring",
  "file_path": "/path/to/dataset.csv",
  "num_samples": 10000,
  "num_features": 15,
  "feature_names": ["feature1", "feature2", ...]
}
```

---

## Common Response Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Error Response Format

```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Notes

1. All timestamps should be in ISO 8601 format
2. Coordinates should be in decimal degrees format
3. Risk scores are normalized between 0.0 and 1.0
4. Pagination is available on list endpoints using `page` and `page_size` query parameters
5. All endpoints support filtering, ordering, and search where applicable
