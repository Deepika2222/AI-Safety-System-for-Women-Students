import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, Switch, Alert, TouchableOpacity } from 'react-native';
import { SectionCard } from '../components/SectionCard';
import { colors, spacing, typography, shadows } from '../theme-soft';
import { useAuth } from '../context/AuthContext';
import { accelerometer, setUpdateIntervalForType, SensorTypes } from 'react-native-sensors';

export function SettingsScreen() {
  const { user, logout } = useAuth();
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [backgroundLocation, setBackgroundLocation] = useState(true);
  const [shakeSensitivity, setShakeSensitivity] = useState(1.5);

  // Sensor Test State
  const [isTestingSensors, setIsTestingSensors] = useState(false);
  const [sensorData, setSensorData] = useState<{ x: number, y: number, z: number } | null>(null);

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Logout', onPress: logout, style: 'destructive' }
    ]);
  };

  useEffect(() => {
    let subscription: any;
    if (isTestingSensors) {
      setUpdateIntervalForType(SensorTypes.accelerometer, 200);
      subscription = accelerometer.subscribe(({ x, y, z }) => {
        setSensorData({ x, y, z });
      });
    } else {
      setSensorData(null);
    }
    return () => {
      if (subscription) subscription.unsubscribe();
    };
  }, [isTestingSensors]);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Settings</Text>
      </View>

      {/* Profile Section */}
      <SectionCard title="Account" style={styles.card}>
        <View style={styles.row}>
          <Text style={styles.label}>Username</Text>
          <Text style={styles.value}>{user?.username || 'Guest'}</Text>
        </View>
        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Text style={styles.logoutText}>Log Out</Text>
        </TouchableOpacity>
      </SectionCard>

      {/* Safety Preferences */}
      <SectionCard title="Safety Preferences" style={styles.card}>
        <View style={styles.optionRow}>
          <Text style={styles.optionLabel}>Push Notifications</Text>
          <Switch
            value={notificationsEnabled}
            onValueChange={setNotificationsEnabled}
            trackColor={{ false: '#767577', true: colors.secondary }}
          />
        </View>
        <View style={styles.optionRow}>
          <Text style={styles.optionLabel}>Background Protection</Text>
          <Switch
            value={backgroundLocation}
            onValueChange={setBackgroundLocation}
            trackColor={{ false: '#767577', true: colors.secondary }}
          />
        </View>
      </SectionCard>

      {/* Sensor Diagnostics */}
      <SectionCard title="Diagnostics" style={styles.card}>
        <View style={styles.optionRow}>
          <Text style={styles.optionLabel}>Test Accelerometer</Text>
          <Switch
            value={isTestingSensors}
            onValueChange={setIsTestingSensors}
            trackColor={{ false: '#767577', true: colors.primary }}
          />
        </View>
        {isTestingSensors && sensorData && (
          <View style={styles.sensorDebug}>
            <Text style={styles.debugText}>X: {sensorData.x.toFixed(2)}</Text>
            <Text style={styles.debugText}>Y: {sensorData.y.toFixed(2)}</Text>
            <Text style={styles.debugText}>Z: {sensorData.z.toFixed(2)}</Text>
            <Text style={styles.debugText}>Vector: {Math.sqrt(sensorData.x ** 2 + sensorData.y ** 2 + sensorData.z ** 2).toFixed(2)}</Text>
          </View>
        )}
        {isTestingSensors && !sensorData && (
          <Text style={styles.debugText}>Waiting for sensor data...</Text>
        )}
      </SectionCard>

      <View style={styles.footer}>
        <Text style={styles.version}>Protego v0.0.1</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: spacing.lg,
    paddingTop: 60,
  },
  header: {
    marginBottom: spacing.lg,
  },
  title: {
    ...typography.header,
    color: colors.text,
  },
  card: {
    marginBottom: spacing.lg,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.md,
  },
  label: {
    ...typography.body,
    color: colors.textSecondary,
  },
  value: {
    ...typography.body,
    color: colors.text,
    fontWeight: '600',
  },
  optionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  optionLabel: {
    ...typography.body,
    color: colors.text,
  },
  logoutButton: {
    marginTop: spacing.sm,
    paddingVertical: spacing.sm,
    alignItems: 'center',
  },
  logoutText: {
    ...typography.button,
    color: colors.error,
  },
  footer: {
    alignItems: 'center',
    paddingBottom: spacing.xl,
  },
  version: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  sensorDebug: {
    marginTop: spacing.sm,
    padding: spacing.sm,
    backgroundColor: '#F3F3F3',
    borderRadius: 8,
  },
  debugText: {
    fontFamily: 'monospace',
    fontSize: 12,
    color: colors.text,
  }
});
