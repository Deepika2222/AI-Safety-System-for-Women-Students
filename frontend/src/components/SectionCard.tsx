import React from 'react';
import { StyleSheet, Text, View, ViewStyle } from 'react-native';
import { colors, spacing, typography } from '../theme-soft';

type SectionCardProps = {
  title: string;
  children: React.ReactNode;
  subtitle?: string;
  style?: ViewStyle;
};

export function SectionCard({ title, subtitle, children, style }: SectionCardProps) {
  return (
    <View style={[styles.card, style]}>
      <Text style={styles.label}>{title}</Text>
      {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
      <View style={styles.content}>{children}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: 20,
    padding: spacing.lg,
    borderWidth: 1,
    borderColor: colors.border,
    shadowColor: colors.primary, // Subtle tint
    shadowOpacity: 0.05,
    shadowOffset: { width: 0, height: 4 },
    shadowRadius: 12,
    elevation: 3,
    marginBottom: spacing.md,
  },
  label: {
    ...typography.title,
    fontSize: 18,
    marginBottom: 4,
  },
  subtitle: {
    ...typography.caption,
    fontSize: 14,
    color: colors.textSecondary,
  },
  content: {
    marginTop: spacing.sm,
    gap: spacing.sm,
  },
});
