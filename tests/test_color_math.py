import pytest
from conftest import lcms2_available
from swatchbook.color import (
    HSV2RGB, RGB2HSV,
    HSL2RGB, RGB2HSL,
    CMY2RGB, YIQ2RGB,
    XYZ2Lab, xyY2XYZ, LCH2Lab,
    sRGB_to_linear, linear_to_sRGB,
    toRGB,
    ref_XYZ,
)

# ── HSV ──────────────────────────────────────────────────────────────────────

def test_hsv_black():
    assert HSV2RGB(0, 0, 0) == pytest.approx((0, 0, 0))

def test_hsv_white():
    assert HSV2RGB(0, 0, 1) == pytest.approx((1, 1, 1))

def test_hsv_pure_red():
    assert HSV2RGB(0, 1, 1) == pytest.approx((1, 0, 0))

def test_hsv_pure_green():
    assert HSV2RGB(1/3, 1, 1) == pytest.approx((0, 1, 0), abs=1e-9)

def test_hsv_pure_blue():
    assert HSV2RGB(2/3, 1, 1) == pytest.approx((0, 0, 1), abs=1e-9)

def test_hsv_round_trip():
    for rgb in [(0.2, 0.5, 0.8), (0.9, 0.1, 0.4), (0.0, 1.0, 0.5)]:
        h, s, v = RGB2HSV(*rgb)
        assert HSV2RGB(h, s, v) == pytest.approx(rgb, abs=1e-9)

# ── HSL ──────────────────────────────────────────────────────────────────────

def test_hsl_black():
    assert HSL2RGB(0, 0, 0) == pytest.approx((0, 0, 0))

def test_hsl_white():
    assert HSL2RGB(0, 0, 1) == pytest.approx((1, 1, 1))

def test_hsl_pure_red():
    assert HSL2RGB(0, 1, 0.5) == pytest.approx((1, 0, 0))

def test_hsl_round_trip():
    for rgb in [(0.1, 0.6, 0.9), (0.8, 0.2, 0.5), (0.3, 0.3, 0.3)]:
        h, s, l = RGB2HSL(*rgb)
        assert HSL2RGB(h, s, l) == pytest.approx(rgb, abs=1e-9)

# ── CMY ───────────────────────────────────────────────────────────────────────

def test_cmy_black():
    assert CMY2RGB(1, 1, 1) == pytest.approx((0, 0, 0))

def test_cmy_white():
    assert CMY2RGB(0, 0, 0) == pytest.approx((1, 1, 1))

def test_cmy_pure_cyan():
    assert CMY2RGB(1, 0, 0) == pytest.approx((0, 1, 1))

# ── YIQ ───────────────────────────────────────────────────────────────────────

def test_yiq_white():
    r, g, b = YIQ2RGB(1, 0, 0)
    assert r == pytest.approx(1.0)
    assert g == pytest.approx(1.0)
    assert b == pytest.approx(1.0)

def test_yiq_black():
    r, g, b = YIQ2RGB(0, 0, 0)
    assert r == pytest.approx(0.0)
    assert g == pytest.approx(0.0)
    assert b == pytest.approx(0.0)

# ── XYZ / Lab ─────────────────────────────────────────────────────────────────

def test_xyz2lab_d65_white():
    X, Y, Z = ref_XYZ['2°']['D65']  # 95.047, 100, 108.883
    L, a, b = XYZ2Lab(X, Y, Z)
    assert L == pytest.approx(100.0, abs=0.001)
    assert a == pytest.approx(0.0, abs=0.001)
    assert b == pytest.approx(0.0, abs=0.001)

def test_xyz2lab_black():
    L, a, b = XYZ2Lab(0, 0, 0)
    assert L == pytest.approx(0.0, abs=0.001)

def test_xyy2xyz_d65():
    # D65 2° standard illuminant chromaticity
    x, y, Y = 0.3127, 0.3290, 100.0
    X, Yout, Z = xyY2XYZ(x, y, Y)
    ref_X, ref_Y, ref_Z = ref_XYZ['2°']['D65']
    assert X == pytest.approx(ref_X, rel=0.001)
    assert Yout == pytest.approx(ref_Y)
    assert Z == pytest.approx(ref_Z, rel=0.001)

def test_xyy2xyz_zero_y_no_error():
    # y=0 must not raise ZeroDivisionError (special Munsell palette handling)
    result = xyY2XYZ(0.1, 0, 50)
    assert len(result) == 3

# ── LCH ───────────────────────────────────────────────────────────────────────

def test_lch2lab_zero_hue():
    L, a, b = LCH2Lab(50, 50, 0)
    assert L == pytest.approx(50)
    assert a == pytest.approx(50)
    assert b == pytest.approx(0, abs=1e-9)

def test_lch2lab_90_hue():
    L, a, b = LCH2Lab(50, 50, 90)
    assert L == pytest.approx(50)
    assert a == pytest.approx(0, abs=1e-9)
    assert b == pytest.approx(50)

# ── sRGB gamma ────────────────────────────────────────────────────────────────

def test_srgb_gamma_zero():
    assert sRGB_to_linear(0) == pytest.approx(0)

def test_srgb_gamma_one():
    assert sRGB_to_linear(1) == pytest.approx(1, rel=1e-9)

def test_gamma_round_trip():
    for v in [0.0, 0.1, 0.5, 0.9, 1.0]:
        assert linear_to_sRGB(sRGB_to_linear(v)) == pytest.approx(v, abs=1e-9)

# ── toRGB dispatch ────────────────────────────────────────────────────────────

def test_to_rgb_srgb():
    result = toRGB('sRGB', [1.0, 0.0, 0.0])
    assert result == pytest.approx((1.0, 0.0, 0.0))

def test_to_rgb_rgb():
    result = toRGB('RGB', [0.0, 1.0, 0.0])
    assert result == pytest.approx((0.0, 1.0, 0.0))

def test_to_rgb_hsv():
    result = toRGB('HSV', [0, 1, 1])
    assert result == pytest.approx((1.0, 0.0, 0.0))

def test_to_rgb_hls():
    # HLS order: H, L, S
    result = toRGB('HLS', [0, 0.5, 1.0])
    assert result == pytest.approx((1.0, 0.0, 0.0))

def test_to_rgb_cmy():
    result = toRGB('CMY', [0.0, 0.0, 0.0])
    assert result == pytest.approx((1.0, 1.0, 1.0))

def test_to_rgb_gray():
    result = toRGB('GRAY', [0.0])
    assert result == pytest.approx((1.0, 1.0, 1.0))
    result = toRGB('GRAY', [1.0])
    assert result == pytest.approx((0.0, 0.0, 0.0))

@pytest.mark.skipif(not lcms2_available, reason='liblcms2 not found')
def test_to_rgb_lab_black():
    result = toRGB('Lab', [0, 0, 0])
    assert len(result) == 3
    assert all(abs(v) < 0.1 for v in result)  # should be near black

@pytest.mark.skipif(not lcms2_available, reason='liblcms2 not found')
def test_to_rgb_lab_white():
    result = toRGB('Lab', [100, 0, 0])
    assert len(result) == 3
    assert all(0.9 <= v <= 1.05 for v in result)  # should be near white

@pytest.mark.skipif(not lcms2_available, reason='liblcms2 not found')
def test_to_rgb_cmyk_white():
    result = toRGB('CMYK', [0, 0, 0, 0])
    assert len(result) == 3
    assert all(0.85 <= v <= 1.05 for v in result)  # paper white, near white

def test_to_rgb_unknown_model():
    assert toRGB('BOGUS', [1, 0, 0]) is False
