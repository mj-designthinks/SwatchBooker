import pytest
from swatchbook import SwatchBook, Color
from swatchbook.codecs import gimp_gpl, adobe_ase


@pytest.fixture(scope='module')
def loaded_sb():
    import os
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.sbz')
    return SwatchBook(file=os.path.abspath(path))


def test_book_items_non_empty(loaded_sb):
    assert len(loaded_sb.book.items) > 0


def test_all_colors_have_valid_rgb(loaded_sb):
    colors = [m for m in loaded_sb.materials.values() if isinstance(m, Color)]
    assert len(colors) > 0
    for color in colors:
        result = color.toRGB()
        assert result is not False, f"toRGB() returned False for {color.info.identifier}"
        assert len(result) == 3, f"toRGB() did not return a 3-tuple for {color.info.identifier}"


def test_write_gpl_from_sample(loaded_sb):
    data = gimp_gpl.write(loaded_sb)
    assert isinstance(data, bytes)
    assert data.startswith(b'GIMP Palette')


def test_write_ase_from_sample(loaded_sb):
    data = adobe_ase.write(loaded_sb)
    assert isinstance(data, bytes)
    assert data[:4] == b'ASEF'
