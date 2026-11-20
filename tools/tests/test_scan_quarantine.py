import hashlib
import json
import subprocess
import sys
from pathlib import Path
from tools.scan_quarantine import quarantine, compute_sha256

SCRIPT = Path(__file__).resolve().parents[1] / "scan_quarantine.py"


def write_file(tmp_path, name, data):
    p = tmp_path / name
    raw = data.encode("utf-8") if isinstance(data, str) else data
    p.write_bytes(raw)
    return p


def write_scan_json(tmp_path, name, level, sha256, ruleset="1.0.0", reasons=None):
    p = tmp_path / name
    payload = {
        "level": level,
        "ruleset": ruleset,
        "sha256": sha256,
        "reasons": reasons or [],
        "decoded_skipped": 0,
    }
    p.write_text(json.dumps(payload, ensure_ascii=True), encoding="utf-8")
    return p


def test_quarantine_moves_file_and_matches_sha256(tmp_path):
    content = b"quarantine target content\r\nline2\n"
    src = write_file(tmp_path, "suspicious.txt", content)
    digest = hashlib.sha256(content).hexdigest()
    scan_json = write_scan_json(tmp_path, "scan.json", "QUARANTINE", digest)
    qdir = tmp_path / "quarantine_box"
    code, info = quarantine(src, scan_json, qdir)
    assert code == 0 and info["ok"] is True and info["action"] == "quarantined"
    assert not src.exists()
    dest = qdir / "suspicious.txt"
    assert dest.exists() and dest.read_bytes() == content and compute_sha256(dest) == digest


def test_quarantine_cli_subprocess(tmp_path):
    raw = "Nội dung cần cách ly tiếng Việt 123".encode("utf-8")
    src = write_file(tmp_path, "sample.txt", raw)
    digest = hashlib.sha256(raw).hexdigest()
    scan_json = write_scan_json(tmp_path, "scan.json", "QUARANTINE", digest)
    qdir = tmp_path / "isolated"
    cmd = [sys.executable, str(SCRIPT), str(src), str(scan_json), str(qdir), "--json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["ok"] is True and data["action"] == "quarantined"
    assert not src.exists() and (qdir / "sample.txt").read_bytes() == raw


def test_quarantine_hash_mismatch_fails_and_keeps_original(tmp_path):
    content = b"actual real content"
    src = write_file(tmp_path, "tampered.txt", content)
    scan_json = write_scan_json(tmp_path, "scan.json", "QUARANTINE", "0" * 64)
    qdir = tmp_path / "quarantine_box"
    code, info = quarantine(src, scan_json, qdir)
    assert code == 2 and info["ok"] is False
    assert src.exists() and src.read_bytes() == content
    assert not (qdir / "tampered.txt").exists()
    cmd = [sys.executable, str(SCRIPT), str(src), str(scan_json), str(qdir)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 2 and src.exists() and src.read_bytes() == content


def test_quarantine_collision_fails_and_keeps_both(tmp_path):
    qdir = tmp_path / "quarantine_box"
    qdir.mkdir(parents=True, exist_ok=True)
    existing = write_file(qdir, "collision.txt", b"pre-existing file in quarantine")
    src = write_file(tmp_path, "collision.txt", b"new suspicious file")
    digest = hashlib.sha256(b"new suspicious file").hexdigest()
    scan_json = write_scan_json(tmp_path, "scan.json", "QUARANTINE", digest)
    code, info = quarantine(src, scan_json, qdir)
    assert code == 2 and info["ok"] is False
    assert src.exists() and src.read_bytes() == b"new suspicious file"
    assert existing.exists() and existing.read_bytes() == b"pre-existing file in quarantine"


def test_block_level_does_not_copy_or_move(tmp_path):
    content = b"blocked content strictly blocked"
    src = write_file(tmp_path, "blocked.txt", content)
    scan_json = write_scan_json(tmp_path, "scan.json", "BLOCK", hashlib.sha256(content).hexdigest())
    qdir = tmp_path / "quarantine_box"
    code, info = quarantine(src, scan_json, qdir)
    assert code == 0 and info["action"] == "none"
    assert src.exists() and src.read_bytes() == content
    assert not (qdir / "blocked.txt").exists() and not qdir.exists()


def test_allow_and_warn_levels_do_not_touch_file(tmp_path):
    for level in ("ALLOW", "WARN"):
        content = f"content for {level}".encode("utf-8")
        src = write_file(tmp_path, f"{level.lower()}.txt", content)
        scan_json = write_scan_json(tmp_path, f"{level.lower()}.json", level, hashlib.sha256(content).hexdigest())
        qdir = tmp_path / f"qdir_{level.lower()}"
        code, info = quarantine(src, scan_json, qdir)
        assert code == 0 and info["action"] == "none" and info["level"] == level
        assert src.exists() and src.read_bytes() == content and not qdir.exists()


def test_quarantine_error_conditions(tmp_path):
    v_file = write_file(tmp_path, "v.txt", b"data")
    v_json = write_scan_json(tmp_path, "v.json", "QUARANTINE", hashlib.sha256(b"data").hexdigest())
    qdir = tmp_path / "qdir"
    bad_cases = [
        (tmp_path / "missing.txt", v_json, qdir),
        (v_file, tmp_path / "missing.json", qdir),
        (v_file, write_file(tmp_path, "c.json", b"{bad"), qdir),
        (v_file, write_file(tmp_path, "i.json", json.dumps({"level": "QUARANTINE"})), qdir),
        (v_file, write_file(tmp_path, "u.json", json.dumps({"level": "UNK", "sha256": "x"})), qdir),
        (v_file, v_json, write_file(tmp_path, "f.txt", b"x")),
    ]
    for s, j, q in bad_cases:
        assert quarantine(s, j, q)[0] == 2
    assert subprocess.run([sys.executable, str(SCRIPT)], capture_output=True).returncode == 2
