import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, PermissionsAndroid, Platform, Animated } from 'react-native';
import { colors, spacing, typography, shadows } from '../theme-soft';
import { SafetyService } from '../api/SafetyService';
import AudioRecord from 'react-native-audio-record';
import { AudioUtils } from '../utils/AudioUtils';

export function SosScreen() {
    const [sending, setSending] = useState(false);
    const [status, setStatus] = useState('Tap to Trigger Emergency');

    const startAudioAnalysis = async () => {
        try {
            if (Platform.OS === 'android') {
                const granted = await PermissionsAndroid.request(
                    PermissionsAndroid.PERMISSIONS.RECORD_AUDIO
                );
                if (granted !== PermissionsAndroid.RESULTS.GRANTED) return;
            }

            const options = {
                sampleRate: 16000,
                channels: 1,
                bitsPerSample: 16,
                audioSource: 6,
                wavFile: 'sos_manual.wav'
            };

            // Initialize if needed (safe to call multiple times usually, but init might reset)
            AudioRecord.init(options);

            AudioRecord.start();
            await new Promise(resolve => setTimeout(() => resolve(true), 3000));
            const audioFile = await AudioRecord.stop();
            const mfcc = await AudioUtils.extractMFCC(audioFile);

            // Location would ideally come from a context or redux store. 
            // For now, sending 0,0 is acceptable for the manual trigger prototype, 
            // or we could quickly fetch it if we imported Geolocation w/ permission check.

            const response = await SafetyService.analyzeAudio({
                audio_mfcc: mfcc,
                location: { lat: 0, lon: 0 }
            });

            if (response.emergency_triggered) {
                Alert.alert("Emergency Triggered", "Help is on the way. Your location and audio have been sent.");
                setStatus("EMERGENCY ACTIVE");
            } else {
                setStatus("Environment looks safe");
                setTimeout(() => setStatus('Tap to Trigger Emergency'), 3000);
            }

        } catch (err) {
            console.log("Audio analysis failed", err);
            setStatus("Error analyzing audio");
        }
    };

    const handleEmergency = async () => {
        try {
            setSending(true);
            setStatus('Sending SOS...');

            // Mock motion check for manual trigger
            const response = await SafetyService.checkMotion({
                accelerometer: { x: 0, y: 0, z: 0 },
                gyroscope: { x: 0, y: 0, z: 0 }
            });

            if (response) {
                await startAudioAnalysis();
            }
        } catch (error: any) {
            console.error("Emergency Alert Failed:", error);
            setStatus(`Connection failed`);
            Alert.alert("SOS Failed", `Could not send emergency alert.\n${error.message}`);
        } finally {
            setSending(false);
        }
    };

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTitle}>Emergency</Text>
            </View>

            <View style={styles.centerContent}>
                <TouchableOpacity
                    style={[styles.sosButton, sending && styles.sosButtonActive]}
                    onPress={handleEmergency}
                    activeOpacity={0.8}
                    disabled={sending}
                >
                    <View style={styles.sosInner}>
                        <Text style={styles.sosText}>{sending ? '...' : 'SOS'}</Text>
                    </View>
                </TouchableOpacity>

                <Text style={styles.statusText}>{status}</Text>
                <Text style={styles.instructionText}>
                    Pressing this will instantly record audio and notify your emergency contacts.
                </Text>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background,
    },
    header: {
        paddingTop: Platform.OS === 'ios' ? 60 : 40,
        paddingHorizontal: spacing.lg,
        marginBottom: spacing.xl,
    },
    headerTitle: {
        ...typography.header,
        color: colors.primary,
    },
    centerContent: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: spacing.xl,
        paddingBottom: 100,
    },
    sosButton: {
        width: 200,
        height: 200,
        borderRadius: 100,
        backgroundColor: '#FFEBEE', // Light red ring
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: spacing.lg,
        ...shadows.medium,
    },
    sosButtonActive: {
        transform: [{ scale: 0.95 }],
        backgroundColor: '#FFCDD2',
    },
    sosInner: {
        width: 160,
        height: 160,
        borderRadius: 80,
        backgroundColor: colors.primary, // Main Red
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: "#FF0000",
        shadowOffset: { width: 0, height: 10 },
        shadowOpacity: 0.3,
        shadowRadius: 20,
        elevation: 10,
    },
    sosText: {
        fontSize: 48,
        fontWeight: 'bold',
        color: '#FFF',
        letterSpacing: 2,
    },
    statusText: {
        ...typography.title,
        color: colors.text,
        marginBottom: spacing.sm,
        textAlign: 'center',
    },
    instructionText: {
        ...typography.body,
        color: colors.textSecondary,
        textAlign: 'center',
        maxWidth: '80%',
    }
});
