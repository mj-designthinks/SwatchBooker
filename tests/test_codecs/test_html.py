"""Tests for the HTML write codec (swatchbook.codecs.html)."""
import pytest
from swatchbook import SwatchBook, Color, Swatch
from swatchbook.codecs import html


@pytest.fixture
def simple_sb():
    sb = SwatchBook()
    color = Color(sb)
    color.values[('RGB', False)] = [1.0, 0.0, 0.0]
    color.info.identifier = "red"
    color.info.title = "Red"
    sb.materials["red"] = color
    sb.book.items.append(Swatch("red"))
    return sb


def test_html_write_returns_bytes(simple_sb):
    result = html.write(simple_sb)
    assert isinstance(result, bytes)


def test_html_write_starts_with_doctype(simple_sb):
    result = html.write(simple_sb)
    assert b"<html" in result[:200]


def test_html_write_contains_color_hex(simple_sb):
    result = html.write(simple_sb)
    # Pure red in hex
    assert b"ff0000" in result.lower()
