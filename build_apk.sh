#!/bin/bash

# Local APK Build Script for Better Lyrics
# This script sets up and builds the Android APK locally

set -e

echo "🚀 Starting Better Lyrics Android Build Process"

# Check if required tools are available
command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 is required but not installed. Aborting." >&2; exit 1; }
command -v java >/dev/null 2>&1 || { echo "❌ Java is required but not installed. Aborting." >&2; exit 1; }

echo "✅ Prerequisites check passed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install --upgrade pip setuptools wheel
pip3 install -r requirements.txt
pip3 install buildozer==1.5.0 cython==0.29.36

# Clean previous builds
echo "🧹 Cleaning previous builds..."
buildozer android clean || echo "No previous build to clean"

# Use the Flet-optimized buildozer spec
echo "⚙️ Using Flet-optimized buildozer configuration..."
cp buildozer-flet.spec buildozer.spec

# Build the APK
echo "🔨 Building Android APK..."
buildozer -v android debug

# Check build results
echo "📱 Checking build results..."
if [ -d "bin" ]; then
    echo "✅ Build directory found:"
    ls -la bin/
    
    # Find APK files
    APK_FILES=$(find bin -name "*.apk" -type f)
    if [ -n "$APK_FILES" ]; then
        echo "🎉 APK files built successfully:"
        echo "$APK_FILES"
    else
        echo "⚠️ No APK files found in bin directory"
    fi
else
    echo "❌ No bin directory found"
fi

# Also check .buildozer directory for APK files
BUILDOZER_APKS=$(find .buildozer -name "*.apk" -type f 2>/dev/null || true)
if [ -n "$BUILDOZER_APKS" ]; then
    echo "📱 Additional APK files found in .buildozer:"
    echo "$BUILDOZER_APKS"
fi

echo "✅ Build process completed!"
echo "📝 Check the output above for any errors or warnings"
