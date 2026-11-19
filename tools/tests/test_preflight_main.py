import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from tools.preflight_main import check_branch_pattern, run_preflight


def init_repo(path):
    subprocess.run(["git", "init", "-b", "main"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Worker Test"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "worker@test.local"], cwd=path, check=True, capture_output=True)
    (path / "file.txt").write_text("initial", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=path, check=True, capture_output=True)


def add_worktree(repo_dir, wt_dir, branch_name):
    subprocess.run(["git", "worktree", "add", str(wt_dir), "-b", branch_name], cwd=repo_dir, check=True, capture_output=True)


def run_cli(args, cwd, env=None):
    script = Path(__file__).resolve().parent.parent / "preflight_main.py"
    return subprocess.run([sys.executable, str(script)] + args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", env=env)


def child_env(narrow):
    env = os.environ.copy()
    env.pop("PYTHONUTF8", None)
    env.pop("PYTHONIOENCODING", None)
    if narrow:
        env["PYTHONUTF8"] = "0"
        env["PYTHONIOENCODING"] = "cp1252:strict"
    return env


def run_cli_child(args, cwd, narrow=False):
    script = Path(__file__).resolve().parent.parent / "preflight_main.py"
    cmd = [sys.executable]
    if narrow:
        cmd.extend(["-X", "utf8=0"])
    cmd.append(str(script))
    cmd.extend(args)
    return subprocess.run(cmd, cwd=cwd, capture_output=True, env=child_env(narrow))


def utf8_text(res):
    assert b"UnicodeEncodeError" not in res.stderr
    return res.stdout.decode("utf-8")


def write_hook_bytes(directory, name, payload):
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / name
    target.write_bytes(payload)
    seen = target.read_bytes()
    if b"\r" in payload:
        assert b"\r" in seen
    return seen


def load_cli_json(res):
    return json.loads(res.stdout)


def git_hooks_dir(cwd):
    res = subprocess.run(["git", "rev-parse", "--git-path", "hooks"], cwd=cwd, check=True, capture_output=True, text=True)
    path = Path(res.stdout.strip())
    if not path.is_absolute():
        path = cwd / path
    return path


HOOK_CASES = [
    ("missing", "abs", {}, None, 0, "missing"),
    ("lf", "abs", {"pre-commit": b"#!/bin/sh\n"}, None, 0, "installed"),
    ("cr-name", "abs", {"pre-commit": b"#!/bin/sh\r\n"}, ["pre-commit"], 1, "crlf"),
    ("cr-py", "abs", {"tool.py": b"#!/usr/bin/env python\r\n"}, ["tool.py"], 1, "crlf"),
    ("rel-lf", "rel", {"pre-commit": b"#!/bin/sh\n"}, None, 0, "installed"),
    ("absent", "absent", {}, None, 0, "installed"),
    ("empty", "empty", {}, None, 0, "installed"),
    ("skip", "abs", {"pre-commit.sample": b"#!/bin/sh\r\n", "pre-push.SAMPLE": b"#!/bin/sh\r\n", "POLICY.MD": b"#!x\r\n", "readme.md": b"#!x\r\n", "README": b"plain\r\n", "NOTES": b"plain\r\n", "LICENSE": b"plain\r\n"}, None, 0, "missing"),
    ("order", "abs", {"pre-push": b"push\r\n", "pre-commit": b"commit\r\n", "tool.py": b"#!/usr/bin/env python\r\n", "NOTES": b"plain\r\n"}, ["pre-commit", "pre-push", "tool.py"], 1, "crlf"),
    ("shebang-lf", "abs", {"README": b"#!/bin/sh\n"}, None, 0, "installed"),
    ("cr-shebang", "abs", {"custom-hook": b"#!/bin/sh\r\n"}, ["custom-hook"], 1, "crlf"),
    ("py-plain", "abs", {"tool.py": b"print(1)\r\n"}, None, 0, "missing"),
]


def test_branch_patterns():
    assert check_branch_pattern("worker", "task/TK-0007-R1")
    assert check_branch_pattern("worker", "task/TK-9999-R2")
    assert not check_branch_pattern("worker", "task/TK-07-R1")
    assert not check_branch_pattern("worker", "task/TK-0007")
    assert not check_branch_pattern("worker", "main")
    assert not check_branch_pattern("worker", "feat/test")

    assert check_branch_pattern("lead", "lead/plan-cyc-03")
    assert check_branch_pattern("lead", "lead/revert-TK-0007")
    assert check_branch_pattern("lead", "upgrade/1.0.1")
    assert not check_branch_pattern("lead", "lead/")
    assert not check_branch_pattern("lead", "main")
    assert not check_branch_pattern("lead", "task/TK-0007-R1")

    assert check_branch_pattern("reviewer", "review/CYC-03-R1-a1b2")
    assert check_branch_pattern("reviewer", "review/CYC-02-R1")
    assert check_branch_pattern("reviewer", "review/CYC-01")
    assert not check_branch_pattern("reviewer", "review/CYC-03-R1-TOOLONG")
    assert not check_branch_pattern("reviewer", "review/invalid")
    assert not check_branch_pattern("reviewer", "main")


def test_session_in_main_checkout_fails(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    subprocess.run(["git", "checkout", "-b", "task/TK-0007-R1"], cwd=repo, check=True, capture_output=True)
    res = run_cli(["--role", "worker", "--stage", "session"], cwd=repo)
    assert res.returncode == 1
    code, data = run_preflight("worker", "session", cwd=repo)
    assert code == 1
    assert not data["ok"]
    wt_check = next(c for c in data["checks"] if c["name"] == "worktree")
    assert not wt_check["passed"]


def test_session_on_main_branch_fails(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    subprocess.run(["git", "branch", "-m", "temp_main_holder"], cwd=repo, check=True, capture_output=True)
    wt = tmp_path / "wt"
    subprocess.run(["git", "worktree", "add", str(wt), "-b", "main"], cwd=repo, check=True, capture_output=True)
    res = run_cli(["--role", "worker", "--stage", "session"], cwd=wt)
    assert res.returncode == 1
    code, data = run_preflight("worker", "session", cwd=wt)
    assert code == 1
    assert not data["ok"]
    not_main_check = next(c for c in data["checks"] if c["name"] == "not_main")
    assert not not_main_check["passed"]


def test_session_wrong_branch_fails(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "wrong-branch-name")
    res = run_cli(["--role", "worker", "--stage", "session"], cwd=wt)
    assert res.returncode == 1
    code, data = run_preflight("worker", "session", cwd=wt)
    assert code == 1
    pat_check = next(c for c in data["checks"] if c["name"] == "branch_pattern")
    assert not pat_check["passed"]


def test_session_valid_worktree_passes(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    subprocess.run(["git", "config", "core.hooksPath", "tools/hooks"], cwd=repo, check=True, capture_output=True)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "task/TK-0007-R1")
    write_hook_bytes(wt / "tools" / "hooks", "pre-commit", b"#!/bin/sh\n")
    subprocess.run(["git", "add", "tools/hooks/pre-commit"], cwd=wt, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "hook"], cwd=wt, check=True, capture_output=True)
    res = run_cli(["--role", "worker", "--stage", "session", "--json"], cwd=wt)
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert data["ok"]
    assert data["hook_status"] == "installed"
    assert all(c["passed"] for c in data["checks"])


def test_session_missing_hook_warning(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "task/TK-0007-R1")
    res = run_cli(["--role", "worker", "--stage", "session"], cwd=wt)
    assert res.returncode == 0
    assert "Hook chưa cài" in res.stdout
    code, data = run_preflight("worker", "session", cwd=wt)
    assert code == 0
    assert data["ok"]
    assert data["hook_status"] == "missing"
    assert "Hook chưa cài" in data["warnings"]


def test_session_dirty_worktree_reports_warning(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "task/TK-0007-R1")
    (wt / "dirty.txt").write_text("changes", encoding="utf-8")
    res = run_cli(["--role", "worker", "--stage", "session"], cwd=wt)
    assert res.returncode == 0
    assert "Worktree có thay đổi chưa commit" in res.stdout
    code, data = run_preflight("worker", "session", cwd=wt)
    assert code == 0
    assert data["ok"]
    assert "Worktree có thay đổi chưa commit" in data["warnings"]
    clean_check = next(c for c in data["checks"] if c["name"] == "clean")
    assert not clean_check["clean"]


def test_commit_stage(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    res_main = run_cli(["--role", "worker", "--stage", "commit"], cwd=repo)
    assert res_main.returncode == 1

    wt_worker = tmp_path / "wt_worker"
    add_worktree(repo, wt_worker, "task/TK-0007-R1")
    res_worker = run_cli(["--role", "worker", "--stage", "commit"], cwd=wt_worker)
    assert res_worker.returncode == 0

    wt_lead = tmp_path / "wt_lead"
    add_worktree(repo, wt_lead, "lead/review-notes")
    res_lead = run_cli(["--role", "lead", "--stage", "commit"], cwd=wt_lead)
    assert res_lead.returncode == 0

    wt_rev = tmp_path / "wt_rev"
    add_worktree(repo, wt_rev, "review/CYC-03-R1-a1b2")
    res_rev = run_cli(["--role", "reviewer", "--stage", "commit"], cwd=wt_rev)
    assert res_rev.returncode == 0

    res_mismatch = run_cli(["--role", "reviewer", "--stage", "commit"], cwd=wt_worker)
    assert res_mismatch.returncode == 1


def test_push_stage(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "task/TK-0007-R1")

    assert run_cli(["--role", "worker", "--stage", "push", "--ref", "refs/heads/main"], cwd=wt).returncode == 1
    assert run_cli(["--role", "worker", "--stage", "push", "--ref", "main"], cwd=wt).returncode == 1
    assert run_cli(["--role", "worker", "--stage", "push", "--ref", "refs/tags/v1.0"], cwd=wt).returncode == 1
    assert run_cli(["--role", "worker", "--stage", "push", "--ref", "refs/tags/cycle/CYC-03"], cwd=wt).returncode == 1
    assert run_cli(["--role", "worker", "--stage", "push", "--ref", "other-branch"], cwd=wt).returncode == 1
    assert run_cli(["--role", "worker", "--stage", "push", "--ref", "refs/heads/task/TK-9999-R1"], cwd=wt).returncode == 1

    assert run_cli(["--role", "worker", "--stage", "push", "--ref", "task/TK-0007-R1"], cwd=wt).returncode == 0
    assert run_cli(["--role", "worker", "--stage", "push", "--ref", "refs/heads/task/TK-0007-R1"], cwd=wt).returncode == 0
    assert run_cli(["--role", "worker", "--stage", "push", "--ref", "HEAD:refs/heads/task/TK-0007-R1"], cwd=wt).returncode == 0
    assert run_cli(["--role", "worker", "--stage", "push"], cwd=wt).returncode == 0

    assert run_cli(["--role", "worker", "--stage", "push"], cwd=repo).returncode == 1


def test_cli_usage_and_errors(tmp_path):
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    assert run_cli(["--role", "worker", "--stage", "session"], cwd=empty_dir).returncode == 2
    assert run_cli(["--role", "unknown", "--stage", "session"], cwd=empty_dir).returncode == 2
    assert run_cli(["--role", "worker", "--stage", "unknown"], cwd=empty_dir).returncode == 2
    assert run_cli(["--role", "worker"], cwd=empty_dir).returncode == 2


def test_preflight_does_not_modify_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    subprocess.run(["git", "config", "core.hooksPath", "tools/hooks"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "tag", "cycle/CYC-01"], cwd=repo, check=True, capture_output=True)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "task/TK-0007-R1")

    def snapshot(path):
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True).stdout
        refs = subprocess.run(["git", "show-ref"], cwd=path, capture_output=True, text=True).stdout
        config = subprocess.run(["git", "config", "--list"], cwd=path, capture_output=True, text=True).stdout
        status = subprocess.run(["git", "status", "--porcelain"], cwd=path, capture_output=True, text=True).stdout
        files = {p.relative_to(path): p.read_bytes() for p in path.rglob("*") if ".git" not in p.parts}
        return head, refs, config, status, files

    snap_repo_before = snapshot(repo)
    snap_wt_before = snapshot(wt)

    run_cli(["--role", "worker", "--stage", "session"], cwd=wt)
    run_cli(["--role", "worker", "--stage", "commit"], cwd=wt)
    run_cli(["--role", "worker", "--stage", "push", "--ref", "task/TK-0007-R1"], cwd=wt)
    run_cli(["--role", "worker", "--stage", "push", "--ref", "refs/heads/main"], cwd=wt)
    run_cli(["--role", "lead", "--stage", "session"], cwd=repo)

    snap_repo_after = snapshot(repo)
    snap_wt_after = snapshot(wt)

    assert snap_repo_before == snap_repo_after
    assert snap_wt_before == snap_wt_after


@pytest.mark.parametrize("narrow", [False, True])
def test_encoding_outside_repo_exits_2(tmp_path, narrow):
    empty = tmp_path / "empty"
    empty.mkdir()
    res = run_cli_child(["--role", "worker", "--stage", "session"], empty, narrow=narrow)
    assert res.returncode == 2
    text = utf8_text(res)
    assert "Lỗi: Not a git repo" in text
    assert "L?i" not in text


@pytest.mark.parametrize("narrow", [False, True])
def test_encoding_usage_exits_2(tmp_path, narrow):
    empty = tmp_path / "empty"
    empty.mkdir()
    res = run_cli_child(["--role", "unknown", "--stage", "session"], empty, narrow=narrow)
    assert res.returncode == 2
    utf8_text(res)


@pytest.mark.parametrize("narrow", [False, True])
def test_encoding_main_checkout_exits_1(tmp_path, narrow):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    res = run_cli_child(["--role", "worker", "--stage", "session"], repo, narrow=narrow)
    assert res.returncode == 1
    text = utf8_text(res)
    assert "Preflight FAILED" in text


@pytest.mark.parametrize("narrow", [False, True])
def test_encoding_warnings_and_json(tmp_path, narrow):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "task/TK-0007-R1")
    (wt / "dirty.txt").write_text("changes", encoding="utf-8")
    res = run_cli_child(["--role", "worker", "--stage", "session"], wt, narrow=narrow)
    assert res.returncode == 0
    text = utf8_text(res)
    assert "Cảnh báo: Hook chưa cài" in text
    assert "Cảnh báo: Worktree có thay đổi chưa commit" in text
    assert "Preflight PASSED" in text
    js = run_cli_child(["--role", "worker", "--stage", "session", "--json"], wt, narrow=narrow)
    assert js.returncode == 0
    data = json.loads(utf8_text(js))
    assert data["ok"] is True
    assert data["warnings"] == ["Hook chưa cài", "Worktree có thay đổi chưa commit"]


@pytest.mark.parametrize("case_id,anchor,payloads,names,code,status", HOOK_CASES, ids=[item[0] for item in HOOK_CASES])
def test_session_hook_bytes(tmp_path, case_id, anchor, payloads, names, code, status):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "task/TK-0034-R1")
    write_hook_bytes(repo / "tools" / "hooks", "pre-commit", b"#!/bin/sh\r\n")
    if anchor == "absent":
        write_hook_bytes(wt, "pre-commit", b"#!/bin/sh\r\n")
        subprocess.run(["git", "add", "pre-commit"], cwd=wt, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "hooks"], cwd=wt, check=True, capture_output=True)
        write_hook_bytes(git_hooks_dir(wt), "pre-commit", b"#!/bin/sh\n")
    elif anchor == "empty":
        write_hook_bytes(git_hooks_dir(wt), "pre-commit", b"#!/bin/sh\r\n")
        write_hook_bytes(wt, "pre-commit", b"#!/bin/sh\n")
        subprocess.run(["git", "add", "pre-commit"], cwd=wt, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "hooks"], cwd=wt, check=True, capture_output=True)
        subprocess.run(["git", "config", "core.hooksPath", ""], cwd=wt, check=True, capture_output=True)
    elif anchor == "rel":
        subprocess.run(["git", "config", "core.hooksPath", "tools/hooks"], cwd=wt, check=True, capture_output=True)
        for name, payload in payloads.items():
            write_hook_bytes(wt / "tools" / "hooks", name, payload)
        subprocess.run(["git", "add", "-A"], cwd=wt, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "hooks"], cwd=wt, check=True, capture_output=True)
    else:
        dest = tmp_path / "abs-hooks"
        dest.mkdir()
        subprocess.run(["git", "config", "core.hooksPath", str(dest)], cwd=wt, check=True, capture_output=True)
        for name, payload in payloads.items():
            write_hook_bytes(dest, name, payload)
    res = run_cli(["--role", "worker", "--stage", "session", "--json"], cwd=wt)
    data = load_cli_json(res)
    assert res.returncode == code, case_id
    assert data["hook_status"] == status
    if names is None:
        assert "files" not in data
    else:
        assert data["files"] == names
    if status == "missing":
        assert data["ok"] is True
        assert data["warnings"] == ["Hook chưa cài"]
    elif status == "installed":
        assert data["ok"] is True
        assert "warnings" not in data
    else:
        assert data["ok"] is False
        assert "warnings" not in data


def test_commit_push_do_not_classify_hooks(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "task/TK-0034-R1")
    blocker = tmp_path / "hookfile"
    blocker.write_bytes(b"#!/bin/sh\r\n")
    assert b"\r" in blocker.read_bytes()
    subprocess.run(["git", "config", "core.hooksPath", str(blocker)], cwd=wt, check=True, capture_output=True)
    commit = run_cli(["--role", "worker", "--stage", "commit", "--json"], cwd=wt)
    assert commit.returncode == 0
    assert "hook_status" not in load_cli_json(commit)
    push = run_cli(["--role", "worker", "--stage", "push", "--json"], cwd=wt)
    assert push.returncode == 0
    assert "hook_status" not in load_cli_json(push)
    session = run_cli(["--role", "worker", "--stage", "session", "--json"], cwd=wt)
    assert session.returncode == 1
    assert "Traceback" not in session.stderr
    data = load_cli_json(session)
    assert data["hook_status"] == "error"
    assert data["files"] == []
    assert data["errors"][0]["op"] == "is_dir"
    assert data["reason"] == "not a directory"


def session_wt(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)
    wt = tmp_path / "wt"
    add_worktree(repo, wt, "task/TK-0035-R1")
    return repo, wt


def write_fault(directory):
    directory.mkdir(parents=True, exist_ok=True)
    code = (
        "import os\nfrom pathlib import Path\n"
        "pairs={}\n"
        "for item in os.environ.get('TK0035_FAULTS','').split(','):\n"
        "    if item:\n"
        "        name,op=item.split(':',1)\n"
        "        pairs.setdefault(name,set()).add(op)\n"
        "orig={k:getattr(Path,k) for k in ('is_dir','is_file','iterdir','read_bytes')}\n"
        "def is_dir(self,*a,**k):\n"
        "    if 'is_dir' in pairs.get(self.name,()):\n"
        "        raise OSError('denied')\n"
        "    return orig['is_dir'](self,*a,**k)\n"
        "def is_file(self,*a,**k):\n"
        "    if 'is_file' in pairs.get(self.name,()):\n"
        "        raise OSError('denied')\n"
        "    return orig['is_file'](self,*a,**k)\n"
        "def iterdir(self):\n"
        "    if 'iterdir' in pairs.get(self.name,()):\n"
        "        raise OSError('denied')\n"
        "    return orig['iterdir'](self)\n"
        "def read_bytes(self):\n"
        "    if 'read_bytes' in pairs.get(self.name,()):\n"
        "        raise OSError('denied')\n"
        "    return orig['read_bytes'](self)\n"
        "Path.is_dir=is_dir\nPath.is_file=is_file\nPath.iterdir=iterdir\nPath.read_bytes=read_bytes\n"
    )
    (directory / "sitecustomize.py").write_text(code, encoding="utf-8", newline="\n")


def fault_env(directory, faults):
    env = os.environ.copy()
    prev = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(directory) if not prev else str(directory) + os.pathsep + prev
    env["TK0035_FAULTS"] = faults
    return env


FORM_HOOKS = {
    "POLICY.MD": b"#!x\r\n",
    "pre-commit.sample": b"#!/bin/sh\r\n",
    "pre-push.SAMPLE": b"#!/bin/sh\r\n",
    "X.SaMpLe": b"#!/bin/sh\r\n",
    "README": b"plain\r\n",
    "NOTES": b"plain\r\n",
    "LICENSE": b"plain\r\n",
    "custom-hook": b"#!/bin/sh\r\n",
    "pre-commit": b"#!/bin/sh\r\n",
}


@pytest.mark.parametrize("form", ["relative", "absolute", "whitespace", "linked"])
def test_session_hook_path_forms(tmp_path, form):
    repo, wt = session_wt(tmp_path)
    if form == "relative":
        dest = wt / "tools" / "hooks"
        config = "tools/hooks"
    elif form == "absolute":
        dest = tmp_path / "abs-hooks"
        config = str(dest)
    elif form == "whitespace":
        dest = tmp_path / "hook dir"
        config = str(dest)
    else:
        assert (wt / ".git").is_file()
        write_hook_bytes(repo / "tools" / "hooks", "pre-commit", b"#!/bin/sh\n")
        dest = wt / "tools" / "hooks"
        config = "tools/hooks"
    for name, payload in FORM_HOOKS.items():
        write_hook_bytes(dest, name, payload)
    subprocess.run(["git", "config", "core.hooksPath", config], cwd=wt, check=True, capture_output=True)
    res = run_cli(["--role", "worker", "--stage", "session", "--json"], cwd=wt)
    assert "Traceback" not in res.stderr
    data = load_cli_json(res)
    assert res.returncode == 1, form
    assert data["hook_status"] == "crlf"
    assert data["files"] == ["custom-hook", "pre-commit"]


@pytest.mark.parametrize("op", ["is_dir", "iterdir", "is_file", "read_bytes"])
def test_session_oserror_points(tmp_path, op):
    _repo, wt = session_wt(tmp_path)
    dest = tmp_path / "hookdir"
    write_hook_bytes(dest, "pre-commit", b"#!/bin/sh\r\n")
    subprocess.run(["git", "config", "core.hooksPath", str(dest)], cwd=wt, check=True, capture_output=True)
    fault_dir = tmp_path / "fault"
    write_fault(fault_dir)
    target = "hookdir" if op in ("is_dir", "iterdir") else "pre-commit"
    res = run_cli(["--role", "worker", "--stage", "session", "--json"], cwd=wt, env=fault_env(fault_dir, f"{target}:{op}"))
    assert "Traceback" not in res.stderr
    data = load_cli_json(res)
    assert res.returncode == 1
    assert data["hook_status"] == "error"
    assert "files" in data and "errors" in data and "reason" in data
    assert data["files"] == []
    assert data["errors"][0]["op"] == op
    assert data["errors"][0]["name"] == target
    assert data["reason"] == data["errors"][0]["reason"] == "denied"


def test_session_crlf_keeps_files_and_error_order(tmp_path):
    _repo, wt = session_wt(tmp_path)
    dest = tmp_path / "hookdir"
    write_hook_bytes(dest, "aaa", b"#!/bin/sh\r\n")
    write_hook_bytes(dest, "mid", b"#!/bin/sh\n")
    write_hook_bytes(dest, "pre-commit", b"#!/bin/sh\r\n")
    write_hook_bytes(dest, "tool.py", b"#!/usr/bin/env python\r\n")
    write_hook_bytes(dest, "zzz", b"#!/bin/sh\r\n")
    write_hook_bytes(dest, "POLICY.MD", b"#!x\r\n")
    write_hook_bytes(dest, "pre-push.SAMPLE", b"#!/bin/sh\r\n")
    write_hook_bytes(dest, "README", b"plain\r\n")
    write_hook_bytes(dest, "NOTES", b"plain\r\n")
    write_hook_bytes(dest, "LICENSE", b"plain\r\n")
    subprocess.run(["git", "config", "core.hooksPath", str(dest)], cwd=wt, check=True, capture_output=True)
    fault_dir = tmp_path / "fault"
    write_fault(fault_dir)
    res = run_cli(["--role", "worker", "--stage", "session", "--json"], cwd=wt, env=fault_env(fault_dir, "aaa:read_bytes,zzz:is_file"))
    assert "Traceback" not in res.stderr
    data = load_cli_json(res)
    assert res.returncode == 1
    assert data["hook_status"] == "error"
    assert data["files"] == ["pre-commit", "tool.py"]
    assert [(item["name"], item["op"]) for item in data["errors"]] == [("aaa", "read_bytes"), ("zzz", "is_file")]
    assert data["reason"] == "denied"
    for blocked in ("POLICY.MD", "pre-push.SAMPLE", "README", "NOTES", "LICENSE", "mid", "aaa", "zzz"):
        assert blocked not in data["files"]


@pytest.mark.parametrize("narrow", [False, True])
@pytest.mark.parametrize("kind", ["crlf", "error"])
def test_encoding_crlf_and_error(tmp_path, narrow, kind):
    _repo, wt = session_wt(tmp_path)
    if kind == "crlf":
        dest = tmp_path / "hooks"
        write_hook_bytes(dest, "pre-commit", b"#!/bin/sh\r\n")
        subprocess.run(["git", "config", "core.hooksPath", str(dest)], cwd=wt, check=True, capture_output=True)
        (wt / "dirty.txt").write_text("changes", encoding="utf-8")
        res = run_cli_child(["--role", "worker", "--stage", "session"], wt, narrow=narrow)
        assert res.returncode == 1
        text = utf8_text(res)
        assert "Hook CRLF" in text
        assert "Cảnh báo: Worktree có thay đổi chưa commit" in text
    else:
        blocker = tmp_path / "hookfile"
        blocker.write_bytes(b"#!/bin/sh\r\n")
        assert b"\r" in blocker.read_bytes()
        subprocess.run(["git", "config", "core.hooksPath", str(blocker)], cwd=wt, check=True, capture_output=True)
        res = run_cli_child(["--role", "worker", "--stage", "session"], wt, narrow=narrow)
        assert res.returncode == 1
        text = utf8_text(res)
        assert "Lỗi: not a directory" in text
    assert "Traceback" not in res.stderr.decode("utf-8")
    js = run_cli_child(["--role", "worker", "--stage", "session", "--json"], wt, narrow=narrow)
    assert js.returncode == 1
    data = json.loads(utf8_text(js))
    if kind == "crlf":
        assert data["hook_status"] == "crlf"
        assert data["files"] == ["pre-commit"]
    else:
        assert data["hook_status"] == "error"
        assert "files" in data and "errors" in data and "reason" in data