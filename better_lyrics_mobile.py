import flet as ft
import pyperclip as pyclip # type: ignore
import json
import os
import re
import threading
import time
import traceback
from datetime import datetime
import uuid


class BetterLyricsMobile:
    """
    A mobile-optimized Flet application for Better Lyrics.
    Designed for Android/iOS with touch-friendly controls and responsive layout.
    """
    def __init__(self):
        # --- State Management ---
        self.is_dark_mode = True
        self.is_preview_mode = False
        self.original_lyrics = ""
        self.formatted_lyrics = ""
        self.current_song = None

        # --- Song Library Management ---
        self.songs_directory = "saved_songs"
        if not os.path.exists(self.songs_directory):
            os.makedirs(self.songs_directory)
        
        self.songs_file = os.path.join(self.songs_directory, "songs_library.json")
        self.playlists_file = os.path.join(self.songs_directory, "playlists.json")
        self.song_library = self._load_song_library()
        self.playlists = self._load_playlists()
        self.current_playlist = None
        self.show_library = False

        # --- Auto-scroll Properties (Mobile optimized) ---
        self.is_playing = False
        self.scroll_speed = 1.0
        self.buffer_lines = 2  # Reduced for mobile
        self.song_length_seconds = 180
        self.use_song_length_mode = False

        # --- Mobile-specific Properties ---
        self.is_portrait = True
        self.font_size_mobile = 16  # Larger for mobile readability
        self.button_height = 50     # Touch-friendly button size
        self.button_width = 120     # Touch-friendly button width

        # --- UI Controls (will be set in build_ui) ---
        self.page = None
        self.main_container = None
        self.lyrics_display = None
        self.lyrics_input = None

    def _load_song_library(self):
        """Load the song library from JSON file"""
        try:
            if os.path.exists(self.songs_file):
                with open(self.songs_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"❌ Error loading song library: {e}")
            return {}

    def _load_playlists(self):
        """Load playlists from JSON file"""
        try:
            if os.path.exists(self.playlists_file):
                with open(self.playlists_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"❌ Error loading playlists: {e}")
            return {}

    def _save_song_library(self):
        """Save the song library to JSON file"""
        try:
            with open(self.songs_file, 'w', encoding='utf-8') as f:
                json.dump(self.song_library, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving song library: {e}")
            return False

    def _save_playlists(self):
        """Save playlists to JSON file"""
        try:
            with open(self.playlists_file, 'w', encoding='utf-8') as f:
                json.dump(self.playlists, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving playlists: {e}")
            return False

    def format_lyrics(self, lyrics_text):
        """Format lyrics for mobile display with better spacing"""
        if not lyrics_text.strip():
            return "No lyrics to display"

        # Split by lines and clean
        lines = [line.strip() for line in lyrics_text.split('\n')]
        formatted_lines = []
        
        for line in lines:
            if line:
                # Add some spacing for chorus sections (lines in brackets or repeated)
                if line.startswith('[') and line.endswith(']'):
                    formatted_lines.extend(['', f"  {line}", ''])
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append('')

        return '\n'.join(formatted_lines)

    def paste_from_clipboard(self, e):
        """Paste text from clipboard (mobile-friendly)"""
        try:
            clipboard_text = pyclip.paste()
            if clipboard_text:
                self.original_lyrics = clipboard_text
                self.lyrics_input.value = clipboard_text
                self.page.update()
                
                # Show a brief success message
                self.show_snackbar("📋 Lyrics pasted!", ft.Colors.GREEN)
            else:
                self.show_snackbar("📋 Clipboard is empty", ft.Colors.AMBER)
        except Exception as ex:
            self.show_snackbar(f"❌ Paste failed: {str(ex)}", ft.Colors.RED)

    def show_snackbar(self, message, color=ft.Colors.BLUE):
        """Show a mobile-friendly snackbar message"""
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
            duration=2000  # 2 seconds
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()

    def transform_lyrics(self, e):
        """Transform and display formatted lyrics"""
        lyrics_text = self.lyrics_input.value.strip()
        
        if not lyrics_text:
            self.show_snackbar("⚠️ Please paste some lyrics first!", ft.Colors.AMBER)
            return
        
        self.original_lyrics = lyrics_text
        self.formatted_lyrics = self.format_lyrics(lyrics_text)
        
        # Update the display
        self.lyrics_display.value = self.formatted_lyrics
        self.is_preview_mode = True
        
        # Switch to preview view
        self.switch_to_preview_mode()
        self.page.update()
        
        self.show_snackbar("✨ Lyrics transformed!", ft.Colors.GREEN)

    def switch_to_preview_mode(self):
        """Switch to preview mode for mobile"""
        self.is_preview_mode = True
        self.build_ui(self.page)

    def switch_to_edit_mode(self):
        """Switch back to edit mode"""
        self.is_preview_mode = False
        self.build_ui(self.page)

    def toggle_theme(self, e):
        """Toggle between dark and light theme"""
        self.is_dark_mode = not self.is_dark_mode
        self.page.theme_mode = ft.ThemeMode.DARK if self.is_dark_mode else ft.ThemeMode.LIGHT
        self.page.update()
        
        theme_text = "🌙 Dark" if self.is_dark_mode else "☀️ Light"
        self.show_snackbar(f"Theme: {theme_text}", ft.Colors.BLUE)

    def save_current_song(self, e):
        """Save current lyrics as a song (mobile optimized)"""
        if not self.formatted_lyrics or self.formatted_lyrics == "No lyrics to display":
            self.show_snackbar("⚠️ No lyrics to save!", ft.Colors.AMBER)
            return

        # Create a simple dialog for mobile
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        def save_song(e):
            title = title_field.value.strip()
            artist = artist_field.value.strip() if artist_field.value else "Unknown Artist"
            
            if not title:
                self.show_snackbar("⚠️ Please enter a song title!", ft.Colors.AMBER)
                return
            
            # Create song entry
            song_id = str(uuid.uuid4())
            song_data = {
                'id': song_id,
                'title': title,
                'artist': artist,
                'lyrics': self.formatted_lyrics,
                'original_lyrics': self.original_lyrics,
                'date_added': datetime.now().isoformat(),
                'play_count': 0,
                'is_favorite': False
            }
            
            # Save to library
            self.song_library[song_id] = song_data
            if self._save_song_library():
                self.show_snackbar(f"💾 '{title}' saved!", ft.Colors.GREEN)
                close_dialog(e)
            else:
                self.show_snackbar("❌ Failed to save song", ft.Colors.RED)

        # Mobile-friendly dialog
        title_field = ft.TextField(
            label="Song Title",
            hint_text="Enter song title...",
            autofocus=True,
            height=60
        )
        
        artist_field = ft.TextField(
            label="Artist (optional)",
            hint_text="Enter artist name...",
            height=60
        )

        dialog = ft.AlertDialog(
            title=ft.Text("💾 Save Song", size=20),
            content=ft.Container(
                content=ft.Column([
                    title_field,
                    ft.Container(height=10),  # Spacing
                    artist_field,
                ], tight=True),
                width=300,
                height=150
            ),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.FilledButton("Save", on_click=save_song),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_library(self, e):
        """Show the song library (mobile optimized)"""
        self.show_library = True
        self.build_ui(self.page)

    def back_to_main(self, e):
        """Go back to main app from library"""
        self.show_library = False
        self.build_ui(self.page)

    def build_library_view(self):
        """Build mobile-optimized library view"""
        if not self.song_library:
            return ft.Container(
                content=ft.Column([
                    ft.Container(height=50),
                    ft.Icon(ft.Icons.MUSIC_NOTE, size=80, color=ft.Colors.GREY),
                    ft.Text("No songs saved yet", size=18, color=ft.Colors.GREY),
                    ft.Container(height=20),
                    ft.FilledButton(
                        "← Back to Main",
                        on_click=self.back_to_main,
                        height=self.button_height
                    )
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True
            )

        # Create song list
        song_items = []
        for song_id, song in self.song_library.items():
            def load_song(song_data):
                def _load(e):
                    self.current_song = song_data
                    self.formatted_lyrics = song_data['lyrics']
                    self.original_lyrics = song_data.get('original_lyrics', song_data['lyrics'])
                    self.lyrics_display.value = self.formatted_lyrics
                    self.is_preview_mode = True
                    self.back_to_main(e)
                return _load

            song_tile = ft.ListTile(
                leading=ft.Icon(ft.Icons.MUSIC_NOTE),
                title=ft.Text(song['title'], weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"by {song['artist']}", color=ft.Colors.GREY),
                on_click=load_song(song),
                content_padding=ft.padding.all(15)
            )
            song_items.append(song_tile)

        return ft.Column([
            # Header
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        on_click=self.back_to_main,
                        icon_size=30
                    ),
                    ft.Text("📚 Song Library", size=24, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.START),
                padding=ft.padding.all(15)
            ),
            
            # Song list
            ft.Container(
                content=ft.ListView(
                    controls=song_items,
                    spacing=5
                ),
                expand=True
            )
        ])

    def build_ui(self, page):
        """Build the main UI (mobile-optimized)"""
        self.page = page
        page.title = "Better Lyrics Mobile"
        page.theme_mode = ft.ThemeMode.DARK if self.is_dark_mode else ft.ThemeMode.LIGHT
        page.padding = 0
        
        # Clear existing controls
        page.controls.clear()
        
        if self.show_library:
            page.add(self.build_library_view())
            return

        if self.is_preview_mode:
            # Preview Mode - Show formatted lyrics
            self.lyrics_display = ft.Text(
                value=self.formatted_lyrics,
                size=self.font_size_mobile,
                selectable=True
            )
            
            content = ft.Column([
                # Header with back button
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            ft.Icons.EDIT,
                            on_click=lambda e: self.switch_to_edit_mode(),
                            icon_size=30,
                            tooltip="Edit lyrics"
                        ),
                        ft.Text("Better Lyrics", size=20, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            ft.Icons.LIBRARY_MUSIC,
                            on_click=self.show_library,
                            icon_size=30,
                            tooltip="Song library"
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.Colors.SURFACE,
                    padding=ft.padding.all(15)
                ),
                
                # Lyrics display
                ft.Container(
                    content=ft.ListView([
                        ft.Container(
                            content=self.lyrics_display,
                            padding=ft.padding.all(20)
                        )
                    ]),
                    expand=True
                ),
                
                # Bottom controls
                ft.Container(
                    content=ft.Row([
                        ft.FilledButton(
                            "💾 Save",
                            on_click=self.save_current_song,
                            height=self.button_height,
                            width=100
                        ),
                        ft.FilledTonalButton(
                            "🌓 Theme",
                            on_click=self.toggle_theme,
                            height=self.button_height,
                            width=100
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                    padding=ft.padding.all(15),
                    bgcolor=ft.Colors.SURFACE
                )
            ])
            
        else:
            # Edit Mode - Input lyrics
            self.lyrics_input = ft.TextField(
                label="Paste your lyrics here...",
                multiline=True,
                min_lines=15,
                max_lines=20,
                value=self.original_lyrics,
                text_size=14,
                expand=True
            )
            
            content = ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Text("Better Lyrics", size=20, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            ft.Icons.LIBRARY_MUSIC,
                            on_click=self.show_library,
                            icon_size=30,
                            tooltip="Song library"
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.Colors.SURFACE,
                    padding=ft.padding.all(15)
                ),
                
                # Input area
                ft.Container(
                    content=self.lyrics_input,
                    padding=ft.padding.all(15),
                    expand=True
                ),
                
                # Bottom controls
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.FilledButton(
                                "📋 Paste",
                                on_click=self.paste_from_clipboard,
                                height=self.button_height,
                                width=self.button_width
                            ),
                            ft.FilledButton(
                                "✨ Transform",
                                on_click=self.transform_lyrics,
                                height=self.button_height,
                                width=self.button_width
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                        
                        ft.Container(height=10),  # Spacing
                        
                        ft.FilledTonalButton(
                            "🌓 Toggle Theme",
                            on_click=self.toggle_theme,
                            height=self.button_height,
                            width=200
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(15),
                    bgcolor=ft.Colors.SURFACE
                )
            ])

        page.add(content)


def main(page: ft.Page):
    """Main entry point for mobile app"""
    # Mobile-specific settings
    page.window.width = 400
    page.window.height = 800
    page.window.resizable = False  # Fixed size for mobile simulation
    page.scroll = ft.ScrollMode.AUTO
    
    app = BetterLyricsMobile()
    app.build_ui(page)


if __name__ == "__main__":
    # Mobile app entry point
    import os
    assets_dir = os.path.dirname(os.path.abspath(__file__))
    ft.app(target=main, assets_dir=assets_dir)
