from django.contrib import admin
from .models import (
    SensorData, AccelerometerReading, AudioFeatures,
    EmergencyDetection, Alert, EmergencyContact
)

admin.site.register(SensorData)
admin.site.register(AccelerometerReading)
admin.site.register(AudioFeatures)
admin.site.register(EmergencyDetection)
admin.site.register(Alert)
admin.site.register(EmergencyContact)
