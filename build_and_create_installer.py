#!/usr/bin/env python3
"""
Better Lyrics - Complete Build and Installer Creation Script
This script builds the EXE and creates a Windows installer package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(message):
    """Print a formatted step message."""
    print(f"\n{'='*60}")
    print(f"🚀 {message}")
    print(f"{'='*60}")

def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"Output: {result.stdout}")
        print_success(f"{description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main build and installer creation process."""
    project_dir = Path.cwd()
    dist_dir = project_dir / "dist"
    build_dir = project_dir / "build"
    installer_output_dir = project_dir / "installer_output"
    
    print_step("Better Lyrics v1.0.0 - Complete Build Process")
    print(f"📁 Working directory: {project_dir}")
    
    # Step 1: Clean previous builds
    print_step("Cleaning previous builds")
    
    if dist_dir.exists():
        print("🧹 Removing old dist/ directory...")
        shutil.rmtree(dist_dir)
        
    if build_dir.exists():
        print("🧹 Removing old build/ directory...")
        shutil.rmtree(build_dir)
        
    if installer_output_dir.exists():
        print("🧹 Removing old installer_output/ directory...")
        shutil.rmtree(installer_output_dir)
    
    print_success("Cleanup completed!")
    
    # Step 2: Check required files
    print_step("Checking required files")
    
    required_files = [
        "better_lyrics_flet.py",
        "better_lyrics.spec",
        "version_info.txt",
        "betterlyrics3.ico",
        "better_lyrics_header_final.png"
    ]
    
    missing_files = []
    for file in required_files:
        if not (project_dir / file).exists():
            missing_files.append(file)
        else:
            print(f"✅ Found: {file}")
    
    if missing_files:
        print_error(f"Missing required files: {missing_files}")
        return False
    
    print_success("All required files found!")
    
    # Step 3: Install/Update dependencies
    print_step("Installing dependencies")
    
    if not run_command("pip install --upgrade pyinstaller", "Installing PyInstaller"):
        return False
    
    if not run_command("pip install --upgrade flet pyclip", "Installing app dependencies"):
        return False
    
    # Step 4: Build the EXE using PyInstaller
    print_step("Building Better Lyrics EXE")
    
    if not run_command("pyinstaller better_lyrics.spec --clean", "Building EXE with PyInstaller"):
        return False
    
    # Check if EXE was created
    exe_path = dist_dir / "Better Lyrics.exe"
    if not exe_path.exists():
        print_error("EXE file was not created!")
        return False
    
    exe_size_mb = exe_path.stat().st_size / (1024 * 1024)
    print_success(f"EXE built successfully! Size: {exe_size_mb:.1f} MB")
    
    # Step 5: Create installer output directory
    print_step("Preparing installer directory")
    installer_output_dir.mkdir(exist_ok=True)
    print_success("Installer directory ready!")
    
    # Step 6: Check for Inno Setup
    print_step("Checking Inno Setup installation")
    
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe"
    ]
    
    inno_compiler = None
    for path in inno_paths:
        if Path(path).exists():
            inno_compiler = path
            break
    
    if not inno_compiler:
        print_error("Inno Setup compiler not found!")
        print("Please install Inno Setup from: https://jrsoftware.org/isdl.php")
        print("Or create the installer manually using the installer_script.iss file")
        print_success("EXE build completed successfully!")
        print(f"📦 EXE location: {exe_path}")
        return True  # Still return True since EXE was built successfully
    
    print_success(f"Found Inno Setup: {inno_compiler}")
    
    # Step 7: Create the installer
    print_step("Creating Windows installer")
    
    iss_file = project_dir / "installer_script.iss"
    if not iss_file.exists():
        print_error("Installer script not found: installer_script.iss")
        return False
    
    if not run_command(f'"{inno_compiler}" "{iss_file}"', "Creating installer with Inno Setup"):
        print_error("Installer creation failed!")
        print_success("EXE build completed successfully!")
        print(f"📦 EXE location: {exe_path}")
        return True  # Still return True since EXE was built
    
    # Step 8: Verify installer creation
    print_step("Verifying installer creation")
    
    installer_path = installer_output_dir / "Better_Lyrics_Setup.exe"
    if installer_path.exists():
        installer_size_mb = installer_path.stat().st_size / (1024 * 1024)
        print_success(f"Installer created successfully! Size: {installer_size_mb:.1f} MB")
        print_success(f"Installer location: {installer_path}")
    else:
        print_error("Installer file not found!")
        return False
    
    # Final summary
    print_step("Build Summary - Better Lyrics v1.0.0")
    print(f"✅ EXE File: {exe_path} ({exe_size_mb:.1f} MB)")
    print(f"✅ Installer: {installer_path} ({installer_size_mb:.1f} MB)")
    print("\n🎉 Build completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Test the EXE to ensure it works correctly")
    print("   2. Test the installer on a clean Windows system")
    print("   3. Share the installer with users")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🏆 Better Lyrics v1.0.0 build process completed successfully!")
            sys.exit(0)
        else:
            print("\n💥 Build process failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Build process cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
