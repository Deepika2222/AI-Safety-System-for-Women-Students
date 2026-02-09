export const colors = {
  background: '#f4f1ec',
  panel: '#ffffff',
  text: '#1f1f1f',
  muted: '#6b6b6b',
  accent: '#c0392b',
  accentDark: '#8e2c22',
  border: '#e0d9cf',
  success: '#2d7d46',
  warning: '#b56b1c',
};

export const spacing = {
  xs: 8,
  sm: 12,
  md: 16,
  lg: 20,
  xl: 28,
};

export const typography = {
  title: {
    fontSize: 22,
    fontWeight: '700' as const,
    letterSpacing: 0.2,
  },
  subtitle: {
    fontSize: 16,
    fontWeight: '600' as const,
  },
  body: {
    fontSize: 14,
    fontWeight: '400' as const,
  },
  label: {
    fontSize: 12,
    fontWeight: '600' as const,
    textTransform: 'uppercase' as const,
    letterSpacing: 1.1,
  },
};
