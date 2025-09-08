#!/usr/bin/env python3
"""
Script to fix incorrect color constants in better_lyrics_mobile.py
"""

# Read the file
with open('better_lyrics_mobile.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix color constants that don't exist
replacements = {
    'ft.Colors.SURFACE_VARIANT': 'ft.Colors.SURFACE',
    'ft.Colors.GREY_600': 'ft.Colors.GREY',
    'ft.Colors.WHITE': 'ft.Colors.WHITE',
    'ft.Colors.GREEN': 'ft.Colors.GREEN',
    'ft.Colors.RED': 'ft.Colors.RED',
    'ft.Colors.BLUE': 'ft.Colors.BLUE',
    'ft.Colors.AMBER': 'ft.Colors.AMBER',
    'ft.Colors.GREY': 'ft.Colors.GREY'
}

fixed_content = content
for old_color, new_color in replacements.items():
    fixed_content = fixed_content.replace(old_color, new_color)

# Write the fixed content back
with open('better_lyrics_mobile.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Fixed all color constants!")
print("📱 Mobile app should work now!")
