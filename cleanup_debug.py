#!/usr/bin/env python3
"""
Remove all debug print statements from the app
"""

def remove_debug_prints():
    """Remove all debug print statements"""
    file_path = "better_lyrics_flet.py"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove lines that start with debug prints
    new_lines = []
    for line in lines:
        if not line.strip().startswith('print("🐛 DEBUG:'):
            new_lines.append(line)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ Removed all debug print statements")

if __name__ == "__main__":
    remove_debug_prints()
