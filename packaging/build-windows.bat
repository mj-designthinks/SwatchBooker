@echo off
REM build-windows.bat - Build SwatchBooker-Setup.exe for Windows
REM
REM Requirements:
REM   - Python 3.10+ and uv installed and on PATH
REM   - liblcms2.dll present in the repo root (or on PATH)
REM     Obtain from: https://www.littlecms.com/ or GIMP's Windows distribution
REM   - Inno Setup 6 installed at default location
REM   - rsvg-convert or another SVG converter if you need to regenerate the icon
REM
REM Run from the repo root:
REM   packaging\build-windows.bat

setlocal enabledelayedexpansion

cd /d "%~dp0.."

echo =^> Compiling translations (.po -^> .mo)
for %%f in (translations\*.po) do (
    set "po=%%f"
    set "mo=%%~dpnf.mo"
    python msgfmt.py -o "!mo!" "!po!"
    echo     %%f -^> !mo!
)

echo =^> Checking for liblcms2.dll
if not exist liblcms2.dll (
    echo WARNING: liblcms2.dll not found in repo root.
    echo          Copy it here from LittleCMS or GIMP before distributing.
    echo          Continuing build - the app will NOT render CMYK without it.
)

echo =^> Running PyInstaller
pyinstaller packaging\swatchbooker.spec --noconfirm

echo =^> Running Inno Setup
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %ISCC% (
    set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"
)
%ISCC% packaging\swatchbooker.iss

echo.
echo Done: dist\SwatchBooker-Setup.exe
echo.
echo Smoke test:
echo   1. Run dist\SwatchBooker-Setup.exe on a clean machine ^(no Python^)
echo   2. Launch SwatchBooker from Start Menu
echo   3. File ^> Open ^> data\sample.sbz - verify CMYK swatch renders
