import pytest
import xml.etree.ElementTree as ET
from swatchbook import SwatchBook, Color, Swatch
from swatchbook.codecs import ooo_soc

SOC_CONTENT = (
    b'<?xml version="1.0" encoding="UTF-8"?>'
    b'<office:color-table'
    b'  xmlns:office="http://openoffice.org/2000/office"'
    b'  xmlns:draw="http://openoffice.org/2000/drawing">'
    b'<draw:color draw:name="Red" draw:color="#ff0000"/>'
    b'<draw:color draw:name="Green" draw:color="#00ff00"/>'
    b'<draw:color draw:name="Blue" draw:color="#0000ff"/>'
    b'</office:color-table>'
)


@pytest.fixture
def soc_file(tmp_path):
    f = tmp_path / 'test.soc'
    f.write_bytes(SOC_CONTENT)
    return str(f)


@pytest.fixture
def gpl_file(tmp_path):
    f = tmp_path / 'fake.gpl'
    f.write_bytes(b'GIMP Palette\n#\n255 0 0 Red\n')
    return str(f)


def test_soc_test_positive(soc_file):
    assert ooo_soc.test(soc_file) is True


def test_soc_test_negative(gpl_file):
    assert not ooo_soc.test(gpl_file)


def test_soc_read_three_colors(soc_file):
    sb = SwatchBook()
    ooo_soc.read(sb, soc_file)
    assert len(sb.materials) == 3


def test_soc_write_is_valid_xml():
    sb = SwatchBook()
    c = Color(sb)
    c.values[('RGB', False)] = [1.0, 0.0, 0.0]
    c.info.identifier = 'Red'
    c.info.title = 'Red'
    sb.materials['Red'] = c
    sb.book.items.append(Swatch('Red'))

    data = ooo_soc.write(sb)
    assert isinstance(data, bytes)
    root = ET.fromstring(data)
    assert root is not None


def test_soc_round_trip(soc_file, tmp_path):
    sb1 = SwatchBook()
    ooo_soc.read(sb1, soc_file)

    out = tmp_path / 'out.soc'
    out.write_bytes(ooo_soc.write(sb1))

    sb2 = SwatchBook()
    ooo_soc.read(sb2, str(out))

    assert len(sb2.materials) == len(sb1.materials)
    for name in sb1.materials:
        v1 = sb1.materials[name].toRGB8()
        v2 = sb2.materials[name].toRGB8()
        assert v1 == v2
