"""
Service layer for routing app
Contains business logic for route prediction and risk scoring
"""
import time
from typing import Dict, List, Tuple, Optional
from datetime import time as dt_time
import numpy as np
from django.contrib.auth.models import User

from .models import Location, RiskScore, Route, RouteSegment


class RiskScoringService:
    """
    Service for calculating ML-based location risk scores
    Implements risk assessment using multiple factors
    """
    
    def calculate_location_risk(
        self,
        location: Location,
        time_of_day: Optional[dt_time] = None,
        day_of_week: Optional[int] = None
    ) -> float:
        """
        Calculate risk score for a location using ML model
        
        Args:
            location: Location object
            time_of_day: Time of day for risk calculation
            day_of_week: Day of week (0=Monday, 6=Sunday)
            
        Returns:
            Risk score between 0.0 and 1.0
        """
        # Placeholder for ML-based risk scoring logic
        # In production, this would call a trained ML model
        
        # Get existing risk scores for this location
        existing_scores = RiskScore.objects.filter(
            location=location,
            time_of_day=time_of_day,
            day_of_week=day_of_week
        ).first()
        
        if existing_scores:
            return existing_scores.risk_level
        
        # Default risk calculation (placeholder)
        base_risk = 0.3
        return base_risk
    
    def recalculate_route_risk(self, route: Route) -> Route:
        """
        Recalculate overall risk score for a route
        
        Args:
            route: Route object
            
        Returns:
            Updated Route object
        """
        segments = route.segments.all()
        if not segments:
            return route
        
        # Calculate weighted average risk based on segment distances
        total_distance = sum(seg.segment_distance for seg in segments)
        weighted_risk = sum(
            seg.segment_risk_score * seg.segment_distance
            for seg in segments
        ) / total_distance if total_distance > 0 else 0.0
        
        route.overall_risk_score = weighted_risk
        route.save()
        return route


class DijkstraRoutingService:
    """
    Service implementing modified Dijkstra algorithm for safe route finding
    Considers both distance and risk scores
    """
    
    def __init__(self, risk_weight: float = 0.5):
        """
        Initialize routing service
        
        Args:
            risk_weight: Weight for risk score in path calculation (0.0 to 1.0)
        """
        self.risk_weight = risk_weight
    
    def calculate_edge_weight(
        self,
        distance: float,
        risk_score: float
    ) -> float:
        """
        Calculate edge weight combining distance and risk
        
        Args:
            distance: Physical distance in km
            risk_score: Risk score (0.0 to 1.0)
            
        Returns:
            Combined weight for graph traversal
        """
        # Normalize distance (assuming max distance of 50km)
        normalized_distance = min(distance / 50.0, 1.0)
        
        # Combined weight: balance between distance and risk
        weight = (
            (1 - self.risk_weight) * normalized_distance +
            self.risk_weight * risk_score
        )
        return weight
    
    def find_safe_route(
        self,
        origin: Location,
        destination: Location,
        route_type: str = 'safest'
    ) -> List[Location]:
        """
        Find safe route using modified Dijkstra algorithm
        
        Args:
            origin: Starting location
            destination: Destination location
            route_type: Type of route ('safest', 'fastest', 'balanced')
            
        Returns:
            List of Location objects representing the route
        """
        # Adjust risk weight based on route type
        if route_type == 'safest':
            self.risk_weight = 0.8
        elif route_type == 'fastest':
            self.risk_weight = 0.2
        else:  # balanced
            self.risk_weight = 0.5
        
        # Placeholder for actual Dijkstra implementation
        # In production, this would use a graph structure and implement
        # the modified Dijkstra algorithm with risk-aware edge weights
        
        # For now, return simple path
        return [origin, destination]


class RoutePredictionService:
    """
    Main service for route prediction combining risk scoring and routing
    """
    
    def __init__(self):
        self.risk_service = RiskScoringService()
        self.routing_service = DijkstraRoutingService()
    
    def predict_safe_route(
        self,
        origin_lat: float,
        origin_lng: float,
        destination_lat: float,
        destination_lng: float,
        route_type: str,
        user: User,
        time_of_day: Optional[dt_time] = None,
        day_of_week: Optional[int] = None
    ) -> Dict:
        """
        Predict safe route from origin to destination
        
        Args:
            origin_lat: Origin latitude
            origin_lng: Origin longitude
            destination_lat: Destination latitude
            destination_lng: Destination longitude
            route_type: Type of route to calculate
            user: User requesting the route
            time_of_day: Time for risk calculation
            day_of_week: Day of week for risk calculation
            
        Returns:
            Dictionary containing route and metadata
        """
        start_time = time.time()
        
        # Get or create locations
        origin, _ = Location.objects.get_or_create(
            latitude=origin_lat,
            longitude=origin_lng,
            defaults={'location_type': 'waypoint'}
        )
        
        destination, _ = Location.objects.get_or_create(
            latitude=destination_lat,
            longitude=destination_lng,
            defaults={'location_type': 'waypoint'}
        )
        
        # Find safe route using modified Dijkstra
        path = self.routing_service.find_safe_route(
            origin, destination, route_type
        )
        
        # Calculate route metrics
        total_distance = self._calculate_total_distance(path)
        estimated_duration = self._estimate_duration(total_distance)
        
        # Calculate risk scores for path
        overall_risk = self._calculate_path_risk(
            path, time_of_day, day_of_week
        )
        
        # Create route object
        route = Route.objects.create(
            user=user,
            origin=origin,
            destination=destination,
            total_distance=total_distance,
            estimated_duration=estimated_duration,
            overall_risk_score=overall_risk,
            route_type=route_type
        )
        
        # Create route segments
        self._create_route_segments(route, path, time_of_day, day_of_week)
        
        computation_time = time.time() - start_time
        
        return {
            'route': route,
            'alternatives': [],  # Placeholder for alternative routes
            'computation_time': computation_time,
            'message': 'Route calculated successfully'
        }
    
    def _calculate_total_distance(self, path: List[Location]) -> float:
        """Calculate total distance for a path"""
        # Placeholder: Simple Euclidean distance
        if len(path) < 2:
            return 0.0
        
        total = 0.0
        for i in range(len(path) - 1):
            lat1, lng1 = path[i].latitude, path[i].longitude
            lat2, lng2 = path[i + 1].latitude, path[i + 1].longitude
            # Approximate distance (should use haversine in production)
            distance = np.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2) * 111  # ~111 km per degree
            total += distance
        
        return total
    
    def _estimate_duration(self, distance: float) -> float:
        """Estimate duration based on distance (minutes)"""
        # Assume average speed of 30 km/h
        return (distance / 30.0) * 60.0
    
    def _calculate_path_risk(
        self,
        path: List[Location],
        time_of_day: Optional[dt_time],
        day_of_week: Optional[int]
    ) -> float:
        """Calculate overall risk for a path"""
        if not path:
            return 0.5
        
        risks = [
            self.risk_service.calculate_location_risk(
                loc, time_of_day, day_of_week
            )
            for loc in path
        ]
        
        return np.mean(risks)
    
    def _create_route_segments(
        self,
        route: Route,
        path: List[Location],
        time_of_day: Optional[dt_time],
        day_of_week: Optional[int]
    ) -> None:
        """Create route segments from path"""
        for i in range(len(path) - 1):
            start_loc = path[i]
            end_loc = path[i + 1]
            
            # Calculate segment metrics
            lat1, lng1 = start_loc.latitude, start_loc.longitude
            lat2, lng2 = end_loc.latitude, end_loc.longitude
            segment_distance = np.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2) * 111
            segment_duration = (segment_distance / 30.0) * 60.0
            
            # Calculate segment risk
            start_risk = self.risk_service.calculate_location_risk(
                start_loc, time_of_day, day_of_week
            )
            end_risk = self.risk_service.calculate_location_risk(
                end_loc, time_of_day, day_of_week
            )
            segment_risk = (start_risk + end_risk) / 2.0
            
            RouteSegment.objects.create(
                route=route,
                start_location=start_loc,
                end_location=end_loc,
                sequence_order=i,
                segment_distance=segment_distance,
                segment_duration=segment_duration,
                segment_risk_score=segment_risk
            )
