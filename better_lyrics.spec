# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['better_lyrics_flet.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('better_lyrics_header_final.png', '.'),
        ('better_lyrics_header_logo.png', '.'),
        ('better_lyrics_new_header_logo.png', '.'),
        ('betterlyrics3.ico', '.'),
        ('betterlyrics3.png', '.'),
        ('betterlyricslogo.png', '.'),
    ],
    hiddenimports=['flet', 'pyperclip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Better Lyrics',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='betterlyrics3.ico'
)
