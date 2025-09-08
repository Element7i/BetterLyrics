#!/usr/bin/env python3
"""
Quick script to remove the save and copy buttons from edit mode
"""

def fix_edit_mode_buttons():
    """Remove save and copy buttons from edit mode"""
    file_path = "better_lyrics_flet.py"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the button row
    old_buttons = '''ft.Row(
                    [
                        ft.ElevatedButton("📋 Paste from Clipboard", icon=ft.Icons.CONTENT_PASTE, on_click=self.paste_lyrics),
                        ft.ElevatedButton("✨ Transform Lyrics", icon=ft.Icons.AUTO_FIX_HIGH, on_click=self.transform_lyrics, autofocus=True),'''
    
    # Look for lines that have Save Song or Copy Lyrics buttons in edit mode
    lines = content.split('\n')
    new_lines = []
    skip_next = False
    
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
            
        if 'Save Song", icon=ft.Icons.SAVE' in line and '_save_from_edit_mode' in line:
            # Skip this save button line
            continue
        elif 'Copy Lyrics", icon=ft.Icons.COPY' in line and 'Transform Lyrics' in lines[i-1]:
            # Skip this copy button line
            continue
        else:
            new_lines.append(line)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ Removed save and copy buttons from edit mode")

if __name__ == "__main__":
    fix_edit_mode_buttons()
