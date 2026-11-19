import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HOOKS = ROOT / "tools/hooks"


def git(repo, *args, ok=True):
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX"):
        env.pop(key, None)
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8", env=env)
    if ok:
        assert result.returncode == 0, result.stdout + result.stderr
    return result


def commit(repo, value):
    (repo / "file.txt").write_text(value, encoding="utf-8")
    git(repo, "add", "file.txt")
    git(repo, "commit", "-m", value)
    return git(repo, "rev-parse", "HEAD").stdout.strip()


@pytest.fixture
def repos(tmp_path):
    bare, repo = tmp_path / "origin.git", tmp_path / "working repo"
    git(tmp_path, "init", "--bare", "--initial-branch=main", str(bare))
    git(tmp_path, "clone", str(bare), str(repo))
    empty = tmp_path / "empty hooks"
    empty.mkdir()
    for key, value in (("user.name", "edge-test"), ("user.email", "edge@test.local"), ("commit.gpgsign", "false"), ("core.hooksPath", str(empty))):
        git(repo, "config", key, value)
    commit(repo, "base")
    git(repo, "tag", "v1")
    git(repo, "push", "origin", "main", "refs/tags/v1")
    git(repo, "switch", "-c", "task/TK-0001-R1")
    git(repo, "config", "core.hooksPath", str(HOOKS))
    return bare, repo, empty


@pytest.mark.parametrize("args,ref", [((":main",), "refs/heads/main"), (("--all",), "refs/heads/main"), (("--mirror",), "refs/heads/"), (("--tags",), "refs/tags/v2"), ((":refs/tags/v1",), "refs/tags/v1"), (("HEAD:refs/heads/main",), "refs/heads/main")])
def test_push_blocked(repos, args, ref):
    bare, repo, _ = repos
    head = commit(repo, "ahead")
    git(repo, "update-ref", "refs/heads/main", head)
    git(repo, "tag", "v2")
    before = git(bare, "show-ref").stdout
    result = git(repo, "push", "origin", *args, ok=False)
    assert result.returncode == 1 and "refused: destination ref " + ref in result.stdout + result.stderr
    assert git(bare, "show-ref").stdout == before


@pytest.mark.parametrize("branch", ["main-fix", "mainline", "task/TK-0001-R1", "lead/main-protection"])
def test_limit_similar_branch_allowed(repos, branch):
    bare, repo, _ = repos
    git(repo, "switch", "-C", branch)
    head = commit(repo, "message contains main")
    git(repo, "push", "origin", "HEAD:refs/heads/" + branch)
    assert git(bare, "rev-parse", "refs/heads/" + branch).stdout.strip() == head


@pytest.mark.parametrize("operation", ["amend", "worktree", "merge"])
def test_commit_on_main_blocked(repos, tmp_path, operation):
    _, repo, _ = repos
    side = commit(repo, "side")
    if operation == "worktree":
        target = tmp_path / "main worktree"
        git(repo, "worktree", "add", str(target), "main")
    else:
        git(repo, "switch", "main")
        target = repo
    before = git(target, "rev-parse", "HEAD").stdout
    args = ("merge", "--no-ff", "--no-edit", "task/TK-0001-R1") if operation == "merge" else ("commit", "--allow-empty", "-m", "blocked", *( ["--amend"] if operation == "amend" else []))
    result = git(target, *args, ok=False)
    assert result.returncode == 1 and "refused: commit blocked on branch main" in result.stdout + result.stderr
    assert git(target, "rev-parse", "HEAD").stdout == before
    if operation == "merge":
        assert git(target, "rev-parse", "refs/heads/main").stdout == before
        assert git(target, "rev-parse", "--verify", "MERGE_HEAD").stdout.strip() == side
        assert git(target, "merge", "--abort").returncode == 0
        assert git(target, "status", "--porcelain").stdout.strip() == ""
        assert git(target, "rev-parse", "--verify", "MERGE_HEAD", ok=False).returncode != 0


@pytest.mark.parametrize("operation", ["no-verify", "hooksPath", "update-ref", "cherry-pick", "rebase"])
def test_limit_main_bypass(repos, operation):
    _, repo, empty = repos
    side = commit(repo, "side")
    git(repo, "switch", "main")
    before = git(repo, "rev-parse", "HEAD").stdout.strip()
    if operation == "hooksPath":
        git(repo, "config", "core.hooksPath", str(empty))
    if operation in ("no-verify", "hooksPath"):
        git(repo, "commit", "--allow-empty", "-m", "bypass", *(["--no-verify"] if operation == "no-verify" else []))
    elif operation == "update-ref":
        git(repo, "update-ref", "refs/heads/main", side)
    elif operation == "cherry-pick":
        git(repo, "cherry-pick", side)
    else:
        git(repo, "rebase", "--force-rebase", "task/TK-0001-R1")
    assert git(repo, "branch", "--show-current").stdout.strip() == "main"
    assert git(repo, "rev-parse", "HEAD").stdout.strip() != before


@pytest.mark.parametrize("branch,ref", [("Main", None), ("task/tk-0001-r1", None), ("task/TK-0001-R1", "refs/heads/task/TK-0001-R1 bad"), ("task/TK-0001-R1", "refs/heads/task/TK-0001-R1?bad")])
def test_preflight_invalid_blocked(repos, branch, ref):
    _, repo, _ = repos
    git(repo, "switch", "-C", branch)
    args = ["--role", "worker", "--stage", "push" if ref else "commit", "--json"]
    if ref:
        args.extend(["--ref", ref])
    result = subprocess.run([sys.executable, str(ROOT / "tools/preflight_main.py"), *args], cwd=repo, capture_output=True, text=True, encoding="utf-8")
    data = json.loads(result.stdout)
    assert result.returncode == 1 and data["ok"] is False
    assert any(check["name"] == ("target_matches_session" if ref else "branch_pattern") and check["passed"] is False for check in data["checks"])


@pytest.mark.parametrize("name", ["pre-commit", "pre-push", "pre-merge-commit"])
def test_crlf_hook_installation_blocked(repos, tmp_path, name):
    _, repo, _ = repos
    copied = tmp_path / "copied hooks"
    copied.mkdir()
    original = (HOOKS / name).read_bytes()
    assert b"\r" not in original
    payload = original.replace(b"\n", b"\r\n")
    assert b"\r\n" in payload
    (copied / name).write_bytes(payload)
    assert (copied / name).read_bytes() == payload
    git(repo, "config", "core.hooksPath", str(copied))
    result = subprocess.run([sys.executable, str(ROOT / "tools/preflight_main.py"), "--role", "worker", "--stage", "session", "--json"], cwd=repo, capture_output=True, text=True, encoding="utf-8")
    data = json.loads(result.stdout)
    assert result.returncode == 1 and data["ok"] is False and data["hook_status"] == "crlf" and data["files"] == [name]
