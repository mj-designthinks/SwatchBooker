import pytest
from swatchbook import SwatchBook, Color, Swatch, Group
from swatchbook.codecs import adobe_ase


def make_rgb_swatchbook(*colors):
    """Build a SwatchBook with named sRGB Color objects."""
    sb = SwatchBook()
    for name, (r, g, b) in colors:
        c = Color(sb)
        c.values[('RGB', False)] = [r, g, b]
        c.info.identifier = name
        c.info.title = name
        sb.materials[name] = c
        sb.book.items.append(Swatch(name))
    return sb


@pytest.fixture
def rgb_sb():
    return make_rgb_swatchbook(
        ('Red',   (1.0, 0.0, 0.0)),
        ('Green', (0.0, 1.0, 0.0)),
        ('Blue',  (0.0, 0.0, 1.0)),
    )


@pytest.fixture
def ase_file(rgb_sb, tmp_path):
    f = tmp_path / 'test.ase'
    f.write_bytes(adobe_ase.write(rgb_sb))
    return str(f)


@pytest.fixture
def gpl_file(tmp_path):
    f = tmp_path / 'fake.gpl'
    f.write_bytes(b'GIMP Palette\n#\n255 0 0 Red\n')
    return str(f)


def test_ase_test_positive(ase_file):
    assert adobe_ase.test(ase_file) is True


def test_ase_test_negative(gpl_file):
    assert adobe_ase.test(gpl_file) is False


def test_ase_write_starts_with_magic(rgb_sb):
    data = adobe_ase.write(rgb_sb)
    assert data[:4] == b'ASEF'


def test_ase_write_version_bytes(rgb_sb):
    data = adobe_ase.write(rgb_sb)
    assert data[4:8] == b'\x00\x01\x00\x00'


def test_ase_round_trip_rgb(rgb_sb, tmp_path):
    out = tmp_path / 'out.ase'
    out.write_bytes(adobe_ase.write(rgb_sb))

    sb2 = SwatchBook()
    adobe_ase.read(sb2, str(out))

    assert len(sb2.materials) == 3
    for name, (r, g, b) in [('Red', (1.0, 0.0, 0.0)),
                              ('Green', (0.0, 1.0, 0.0)),
                              ('Blue', (0.0, 0.0, 1.0))]:
        mat = sb2.materials[name]
        vals = mat.values[list(mat.values.keys())[0]]
        assert vals == pytest.approx([r, g, b], abs=1e-5)


def test_ase_round_trip_cmyk(tmp_path):
    sb = SwatchBook()
    c = Color(sb)
    c.values[('CMYK', False)] = [0.1, 0.2, 0.3, 0.4]
    c.info.identifier = 'TestCMYK'
    c.info.title = 'TestCMYK'
    sb.materials['TestCMYK'] = c
    sb.book.items.append(Swatch('TestCMYK'))

    out = tmp_path / 'cmyk.ase'
    out.write_bytes(adobe_ase.write(sb))

    sb2 = SwatchBook()
    adobe_ase.read(sb2, str(out))
    mat = sb2.materials['TestCMYK']
    vals = mat.values[('CMYK', False)]
    assert vals == pytest.approx([0.1, 0.2, 0.3, 0.4], abs=1e-5)


def test_ase_group_name_preserved(tmp_path):
    sb = SwatchBook()
    g = Group()
    g.info.title = 'My Group'
    c = Color(sb)
    c.values[('RGB', False)] = [0.5, 0.5, 0.5]
    c.info.identifier = 'Gray'
    c.info.title = 'Gray'
    sb.materials['Gray'] = c
    g.items.append(Swatch('Gray'))
    sb.book.items.append(g)

    out = tmp_path / 'group.ase'
    out.write_bytes(adobe_ase.write(sb))

    sb2 = SwatchBook()
    adobe_ase.read(sb2, str(out))

    groups = [item for item in sb2.book.items if isinstance(item, Group)]
    assert any(gr.info.title == 'My Group' for gr in groups)
