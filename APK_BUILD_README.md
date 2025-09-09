# Better Lyrics - Android APK Build Guide

This document explains how to build the Better Lyrics Android APK using GitHub Actions or locally.

## 🚀 Automated Build with GitHub Actions

We have created multiple GitHub Actions workflows to build the Android APK automatically:

### Available Workflows

1. **`build-apk.yml`** - Main workflow with comprehensive setup
2. **`build-apk-docker.yml`** - Docker-based build for consistency
3. **`build-apk-specialized.yml`** - Using specialized Buildozer action
4. **`build-apk-comprehensive.yml`** - Most comprehensive with caching and optimization

### How to Trigger a Build

1. **Automatic**: Push code to the `master` branch
2. **Manual**: Go to Actions tab → Select a workflow → Click "Run workflow"
3. **Pull Request**: Create a PR targeting `master` branch

### Download the APK

1. Go to the "Actions" tab in your GitHub repository
2. Click on the latest successful workflow run
3. Download the APK from the "Artifacts" section
4. Extract the ZIP file to get your `.apk` file

## 🛠️ Local Development Build

### Prerequisites

- Python 3.11+
- Java JDK 17+
- Android SDK and NDK
- Git

### Quick Build (Windows)

```powershell
# Run the PowerShell build script
.\build_apk.ps1
```

### Quick Build (Linux/macOS)

```bash
# Make the script executable
chmod +x build_apk.sh
# Run the build script
./build_apk.sh
```

### Manual Build Steps

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install buildozer==1.5.0 cython==0.29.36
   ```

2. **Use the Flet-optimized configuration**:
   ```bash
   cp buildozer-flet.spec buildozer.spec
   ```

3. **Build the APK**:
   ```bash
   buildozer android debug
   ```

4. **Find your APK**:
   - Check the `bin/` directory
   - Look for files ending in `.apk`

## 📱 Configuration Files

### `buildozer.spec`
Main Buildozer configuration with standard settings.

### `buildozer-flet.spec`
Optimized configuration for Flet applications with:
- WebView bootstrap for better Flet compatibility
- Required Android permissions
- Androidx support for modern Android features
- Optimized dependencies

## 🔧 Troubleshooting

### Common Issues

1. **Build fails with SDK errors**:
   - Ensure Android SDK is properly installed
   - Accept all SDK licenses: `yes | sdkmanager --licenses`

2. **Python dependencies issues**:
   - Update pip: `pip install --upgrade pip`
   - Install exact versions from requirements.txt

3. **Java version conflicts**:
   - Use Java 17 (recommended for Android builds)
   - Set JAVA_HOME environment variable

4. **Build takes too long**:
   - Use the Docker workflow for consistent builds
   - Enable caching in GitHub Actions (already configured)

### Debugging

1. **Enable verbose logging**:
   ```bash
   buildozer -v android debug
   ```

2. **Check buildozer logs**:
   - Located in `.buildozer/logs/`

3. **Clean build**:
   ```bash
   buildozer android clean
   ```

## 📦 Build Outputs

Successful builds will create:
- `bin/betterlyrics-{version}-arm64-v8a_armeabi-v7a-debug.apk` - Main APK file
- `.buildozer/android/platform/build-*/outputs/apk/debug/` - Alternative location

## 🎯 Testing the APK

1. Enable "Developer Options" and "USB Debugging" on your Android device
2. Install using ADB: `adb install path/to/your.apk`
3. Or transfer the APK to your device and install manually

## 📋 App Features in Mobile Version

- Touch-optimized interface
- Portrait and landscape support  
- Mobile-friendly font sizes
- Gesture controls
- Local song library management
- Playlist support
- Auto-scroll functionality
- Dark/light theme support

## 🤝 Contributing

If you encounter issues with the build process:

1. Check existing GitHub Issues
2. Create a new issue with:
   - Build logs
   - System information
   - Steps to reproduce

---

Happy building! 🎵📱
