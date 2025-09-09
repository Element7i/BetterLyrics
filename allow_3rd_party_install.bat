@echo off
:: Must run as administrator!

echo Setting PowerShell execution policy to RemoteSigned...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

echo Enabling app sideloading for MSIX/APPX packages...
powershell -Command "Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock' -Name 'AllowAllTrustedApps' -Value 1"
powershell -Command "Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock' -Name 'AllowDevelopmentWithoutDevLicense' -Value 1"

echo Disabling Windows Defender SmartScreen...
powershell -Command "Set-MpPreference -EnableSmartScreen $false"

echo Disabling AppLocker service (if present)...
powershell -Command "Stop-Service AppIDSvc"
powershell -Command "Set-Service AppIDSvc -StartupType Disabled"

echo Disabling User Account Control (UAC)...
powershell -Command "Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' -Name 'EnableLUA' -Value 0"

echo.
echo -------------------------------------------
echo Please restart your computer for changes to take effect!
echo -------------------------------------------
pause