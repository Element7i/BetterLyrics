#!/usr/bin/env python3
"""
Main entry point for Better Lyrics Mobile Android App
"""
import flet as ft
from better_lyrics_mobile import main

def app_main(page: ft.Page):
    """Main app function that calls the mobile implementation"""
    return main(page)

if __name__ == "__main__":
    # Run the mobile app
    ft.app(target=app_main, port=8080, host="0.0.0.0")
