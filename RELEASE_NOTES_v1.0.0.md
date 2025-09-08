# Better Lyrics v1.0.0 - Official Release

## 🎉 Release Summary

**Version:** 1.0.0  
**Release Date:** September 8, 2025  
**Build Status:** ✅ Successfully Built  

## 📦 Release Files

### Standalone EXE
- **File:** `dist\Better Lyrics.exe`
- **Size:** 68.9 MB
- **Description:** Standalone executable that runs without installation
- **Requirements:** Windows 10/11 (64-bit)

### Windows Installer
- **File:** `installer_output\Better_Lyrics_Setup.exe`
- **Size:** 72.3 MB  
- **Description:** Professional Windows installer with Start Menu integration
- **Features:**
  - Automatic desktop shortcut creation (optional)
  - Start Menu integration
  - File association for .bl files
  - Clean uninstall support
  - Bundled assets and documentation

## 🚀 Key Features

### Core Functionality
- ✅ Advanced lyrics formatting and display
- ✅ Auto-scroll with customizable speed
- ✅ Song length mode for optimal scrolling
- ✅ Multiple text alignment options (left, center, right)
- ✅ Adjustable font size and line spacing
- ✅ Dark/Light theme support

### Smart Features  
- ✅ Intelligent title/artist parsing from pasted text
- ✅ Portal paste with auto-detection
- ✅ Drag & drop support for lyrics
- ✅ Buffer lines for better scrolling experience

### Library Management
- ✅ Complete song library with favorites
- ✅ Custom playlist creation and management
- ✅ Song search and organization
- ✅ Artist-grouped views
- ✅ Play count tracking
- ✅ Persistent data storage

### User Interface
- ✅ Centered song title to avoid logo clash
- ✅ Modern Flet-based UI
- ✅ Responsive design with visual feedback
- ✅ Professional header with branding
- ✅ Comprehensive control panels

## 🛠️ Technical Details

### Build Configuration
- **PyInstaller:** 6.15.0
- **Python:** 3.12.2
- **GUI Framework:** Flet 0.28.3
- **Dependencies:** pyclip for clipboard operations
- **Icon:** Custom betterlyrics3.ico
- **Version Info:** Embedded Windows version information

### Installer Features
- **Created with:** Inno Setup 6.5.0
- **Installation Locations:** Program Files
- **Registry Integration:** File associations and context menus
- **Bundled Assets:** All required images and icons
- **Documentation:** README and CHANGELOG included

## 📋 Installation Instructions

### Option 1: Use the Installer (Recommended)
1. Download `Better_Lyrics_Setup.exe` (72.3 MB)
2. Right-click and select "Run as administrator" (if needed)
3. Follow the installation wizard
4. Launch from Start Menu or desktop shortcut

### Option 2: Standalone EXE
1. Download `Better Lyrics.exe` (68.9 MB)  
2. Create a folder for the app (e.g., `C:\Better Lyrics\`)
3. Copy the EXE to that folder
4. Double-click to run
5. **Note:** Song library will be saved relative to EXE location

## 🔧 System Requirements

### Minimum Requirements
- **OS:** Windows 10 (64-bit) or Windows 11
- **RAM:** 4 GB RAM
- **Storage:** 100 MB free space
- **Display:** 1024x768 resolution minimum

### Recommended Requirements
- **OS:** Windows 11 (latest updates)
- **RAM:** 8 GB RAM or more
- **Storage:** 500 MB free space
- **Display:** 1920x1080 or higher resolution

## 📚 Usage Tips

### Getting Started
1. **First Launch:** The app opens in edit mode ready for lyrics input
2. **Add Lyrics:** Paste lyrics using Ctrl+V or the Portal Paste feature
3. **Transform:** Click "Transform" to enter enhanced viewing mode
4. **Save Songs:** Use the save button to add songs to your library

### Power Features
- **Smart Parsing:** Use format "Song Title - Artist" for auto-detection
- **Song Length Mode:** Set your song duration for perfect auto-scroll timing
- **Playlists:** Organize your favorite songs into custom collections
- **Drag & Drop:** Drag text from browsers directly into the app

## 🐛 Known Issues

### Minor Issues
- First launch may take a few seconds to initialize
- Very large lyrics (1000+ lines) may cause slower scrolling
- Windows Defender may show initial security warning (normal for new apps)

### Workarounds
- **Security Warning:** Click "More info" → "Run anyway"
- **Slow Performance:** Close other resource-intensive applications
- **Font Issues:** Use Windows built-in fonts for best compatibility

## 🎯 Future Updates

### Planned Features (v1.1.0)
- Export songs to various formats (PDF, TXT)
- Cloud sync for song library
- Multiple language support
- Advanced search and filtering
- Import from popular lyrics websites

### Enhancement Requests
- Karaoke mode with word highlighting
- Custom color themes
- Print functionality
- Lyrics editing tools
- Sharing capabilities

## 📞 Support & Feedback

### Getting Help
- **Documentation:** Check the included README.md
- **Issues:** Report bugs through the application's feedback system
- **Community:** Share your experience and tips with other users

### Feedback
We value your feedback! Let us know about:
- Feature requests
- Bug reports  
- User experience improvements
- Performance issues

## 🏆 Acknowledgments

### Development
- **Framework:** Built with Python and Flet
- **Packaging:** PyInstaller for executable creation
- **Installer:** Inno Setup for Windows installer
- **Icons:** Custom designed application icons

### Testing
- Tested on Windows 10 and Windows 11
- Various screen resolutions and DPI settings
- Multiple lyrics formats and sizes
- Extensive playlist and library functionality testing

---

**🎵 Better Lyrics v1.0.0 - Making your lyrics look and feel better! 🎵**

*Built with ❤️ for music lovers who want the best lyrics viewing experience*
