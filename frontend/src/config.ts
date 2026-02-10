import { Platform } from 'react-native';

const ANDROID_EMULATOR_HOST = '127.0.0.1'; // Use with adb reverse tcp:8000 tcp:8000
const IOS_SIMULATOR_HOST = '127.0.0.1';

const apiHost = Platform.select({
	android: ANDROID_EMULATOR_HOST,
	ios: IOS_SIMULATOR_HOST,
	default: IOS_SIMULATOR_HOST,
});

export const API_BASE_URL = `http://${apiHost}:8000`;

// Optional token for authenticated endpoints. Leave empty until auth is wired.
export const API_TOKEN = '';
