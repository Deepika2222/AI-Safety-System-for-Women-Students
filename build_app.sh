#!/usr/bin/env bash
set -e

echo "Building Protego Android App..."

cd frontend/android
./gradlew assembleRelease

echo "Build complete. Copying APK..."
cp app/build/outputs/apk/release/app-release.apk ../../Protego-Release.apk

echo "Done! APK is at Protego-Release.apk"
