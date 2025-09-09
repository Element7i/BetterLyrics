# Quick script to update icon and trigger new build
# Run this AFTER saving the icon as better_lyrics_space_icon.png

Write-Host "🔍 Checking if icon file exists..." -ForegroundColor Blue

if (Test-Path "better_lyrics_space_icon.png") {
    Write-Host "✅ Icon found! Committing changes..." -ForegroundColor Green
    
    git add .
    git commit -m "🎨 Add beautiful space-themed app icon for Android APK

- Replace default icon with stunning space/planet design
- Updates both buildozer.spec and buildozer-flet.spec
- Will be used for app icon and splash screen
- Triggers new APK build with updated branding"
    
    git push origin master
    
    Write-Host "🚀 Changes pushed! New APK build will start automatically." -ForegroundColor Cyan
    Write-Host "📱 Check GitHub Actions for build progress." -ForegroundColor Yellow
    
} else {
    Write-Host "❌ Icon file not found!" -ForegroundColor Red
    Write-Host "📋 Please save the image as: better_lyrics_space_icon.png" -ForegroundColor Yellow
    Write-Host "📂 In folder: $PWD" -ForegroundColor Yellow
}
