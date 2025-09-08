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


class BetterLyricsApp:
    """
    A Flet desktop application to format and display song lyrics with enhanced
    readability and customization options, plus song library management.
    """
    def __init__(self):
        # --- State Management ---
        self.is_dark_mode = True
        self.is_preview_mode = False
        self.original_lyrics = ""
        self.formatted_lyrics = ""
        self.current_song = None  # Currently loaded song data

        # --- Logo Path ---
        # Get the relative path to the logo file for Flet assets
        self.logo_path = "better_lyrics_header_final.png"
        print(f"🖼️ Logo path: {self.logo_path}")

        # --- Song Library Management ---
        # Create saved_songs directory if it doesn't exist
        self.songs_directory = "saved_songs"
        if not os.path.exists(self.songs_directory):
            os.makedirs(self.songs_directory)
        
        self.songs_file = os.path.join(self.songs_directory, "songs_library.json")
        self.playlists_file = os.path.join(self.songs_directory, "playlists.json")
        self.song_library = self._load_song_library()
        self.playlists = self._load_playlists()
        self.current_playlist = None
        self.show_library = False  # Toggle between main app and library view

        # --- Auto-scroll Properties ---
        self.is_playing = False
        self.scroll_speed = 1.0  # Speed multiplier
        self.buffer_lines = 4  # Buffer lines at top before lyrics start
        self.song_length_seconds = 180  # Default 3 minutes
        self.use_song_length_mode = False  # False = speed mode, True = song length mode
        self.song_length_display_text = None  # For displaying time in the UI

        # --- Customization Properties ---
        self.text_alignment = ft.TextAlign.CENTER
        self.line_spacing = 1.2
        self.font_size = 24

        # --- UI Control References ---
        self.lyrics_input = None
        self.theme_button = None
        self.lyrics_display_container = None
        
        # Portal box for drag and drop - removed (not reliable)
        # self.portal_overlay = None
        # self.is_portal_visible = False

    def _show_message(self, page, message):
        """Displays a short message at the bottom of the app."""
        page.snack_bar = ft.SnackBar(ft.Text(message), duration=2000)
        page.snack_bar.open = True
        page.update()

    def _rebuild_ui(self, page):
        """Clears and rebuilds the entire UI based on the current app state."""
        try:
            print("🔄 Starting UI rebuild...")
            page.clean()
            self.build_ui(page)
            page.update()
            print("✅ UI rebuild completed successfully")
        except Exception as e:
            print(f"❌ Error during UI rebuild: {e}")
            traceback.print_exc()
            # Try to recover by at least updating the page
            try:
                page.update()
            except:
                print("❌ Could not even update page, app may be frozen")
                pass

    # --- Song Library Management ---

    def _load_song_library(self):
        """Load song library from JSON file."""
        if os.path.exists(self.songs_file):
            try:
                with open(self.songs_file, 'r', encoding='utf-8') as f:
                    library = json.load(f)
                    print(f"✅ Loaded {len(library)} songs from {self.songs_file}")
                    return library
            except Exception as e:
                print(f"❌ Error loading song library: {e}")
                # Create backup of corrupted file
                backup_file = self.songs_file + ".backup"
                try:
                    if os.path.exists(self.songs_file):
                        os.rename(self.songs_file, backup_file)
                        print(f"💾 Corrupted file backed up as {backup_file}")
                except:
                    pass
        
        print(f"📁 Creating new song library at {self.songs_file}")
        return []

    def _save_song_library(self):
        """Save song library to JSON file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.songs_file), exist_ok=True)
            
            with open(self.songs_file, 'w', encoding='utf-8') as f:
                json.dump(self.song_library, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved {len(self.song_library)} songs to {self.songs_file}")
        except Exception as e:
            print(f"❌ Error saving song library: {e}")

    def _load_playlists(self):
        """Load playlists from JSON file."""
        if os.path.exists(self.playlists_file):
            try:
                with open(self.playlists_file, 'r', encoding='utf-8') as f:
                    playlists = json.load(f)
                    print(f"✅ Loaded playlists from {self.playlists_file}")
                    return playlists
            except Exception as e:
                print(f"❌ Error loading playlists: {e}")
                # Create backup of corrupted file
                backup_file = self.playlists_file + ".backup"
                try:
                    if os.path.exists(self.playlists_file):
                        os.rename(self.playlists_file, backup_file)
                        print(f"💾 Corrupted file backed up as {backup_file}")
                except:
                    pass
        
        print(f"📁 Creating new playlists file at {self.playlists_file}")
        return {"Favorites": []}

    def _save_playlists(self):
        """Save playlists to JSON file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.playlists_file), exist_ok=True)
            
            with open(self.playlists_file, 'w', encoding='utf-8') as f:
                json.dump(self.playlists, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved playlists to {self.playlists_file}")
        except Exception as e:
            print(f"❌ Error saving playlists: {e}")

    def _delete_playlist_dialog(self, playlist_name, page):
        """Show confirmation dialog for deleting a playlist."""
        if playlist_name == "Favorites":
            self._show_message(page, "Cannot delete the Favorites playlist!")
            return
        
        song_count = len(self.playlists.get(playlist_name, []))
        
        def confirm_delete(e):
            if playlist_name in self.playlists:
                del self.playlists[playlist_name]
                self._save_playlists()
                self._show_message(page, f"🗑️ Deleted playlist: {playlist_name}")
                self._rebuild_ui(page)
            dialog.open = False
            page.update()
        
        def cancel_delete(e):
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Delete Playlist?"),
            content=ft.Text(f"Are you sure you want to delete '{playlist_name}'?\n\nThis playlist contains {song_count} songs.\nThe songs themselves will not be deleted.\n\nThis action cannot be undone."),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.ElevatedButton("Delete Playlist", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED_400))
            ]
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def _create_song_entry(self, title, artist, lyrics, original_lyrics=None):
        """Create a new song entry for the library."""
        return {
            "id": str(uuid.uuid4()),
            "title": title.strip(),
            "artist": artist.strip(),
            "lyrics": lyrics,
            "original_lyrics": original_lyrics or lyrics,
            "created_at": datetime.now().isoformat(),
            "last_played": None,
            "play_count": 0,
            "is_favorite": False
        }

    def _add_song_to_library(self, title, artist, lyrics, original_lyrics=None):
        """Add a new song to the library."""
        song = self._create_song_entry(title, artist, lyrics, original_lyrics)
        self.song_library.append(song)
        self._save_song_library()
        self._save_playlists()
        
        return song

    def _get_song_by_id(self, song_id):
        """Get a song by its ID."""
        for song in self.song_library:
            if song["id"] == song_id:
                return song
        return None

    def _update_song_played(self, song_id):
        """Update song play statistics."""
        song = self._get_song_by_id(song_id)
        if song:
            song["last_played"] = datetime.now().isoformat()
            song["play_count"] += 1
            self._save_song_library()
            self._save_playlists()

    def _create_new_playlist(self, e):
        """Create a new playlist."""
        page = e.page
        dialog_ref = None  # Store dialog reference
        
        def close_dialog(e=None):
            # Safely close and remove dialog
            try:
                if dialog_ref and dialog_ref in page.overlay:
                    dialog_ref.open = False
                    page.overlay.remove(dialog_ref)
                    print(f"✅ Dialog closed successfully")
                page.update()
            except Exception as ex:
                print(f"Error closing dialog: {ex}")
                # Try to update page anyway
                try:
                    page.update()
                except:
                    pass
        
        def create_playlist(e=None):
            try:
                playlist_name = playlist_name_field.value.strip()
                print(f"🐛 Creating playlist: '{playlist_name}'")
                
                if not playlist_name:
                    self._show_message(page, " Please enter a playlist name!")
                    return
                    
                if playlist_name in self.playlists:
                    self._show_message(page, f" Playlist '{playlist_name}' already exists!")
                    return
                
                # Create the playlist
                self.playlists[playlist_name] = []
                self._save_playlists()
                print(f"✅ Playlist '{playlist_name}' created successfully")
                
                # Close dialog first
                close_dialog()
                
                # Show success message and refresh the library view
                self._show_message(page, f"✨ Playlist '{playlist_name}' created!")
                
                # Properly refresh the library view to show the new playlist
                def refresh_library():
                    try:
                        if self.show_library:
                            print("🔄 Refreshing library view to show new playlist...")
                            self._rebuild_ui(page)
                            print("✅ Library view refreshed successfully")
                        else:
                            print("Not in library view, just updating page")
                            page.update()
                    except Exception as ex:
                        print(f"❌ Error refreshing library: {ex}")
                        traceback.print_exc()
                
                # Call refresh after a small delay to ensure dialog is fully closed
                import threading
                def delayed_refresh():
                    time.sleep(0.1)  # Small delay to ensure dialog is closed
                    refresh_library()
                
                threading.Thread(target=delayed_refresh, daemon=True).start()
                
            except Exception as ex:
                print(f" Error in create_playlist: {ex}")
                traceback.print_exc()
                self._show_message(page, f" Error: {str(ex)}")
        
        def on_text_submit(e):
            # Handle Enter key press - call create_playlist without rebuilding UI immediately
            print(f"🐛 Text submitted via Enter key")
            create_playlist(e)
        
        playlist_name_field = ft.TextField(
            label="Playlist Name",
            hint_text="Enter a name for your new playlist",
            autofocus=True,
            on_submit=on_text_submit
        )
        
        dialog_ref = ft.AlertDialog(
            modal=True,
            title=ft.Text("🎵 Create New Playlist"),
            content=ft.Container(
                content=playlist_name_field,
                width=300,
                padding=ft.padding.all(20)
            ),
            actions=[
                ft.ElevatedButton("✨ Create", on_click=create_playlist),
                ft.TextButton("Cancel", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        
        try:
            page.overlay.append(dialog_ref)
            dialog_ref.open = True
            page.update()
            print(f"✅ Dialog opened successfully")
        except Exception as ex:
            print(f" Error opening dialog: {ex}")
            import traceback
            traceback.print_exc()

    def _toggle_favorite(self, song_id):
        """Toggle favorite status of a song."""
        song = self._get_song_by_id(song_id)
        if song:
            song["is_favorite"] = not song["is_favorite"]
            self._save_song_library()
            
            # Ensure Favorites playlist exists
            if "Favorites" not in self.playlists:
                self.playlists["Favorites"] = []
            
            # Update favorites playlist
            favorites_list = self.playlists["Favorites"]
            if song["is_favorite"] and song_id not in favorites_list:
                favorites_list.append(song_id)
            elif not song["is_favorite"] and song_id in favorites_list:
                favorites_list.remove(song_id)
            
            self._save_playlists()

    def _delete_song(self, song_id):
        """Delete a song from the library."""
        self.song_library = [s for s in self.song_library if s["id"] != song_id]
        self._save_song_library()
        
        # Remove from all playlists
        for playlist_name in self.playlists:
            if song_id in self.playlists[playlist_name]:
                self.playlists[playlist_name].remove(song_id)
        self._save_playlists()

    def _load_song(self, song_id, page):
        """Load a song from the library into the app."""
        song = self._get_song_by_id(song_id)
        if song:
            self.current_song = song
            self.original_lyrics = song["original_lyrics"]
            self.formatted_lyrics = song["lyrics"]
            self.is_preview_mode = True
            self.show_library = False
            
            # Update play statistics
            self._update_song_played(song_id)
            
            self._rebuild_ui(page)
            self._show_message(page, f"🎵 Loaded: {song['title']} - {song['artist']}")

    def toggle_library_view(self, e):
        """Toggle between main app and library view."""
        self.show_library = not self.show_library
        self._rebuild_ui(e.page)

    def _parse_title_artist_from_text(self, text):
        """Try to extract title and artist from pasted text."""
        lines = text.strip().split('\n')
        first_line = lines[0].strip()
        
        # Common patterns to look for
        patterns = [
            r'^(.+?)\s*-\s*(.+?)$',  # "Artist - Title" or "Title - Artist"
            r'^(.+?)\s*by\s+(.+?)$',  # "Title by Artist"
            r'^(.+?)\s*\|\s*(.+?)$',  # "Title | Artist"
            r'^\[(.+?)\]\s*(.+?)$',   # "[Artist] Title"
        ]
        
        import re
        for pattern in patterns:
            match = re.match(pattern, first_line, re.IGNORECASE)
            if match:
                part1, part2 = match.groups()
                
                # Improved logic for determining title vs artist
                # Check for common separators and formats
                if ' by ' in first_line.lower():
                    # "Title by Artist" format
                    return part1.strip(), part2.strip()  # title, artist
                elif any(indicator in part1.lower() for indicator in ['feat', 'ft.', 'featuring', '&', 'and']):
                    # First part looks like it has featured artists
                    return part2.strip(), part1.strip()  # title, artist
                elif any(indicator in part2.lower() for indicator in ['feat', 'ft.', 'featuring']):
                    # Second part has featured info, so first is likely title
                    return part1.strip(), part2.strip()  # title, artist
                else:
                    # Default: assume "Artist - Title" format (most common)
                    # But check if first part looks more like a title (longer, has common title words)
                    title_indicators = ['love', 'you', 'me', 'my', 'the', 'a', 'an', 'is', 'are', 'was', 'were']
                    part1_words = part1.lower().split()
                    part2_words = part2.lower().split()
                    
                    part1_has_title_words = any(word in title_indicators for word in part1_words)
                    part2_has_title_words = any(word in title_indicators for word in part2_words)
                    
                    if part1_has_title_words and not part2_has_title_words:
                        # First part looks more like a title
                        return part1.strip(), part2.strip()  # title, artist
                    elif part2_has_title_words and not part1_has_title_words:
                        # Second part looks more like a title
                        return part2.strip(), part1.strip()  # title, artist
                    else:
                        # Default to "Artist - Title" format
                        return part2.strip(), part1.strip()  # title, artist
        
        # If no pattern matches, return first line as title, empty artist
        return first_line, ""

    def _toggle_current_favorite(self, e):
        """Toggle favorite status of current song."""
        print(f"🐛 DEBUG: current_song = {self.current_song}")
        
        if self.current_song:
            self._toggle_favorite(self.current_song["id"])
            # Update the current song reference
            self.current_song = self._get_song_by_id(self.current_song["id"])
            status = "Added to" if self.current_song["is_favorite"] else "Removed from"
            self._show_message(e.page, f"⭐ {status} favorites!")
            self._rebuild_ui(e.page)
        else:
            # If no current song is saved, show the save dialog first
            self._show_save_song_dialog_for_favorite(e.page)

    def _add_song_to_playlist_dialog(self, song_id, page):
        """Show dialog to add song to a playlist."""
        song = self._get_song_by_id(song_id)
        if not song:
            return
        
        # Get available playlists (exclude Favorites as it's handled separately)
        available_playlists = [name for name in self.playlists.keys() if name != "Favorites"]
        
        if not available_playlists:
            self._show_message(page, "No custom playlists found! Create one first.")
            return
        
        def add_to_playlist(playlist_name):
            if song_id not in self.playlists[playlist_name]:
                self.playlists[playlist_name].append(song_id)
                self._save_playlists()
                self._show_message(page, f"🎵 Added '{song['title']}' to '{playlist_name}'!")
            else:
                self._show_message(page, f"Song already in '{playlist_name}'!")
            # Properly remove dialog from overlay
            if dialog in page.overlay:
                page.overlay.remove(dialog)
            page.update()
            self._rebuild_ui(page)
        
        def close_dialog(e):
            # Properly remove dialog from overlay
            if dialog in page.overlay:
                page.overlay.remove(dialog)
            page.update()
        
        # Create playlist buttons
        playlist_buttons = []
        for playlist_name in available_playlists:
            song_count = len(self.playlists[playlist_name])
            playlist_buttons.append(
                ft.ElevatedButton(
                    f"🎵 {playlist_name} ({song_count})",
                    on_click=lambda e, pname=playlist_name: add_to_playlist(pname),
                    width=250
                )
            )
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Add to Playlist: {song['title']}"),
            content=ft.Container(
                content=ft.Column(
                    [ft.Text("Choose a playlist:", size=14)] + playlist_buttons,
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                width=300,
                padding=ft.padding.all(20)
            ),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def _remove_song_from_playlist_dialog(self, song_id, current_playlist, page):
        """Show dialog to remove song from current playlist."""
        song = self._get_song_by_id(song_id)
        if not song or not current_playlist:
            return
        
        def confirm_remove(e):
            if song_id in self.playlists[current_playlist]:
                self.playlists[current_playlist].remove(song_id)
                self._save_playlists()
                self._show_message(page, f"🗑️ Removed '{song['title']}' from '{current_playlist}'!")
            # Properly remove dialog from overlay
            if dialog in page.overlay:
                page.overlay.remove(dialog)
            page.update()
            self._rebuild_ui(page)
        
        def cancel_remove(e):
            # Properly remove dialog from overlay
            if dialog in page.overlay:
                page.overlay.remove(dialog)
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Remove from Playlist?"),
            content=ft.Text(f"Remove '{song['title']}' from '{current_playlist}'?"),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_remove),
                ft.ElevatedButton("Remove", on_click=confirm_remove, style=ft.ButtonStyle(color=ft.Colors.RED_400))
            ]
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def _create_portal_box(self):
        """Create the portal box overlay for drag and drop."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        ft.Icons.CLOUD_UPLOAD_ROUNDED,
                        size=80,
                        color=ft.Colors.BLUE_400
                    ),
                    ft.Text(
                        "🌟 Drop Your Lyrics Here!",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_600,
                        text_align="center"
                    ),
                    ft.Text(
                        "Release to instantly paste and auto-detect title/artist",
                        size=16,
                        color=ft.Colors.BLUE_500,
                        text_align="center"
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.SMART_TOY, size=20, color=ft.Colors.ORANGE_400),
                                ft.Text("Smart parsing enabled", size=14, color=ft.Colors.GREY_600),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        margin=ft.margin.only(top=10)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            width=400,
            height=300,
            bgcolor=ft.Colors.BLUE_50,
            border=ft.border.all(3, ft.Colors.BLUE_400),
            border_radius=20,
            padding=ft.padding.all(30),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=20,
                color=ft.Colors.BLUE_200,
            ),
            alignment=ft.alignment.center
        )

    def _show_portal_box(self, page):
        """Show the portal box overlay."""
        if not self.is_portal_visible:
            self.portal_overlay = ft.Container(
                content=self._create_portal_box(),
                width=page.width,
                height=page.height,
                bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
                alignment=ft.alignment.center,
            )
            
            # Add overlay to page
            page.overlay.append(self.portal_overlay)
            self.is_portal_visible = True
            page.update()

    def _hide_portal_box(self, page):
        """Hide the portal box overlay."""
        if self.is_portal_visible and self.portal_overlay:
            page.overlay.remove(self.portal_overlay)
            self.is_portal_visible = False
            self.portal_overlay = None
            page.update()

    def _create_drag_target_with_portal(self, content):
        """Create a drag target that shows/hides the portal box."""
        
        def on_will_accept(e):
            # Show portal box when drag enters
            self._show_portal_box(e.page)
            return True
        
        def on_leave(e):
            # Hide portal box when drag leaves
            self._hide_portal_box(e.page)
        
        def on_accept(e):
            # Hide portal box and handle dropped text
            self._hide_portal_box(e.page)
            
            # Handle dropped text
            dropped_text = e.data
            if dropped_text and self.lyrics_input:
                self.lyrics_input.value = dropped_text
                self.lyrics_input.update()
                # Try to parse title and artist
                title, artist = self._parse_title_artist_from_text(dropped_text)
                message = f"🌟 Lyrics dropped via portal!"
                if title:
                    message += f" Detected: '{title}'"
                    if artist:
                        message += f" by {artist}"
                self._show_message(e.page, message)
        
        # Create DragTarget that covers the whole input area
        return ft.DragTarget(
            group="text",
            content=content,
            on_will_accept=on_will_accept,
            on_leave=on_leave,
            on_accept=on_accept
        )

    def _create_enhanced_input_area(self, content):
        """Create an enhanced input area with better visual feedback and instructions."""
        
        def on_click(e):
            # Focus the text field when container is clicked
            if self.lyrics_input:
                self.lyrics_input.focus()
        
        def on_hover(e):
            # Visual feedback on hover
            if e.data == "true":  # Mouse enter
                e.control.bgcolor = ft.Colors.BLUE_50 if not self.is_dark_mode else ft.Colors.BLUE_GREY_900
                e.control.border = ft.border.all(2, ft.Colors.BLUE_300)
            else:  # Mouse leave
                e.control.bgcolor = None
                e.control.border = ft.border.all(2, ft.Colors.GREY_300)
            e.control.update()
        
        # Create enhanced container with visual feedback
        return ft.Container(
            content=content,
            expand=True,
            padding=ft.padding.all(15),
            border=ft.border.all(2, ft.Colors.GREY_300),
            border_radius=12,
            bgcolor=None,
            on_click=on_click,
            on_hover=on_hover,
        )

    # --- Customization Methods ---

    def change_alignment(self, e):
        """Changes the text alignment of the lyrics display."""
        self.text_alignment = e.control.data
        self._rebuild_ui(e.page)

    def change_line_spacing(self, e):
        """Changes the line spacing based on the slider."""
        self.line_spacing = e.control.value
        self._rebuild_ui(e.page)

    def change_font_size(self, e):
        """Changes the font size based on the slider."""
        self.font_size = e.control.value
        self._rebuild_ui(e.page)

    def change_scroll_speed(self, e):
        """Changes the auto-scroll speed based on the slider."""
        self.scroll_speed = e.control.value
        # Rebuild UI to update the display text above slider
        self._rebuild_ui(e.page)

    def change_song_length(self, e):
        """Updates song length and calculates optimal scroll speed."""
        self.song_length_seconds = e.control.value
        # Update the label dynamically with compact format
        e.control.label = self._format_time_compact(self.song_length_seconds)
        # Auto-calculate optimal scroll speed based on content and song length
        self._calculate_optimal_scroll_speed()
        # Rebuild UI to update the display text above slider
        self._rebuild_ui(e.page)

    def toggle_scroll_mode(self, e):
        """Toggles between manual speed control and song length mode."""
        self.use_song_length_mode = not self.use_song_length_mode
        # Rebuild the UI to show the correct slider
        self._rebuild_ui(e.page)

    def _calculate_optimal_scroll_speed(self):
        """Calculates perfect scroll speed based on song length and lyrics content."""
        if not self.formatted_lyrics:
            return
        
        # Estimate total scroll distance needed
        total_lines = len(self.formatted_lyrics.split('\n')) + self.buffer_lines
        estimated_scroll_height = total_lines * (self.font_size + 5)  # Rough estimate
        
        # Calculate pixels per second needed to finish in song_length_seconds
        pixels_per_second = estimated_scroll_height / self.song_length_seconds
        
        # Convert to our scroll speed multiplier with better scaling
        # Base is ~0.8 pixels per frame at 40fps = 32 pixels/second at 1x speed
        base_pixels_per_second = 32  # 0.8 * 40 fps
        calculated_speed = pixels_per_second / base_pixels_per_second
        
        # Apply more aggressive scaling for extreme values
        if self.song_length_seconds <= 60:  # 1 minute or less - SUPER FAST
            calculated_speed *= 2.0  # Double the speed for short songs
        elif self.song_length_seconds >= 600:  # 10+ minutes - SLOWER
            calculated_speed *= 0.6  # Slower for long songs
        
        # Clamp between reasonable bounds but allow more extreme values
        self.scroll_speed = max(0.05, min(5.0, calculated_speed))

    def _create_scroll_slider(self):
        """Creates the appropriate slider based on current mode."""
        if self.use_song_length_mode:
            # Create a column with slider and time display
            current_time_text = self._format_time_compact(self.song_length_seconds)
            
            return ft.Column([
                ft.Text(current_time_text, size=10, text_align="center", color=ft.Colors.BLUE_400),
                ft.Slider(
                    min=15,
                    max=1200,  # 20 minutes = 1200 seconds
                    value=self.song_length_seconds,
                    label=self._format_time_compact(self.song_length_seconds),
                    on_change=self.change_song_length,
                    width=120,
                    height=25
                )
            ], spacing=2, horizontal_alignment="center")
        else:
            return ft.Column([
                ft.Text(f"{self.scroll_speed:.1f}x", size=10, text_align="center", color=ft.Colors.GREEN_400),
                ft.Slider(
                    min=0.1,
                    max=5.0,  # Increased max to allow super fast speeds
                    value=self.scroll_speed,
                    label="Speed: {value:.1f}x",
                    on_change=self.change_scroll_speed,
                    width=120,
                    height=25
                )
            ], spacing=2, horizontal_alignment="center")

    def _format_time_compact(self, seconds):
        """Formats seconds into a compact time display for the slider."""
        seconds = int(seconds)
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:  # Less than 1 hour
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes}m"
            else:
                return f"{minutes}m:{remaining_seconds:02d}s"
        else:  # 1 hour or more (though we max at 20 min)
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h:{minutes:02d}m"

    def _format_time_label(self, seconds):
        """Formats seconds into a readable time label."""
        seconds = int(seconds)
        if seconds < 60:
            return f"{seconds} sec"
        elif seconds < 3600:  # Less than 1 hour
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes} min"
            else:
                return f"{minutes}m {remaining_seconds}s"
        else:  # 1 hour or more (though we max at 20 min)
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"

    def change_buffer_lines(self, e):
        """Updates the buffer lines and refreshes the lyrics display."""
        self.buffer_lines = int(e.control.value)
        # Refresh the preview to show the new buffer
        self._refresh_preview_display(e.page)
        e.page.update()

    def _refresh_preview_display(self, page):
        """Refreshes the lyrics display with current buffer lines."""
        if self.is_preview_mode and self.lyrics_display_container:
            # Rebuild the lyrics with new buffer
            lyrics_lines = self.formatted_lyrics.split('\n') if self.formatted_lyrics else [""]
            buffer_lines = [" "] * self.buffer_lines
            all_lines = buffer_lines + lyrics_lines
            
            # Update the ListView controls
            self.lyrics_display_container.controls = [
                ft.Text(
                    line if line.strip() else " ",
                    size=self.font_size,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE if self.is_dark_mode else ft.Colors.BLACK,
                    text_align=self.text_alignment,
                    selectable=True,
                ) for line in all_lines
            ]

    def toggle_play_pause(self, e):
        """Toggles the auto-scroll play/pause state."""
        import threading
        import time
        
        self.is_playing = not self.is_playing
        
        if self.is_playing:
            # Start auto-scroll at fixed speed
            def scroll_lyrics():
                scroll_position = 0
                while self.is_playing and self.lyrics_display_container:
                    try:
                        # Slower, smoother scrolling: even smaller increments
                        scroll_increment = max(0.5, self.scroll_speed * 0.8)  # Much slower base speed
                        scroll_position += scroll_increment
                        
                        # Update the scroll position of the ListView with no duration for instant updates
                        self.lyrics_display_container.scroll_to(offset=scroll_position, duration=0)
                        e.page.update()
                        
                        # Keep smooth 40 fps timing
                        sleep_time = 0.025  # 40 fps base rate
                        time.sleep(sleep_time)
                    except Exception as ex:
                        print(f"Scroll error: {ex}")
                        break
            
            # Start scrolling in background thread
            scroll_thread = threading.Thread(target=scroll_lyrics, daemon=True)
            scroll_thread.start()
            
            self._show_message(e.page, "▶️ Auto-scroll started")
        else:
            self._show_message(e.page, "⏸️ Auto-scroll paused")
        
        self._rebuild_ui(e.page)

    # --- Core Logic Methods ---

    def format_lyrics(self, text: str) -> str:
        """Cleans up lyrics text by trimming whitespace and normalizing line breaks."""
        if not text.strip():
            return ""
        
        lines = text.strip().split('\n')
        cleaned_lines = [line.strip() for line in lines]
        
        # Consolidate multiple blank lines into a single one
        final_lyrics = []
        for i, line in enumerate(cleaned_lines):
            if line or (i > 0 and cleaned_lines[i-1]):
                final_lyrics.append(line)
        
        return '\n'.join(final_lyrics)

    def _create_portal_dialog(self):
        """Create a portal dialog for enhanced pasting experience."""
        
        def close_portal(e):
            self.portal_dialog.open = False
            self.page.update()
        
        def paste_and_parse(e):
            try:
                clipboard_text = pyclip.paste()
                if clipboard_text.strip():
                    self.lyrics_input.value = clipboard_text
                    self.lyrics_input.update()
                    
                    # Try to parse title and artist
                    title, artist = self._parse_title_artist_from_text(clipboard_text)
                    message = f"🌟 Portal paste successful!"
                    if title:
                        message += f" Detected: '{title}'"
                        if artist:
                            message += f" by {artist}"
                    
                    self._show_message(self.page, message)
                    close_portal(e)
                else:
                    self._show_message(self.page, "❌ Clipboard is empty - copy some text first!")
            except Exception as ex:
                self._show_message(self.page, f"❌ Error: {str(ex)}")
        
        self.portal_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.OPEN_IN_NEW, color=ft.Colors.BLUE_400),
                    ft.Text("🌟 Lyrics Portal", weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.CLOUD_DOWNLOAD_ROUNDED,
                                size=80,
                                color=ft.Colors.BLUE_400
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(bottom=20)
                        ),
                        ft.Text(
                            "Ready to import your lyrics!",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            text_align="center"
                        ),
                        ft.Text(
                            "1. Copy lyrics from any website (Ctrl+C)\n"
                            "2. Click 'Portal Paste' below\n"
                            "3. Title/artist will be auto-detected!",
                            size=14,
                            text_align="center",
                            color=ft.Colors.GREY_600
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.SMART_TOY, size=20, color=ft.Colors.ORANGE_400),
                                    ft.Text("Smart parsing enabled", size=12, color=ft.Colors.GREY_600),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            margin=ft.margin.only(top=15)
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                width=350,
                padding=ft.padding.all(20)
            ),
            actions=[
                ft.ElevatedButton(
                    "🌟 Portal Paste",
                    icon=ft.Icons.DOWNLOAD_ROUNDED,
                    on_click=paste_and_parse,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE
                    )
                ),
                ft.TextButton("Cancel", on_click=close_portal),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        
        return self.portal_dialog

    def show_portal(self, e):
        """Show the portal dialog."""
        if not hasattr(self, 'portal_dialog'):
            self._create_portal_dialog()
        
        self.portal_dialog.open = True
        self.page.overlay.append(self.portal_dialog)
        self.page.update()

    def smart_paste_lyrics(self, e):
        """Smart paste that also attempts to parse title/artist."""
        try:
            # Get clipboard content
            clipboard_text = pyclip.paste()
            if clipboard_text.strip():
                # Set the lyrics
                self.lyrics_input.value = clipboard_text
                self.lyrics_input.update()
                
                # Try to parse title and artist
                title, artist = self._parse_title_artist_from_text(clipboard_text)
                message = f"📋 Lyrics pasted!"
                if title:
                    message += f" Detected: '{title}'"
                    if artist:
                        message += f" by {artist}"
                    message += " - Use save button to store!"
                    
                self._show_message(e.page, message)
                self.page.update()
            else:
                self._show_message(e.page, "❌ Clipboard is empty - copy some text first!")
        except Exception as ex:
            self._show_message(e.page, f"❌ Error pasting: {str(ex)}")

    def paste_lyrics(self, e):
        """Pastes lyrics from the system clipboard into the input field."""
        try:
            clipboard_content = pyclip.paste()
            if clipboard_content and self.lyrics_input:
                self.lyrics_input.value = clipboard_content
                self.lyrics_input.update()
                self._show_message(e.page, "✨ Lyrics pasted successfully!")
            else:
                self._show_message(e.page, "Clipboard is empty or input field is not available.")
        except Exception:
            self._show_message(e.page, "Could not paste lyrics. Please try Ctrl+V.")

    def copy_lyrics(self, e):
        """Copies the currently displayed lyrics to the system clipboard."""
        lyrics_to_copy = self.formatted_lyrics if self.is_preview_mode else (self.lyrics_input.value if self.lyrics_input else "")
        
        if lyrics_to_copy.strip():
            try:
                pyclip.copy(lyrics_to_copy)
                self._show_message(e.page, "✨ Lyrics copied to clipboard!")
            except Exception:
                self._show_message(e.page, "Could not copy to clipboard.")
        else:
            self._show_message(e.page, "There are no lyrics to copy.")

    def transform_lyrics(self, e):
        """Switches to the preview mode to display formatted lyrics."""
        if not self.lyrics_input or not self.lyrics_input.value.strip():
            self._show_message(e.page, "Please enter some lyrics first!")
            return
        
        self.original_lyrics = self.lyrics_input.value
        self.formatted_lyrics = self.format_lyrics(self.original_lyrics)
        self.is_preview_mode = True
        
        # If in song length mode, calculate optimal scroll speed
        if self.use_song_length_mode:
            self._calculate_optimal_scroll_speed()
        
        self._rebuild_ui(e.page)
        self._show_message(e.page, "✨ Better Lyrics Enhanced View Activated!")

    def _show_save_song_dialog(self, page):
        """Show dialog to save the current song to library."""
        print(f"🐛 DEBUG: is_preview_mode = {self.is_preview_mode}")
        print(f"🐛 DEBUG: current_song = {self.current_song}")
        print(f"🐛 DEBUG: original_lyrics length = {len(self.original_lyrics) if self.original_lyrics else 0}")
        
        # Try to auto-parse title and artist from the original lyrics
        suggested_title, suggested_artist = self._parse_title_artist_from_text(self.original_lyrics)
        print(f"🐛 DEBUG: suggested_title = '{suggested_title}', suggested_artist = '{suggested_artist}'")
        
        # If updating existing song, use current values
        if self.current_song:
            initial_title = self.current_song.get("title", suggested_title)
            initial_artist = self.current_song.get("artist", suggested_artist)
            dialog_title = "Update Song in Library"
            save_button_text = "💾 Update Song"
        else:
            initial_title = suggested_title
            initial_artist = suggested_artist
            dialog_title = "Save Song to Library"
            save_button_text = "💾 Save Song"
        
        print(f"🐛 DEBUG: Creating dialog with title='{dialog_title}'")
        
        title_field = ft.TextField(
            label="Song Title",
            value=initial_title,
            width=300,
            helper_text="Auto-detected from first line" if suggested_title else "Enter the song title"
        )
        artist_field = ft.TextField(
            label="Artist",
            value=initial_artist,
            width=300,
            helper_text="Auto-detected from first line" if suggested_artist else "Enter the artist name"
        )
        
        def save_song(e):
            print(f"🐛 DEBUG: save_song called with title='{title_field.value}', artist='{artist_field.value}'")
            if title_field.value and artist_field.value:
                if self.current_song:
                    # Update existing song
                    self.current_song["title"] = title_field.value
                    self.current_song["artist"] = artist_field.value
                    self.current_song["lyrics"] = self.formatted_lyrics
                    self.current_song["original_lyrics"] = self.original_lyrics
                    self._save_song_library()
                    self._show_message(page, f"💾 Updated: {self.current_song['title']} - {self.current_song['artist']}")
                else:
                    # Save new song
                    song = self._add_song_to_library(
                        title_field.value,
                        artist_field.value,
                        self.formatted_lyrics,
                        self.original_lyrics
                    )
                    self.current_song = song
                    self._show_message(page, f"💾 Saved: {song['title']} - {song['artist']}")
                
                # Properly remove dialog from overlay
                if dialog in page.overlay:
                    page.overlay.remove(dialog)
                page.update()
                self._rebuild_ui(page)  # Refresh UI to show updated state
            else:
                self._show_message(page, "Please enter both title and artist!")
        
        def skip_save(e):
            # Properly remove dialog from overlay
            if dialog in page.overlay:
                page.overlay.remove(dialog)
            page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(dialog_title),
            content=ft.Column([
                ft.Text("Save this song for easy access later:", size=14),
                ft.Text("💡 Title and artist were auto-detected from your lyrics!" if suggested_title or suggested_artist else "💡 Tip: Use format 'Title - Artist' for auto-detection", 
                       size=12, color=ft.Colors.BLUE_400),
                title_field,
                artist_field
            ], spacing=10, height=180),
            actions=[
                ft.TextButton("Cancel", on_click=skip_save),
                ft.ElevatedButton(save_button_text, on_click=save_song)
            ]
        )
        
        # For Flet 0.28.3, use page.overlay instead of page.dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def _show_save_song_dialog_for_favorite(self, page):
        """Show dialog to save the current song and automatically add to favorites."""
        # Present blank fields for user to fill in
        title_field = ft.TextField(
            label="Song Title",
            value="",
            width=300,
            helper_text="Enter the song title",
            autofocus=True
        )
        artist_field = ft.TextField(
            label="Artist",
            value="",
            width=300,
            helper_text="Enter the artist name"
        )
        
        def save_and_favorite(e):
            if title_field.value and artist_field.value:
                try:
                    # Save new song
                    song = self._add_song_to_library(
                        title_field.value,
                        artist_field.value,
                        self.formatted_lyrics,
                        self.original_lyrics
                    )
                    self.current_song = song
                    
                    # Automatically add to favorites
                    self._toggle_favorite(song["id"])
                    # Update the current song reference to get the favorite status
                    self.current_song = self._get_song_by_id(song["id"])
                    
                    # Properly remove dialog from overlay first
                    if dialog in page.overlay:
                        page.overlay.remove(dialog)
                    
                    self._show_message(page, f"⭐ Saved and added to favorites: {song['title']} - {song['artist']}")
                    page.update()
                    
                    # Refresh UI to show updated state with error handling
                    try:
                        self._rebuild_ui(page)
                    except Exception as rebuild_error:
                        print(f"❌ Error during UI rebuild after saving favorite: {rebuild_error}")
                        # Fallback: just update the page instead of full rebuild
                        page.update()
                        
                except Exception as save_error:
                    print(f"❌ Error saving favorite song: {save_error}")
                    # Properly remove dialog from overlay
                    if dialog in page.overlay:
                        page.overlay.remove(dialog)
                    self._show_message(page, "❌ Error saving song. Please try again.")
                    page.update()
            else:
                self._show_message(page, "Please enter both title and artist!")
        
        def skip_save(e):
            # Properly remove dialog from overlay
            if dialog in page.overlay:
                page.overlay.remove(dialog)
            page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⭐ Save Song to Favorites"),
            content=ft.Column([
                ft.Text("Save this song and add it to your favorites:", size=14),
                ft.Text("💡 Enter the title and artist for this song", 
                       size=12, color=ft.Colors.BLUE_400),
                title_field,
                artist_field
            ], spacing=10, height=180),
            actions=[
                ft.TextButton("Cancel", on_click=skip_save),
                ft.ElevatedButton("⭐ Save & Favorite", on_click=save_and_favorite, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_100))
            ]
        )
        
        # For Flet 0.28.3, use page.overlay instead of page.dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def _save_from_edit_mode(self, page):
        """Save song directly from edit mode without transforming first."""
        
        if not self.lyrics_input or not self.lyrics_input.value.strip():
            self._show_message(page, "Please enter some lyrics first!")
            return
        
        # Set the lyrics data for saving
        self.original_lyrics = self.lyrics_input.value
        self.formatted_lyrics = self.format_lyrics(self.original_lyrics)
        
        # Show the save dialog
        self._show_save_song_dialog(page)

    def start_new_transformation(self, e):
        """Switches back to the edit mode, clearing the previous input."""
        self.is_preview_mode = False
        self.original_lyrics = ""
        self.formatted_lyrics = ""
        self.current_song = None  # Clear current song
        if self.lyrics_input:
            self.lyrics_input.value = ""
        self._rebuild_ui(e.page)
        self._show_message(e.page, "Ready for new lyrics!")

    def toggle_theme(self, e):
        """Toggles the app's theme between dark and light mode."""
        self.is_dark_mode = not self.is_dark_mode
        e.page.theme_mode = ft.ThemeMode.DARK if self.is_dark_mode else ft.ThemeMode.LIGHT
        
        if self.is_dark_mode:
            self._show_message(e.page, "🌙 Switched to Dark Mode")
        else:
            self._show_message(e.page, "☀️ Switched to Light Mode")
            
        self._rebuild_ui(e.page)

    # --- UI Construction ---

    def _build_library_ui(self):
        """Builds the library/history view UI."""
        # Build dynamic tabs for all playlists
        playlist_tabs = []
        
        # All Songs tab
        playlist_tabs.append(
            ft.Tab(
                text=f"📚 All Songs ({len(self.song_library)})",
                content=self._build_song_list_view(self.song_library, sort_by="title", current_playlist="All Songs")
            )
        )
        
        # Favorites tab
        favorites_count = len(self.playlists.get('Favorites', []))
        playlist_tabs.append(
            ft.Tab(
                text=f"⭐ Favorites ({favorites_count})",
                content=self._build_playlist_view("Favorites")
            )
        )
        
        # Custom playlist tabs
        for playlist_name, song_ids in self.playlists.items():
            if playlist_name != "Favorites":  # Skip favorites as it's already added
                playlist_tabs.append(
                    ft.Tab(
                        text=f"� {playlist_name} ({len(song_ids)})",
                        content=self._build_playlist_view(playlist_name)
                    )
                )
        
        # By Artist tab
        playlist_tabs.append(
            ft.Tab(
                text=f"🎤 By Artist",
                content=self._build_artist_grouped_view()
            )
        )
        
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=200,
            tabs=playlist_tabs
        )

        # Action buttons
        action_buttons = ft.Row([
            ft.ElevatedButton(
                "📄 New Song",
                icon=ft.Icons.ADD,
                on_click=self.toggle_library_view
            ),
            ft.ElevatedButton(
                "🎵 New Playlist",
                icon=ft.Icons.PLAYLIST_ADD,
                on_click=self._create_new_playlist
            ),
            ft.ElevatedButton(
                f"Clear All ({len(self.song_library)})",
                icon=ft.Icons.DELETE_SWEEP,
                on_click=self._clear_library_dialog,
                style=ft.ButtonStyle(color=ft.Colors.RED_400)
            )
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)

        # Library stats
        stats_row = ft.Row([
            ft.Text(f"� {len(self.song_library)} songs total", size=14, color=ft.Colors.GREY_500),
            ft.Text(f"⭐ {len(self.playlists.get('Favorites', []))} favorites", size=14, color=ft.Colors.GREY_500),
            ft.Text(f"📁 Saved in: {self.songs_directory}/", size=14, color=ft.Colors.GREY_500)
        ], spacing=20)

        return ft.Column([
            action_buttons,
            stats_row,
            # Tabs content gets the remaining space with spacer from logo
            ft.Container(
                content=tabs, 
                expand=True, 
                padding=10,
                margin=ft.margin.only(top=20)  # Add space between logo and tabs
            )
        ], expand=True, spacing=15)

    def _build_song_list_view(self, songs, sort_by="recent", current_playlist=None):
        """Build a scrollable list of songs."""
        if not songs:
            return ft.Container(
                content=ft.Column([
                    ft.Text("📭 No songs yet!", size=20, text_align="center"),
                    ft.Text("Add your first song by clicking 'New Song'", text_align="center", color=ft.Colors.GREY_500)
                ], horizontal_alignment="center"),
                alignment=ft.alignment.center,
                expand=True
            )

        song_items = []
        # Sort songs based on sort_by parameter
        if sort_by == "title":
            sorted_songs = sorted(songs, key=lambda x: x.get("title", "").lower())
        elif sort_by == "artist":
            sorted_songs = sorted(songs, key=lambda x: x.get("artist", "").lower())
        else:  # recent
            sorted_songs = sorted(songs, key=lambda x: x.get("last_played", ""), reverse=True)
        
        for song in sorted_songs:
            song_items.append(self._create_song_item(song, show_artist=True, current_playlist=current_playlist))

        return ft.ListView(controls=song_items, expand=True, spacing=5)

    def _build_artist_grouped_view(self):
        """Build a view grouped by artist."""
        if not self.song_library:
            return ft.Container(
                content=ft.Column([
                    ft.Text("📭 No songs yet!", size=20, text_align="center"),
                    ft.Text("Add songs to see them grouped by artist", text_align="center", color=ft.Colors.GREY_500)
                ], horizontal_alignment="center"),
                alignment=ft.alignment.center,
                expand=True
            )

        # Group songs by artist
        artists = {}
        for song in self.song_library:
            artist = song.get("artist", "Unknown Artist").strip()
            if not artist:
                artist = "Unknown Artist"
            if artist not in artists:
                artists[artist] = []
            artists[artist].append(song)

        # Sort artists alphabetically
        sorted_artists = sorted(artists.keys(), key=str.lower)

        artist_groups = []
        for artist in sorted_artists:
            songs = sorted(artists[artist], key=lambda x: x.get("title", "").lower())
            
            # Create artist header
            artist_groups.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"🎤 {artist}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                        ft.Text(f"({len(songs)} songs)", size=12, color=ft.Colors.GREY_500)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.Colors.BLUE_50 if not self.is_dark_mode else ft.Colors.BLUE_GREY_900,
                    border_radius=8,
                    padding=12,
                    margin=ft.margin.only(top=10, bottom=5)
                )
            )
            
            # Add songs for this artist
            for song in songs:
                artist_groups.append(self._create_song_item(song, show_artist=False, current_playlist="By Artist"))

        return ft.ListView(controls=artist_groups, expand=True, spacing=2)

    def _build_playlist_view(self, playlist_name):
        """Build a playlist view."""
        song_ids = self.playlists.get(playlist_name, [])
        songs = [self._get_song_by_id(sid) for sid in song_ids if self._get_song_by_id(sid)]
        
        # Create song list
        song_list = self._build_song_list_view(songs, sort_by="title", current_playlist=playlist_name)
        
        # Add playlist management header (except for special playlists)
        if playlist_name not in ["Favorites", "All Songs", "By Artist"]:
            playlist_header = ft.Container(
                content=ft.Row([
                    ft.Text(f"🎵 {playlist_name}", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Text(f"{len(songs)} songs", size=12, color=ft.Colors.GREY_500),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color=ft.Colors.RED_400,
                            tooltip=f"Delete '{playlist_name}' playlist",
                            on_click=lambda e: self._delete_playlist_dialog(playlist_name, e.page)
                        )
                    ], spacing=10)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.all(10),
                bgcolor=ft.Colors.BLUE_50 if not self.is_dark_mode else ft.Colors.BLUE_GREY_900,
                border_radius=8,
                margin=ft.margin.only(bottom=10)
            )
            
            return ft.Column([
                playlist_header,
                ft.Container(content=song_list, expand=True)
            ], expand=True)
        
        return song_list

    def _create_song_item(self, song, show_artist=True, current_playlist=None):
        """Create a song item for the library list."""
        # Format play count and date
        play_count = song.get("play_count", 0)
        last_played = song.get("last_played")
        date_text = ""
        if last_played:
            try:
                date_obj = datetime.fromisoformat(last_played.replace('Z', '+00:00'))
                date_text = date_obj.strftime("%m/%d %H:%M")
            except:
                date_text = "Recently"

        # Song info column
        song_info = [ft.Text(song["title"], size=16, weight=ft.FontWeight.BOLD)]
        if show_artist and song["artist"]:
            song_info.append(ft.Text(song["artist"], size=12, color=ft.Colors.GREY_500))

        # Action buttons
        action_buttons = [
            ft.Text(f"♪{play_count}", size=10, color=ft.Colors.BLUE_400, tooltip=f"Played {play_count} times"),
            ft.Text(date_text, size=10, color=ft.Colors.GREY_400),
            ft.IconButton(
                icon=ft.Icons.FAVORITE if song.get("is_favorite") else ft.Icons.FAVORITE_BORDER,
                icon_color=ft.Colors.RED_400 if song.get("is_favorite") else ft.Colors.GREY_400,
                tooltip="Toggle Favorite",
                on_click=lambda e, sid=song["id"]: self._toggle_favorite_and_refresh(sid, e.page)
            ),
        ]

        # Add playlist management buttons
        if current_playlist and current_playlist != "All Songs" and current_playlist != "By Artist":
            # If viewing a specific playlist, show remove button
            action_buttons.append(
                ft.IconButton(
                    icon=ft.Icons.PLAYLIST_REMOVE,
                    icon_color=ft.Colors.ORANGE_400,
                    tooltip=f"Remove from {current_playlist}",
                    on_click=lambda e, sid=song["id"]: self._remove_song_from_playlist_dialog(sid, current_playlist, e.page)
                )
            )
        else:
            # If viewing all songs, show add to playlist button
            action_buttons.append(
                ft.IconButton(
                    icon=ft.Icons.PLAYLIST_ADD,
                    icon_color=ft.Colors.BLUE_400,
                    tooltip="Add to Playlist",
                    on_click=lambda e, sid=song["id"]: self._add_song_to_playlist_dialog(sid, e.page)
                )
            )

        # Always show play and delete buttons
        action_buttons.extend([
            ft.IconButton(
                icon=ft.Icons.PLAY_ARROW,
                icon_color=ft.Colors.GREEN_400,
                tooltip="Load Song",
                on_click=lambda e, sid=song["id"]: self._load_song(sid, e.page)
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE_OUTLINE,
                icon_color=ft.Colors.RED_400,
                tooltip="Delete Song",
                on_click=lambda e, sid=song["id"]: self._delete_song_dialog(sid, e.page)
            )
        ])

        return ft.Container(
            content=ft.Row([
                # Song info
                ft.Column(song_info, spacing=2, expand=True),
                
                # Stats and actions
                ft.Row(action_buttons, spacing=5)
            ], vertical_alignment="center"),
            bgcolor=ft.Colors.GREY_100 if not self.is_dark_mode else ft.Colors.GREY_800,
            border_radius=8,
            padding=12,
            margin=ft.margin.symmetric(vertical=2)
        )

    def _toggle_favorite_and_refresh(self, song_id, page):
        """Toggle favorite and refresh UI."""
        self._toggle_favorite(song_id)
        self._rebuild_ui(page)
        
        song = self._get_song_by_id(song_id)
        if song:
            status = "Added to" if song["is_favorite"] else "Removed from"
            self._show_message(page, f"⭐ {status} favorites: {song['title']}")

    def _delete_song_dialog(self, song_id, page):
        """Show confirmation dialog for deleting a song."""
        song = self._get_song_by_id(song_id)
        if not song:
            return
        
        def confirm_delete(e):
            self._delete_song(song_id)
            self._show_message(page, f"🗑️ Deleted: {song['title']}")
            # Close dialog first
            dialog.open = False
            if dialog in page.overlay:
                page.overlay.remove(dialog)
            # Then rebuild UI
            self._rebuild_ui(page)
        
        def cancel_delete(e):
            dialog.open = False
            if dialog in page.overlay:
                page.overlay.remove(dialog)
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Delete Song?"),
            content=ft.Text(f"Are you sure you want to delete '{song['title']}' by {song['artist']}?\n\nThis action cannot be undone."),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.ElevatedButton("Delete", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED_400))
            ]
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def _clear_library_dialog(self, e):
        """Show confirmation dialog for clearing entire library."""
        if not self.song_library:
            self._show_message(e.page, "Library is already empty!")
            return
        
        def confirm_clear(e):
            # Clear data
            self.song_library = []
            self.playlists = {"Favorites": []}
            self._save_song_library()
            self._save_playlists()
            
            # Close dialog first  
            dialog.open = False
            if dialog in e.page.overlay:
                e.page.overlay.remove(dialog)
            
            # Show message and rebuild UI
            self._show_message(e.page, "🧹 Library cleared!")
            self._rebuild_ui(e.page)
        
        def cancel_clear(e):
            dialog.open = False
            if dialog in e.page.overlay:
                e.page.overlay.remove(dialog)
            e.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Clear Entire Library?"),
            content=ft.Text(f"Are you sure you want to delete ALL {len(self.song_library)} songs?\n\nThis will also clear favorites and playlists.\nThis action cannot be undone!"),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_clear),
                ft.ElevatedButton("Clear All", on_click=confirm_clear, style=ft.ButtonStyle(color=ft.Colors.RED_400))
            ]
        )
        
        e.page.overlay.append(dialog)
        dialog.open = True
        e.page.update()

    def build_ui(self, page: ft.Page):
        """Builds and displays the UI based on the current mode."""
        page.title = "Better Lyrics"
        page.theme_mode = ft.ThemeMode.DARK if self.is_dark_mode else ft.ThemeMode.LIGHT
        page.padding = 5  # Much smaller padding so content reaches edges
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH # Stretch content horizontally
        
        # Store page reference for portal box
        self.page = page

        # Choose which UI to show
        if self.show_library:
            main_content = self._build_library_ui()
        elif self.is_preview_mode:
            main_content = self._build_preview_mode_ui()
        else:
            main_content = self._build_edit_mode_ui()

        # Navigation buttons
        nav_buttons = []
        
        # Library button (always visible)
        library_text = f"🎵 Library ({len(self.song_library)})" if self.song_library else "🎵 Library"
        nav_buttons.append(
            ft.ElevatedButton(
                library_text,
                icon=ft.Icons.LIBRARY_MUSIC,
                on_click=self.toggle_library_view,
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_100 if self.show_library else None)
            )
        )
        
        # Theme button
        self.theme_button = ft.ElevatedButton(
            "Light Mode" if self.is_dark_mode else "Dark Mode",
            icon=ft.Icons.WB_SUNNY_OUTLINED if self.is_dark_mode else ft.Icons.BRIGHTNESS_2,
            on_click=self.toggle_theme,
            style=ft.ButtonStyle(padding=15)
        )
        nav_buttons.append(self.theme_button)
        
        # Clean header with just Pro Tips (only in edit mode)
        header = ft.Row(
            [
                # Empty left space
                ft.Container(),
                # Pro Tips on the right (only in edit mode)
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("💡 Pro Tips", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                            ft.Text(
                                "• Ask AI (ChatGPT/Gemini) to organize lyrics:\n"
                                "  [Verse 1] / [Chorus] / [Verse 2]\n"
                                "• Use format: 'Title - Artist' for auto-detection\n"
                                "• Copy/paste works best (Ctrl+C → Ctrl+V)",
                                size=9,
                                color=ft.Colors.GREY_600,
                                text_align="left"
                            ),
                        ],
                        spacing=3,
                        tight=True
                    ),
                    bgcolor=ft.Colors.BLUE_50 if not self.is_dark_mode else ft.Colors.BLUE_GREY_900,
                    border_radius=6,
                    padding=8,
                    width=220,
                    border=ft.border.all(1, ft.Colors.BLUE_200 if not self.is_dark_mode else ft.Colors.BLUE_GREY_700),
                    visible=not self.is_preview_mode and not self.show_library  # Only show in edit mode
                ),
            ],
            alignment=ft.MainAxisAlignment.END,  # Align to right
            vertical_alignment=ft.CrossAxisAlignment.START
        )
        
        # Add the main content using Stack for logo overlay
        main_ui_content = ft.Column([
            header,
            ft.Container(
                content=main_content,
                expand=True,
                padding=ft.padding.only(top=100)  # Increased to clear logo overlay (80px height + 20px buffer)
            ),
            ft.Row(nav_buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ], expand=True)

        # Create logo overlay (snug to top-left)
        logo_overlay = ft.Container(
            content=ft.Image(
                src=self.logo_path,
                width=250,  # Larger size for the new colorful logo
                height=80,  # Better aspect ratio for header logo
                fit=ft.ImageFit.CONTAIN,
            ),
            left=10,   # Slightly more space from left edge
            top=10,    # Slightly more space from top edge
        )

        # Use Stack to overlay logo on top of main content
        page.add(
            ft.Stack([
                main_ui_content,  # Main content underneath
                logo_overlay,     # Logo overlay on top
            ], expand=True)
        )

    def _build_edit_mode_ui(self) -> ft.Column:
        """Builds the UI for pasting and editing lyrics."""
        self.lyrics_input = ft.TextField(
            value=self.original_lyrics,
            multiline=True,
            min_lines=15,
            hint_text="Click here to paste your lyrics, or use Ctrl+V after copying text from anywhere!",
            border_radius=10,
            border_color=ft.Colors.TRANSPARENT,
            expand=True,
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500, size=14),
            text_style=ft.TextStyle(size=14),
        )

        # Create enhanced input container
        input_container = self._create_enhanced_input_area(self.lyrics_input)

        return ft.Column(
            [
                # No Pro Tips here anymore - moved to header
                ft.Text("", size=16, color=ft.Colors.GREY_500, text_align="center"),
                ft.Row(
                    [
                        ft.ElevatedButton("📋 Paste from Clipboard", icon=ft.Icons.CONTENT_PASTE, on_click=self.paste_lyrics),
                        ft.ElevatedButton("✨ Transform Lyrics", icon=ft.Icons.AUTO_FIX_HIGH, on_click=self.transform_lyrics, autofocus=True),
                        ft.ElevatedButton("📄 Copy Lyrics", icon=ft.Icons.COPY, on_click=self.copy_lyrics),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15
                ),
                input_container,
            ],
            expand=True,
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def _build_preview_mode_ui(self) -> ft.Column:
        """Builds the UI for displaying and customizing the formatted lyrics."""
        
        # Split lyrics into lines for ListView
        lyrics_lines = self.formatted_lyrics.split('\n') if self.formatted_lyrics else [""]
        
        # Add buffer lines at the top (empty lines for smooth start)
        buffer_lines = [" "] * self.buffer_lines
        all_lines = buffer_lines + lyrics_lines
        
        # Create ListView with buffer + lyrics
        self.lyrics_display_container = ft.ListView(
            controls=[
                ft.Text(
                    line if line.strip() else " ",  # Empty lines show as space
                    size=self.font_size,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE if self.is_dark_mode else ft.Colors.BLACK,
                    text_align=self.text_alignment,
                    selectable=True,
                ) for line in all_lines
            ],
            expand=1,
            spacing=5,
            padding=ft.padding.all(15),
            auto_scroll=False,
        )
        
        # Container to hold the ListView
        lyrics_container = ft.Container(
            content=self.lyrics_display_container,
            bgcolor=ft.Colors.BLACK if self.is_dark_mode else ft.Colors.WHITE,
            border_radius=10,
            border=ft.border.all(2, ft.Colors.WHITE30 if self.is_dark_mode else ft.Colors.BLACK38),
            expand=True,
            margin=ft.margin.all(0),
        )

        return ft.Column(
            [
                # Header with current song info (logo is now overlay at bottom-right)
                ft.Row(
                    [
                        # Left spacer to push content away from logo
                        ft.Container(width=120),
                        # Centered song info
                        ft.Container(
                            content=ft.Column([
                                # Current song info
                                ft.Text(
                                    f"🎵 {self.current_song['title']} - {self.current_song['artist']}" if self.current_song else "",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_400 if self.current_song else ft.Colors.ORANGE_400,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                # Favorite indicator - centered
                                ft.Row([
                                    ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_400, size=16) if self.current_song and self.current_song.get("is_favorite") else ft.Container(),
                                    ft.Text(f"♪ Played {self.current_song.get('play_count', 0)} times" if self.current_song else "", size=12, color=ft.Colors.GREY_500)
                                ], spacing=5, alignment=ft.MainAxisAlignment.CENTER) if self.current_song else ft.Container()
                            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True
                        ),
                        # Pro tip container on the right
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("💡 Pro Tip", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                                    ft.Text(
                                        "Ask AI (ChatGPT/Gemini) to organize your lyrics:\n"
                                        "[Verse 1] / [Chorus] / [Verse 2]\n"
                                        "Much better viewing experience!",
                                        size=9,
                                        color=ft.Colors.GREY_600,
                                        text_align="left"
                                    ),
                                ],
                                spacing=3,
                                tight=True
                            ),
                            bgcolor=ft.Colors.BLUE_50 if not self.is_dark_mode else ft.Colors.BLUE_GREY_900,
                            border_radius=6,
                            padding=8,
                            width=200,
                            border=ft.border.all(1, ft.Colors.BLUE_200 if not self.is_dark_mode else ft.Colors.BLUE_GREY_700)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                lyrics_container,
                # Single row controls - Viva Video style
                ft.Row(
                    [
                        # Alignment controls
                        ft.Column([
                            ft.Text("Alignment", size=12, text_align="center"),
                            ft.Row([
                                ft.IconButton(icon=ft.Icons.FORMAT_ALIGN_LEFT, tooltip="Left", on_click=self.change_alignment, data=ft.TextAlign.LEFT, icon_size=18),
                                ft.IconButton(icon=ft.Icons.FORMAT_ALIGN_CENTER, tooltip="Center", on_click=self.change_alignment, data=ft.TextAlign.CENTER, icon_size=18),
                                ft.IconButton(icon=ft.Icons.FORMAT_ALIGN_RIGHT, tooltip="Right", on_click=self.change_alignment, data=ft.TextAlign.RIGHT, icon_size=18),
                            ], spacing=2)
                        ], horizontal_alignment="center", spacing=5),
                        
                        # Font Size
                        ft.Column([
                            ft.Text("Font Size", size=12, text_align="center"),
                            ft.Slider(min=14, max=60, value=self.font_size, divisions=46, on_change=self.change_font_size, width=120, height=30)
                        ], horizontal_alignment="center", spacing=5),
                        
                        # Buffer Lines
                        ft.Column([
                            ft.Text("Buffer Lines", size=12, text_align="center"),
                            ft.Slider(min=4, max=48, value=self.buffer_lines, divisions=44, on_change=self.change_buffer_lines, width=120, height=30)
                        ], horizontal_alignment="center", spacing=5),
                        
                        # Speed/Song Length Toggle
                        ft.Column([
                            ft.Row([
                                ft.Text("Speed" if not self.use_song_length_mode else "Song Length", size=12),
                                ft.Switch(value=self.use_song_length_mode, on_change=self.toggle_scroll_mode, scale=0.8)
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                            self._create_scroll_slider(),
                            # Disclaimer for song length mode
                            ft.Text(
                                "*Song length scroll is a concept feature" if self.use_song_length_mode else "",
                                size=8,
                                color=ft.Colors.ORANGE_300,
                                text_align="center",
                                italic=True
                            ) if self.use_song_length_mode else ft.Container()
                        ], horizontal_alignment="center", spacing=5),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    spacing=20,
                    wrap=False,
                ),
                # Action buttons row
                ft.Row(
                    [
                        ft.ElevatedButton("📄 Start New", icon=ft.Icons.REFRESH, on_click=self.start_new_transformation),
                        ft.ElevatedButton("📋 Copy Lyrics", icon=ft.Icons.COPY, on_click=self.copy_lyrics),
                        # Favorite button (always available)
                        ft.ElevatedButton(
                            "⭐ Unfavorite" if self.current_song and self.current_song.get("is_favorite") else "⭐ Favorite",
                            icon=ft.Icons.FAVORITE if self.current_song and self.current_song.get("is_favorite") else ft.Icons.FAVORITE_BORDER,
                            on_click=self._toggle_current_favorite,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_100 if self.current_song and self.current_song.get("is_favorite") else None)
                        ),
                        ft.ElevatedButton(
                            "▶️ Play" if not self.is_playing else "⏸️ Pause",
                            icon=ft.Icons.PLAY_ARROW if not self.is_playing else ft.Icons.PAUSE,
                            on_click=self.toggle_play_pause,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_100 if not self.is_dark_mode else ft.Colors.GREEN_900)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                    wrap=True
                ),
            ],
            expand=True,
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )


def main(page: ft.Page):
    """Initializes and runs the Better Lyrics application."""
    # Set window properties for clean windowed mode
    page.title = "Better Lyrics"
    page.window.icon = "betterlogo2.png"  # Custom logo icon using assets
    page.window.width = 1400  # Increased width for library view
    page.window.height = 900  # Increased height for library view
    page.window.min_width = 1200
    page.window.min_height = 800
    page.window.resizable = True
    page.window.maximizable = True
    
    app = BetterLyricsApp()
    app.build_ui(page)


if __name__ == "__main__":
    # Set up assets directory for Flet
    import os
    assets_dir = os.path.dirname(os.path.abspath(__file__))
    ft.app(target=main, assets_dir=assets_dir)
