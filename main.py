"""
Better Lyrics v1.0.0
A cross-platform lyrics management app built with Python and Flet
Features: dark/light mode, auto-scroll, smart formatting, font customization
"""

import flet as ft
import time
import threading


class BetterLyricsApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Better Lyrics v1.0.0"
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.padding = 20
        self.page.window_width = 800
        self.page.window_height = 600
        
        # App state
        self.is_auto_scroll = False
        self.scroll_speed = 1.0
        self.font_size = 16
        self.is_bold = True
        self.text_alignment = ft.TextAlign.CENTER
        
        # UI components
        self.lyrics_text = ft.Text(
            value="Paste your lyrics here...",
            size=self.font_size,
            weight=ft.FontWeight.BOLD if self.is_bold else ft.FontWeight.NORMAL,
            text_align=self.text_alignment,
            selectable=True
        )
        
        self.lyrics_input = ft.TextField(
            label="Enter or paste lyrics",
            multiline=True,
            max_lines=10,
            on_change=self.on_lyrics_change
        )
        
        self.scroll_container = ft.Column(
            [self.lyrics_text],
            scroll=ft.ScrollMode.AUTO,
            height=300,
            spacing=10
        )
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI components"""
        
        # Control panel
        controls = ft.Row([
            ft.IconButton(
                icon=ft.Icons.LIGHT_MODE if self.page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE,
                tooltip="Toggle theme",
                on_click=self.toggle_theme
            ),
            ft.IconButton(
                icon=ft.Icons.PLAY_ARROW if not self.is_auto_scroll else ft.Icons.PAUSE,
                tooltip="Toggle auto-scroll",
                on_click=self.toggle_auto_scroll
            ),
            ft.IconButton(
                icon=ft.Icons.FORMAT_BOLD,
                tooltip="Toggle bold text",
                on_click=self.toggle_bold
            ),
            ft.Slider(
                min=12,
                max=24,
                value=self.font_size,
                label="Font Size: {value}",
                width=150,
                on_change=self.on_font_size_change
            ),
            ft.Slider(
                min=0.5,
                max=3.0,
                value=self.scroll_speed,
                label="Scroll Speed: {value}x",
                width=150,
                on_change=self.on_scroll_speed_change
            ),
        ], wrap=True)
        
        # Alignment controls
        alignment_controls = ft.Row([
            ft.Text("Text Alignment:"),
            ft.RadioGroup(
                content=ft.Row([
                    ft.Radio(value="left", label="Left"),
                    ft.Radio(value="center", label="Center"),
                    ft.Radio(value="right", label="Right"),
                ]),
                value="center",
                on_change=self.on_alignment_change
            )
        ])
        
        # Main layout
        self.page.add(
            ft.Text("Better Lyrics", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            controls,
            alignment_controls,
            ft.Divider(),
            self.lyrics_input,
            ft.Text("Preview:", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=self.scroll_container,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=5,
                padding=10
            )
        )
        
    def on_lyrics_change(self, e):
        """Handle lyrics text change"""
        lyrics = e.control.value
        if lyrics.strip():
            # Smart formatting: split by lines and create styled text
            lines = lyrics.split('\n')
            formatted_lines = []
            
            for line in lines:
                line = line.strip()
                if line:
                    # Add some spacing for better readability
                    formatted_lines.append(line)
                else:
                    formatted_lines.append("")
            
            formatted_text = '\n'.join(formatted_lines)
            self.lyrics_text.value = formatted_text
        else:
            self.lyrics_text.value = "Paste your lyrics here..."
        
        self.page.update()
        
    def toggle_theme(self, e):
        """Toggle between light and dark mode"""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.Icons.DARK_MODE
        self.page.update()
        
    def toggle_auto_scroll(self, e):
        """Toggle auto-scroll functionality"""
        self.is_auto_scroll = not self.is_auto_scroll
        if self.is_auto_scroll:
            e.control.icon = ft.Icons.PAUSE
            threading.Thread(target=self.auto_scroll_worker, daemon=True).start()
        else:
            e.control.icon = ft.Icons.PLAY_ARROW
        self.page.update()
        
    def auto_scroll_worker(self):
        """Worker thread for auto-scrolling"""
        while self.is_auto_scroll:
            try:
                current_scroll = self.scroll_container.scroll_position
                if current_scroll is None:
                    current_scroll = 0
                
                # Calculate scroll increment based on speed
                scroll_increment = 2 * self.scroll_speed
                new_position = current_scroll + scroll_increment
                
                self.scroll_container.scroll_to(offset=new_position, duration=100)
                self.page.update()
                
                time.sleep(0.1)
            except Exception:
                break
                
    def toggle_bold(self, e):
        """Toggle bold text formatting"""
        self.is_bold = not self.is_bold
        self.lyrics_text.weight = ft.FontWeight.BOLD if self.is_bold else ft.FontWeight.NORMAL
        self.page.update()
        
    def on_font_size_change(self, e):
        """Handle font size change"""
        self.font_size = int(e.control.value)
        self.lyrics_text.size = self.font_size
        self.page.update()
        
    def on_scroll_speed_change(self, e):
        """Handle scroll speed change"""
        self.scroll_speed = float(e.control.value)
        
    def on_alignment_change(self, e):
        """Handle text alignment change"""
        alignment_map = {
            "left": ft.TextAlign.LEFT,
            "center": ft.TextAlign.CENTER,
            "right": ft.TextAlign.RIGHT
        }
        self.text_alignment = alignment_map.get(e.control.value, ft.TextAlign.CENTER)
        self.lyrics_text.text_align = self.text_alignment
        self.page.update()


def main(page: ft.Page):
    """Main entry point for the Flet app"""
    app = BetterLyricsApp(page)


if __name__ == "__main__":
    ft.app(target=main)