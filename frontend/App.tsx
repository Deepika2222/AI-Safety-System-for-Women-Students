import React, { useMemo, useState } from 'react';
import { SafeAreaView, StatusBar, StyleSheet, Text, Pressable, View } from 'react-native';
import { MapScreen } from './src/screens/MapScreen';
import { ProfileScreen } from './src/screens/ProfileScreen';
import { SettingsScreen } from './src/screens/SettingsScreen';
import { colors, spacing, typography, shadows } from './src/theme-soft';

type TabKey = 'map' | 'profile' | 'settings';

function App() {
  const [tab, setTab] = useState<TabKey>('map');

  const screen = useMemo(() => {
    if (tab === 'profile') {
      return <ProfileScreen />;
    }
    if (tab === 'settings') {
      return <SettingsScreen />;
    }
    return <MapScreen />;
  }, [tab]);

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor={colors.background} />
      <View style={styles.content}>{screen}</View>
      <View style={styles.tabBar}>
        <TabButton label="Home" active={tab === 'map'} onPress={() => setTab('map')} />
        <TabButton label="Profile" active={tab === 'profile'} onPress={() => setTab('profile')} />
        <TabButton label="Settings" active={tab === 'settings'} onPress={() => setTab('settings')} />
      </View>
    </SafeAreaView>
  );
}

type TabButtonProps = {
  label: string;
  active: boolean;
  onPress: () => void;
};

function TabButton({ label, active, onPress }: TabButtonProps) {
  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      style={({ pressed }) => [
        styles.tabButton,
        active && styles.tabButtonActive,
        pressed && styles.tabButtonPressed
      ]}
    >
      <Text style={[styles.tabLabel, active && styles.tabLabelActive]}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    flex: 1,
  },
  tabBar: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.xl,
    paddingBottom: spacing.lg,
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
    ...shadows.floating,
  },
  tabButton: {
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.lg,
    borderRadius: 20,
    alignItems: 'center',
  },
  tabButtonActive: {
    backgroundColor: '#F0FDF4', // Very light green
  },
  tabButtonPressed: {
    opacity: 0.7,
  },
  tabLabel: {
    color: '#BDBDBD',
    ...typography.caption,
    fontWeight: '600',
  },
  tabLabelActive: {
    color: colors.primary,
  },
});

export default App;
