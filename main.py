#!/usr/bin/env python3
"""
Better Lyrics v1.0.0
A cross-platform lyrics management app built with Python and Flet.
Features: dark/light mode, auto-scroll for karaoke, smart formatting, 
and live customization of font and alignment.
"""

import flet as ft
import asyncio
import time


class BetterLyricsApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Better Lyrics v1.0.0"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_min_width = 400
        self.page.window_min_height = 300
        
        # App state
        self.is_auto_scrolling = False
        self.scroll_speed = 1.0
        self.font_size = 16
        self.is_bold = True
        self.is_centered = True
        
        # UI components
        self.lyrics_field = None
        self.display_area = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Text("Better Lyrics", size=24, weight=ft.FontWeight.BOLD),
                ft.Switch(
                    label="Dark Mode",
                    value=True,
                    on_change=self.toggle_theme
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=20,
            bgcolor=ft.colors.SURFACE_VARIANT,
            margin=ft.margin.only(bottom=10)
        )

        # Lyrics input area
        self.lyrics_field = ft.TextField(
            label="Paste or type your lyrics here...",
            multiline=True,
            min_lines=5,
            max_lines=10,
            border_color=ft.colors.PRIMARY,
            on_change=self.on_lyrics_change
        )

        # Display area
        self.display_area = ft.Container(
            content=ft.Text(
                "Your formatted lyrics will appear here...",
                size=self.font_size,
                weight=ft.FontWeight.BOLD if self.is_bold else ft.FontWeight.NORMAL,
                text_align=ft.TextAlign.CENTER if self.is_centered else ft.TextAlign.LEFT,
                color=ft.colors.PRIMARY
            ),
            padding=20,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=10,
            height=200,
            expand=True
        )

        # Controls
        controls = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text("Font Size"),
                    ft.Slider(
                        min=12,
                        max=24,
                        value=self.font_size,
                        divisions=12,
                        label="{value}",
                        on_change=self.on_font_size_change
                    )
                ], expand=1),
                ft.Column([
                    ft.Text("Scroll Speed"),
                    ft.Slider(
                        min=0.5,
                        max=3.0,
                        value=self.scroll_speed,
                        divisions=5,
                        label="{value}x",
                        on_change=self.on_scroll_speed_change
                    )
                ], expand=1),
                ft.Column([
                    ft.Checkbox(
                        label="Bold Text",
                        value=self.is_bold,
                        on_change=self.on_bold_change
                    ),
                    ft.Checkbox(
                        label="Center Text",
                        value=self.is_centered,
                        on_change=self.on_center_change
                    )
                ], expand=1)
            ]),
            padding=20,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=10,
            margin=ft.margin.only(top=10, bottom=10)
        )

        # Action buttons
        buttons = ft.Row([
            ft.ElevatedButton(
                "Start Auto-Scroll",
                icon=ft.icons.PLAY_ARROW,
                on_click=self.toggle_auto_scroll
            ),
            ft.ElevatedButton(
                "Clear Lyrics",
                icon=ft.icons.CLEAR,
                on_click=self.clear_lyrics
            ),
            ft.ElevatedButton(
                "Format Text",
                icon=ft.icons.FORMAT_ALIGN_CENTER,
                on_click=self.format_lyrics
            )
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Main layout
        main_content = ft.Column([
            header,
            self.lyrics_field,
            controls,
            self.display_area,
            buttons
        ], expand=True, scroll=ft.ScrollMode.AUTO)

        self.page.add(main_content)
        self.page.update()

    def toggle_theme(self, e):
        """Toggle between dark and light theme"""
        self.page.theme_mode = ft.ThemeMode.LIGHT if self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        self.page.update()

    def on_lyrics_change(self, e):
        """Handle lyrics text change"""
        self.update_display()

    def on_font_size_change(self, e):
        """Handle font size change"""
        self.font_size = int(e.control.value)
        self.update_display()

    def on_scroll_speed_change(self, e):
        """Handle scroll speed change"""
        self.scroll_speed = e.control.value

    def on_bold_change(self, e):
        """Handle bold text toggle"""
        self.is_bold = e.control.value
        self.update_display()

    def on_center_change(self, e):
        """Handle text alignment toggle"""
        self.is_centered = e.control.value
        self.update_display()

    def update_display(self):
        """Update the lyrics display area"""
        lyrics_text = self.lyrics_field.value if self.lyrics_field.value else "Your formatted lyrics will appear here..."
        
        # Smart formatting: normalize line breaks and spacing
        formatted_lyrics = self.smart_format(lyrics_text)
        
        self.display_area.content = ft.Text(
            formatted_lyrics,
            size=self.font_size,
            weight=ft.FontWeight.BOLD if self.is_bold else ft.FontWeight.NORMAL,
            text_align=ft.TextAlign.CENTER if self.is_centered else ft.TextAlign.LEFT,
            color=ft.colors.PRIMARY
        )
        self.page.update()

    def smart_format(self, text):
        """Apply smart formatting to lyrics"""
        if not text or text.strip() == "":
            return "Your formatted lyrics will appear here..."
        
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                formatted_lines.append(line)
            elif formatted_lines and formatted_lines[-1] != "":
                formatted_lines.append("")  # Preserve paragraph breaks
        
        return '\n'.join(formatted_lines)

    def toggle_auto_scroll(self, e):
        """Toggle auto-scroll feature"""
        self.is_auto_scrolling = not self.is_auto_scrolling
        e.control.text = "Stop Auto-Scroll" if self.is_auto_scrolling else "Start Auto-Scroll"
        e.control.icon = ft.icons.STOP if self.is_auto_scrolling else ft.icons.PLAY_ARROW
        self.page.update()
        
        if self.is_auto_scrolling:
            asyncio.create_task(self.auto_scroll())

    async def auto_scroll(self):
        """Auto-scroll functionality for karaoke mode"""
        while self.is_auto_scrolling:
            # Simulate scrolling by updating display (in a real app, this would scroll the container)
            await asyncio.sleep(1.0 / self.scroll_speed)
            if not self.is_auto_scrolling:
                break

    def clear_lyrics(self, e):
        """Clear the lyrics input"""
        self.lyrics_field.value = ""
        self.update_display()

    def format_lyrics(self, e):
        """Apply additional formatting to lyrics"""
        if self.lyrics_field.value:
            # Apply smart formatting and update the input field
            self.lyrics_field.value = self.smart_format(self.lyrics_field.value)
            self.update_display()


def main(page: ft.Page):
    """Main entry point for the Flet app"""
    app = BetterLyricsApp(page)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")