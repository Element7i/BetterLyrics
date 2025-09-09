@echo off
echo 🎨 Better Lyrics Icon Updater
echo.
echo 🔍 Checking for icon file...

if exist "better_lyrics_space_icon.png" (
    echo ✅ Icon found! Updating APK build...
    echo.
    echo 📝 Adding files to git...
    git add .
    
    echo 💾 Committing changes...
    git commit -m "🎨 Add beautiful space-themed app icon for Android APK - Replace default icon with stunning space/planet design - Updates both buildozer configurations - Will be used for app icon and splash screen - Triggers new APK build with updated branding"
    
    echo 🚀 Pushing to GitHub...
    git push origin master
    
    echo.
    echo ✅ SUCCESS! New APK build started automatically!
    echo 📱 Check GitHub Actions: https://github.com/Element7i/BetterLyrics/actions
    echo.
    pause
) else (
    echo ❌ Icon file not found!
    echo.
    echo 📋 Please save the space icon image as: better_lyrics_space_icon.png
    echo 📂 In this folder: %CD%
    echo.
    echo 💡 Then run this script again.
    echo.
    pause
)
