"""
Models for ml_engine app - handles ML models and predictions
"""
from django.db import models
from django.contrib.auth.models import User


class MLModel(models.Model):
    """Stores information about trained ML models"""
    name = models.CharField(max_length=255, unique=True)
    model_type = models.CharField(
        max_length=50,
        choices=[
            ('risk_scoring', 'Risk Scoring Model'),
            ('audio_classification', 'Audio Classification Model'),
            ('anomaly_detection', 'Anomaly Detection Model'),
            ('route_optimization', 'Route Optimization Model'),
        ]
    )
    version = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    # Model metadata
    model_file_path = models.CharField(max_length=500, help_text="Path to model file")
    input_features = models.JSONField(help_text="List of input feature names")
    output_classes = models.JSONField(
        null=True,
        blank=True,
        help_text="Output classes for classification models"
    )
    
    # Performance metrics
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_production = models.BooleanField(default=False)
    
    # Timestamps
    trained_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['model_type', 'is_active']),
            models.Index(fields=['is_production']),
        ]

    def __str__(self):
        return f"{self.name} v{self.version} ({self.model_type})"


class Prediction(models.Model):
    """Stores predictions made by ML models"""
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='predictions')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ml_predictions',
        null=True,
        blank=True
    )
    
    # Input and output
    input_data = models.JSONField(help_text="Input features used for prediction")
    prediction_result = models.JSONField(help_text="Model output/prediction")
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        help_text="Confidence level of prediction"
    )
    
    # Context
    prediction_type = models.CharField(max_length=100)
    context_data = models.JSONField(default=dict, blank=True)
    
    # Feedback
    actual_outcome = models.JSONField(
        null=True,
        blank=True,
        help_text="Actual outcome for model evaluation"
    )
    is_correct = models.BooleanField(null=True, blank=True)
    
    # Timestamps
    predicted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-predicted_at']
        indexes = [
            models.Index(fields=['model', 'predicted_at']),
            models.Index(fields=['user', 'prediction_type']),
        ]

    def __str__(self):
        return f"Prediction by {self.model.name} at {self.predicted_at}"


class TrainingDataset(models.Model):
    """Stores information about training datasets"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    dataset_type = models.CharField(
        max_length=50,
        choices=[
            ('risk_scoring', 'Risk Scoring Data'),
            ('audio_samples', 'Audio Samples'),
            ('sensor_data', 'Sensor Data'),
            ('route_data', 'Route Data'),
        ]
    )
    
    # Dataset metadata
    file_path = models.CharField(max_length=500)
    num_samples = models.IntegerField()
    num_features = models.IntegerField()
    feature_names = models.JSONField()
    
    # Quality metrics
    completeness_score = models.FloatField(
        null=True,
        blank=True,
        help_text="Percentage of complete records"
    )
    balance_score = models.FloatField(
        null=True,
        blank=True,
        help_text="Class balance score"
    )
    
    # Status
    is_validated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.num_samples} samples)"


class ModelPerformance(models.Model):
    """Tracks model performance over time"""
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='performance_metrics')
    
    # Time period
    evaluation_date = models.DateField()
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    # Metrics
    num_predictions = models.IntegerField()
    accuracy = models.FloatField()
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    
    # Additional metrics
    avg_confidence = models.FloatField(null=True, blank=True)
    false_positive_rate = models.FloatField(null=True, blank=True)
    false_negative_rate = models.FloatField(null=True, blank=True)
    
    # Context
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-evaluation_date']
        unique_together = ['model', 'evaluation_date']
        indexes = [
            models.Index(fields=['model', 'evaluation_date']),
        ]

    def __str__(self):
        return f"{self.model.name} performance on {self.evaluation_date}"


class FeatureImportance(models.Model):
    """Stores feature importance for model interpretability"""
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='feature_importances')
    feature_name = models.CharField(max_length=255)
    importance_score = models.FloatField()
    rank = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank']
        unique_together = ['model', 'feature_name']

    def __str__(self):
        return f"{self.feature_name}: {self.importance_score}"

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=255, blank=True, null=True)
    risk_score = models.FloatField(default=0.0)

class Route(models.Model):
    ROUTE_TYPES = (('safest', 'Safest'), ('fastest', 'Fastest'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='route_origin')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='route_destination')
    route_type = models.CharField(max_length=10, choices=ROUTE_TYPES)
    total_distance = models.FloatField()
    safety_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class RouteSegment(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    start_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='segment_start')
    end_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='segment_end')
    risk_weight = models.FloatField()
    distance = models.FloatField()

class SensorEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accel_x = models.FloatField()
    accel_y = models.FloatField()
    accel_z = models.FloatField()
    gyro_x = models.FloatField()
    gyro_y = models.FloatField()
    gyro_z = models.FloatField()
    anomaly_score = models.FloatField()
    timestamp = models.DateTimeField()

class AudioEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    distress_probability = models.FloatField()
    timestamp = models.DateTimeField()

class EmergencyAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    final_risk_score = models.FloatField()
    alert_triggered = models.BooleanField(default=False)
    timestamp = models.DateTimeField()

class MLModel(models.Model):
    model_name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    accuracy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.TextField()

