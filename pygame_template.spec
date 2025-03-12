# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ['./src/main.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[
        ('assets/sounds', 'assets/sounds'),
        ('assets/sounds/ui_sounds', 'assets/sounds/ui_sounds'),
        ('assets/fonts', 'assets/fonts'),
        ('assets/images', 'assets/images'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Pygame Pong Template',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pygame_template',
)