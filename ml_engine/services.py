"""
Service layer for ml_engine app
Contains business logic for ML model management and predictions
"""
import time
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    MLModel, Prediction, TrainingDataset,
    ModelPerformance, FeatureImportance
)


class MLModelService:
    """
    Service for ML model management operations
    """
    
    def load_model(self, model: MLModel):
        """
        Load a trained ML model from file
        
        Args:
            model: MLModel object
            
        Returns:
            Loaded model object (placeholder)
        """
        # Placeholder for actual model loading
        # In production, this would use joblib or pickle to load the model
        # from model.model_file_path
        
        return None
    
    def set_production_model(self, model: MLModel) -> MLModel:
        """
        Set a model as the production model
        Deactivates other production models of the same type
        
        Args:
            model: MLModel to set as production
            
        Returns:
            Updated MLModel object
        """
        # Deactivate other production models of the same type
        MLModel.objects.filter(
            model_type=model.model_type,
            is_production=True
        ).update(is_production=False)
        
        # Set this model as production
        model.is_production = True
        model.is_active = True
        model.save()
        
        return model
    
    def get_production_model(self, model_type: str) -> Optional[MLModel]:
        """
        Get the current production model for a given type
        
        Args:
            model_type: Type of model
            
        Returns:
            Production MLModel or None
        """
        return MLModel.objects.filter(
            model_type=model_type,
            is_production=True,
            is_active=True
        ).first()


class PredictionService:
    """
    Service for making predictions using ML models
    """
    
    def __init__(self):
        self.model_service = MLModelService()
    
    def make_prediction(
        self,
        model_id: int,
        input_data: Dict,
        prediction_type: str,
        context_data: Dict,
        user: Optional[User] = None
    ) -> Dict:
        """
        Make a prediction using a specified model
        
        Args:
            model_id: ID of the model to use
            input_data: Input features for prediction
            prediction_type: Type of prediction
            context_data: Additional context information
            user: User making the request
            
        Returns:
            Dictionary containing prediction results
        """
        start_time = time.time()
        
        # Get model
        model = MLModel.objects.get(id=model_id, is_active=True)
        
        # Load and use model for prediction
        loaded_model = self.model_service.load_model(model)
        
        # Make prediction (placeholder logic)
        prediction_result = self._execute_prediction(
            loaded_model,
            model,
            input_data
        )
        
        # Calculate confidence
        confidence_score = prediction_result.get('confidence', 0.0)
        
        # Save prediction record
        prediction = Prediction.objects.create(
            model=model,
            user=user,
            input_data=input_data,
            prediction_result=prediction_result,
            confidence_score=confidence_score,
            prediction_type=prediction_type,
            context_data=context_data
        )
        
        processing_time = time.time() - start_time
        
        return {
            'prediction': prediction,
            'model_info': model,
            'processing_time': processing_time,
            'message': 'Prediction completed successfully'
        }
    
    def _execute_prediction(
        self,
        loaded_model,
        model: MLModel,
        input_data: Dict
    ) -> Dict:
        """
        Execute prediction using the loaded model
        
        Args:
            loaded_model: Loaded ML model
            model: MLModel metadata
            input_data: Input features
            
        Returns:
            Prediction result dictionary
        """
        # Placeholder prediction logic
        # In production, this would use the actual loaded model
        
        if model.model_type == 'risk_scoring':
            # Simulate risk scoring prediction
            risk_score = np.random.uniform(0.0, 1.0)
            return {
                'risk_score': risk_score,
                'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low',
                'confidence': 0.85
            }
        
        elif model.model_type == 'audio_classification':
            # Simulate audio classification
            classes = ['normal', 'scream', 'distress', 'alarm']
            predicted_class = np.random.choice(classes)
            return {
                'predicted_class': predicted_class,
                'probabilities': {c: np.random.uniform(0, 1) for c in classes},
                'confidence': 0.78
            }
        
        elif model.model_type == 'anomaly_detection':
            # Simulate anomaly detection
            is_anomaly = np.random.random() > 0.8
            return {
                'is_anomaly': is_anomaly,
                'anomaly_score': np.random.uniform(0.0, 1.0),
                'confidence': 0.82
            }
        
        else:
            return {
                'result': 'prediction_placeholder',
                'confidence': 0.75
            }


class ModelEvaluationService:
    """
    Service for evaluating ML model performance
    """
    
    def evaluate_model(self, model: MLModel) -> Dict:
        """
        Evaluate a model's performance based on recent predictions
        
        Args:
            model: MLModel to evaluate
            
        Returns:
            Dictionary containing evaluation results
        """
        # Get recent predictions with feedback
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        predictions = Prediction.objects.filter(
            model=model,
            predicted_at__gte=start_date,
            predicted_at__lte=end_date,
            is_correct__isnull=False
        )
        
        num_predictions = predictions.count()
        
        if num_predictions == 0:
            # No data to evaluate
            return {
                'model': model,
                'performance': None,
                'feature_importances': [],
                'recommendations': ['No prediction data available for evaluation']
            }
        
        # Calculate metrics
        correct_predictions = predictions.filter(is_correct=True).count()
        accuracy = correct_predictions / num_predictions if num_predictions > 0 else 0.0
        
        avg_confidence = predictions.aggregate(
            avg=models.Avg('confidence_score')
        )['avg'] or 0.0
        
        # Create performance record
        performance = ModelPerformance.objects.create(
            model=model,
            evaluation_date=timezone.now().date(),
            period_start=start_date,
            period_end=end_date,
            num_predictions=num_predictions,
            accuracy=accuracy,
            avg_confidence=avg_confidence
        )
        
        # Get feature importances
        feature_importances = model.feature_importances.all()
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            accuracy,
            avg_confidence,
            num_predictions
        )
        
        return {
            'model': model,
            'performance': performance,
            'feature_importances': list(feature_importances),
            'recommendations': recommendations
        }
    
    def _generate_recommendations(
        self,
        accuracy: float,
        avg_confidence: float,
        num_predictions: int
    ) -> List[str]:
        """
        Generate recommendations based on model performance
        
        Args:
            accuracy: Model accuracy
            avg_confidence: Average confidence score
            num_predictions: Number of predictions evaluated
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if accuracy < 0.7:
            recommendations.append(
                "Model accuracy is below 70%. Consider retraining with more data."
            )
        
        if avg_confidence < 0.6:
            recommendations.append(
                "Average confidence is low. Consider feature engineering or model tuning."
            )
        
        if num_predictions < 100:
            recommendations.append(
                "Limited evaluation data. Collect more predictions with feedback for better assessment."
            )
        
        if accuracy > 0.9 and avg_confidence > 0.85:
            recommendations.append(
                "Model is performing well. Consider promoting to production if not already active."
            )
        
        if not recommendations:
            recommendations.append(
                "Model performance is satisfactory. Continue monitoring."
            )
        
        return recommendations


class DataPreprocessingService:
    """
    Service for data preprocessing and feature engineering
    """
    
    def preprocess_sensor_data(self, sensor_data: Dict) -> Dict:
        """
        Preprocess sensor data for ML model input
        
        Args:
            sensor_data: Raw sensor data
            
        Returns:
            Preprocessed feature dictionary
        """
        # Placeholder preprocessing logic
        # In production, this would include normalization, scaling, etc.
        
        features = {}
        
        if 'accelerometer' in sensor_data:
            acc_data = sensor_data['accelerometer']
            features['acc_magnitude'] = np.sqrt(
                acc_data.get('x', 0)**2 +
                acc_data.get('y', 0)**2 +
                acc_data.get('z', 0)**2
            )
            features['acc_x'] = acc_data.get('x', 0)
            features['acc_y'] = acc_data.get('y', 0)
            features['acc_z'] = acc_data.get('z', 0)
        
        if 'audio' in sensor_data:
            audio_data = sensor_data['audio']
            features['audio_energy'] = audio_data.get('energy', 0)
            features['audio_zcr'] = audio_data.get('zero_crossing_rate', 0)
        
        return features
    
    def extract_features(self, raw_data: Dict, feature_names: List[str]) -> np.ndarray:
        """
        Extract specific features from raw data
        
        Args:
            raw_data: Raw input data
            feature_names: List of feature names to extract
            
        Returns:
            Numpy array of feature values
        """
        features = []
        for feature_name in feature_names:
            features.append(raw_data.get(feature_name, 0.0))
        
        return np.array(features)
