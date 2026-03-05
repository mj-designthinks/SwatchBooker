import pytest
import os
import tempfile
from swatchbook import (
    SwatchBook, Color, Group, Book, Swatch, Spacer, Break,
    Tint, Tone, Shade, Info, FileFormatError, SortedDict,
)


def test_info_dc_fields_default_empty():
    info = Info()
    for field in ('title', 'creator', 'description', 'identifier',
                  'publisher', 'rights', 'source', 'subject',
                  'contributor', 'coverage', 'relation', 'language', 'license'):
        assert getattr(info, field) == ""


def test_info_format_and_type():
    info = Info()
    assert info.format == 'application/swatchbook'
    assert 'purl.org/dc' in info.type


def test_swatchbook_empty_on_init():
    sb = SwatchBook()
    assert sb.materials == {}
    assert sb.book.items == []
    assert sb.profiles == {}
    assert sb.codec is False


def test_book_count_total():
    book = Book()
    book.items = [Swatch('x'), Spacer(), Break()]
    assert book.count() == 3


def test_book_count_swatches_only():
    book = Book()
    book.items = [Swatch('x'), Swatch('y'), Spacer(), Break()]
    assert book.count(swatchesonly=True) == 2


def test_group_count_simple():
    g = Group()
    g.items = [Swatch('a'), Swatch('b')]
    assert g.count(swatchesonly=True) == 2


def test_group_count_recursive():
    inner = Group()
    inner.items = [Swatch('c'), Swatch('d')]
    outer = Group()
    outer.items = [Swatch('a'), inner]
    assert outer.count(swatchesonly=True) == 3


def test_color_values_stored_and_retrieved():
    sb = SwatchBook()
    c = Color(sb)
    c.values[('sRGB', False)] = [0.5, 0.25, 0.75]
    assert c.values[('sRGB', False)] == [0.5, 0.25, 0.75]


def test_color_to_rgb8_red():
    sb = SwatchBook()
    c = Color(sb)
    c.values[('RGB', False)] = [1.0, 0.0, 0.0]
    assert c.toRGB8() == (255, 0, 0)


def test_color_to_rgb8_black():
    sb = SwatchBook()
    c = Color(sb)
    c.values[('RGB', False)] = [0.0, 0.0, 0.0]
    assert c.toRGB8() == (0, 0, 0)


def test_tint_attributes():
    t = Tint()
    assert t.color is False
    assert t.amount is False
    assert isinstance(t.info, Info)


def test_tone_attributes():
    t = Tone()
    assert t.color is False
    assert t.amount is False


def test_shade_attributes():
    s = Shade()
    assert s.color is False
    assert s.amount is False


def test_spacer_and_break_instantiate():
    sp = Spacer()
    br = Break()
    # Just verifying construction doesn't raise
    assert sp is not None
    assert br is not None


def test_swatch_stores_material_id():
    sw = Swatch('my-color')
    assert sw.material == 'my-color'


def test_swatchbook_test_detects_gpl(tmp_path):
    gpl_file = tmp_path / 'test.gpl'
    gpl_file.write_text('GIMP Palette\n#\n255   0   0 Red\n')
    sb = SwatchBook()
    result = sb.test(str(gpl_file))
    assert result == 'gimp_gpl'


def test_swatchbook_bad_file_raises(tmp_path):
    junk = tmp_path / 'bad.xyz'
    junk.write_bytes(b'NOTASWATCHFILE')
    with pytest.raises((FileFormatError, Exception)):
        SwatchBook(file=str(junk))
