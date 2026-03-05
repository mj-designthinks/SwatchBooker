# SwatchBooker

A free/libre color swatch editor and batch converter for Linux, macOS, and Windows.

This is a fork of [olivierberten/SwatchBooker](https://github.com/olivierberten/SwatchBooker) by Olivier Berten, updated from Python 2 / Qt5 to **Python 3 / Qt6** using [Claude Code](https://claude.ai/code).

## Overview

SwatchBooker lets you open, inspect, convert, and save color palette files from virtually every major design application. It displays swatches with accurate color rendering via ICC profile support and Little CMS 2, and can fetch palettes directly from online color systems such as Pantone and Munsell.

Three entry points are provided:

| Entry point | Purpose |
|---|---|
| `src/swatchbooker.pyw` | Full GUI editor |
| `src/sbconvertor.pyw` | GUI batch converter |
| `src/sbconvert.py` | CLI batch converter |

## Installation

**Requirements:** Python 3.10+, PySide6, Pillow, Little CMS 2 (`liblcms2`)

### macOS (Homebrew)

```sh
brew install little-cms2
git clone https://github.com/your-fork/SwatchBooker.git
cd SwatchBooker
uv venv .venv
source .venv/bin/activate
uv pip install PySide6 Pillow
python src/swatchbooker.pyw
```

### Linux (apt)

```sh
sudo apt install liblcms2-2
git clone https://github.com/your-fork/SwatchBooker.git
cd SwatchBooker
python -m venv .venv
source .venv/bin/activate
pip install PySide6 Pillow
python src/swatchbooker.pyw
```

### Windows

Install [Little CMS 2](https://www.littlecms.com/) and ensure `lcms2.dll` is on your `PATH`, then:

```sh
pip install PySide6 Pillow
python src/swatchbooker.pyw
```

## Features

**Supported color models:** RGB, HSV, HSL, CMY, CMYK, nCLR, YIQ, CIE LAB, CIE LCH, CIE XYZ

**Reads color swatches from:**
- Adobe aco, acb, act, ase, acf, bcf, clr
- AutoCAD acb (unencrypted only)
- ColorSchemer cs
- Corel cpl, xml (X5)
- GIMP gpl
- ICC named color profiles
- OpenOffice.org soc
- QuarkXPress qcl (+cui)
- RAL bcs
- RIFF pal
- Scribus xml
- VivaDesigner xml
- Xara jcw

**Reads gradient swatches from:** Adobe grd/clr, GIMP ggr, OpenOffice.org sog, Scribus xml

**Reads pattern swatches from:** Adobe pat, GIMP pat, OpenOffice.org sob/soh

**Fetches online palettes from:** Munsell Renotation, Pantone (CMYK/sRGB/Lab), Digital Colour Atlas, and others

**Writes:** Adobe ase, GIMP gpl, HTML, OpenOffice.org soc, Scribus xml

**Other:** ICC color profile assignment per palette, localized swatch names and palette descriptions

## License

SwatchBooker is free software licensed under the GNU General Public License v3 or later. See `src/COPYING` for the full text.
