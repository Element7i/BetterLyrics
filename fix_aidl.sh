#!/bin/bash
# Fix AIDL issue by ensuring Buildozer can find the Android SDK build-tools

echo "🔧 Fixing AIDL path issue..."

# Ensure Buildozer directory exists
mkdir -p ~/.buildozer/android/platform/

# Remove any existing android-sdk link/directory
rm -rf ~/.buildozer/android/platform/android-sdk

# Create symlink from Buildozer's expected location to system Android SDK
echo "Creating symlink: ~/.buildozer/android/platform/android-sdk -> $ANDROID_HOME"
ln -sf "$ANDROID_HOME" ~/.buildozer/android/platform/android-sdk

# Verify the build-tools and AIDL are accessible
echo "Verifying AIDL availability:"
if [ -f "$ANDROID_HOME/build-tools/34.0.0/aidl" ]; then
    echo "✅ AIDL found in system Android SDK: $ANDROID_HOME/build-tools/34.0.0/aidl"
else
    echo "❌ AIDL not found in system Android SDK"
    find "$ANDROID_HOME" -name "aidl" -type f 2>/dev/null || echo "No AIDL found anywhere in Android SDK"
fi

if [ -f ~/.buildozer/android/platform/android-sdk/build-tools/34.0.0/aidl ]; then
    echo "✅ AIDL accessible through Buildozer path"
else
    echo "❌ AIDL not accessible through Buildozer path"
    ls -la ~/.buildozer/android/platform/android-sdk/build-tools/ || echo "No build-tools directory found"
fi

echo "🔧 AIDL fix completed!"
