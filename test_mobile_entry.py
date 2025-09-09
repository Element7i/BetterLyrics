#!/usr/bin/env python3
"""
Test script to verify the main entry point works before building APK
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🧪 Testing Better Lyrics mobile entry point...")
    
    # Test importing the main module
    print("📦 Importing main module...")
    import main
    print("✅ main.py imported successfully")
    
    # Test importing the mobile module
    print("📱 Importing better_lyrics_mobile...")
    import better_lyrics_mobile
    print("✅ better_lyrics_mobile.py imported successfully")
    
    # Test Flet import
    print("🌐 Testing Flet import...")
    import flet as ft
    print("✅ Flet imported successfully")
    
    # Test other dependencies
    print("📋 Testing other dependencies...")
    import pyperclip
    print("✅ pyperclip imported successfully")
    
    import json
    import os
    import re  
    import threading
    import time
    import traceback
    from datetime import datetime
    import uuid
    print("✅ All standard library imports successful")
    
    print("\n🎉 All tests passed! The app should build successfully.")
    print("📱 Main entry point is ready for APK building.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure to install requirements: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
