from django.contrib import admin
from .models import (
    MLModel, Prediction, TrainingDataset,
    ModelPerformance, FeatureImportance
)

admin.site.register(MLModel)
admin.site.register(Prediction)
admin.site.register(TrainingDataset)
admin.site.register(ModelPerformance)
admin.site.register(FeatureImportance)
