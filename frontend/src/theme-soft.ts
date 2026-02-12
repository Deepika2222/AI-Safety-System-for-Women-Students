export const colors = {
    background: '#FAFAFA', // Warm white
    surface: '#FFFFFF',    // Pure white
    primary: '#FF6B6B',    // Soft Red/Salmon (SOS)
    secondary: '#4ECDC4',  // Teal (Safe/Active)
    text: '#2D3436',       // Dark Charcoal
    textSecondary: '#636E72',
    border: '#F0F0F0',
    success: '#55EFC4',
    warning: '#FFEAA7',
    error: '#FF7675',
    cardBackground: '#FFFFFF',
};

export const spacing = {
    xs: 8,
    sm: 12,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 40,
};

export const shadows = {
    soft: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.05,
        shadowRadius: 15,
        elevation: 3,
    },
    medium: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.1,
        shadowRadius: 12,
        elevation: 5,
    },
    floating: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 10 },
        shadowOpacity: 0.15,
        shadowRadius: 20,
        elevation: 10,
    }
};

export const typography = {
    header: {
        fontSize: 28,
        fontWeight: '700' as const,
        color: colors.text,
        letterSpacing: -0.5,
    },
    title: {
        fontSize: 20,
        fontWeight: '600' as const,
        color: colors.text,
        letterSpacing: -0.2,
    },
    subtitle: {
        fontSize: 16,
        fontWeight: '500' as const,
        color: colors.textSecondary,
    },
    body: {
        fontSize: 15,
        fontWeight: '400' as const,
        color: colors.textSecondary,
        lineHeight: 24,
    },
    caption: {
        fontSize: 13,
        fontWeight: '500' as const,
        color: colors.textSecondary,
    },
    subhead: {
        fontSize: 14,
        fontWeight: '600' as const,
        color: colors.text,
        letterSpacing: 0.5,
    },
    button: {
        fontSize: 16,
        fontWeight: '600' as const,
        color: colors.surface,
        letterSpacing: 1,
    }
};
