"""
URL configuration for ml_engine app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MLModelViewSet, PredictionViewSet, TrainingDatasetViewSet,
    ModelPerformanceViewSet
)

router = DefaultRouter()
router.register(r'models', MLModelViewSet, basename='ml-model')
router.register(r'predictions', PredictionViewSet, basename='prediction')
router.register(r'datasets', TrainingDatasetViewSet, basename='training-dataset')
router.register(r'performance', ModelPerformanceViewSet, basename='model-performance')

urlpatterns = [
    path('', include(router.urls)),
]
