# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller spec for sbconvertor (GUI batch converter)
#
# Usage:
#   pyinstaller packaging/sbconvertor.spec

import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hidden = (
    collect_submodules('swatchbook.codecs')
    + collect_submodules('swatchbook.websvc')
)

a = Analysis(
    ['../src/sbconvertor.pyw'],
    pathex=['../src'],
    binaries=[],
    datas=[
        ('../src/swatchbook/Fogra27L.icm', 'swatchbook'),
        ('../translations', 'translations'),
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
    name='SBConvertor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../data/swatchbooker.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SBConvertor',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='SBConvertor.app',
        icon='../data/swatchbooker.icns',
        bundle_identifier='org.swatchbooker.SBConvertor',
        info_plist={
            'NSHighResolutionCapable': True,
            'CFBundleShortVersionString': '0.8',
        },
    )
