"""
URL configuration for ai_safety_system project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/routing/', include('routing.urls')),
    path('api/safety/', include('safety.urls')),
    path('api/ml/', include('ml_engine.urls')),
]
