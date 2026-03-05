#!/usr/bin/env bash
# build-macos.sh — Build SwatchBooker.dmg for macOS
#
# Requirements:
#   brew install create-dmg little-cms2 uv gettext librsvg
#   uv sync (or uv sync --extra dev)
#   uv pip install pyinstaller
#
# Run from the repo root:
#   bash packaging/build-macos.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "==> Compiling translations (.po → .mo)"
for po in translations/*.po; do
    mo="${po%.po}.mo"
    msgfmt -o "$mo" "$po"
    echo "    $po → $mo"
done

echo "==> Generating macOS icon (.icns) from SVG"
# Requires Inkscape or rsvg-convert for SVG → PNG, then iconutil for .icns
# If you already have data/swatchbooker.icns, skip this block.
ICONSET="data/swatchbooker.iconset"
mkdir -p "$ICONSET"
for size in 16 32 128 256 512; do
    rsvg-convert -w $size -h $size data/swatchbooker.svg -o "$ICONSET/icon_${size}x${size}.png"
    rsvg-convert -w $((size*2)) -h $((size*2)) data/swatchbooker.svg -o "$ICONSET/icon_${size}x${size}@2x.png"
done
iconutil -c icns "$ICONSET" -o data/swatchbooker.icns
rm -rf "$ICONSET"
echo "    data/swatchbooker.icns created"

echo "==> Running PyInstaller"
pyinstaller packaging/swatchbooker.spec --noconfirm

echo "==> Building DMG"
# Stage the .app into a clean folder for create-dmg
rm -rf dist/dmg-stage
mkdir dist/dmg-stage
cp -r dist/SwatchBooker.app dist/dmg-stage/

create-dmg \
    --volname "SwatchBooker" \
    --volicon "data/swatchbooker.icns" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "SwatchBooker.app" 150 185 \
    --hide-extension "SwatchBooker.app" \
    --app-drop-link 450 185 \
    "dist/SwatchBooker.dmg" \
    "dist/dmg-stage/"

rm -rf dist/dmg-stage

echo ""
echo "Done: dist/SwatchBooker.dmg"
echo ""
echo "Smoke test:"
echo "  1. Mount SwatchBooker.dmg"
echo "  2. Drag SwatchBooker.app to Applications"
echo "  3. Launch SwatchBooker"
echo "  4. File > Open > data/sample.sbz — verify CMYK swatch renders"
