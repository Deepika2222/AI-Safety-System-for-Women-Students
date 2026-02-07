"""
Serializers for ml_engine app
"""
from rest_framework import serializers
from .models import (
    MLModel, Prediction, TrainingDataset,
    ModelPerformance, FeatureImportance
)


class MLModelSerializer(serializers.ModelSerializer):
    """Serializer for MLModel"""
    
    class Meta:
        model = MLModel
        fields = [
            'id', 'name', 'model_type', 'version', 'description',
            'model_file_path', 'input_features', 'output_classes',
            'accuracy', 'precision', 'recall', 'f1_score',
            'is_active', 'is_production', 'trained_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PredictionSerializer(serializers.ModelSerializer):
    """Serializer for Prediction"""
    model_name = serializers.CharField(source='model.name', read_only=True)
    
    class Meta:
        model = Prediction
        fields = [
            'id', 'model', 'model_name', 'user', 'input_data',
            'prediction_result', 'confidence_score', 'prediction_type',
            'context_data', 'actual_outcome', 'is_correct', 'predicted_at'
        ]
        read_only_fields = ['id', 'user', 'predicted_at']


class PredictionRequestSerializer(serializers.Serializer):
    """Serializer for prediction requests"""
    model_id = serializers.IntegerField()
    input_data = serializers.JSONField()
    prediction_type = serializers.CharField(max_length=100)
    context_data = serializers.JSONField(required=False, default=dict)


class PredictionResponseSerializer(serializers.Serializer):
    """Serializer for prediction responses"""
    prediction = PredictionSerializer()
    model_info = MLModelSerializer()
    processing_time = serializers.FloatField()
    message = serializers.CharField()


class TrainingDatasetSerializer(serializers.ModelSerializer):
    """Serializer for TrainingDataset"""
    
    class Meta:
        model = TrainingDataset
        fields = [
            'id', 'name', 'description', 'dataset_type', 'file_path',
            'num_samples', 'num_features', 'feature_names',
            'completeness_score', 'balance_score', 'is_validated',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ModelPerformanceSerializer(serializers.ModelSerializer):
    """Serializer for ModelPerformance"""
    model_name = serializers.CharField(source='model.name', read_only=True)
    
    class Meta:
        model = ModelPerformance
        fields = [
            'id', 'model', 'model_name', 'evaluation_date',
            'period_start', 'period_end', 'num_predictions',
            'accuracy', 'precision', 'recall', 'f1_score',
            'avg_confidence', 'false_positive_rate',
            'false_negative_rate', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class FeatureImportanceSerializer(serializers.ModelSerializer):
    """Serializer for FeatureImportance"""
    
    class Meta:
        model = FeatureImportance
        fields = [
            'id', 'model', 'feature_name', 'importance_score',
            'rank', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ModelEvaluationSerializer(serializers.Serializer):
    """Serializer for model evaluation results"""
    model = MLModelSerializer()
    performance = ModelPerformanceSerializer()
    feature_importances = FeatureImportanceSerializer(many=True)
    recommendations = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
