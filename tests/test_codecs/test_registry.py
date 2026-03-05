import pytest
import swatchbook.codecs as codecs
from swatchbook.codecs import idfromvals, hex2


def test_reads_non_empty():
    assert len(codecs.reads) > 0


def test_writes_contains_expected():
    for name in ('gimp_gpl', 'adobe_ase', 'ooo_soc', 'scribus'):
        assert name in codecs.writes, f"'{name}' missing from writes"


def test_readexts_gpl():
    assert 'gpl' in codecs.readexts
    assert 'gimp_gpl' in codecs.readexts['gpl']


def test_readexts_ase():
    assert 'ase' in codecs.readexts
    assert 'adobe_ase' in codecs.readexts['ase']


def test_readexts_soc():
    assert 'soc' in codecs.readexts
    assert 'ooo_soc' in codecs.readexts['soc']


def test_idfromvals_returns_string():
    result = idfromvals([1.0, 0.0, 0.0])
    assert isinstance(result, str)
    assert len(result) > 0


def test_hex2_known_values():
    assert hex2(255) == 'ff'
    assert hex2(0) == '00'
    assert hex2(16) == '10'
    assert hex2(128) == '80'
