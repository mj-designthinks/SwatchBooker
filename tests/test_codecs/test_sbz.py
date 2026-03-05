import pytest
from swatchbook import SwatchBook
from swatchbook.codecs import sbz


def test_sbz_test_positive(sample_sbz):
    assert sbz.test(sample_sbz) is True


def test_sbz_test_negative_on_gpl(tmp_path):
    f = tmp_path / 'fake.gpl'
    f.write_bytes(b'GIMP Palette\n#\n255 0 0 Red\n')
    assert sbz.test(str(f)) is False


def test_sbz_read_materials_non_empty(sample_sbz):
    sb = SwatchBook(file=sample_sbz)
    assert len(sb.materials) > 0


def test_sbz_has_title(sample_sbz):
    sb = SwatchBook(file=sample_sbz)
    assert sb.info.title != ''


def test_sbz_book_has_items(sample_sbz):
    sb = SwatchBook(file=sample_sbz)
    assert len(sb.book.items) > 0
