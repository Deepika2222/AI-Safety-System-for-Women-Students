"""
Service layer for safety app
Contains business logic for sensor processing and emergency detection
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from django.contrib.auth.models import User

from .models import (
    SensorData, AccelerometerReading, AudioFeatures,
    EmergencyDetection, Alert, EmergencyContact
)


class AccelerometerProcessingService:
    """
    Service for processing accelerometer data and detecting anomalies
    """
    
    def __init__(self):
        self.fall_threshold = 2.5  # g-force threshold for fall detection
        self.shake_threshold = 3.0  # g-force threshold for shake detection
        self.sudden_change_threshold = 1.5
    
    def process_accelerometer_data(self, data: Dict) -> Tuple[AccelerometerReading, float]:
        """
        Process raw accelerometer data and detect anomalies
        
        Args:
            data: Dictionary containing x, y, z accelerometer values
            
        Returns:
            Tuple of (AccelerometerReading object, risk_score)
        """
        x = data.get('x', 0.0)
        y = data.get('y', 0.0)
        z = data.get('z', 0.0)
        
        # Calculate magnitude
        magnitude = np.sqrt(x**2 + y**2 + z**2)
        
        # Detect anomalies
        fall_detected = magnitude < self.fall_threshold
        shake_detected = magnitude > self.shake_threshold
        sudden_change = abs(magnitude - 9.8) > self.sudden_change_threshold
        
        # Calculate risk score
        risk_score = 0.0
        if fall_detected:
            risk_score = max(risk_score, 0.8)
        if shake_detected:
            risk_score = max(risk_score, 0.7)
        if sudden_change:
            risk_score = max(risk_score, 0.5)
        
        # Create reading object (without saving to DB yet)
        reading = AccelerometerReading(
            x_axis=x,
            y_axis=y,
            z_axis=z,
            magnitude=magnitude,
            sudden_change_detected=sudden_change,
            fall_detected=fall_detected,
            shake_detected=shake_detected
        )
        
        return reading, risk_score
    
    def analyze_acceleration_pattern(
        self,
        readings: List[AccelerometerReading]
    ) -> Dict[str, float]:
        """
        Analyze patterns in accelerometer readings over time
        
        Args:
            readings: List of AccelerometerReading objects
            
        Returns:
            Dictionary with pattern analysis results
        """
        if not readings:
            return {'pattern_risk': 0.0}
        
        # Calculate statistics
        magnitudes = [r.magnitude for r in readings]
        mean_magnitude = np.mean(magnitudes)
        std_magnitude = np.std(magnitudes)
        
        # High variance might indicate distress
        pattern_risk = min(std_magnitude / 5.0, 1.0)
        
        return {
            'pattern_risk': pattern_risk,
            'mean_magnitude': mean_magnitude,
            'std_magnitude': std_magnitude
        }


class AudioVerificationService:
    """
    Service for audio verification and distress sound detection
    """
    
    def __init__(self):
        self.scream_threshold = 0.7
        self.distress_threshold = 0.6
    
    def extract_audio_features(self, audio_data: Dict) -> Tuple[AudioFeatures, float]:
        """
        Extract features from audio data for emergency detection
        
        Args:
            audio_data: Dictionary containing raw audio data
            
        Returns:
            Tuple of (AudioFeatures object, risk_score)
        """
        # Placeholder for actual audio processing
        # In production, this would use librosa or similar library
        
        duration = audio_data.get('duration', 0.0)
        sample_rate = audio_data.get('sample_rate', 16000)
        
        # Mock feature extraction
        mfcc_features = audio_data.get('mfcc', [])
        spectral_centroid = audio_data.get('spectral_centroid', 0.0)
        zero_crossing_rate = audio_data.get('zcr', 0.0)
        energy = audio_data.get('energy', 0.0)
        
        # Mock ML predictions
        scream_probability = audio_data.get('scream_prob', 0.0)
        distress_probability = audio_data.get('distress_prob', 0.0)
        
        # Calculate risk score
        risk_score = max(scream_probability, distress_probability)
        
        features = AudioFeatures(
            duration=duration,
            sample_rate=sample_rate,
            mfcc_features=mfcc_features,
            spectral_centroid=spectral_centroid,
            zero_crossing_rate=zero_crossing_rate,
            energy=energy,
            scream_probability=scream_probability,
            distress_probability=distress_probability
        )
        
        return features, risk_score
    
    def verify_emergency_audio(self, features: AudioFeatures) -> bool:
        """
        Verify if audio indicates an emergency
        
        Args:
            features: AudioFeatures object
            
        Returns:
            Boolean indicating if emergency is detected
        """
        return (
            features.scream_probability > self.scream_threshold or
            features.distress_probability > self.distress_threshold
        )


class MultiModalRiskFusionService:
    """
    Service for fusing multiple sensor modalities for emergency detection
    """
    
    def __init__(self):
        self.accelerometer_service = AccelerometerProcessingService()
        self.audio_service = AudioVerificationService()
        self.alert_service = AlertService()
        
        # Weights for different modalities
        self.accelerometer_weight = 0.4
        self.audio_weight = 0.4
        self.location_weight = 0.2
        
        # Emergency threshold
        self.emergency_threshold = 0.7
    
    def process_emergency_detection(
        self,
        user: User,
        accelerometer_data: Optional[Dict] = None,
        audio_data: Optional[Dict] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        timestamp: datetime = None
    ) -> Dict:
        """
        Process multi-modal sensor data and detect emergency
        
        Args:
            user: User object
            accelerometer_data: Raw accelerometer data
            audio_data: Raw audio data
            latitude: GPS latitude
            longitude: GPS longitude
            timestamp: Timestamp of the data
            
        Returns:
            Dictionary containing detection results
        """
        # Initialize risk scores
        accelerometer_risk = 0.0
        audio_risk = 0.0
        location_risk = 0.0
        
        # Store sensor data references
        accelerometer_sensor = None
        audio_sensor = None
        
        # Process accelerometer data
        if accelerometer_data:
            _, accelerometer_risk = self.accelerometer_service.process_accelerometer_data(
                accelerometer_data
            )
            # Save sensor data
            accelerometer_sensor = SensorData.objects.create(
                user=user,
                sensor_type='accelerometer',
                timestamp=timestamp,
                data_json=accelerometer_data,
                latitude=latitude,
                longitude=longitude
            )
        
        # Process audio data
        if audio_data:
            _, audio_risk = self.audio_service.extract_audio_features(audio_data)
            # Save sensor data
            audio_sensor = SensorData.objects.create(
                user=user,
                sensor_type='audio',
                timestamp=timestamp,
                data_json=audio_data,
                latitude=latitude,
                longitude=longitude
            )
        
        # Calculate location risk (placeholder)
        if latitude and longitude:
            location_risk = self._calculate_location_risk(latitude, longitude)
        
        # Fuse risk scores
        fused_risk = self._fuse_risk_scores(
            accelerometer_risk,
            audio_risk,
            location_risk
        )
        
        # Calculate confidence level
        confidence = self._calculate_confidence(
            accelerometer_risk,
            audio_risk,
            location_risk
        )
        
        # Determine if emergency
        is_emergency = fused_risk >= self.emergency_threshold
        
        # Create emergency detection record
        detection = EmergencyDetection.objects.create(
            user=user,
            accelerometer_risk_score=accelerometer_risk,
            audio_risk_score=audio_risk,
            location_risk_score=location_risk,
            fused_risk_score=fused_risk,
            is_emergency=is_emergency,
            confidence_level=confidence,
            latitude=latitude,
            longitude=longitude,
            accelerometer_data=accelerometer_sensor,
            audio_data=audio_sensor
        )
        
        # Send alerts if emergency
        alerts_sent = 0
        if is_emergency:
            alerts_sent = self.alert_service.send_emergency_alerts(detection)
        
        return {
            'detection': detection,
            'is_emergency': is_emergency,
            'fused_risk_score': fused_risk,
            'confidence_level': confidence,
            'alerts_sent': alerts_sent,
            'message': 'Emergency detected and alerts sent' if is_emergency else 'No emergency detected'
        }
    
    def _fuse_risk_scores(
        self,
        accelerometer_risk: float,
        audio_risk: float,
        location_risk: float
    ) -> float:
        """
        Fuse multiple risk scores using weighted average
        
        Args:
            accelerometer_risk: Risk score from accelerometer
            audio_risk: Risk score from audio
            location_risk: Risk score from location
            
        Returns:
            Fused risk score
        """
        fused = (
            self.accelerometer_weight * accelerometer_risk +
            self.audio_weight * audio_risk +
            self.location_weight * location_risk
        )
        return min(fused, 1.0)
    
    def _calculate_confidence(
        self,
        accelerometer_risk: float,
        audio_risk: float,
        location_risk: float
    ) -> float:
        """
        Calculate confidence level based on agreement between modalities
        
        Args:
            accelerometer_risk: Risk score from accelerometer
            audio_risk: Risk score from audio
            location_risk: Risk score from location
            
        Returns:
            Confidence level
        """
        # High confidence if all modalities agree
        risks = [accelerometer_risk, audio_risk, location_risk]
        std = np.std(risks)
        mean = np.mean(risks)
        
        # Lower std means higher agreement/confidence
        confidence = max(0.0, min(1.0, mean * (1 - std)))
        return confidence
    
    def _calculate_location_risk(self, latitude: float, longitude: float) -> float:
        """
        Calculate risk based on location
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Location-based risk score
        """
        # Placeholder - would integrate with routing app's risk scoring
        return 0.3


class AlertService:
    """
    Service for sending emergency alerts to contacts
    """
    
    def send_emergency_alerts(self, detection: EmergencyDetection) -> int:
        """
        Send emergency alerts to user's emergency contacts
        
        Args:
            detection: EmergencyDetection object
            
        Returns:
            Number of alerts sent
        """
        contacts = EmergencyContact.objects.filter(
            user=detection.user,
            is_active=True
        ).order_by('priority')[:5]  # Send to top 5 contacts
        
        alerts_sent = 0
        for contact in contacts:
            # Create alert message
            message = self._create_alert_message(detection, contact)
            
            # Create alert record
            alert = Alert.objects.create(
                emergency_detection=detection,
                alert_type='sms',  # Default to SMS
                recipient=contact.phone_number,
                message=message,
                delivery_status='pending'
            )
            
            # In production, this would actually send the alert
            # For now, just mark as sent
            alert.delivery_status = 'sent'
            alert.save()
            
            alerts_sent += 1
        
        return alerts_sent
    
    def _create_alert_message(
        self,
        detection: EmergencyDetection,
        contact: EmergencyContact
    ) -> str:
        """
        Create alert message for emergency contact
        
        Args:
            detection: EmergencyDetection object
            contact: EmergencyContact object
            
        Returns:
            Alert message string
        """
        user = detection.user
        location_info = ""
        if detection.latitude and detection.longitude:
            location_info = f" at location ({detection.latitude}, {detection.longitude})"
        
        message = (
            f"EMERGENCY ALERT: {user.get_full_name() or user.username} "
            f"may be in danger{location_info}. "
            f"Risk level: {detection.fused_risk_score:.2f}. "
            f"Please check on them immediately."
        )
        
        return message
