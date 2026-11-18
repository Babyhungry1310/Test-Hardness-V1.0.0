import json

import pytest

from tools import github_audit


@pytest.fixture
def audit_snapshot(tmp_path, monkeypatch):
    data = {
        "repo": {"owner": {"login": "Owner", "id": 17, "type": "User"}},
        "user": {"login": "Owner"},
        "branch": {"protected": True},
        "protection": {"required_pull_request_reviews": {"require_code_owner_reviews": True}},
        "rulesets": [],
        "details": [],
        "manifest": {},
        "codeowners": "* @Owner",
        "protected_paths": None,
    }
    state = {key: "ok" for key in ("repo", "user", "branch", "protection", "rulesets", "codeowners")}
    state["ruleset_details"] = "ok"

    def load(directory):
        assert directory == tmp_path
        bundle = json.loads((directory / "snapshot.json").read_text(encoding="utf-8"))
        return bundle["data"], bundle["state"]

    monkeypatch.setattr(github_audit, "load", load)

    def run():
        bundle = {"data": data, "state": state}
        (tmp_path / "snapshot.json").write_text(json.dumps(bundle), encoding="utf-8")
        lines, manifest = github_audit.audit(tmp_path)
        return {number: (result, reason) for number, result, reason in lines}, github_audit.format_report(lines, manifest)

    return data, state, run


@pytest.mark.parametrize("login", ["Owner", "oWnEr"])
def test_confirmed_shared_account_reports_identity_limit(audit_snapshot, login):
    data, state, run = audit_snapshot
    data["user"]["login"] = login
    rows, report = run()
    assert rows[9] == (
        "PASS",
        "đang dùng tài khoản OWNER; trùng CODEOWNERS hữu hiệu; không phân biệt được OWNER với tác tử",
    )
    assert "không phân biệt được OWNER với tác tử" in report
    assert "cảnh báo: tự duyệt PR cùng tài khoản không khả thi" in rows[4][1]


@pytest.mark.parametrize("case,expected", [
    ("different_user", "FAIL"),
    ("missing_user", "UNKNOWN"),
    ("missing_repo", "UNKNOWN"),
    ("missing_owner", "UNKNOWN"),
    ("missing_login", "UNKNOWN"),
    ("missing_codeowners", "UNKNOWN"),
    ("other_codeowner", "FAIL"),
    ("comment_only", "FAIL"),
    ("overridden_owner", "FAIL"),
    ("uncertain_paths", "UNKNOWN"),
])
def test_unconfirmed_account_never_claims_shared_identity(audit_snapshot, case, expected):
    data, state, run = audit_snapshot
    if case == "different_user":
        data["user"]["login"] = "Agent"
    elif case in ("missing_user", "missing_repo"):
        key = case.removeprefix("missing_")
        data[key], state[key] = None, "missing"
    elif case == "missing_owner":
        data["repo"].pop("owner")
    elif case == "missing_login":
        data["user"].pop("login")
    elif case == "missing_codeowners":
        data["codeowners"], state["codeowners"] = "", "missing"
    else:
        data["codeowners"] = {
            "other_codeowner": "* @Agent",
            "comment_only": "# @Owner",
            "overridden_owner": "* @Owner\n* @Agent",
            "uncertain_paths": "/protected/ @Owner",
        }[case]
    rows, report = run()
    assert rows[9][0] == expected
    assert "trùng CODEOWNERS hữu hiệu" not in rows[9][1]
    assert "cảnh báo: tự duyệt PR cùng tài khoản không khả thi" not in rows[4][1]
    assert f"9 {expected} {rows[9][1]}" in report


@pytest.mark.parametrize("required,expected", [(True, "PASS"), (False, "FAIL"), (None, "UNKNOWN")])
@pytest.mark.parametrize("source", ["classic", "ruleset"])
def test_review_configuration_is_not_owner_approval(audit_snapshot, required, expected, source):
    data, state, run = audit_snapshot
    data["protection"]["required_pull_request_reviews"]["require_code_owner_reviews"] = required
    if source == "ruleset":
        data["protection"]["required_pull_request_reviews"]["require_code_owner_reviews"] = False
        data["details"] = [{
            "target": "branch", "enforcement": "active",
            "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
            "rules": [{"type": "pull_request", "parameters": {"require_code_owner_review": required}}],
            "bypass_actors": [],
        }]
    rows, report = run()
    assert rows[4][0] == expected
    assert rows[9][0] == "PASS"
    assert "cảnh báo: tự duyệt PR cùng tài khoản không khả thi" in rows[4][1]
    assert f"4 {expected} {rows[4][1]}" in report
    assert "Chỉ đọc cấu hình, không chứng minh máy chủ từ chối một lượt đẩy thật." in report
    assert "OWNER đã duyệt" not in report
    if required is True:
        assert rows[4][1].startswith(f"{source} bắt buộc duyệt của code owner;")
