[app]

# (str) Title of your application
title = Better Lyrics

# (str) Package name
package.name = betterlyrics

# (str) Package domain (needed for android/ios packaging)
package.domain = com.betterlyrics

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,md,txt,ico

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,flet==0.28.3,pyperclip,certifi,charset-normalizer,idna,urllib3,websockets,watchdog,pathspec,packaging

# (str) Presplash of the application
presplash.filename = betterlyrics3.png

# (str) Icon of the application
icon.filename = betterlyrics3.png

# (str) Supported orientation (portrait or landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 23b

# (int) Android SDK version to use
android.sdk = 33

# (str) Bootstrap to use for android builds
p4a.bootstrap = webview

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) Android app theme for Flet
android.theme = "@android:style/Theme.NoTitleBar.Fullscreen"

# Enable androidx support for modern Android
android.enable_androidx = True

# Gradle dependencies for Flet/WebView
android.gradle_dependencies = androidx.webkit:webkit:1.4.0, androidx.browser:browser:1.4.0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# Android SDK and NDK paths for GitHub Actions
android.sdk_path = 
android.ndk_path = 
android.accept_sdk_license = True
