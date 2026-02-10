import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ActivityIndicator, Alert, PermissionsAndroid, Platform, StyleSheet, Text, View, StatusBar, Animated, TouchableOpacity } from 'react-native';
import { WebView } from 'react-native-webview';
import Geolocation, { GeoPosition } from 'react-native-geolocation-service';
import { accelerometer, setUpdateIntervalForType, SensorTypes } from 'react-native-sensors';
import AudioRecord from 'react-native-audio-record';
import { SafetyService } from '../api/SafetyService';
import { AudioUtils } from '../utils/AudioUtils';
import { fetchRiskScores } from '../api/routing';
import { PrimaryButton } from '../components/PrimaryButton';
import { SectionCard } from '../components/SectionCard';
import { colors, spacing, typography, shadows } from '../theme-soft';

const initialRegion = {
  latitude: 12.9716,
  longitude: 77.5946,
};

export function MapScreen() {
  const [sending, setSending] = useState(false);
  const [status, setStatus] = useState('You are safe');
  const [locationStatus, setLocationStatus] = useState('Updating location...');
  const [riskSummary, setRiskSummary] = useState<string | null>(null);
  const [currentLocation, setCurrentLocation] = useState<{ latitude: number; longitude: number } | null>(null);
  const webViewRef = useRef<WebView>(null);

  // Initialize Audio
  useEffect(() => {
    const initAudio = async () => {
      const options = {
        sampleRate: 16000,
        channels: 1,
        bitsPerSample: 16,
        audioSource: 6,
        wavFile: 'test.wav'
      };
      AudioRecord.init(options);
    };
    initAudio();
  }, []);

  // Motion Monitoring Logic
  useEffect(() => {
    let subscription: any;
    setUpdateIntervalForType(SensorTypes.accelerometer, 200);

    const monitorMotion = async () => {
      console.log("Starting accelerometer monitoring...");
      try {
        subscription = accelerometer.subscribe(({ x, y, z }) => {
          const magnitude = Math.sqrt(x * x + y * y + z * z);
          // Lower threshold to 1.5g (approx 14.7 m/s^2) for easier testing
          // Earth gravity is ~9.8, so 15 is a firm shake.
          if (magnitude > 15 && !sending) {
            console.log(`Motion detected! Magnitude: ${magnitude.toFixed(2)}`);
            handleMotionCheck({ x, y, z });
          }
        });
      } catch (error) {
        console.error("Accelerometer subscription failed:", error);
      }
    };

    monitorMotion();
    return () => {
      if (subscription) {
        console.log("Stopping accelerometer monitoring...");
        subscription.unsubscribe();
      }
    };
  }, [sending]);

  const handleMotionCheck = async (accel: { x: number, y: number, z: number }) => {
    if (sending) return;
    setSending(true);
    setStatus('Checking potential fall...');

    try {
      const response = await SafetyService.checkMotion({
        accelerometer: accel,
        gyroscope: { x: 0, y: 0, z: 0 }
      });

      if (response.anomaly_detected) {
        setStatus('Analyzing audio environment...');
        await startAudioAnalysis();
      } else {
        setStatus('Movement cleared');
        setTimeout(() => setStatus('You are safe'), 2000);
      }
    } catch (err) {
      console.log("Motion check failed", err);
    } finally {
      setSending(false);
    }
  };

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
        wavFile: 'test.wav'
      };
      AudioRecord.init(options);
      AudioRecord.start();
      await new Promise(resolve => setTimeout(resolve, 3000));
      const audioFile = await AudioRecord.stop();
      const mfcc = await AudioUtils.extractMFCC(audioFile);

      const location = currentLocation || { latitude: 0, longitude: 0 };
      const response = await SafetyService.analyzeAudio({
        audio_mfcc: mfcc,
        location: { lat: location.latitude, lon: location.longitude }
      });

      if (response.emergency_triggered) {
        Alert.alert("Emergency Triggered", "Help is on the way. Your location and audio have been sent.");
        setStatus("Emergency Alert Active");
      } else {
        setStatus("Environment looks safe");
        setTimeout(() => setStatus('You are safe'), 3000);
      }

    } catch (err) {
      console.log("Audio analysis failed", err);
    }
  };

  useEffect(() => {
    let isMounted = true;
    fetchRiskScores()
      .then((scores) => {
        if (!isMounted) return;
        if (!scores.length) {
          setRiskSummary('Safety score: Unknown');
          return;
        }
        const avgRisk = scores.reduce((sum, item) => sum + item.risk_level, 0) / scores.length;
        setRiskSummary(`Safety Score: ${(10 - avgRisk).toFixed(1)}/10`);
      })
      .catch((error) => {
        if (isMounted) setRiskSummary(`Offline Mode`);
      });
    return () => { isMounted = false; };
  }, []);

  useEffect(() => {
    let watchId: number | null = null;
    let isActive = true;

    const updateLocation = (position: GeoPosition) => {
      if (!isActive) return;
      const { latitude, longitude } = position.coords;
      setCurrentLocation({ latitude, longitude });
      setLocationStatus(`You are at: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`);
      webViewRef.current?.postMessage(
        JSON.stringify({ type: 'location', latitude, longitude })
      );
    };

    const startWatching = async () => {
      const hasPermission = await requestLocationPermission();
      if (!hasPermission) {
        setLocationStatus('Location permission unavailable');
        return;
      }
      watchId = Geolocation.watchPosition(
        updateLocation,
        (error) => setLocationStatus(`GPS Error: ${error.message}`),
        { enableHighAccuracy: true, distanceFilter: 5, interval: 2000, fastestInterval: 1000 }
      );
    };

    startWatching();
    return () => {
      isActive = false;
      if (watchId !== null) Geolocation.clearWatch(watchId);
    };
  }, []);

  const handleEmergency = async () => {
    try {
      setSending(true);
      setStatus('Sending SOS...');
      const response = await SafetyService.checkMotion({
        accelerometer: { x: 0, y: 0, z: 0 },
        gyroscope: { x: 0, y: 0, z: 0 }
      });
      if (response) {
        await startAudioAnalysis();
      }
    } catch (error) {
      setStatus(`Connection failed`);
    } finally {
      setSending(false);
    }
  };

  const mapHtml = `<!doctype html>
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
          html, body, #map { height: 100%; margin: 0; padding: 0; background: #FAFAFA; }
          .leaflet-control-attribution { display: none; }
        </style>
      </head>
      <body>
        <div id="map"></div>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
          const map = L.map('map', { zoomControl: false, attributionControl: false }).setView([${initialRegion.latitude}, ${initialRegion.longitude}], 13);
          L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', { maxZoom: 19 }).addTo(map);
          
          const icon = L.divIcon({
            className: 'custom-pin',
            html: '<div style="background-color: #4ECDC4; width: 16px; height: 16px; border: 3px solid white; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.2);"></div>',
            iconSize: [20, 20],
            iconAnchor: [10, 10]
          });
          
          const liveMarker = L.marker([${initialRegion.latitude}, ${initialRegion.longitude}], {icon: icon}).addTo(map);
          let hasCentered = false;

          const updateLocation = (lat, lng) => {
            liveMarker.setLatLng([lat, lng]);
            if (!hasCentered) {
              map.setView([lat, lng], 15);
              hasCentered = true;
            } else {
              map.panTo([lat, lng]);
            }
          };

          const handleMessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              if (data?.type === 'location') {
                updateLocation(data.latitude, data.longitude);
              }
            } catch (err) {}
          };

          document.addEventListener('message', handleMessage);
          window.addEventListener('message', handleMessage);
        </script>
      </body>
    </html>`;

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor={colors.background} />

      {/* Map Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Home</Text>
        <View style={styles.statusPill}>
          <View style={[styles.statusDot, status.includes('Alert') ? styles.dotRed : styles.dotGreen]} />
          <Text style={styles.statusText}>{status}</Text>
        </View>
      </View>

      <View style={styles.mapContainer}>
        <WebView
          ref={webViewRef}
          originWhitelist={['*']}
          source={{ html: mapHtml }}
          style={styles.map}
        />
      </View>

      {/* Bottom Panel */}
      <View style={styles.bottomSheet}>
        <View style={styles.handle} />
        <SectionCard title="Your Safety Status" subtitle={locationStatus} style={styles.card}>
          <Text style={styles.riskText}>{riskSummary || 'Checking safety score...'}</Text>
        </SectionCard>

        <PrimaryButton
          label={sending ? 'Sending Alert...' : 'SOS Emergency'}
          onPress={handleEmergency}
          disabled={sending}
          style={styles.sosButton}
        />
      </View>
    </View>
  );
}

async function requestLocationPermission() {
  if (Platform.OS === 'ios') return true;
  const granted = await PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION);
  return granted === PermissionsAndroid.RESULTS.GRANTED;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingHorizontal: spacing.lg,
    paddingTop: Platform.OS === 'ios' ? 60 : 40,
    paddingBottom: spacing.md,
    backgroundColor: colors.background,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  headerTitle: {
    ...typography.header,
  },
  statusPill: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0F0F0',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  dotGreen: { backgroundColor: colors.success },
  dotRed: { backgroundColor: colors.primary },
  statusText: {
    ...typography.caption,
    color: colors.textSecondary,
    fontWeight: '600',
  },
  mapContainer: {
    flex: 1,
    marginHorizontal: spacing.md,
    borderRadius: 24,
    overflow: 'hidden',
    ...shadows.soft,
  },
  map: {
    flex: 1,
    backgroundColor: '#FAFAFA',
  },
  bottomSheet: {
    padding: spacing.lg,
    paddingBottom: spacing.xl,
    backgroundColor: colors.background,
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
  },
  handle: {
    width: 40,
    height: 4,
    backgroundColor: '#E0E0E0',
    borderRadius: 2,
    alignSelf: 'center',
    marginBottom: spacing.lg,
  },
  card: {
    marginBottom: spacing.lg,
  },
  riskText: {
    ...typography.title,
    color: colors.secondary,
  },
  sosButton: {
    backgroundColor: colors.primary,
    ...shadows.medium,
  },
});
