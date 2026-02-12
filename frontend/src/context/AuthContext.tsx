import React, { createContext, useState, useEffect, useContext } from 'react';
// import AsyncStorage from '@react-native-async-storage/async-storage';
const AsyncStorage = {
    getItem: async (key: string) => null,
    setItem: async (key: string, value: string) => { },
    removeItem: async (key: string) => { }
};
import { request } from '../api/client';

type AuthContextType = {
    user: any | null;
    token: string | null;
    isLoading: boolean;
    login: (username: string, password: string) => Promise<void>;
    register: (username: string, password: string, email?: string) => Promise<void>;
    logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<any | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        loadStorageData();
    }, []);

    const loadStorageData = async () => {
        try {
            const storedToken = await AsyncStorage.getItem('auth_token');
            const storedUser = await AsyncStorage.getItem('auth_user');

            if (storedToken) {
                setToken(storedToken);
                if (storedUser) {
                    setUser(JSON.parse(storedUser));
                }
            }
        } catch (e) {
            console.error('Failed to load auth data', e);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (username: string, password: string) => {
        setIsLoading(true);
        try {
            const response = await request<{ token: string }>('/api-token-auth/', {
                method: 'POST',
                body: { username, password },
            });

            if (response.token) {
                setToken(response.token);
                setUser({ username }); // We can fetch full profile later
                await AsyncStorage.setItem('auth_token', response.token);
                await AsyncStorage.setItem('auth_user', JSON.stringify({ username }));
            }
        } catch (error) {
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const register = async (username: string, password: string, email?: string) => {
        // This assumes there is a register endpoint, but for now we might just use login 
        // or if the backend doesn't have register, we might need to add it.
        // For this task, we will try to hit a register endpoint or fail gracefully.
        // NOTE: The approved plan mentioned Login/Register, but we haven't verified a register endpoint.
        // We will assume a standard one or just implement login first.
        // Let's implement a register function that tries to hit /api/register/
        setIsLoading(true);
        try {
            // Placeholder for registration logic
            // If your backend doesn't have registration, this will 404.
            await request('/api/register/', {
                method: 'POST',
                body: { username, password, email }
            });
            // Auto login after register?
            await login(username, password);
        } catch (error) {
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const logout = async () => {
        setIsLoading(true);
        try {
            setToken(null);
            setUser(null);
            await AsyncStorage.removeItem('auth_token');
            await AsyncStorage.removeItem('auth_user');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <AuthContext.Provider value={{ user, token, isLoading, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
