import pytest
from swatchbook import SwatchBook, Color, Swatch
from swatchbook.codecs import gimp_gpl

GPL_CONTENT = (
    b'GIMP Palette\n'
    b'#\n'
    b'255   0   0\tRed\n'
    b'  0 255   0\tGreen\n'
    b'  0   0 255\tBlue\n'
)


@pytest.fixture
def gpl_file(tmp_path):
    f = tmp_path / 'test.gpl'
    f.write_bytes(GPL_CONTENT)
    return str(f)


@pytest.fixture
def ase_file(tmp_path):
    f = tmp_path / 'fake.ase'
    f.write_bytes(b'ASEF\x00\x01\x00\x00\x00\x00\x00\x00')
    return str(f)


def test_gpl_test_positive(gpl_file):
    assert gimp_gpl.test(gpl_file) is True


def test_gpl_test_negative(ase_file):
    assert gimp_gpl.test(ase_file) is False


def test_gpl_read_three_colors(gpl_file):
    sb = SwatchBook()
    gimp_gpl.read(sb, gpl_file)
    assert len(sb.materials) == 3


def test_gpl_read_color_names(gpl_file):
    sb = SwatchBook()
    gimp_gpl.read(sb, gpl_file)
    assert 'Red' in sb.materials
    assert 'Green' in sb.materials
    assert 'Blue' in sb.materials


def test_gpl_read_red_values(gpl_file):
    sb = SwatchBook()
    gimp_gpl.read(sb, gpl_file)
    red = sb.materials['Red']
    assert red.values[('RGB', False)] == pytest.approx([1.0, 0.0, 0.0], abs=1/255)


def test_gpl_write_starts_with_header():
    sb = SwatchBook()
    data = gimp_gpl.write(sb)
    assert data.startswith(b'GIMP Palette')


def test_gpl_round_trip(gpl_file, tmp_path):
    # Read original
    sb1 = SwatchBook()
    gimp_gpl.read(sb1, gpl_file)

    # Write to new file
    out = tmp_path / 'out.gpl'
    out.write_bytes(gimp_gpl.write(sb1))

    # Read back
    sb2 = SwatchBook()
    gimp_gpl.read(sb2, str(out))

    assert len(sb2.materials) == len(sb1.materials)
    for name in ('Red', 'Green', 'Blue'):
        v1 = sb1.materials[name].values[('RGB', False)]
        v2 = sb2.materials[name].values[('RGB', False)]
        assert v1 == pytest.approx(v2, abs=1/255)
