import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "tools" / "hooks" / "pre-merge-commit"
REFUSED = "refused: commit blocked on branch main"


def git_env():
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX"):
        env.pop(key, None)
    return env


def git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args], text=True, capture_output=True, env=git_env())


def git_bytes(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, env=git_env())


def text(proc):
    return proc.stdout + proc.stderr


def init_repo(tmp_path):
    base = tmp_path / "repo dir"
    bare, work = base / "origin.git", base / "work"
    base.mkdir(parents=True)
    subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(bare)], check=True, capture_output=True, env=git_env())
    subprocess.run(["git", "clone", str(bare), str(work)], check=True, capture_output=True, env=git_env())
    for key, value in (
        ("user.name", "hook-test"),
        ("user.email", "hook-test@example.com"),
        ("commit.gpgsign", "false"),
    ):
        assert git(work, "config", key, value).returncode == 0
    (work / "base.txt").write_bytes(b"base\n")
    assert git(work, "add", "base.txt").returncode == 0
    assert git(work, "commit", "-m", "base").returncode == 0
    assert git(work, "switch", "-c", "side").returncode == 0
    (work / "side.txt").write_bytes(b"side\n")
    assert git(work, "add", "side.txt").returncode == 0
    assert git(work, "commit", "-m", "side").returncode == 0
    assert git(work, "switch", "main").returncode == 0
    (work / "main.txt").write_bytes(b"main\n")
    assert git(work, "add", "main.txt").returncode == 0
    assert git(work, "commit", "-m", "main").returncode == 0
    assert git(work, "branch", "task/TK-0032-R1").returncode == 0
    assert git(work, "config", "core.hooksPath", str(ROOT / "tools" / "hooks")).returncode == 0
    return work


def assert_blocked(repo, before, side):
    proc = git(repo, "merge", "--no-ff", "side", "-m", "merge side")
    assert proc.returncode == 1 and REFUSED in text(proc)
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == before
    assert git(repo, "rev-parse", "refs/heads/main").stdout.strip() == before
    assert git(repo, "rev-parse", "--verify", "MERGE_HEAD").stdout.strip() == side
    assert git(repo, "merge", "--abort").returncode == 0
    assert git(repo, "status", "--porcelain").stdout.strip() == ""
    assert git(repo, "rev-parse", "--verify", "MERGE_HEAD").returncode != 0


def test_hook_lf_blob_and_mode_100755():
    data = HOOK.read_bytes()
    assert b"\r" not in data and data.startswith(b"#!/bin/sh\n") and data.endswith(b"\n")
    listed = git(ROOT, "ls-files", "-s", "--", "tools/hooks/pre-merge-commit")
    assert listed.returncode == 0
    lines = [item for item in listed.stdout.splitlines() if item.strip()]
    assert len(lines) == 1 and lines[0].startswith("100755 ")
    oid = lines[0].split()[1]
    blob = git_bytes(ROOT, "cat-file", "blob", oid)
    assert blob.returncode == 0 and blob.stdout == data and b"\r" not in blob.stdout
    tree = git(ROOT, "ls-tree", "HEAD", "--", "tools/hooks/pre-merge-commit")
    assert tree.returncode == 0 and tree.stdout.startswith("100755 blob " + oid)
    assert git(ROOT, "config", "--get", "core.hooksPath").returncode != 0


def test_merge_no_ff_blocked_on_main_allowed_on_task(tmp_path):
    work = init_repo(tmp_path)
    assert " " in str(work)
    head = git(ROOT, "rev-parse", "HEAD").stdout
    status = git(ROOT, "status", "--porcelain").stdout
    before = git(work, "rev-parse", "HEAD").stdout.strip()
    side = git(work, "rev-parse", "side").stdout.strip()
    assert git(work, "rev-parse", "refs/heads/main").stdout.strip() == before
    assert_blocked(work, before, side)
    assert git(work, "switch", "task/TK-0032-R1").returncode == 0
    allowed = git(work, "merge", "--no-ff", "side", "-m", "merge side")
    assert allowed.returncode == 0 and REFUSED not in text(allowed)
    parents = git(work, "rev-parse", "HEAD^1", "HEAD^2")
    assert parents.returncode == 0 and parents.stdout.split() == [before, side]
    linked = work.parent / "work tree"
    assert " " in str(linked)
    assert git(work, "worktree", "add", str(linked), "main").returncode == 0
    assert_blocked(linked, before, side)
    assert git(ROOT, "rev-parse", "HEAD").stdout == head
    assert git(ROOT, "status", "--porcelain").stdout == status
    assert git(ROOT, "config", "--get", "core.hooksPath").returncode != 0


def test_detached_merge_allowed(tmp_path):
    work = init_repo(tmp_path)
    assert git(work, "switch", "--detach").returncode == 0
    proc = git(work, "merge", "--no-ff", "side", "-m", "merge side")
    assert proc.returncode == 0 and "warning: detached HEAD" in text(proc) and REFUSED not in text(proc)
    assert len(git(work, "rev-parse", "HEAD^1", "HEAD^2").stdout.split()) == 2
