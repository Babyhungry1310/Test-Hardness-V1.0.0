import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOKS = ROOT / "tools" / "hooks"
REFUSED_MAIN = "refused: commit blocked on branch main"
DETACHED = "warning: detached HEAD"
PUSH_MAIN = "refused: destination ref refs/heads/main"
PUSH_TAG = "refused: destination ref refs/tags/v1"
ZERO = "0000000000000000000000000000000000000000"
SHA = "0123456789abcdef0123456789abcdef01234567"


def git_env():
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX"):
        env.pop(key, None)
    return env


def git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args], text=True, capture_output=True, env=git_env())


def sh_path():
    git_exe = shutil.which("git")
    if not git_exe:
        raise RuntimeError("git missing")
    candidate = Path(git_exe).resolve().parent.parent / "usr" / "bin" / "sh.exe"
    if candidate.is_file():
        return str(candidate)
    found = shutil.which("sh")
    if not found:
        raise RuntimeError("sh missing")
    return found


def hook(repo, name, stdin=""):
    return subprocess.run([sh_path(), str(HOOKS / name)], cwd=repo, input=stdin, text=True, capture_output=True, env=git_env())


def text(proc):
    return proc.stdout + proc.stderr


def ref_line(local_ref, remote_ref):
    return f"{local_ref} {SHA} {remote_ref} {ZERO}\n"


def init_repo(tmp_path):
    base = tmp_path / "repo dir"
    bare, work = base / "origin.git", base / "work"
    base.mkdir(parents=True)
    subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(bare)], check=True, capture_output=True, env=git_env())
    subprocess.run(["git", "clone", str(bare), str(work)], check=True, capture_output=True, env=git_env())
    pairs = (
        ("user.name", "hook-test"),
        ("user.email", "hook-test@example.com"),
        ("commit.gpgsign", "false"),
        ("advice.detachedHead", "false"),
        ("core.hooksPath", str(HOOKS)),
    )
    for key, value in pairs:
        assert git(work, "config", key, value).returncode == 0
    return bare, work


def test_hook_files_lf_executable_and_clone_untouched():
    listed = git(ROOT, "ls-files", "-s", "--", "tools/hooks/pre-commit", "tools/hooks/pre-push")
    lines = [item for item in listed.stdout.splitlines() if item.strip()]
    assert listed.returncode == 0 and len(lines) == 2
    assert all(item.startswith("100755 ") for item in lines)
    for name in ("pre-commit", "pre-push"):
        data = (HOOKS / name).read_bytes()
        assert b"\r" not in data and data.startswith(b"#!/bin/sh\n")
    assert git(ROOT, "config", "--get", "core.hooksPath").returncode != 0


def test_pre_commit_main_task_and_detached(tmp_path):
    _, work = init_repo(tmp_path)
    direct = hook(work, "pre-commit")
    blocked = git(work, "commit", "--allow-empty", "-m", "nope")
    assert direct.returncode == 1 and direct.stdout == REFUSED_MAIN + "\n" and direct.stderr == ""
    assert blocked.returncode == 1 and REFUSED_MAIN in text(blocked)
    assert git(work, "switch", "-c", "task/TK-9999-R1").returncode == 0
    quiet = hook(work, "pre-commit")
    allowed = git(work, "commit", "--allow-empty", "-m", "ok")
    assert quiet.returncode == 0 and quiet.stdout == "" and quiet.stderr == ""
    assert allowed.returncode == 0 and REFUSED_MAIN not in text(allowed) and DETACHED not in text(allowed)
    assert git(work, "switch", "--detach").returncode == 0
    warned = hook(work, "pre-commit")
    detached = git(work, "commit", "--allow-empty", "-m", "det")
    assert warned.returncode == 0 and warned.stdout == DETACHED + "\n" and warned.stderr == ""
    assert detached.returncode == 0 and text(detached).count(DETACHED) == 1


def test_pre_push_reject_and_allow(tmp_path):
    bare, work = init_repo(tmp_path)
    assert git(work, "switch", "-c", "task/TK-9999-R1").returncode == 0
    assert git(work, "commit", "--allow-empty", "-m", "base").returncode == 0
    quiet = hook(work, "pre-push", ref_line("refs/heads/task/TK-9999-R1", "refs/heads/task/TK-9999-R1") + ref_line("refs/heads/maintenance", "refs/heads/maintenance"))
    pushed = git(work, "push", "origin", "task/TK-9999-R1")
    assert quiet.returncode == 0 and quiet.stdout == "" and quiet.stderr == ""
    assert pushed.returncode == 0 and "refused:" not in text(pushed)
    assert git(bare, "rev-parse", "--verify", "refs/heads/task/TK-9999-R1").returncode == 0
    assert git(work, "branch", "main").returncode == 0
    for args in (("push", "origin", "main"), ("push", "origin", "HEAD:main"), ("push", "--force", "origin", "HEAD:main")):
        proc = git(work, *args)
        assert proc.returncode != 0 and PUSH_MAIN in text(proc)
    assert git(bare, "rev-parse", "--verify", "refs/heads/main").returncode != 0
    assert git(work, "tag", "v1").returncode == 0
    tagged = git(work, "push", "origin", "v1")
    assert tagged.returncode != 0 and PUSH_TAG in text(tagged)
    assert git(work, "branch", "task/TK-9999-R2").returncode == 0
    mixed = git(work, "push", "origin", "task/TK-9999-R2", "refs/tags/v1")
    assert mixed.returncode != 0
    assert git(bare, "rev-parse", "--verify", "refs/tags/v1").returncode != 0
    assert git(bare, "rev-parse", "--verify", "refs/heads/task/TK-9999-R2").returncode != 0
    direct = hook(work, "pre-push", ref_line("refs/heads/task/TK-9999-R1", "refs/heads/task/TK-9999-R1") + ref_line("refs/heads/task/TK-9999-R1", "refs/heads/main"))
    assert direct.returncode == 1 and direct.stdout == PUSH_MAIN + "\n" and direct.stderr == ""


def test_worktree_space_path_and_known_limits(tmp_path):
    bare, work = init_repo(tmp_path)
    assert " " in str(work)
    assert git(work, "switch", "-c", "task/TK-9999-R1").returncode == 0
    assert git(work, "commit", "--allow-empty", "-m", "base").returncode == 0
    assert git(work, "push", "origin", "task/TK-9999-R1").returncode == 0
    assert git(work, "branch", "main").returncode == 0
    blocked = work.parent / "work tree"
    allowed = work.parent / "task tree"
    plain = work.parent / "plain clone"
    assert git(work, "worktree", "add", str(blocked), "main").returncode == 0
    proc = git(blocked, "commit", "--allow-empty", "-m", "blocked")
    assert proc.returncode != 0 and REFUSED_MAIN in text(proc)
    assert git(work, "worktree", "add", "-b", "task/TK-8888-R1", str(allowed)).returncode == 0
    quiet = hook(allowed, "pre-commit")
    assert quiet.returncode == 0 and quiet.stdout == "" and quiet.stderr == ""
    assert git(allowed, "commit", "--allow-empty", "-m", "ok").returncode == 0
    assert git(blocked, "commit", "--allow-empty", "--no-verify", "-m", "bypass").returncode == 0
    assert git(bare, "symbolic-ref", "HEAD", "refs/heads/task/TK-9999-R1").returncode == 0
    cloned = subprocess.run(["git", "clone", str(bare), str(plain)], text=True, capture_output=True, env=git_env())
    assert cloned.returncode == 0
    for key, value in (("user.name", "hook-test"), ("user.email", "hook-test@example.com"), ("commit.gpgsign", "false")):
        assert git(plain, "config", key, value).returncode == 0
    assert git(plain, "config", "--get", "core.hooksPath").returncode != 0
    assert git(plain, "switch", "-c", "main").returncode == 0
    assert git(plain, "commit", "--allow-empty", "-m", "no hook").returncode == 0
