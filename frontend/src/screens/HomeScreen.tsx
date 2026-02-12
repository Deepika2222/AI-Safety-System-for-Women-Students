import React from 'react';
import { View, Text, StyleSheet, Image, ScrollView, TouchableOpacity, Linking } from 'react-native';
import { colors, spacing, typography, shadows } from '../theme-soft';
import { SectionCard } from '../components/SectionCard';

export function HomeScreen() {
    return (
        <ScrollView style={styles.container} contentContainerStyle={styles.content}>
            {/* Hero Section */}
            <View style={styles.hero}>
                <View style={styles.logoContainer}>
                    {/* Placeholder for Logo if image not available, user can replace later */}
                    <View style={styles.logoPlaceholder}>
                        <Text style={styles.logoText}>P</Text>
                    </View>
                </View>
                <Text style={styles.title}>Protego</Text>
                <Text style={styles.subtitle}>AI Safety System for Women Students</Text>
            </View>

            {/* Status Card */}
            <SectionCard title="System Status" style={styles.card}>
                <View style={styles.statusRow}>
                    <View style={[styles.dot, { backgroundColor: colors.success }]} />
                    <Text style={styles.statusText}>Background Protection Active</Text>
                </View>
                <Text style={styles.description}>
                    Shake your phone firmly to trigger an SOS alert, even when the app is closed.
                </Text>
            </SectionCard>

            {/* Features Grid */}
            <Text style={styles.sectionHeader}>Features</Text>

            <View style={styles.grid}>
                <View style={styles.gridItem}>
                    <Text style={styles.gridEmoji}>📍</Text>
                    <Text style={styles.gridTitle}>Safe Routing</Text>
                    <Text style={styles.gridDesc}>AI-powered navigation avoiding high-risk areas.</Text>
                </View>
                <View style={styles.gridItem}>
                    <Text style={styles.gridEmoji}>🆘</Text>
                    <Text style={styles.gridTitle}>Smart SOS</Text>
                    <Text style={styles.gridDesc}>Motion & Audio analysis to detect emergencies.</Text>
                </View>
            </View>

            <TouchableOpacity style={styles.helpButton} onPress={() => Linking.openURL('tel:100')}>
                <Text style={styles.helpButtonText}>Call Police (100)</Text>
            </TouchableOpacity>

        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background,
    },
    content: {
        padding: spacing.lg,
        paddingTop: 60,
    },
    hero: {
        alignItems: 'center',
        marginBottom: spacing.xl,
    },
    logoContainer: {
        marginBottom: spacing.md,
        ...shadows.medium,
    },
    logoPlaceholder: {
        width: 80,
        height: 80,
        borderRadius: 40,
        backgroundColor: colors.primary,
        justifyContent: 'center',
        alignItems: 'center',
    },
    logoText: {
        fontSize: 40,
        color: '#FFF',
        fontWeight: 'bold',
    },
    title: {
        ...typography.header,
        color: colors.text,
        fontSize: 32,
        marginBottom: spacing.xs,
    },
    subtitle: {
        ...typography.body,
        color: colors.textSecondary,
        textAlign: 'center',
    },
    card: {
        marginBottom: spacing.lg,
    },
    statusRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: spacing.sm,
    },
    dot: {
        width: 10,
        height: 10,
        borderRadius: 5,
        marginRight: spacing.sm,
    },
    statusText: {
        ...typography.subhead,
        color: colors.success,
        fontWeight: '600',
    },
    description: {
        ...typography.caption,
        color: colors.textSecondary,
        lineHeight: 20,
    },
    sectionHeader: {
        ...typography.title,
        marginBottom: spacing.md,
        color: colors.text,
    },
    grid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        marginBottom: spacing.lg,
    },
    gridItem: {
        width: '48%',
        backgroundColor: colors.surface,
        padding: spacing.md,
        borderRadius: 16,
        marginBottom: spacing.md,
        ...shadows.soft,
    },
    gridEmoji: {
        fontSize: 32,
        marginBottom: spacing.sm,
    },
    gridTitle: {
        ...typography.subhead,
        color: colors.text,
        marginBottom: 4,
    },
    gridDesc: {
        ...typography.caption,
        color: colors.textSecondary,
        fontSize: 12,
    },
    helpButton: {
        backgroundColor: colors.surface,
        padding: spacing.md,
        borderRadius: 12,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: '#E0E0E0',
    },
    helpButtonText: {
        ...typography.button,
        color: colors.primary,
    }
});
