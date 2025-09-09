# APK Build Setup Guide for Better Lyrics

## ✅ Already Installed:
- ✅ Python 3.12.2
- ✅ Git 2.50.1
- ✅ Buildozer 1.5.0  
- ✅ Cython 0.29.36
- ✅ Flet and other dependencies

## ❌ Missing Required Components:

### 1. Java JDK (CRITICAL - Required for Android builds)

**Download & Install:**
1. Go to https://adoptium.net/
2. Choose **OpenJDK 11 (LTS)** or **OpenJDK 17 (LTS)**
3. Select your operating system (Windows)
4. Download and run the installer
5. During installation, make sure "Add to PATH" is checked

**Verify Installation:**
After installing, open a new PowerShell window and run:
```powershell
java -version
```

You should see output like:
```
openjdk version "11.0.x" or "17.0.x"
```

### 2. Optional but Recommended:

#### Android Studio (for advanced debugging)
- Download from: https://developer.android.com/studio
- This is optional as buildozer will handle the Android SDK automatically

#### Visual Studio Build Tools (for some Python packages)
- May be needed for certain Python dependencies
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

## 🔧 Fixed Issues:
- ✅ Fixed icon path in buildozer-flet.spec (now uses betterlyrics3.png)

## 📱 Once Java is Installed:

Run the APK build command:
```powershell
.\build_apk.ps1
```

## 🚨 Important Notes:

1. **First build will take 20-60 minutes** - Buildozer downloads Android SDK, NDK, and other components
2. **Internet connection required** - Downloads ~1-2GB of Android development tools
3. **Disk space** - Need at least 5GB free space for Android SDK
4. **Windows Defender** - May need to exclude the project folder from real-time scanning

## 🎯 Build Process:

1. Install Java JDK ⬅️ **YOU ARE HERE**
2. Run `.\build_apk.ps1`
3. Wait for first-time setup (downloads Android SDK automatically)
4. APK will be created in `bin/` folder

## 🐛 Common Issues:

- **"java not found"** - Java not installed or not in PATH
- **"Permission denied"** - Run PowerShell as Administrator
- **"Download failed"** - Check internet connection
- **Build takes forever** - First build is slow, subsequent builds are faster
