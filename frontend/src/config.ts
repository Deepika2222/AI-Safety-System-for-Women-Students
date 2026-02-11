import { NativeModules, Platform } from 'react-native';

const DEV_SERVER_HOST = (() => {
	const scriptURL = NativeModules.SourceCode?.scriptURL as string | undefined;
	if (!scriptURL) {
		return null;
	}
	const match = scriptURL.match(/https?:\/\/([^:/]+)/);
	return match ? match[1] : null;
})();

const ANDROID_DEVICE_HOST = DEV_SERVER_HOST || '192.168.1.10'; // Fallback to PC LAN IP
const IOS_SIMULATOR_HOST = DEV_SERVER_HOST || '127.0.0.1';

const PROD_BACKEND_URL = 'https://ai-safety-system-for-women-students.onrender.com'; // REPLACE WITH YOUR RENDER URL

const apiHost = Platform.select({
	android: ANDROID_DEVICE_HOST,
	ios: IOS_SIMULATOR_HOST,
	default: IOS_SIMULATOR_HOST,
});

// Set this to true when building for release/production
const IS_PROD = false;

export const API_BASE_URL = IS_PROD
	? PROD_BACKEND_URL
	: `http://${apiHost}:8000`;

// Optional token for authenticated endpoints. Leave empty until auth is wired.
export const API_TOKEN = '';
