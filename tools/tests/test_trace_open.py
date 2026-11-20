import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_storage_freeze import MANIFEST_PATH, head_blobs

ROOT = Path(__file__).resolve().parents[2]
RFC_PATH = ROOT / "harness" / "rfc" / "RFC-0001_trace-attribution.md"
GRAMMAR = (
    "harness/schemas/LOG_GRAMMAR.md",
    "harness/schemas/POINTER_GRAMMAR.md",
)


def status_cell(text):
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) >= 3 and cells[1] == "Trạng thái":
            return cells[2]
    raise AssertionError("missing status")


def test_rfc_0001_remains_open():
    cell = status_cell(RFC_PATH.read_text(encoding="utf-8"))
    assert "`OPEN`" in cell
    assert "ACCEPTED" not in cell
    assert "REJECTED" not in cell


def test_log_and_pointer_grammar_blobs_match_manifest():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    blobs = head_blobs(ROOT)
    for path in GRAMMAR:
        assert blobs[path] == manifest[path]
