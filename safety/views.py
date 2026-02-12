"""
Views for safety app - API endpoints for emergency detection
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    SensorData, AccelerometerReading, AudioFeatures,
    EmergencyDetection, Alert, EmergencyContact
)
from .serializers import (
    SensorDataSerializer, SensorDataInputSerializer,
    EmergencyDetectionSerializer, AlertSerializer,
    EmergencyContactSerializer, EmergencyDetectionRequestSerializer,
    EmergencyDetectionResponseSerializer, UserRegistrationSerializer
)
from .services import (
    AccelerometerProcessingService, AudioVerificationService,
    MultiModalRiskFusionService, AlertService
)


class SensorDataViewSet(viewsets.ModelViewSet):
    """ViewSet for managing sensor data"""
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return sensor data for the current user"""
        queryset = self.queryset.filter(user=self.request.user)
        sensor_type = self.request.query_params.get('sensor_type', None)
        if sensor_type:
            queryset = queryset.filter(sensor_type=sensor_type)
        return queryset

    def perform_create(self, serializer):
        """Associate sensor data with the current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def batch_upload(self, request):
        """Upload multiple sensor data points at once"""
        if not isinstance(request.data, list):
            return Response(
                {'error': 'Expected a list of sensor data'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SensorDataInputSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        created_data = []
        for item in serializer.validated_data:
            sensor_data = SensorData.objects.create(
                user=request.user,
                sensor_type=item['sensor_type'],
                timestamp=item['timestamp'],
                data_json=item['data'],
                latitude=item.get('latitude'),
                longitude=item.get('longitude')
            )
            created_data.append(sensor_data)

        output_serializer = self.get_serializer(created_data, many=True)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class EmergencyDetectionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing emergency detections"""
    queryset = EmergencyDetection.objects.all()
    serializer_class = EmergencyDetectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return emergency detections for the current user"""
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def detect_emergency(self, request):
        """
        Detect emergency using multi-modal sensor fusion
        Processes accelerometer, audio, and location data
        """
        serializer = EmergencyDetectionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Process sensor data through services
        fusion_service = MultiModalRiskFusionService()
        
        try:
            result = fusion_service.process_emergency_detection(
                user=request.user,
                accelerometer_data=serializer.validated_data.get('accelerometer_data'),
                audio_data=serializer.validated_data.get('audio_data'),
                latitude=serializer.validated_data.get('latitude'),
                longitude=serializer.validated_data.get('longitude'),
                timestamp=serializer.validated_data['timestamp']
            )
            
            response_serializer = EmergencyDetectionResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def mark_false_positive(self, request, pk=None):
        """Mark an emergency detection as false positive"""
        detection = self.get_object()
        detection.is_false_positive = True
        detection.is_emergency = False
        detection.save()
        
        serializer = self.get_serializer(detection)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_history(self, request):
        """Get user's emergency detection history"""
        detections = self.get_queryset().order_by('-detection_timestamp')[:20]
        serializer = self.get_serializer(detections, many=True)
        return Response(serializer.data)


class EmergencyContactViewSet(viewsets.ModelViewSet):
    """ViewSet for managing emergency contacts"""
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return emergency contacts for the current user"""
        return self.queryset.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        """Associate emergency contact with the current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def active_contacts(self, request):
        """Get all active emergency contacts"""
        contacts = self.get_queryset().order_by('priority')
        serializer = self.get_serializer(contacts, many=True)
        return Response(serializer.data)


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing alerts (read-only)"""
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return alerts for the current user's emergency detections"""
        return self.queryset.filter(
            emergency_detection__user=self.request.user
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    MotionCheckRequestSerializer, MotionCheckResponseSerializer,
    AudioAnalyzeRequestSerializer, AudioAnalyzeResponseSerializer
)
from .services import MotionDetectionService, AudioAnalysisService

class CheckMotionView(APIView):
    """
    API endpoint for Stage 1: Motion anomaly detection.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MotionCheckRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = MotionDetectionService.process_motion_data(request.user, serializer.validated_data)
                response_serializer = MotionCheckResponseSerializer(result)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnalyzeAudioView(APIView):
    """
    API endpoint for Stage 2: Audio distress detection.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AudioAnalyzeRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = AudioAnalysisService.process_audio_data(request.user, serializer.validated_data)
                response_serializer = AudioAnalyzeResponseSerializer(result)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [] # Allow anonymous registration

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
