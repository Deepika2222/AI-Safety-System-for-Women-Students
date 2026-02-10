import { request } from './client';

export type MotionCheckRequest = {
    accelerometer: { x: number; y: number; z: number };
    gyroscope: { x: number; y: number; z: number };
};

export type MotionCheckResponse = {
    anomaly_score: number;
    anomaly_detected: boolean;
};

export type AudioAnalyzeRequest = {
    audio_mfcc: number[];
    location: { lat: number; lon: number };
};

export type AudioAnalyzeResponse = {
    distress_probability: number;
    emergency_triggered: boolean;
};

export const SafetyService = {
    checkMotion: async (data: MotionCheckRequest): Promise<MotionCheckResponse> => {
        return request<MotionCheckResponse>('/api/safety/check_motion/', {
            method: 'POST',
            body: data,
        });
    },

    analyzeAudio: async (data: AudioAnalyzeRequest): Promise<AudioAnalyzeResponse> => {
        return request<AudioAnalyzeResponse>('/api/safety/analyze_audio/', {
            method: 'POST',
            body: data,
        });
    },
};
