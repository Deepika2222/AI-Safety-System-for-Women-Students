"""
Serializers for safety app
"""
from rest_framework import serializers
from .models import (
    SensorData, AccelerometerReading, AudioFeatures,
    EmergencyDetection, Alert, EmergencyContact
)


class AccelerometerReadingSerializer(serializers.ModelSerializer):
    """Serializer for AccelerometerReading model"""
    
    class Meta:
        model = AccelerometerReading
        fields = [
            'id', 'x_axis', 'y_axis', 'z_axis', 'magnitude',
            'sudden_change_detected', 'fall_detected', 'shake_detected'
        ]
        read_only_fields = ['id']


class AudioFeaturesSerializer(serializers.ModelSerializer):
    """Serializer for AudioFeatures model"""
    
    class Meta:
        model = AudioFeatures
        fields = [
            'id', 'duration', 'sample_rate', 'mfcc_features',
            'spectral_centroid', 'zero_crossing_rate', 'energy',
            'scream_probability', 'distress_probability'
        ]
        read_only_fields = ['id']


class SensorDataSerializer(serializers.ModelSerializer):
    """Serializer for SensorData model"""
    accelerometer_readings = AccelerometerReadingSerializer(many=True, read_only=True)
    audio_features = AudioFeaturesSerializer(many=True, read_only=True)
    
    class Meta:
        model = SensorData
        fields = [
            'id', 'user', 'sensor_type', 'timestamp', 'data_json',
            'latitude', 'longitude', 'created_at',
            'accelerometer_readings', 'audio_features'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class SensorDataInputSerializer(serializers.Serializer):
    """Serializer for sensor data input"""
    sensor_type = serializers.ChoiceField(
        choices=['accelerometer', 'gyroscope', 'gps', 'audio']
    )
    timestamp = serializers.DateTimeField()
    data = serializers.JSONField()
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)


class AlertSerializer(serializers.ModelSerializer):
    """Serializer for Alert model"""
    
    class Meta:
        model = Alert
        fields = [
            'id', 'emergency_detection', 'alert_type', 'recipient',
            'message', 'sent_at', 'delivery_status'
        ]
        read_only_fields = ['id', 'sent_at']


class EmergencyDetectionSerializer(serializers.ModelSerializer):
    """Serializer for EmergencyDetection model"""
    alerts = AlertSerializer(many=True, read_only=True)
    
    class Meta:
        model = EmergencyDetection
        fields = [
            'id', 'user', 'detection_timestamp',
            'accelerometer_risk_score', 'audio_risk_score',
            'location_risk_score', 'fused_risk_score',
            'is_emergency', 'is_false_positive', 'confidence_level',
            'latitude', 'longitude', 'context_data', 'alerts'
        ]
        read_only_fields = ['id', 'user', 'detection_timestamp']


class EmergencyContactSerializer(serializers.ModelSerializer):
    """Serializer for EmergencyContact model"""
    
    class Meta:
        model = EmergencyContact
        fields = [
            'id', 'user', 'name', 'phone_number', 'email',
            'relationship', 'priority', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class EmergencyDetectionRequestSerializer(serializers.Serializer):
    """Serializer for emergency detection request"""
    accelerometer_data = serializers.JSONField(required=False)
    audio_data = serializers.JSONField(required=False)
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    timestamp = serializers.DateTimeField()


class EmergencyDetectionResponseSerializer(serializers.Serializer):
    """Serializer for emergency detection response"""
    detection = EmergencyDetectionSerializer()
    is_emergency = serializers.BooleanField()
    fused_risk_score = serializers.FloatField()
    confidence_level = serializers.FloatField()
    alerts_sent = serializers.IntegerField()
    message = serializers.CharField()
