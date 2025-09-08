#!/usr/bin/env python3
"""
Build script for Better Lyrics desktop application.
Creates a distributable Windows executable.
"""
import os
import subprocess
import sys

def build_app():
    """Build the Better Lyrics app using PyInstaller."""
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',  # Create a single executable file
        '--windowed',  # No console window
        '--name=Better Lyrics',
        '--icon=icon.ico',  # Will use default if no icon file exists
        '--add-data=better_lyrics_flet.py;.',
        '--distpath=./dist',
        '--workpath=./build',
        '--specpath=./build',
        'better_lyrics_flet.py'
    ]
    
    # Remove icon argument if no icon file exists
    if not os.path.exists(os.path.join(current_dir, 'icon.ico')):
        cmd = [arg for arg in cmd if not arg.startswith('--icon')]
    
    print("Building Better Lyrics executable...")
    print("Command:", ' '.join(cmd))
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("\n✅ Build completed successfully!")
        print(f"📁 Executable created in: {os.path.join(current_dir, 'dist')}")
        print("📦 File: Better Lyrics.exe")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def clean_build():
    """Clean build artifacts."""
    import shutil
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"🧹 Cleaned {dir_name}")
            except Exception as e:
                print(f"⚠️ Could not clean {dir_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_build()
    else:
        build_app()
