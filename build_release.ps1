# Better Lyrics v1.0.0 - Build and Installer Creation Script
# PowerShell script to build the EXE and create Windows installer

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "🚀 Better Lyrics v1.0.0 - Complete Build Process" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

# Get the current directory
$ProjectDir = Get-Location
Write-Host "📁 Working directory: $ProjectDir" -ForegroundColor Yellow

# Function to print success messages
function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

# Function to print error messages  
function Write-Error-Message {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Function to print step headers
function Write-Step {
    param([string]$Message)
    Write-Host "`n=============================================" -ForegroundColor Cyan
    Write-Host "🚀 $Message" -ForegroundColor Green  
    Write-Host "=============================================" -ForegroundColor Cyan
}

try {
    # Step 1: Clean previous builds
    Write-Step "Cleaning previous builds"
    
    if (Test-Path "dist") {
        Write-Host "🧹 Removing old dist/ directory..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force "dist"
    }
    
    if (Test-Path "build") {
        Write-Host "🧹 Removing old build/ directory..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force "build"
    }
    
    if (Test-Path "installer_output") {
        Write-Host "🧹 Removing old installer_output/ directory..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force "installer_output"
    }
    
    Write-Success "Cleanup completed!"

    # Step 2: Check required files
    Write-Step "Checking required files"
    
    $RequiredFiles = @(
        "better_lyrics_flet.py",
        "better_lyrics.spec", 
        "version_info.txt",
        "betterlyrics3.ico",
        "better_lyrics_header_final.png"
    )
    
    $MissingFiles = @()
    foreach ($file in $RequiredFiles) {
        if (Test-Path $file) {
            Write-Success "Found: $file"
        } else {
            $MissingFiles += $file
        }
    }
    
    if ($MissingFiles.Count -gt 0) {
        Write-Error-Message "Missing required files: $($MissingFiles -join ', ')"
        exit 1
    }
    
    Write-Success "All required files found!"

    # Step 3: Install/Update dependencies
    Write-Step "Installing dependencies"
    
    Write-Host "🔧 Installing PyInstaller..." -ForegroundColor Yellow
    & pip install --upgrade pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Message "Failed to install PyInstaller"
        exit 1
    }
    
    Write-Host "🔧 Installing app dependencies..." -ForegroundColor Yellow
    & pip install --upgrade flet pyclip
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Message "Failed to install app dependencies"
        exit 1
    }
    
    Write-Success "Dependencies installed!"

    # Step 4: Build the EXE
    Write-Step "Building Better Lyrics EXE"
    
    Write-Host "🔧 Building EXE with PyInstaller..." -ForegroundColor Yellow
    & pyinstaller better_lyrics.spec --clean
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Message "EXE build failed!"
        exit 1
    }
    
    # Check if EXE was created
    $ExePath = "dist\Better Lyrics.exe"
    if (-not (Test-Path $ExePath)) {
        Write-Error-Message "EXE file was not created!"
        exit 1
    }
    
    $ExeSize = (Get-Item $ExePath).Length / 1MB
    Write-Success "EXE built successfully! Size: $([math]::Round($ExeSize, 1)) MB"

    # Step 5: Prepare installer directory
    Write-Step "Preparing installer directory"
    
    if (-not (Test-Path "installer_output")) {
        New-Item -ItemType Directory -Path "installer_output" | Out-Null
    }
    Write-Success "Installer directory ready!"

    # Step 6: Check for Inno Setup and create installer
    Write-Step "Creating Windows installer"
    
    $InnoSetupPaths = @(
        "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        "C:\Program Files\Inno Setup 6\ISCC.exe", 
        "C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        "C:\Program Files\Inno Setup 5\ISCC.exe"
    )
    
    $InnoCompiler = $null
    foreach ($path in $InnoSetupPaths) {
        if (Test-Path $path) {
            $InnoCompiler = $path
            break
        }
    }
    
    if (-not $InnoCompiler) {
        Write-Error-Message "Inno Setup compiler not found!"
        Write-Host "Please install Inno Setup from: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
        Write-Host "Or create the installer manually using the installer_script.iss file" -ForegroundColor Yellow
        Write-Success "EXE build completed successfully!"
        Write-Host "📦 EXE location: $ExePath" -ForegroundColor Cyan
        exit 0
    }
    
    Write-Success "Found Inno Setup: $InnoCompiler"
    
    # Create the installer
    if (-not (Test-Path "installer_script.iss")) {
        Write-Error-Message "Installer script not found: installer_script.iss"
        exit 1
    }
    
    Write-Host "🔧 Creating installer with Inno Setup..." -ForegroundColor Yellow
    & "$InnoCompiler" "installer_script.iss"
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Message "Installer creation failed!"
        Write-Success "EXE build completed successfully!"
        Write-Host "📦 EXE location: $ExePath" -ForegroundColor Cyan
        exit 0
    }

    # Step 7: Verify installer creation
    Write-Step "Verifying installer creation"
    
    $InstallerPath = "installer_output\Better_Lyrics_Setup.exe"
    if (Test-Path $InstallerPath) {
        $InstallerSize = (Get-Item $InstallerPath).Length / 1MB
        Write-Success "Installer created successfully! Size: $([math]::Round($InstallerSize, 1)) MB"
        Write-Success "Installer location: $InstallerPath"
    } else {
        Write-Error-Message "Installer file not found!"
        exit 1
    }

    # Final summary
    Write-Step "Build Summary - Better Lyrics v1.0.0"
    Write-Host "✅ EXE File: $ExePath ($([math]::Round($ExeSize, 1)) MB)" -ForegroundColor Green
    Write-Host "✅ Installer: $InstallerPath ($([math]::Round($InstallerSize, 1)) MB)" -ForegroundColor Green
    Write-Host "`n🎉 Build completed successfully!" -ForegroundColor Green
    Write-Host "`n📋 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Test the EXE to ensure it works correctly"
    Write-Host "   2. Test the installer on a clean Windows system" 
    Write-Host "   3. Share the installer with users"
    
    Write-Host "`n🏆 Better Lyrics v1.0.0 build process completed successfully!" -ForegroundColor Green

} catch {
    Write-Host "`n💥 Build process failed with error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
