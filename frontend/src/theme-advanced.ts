export const colors = {
    background: '#0F111A', // Deep dark blue/black
    surface: '#1A1D2D',    // Slightly lighter for cards
    primary: '#FF2A68',    // Neon Red/Pink for SOS
    secondary: '#05F2DB',  // Cyan for Status/Safe
    text: '#FFFFFF',
    textSecondary: '#A0A3BD',
    border: 'rgba(255, 255, 255, 0.1)',
    success: '#00E676',
    warning: '#FFD600',
    error: '#FF453A',
    overlay: 'rgba(15, 17, 26, 0.8)',
};

export const spacing = {
    xs: 8,
    sm: 12,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
};

export const shadows = {
    soft: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.2,
        shadowRadius: 8,
        elevation: 4,
    },
    glow: {
        shadowColor: '#FF2A68',
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.4,
        shadowRadius: 12,
        elevation: 8,
    },
};

export const typography = {
    header: {
        fontSize: 28,
        fontWeight: '800' as const,
        color: colors.text,
        letterSpacing: 0.5,
    },
    title: {
        fontSize: 20,
        fontWeight: '700' as const,
        color: colors.text,
        letterSpacing: 0.3,
    },
    subtitle: {
        fontSize: 16,
        fontWeight: '600' as const,
        color: colors.textSecondary,
        letterSpacing: 0.2,
    },
    body: {
        fontSize: 14,
        fontWeight: '400' as const,
        color: colors.textSecondary,
        lineHeight: 22,
    },
    caption: {
        fontSize: 12,
        fontWeight: '500' as const,
        color: colors.textSecondary,
        textTransform: 'uppercase' as const,
        letterSpacing: 1,
    },
};
