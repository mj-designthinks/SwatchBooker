# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec for SwatchBooker (main GUI editor)
#
# Usage:
#   pyinstaller packaging/swatchbooker.spec
#
# Pre-requisites:
#   1. Run `python msgfmt.py` (or build-macos.sh / build-windows.bat) to
#      compile translations/*.po → translations/*.mo.
#   2. On macOS, convert data/swatchbooker.svg → data/swatchbooker.icns
#      before building (see build-macos.sh for the iconutil commands).
#   3. On Windows, liblcms2.dll must be present in the repo root or on PATH.

import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all codec and web-service submodules (dynamically imported at runtime)
hidden = (
    collect_submodules('swatchbook.codecs')
    + collect_submodules('swatchbook.websvc')
)

a = Analysis(
    ['../src/swatchbooker.pyw'],
    pathex=['../src'],
    binaries=[],
    datas=[
        # ICC profile used for CMYK rendering
        ('../src/swatchbook/Fogra27L.icm', 'swatchbook'),
        # Compiled translation catalogues (must be built before packaging)
        ('../translations', 'translations'),
        # Web-service icons
        *collect_data_files('swatchbook.websvc'),
    ],
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SwatchBooker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,         # GUI app — no terminal window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../data/swatchbooker.ico',   # Windows; macOS uses BUNDLE below
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SwatchBooker',
)

# macOS .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='SwatchBooker.app',
        icon='../data/swatchbooker.icns',   # generate from SVG before building
        bundle_identifier='org.swatchbooker.SwatchBooker',
        info_plist={
            'NSHighResolutionCapable': True,
            'CFBundleShortVersionString': '0.8',
        },
    )
