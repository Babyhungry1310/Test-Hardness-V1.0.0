import json
import os
import subprocess
import sys
from pathlib import Path

from tools.integrate_check import main

ROOT = Path(__file__).resolve().parents[2]


def git_env():
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX"):
        env.pop(key, None)
    return env


def git(cwd, *args):
    return subprocess.run(
        ["git", "-C", str(cwd), *args],
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=git_env(),
    )


def init_repo(tmp_path):
    base = tmp_path / "repo dir"
    bare = base / "origin.git"
    work = base / "work tree"
    base.mkdir(parents=True)
    assert subprocess.run(
        ["git", "init", "--bare", "--initial-branch=main", str(bare)],
        check=True,
        capture_output=True,
        env=git_env(),
    ).returncode == 0
    assert subprocess.run(
        ["git", "clone", str(bare), str(work)],
        check=True,
        capture_output=True,
        env=git_env(),
    ).returncode == 0
    for key, value in (
        ("user.name", "integrate-test"),
        ("user.email", "integrate-test@example.com"),
        ("commit.gpgsign", "false"),
        ("advice.detachedHead", "false"),
    ):
        assert git(work, "config", key, value).returncode == 0
    (work / "keep.txt").write_bytes(b"base\n")
    assert git(work, "add", "keep.txt").returncode == 0
    assert git(work, "commit", "-m", "base").returncode == 0
    assert git(work, "push", "origin", "main").returncode == 0
    return bare, work


def commit_file(repo, branch, name, content, message):
    assert git(repo, "switch", "-c", branch).returncode == 0
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    assert git(repo, "add", "--", name).returncode == 0
    assert git(repo, "commit", "-m", message).returncode == 0
    sha = git(repo, "rev-parse", "HEAD").stdout.strip()
    assert git(repo, "switch", "main").returncode == 0
    return sha


def sha(repo, rev="HEAD"):
    res = git(repo, "rev-parse", rev)
    assert res.returncode == 0
    return res.stdout.strip()


def refs(repo):
    return git(repo, "for-each-ref", "--format=%(objectname) %(refname)").stdout


def porcelain(repo):
    return git(repo, "status", "--porcelain").stdout


def worktrees(repo):
    lines = git(repo, "worktree", "list", "--porcelain").stdout.splitlines()
    return [line[len("worktree "):] for line in lines if line.startswith("worktree ")]


def snapshot(repo):
    return {
        "head": sha(repo),
        "refs": refs(repo),
        "status": porcelain(repo),
    }


def run_check(repo, base, heads, scopes=None):
    argv = ["--repo", str(repo), "--base", base, "--heads", *heads, "--json"]
    if scopes is not None:
        argv.extend(["--scopes", str(scopes)])
    old = sys.argv
    sys.argv = ["integrate_check.py", *argv]
    try:
        code = main()
    finally:
        sys.argv = old
    return code


def run_cli(repo, base, heads, scopes=None):
    argv = [sys.executable, str(ROOT / "tools" / "integrate_check.py"), "--repo", str(repo), "--base", base, "--heads", *heads, "--json"]
    if scopes is not None:
        argv.extend(["--scopes", str(scopes)])
    return subprocess.run(argv, text=True, capture_output=True, encoding="utf-8", errors="replace", env=git_env())


def write_scopes(path, mapping):
    path.write_text(json.dumps(mapping), encoding="utf-8", newline="\n")
    return path


def test_clean_merge_orders_share_tree(tmp_path, capsys):
    _bare, work = init_repo(tmp_path)
    base = sha(work)
    left = commit_file(work, "task/left", "left.txt", b"left\n", "left")
    right = commit_file(work, "task/right", "right dir/right.txt", b"right\n", "right")
    scopes = write_scopes(tmp_path / "scopes.json", {left: ["left.txt"], right: ["right dir"]})
    before = snapshot(work)
    code_ab = run_check(work, base, [left, right], scopes)
    payload_ab = json.loads(capsys.readouterr().out)
    code_ba = run_check(work, base, [right, left], scopes)
    payload_ba = json.loads(capsys.readouterr().out)
    assert code_ab == 0 and code_ba == 0
    assert payload_ab["tree"] == payload_ba["tree"]
    assert payload_ab["merged"] == [left, right]
    assert payload_ba["merged"] == [right, left]
    assert payload_ab["base"] == base
    assert payload_ab["conflict"] is None
    assert payload_ab["out_of_scope"] == []
    assert snapshot(work) == before
    assert Path(payload_ab["worktree"]).is_dir()
    assert " " in payload_ab["worktree"]


def test_conflict_names_file_and_shas_then_aborts(tmp_path, capsys):
    _bare, work = init_repo(tmp_path)
    base = sha(work)
    left = commit_file(work, "task/left", "same.txt", b"left\n", "left")
    right = commit_file(work, "task/right", "same.txt", b"right\n", "right")
    other = commit_file(work, "task/other", "other.txt", b"other\n", "other")
    before = snapshot(work)
    code = run_check(work, base, [left, right, other])
    payload = json.loads(capsys.readouterr().out)
    assert code == 1
    assert payload["conflict"]["files"] == ["same.txt"]
    assert payload["conflict"]["heads"] == [right, left]
    assert payload["merged"] == [left]
    assert other not in payload["merged"]
    trial = Path(payload["worktree"])
    assert git(trial, "rev-parse", "-q", "--verify", "MERGE_HEAD").returncode != 0
    assert porcelain(trial) == ""
    assert snapshot(work) == before


def test_out_of_scope_reported_on_clean_merge(tmp_path, capsys):
    _bare, work = init_repo(tmp_path)
    base = sha(work)
    left = commit_file(work, "task/left", "tools/extra.py", b"print(1)\n", "extra")
    scopes = write_scopes(tmp_path / "scopes.json", {left: ["tools/integrate_check.py"]})
    code = run_check(work, base, [left], scopes)
    payload = json.loads(capsys.readouterr().out)
    assert code == 1
    assert payload["result"] == "fail"
    assert payload["conflict"] is None
    assert payload["out_of_scope"] == [{"sha": left, "files": ["tools/extra.py"]}]
    assert payload["merged"] == [left]


def test_older_base_still_merges_and_is_offset(tmp_path, capsys):
    _bare, work = init_repo(tmp_path)
    old = sha(work)
    left = commit_file(work, "task/old-left", "old.txt", b"old\n", "old")
    (work / "keep.txt").write_bytes(b"moved\n")
    assert git(work, "commit", "-am", "move base").returncode == 0
    newer = sha(work)
    scopes = write_scopes(tmp_path / "scopes.json", {left: ["old.txt"]})
    code = run_check(work, newer, [left], scopes)
    payload = json.loads(capsys.readouterr().out)
    assert code == 0
    assert payload["offset"] == [left]
    assert payload["heads"][0]["base_offset"] is True
    assert old != newer
    assert payload["merged"] == [left]


def test_two_worktrees_commit_does_not_touch_other(tmp_path):
    _bare, work = init_repo(tmp_path)
    assert git(work, "branch", "task/one").returncode == 0
    assert git(work, "branch", "task/two").returncode == 0
    one = tmp_path / "one tree"
    two = tmp_path / "two tree"
    assert git(work, "worktree", "add", str(one), "task/one").returncode == 0
    assert git(work, "worktree", "add", str(two), "task/two").returncode == 0
    before = snapshot(two)
    (one / "only-one.txt").write_bytes(b"one\n")
    assert git(one, "add", "only-one.txt").returncode == 0
    assert git(one, "commit", "-m", "one").returncode == 0
    after = snapshot(two)
    assert after["head"] == before["head"]
    assert after["status"] == before["status"]
    assert "refs/heads/task/two" in after["refs"]
    assert porcelain(two) == ""
    assert not (two / "only-one.txt").exists()


def test_working_clone_refs_head_status_unchanged(tmp_path, capsys):
    _bare, work = init_repo(tmp_path)
    base = sha(work)
    left = commit_file(work, "task/left", "left.txt", b"left\n", "left")
    other = tmp_path / "other tree"
    assert git(work, "worktree", "add", "--detach", str(other), base).returncode == 0
    (other / "untouched.txt").write_bytes(b"dirty\n")
    before_work = snapshot(work)
    before_other = snapshot(other)
    before_root = {
        "head": git(ROOT, "rev-parse", "HEAD").stdout,
        "refs": git(ROOT, "for-each-ref").stdout,
        "status": git(ROOT, "status", "--porcelain").stdout,
        "main": git(ROOT, "rev-parse", "main").stdout,
    }
    scopes = write_scopes(tmp_path / "scopes.json", {left: ["left.txt"]})
    code = run_check(work, base, [left], scopes)
    assert code == 0
    assert snapshot(work) == before_work
    assert snapshot(other) == before_other
    assert porcelain(other) == "?? untouched.txt\n"
    after_root = {
        "head": git(ROOT, "rev-parse", "HEAD").stdout,
        "refs": git(ROOT, "for-each-ref").stdout,
        "status": git(ROOT, "status", "--porcelain").stdout,
        "main": git(ROOT, "rev-parse", "main").stdout,
    }
    assert after_root == before_root
    capsys.readouterr()


def test_usage_error_and_space_path(tmp_path):
    _bare, work = init_repo(tmp_path)
    base = sha(work)
    missing = run_cli(work, base, [])
    assert missing.returncode == 2
    bad = run_cli(tmp_path / "missing repo", base, [base])
    assert bad.returncode == 2
    good = run_cli(work, base, [base])
    assert good.returncode == 0
    payload = json.loads(good.stdout)
    assert " " in str(work)
    assert Path(payload["worktree"]).is_dir()
