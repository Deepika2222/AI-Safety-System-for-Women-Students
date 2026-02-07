"""
Views for routing app - API endpoints for route prediction
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Location, RiskScore, Route, RouteSegment
from .serializers import (
    LocationSerializer, RiskScoreSerializer, RouteSerializer,
    RouteRequestSerializer, RouteResponseSerializer
)
from .services import RoutePredictionService, RiskScoringService


class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing locations"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def risk_scores(self, request, pk=None):
        """Get risk scores for a specific location"""
        location = self.get_object()
        scores = location.risk_scores.all()
        serializer = RiskScoreSerializer(scores, many=True)
        return Response(serializer.data)


class RiskScoreViewSet(viewsets.ModelViewSet):
    """ViewSet for managing risk scores"""
    queryset = RiskScore.objects.all()
    serializer_class = RiskScoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter risk scores by location if provided"""
        queryset = super().get_queryset()
        location_id = self.request.query_params.get('location_id', None)
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        return queryset


class RouteViewSet(viewsets.ModelViewSet):
    """ViewSet for managing routes"""
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return routes for the current user"""
        return self.queryset.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        """Associate route with the current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def predict_safe_route(self, request):
        """
        Predict safe route using ML-based risk scoring and modified Dijkstra algorithm
        """
        serializer = RouteRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Use route prediction service
        service = RoutePredictionService()
        try:
            result = service.predict_safe_route(
                origin_lat=serializer.validated_data['origin_lat'],
                origin_lng=serializer.validated_data['origin_lng'],
                destination_lat=serializer.validated_data['destination_lat'],
                destination_lng=serializer.validated_data['destination_lng'],
                route_type=serializer.validated_data.get('route_type', 'safest'),
                user=request.user,
                time_of_day=serializer.validated_data.get('time_of_day'),
                day_of_week=serializer.validated_data.get('day_of_week')
            )
            
            response_serializer = RouteResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def recalculate_risk(self, request, pk=None):
        """Recalculate risk scores for an existing route"""
        route = self.get_object()
        service = RiskScoringService()
        
        try:
            updated_route = service.recalculate_route_risk(route)
            serializer = self.get_serializer(updated_route)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def user_history(self, request):
        """Get user's route history"""
        routes = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)
