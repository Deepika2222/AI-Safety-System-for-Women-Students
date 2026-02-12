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
    try {
        // Simple check first to avoid false positives
        // In real app, we might want to check if it sustains for a few frames

        console.log('[Background] Checking cloud for anomaly...');
        const response = await SafetyService.checkMotion({
            accelerometer: accel,
            gyroscope: { x: 0, y: 0, z: 0 }
        });

        if (response.anomaly_detected) {
            console.log('[Background] Anomaly confirmed. Recording audio...');
            await startAudioAnalysis();
        }
    } catch (error) {
        console.error('[Background] Error in emergency check', error);
    }
};

const startAudioAnalysis = async () => {
    try {
        // Initialize Audio (should be safe to re-init)
        // Note: Audio recording in background on Android might require specific permissions or foreground service type 'microphone'
        // For now, we assume standard permission is enough for foreground service.
        const options = {
            sampleRate: 16000,
            channels: 1,
            bitsPerSample: 16,
            audioSource: 6,
            wavFile: 'background_test.wav'
        };

        AudioRecord.init(options);
        AudioRecord.start();
        await sleep(3000); // Record for 3 seconds
        const audioFile = await AudioRecord.stop();

        const mfcc = await AudioUtils.extractMFCC(audioFile);

        // We don't have location easily in background without another listener.
        // Send 0,0 or last known if we stored it globally.
        // For SOS, sending the alert is priority.

        const response = await SafetyService.analyzeAudio({
            audio_mfcc: mfcc,
            location: { lat: 0, lon: 0 }
        });

        if (response.emergency_triggered) {
            console.log('[Background] EMERGENCY TRIGGERED! Sending SMS/Alert...');
            // In a real app, triggering Native Module for SMS or Push Notification would happen here
            // Local Notification to user
            await BackgroundService.updateNotification({
                taskTitle: 'SOS ACTIVATED',
                taskDesc: 'Emergency alert sent to contacts.',
            });
        }
    } catch (err) {
        console.error("[Background] Audio analysis failed", err);
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
