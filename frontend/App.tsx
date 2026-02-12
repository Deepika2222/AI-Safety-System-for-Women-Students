import React, { useMemo, useState, useEffect } from 'react';
import { SafeAreaView, StatusBar, StyleSheet, Text, Pressable, View } from 'react-native';
import { BackgroundSafetyRunner } from './src/services/BackgroundSafetyService';
import { HomeScreen } from './src/screens/HomeScreen';
import { MapScreen } from './src/screens/MapScreen';
import { SosScreen } from './src/screens/SosScreen';
import { ProfileScreen } from './src/screens/ProfileScreen';
import { SettingsScreen } from './src/screens/SettingsScreen';
import { colors, spacing, typography, shadows } from './src/theme-soft';

type TabKey = 'home' | 'map' | 'sos' | 'profile' | 'settings';

function App() {
  const [tab, setTab] = useState<TabKey>('home');

  useEffect(() => {
    BackgroundSafetyRunner.start();
  }, []);

  const screen = useMemo(() => {
    switch (tab) {
      case 'home': return <HomeScreen />;
      case 'map': return <MapScreen />;
      case 'sos': return <SosScreen />;
      case 'profile': return <ProfileScreen />;
      case 'settings': return <SettingsScreen />;
      default: return <HomeScreen />;
    }
  }, [tab]);

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor={colors.background} />
      <View style={styles.content}>{screen}</View>
      <View style={styles.tabBar}>
        <TabButton label="Home" active={tab === 'home'} onPress={() => setTab('home')} />
        <TabButton label="Map" active={tab === 'map'} onPress={() => setTab('map')} />

        {/* Special SOS Tab Button */}
        <Pressable
          style={[styles.sosTab, tab === 'sos' && styles.sosTabActive]}
          onPress={() => setTab('sos')}
        >
          <Text style={styles.sosTabLabel}>SOS</Text>
        </Pressable>

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
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.lg,
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
    ...shadows.floating,
  },
  tabButton: {
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.sm,
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
    ...typography.caption,
    color: '#BDBDBD', // Override caption color
    fontWeight: '600',
    fontSize: 10,
  },
  tabLabelActive: {
    color: colors.secondary,
  },
  sosTab: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: -20, // Pop out effect
    ...shadows.medium,
  },
  sosTabActive: {
    transform: [{ scale: 1.1 }],
    backgroundColor: '#D32F2F',
  },
  sosTabLabel: {
    color: '#FFF',
    fontSize: 10,
    fontWeight: 'bold',
  }
});

export default App;
