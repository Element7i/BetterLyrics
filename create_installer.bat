@echo off
echo ==========================================
echo Building Better Lyrics Installer
echo ==========================================
echo.

:: Check if dist directory exists and has the executable
if not exist "dist\Better Lyrics.exe" (
    echo Building application executable first...
    python build_better_lyrics.py
    if errorlevel 1 (
        echo ERROR: Failed to build executable
        pause
        exit /b 1
    )
) else (
    echo Executable found in dist folder.
)

:: Create installer output directory
if not exist "installer_output" mkdir installer_output

:: Check if Inno Setup is installed
where iscc >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Inno Setup compiler (iscc.exe) not found!
    echo Please install Inno Setup from: https://jrsoftware.org/isdl.php
    echo Make sure to add it to your PATH or install in default location.
    echo.
    pause
    exit /b 1
)

echo.
echo Creating installer...
iscc installer_script.iss

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create installer
    pause
    exit /b 1
) else (
    echo.
    echo ==========================================
    echo SUCCESS! Installer created successfully!
    echo ==========================================
    echo.
    echo Installer location: installer_output\Better_Lyrics_Setup.exe
    echo.
    echo You can now distribute this installer file.
    echo Users will be able to:
    echo - Install Better Lyrics with all assets
    echo - Create desktop shortcuts
    echo - Add to Start Menu
    echo - Uninstall cleanly through Add/Remove Programs
    echo.
)

pause
