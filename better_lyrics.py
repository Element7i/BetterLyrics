import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.clipboard import Clipboard
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

kivy.require('2.0.0')

class BetterLyricsApp(App):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = True
        
    def build(self):
        self.title = "Better Lyrics"
        
        # Main layout with dark background
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Set dark background
        with main_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark gray background
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        
        def update_rect(instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size
        
        main_layout.bind(pos=update_rect, size=update_rect)
        
        # Title
        title = Label(
            text='Better Lyrics',
            font_size='32sp',
            size_hint_y=None,
            height='60dp',
            bold=True,
            color=(1, 1, 1, 1)  # White text
        )
        main_layout.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text='Paste your lyrics below to make them look great.',
            font_size='16sp',
            size_hint_y=None,
            height='40dp',
            color=(0.7, 0.7, 0.7, 1)  # Gray text
        )
        main_layout.add_widget(subtitle)
        
        # Theme toggle button
        self.theme_button = Button(
            text='Switch to Light Mode',
            size_hint_y=None,
            height='50dp',
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.theme_button.bind(on_press=self.toggle_theme)
        main_layout.add_widget(self.theme_button)
        
        # Button layout
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing=10)
        
        self.paste_button = Button(
            text='Paste from Clipboard',
            background_color=(0.2, 0.4, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.paste_button.bind(on_press=self.paste_lyrics)
        button_layout.add_widget(self.paste_button)
        
        self.preview_button = Button(
            text='Preview Formatted Lyrics',
            background_color=(0.4, 0.3, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.preview_button.bind(on_press=self.preview_lyrics)
        button_layout.add_widget(self.preview_button)
        
        self.copy_button = Button(
            text='Copy Formatted Lyrics',
            background_color=(0.4, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.copy_button.bind(on_press=self.copy_lyrics)
        button_layout.add_widget(self.copy_button)
        
        main_layout.add_widget(button_layout)
        
        # Text input (now takes up more space)
        self.lyrics_input = TextInput(
            multiline=True,
            hint_text='Paste your lyrics here...',
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            font_size='16sp'
        )
        main_layout.add_widget(self.lyrics_input)
        
        # Store references for theme switching
        self.main_layout = main_layout
        self.title_label = title
        self.subtitle_label = subtitle
        
        return main_layout
    
    def format_lyrics(self, text):
        """Format lyrics with proper structure and spacing"""
        if not text.strip():
            return text
        
        lines = text.strip().split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines but preserve intentional spacing
            if not line:
                formatted_lines.append('')
                continue
            
            # Check if this line might be a chorus/repeated section
            line_count = text.lower().count(line.lower())
            
            # Format the line
            if line_count > 2:  # Likely chorus/refrain
                formatted_lines.append(f"    {line}")  # Indent chorus
            else:
                formatted_lines.append(line)
            
            # Add spacing after what appears to be verse endings
            if i < len(lines) - 1:  # Not the last line
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                
                # Add extra spacing before chorus or after verse
                if (next_line and 
                    (text.lower().count(next_line.lower()) > 2 or  # Next line is chorus
                     len(line) > 30)):  # Current line seems like end of verse
                    formatted_lines.append('')
        
        return '\n'.join(formatted_lines)
    
    def preview_lyrics(self, instance):
        if self.lyrics_input.text.strip():
            # Format the lyrics with better structure
            formatted_text = self.format_lyrics(self.lyrics_input.text)
            
            # Create a popup with formatted lyrics
            content_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
            
            # Scrollable lyrics display
            scroll = ScrollView()
            formatted_lyrics = Label(
                text=formatted_text,
                text_size=(None, None),
                halign='left',  # Left align for better readability
                valign='top',
                font_size='22sp',  # Slightly smaller for better fitting
                bold=True,
                color=(0, 0, 0, 1),  # Black text for popup
                line_height=1.3  # Better line spacing
            )
            scroll.add_widget(formatted_lyrics)
            content_layout.add_widget(scroll)
            
            # Button layout
            button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing=10)
            
            # Copy button in popup
            copy_popup_button = Button(
                text='Copy These Lyrics',
                background_color=(0.2, 0.4, 0.2, 1),
                color=(1, 1, 1, 1)
            )
            button_layout.add_widget(copy_popup_button)
            
            # Close button
            close_button = Button(
                text='Close Preview',
                background_color=(0.4, 0.2, 0.2, 1),
                color=(1, 1, 1, 1)
            )
            button_layout.add_widget(close_button)
            
            content_layout.add_widget(button_layout)
            
            # Create popup
            popup = Popup(
                title='✨ Beautifully Formatted Lyrics',
                content=content_layout,
                size_hint=(0.85, 0.85),  # Slightly larger
                background_color=(0.98, 0.98, 0.98, 1),  # Very light background
                title_color=(0, 0, 0, 1),  # Black title
                separator_color=(0.7, 0.7, 0.7, 1)  # Gray separator
            )
            
            # Bind buttons
            close_button.bind(on_press=popup.dismiss)
            copy_popup_button.bind(on_press=lambda x: self.copy_formatted_lyrics(formatted_text, popup))
            
            # Update text size after popup opens
            def update_text_size(dt):
                formatted_lyrics.text_size = (popup.width * 0.75, None)
            Clock.schedule_once(update_text_size, 0.1)
            
            popup.open()
        else:
            self.show_message("Please enter some lyrics first!")
    
    def copy_formatted_lyrics(self, formatted_text, popup):
        """Copy the formatted lyrics and show confirmation"""
        try:
            Clipboard.copy(formatted_text)
            popup.dismiss()
            self.show_message("✨ Beautifully formatted lyrics copied!")
        except Exception as e:
            self.show_message("Could not copy to clipboard.")
    
    def on_text_change(self, instance, value):
        # Remove the automatic formatting since we're using popup now
        pass
    
    def update_text_size(self):
        # Not needed anymore since we removed the bottom display
        pass
    
    def paste_lyrics(self, instance):
        try:
            clipboard_content = Clipboard.paste()
            if clipboard_content:
                self.lyrics_input.text = clipboard_content
                self.show_message("Lyrics pasted successfully!")
            else:
                self.show_message("Clipboard is empty")
        except Exception as e:
            self.show_message("Could not paste lyrics. Please try Ctrl+V in the text area.")
    
    def copy_lyrics(self, instance):
        if self.lyrics_input.text.strip():
            clean_text = self.lyrics_input.text
            try:
                Clipboard.copy(clean_text)
                self.show_message("Lyrics copied to clipboard!")
            except Exception as e:
                self.show_message("Could not copy to clipboard.")
        else:
            self.show_message("There are no lyrics to copy.")
    
    def toggle_theme(self, instance):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.apply_dark_theme()
            self.theme_button.text = "Switch to Light Mode"
            self.show_message("Switched to Dark Mode")
        else:
            self.apply_light_theme()
            self.theme_button.text = "Switch to Dark Mode"
            self.show_message("Switched to Light Mode")
    
    def apply_dark_theme(self):
        # Update background
        with self.main_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        
        # Update text colors
        self.title_label.color = (1, 1, 1, 1)
        self.subtitle_label.color = (0.7, 0.7, 0.7, 1)
        
        # Update input colors
        self.lyrics_input.background_color = (0.2, 0.2, 0.2, 1)
        self.lyrics_input.foreground_color = (1, 1, 1, 1)
    
    def apply_light_theme(self):
        # Update background
        with self.main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light background
            Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        
        # Update text colors
        self.title_label.color = (0, 0, 0, 1)
        self.subtitle_label.color = (0.3, 0.3, 0.3, 1)
        
        # Update input colors
        self.lyrics_input.background_color = (1, 1, 1, 1)
        self.lyrics_input.foreground_color = (0, 0, 0, 1)
    
    def show_message(self, message):
        popup = Popup(
            title='Better Lyrics',
            content=Label(text=message, color=(0, 0, 0, 1)),
            size_hint=(None, None),
            size=(350, 200),
            background_color=(1, 1, 1, 1)
        )
        popup.open()
        # Auto-close after 2 seconds
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

if __name__ == '__main__':
    BetterLyricsApp().run()
