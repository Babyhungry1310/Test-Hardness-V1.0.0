import json
import subprocess
import sys
from pathlib import Path

from tools.github_audit import audit, format_report

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "github_audit.py"


def dump(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8", newline="\n")


def protection():
    return {
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
            "require_code_owner_reviews": True,
        },
        "enforce_admins": {"enabled": True},
        "allow_force_pushes": {"enabled": False},
        "allow_deletions": {"enabled": False},
    }


def tag_rule():
    return {
        "id": 9,
        "target": "tag",
        "enforcement": "active",
        "bypass_actors": [{"actor_id": 7, "actor_type": "User", "bypass_mode": "always"}],
        "conditions": {"ref_name": {"include": ["refs/tags/cycle/*"], "exclude": []}},
        "rules": [{"type": "creation"}, {"type": "update"}, {"type": "deletion"}],
    }


def fill(directory, **over):
    directory.mkdir(parents=True, exist_ok=True)
    repo = {
        "default_branch": "main",
        "allow_squash_merge": True,
        "allow_merge_commit": False,
        "allow_rebase_merge": False,
        "allow_auto_merge": False,
        "delete_branch_on_merge": False,
        "owner": {"login": "owner", "id": 7},
    }
    repo.update(over.get("repo", {}))
    dump(directory / "repo.json", repo)
    dump(directory / "branch_main.json", over.get("branch", {"name": "main", "protected": True}))
    dump(directory / "protection.json", over.get("protection", protection()))
    rulesets = over.get("rulesets", [{"id": 9}])
    dump(directory / "rulesets.json", rulesets)
    if rulesets == [{"id": 9}]:
        dump(directory / "ruleset_9.json", over.get("ruleset", tag_rule()))
    dump(directory / "user.json", over.get("user", {"login": "owner", "id": 7, "email": "hidden@example.com"}))
    (directory / "codeowners.txt").write_text(over.get("codeowners", "* @owner\n"), encoding="utf-8", newline="\n")
    if "manifest" in over:
        dump(directory / "manifest.json", over["manifest"])


def rows(directory):
    lines, _manifest = audit(directory)
    return {number: (result, reason) for number, result, reason in lines}


def test_all_nine_pass(tmp_path):
    directory = tmp_path / "audit input"
    fill(directory)
    got = rows(directory)
    assert set(got) == set(range(1, 10))
    assert all(result == "PASS" for result, _reason in got.values())
    assert "không phân biệt được OWNER với tác tử" in got[9][1]
    assert "tự duyệt PR cùng tài khoản không khả thi" in got[4][1]
    assert "hidden@example.com" not in got[9][1]


def test_unprotected_repo(tmp_path):
    directory = tmp_path / "bare"
    fill(
        directory,
        branch={"name": "main", "protected": False},
        protection={"http_status": 404, "message": "Branch not protected"},
        rulesets=[],
    )
    got = rows(directory)
    assert [got[n][0] for n in range(1, 6)] == ["FAIL"] * 5
    assert "tự duyệt PR cùng tài khoản không khả thi" in got[4][1]
    assert got[7][0] == "PASS"
    assert got[9][0] == "PASS"


def test_merge_commit_enabled(tmp_path):
    directory = tmp_path / "merge"
    fill(directory, repo={"allow_merge_commit": True})
    got = rows(directory)
    assert got[6][0] == "FAIL"
    assert "merge_commit=True" in got[6][1]
    assert got[1][0] == "PASS"


def test_auto_merge_enabled(tmp_path):
    directory = tmp_path / "auto"
    fill(directory, repo={"allow_auto_merge": True})
    assert rows(directory)[7] == ("FAIL", "auto-merge bật")


def test_admin_bypass(tmp_path):
    directory = tmp_path / "admin"
    prot = protection()
    prot["enforce_admins"] = {"enabled": False}
    fill(directory, protection=prot)
    assert rows(directory)[3][0] == "FAIL"
    assert "quản trị được bỏ qua" in rows(directory)[3][1]


def test_current_user_differs_from_owner(tmp_path):
    directory = tmp_path / "other"
    fill(directory, user={"login": "agent", "id": 8}, codeowners="* @owner\n")
    got = rows(directory)
    assert got[9][0] == "FAIL"
    assert "khác OWNER" in got[9][1]
    assert "không khả thi" not in got[4][1]
    assert got[4][0] == "PASS"


def test_missing_data_unknown(tmp_path):
    directory = tmp_path / "empty"
    directory.mkdir()
    got = rows(directory)
    assert [got[n][0] for n in range(1, 10)] == ["UNKNOWN"] * 9


def test_denied_file_not_guessed(tmp_path):
    directory = tmp_path / "denied"
    directory.mkdir()
    dump(directory / "protection.json", {"http_status": 403, "message": "Resource not accessible by integration"})
    dump(directory / "rulesets.json", {"http_status": 404, "message": "Not Found"})
    got = rows(directory)
    assert [got[n][0] for n in range(1, 6)] == ["UNKNOWN"] * 5


def test_report_lists_commands_and_limits(tmp_path):
    directory = tmp_path / "report in"
    manifest = {
        "fetched_at": "2026-11-14T00:00:00Z",
        "platform": "Windows",
        "git_version": "git version 2.55.0.windows.5",
        "commands": ["gh api --method GET repos/owner/repo"],
    }
    fill(directory, manifest=manifest)
    lines, loaded = audit(directory)
    text = format_report(lines, loaded)
    assert "fetched_at: 2026-11-14T00:00:00Z" in text
    assert "platform: Windows" in text
    assert "git version 2.55.0.windows.5" in text
    assert "gh api --method GET repos/owner/repo" in text
    assert "không chứng minh máy chủ từ chối một lượt đẩy thật" in text
    assert "chưa kiểm, do OWNER tự kiểm" in text
    assert "Không lớp nào được mô tả là chặn tuyệt đối." in text
    assert "hidden@example.com" not in text
    assert text.count("\n") >= 9


def run_cli(args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
    )


def test_cli_exit_codes(tmp_path):
    directory = tmp_path / "cli input"
    fill(directory)
    passed = run_cli([str(directory), "--json"])
    assert passed.returncode == 0
    assert json.loads(passed.stdout)["lines"][0]["result"] == "PASS"
    missing = run_cli([str(tmp_path / "nope")])
    assert missing.returncode == 2
    fill(directory, repo={"allow_auto_merge": True})
    failed = run_cli([str(directory)])
    assert failed.returncode == 1
