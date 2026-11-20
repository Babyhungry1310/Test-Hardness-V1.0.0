import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "tools" / "tests" / "data" / "freeze_manifest.json"


def load_manifest(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not data:
        raise ValueError("manifest")
    if {"note", "comment", "_comment"} & set(data):
        raise ValueError("comment")
    return data


def head_blobs(repo):
    result = subprocess.run(
        ["git", "ls-tree", "-r", "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    blobs = {}
    for line in result.stdout.splitlines():
        meta, path = line.split("\t", 1)
        _mode, kind, blob = meta.split(" ")
        if kind == "blob":
            blobs[path] = blob
    return blobs


def freeze_mismatches(manifest, blobs):
    return [path for path in sorted(manifest) if blobs.get(path) != manifest[path]]


def git(repo, *args):
    return subprocess.run(
        ["git", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_manifest_maps_paths_to_blobs():
    manifest = load_manifest(MANIFEST_PATH)
    assert len(manifest) == 50
    for path, blob in manifest.items():
        assert path
        assert len(blob) == 40 and all(char in "0123456789abcdef" for char in blob)


def test_head_blobs_match_manifest():
    blobs = head_blobs(ROOT)
    blobs["tools/not-frozen.txt"] = "a" * 40
    assert freeze_mismatches(load_manifest(MANIFEST_PATH), blobs) == []


@pytest.mark.parametrize("kind", ["changed", "deleted", "renamed"])
def test_mutation_reports_frozen_path(kind):
    manifest = load_manifest(MANIFEST_PATH)
    blobs = head_blobs(ROOT)
    path = "src/loader.py"
    if kind == "changed":
        blobs[path] = "f" * 40
    elif kind == "deleted":
        del blobs[path]
    else:
        blobs["src/loader_renamed.py"] = blobs.pop(path)
    assert freeze_mismatches(manifest, blobs) == [path]


def test_copied_manifest_blob_change_reports_path(tmp_path):
    manifest = load_manifest(MANIFEST_PATH)
    path = "tests/test_loader.py"
    copied = dict(manifest)
    copied[path] = "0" * 40
    copy_path = tmp_path / "freeze_manifest.json"
    copy_path.write_text(json.dumps(copied), encoding="utf-8", newline="\n")
    assert freeze_mismatches(load_manifest(copy_path), head_blobs(ROOT)) == [path]


def test_workdir_crlf_does_not_change_head_blob(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    git(repo, "config", "user.email", "worker@test.local")
    git(repo, "config", "user.name", "Worker Test")
    target = repo / "src" / "sample.py"
    target.parent.mkdir()
    payload = b"print('ok')\n"
    target.write_bytes(payload)
    git(repo, "add", "--", "src/sample.py")
    git(repo, "commit", "-m", "init")
    blob = git(repo, "rev-parse", "HEAD:src/sample.py").stdout.strip()
    target.write_bytes(b"print('ok')\r\n")
    assert b"\r\n" in target.read_bytes()
    assert target.read_bytes() != payload
    assert freeze_mismatches({"src/sample.py": blob}, head_blobs(repo)) == []
