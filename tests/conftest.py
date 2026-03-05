import sys
import os
import pytest

# Belt-and-suspenders alongside pytest.ini pythonpath
_SRC = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, os.path.abspath(_SRC))

from swatchbook import SwatchBook, Color, SortedDict

# Detect if the lcms2 shared library loaded successfully
try:
    from swatchbook.color import cmsCreateContext
    _LCMS2_OK = True
except Exception:
    _LCMS2_OK = False

lcms2_available = _LCMS2_OK

_HERE = os.path.dirname(__file__)
_ROOT = os.path.join(_HERE, '..')


@pytest.fixture
def sample_sbz():
    return os.path.abspath(os.path.join(_ROOT, 'data', 'sample.sbz'))


@pytest.fixture
def fogra_icm():
    return os.path.abspath(os.path.join(_ROOT, 'src', 'swatchbook', 'Fogra27L.icm'))


@pytest.fixture
def sb():
    return SwatchBook()


@pytest.fixture
def red_color(sb):
    c = Color(sb)
    c.values[('RGB', False)] = [1.0, 0.0, 0.0]
    c.info.identifier = 'Red'
    sb.materials['Red'] = c
    return c
