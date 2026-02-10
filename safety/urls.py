"""
URL configuration for safety app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SensorDataViewSet, EmergencyDetectionViewSet,
    EmergencyContactViewSet, AlertViewSet,
    CheckMotionView, AnalyzeAudioView
)

router = DefaultRouter()
router.register(r'sensor-data', SensorDataViewSet, basename='sensor-data')
router.register(r'emergency-detections', EmergencyDetectionViewSet, basename='emergency-detection')
router.register(r'emergency-contacts', EmergencyContactViewSet, basename='emergency-contact')
router.register(r'alerts', AlertViewSet, basename='alert')

urlpatterns = [
    path('check_motion/', CheckMotionView.as_view(), name='check-motion'),
    path('analyze_audio/', AnalyzeAudioView.as_view(), name='analyze-audio'),
    path('', include(router.urls)),
]
