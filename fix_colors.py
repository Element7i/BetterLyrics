#!/usr/bin/env python3
"""
Quick script to fix ft.colors and ft.icons references in better_lyrics_mobile.py
"""

import re

# Read the file
with open('better_lyrics_mobile.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all instances of ft.colors. with ft.Colors.
fixed_content = content.replace('ft.colors.', 'ft.Colors.')

# Replace all instances of ft.icons. with ft.Icons.
fixed_content = fixed_content.replace('ft.icons.', 'ft.Icons.')

# Write the fixed content back
with open('better_lyrics_mobile.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Fixed all ft.colors. references to ft.Colors.")
print("✅ Fixed all ft.icons. references to ft.Icons.")
print("📱 Ready to test the mobile app!")
