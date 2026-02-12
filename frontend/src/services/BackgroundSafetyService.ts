import BackgroundService from 'react-native-background-actions';
import { accelerometer, setUpdateIntervalForType, SensorTypes } from 'react-native-sensors';
import { Platform } from 'react-native';
import { SafetyService } from '../api/SafetyService';
import AudioRecord from 'react-native-audio-record';
import { AudioUtils } from '../utils/AudioUtils';

const sleep = (time: number) => new Promise<void>((resolve) => setTimeout(() => resolve(), time));

const options = {
    taskName: 'ProtegoSafety',
    taskTitle: 'Protego is active',
    taskDesc: 'Monitoring for falls and emergency gestures',
    taskIcon: {
        name: 'ic_launcher',
        type: 'mipmap',
    },
    color: '#ff00ff',
    parameters: {
        delay: 1000,
    },
};

let isProcessing = false;

// Task to run in background
const veryIntensiveTask = async (taskDataArguments?: any) => {
    // 1. Setup Sensors
    setUpdateIntervalForType(SensorTypes.accelerometer, 200); // 5Hz is enough for shake, saves battery vs 60Hz

    const subscription = accelerometer.subscribe(async ({ x, y, z }) => {
        if (isProcessing) return;

        const magnitude = Math.sqrt(x * x + y * y + z * z);
        // Threshold: 15 m/s^2 (approx 1.5g). Earth gravity is ~9.8.
        if (magnitude > 15) {
            console.log('[Background] Motion detected:', magnitude);
            isProcessing = true;
            await handleEmergencyCheck({ x, y, z });
            isProcessing = false;
        }
    });

    // 2. Keep the service alive
    await new Promise(async (resolve) => {
        // Infinite loop to keep service alive if needed, though subscription handles it mostly.
        // react-native-background-actions expects a promise that doesn't resolve immediately.
        while (BackgroundService.isRunning()) {
            await sleep(1000);
        }
    });

    // Cleanup
    subscription.unsubscribe();
};

const handleEmergencyCheck = async (accel: { x: number, y: number, z: number }) => {
    console.log('[Background] Motion detected. Starting emergency verification...');

    try {
        // 1. Record Audio
        console.log('[Background] Recording audio for verification...');
        const audioOptions = {
            sampleRate: 16000,
            channels: 1,
            bitsPerSample: 16,
            audioSource: 6,
            wavFile: 'background_emergency.wav'
        };

        // Ensure init
        AudioRecord.init(audioOptions);
        AudioRecord.start();
        await sleep(3000); // Record for 3 seconds
        const audioFile = await AudioRecord.stop();
        const mfcc = await AudioUtils.extractMFCC(audioFile);

        // 2. Prepare Data
        // Ideally fetch location here if permissions allow.
        // For now, sending 0,0 or last known.
        const requestData = {
            accelerometer_data: accel,
            audio_data: { mfcc: mfcc },
            latitude: 0,
            longitude: 0,
            timestamp: new Date().toISOString()
        };

        // 3. Call Fusion Service
        console.log('[Background] Sending data to Safety Fusion Engine...');
        const response = await SafetyService.detectEmergency(requestData);

        // 4. Handle Result
        if (response.is_emergency) {
            console.log('[Background] EMERGENCY CONFIRMED! Risk Score:', response.fused_risk_score);

            await BackgroundService.updateNotification({
                taskTitle: 'SOS ACTIVATED',
                taskDesc: `Emergency sent! Risk: ${(response.fused_risk_score * 100).toFixed(0)}%`,
            });

            // In a real app, trigger native SMS/Call handling here.
        } else {
            console.log('[Background] False positive. Risk Score:', response.fused_risk_score);
        }

    } catch (error) {
        console.error('[Background] Error in emergency check workflow:', error);
    }
};

export const BackgroundSafetyRunner = {
    start: async () => {
        if (!BackgroundService.isRunning()) {
            await BackgroundService.start(veryIntensiveTask, options);
            console.log('[Background] Service started');
        }
    },
    stop: async () => {
        await BackgroundService.stop();
        console.log('[Background] Service stopped');
    }
};
