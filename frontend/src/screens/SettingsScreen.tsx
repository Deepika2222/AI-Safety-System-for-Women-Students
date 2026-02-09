import React, { useState } from 'react';
import { ScrollView, StyleSheet, Switch, Text, View } from 'react-native';
import { SectionCard } from '../components/SectionCard';
import { colors, spacing, typography } from '../theme';

export function SettingsScreen() {
  const [shareLocation, setShareLocation] = useState(true);
  const [autoDetect, setAutoDetect] = useState(true);
  const [nightMode, setNightMode] = useState(false);

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Settings</Text>

      <SectionCard title="Safety Controls" subtitle="Tune your protection level">
        <View style={styles.settingRow}>
          <View>
            <Text style={styles.settingTitle}>Share live location</Text>
            <Text style={styles.settingText}>Allow safety center to track real-time location.</Text>
          </View>
          <Switch value={shareLocation} onValueChange={setShareLocation} />
        </View>
        <View style={styles.settingRow}>
          <View>
            <Text style={styles.settingTitle}>Auto emergency detection</Text>
            <Text style={styles.settingText}>Use sensors to auto-trigger alerts.</Text>
          </View>
          <Switch value={autoDetect} onValueChange={setAutoDetect} />
        </View>
      </SectionCard>

      <SectionCard title="App Experience" subtitle="Personalize the interface">
        <View style={styles.settingRow}>
          <View>
            <Text style={styles.settingTitle}>Night mode</Text>
            <Text style={styles.settingText}>Reduce glare in low light environments.</Text>
          </View>
          <Switch value={nightMode} onValueChange={setNightMode} />
        </View>
      </SectionCard>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: spacing.lg,
    gap: spacing.md,
    backgroundColor: colors.background,
  },
  title: {
    color: colors.text,
    ...typography.title,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
    gap: spacing.sm,
  },
  settingTitle: {
    color: colors.text,
    ...typography.subtitle,
  },
  settingText: {
    color: colors.muted,
    ...typography.body,
  },
});
