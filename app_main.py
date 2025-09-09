#!/usr/bin/env python3
"""
Better Lyrics Mobile Android App - Simple Build
"""
import flet as ft
from better_lyrics_mobile import main as mobile_main

def main(page: ft.Page):
    """Main app function"""
    return mobile_main(page)

if __name__ == "__main__":
    # For Android APK build
    ft.app(target=main, view=ft.WEB_BROWSER, port=0)
