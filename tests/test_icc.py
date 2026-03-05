import pytest
import os
import tempfile
from swatchbook.icc import ICCprofile, BadICCprofile


def test_fogra27l_parses(fogra_icm):
    profile = ICCprofile(fogra_icm)
    assert profile.info is not None


def test_fogra27l_has_desc(fogra_icm):
    profile = ICCprofile(fogra_icm)
    assert 'desc' in profile.info
    assert len(profile.info['desc']) > 0


def test_fogra27l_class_is_4chars(fogra_icm):
    profile = ICCprofile(fogra_icm)
    assert isinstance(profile.info['class'], str)
    assert len(profile.info['class'].strip()) > 0


def test_fogra27l_space_is_cmyk(fogra_icm):
    profile = ICCprofile(fogra_icm)
    assert profile.info['space'].strip() == 'CMYK'


def test_fogra27l_version_tuple(fogra_icm):
    profile = ICCprofile(fogra_icm)
    assert isinstance(profile.info['version'], tuple)
    assert len(profile.info['version']) == 3


def test_bad_profile_empty_file(tmp_path):
    f = tmp_path / 'empty.icc'
    f.write_bytes(b'')
    with pytest.raises(BadICCprofile):
        ICCprofile(str(f))


def test_bad_profile_too_small(tmp_path):
    f = tmp_path / 'small.icc'
    f.write_bytes(b'\x00' * 10)
    with pytest.raises(BadICCprofile):
        ICCprofile(str(f))


def test_bad_profile_garbage_data(tmp_path):
    f = tmp_path / 'garbage.icc'
    # 200 bytes of non-ICC data; size field (first 4 bytes) says 200
    import struct
    size_bytes = struct.pack('>L', 200)
    # CMM signature with non-ASCII bytes to trigger rejection
    cmm = b'\xff\xfe\xfd\xfc'
    f.write_bytes(size_bytes + cmm + b'\x00' * 192)
    with pytest.raises(BadICCprofile):
        ICCprofile(str(f))
