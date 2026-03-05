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

> **PySide6 compatibility:** PySide6 6.10.x has a broken platform plugin loader on macOS that prevents the app from starting (`Could not find the Qt platform plugin "cocoa"`). Use **PySide6 < 6.10** (the `pyproject.toml` and `uv.lock` in this repo already enforce this — `uv sync` will install 6.9.x automatically).

**Requirements:** Python 3.10+, [uv](https://docs.astral.sh/uv/), Little CMS 2 (`liblcms2`)

### macOS (Homebrew)

```sh
brew install little-cms2 uv
git clone https://github.com/your-fork/SwatchBooker.git
cd SwatchBooker
uv sync
source .venv/bin/activate
python src/swatchbooker.pyw
```

### Linux (apt)

```sh
sudo apt install liblcms2-2
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/your-fork/SwatchBooker.git
cd SwatchBooker
uv sync
source .venv/bin/activate
python src/swatchbooker.pyw
```

### Windows

Install [Little CMS 2](https://www.littlecms.com/) and ensure `lcms2.dll` is on your `PATH`, install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
uv sync
.venv\Scripts\activate
python src/swatchbooker.pyw
```

## Development

Install dependencies including the test suite:

```sh
uv sync --extra dev
```

Run all tests:

```sh
uv run pytest
```

Run a specific test file:

```sh
uv run pytest tests/test_color_math.py -v
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
