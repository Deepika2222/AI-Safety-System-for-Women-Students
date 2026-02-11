
import client from './client';

export interface Location {
  id?: number;
  latitude: number;
  longitude: number;
  name?: string;
  address?: string;
}

export interface RouteSegment {
  id: number;
  start_location: Location;
  end_location: Location;
  sequence_order: number;
  segment_distance: number;
  segment_duration: number;
  segment_risk_score: number;
}

export interface Route {
  id: number;
  origin: Location;
  destination: Location;
  waypoints: Location[];
  segments: RouteSegment[];
  total_distance: number;
  estimated_duration: number;
  overall_risk_score: number;
  route_type: 'safest' | 'fastest' | 'balanced';
}

export interface RoutePredictionResponse {
  route: Route;
  alternatives: Route[];
  computation_time: number;
  message: string;
}

export interface RouteRequest {
  origin_lat: number;
  origin_lng: number;
  destination_lat: number;
  destination_lng: number;
  route_type: 'safest' | 'fastest' | 'balanced';
  time_of_day?: string; // HH:MM
  day_of_week?: number; // 0-6
}

export const predictSafeRoute = async (data: RouteRequest): Promise<RoutePredictionResponse> => {
  const response = await client.post('/api/routing/routes/predict_safe_route/', data);
  return response.data;
};

export const getRouteHistory = async (): Promise<Route[]> => {
  const response = await client.get('/api/routing/routes/user_history/');
  return response.data;
};
