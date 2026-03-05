"""
Regression tests for msgfmt.py Python 3 compatibility and translation files.

The tobytes() fix (replacing the removed array.tostring()) is covered by
test_msgfmt_produces_bytes — if that method regresses the test fails
immediately with AttributeError before any .mo file is produced.
"""
import importlib.util
import struct
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TRANSLATIONS_DIR = REPO_ROOT / "translations"

# Minimal valid .po file with one translated string
MINIMAL_PO = b"""\
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

msgid "Hello"
msgstr "Hallo"
"""


def _load_msgfmt():
    """Import msgfmt.py from the repo root without polluting sys.modules."""
    spec = importlib.util.spec_from_file_location("msgfmt", REPO_ROOT / "msgfmt.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_msgfmt_produces_bytes(tmp_path):
    """msgfmt.generate() must return bytes (regression for tobytes() fix)."""
    msgfmt = _load_msgfmt()

    po_file = tmp_path / "test.po"
    po_file.write_bytes(MINIMAL_PO)

    mo_file = tmp_path / "test.mo"
    msgfmt.make(str(po_file), str(mo_file))

    result = mo_file.read_bytes()
    assert isinstance(result, bytes), "msgfmt output must be bytes"


def test_msgfmt_mo_magic_number(tmp_path):
    """Compiled .mo file must start with the GNU MO magic number."""
    msgfmt = _load_msgfmt()

    po_file = tmp_path / "test.po"
    po_file.write_bytes(MINIMAL_PO)
    mo_file = tmp_path / "test.mo"
    msgfmt.make(str(po_file), str(mo_file))

    magic = struct.unpack("<I", mo_file.read_bytes()[:4])[0]
    assert magic == 0x950412DE, f"Unexpected MO magic: {magic:#010x}"


def test_all_po_files_compile(tmp_path):
    """Every .po file in translations/ must compile without error."""
    msgfmt = _load_msgfmt()

    po_files = sorted(TRANSLATIONS_DIR.glob("*.po"))
    assert len(po_files) > 0, "No .po files found in translations/"

    for po_file in po_files:
        mo_file = tmp_path / f"{po_file.stem}.mo"
        msgfmt.make(str(po_file), str(mo_file))
        assert mo_file.exists(), f"{po_file.name} did not produce a .mo file"
        assert mo_file.stat().st_size > 0, f"{po_file.name} produced an empty .mo"
