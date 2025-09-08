#!/usr/bin/env python3
"""
Test application to fix the dialog saving function problem.
This isolated test will help us identify and fix the Flet dialog issues.
"""

import flet as ft
import json
import os
from datetime import datetime

class DialogTestApp:
    def __init__(self):
        self.test_lyrics = """I'm like the water when your ship rolled in that night
Rough on the surface, but you cut through like a knife
And if it was an open-shut case
I never would have known from the look on your face
Lost in your current like a priceless wine

The more that you say, the less I know
Wherever you stray, I follow
I'm begging for you to take my hand
Wreck my plans, that's my man"""
        
        self.saved_songs = []
        self.container_dir = "saved_songs"
        self._ensure_container_exists()
    
    def _ensure_container_exists(self):
        """Create the container directory if it doesn't exist."""
        if not os.path.exists(self.container_dir):
            os.makedirs(self.container_dir)
            print(f"✅ Created container directory: {self.container_dir}")
    
    def _save_song_to_file(self, title, artist, lyrics):
        """Save song to JSON file."""
        song = {
            "id": f"song_{len(self.saved_songs) + 1}",
            "title": title,
            "artist": artist,
            "lyrics": lyrics,
            "saved_at": datetime.now().isoformat(),
            "is_favorite": False
        }
        
        self.saved_songs.append(song)
        
        # Save to file
        songs_file = os.path.join(self.container_dir, "test_songs.json")
        try:
            with open(songs_file, 'w', encoding='utf-8') as f:
                json.dump(self.saved_songs, f, indent=2, ensure_ascii=False)
            print(f"✅ Song saved to {songs_file}")
            return song
        except Exception as e:
            print(f"❌ Error saving song: {e}")
            return None
    
    def _show_simple_dialog(self, page):
        """Test 1: Simple dialog without complex content."""
        def close_dialog(e):
            dialog.open = False
            page.update()
            print("✅ Simple dialog closed")
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("🧪 Simple Test Dialog"),
            content=ft.Text("This is a simple test dialog. Can you see this?"),
            actions=[
                ft.TextButton("Close", on_click=close_dialog)
            ]
        )
        
        # For Flet 0.28.3, use page.overlay instead of page.dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        print("🧪 Simple dialog should be visible now")
    
    def _show_input_dialog(self, page):
        """Test 2: Dialog with input fields."""
        title_field = ft.TextField(
            label="Song Title", 
            value="Test Song",
            width=300
        )
        artist_field = ft.TextField(
            label="Artist", 
            value="Test Artist",
            width=300
        )
        
        def save_song(e):
            if title_field.value and artist_field.value:
                song = self._save_song_to_file(
                    title_field.value, 
                    artist_field.value, 
                    self.test_lyrics
                )
                if song:
                    self._show_message(page, f"✅ Saved: {song['title']} - {song['artist']}")
                else:
                    self._show_message(page, "❌ Failed to save song")
            else:
                self._show_message(page, "❌ Please fill in both fields")
            
            dialog.open = False
            page.update()
        
        def cancel_save(e):
            dialog.open = False
            page.update()
            print("❌ Save dialog cancelled")
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("💾 Save Song Test"),
            content=ft.Column([
                ft.Text("Test saving functionality:", size=14),
                title_field,
                artist_field
            ], spacing=10, height=150),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_save),
                ft.ElevatedButton("💾 Save", on_click=save_song)
            ]
        )
        
        # For Flet 0.28.3, use page.overlay instead of page.dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        print("💾 Save dialog should be visible now")
    
    def _show_message(self, page, message):
        """Show a temporary message."""
        snack = ft.SnackBar(
            content=ft.Text(message),
            duration=3000
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()
        print(f"📢 Message: {message}")
    
    def _show_saved_songs(self, page):
        """Display all saved songs."""
        if not self.saved_songs:
            self._show_message(page, "No songs saved yet!")
            return
        
        songs_list = ft.Column([
            ft.Text("🎵 Saved Songs:", size=18, weight=ft.FontWeight.BOLD)
        ])
        
        for song in self.saved_songs:
            songs_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Title: {song['title']}", weight=ft.FontWeight.BOLD),
                        ft.Text(f"Artist: {song['artist']}"),
                        ft.Text(f"Saved: {song['saved_at'][:19]}"),
                    ]),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=10,
                    margin=5,
                    border_radius=5
                )
            )
        
        def close_songs_dialog(e):
            songs_dialog.open = False
            page.update()
        
        songs_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("📚 Song Library"),
            content=ft.Container(
                content=songs_list,
                width=400,
                height=300
            ),
            actions=[
                ft.TextButton("Close", on_click=close_songs_dialog)
            ]
        )
        
        # For Flet 0.28.3, use page.overlay instead of page.dialog
        page.overlay.append(songs_dialog)
        songs_dialog.open = True
        page.update()
    
    def build_ui(self, page: ft.Page):
        """Build the test application UI."""
        page.title = "Dialog Fix Test App"
        page.window.width = 800
        page.window.height = 600
        page.theme_mode = ft.ThemeMode.LIGHT
        
        # Main content
        main_content = ft.Column([
            ft.Container(
                content=ft.Text(
                    "🧪 Dialog Test Application",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                padding=20
            ),
            
            ft.Container(
                content=ft.Text(
                    "Test the dialog functionality to fix the saving issues:",
                    size=14,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                padding=10
            ),
            
            # Test lyrics display
            ft.Container(
                content=ft.Column([
                    ft.Text("🎵 Test Lyrics:", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(
                            self.test_lyrics,
                            size=12,
                            color=ft.Colors.GREY_700
                        ),
                        bgcolor=ft.Colors.GREY_100,
                        padding=10,
                        border_radius=5
                    )
                ]),
                padding=20
            ),
            
            # Test buttons
            ft.Row([
                ft.ElevatedButton(
                    "🧪 Test Simple Dialog",
                    on_click=lambda e: self._show_simple_dialog(page),
                    icon=ft.Icons.CHAT_BUBBLE
                ),
                ft.ElevatedButton(
                    "💾 Test Save Dialog",
                    on_click=lambda e: self._show_input_dialog(page),
                    icon=ft.Icons.SAVE,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_100)
                ),
                ft.ElevatedButton(
                    "📚 View Saved Songs",
                    on_click=lambda e: self._show_saved_songs(page),
                    icon=ft.Icons.LIBRARY_MUSIC,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_100)
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            
            # Status info
            ft.Container(
                content=ft.Column([
                    ft.Text(f"📁 Container directory: {self.container_dir}", size=12),
                    ft.Text(f"🎵 Songs saved: {len(self.saved_songs)}", size=12),
                    ft.Text("💡 Check the terminal for debug output", size=12, color=ft.Colors.BLUE_600)
                ]),
                padding=20,
                alignment=ft.alignment.center
            )
        ], 
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10)
        
        page.add(main_content)
        page.update()
        
        print("🚀 Dialog Test App loaded!")
        print("📋 Instructions:")
        print("   1. Click 'Test Simple Dialog' to see if basic dialogs work")
        print("   2. Click 'Test Save Dialog' to test the save functionality")
        print("   3. Click 'View Saved Songs' to see saved songs")
        print("   4. Watch the terminal for debug messages")

def main(page: ft.Page):
    """Main application entry point."""
    app = DialogTestApp()
    app.build_ui(page)

if __name__ == "__main__":
    print("🧪 Starting Dialog Fix Test Application...")
    ft.app(target=main)
