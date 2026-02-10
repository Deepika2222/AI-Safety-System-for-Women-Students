import React, { useState } from 'react';
import { ScrollView, StyleSheet, Switch, Text, View } from 'react-native';
import { SectionCard } from '../components/SectionCard';
import { colors, spacing, typography } from '../theme-soft';

export function SettingsScreen() {
  const [shareLocation, setShareLocation] = useState(true);
  const [autoDetect, setAutoDetect] = useState(true);
  const [nightMode, setNightMode] = useState(false);

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.header}>Settings</Text>

      <SectionCard title="Protection & Privacy">
        <View style={styles.settingRow}>
          <View style={styles.textGroup}>
            <Text style={styles.settingTitle}>Live Location Sharing</Text>
            <Text style={styles.settingText}>Allow trusted contacts to see where you are.</Text>
          </View>
          <Switch
            value={shareLocation}
            onValueChange={setShareLocation}
            trackColor={{ false: '#E0E0E0', true: colors.success }}
            thumbColor={'#FFFFFF'}
          />
        </View>
        <View style={styles.settingRow}>
          <View style={styles.textGroup}>
            <Text style={styles.settingTitle}>Smart Crash Detection</Text>
            <Text style={styles.settingText}>Automatically alert if a fall or impact is detected.</Text>
          </View>
          <Switch
            value={autoDetect}
            onValueChange={setAutoDetect}
            trackColor={{ false: '#E0E0E0', true: colors.success }}
            thumbColor={'#FFFFFF'}
          />
        </View>
      </SectionCard>

      <SectionCard title="Preferences">
        <View style={styles.settingRow}>
          <View style={styles.textGroup}>
            <Text style={styles.settingTitle}>Dark Mode</Text>
            <Text style={styles.settingText}>Easier on the eyes at night.</Text>
          </View>
          <Switch
            value={nightMode}
            onValueChange={setNightMode}
            trackColor={{ false: '#E0E0E0', true: colors.primary }}
            thumbColor={'#FFFFFF'}
          />
        </View>
      </SectionCard>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: spacing.lg,
    paddingTop: 60,
    gap: spacing.lg,
    backgroundColor: colors.background,
    minHeight: '100%',
  },
  header: {
    ...typography.header,
    marginBottom: spacing.xs,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
    paddingBottom: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  textGroup: {
    flex: 1,
    paddingRight: spacing.md,
  },
  settingTitle: {
    ...typography.title,
    fontSize: 16,
    marginBottom: 4,
  },
  settingText: {
    ...typography.body,
    fontSize: 13,
  },
});
