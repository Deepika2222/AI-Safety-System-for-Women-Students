import React from 'react';
import { Pressable, StyleSheet, Text, ViewStyle } from 'react-native';
import { colors, spacing, typography } from '../theme';

type PrimaryButtonProps = {
  label: string;
  onPress: () => void;
  style?: ViewStyle;
  disabled?: boolean;
};

export function PrimaryButton({ label, onPress, style, disabled }: PrimaryButtonProps) {
  return (
    <Pressable
      accessibilityRole="button"
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        pressed && styles.pressed,
        disabled && styles.disabled,
        style,
      ]}
      disabled={disabled}
    >
      <Text style={styles.text}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: colors.accent,
    borderRadius: 18,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.lg,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000000',
    shadowOpacity: 0.15,
    shadowOffset: { width: 0, height: 8 },
    shadowRadius: 12,
    elevation: 3,
  },
  pressed: {
    transform: [{ scale: 0.98 }],
  },
  disabled: {
    backgroundColor: colors.accentDark,
    opacity: 0.5,
  },
  text: {
    color: '#ffffff',
    ...typography.subtitle,
  },
});
