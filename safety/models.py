"""
Models for safety app - handles emergency detection, sensor data, and alerts
"""
from django.db import models
from django.contrib.auth.models import User


class SensorData(models.Model):
    """Stores raw sensor data from mobile devices"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sensor_data')
    sensor_type = models.CharField(
        max_length=50,
        choices=[
            ('accelerometer', 'Accelerometer'),
            ('gyroscope', 'Gyroscope'),
            ('gps', 'GPS'),
            ('audio', 'Audio'),
        ]
    )
    timestamp = models.DateTimeField()
    data_json = models.JSONField(help_text="Raw sensor data in JSON format")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'sensor_type', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor_type} data from {self.user.username} at {self.timestamp}"


class AccelerometerReading(models.Model):
    """Specific model for accelerometer readings"""
    sensor_data = models.ForeignKey(
        SensorData,
        on_delete=models.CASCADE,
        related_name='accelerometer_readings'
    )
    x_axis = models.FloatField()
    y_axis = models.FloatField()
    z_axis = models.FloatField()
    magnitude = models.FloatField()
    sudden_change_detected = models.BooleanField(default=False)
    fall_detected = models.BooleanField(default=False)
    shake_detected = models.BooleanField(default=False)

    def __str__(self):
        return f"Accelerometer ({self.x_axis}, {self.y_axis}, {self.z_axis})"


class AudioFeatures(models.Model):
    """Extracted features from audio data for emergency detection"""
    sensor_data = models.ForeignKey(
        SensorData,
        on_delete=models.CASCADE,
        related_name='audio_features'
    )
    duration = models.FloatField(help_text="Audio duration in seconds")
    sample_rate = models.IntegerField()
    mfcc_features = models.JSONField(help_text="MFCC features array")
    spectral_centroid = models.FloatField(null=True, blank=True)
    zero_crossing_rate = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    scream_probability = models.FloatField(default=0.0)
    distress_probability = models.FloatField(default=0.0)

    def __str__(self):
        return f"Audio features: {self.duration}s"


class EmergencyDetection(models.Model):
    """Records emergency detection events"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_detections')
    detection_timestamp = models.DateTimeField(auto_now_add=True)
    
    # Multimodal risk scores
    accelerometer_risk_score = models.FloatField(default=0.0)
    audio_risk_score = models.FloatField(default=0.0)
    location_risk_score = models.FloatField(default=0.0)
    fused_risk_score = models.FloatField(help_text="Combined risk score from all modalities")
    
    # Detection flags
    is_emergency = models.BooleanField(default=False)
    is_false_positive = models.BooleanField(default=False)
    confidence_level = models.FloatField()
    
    # Context data
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    context_data = models.JSONField(default=dict, blank=True)
    
    # Related sensor data
    accelerometer_data = models.ForeignKey(
        SensorData,
        on_delete=models.SET_NULL,
        null=True,
        related_name='accelerometer_detections'
    )
    audio_data = models.ForeignKey(
        SensorData,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audio_detections'
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'detection_timestamp']),
            models.Index(fields=['is_emergency']),
            models.Index(fields=['fused_risk_score']),
        ]
        ordering = ['-detection_timestamp']

    def __str__(self):
        return f"Emergency Detection for {self.user.username} - Risk: {self.fused_risk_score}"


class Alert(models.Model):
    """Stores emergency alerts sent to contacts"""
    emergency_detection = models.ForeignKey(
        EmergencyDetection,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    alert_type = models.CharField(
        max_length=50,
        choices=[
            ('sms', 'SMS'),
            ('push', 'Push Notification'),
            ('email', 'Email'),
            ('call', 'Emergency Call'),
        ]
    )
    recipient = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['emergency_detection', 'sent_at']),
            models.Index(fields=['delivery_status']),
        ]

    def __str__(self):
        return f"{self.alert_type} alert to {self.recipient}"


class EmergencyContact(models.Model):
    """Stores user's emergency contacts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    priority = models.IntegerField(default=1, help_text="Lower number = higher priority")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', 'name']
        unique_together = ['user', 'phone_number']

    def __str__(self):
        return f"{self.name} - {self.phone_number}"
from django.db import models
from django.contrib.auth.models import User

class SensorEvent(models.Model):
    """
    Stores motion sensor events (Stage 1)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sensor_events')
    timestamp = models.DateTimeField(auto_now_add=True)
    accelerometer_data = models.JSONField(help_text="Accelerometer x, y, z")
    gyroscope_data = models.JSONField(help_text="Gyroscope x, y, z")
    anomaly_score = models.FloatField()
    anomaly_detected = models.BooleanField()
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"SensorEvent {self.id} - Anomaly: {self.anomaly_detected}"

class AudioEvent(models.Model):
    """
    Stores audio analysis events (Stage 2)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audio_events')
    timestamp = models.DateTimeField(auto_now_add=True)
    audio_mfcc = models.JSONField(help_text="MFCC features")
    location = models.JSONField(null=True, blank=True, help_text="Lat, Lon")
    distress_probability = models.FloatField()
    emergency_triggered = models.BooleanField()
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"AudioEvent {self.id} - Triggered: {self.emergency_triggered}"

class EmergencyAlert(models.Model):
    """
    Stores emergency alerts triggered by AudioEvent
    """
    audio_event = models.ForeignKey(AudioEvent, on_delete=models.CASCADE, related_name='emergency_alerts')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"EmergencyAlert {self.id} for {self.audio_event.user.username}"
