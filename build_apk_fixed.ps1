# Fixed APK Build Script for Better Lyrics (PowerShell)
# This script sets up and builds the Android APK locally on Windows

Write-Host "🚀 Starting Better Lyrics Android Build Process" -ForegroundColor Green

# Ensure Java is available
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-21.0.8.9-hotspot\bin"
$env:PATH = "$javaPath;$env:PATH"
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.8.9-hotspot"

# Check if required tools are available
try {
    $null = python --version 2>$null
    Write-Host "✅ Python found" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is required but not found. Please install Python and add it to PATH." -ForegroundColor Red
    exit 1
}

try {
    $null = java -version 2>$null
    Write-Host "✅ Java found" -ForegroundColor Green
} catch {
    Write-Host "❌ Java is required but not found. Please install Java JDK and add it to PATH." -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Blue
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install buildozer==1.5.0 cython==0.29.36

# Clean previous builds
Write-Host "🧹 Cleaning previous builds..." -ForegroundColor Blue
try {
    buildozer android clean
} catch {
    Write-Host "No previous build to clean" -ForegroundColor Yellow
}

# Use the Flet-optimized buildozer spec
Write-Host "⚙️ Using Flet-optimized buildozer configuration..." -ForegroundColor Blue
Copy-Item "buildozer-flet.spec" "buildozer.spec" -Force

# Build the APK
Write-Host "🔨 Building Android APK..." -ForegroundColor Blue
Write-Host "⏱️ This will take 20-60 minutes for the first build..." -ForegroundColor Yellow
try {
    buildozer -v android debug
    Write-Host "✅ Build command completed" -ForegroundColor Green
} catch {
    Write-Host "❌ Build failed. Check the output above for errors." -ForegroundColor Red
    exit 1
}

# Check build results
Write-Host "📱 Checking build results..." -ForegroundColor Blue
if (Test-Path "bin") {
    Write-Host "✅ Build directory found:" -ForegroundColor Green
    Get-ChildItem -Path "bin" | Format-Table Name, Length, LastWriteTime
    
    # Find APK files
    $apkFiles = Get-ChildItem -Path "bin" -Filter "*.apk" -Recurse
    if ($apkFiles.Count -gt 0) {
        Write-Host "🎉 APK files built successfully:" -ForegroundColor Green
        foreach ($apk in $apkFiles) {
            Write-Host "  📱 $($apk.FullName)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "⚠️ No APK files found in bin directory" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ No bin directory found" -ForegroundColor Red
}

# Also check .buildozer directory for APK files
if (Test-Path ".buildozer") {
    $buildozerApks = Get-ChildItem -Path ".buildozer" -Filter "*.apk" -Recurse -ErrorAction SilentlyContinue
    if ($buildozerApks.Count -gt 0) {
        Write-Host "📱 Additional APK files found in .buildozer:" -ForegroundColor Cyan
        foreach ($apk in $buildozerApks) {
            Write-Host "  📱 $($apk.FullName)" -ForegroundColor Cyan
        }
    }
}

Write-Host "✅ Build process completed!" -ForegroundColor Green
Write-Host "📝 Check the output above for any errors or warnings" -ForegroundColor Blue
