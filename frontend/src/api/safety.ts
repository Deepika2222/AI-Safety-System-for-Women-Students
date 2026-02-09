import { request } from './client';

type EmergencyDetectRequest = {
  accelerometer_data?: Record<string, unknown>;
  audio_data?: Record<string, unknown>;
  latitude?: number | null;
  longitude?: number | null;
  timestamp: string;
};

type EmergencyDetectResponse = {
  is_emergency: boolean;
  fused_risk_score: number;
  confidence_level: number;
  alerts_sent: number;
  message: string;
};

type EmergencyContact = {
  id: number;
  name: string;
  phone_number: string;
  relationship: string;
  is_active: boolean;
  priority: number;
};

export async function detectEmergency(payload: EmergencyDetectRequest) {
  return request<EmergencyDetectResponse>(
    '/api/safety/emergency-detections/detect_emergency/',
    { method: 'POST', body: payload }
  );
}

export async function fetchEmergencyContacts() {
  return request<EmergencyContact[]>('/api/safety/emergency-contacts/');
}
