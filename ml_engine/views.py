"""
Views for ml_engine app - API endpoints for ML operations
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    MLModel, Prediction, TrainingDataset,
    ModelPerformance, FeatureImportance
)
from .serializers import (
    MLModelSerializer, PredictionSerializer, TrainingDatasetSerializer,
    ModelPerformanceSerializer, FeatureImportanceSerializer,
    PredictionRequestSerializer, PredictionResponseSerializer,
    ModelEvaluationSerializer
)
from .services import (
    MLModelService, PredictionService, ModelEvaluationService
)


class MLModelViewSet(viewsets.ModelViewSet):
    """ViewSet for managing ML models"""
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter models by type and status"""
        queryset = super().get_queryset()
        model_type = self.request.query_params.get('model_type', None)
        is_production = self.request.query_params.get('is_production', None)
        
        if model_type:
            queryset = queryset.filter(model_type=model_type)
        if is_production is not None:
            queryset = queryset.filter(is_production=is_production.lower() == 'true')
        
        return queryset

    @action(detail=True, methods=['get'])
    def performance_history(self, request, pk=None):
        """Get performance history for a model"""
        model = self.get_object()
        performances = model.performance_metrics.all()[:30]  # Last 30 evaluations
        serializer = ModelPerformanceSerializer(performances, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def feature_importance(self, request, pk=None):
        """Get feature importance for a model"""
        model = self.get_object()
        features = model.feature_importances.all()
        serializer = FeatureImportanceSerializer(features, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_production(self, request, pk=None):
        """Set model as production model"""
        model = self.get_object()
        service = MLModelService()
        
        try:
            updated_model = service.set_production_model(model)
            serializer = self.get_serializer(updated_model)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def production_models(self, request):
        """Get all production models"""
        models = self.queryset.filter(is_production=True, is_active=True)
        serializer = self.get_serializer(models, many=True)
        return Response(serializer.data)


class PredictionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing predictions"""
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return predictions for the current user"""
        queryset = super().get_queryset()
        
        # Filter by user if not staff
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        # Filter by model
        model_id = self.request.query_params.get('model_id', None)
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        
        # Filter by prediction type
        prediction_type = self.request.query_params.get('prediction_type', None)
        if prediction_type:
            queryset = queryset.filter(prediction_type=prediction_type)
        
        return queryset

    @action(detail=False, methods=['post'])
    def predict(self, request):
        """
        Make a prediction using a specified ML model
        """
        serializer = PredictionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = PredictionService()
        
        try:
            result = service.make_prediction(
                model_id=serializer.validated_data['model_id'],
                input_data=serializer.validated_data['input_data'],
                prediction_type=serializer.validated_data['prediction_type'],
                context_data=serializer.validated_data.get('context_data', {}),
                user=request.user
            )
            
            response_serializer = PredictionResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except MLModel.DoesNotExist:
            return Response(
                {'error': 'Model not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def provide_feedback(self, request, pk=None):
        """Provide feedback on a prediction for model improvement"""
        prediction = self.get_object()
        
        actual_outcome = request.data.get('actual_outcome')
        is_correct = request.data.get('is_correct')
        
        if actual_outcome is not None:
            prediction.actual_outcome = actual_outcome
        if is_correct is not None:
            prediction.is_correct = is_correct
        
        prediction.save()
        
        serializer = self.get_serializer(prediction)
        return Response(serializer.data)


class TrainingDatasetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing training datasets"""
    queryset = TrainingDataset.objects.all()
    serializer_class = TrainingDatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter datasets by type and status"""
        queryset = super().get_queryset()
        dataset_type = self.request.query_params.get('dataset_type', None)
        
        if dataset_type:
            queryset = queryset.filter(dataset_type=dataset_type)
        
        return queryset

    @action(detail=True, methods=['post'])
    def validate_dataset(self, request, pk=None):
        """Validate a training dataset"""
        dataset = self.get_object()
        dataset.is_validated = True
        dataset.save()
        
        serializer = self.get_serializer(dataset)
        return Response(serializer.data)


class ModelPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing model performance (read-only)"""
    queryset = ModelPerformance.objects.all()
    serializer_class = ModelPerformanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter performance metrics by model"""
        queryset = super().get_queryset()
        model_id = self.request.query_params.get('model_id', None)
        
        if model_id:
            queryset = queryset.filter(model_id=model_id)
        
        return queryset

    @action(detail=False, methods=['post'])
    def evaluate_model(self, request):
        """Evaluate a model's performance"""
        model_id = request.data.get('model_id')
        if not model_id:
            return Response(
                {'error': 'model_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            model = MLModel.objects.get(id=model_id)
            service = ModelEvaluationService()
            result = service.evaluate_model(model)
            
            serializer = ModelEvaluationSerializer(result)
            return Response(serializer.data)
        except MLModel.DoesNotExist:
            return Response(
                {'error': 'Model not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
