# Better Lyrics Installer

This document explains how to create and distribute a Windows installer for the Better Lyrics application.

## What This Creates

The installer will:
- ✅ Install the Better Lyrics executable
- ✅ Install all application assets (icons, images)
- ✅ Create application data directory structure
- ✅ Add Start Menu shortcuts
- ✅ Optionally create Desktop shortcuts
- ✅ Register for clean uninstallation via Windows "Add or Remove Programs"
- ✅ Set up file associations (optional)

## Prerequisites

Before creating the installer, you need:

1. **Python** - To build the executable
2. **Inno Setup** - To create the installer
   - Download from: https://jrsoftware.org/isdl.php
   - Install with default settings

## How to Create the Installer

### Option 1: PowerShell Script (Recommended)
```powershell
.\create_installer.ps1
```

### Option 2: Batch Script
```cmd
create_installer.bat
```

### Option 3: Manual Steps
1. Build the executable:
   ```cmd
   python build_better_lyrics.py
   ```

2. Create the installer:
   ```cmd
   iscc installer_script.iss
   ```

## Installer Features

### Installation Options
- **Installation Directory**: Users can choose where to install (default: Program Files)
- **Desktop Shortcut**: Optional desktop icon
- **Start Menu**: Automatically added to Start Menu
- **File Associations**: Associates .bl files with Better Lyrics

### What Gets Installed
```
Program Files/Better Lyrics/
├── Better Lyrics.exe          # Main executable
├── assets/
│   ├── betterlyrics3.ico     # Application icon
│   ├── betterlyrics3.png     # App images
│   ├── betterlyricslogo.png
│   └── betterlogo2.png
├── docs/
│   ├── README.md             # Documentation
│   └── CHANGELOG.md
└── saved_songs/              # User data directory
    ├── playlists.json
    ├── songs_library.json
    └── README.md
```

### Registry Entries
The installer creates registry entries for:
- File associations (.bl files)
- Uninstall information
- Application settings

## Distribution

After running the installer creation script, you'll get:
- **File**: `installer_output/Better_Lyrics_Setup.exe`
- **Size**: Typically 20-50MB (includes all dependencies)
- **Requirements**: Windows 7 or later

### Sharing Your App
Users can:
1. Download `Better_Lyrics_Setup.exe`
2. Double-click to run the installer
3. Follow the installation wizard
4. Launch Better Lyrics from Start Menu or Desktop

### Uninstallation
Users can uninstall via:
1. **Settings** → Apps → Better Lyrics → Uninstall
2. **Control Panel** → Add or Remove Programs → Better Lyrics
3. **Start Menu** → Right-click Better Lyrics → Uninstall

## Customizing the Installer

Edit `installer_script.iss` to customize:

### Basic Information
```inno
#define MyAppName "Better Lyrics"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Name"
#define MyAppURL "https://your-website.com"
```

### Installation Options
```inno
DefaultDirName={autopf}\{#MyAppName}  ; Installation directory
PrivilegesRequired=lowest             ; User vs Admin install
```

### Files to Include
```inno
[Files]
Source: "your-file.ext"; DestDir: "{app}"; Flags: ignoreversion
```

## Advanced Features

### Code Signing (Optional)
To sign your installer for Windows SmartScreen:
1. Get a code signing certificate
2. Add to installer script:
   ```inno
   SignTool=signtool
   SignedUninstaller=yes
   ```

### Multiple Languages
Add language support:
```inno
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
```

### Custom Pages
Add custom installer pages for configuration, license agreements, etc.

## Troubleshooting

### Common Issues

**"iscc.exe not found"**
- Install Inno Setup from the official website
- Make sure it's in your PATH or use default installation location

**"Better Lyrics.exe not found"**
- Run `python build_better_lyrics.py` first
- Make sure PyInstaller completed successfully

**Installer too large**
- Review files being included in `installer_script.iss`
- Remove unnecessary assets
- Use compression options

**Permission errors**
- Run as Administrator if needed
- Check file permissions in source directory

### Getting Help

If you encounter issues:
1. Check the error messages carefully
2. Verify all prerequisites are installed
3. Make sure source files exist and are accessible
4. Review the Inno Setup documentation: https://jrsoftware.org/ishelp/

## Version History

- **1.0.0**: Initial installer script with basic functionality
