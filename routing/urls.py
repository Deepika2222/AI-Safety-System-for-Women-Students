"""
URL configuration for routing app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, RiskScoreViewSet, RouteViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'risk-scores', RiskScoreViewSet, basename='risk-score')
router.register(r'routes', RouteViewSet, basename='route')

urlpatterns = [
    path('', include(router.urls)),
]
