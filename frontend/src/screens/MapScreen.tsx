import React, { useEffect, useMemo, useState } from 'react';
import { ActivityIndicator, Alert, StyleSheet, Text, View } from 'react-native';
import { WebView } from 'react-native-webview';
import { detectEmergency } from '../api/safety';
import { fetchRiskScores } from '../api/routing';
import { PrimaryButton } from '../components/PrimaryButton';
import { SectionCard } from '../components/SectionCard';
import { colors, spacing, typography } from '../theme';

const initialRegion = {
  latitude: 12.9716,
  longitude: 77.5946,
  latitudeDelta: 0.05,
  longitudeDelta: 0.05,
};

export function MapScreen() {
  const [sending, setSending] = useState(false);
  const [status, setStatus] = useState('Ready');
  const [riskSummary, setRiskSummary] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    fetchRiskScores()
      .then((scores) => {
        if (!isMounted) return;
        if (!scores.length) {
          setRiskSummary('No risk scores yet.');
          return;
        }
        const avgRisk = scores.reduce((sum, item) => sum + item.risk_level, 0) / scores.length;
        setRiskSummary(`Average risk score: ${avgRisk.toFixed(2)}`);
      })
      .catch((error) => {
        if (isMounted) {
          setRiskSummary(`API not connected: ${error.message}`);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const emergencyPayload = useMemo(
    () => ({
      timestamp: new Date().toISOString(),
      latitude: initialRegion.latitude,
      longitude: initialRegion.longitude,
      accelerometer_data: { magnitude: 2.2 },
      audio_data: { scream_probability: 0.4 },
    }),
    []
  );

  const handleEmergency = async () => {
    try {
      setSending(true);
      setStatus('Sending emergency alert...');
      const response = await detectEmergency(emergencyPayload);
      setStatus(`Emergency: ${response.is_emergency ? 'YES' : 'NO'} • Risk ${response.fused_risk_score.toFixed(2)}`);
      Alert.alert('Emergency Triggered', response.message);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      setStatus(`Failed to send: ${message}`);
    } finally {
      setSending(false);
    }
  };

  const mapHtml = `<!doctype html>
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossorigin=""
        />
        <style>
          html, body, #map { height: 100%; margin: 0; padding: 0; }
          .leaflet-control-attribution { font-size: 10px; }
        </style>
      </head>
      <body>
        <div id="map"></div>
        <script
          src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
          integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
          crossorigin=""
        ></script>
        <script>
          const map = L.map('map').setView([${initialRegion.latitude}, ${initialRegion.longitude}], 13);
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap contributors'
          }).addTo(map);
          L.marker([${initialRegion.latitude}, ${initialRegion.longitude}]).addTo(map);
        </script>
      </body>
    </html>`;

  return (
    <View style={styles.container}>
      <View style={styles.mapWrapper}>
        <WebView originWhitelist={['*']} source={{ html: mapHtml }} style={styles.map} />
      </View>

      <View style={styles.panel}>
        <SectionCard title="Map Status" subtitle={status}>
          <Text style={styles.bodyText}>Tap SOS if you feel unsafe. The app sends a detection request.</Text>
          <View style={styles.riskRow}>
            {riskSummary ? (
              <Text style={styles.riskText}>{riskSummary}</Text>
            ) : (
              <ActivityIndicator size="small" color={colors.accent} />
            )}
          </View>
        </SectionCard>

        <PrimaryButton
          label={sending ? 'Sending...' : 'Trigger SOS'}
          onPress={handleEmergency}
          disabled={sending}
          style={styles.sosButton}
        />

        <Text style={styles.noteText}>
          For real devices over USB, run adb reverse tcp:8000 tcp:8000 and keep the API at http://127.0.0.1:8000.
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
  mapWrapper: {
    flex: 1.1,
    borderBottomLeftRadius: 28,
    borderBottomRightRadius: 28,
    overflow: 'hidden',
    marginBottom: spacing.sm,
  },
  map: {
    flex: 1,
    backgroundColor: colors.background,
  },
  panel: {
    flex: 1,
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.lg,
    gap: spacing.md,
  },
  bodyText: {
    color: colors.text,
    ...typography.body,
  },
  riskRow: {
    marginTop: spacing.sm,
  },
  riskText: {
    color: colors.success,
    ...typography.subtitle,
  },
  sosButton: {
    paddingVertical: spacing.md,
  },
  noteText: {
    color: colors.muted,
    ...typography.body,
  },
});
