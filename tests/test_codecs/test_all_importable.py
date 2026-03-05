"""
Verify every codec and websvc submodule can be imported without error.

This catches module-level syntax errors and missing imports in any codec,
which would silently break runtime discovery via `from swatchbook.codecs import *`.
"""
import importlib

import pytest

CODEC_MODULES = [
    "swatchbook.codecs.adobe_acb",
    "swatchbook.codecs.adobe_acf",
    "swatchbook.codecs.adobe_aco",
    "swatchbook.codecs.adobe_act",
    "swatchbook.codecs.adobe_ase",
    "swatchbook.codecs.adobe_bcf",
    "swatchbook.codecs.adobe_clr",
    "swatchbook.codecs.adobe_grd",
    "swatchbook.codecs.adobe_pat",
    "swatchbook.codecs.autocad_acb",
    "swatchbook.codecs.colorschemer",
    "swatchbook.codecs.corel_cpl",
    "swatchbook.codecs.corel_xml",
    "swatchbook.codecs.gimp_ggr",
    "swatchbook.codecs.gimp_gpl",
    "swatchbook.codecs.gimp_pat_PIL",
    "swatchbook.codecs.html",
    "swatchbook.codecs.icc_nmcl",
    "swatchbook.codecs.ooo_sob",
    "swatchbook.codecs.ooo_soc",
    "swatchbook.codecs.ooo_sog",
    "swatchbook.codecs.quark_qcl",
    "swatchbook.codecs.ral_bcs",
    "swatchbook.codecs.riff_pal",
    "swatchbook.codecs.sbz",
    "swatchbook.codecs.scribus",
    "swatchbook.codecs.viva_xml",
    "swatchbook.codecs.xara_jcw",
    "swatchbook.websvc.dtpstudio",
    "swatchbook.websvc.munsell",
    "swatchbook.websvc.pantone",
]


@pytest.mark.parametrize("module_name", CODEC_MODULES)
def test_module_importable(module_name):
    mod = importlib.import_module(module_name)
    assert mod is not None
