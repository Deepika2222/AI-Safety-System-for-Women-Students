# Mobile App "Deployment" Guide

Since the frontend is a React Native mobile application, it isn't "deployed" like a website. Instead, you build it into an executable file (APK for Android, IPA for iOS) and install it on devices.

## 1. Configure for Production

Before building, you must point the app to your deployed Render backend.

1.  Open `frontend/src/config.ts`.
2.  Find the `PROD_BACKEND_URL` constant and replace the placeholder with your actual Render URL (e.g., `https://your-service-name.onrender.com`).
3.  Set `const IS_PROD = true;`.
4.  Save the file.

## 2. Build Android APK

To generate an APK file that you can install on your Android phone:

1.  Open a terminal in the `frontend` directory.
2.  Run the following command:
    ```bash
    cd android && ./gradlew assembleRelease
    ```
    *(Note: On Windows, use `gradlew assembleRelease`)*

3.  Once the build finishes, you can find the APK at:
    `frontend/android/app/build/outputs/apk/release/app-release.apk`

## 3. Install on Device

1.  Transfer the `app-release.apk` file to your Android phone (via USB, Google Drive, etc.).
2.  Tap the file on your phone to install it.
    *(You may need to allow installation from unknown sources)*.

## 4. iOS (Requires Mac)

Building for iOS requires a Mac with Xcode.
1.  Open `frontend/ios/AI_Safety_System.xcworkspace` in Xcode.
2.  Select your target device or "Generic iOS Device".
3.  Go to **Product > Archive**.
4.  Follow the steps to distribute the app (e.g., Ad Hoc or App Store).
