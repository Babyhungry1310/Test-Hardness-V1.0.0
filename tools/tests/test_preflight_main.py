import json
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


def run_cli(args, cwd):
    script = Path(__file__).resolve().parent.parent / "preflight_main.py"
    return subprocess.run([sys.executable, str(script)] + args, cwd=cwd, capture_output=True, text=True, encoding="utf-8")


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