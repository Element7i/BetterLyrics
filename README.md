# Better Lyrics

Better Lyrics v1.0.0 is a cross-platform lyrics management app built with Python and Flet. It offers dark/light mode, auto-scroll for karaoke, smart formatting for pasted lyrics, and live customization of font and alignment—all in a simple, portable package.

## Features

- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **Auto-Scroll**: Karaoke-style scrolling with adjustable speed
- **Smart Formatting**: Automatic formatting and cleanup of pasted lyrics
- **Live Customization**: Real-time font size and alignment adjustment
- **Bold Text Support**: Enhanced readability with bold text option
- **Cross-Platform**: Runs on desktop and mobile (Android via APK builds)

## Installation

### Desktop

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python main.py`

### Android

The Android APK is automatically built via GitHub Actions on every push to the main branch. Download the latest APK from the [Actions artifacts](../../actions).

## Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Android Development

```bash
# Install buildozer
pip install buildozer

# Build for Android (requires Android SDK)
buildozer android debug
```

## Automated Builds

This repository includes a complete GitHub Actions workflow that automatically:

- Sets up Python and Android SDK
- Installs all dependencies
- Builds debug APK using buildozer
- Uploads APK as build artifact

The workflow triggers on every push to the main branch, ensuring you always have the latest build available for testing.

## License

This project is open source and available under the MIT License.
