# Better Lyrics Installer Creation Script
# PowerShell version with better error handling

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Building Better Lyrics Installer" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Check if executable exists
if (-not (Test-Path "dist\Better Lyrics.exe")) {
    Write-Host "Building application executable first..." -ForegroundColor Yellow
    
    # Check if Python is available
    if (-not (Test-CommandExists "python")) {
        Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Build the executable
    $buildResult = Start-Process -FilePath "python" -ArgumentList "build_better_lyrics.py" -Wait -PassThru -NoNewWindow
    
    if ($buildResult.ExitCode -ne 0) {
        Write-Host "ERROR: Failed to build executable" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "Executable found in dist folder." -ForegroundColor Green
}

# Create installer output directory
if (-not (Test-Path "installer_output")) {
    New-Item -ItemType Directory -Path "installer_output" | Out-Null
}

# Check if Inno Setup is installed
$innoSetupPaths = @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\iscc.exe",
    "${env:ProgramFiles}\Inno Setup 6\iscc.exe",
    "iscc.exe"  # If it's in PATH
)

$isccPath = $null
foreach ($path in $innoSetupPaths) {
    if (Test-Path $path -ErrorAction SilentlyContinue) {
        $isccPath = $path
        break
    } elseif ($path -eq "iscc.exe" -and (Test-CommandExists "iscc")) {
        $isccPath = "iscc"
        break
    }
}

if (-not $isccPath) {
    Write-Host ""
    Write-Host "ERROR: Inno Setup compiler (iscc.exe) not found!" -ForegroundColor Red
    Write-Host "Please install Inno Setup from: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Creating installer..." -ForegroundColor Yellow

# Create the installer
$installerResult = Start-Process -FilePath $isccPath -ArgumentList "installer_script.iss" -Wait -PassThru -NoNewWindow

if ($installerResult.ExitCode -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to create installer" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
} else {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "SUCCESS! Installer created successfully!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installer location: installer_output\Better_Lyrics_Setup.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now distribute this installer file." -ForegroundColor White
    Write-Host "Users will be able to:" -ForegroundColor White
    Write-Host "- Install Better Lyrics with all assets" -ForegroundColor Gray
    Write-Host "- Create desktop shortcuts" -ForegroundColor Gray
    Write-Host "- Add to Start Menu" -ForegroundColor Gray
    Write-Host "- Uninstall cleanly through Add/Remove Programs" -ForegroundColor Gray
    Write-Host ""
    
    # Ask if user wants to open the installer folder
    $openFolder = Read-Host "Would you like to open the installer folder? (y/n)"
    if ($openFolder.ToLower() -eq "y" -or $openFolder.ToLower() -eq "yes") {
        Start-Process -FilePath "explorer.exe" -ArgumentList "installer_output"
    }
}

Read-Host "Press Enter to exit"
