import hashlib
import json
import subprocess
import sys
from pathlib import Path
from tools.scan_wrap import wrap, wrap_bytes, unwrap, unwrap_bytes, CLOSING_TAG

SCRIPT = Path(__file__).resolve().parents[1] / "scan_wrap.py"


def test_wrap_closing_tag_count_zero():
    data = b"Plain clean content without any closing marker."
    wrapped = wrap_bytes(data, source="clean.txt", scan="ALLOW", ruleset="1.0.0")
    assert b'closing_tag_count="0"' in wrapped
    attrs, body = unwrap_bytes(wrapped)
    assert attrs["closing_tag_count"] == "0"
    assert attrs["scan"] == "ALLOW"
    assert attrs["ruleset"] == "1.0.0"
    assert attrs["sha256"] == hashlib.sha256(data).hexdigest()
    assert body == data


def test_wrap_closing_tag_count_one():
    data = b"Before tag </EXTERNAL_DATA> after tag."
    wrapped = wrap_bytes(data, source="fake.txt", scan="WARN", ruleset="1.0.0")
    assert b'closing_tag_count="1"' in wrapped
    assert wrapped.count(CLOSING_TAG) == 2
    attrs, body = unwrap_bytes(wrapped)
    assert attrs["closing_tag_count"] == "1"
    assert body == data


def test_wrap_closing_tag_count_multiple():
    data = b"</EXTERNAL_DATA> first </EXTERNAL_DATA> second </EXTERNAL_DATA> third </EXTERNAL_DATA>"
    wrapped = wrap_bytes(data, source="multi.txt", scan="BLOCK", ruleset="1.0.0")
    assert b'closing_tag_count="4"' in wrapped
    assert wrapped.count(CLOSING_TAG) == 5
    attrs, body = unwrap_bytes(wrapped)
    assert attrs["closing_tag_count"] == "4"
    assert body == data


def test_wrap_preserves_crlf_byte_for_byte():
    data = b"line1\r\nline2\r\nline3\r\n"
    wrapped = wrap_bytes(data, source="crlf.txt")
    attrs, body = unwrap_bytes(wrapped)
    assert body == data
    assert b"\r\n" in body
    assert body.count(b"\r\n") == 3


def test_wrap_preserves_non_ascii_and_binary():
    text_data = "Dữ liệu tiếng Việt có dấu: Ứ, Ắ, Ộ và biểu tượng 🎉".encode("utf-8")
    wrapped_text = wrap_bytes(text_data, source="vietnamese.txt")
    _, body_text = unwrap_bytes(wrapped_text)
    assert body_text == text_data

    binary_data = bytes(range(256))
    wrapped_bin = wrap_bytes(binary_data, source="binary.bin")
    _, body_bin = unwrap_bytes(wrapped_bin)
    assert body_bin == binary_data


def test_wrap_escapes_attributes_and_does_not_escape_body():
    source_val = 'external "injection" > test < & done'
    body_val = b'<div class="box">raw content > here & there</div>'
    wrapped = wrap_bytes(body_val, source=source_val, scan="ALLOW", ruleset="1.0.0")
    assert b'source="external &quot;injection&quot; &gt; test &lt; &amp; done"' in wrapped
    assert body_val in wrapped
    assert b'&quot;box&quot;' not in wrapped
    attrs, body = unwrap_bytes(wrapped)
    assert attrs["source"] == source_val
    assert body == body_val


def test_wrap_str_interface():
    text = "Hello world\r\nSecond line"
    wrapped = wrap(text, source="doc.txt", scan="ALLOW", ruleset="1.0.0")
    assert isinstance(wrapped, str)
    attrs, body = unwrap(wrapped)
    assert isinstance(body, str)
    assert body == text
    assert attrs["closing_tag_count"] == "0"


def test_wrap_cli_with_file_and_scan_json(tmp_path):
    content = b"CLI test input content\r\n"
    in_file = tmp_path / "input.txt"
    in_file.write_bytes(content)
    scan_payload = {"level": "QUARANTINE", "ruleset": "2.1.0", "sha256": "fake"}
    scan_file = tmp_path / "scan.json"
    scan_file.write_text(json.dumps(scan_payload), encoding="utf-8")
    out_file = tmp_path / "out.txt"
    cmd = [sys.executable, str(SCRIPT), str(in_file), "--scan-json", str(scan_file), "--out", str(out_file)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert out_file.exists()
    attrs, body = unwrap_bytes(out_file.read_bytes())
    assert attrs["scan"] == "QUARANTINE" and attrs["ruleset"] == "2.1.0"
    assert body == content


def test_wrap_cli_stdout_and_json(tmp_path):
    content = b"stdout test"
    in_file = tmp_path / "test.txt"
    in_file.write_bytes(content)
    cmd_stdout = [sys.executable, str(SCRIPT), str(in_file), "--source", "custom_src"]
    res_stdout = subprocess.run(cmd_stdout, capture_output=True)
    assert res_stdout.returncode == 0
    attrs, body = unwrap_bytes(res_stdout.stdout)
    assert attrs["source"] == "custom_src" and body == content

    cmd_json = [sys.executable, str(SCRIPT), str(in_file), "--json"]
    res_json = subprocess.run(cmd_json, capture_output=True, text=True)
    assert res_json.returncode == 0
    assert json.loads(res_json.stdout)["ok"] is True

    cmd_missing = [sys.executable, str(SCRIPT), str(tmp_path / "nonexistent.txt")]
    res_missing = subprocess.run(cmd_missing, capture_output=True)
    assert res_missing.returncode == 2
