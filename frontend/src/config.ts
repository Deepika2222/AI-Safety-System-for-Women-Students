import { NativeModules, Platform } from 'react-native';

const DEV_SERVER_HOST = (() => {
	const scriptURL = NativeModules.SourceCode?.scriptURL as string | undefined;
	if (!scriptURL) {
		return null;
	}
	const match = scriptURL.match(/https?:\/\/([^:/]+)/);
	return match ? match[1] : null;
})();

const ANDROID_DEVICE_HOST = DEV_SERVER_HOST || '192.168.1.10'; // TODO: Update with your PC's IP if not using Metro
const IOS_SIMULATOR_HOST = DEV_SERVER_HOST || '127.0.0.1';

const PROD_BACKEND_URL = 'https://ai-safety-system-for-women-students.onrender.com'; // Render backend URL

const apiHost = Platform.select({
	android: ANDROID_DEVICE_HOST,
	ios: IOS_SIMULATOR_HOST,
	default: IOS_SIMULATOR_HOST,
});

// Use production backend for release builds (no Metro)
const IS_PROD = !__DEV__;

// FORCE production URL as per user request to run "anywhere"
export const API_BASE_URL = PROD_BACKEND_URL;

// Original logic preserved for reference:
// export const API_BASE_URL = IS_PROD
// 	? PROD_BACKEND_URL
// 	: `http://${apiHost}:8000`;

// Optional token for authenticated endpoints. Leave empty until auth is wired.
export const API_TOKEN = '';
