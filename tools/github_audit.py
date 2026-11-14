import argparse
import json
import sys
from pathlib import Path


def read_json(path):
    if not path.is_file():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "invalid"
    if isinstance(data, dict):
        raw = data.get("http_status", data.get("status"))
        try:
            code = int(raw)
        except (TypeError, ValueError):
            code = None
        if code in (403, 404):
            return None, "denied"
    return data, "ok"


def flag(node):
    if isinstance(node, bool):
        return node
    if isinstance(node, dict) and isinstance(node.get("enabled"), bool):
        return node["enabled"]
    return None


def codeowner_logins(text):
    found = []
    for line in text.splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        for part in item.split():
            if part.startswith("@") and len(part) > 1:
                found.append(part[1:].lower())
    return found


def load(directory):
    root = Path(directory)
    data, state = {}, {}
    names = {
        "repo": "repo.json",
        "branch": "branch_main.json",
        "protection": "protection.json",
        "rulesets": "rulesets.json",
        "user": "user.json",
    }
    for key, name in names.items():
        data[key], state[key] = read_json(root / name)
    if state["rulesets"] == "ok" and not isinstance(data["rulesets"], list):
        data["rulesets"], state["rulesets"] = None, "invalid"
    code = root / "codeowners.txt"
    if not code.is_file():
        code = root / "CODEOWNERS"
    if code.is_file():
        data["codeowners"] = code.read_text(encoding="utf-8")
        state["codeowners"] = "ok"
    else:
        data["codeowners"], state["codeowners"] = "", "missing"
    details, missing = [], False
    if isinstance(data["rulesets"], list):
        for item in data["rulesets"]:
            if not isinstance(item, dict) or "id" not in item:
                continue
            detail, detail_state = read_json(root / f"ruleset_{item['id']}.json")
            if detail_state != "ok":
                missing = True
                continue
            details.append(detail)
        state["ruleset_details"] = "incomplete" if missing else "ok"
    else:
        state["ruleset_details"] = state["rulesets"]
    data["details"] = details
    manifest, manifest_state = read_json(root / "manifest.json")
    data["manifest"] = manifest if manifest_state == "ok" and isinstance(manifest, dict) else {}
    return data, state


def covers(detail, kind, needles):
    if not isinstance(detail, dict) or detail.get("enforcement") != "active":
        return False
    if detail.get("target") != kind:
        return False
    ref_name = (detail.get("conditions") or {}).get("ref_name") or {}
    include = ref_name.get("include") or []
    exclude = ref_name.get("exclude") or []
    if any(needle in exclude for needle in needles):
        return False
    for pattern in include:
        if not isinstance(pattern, str):
            continue
        for needle in needles:
            if pattern == needle or pattern.startswith(needle):
                return True
    return False


def rule_map(detail):
    found = {}
    for rule in detail.get("rules") or []:
        if isinstance(rule, dict) and isinstance(rule.get("type"), str):
            found[rule["type"]] = rule
    return found


def main_needles(data):
    needles = ["refs/heads/main"]
    repo = data["repo"] if isinstance(data["repo"], dict) else {}
    if repo.get("default_branch") == "main":
        needles.append("~DEFAULT_BRANCH")
    return needles


def main_rules(data):
    return [item for item in data["details"] if covers(item, "branch", main_needles(data))]


def tag_rules(data):
    needles = ["refs/tags/cycle/", "refs/tags/cycle/*", "refs/tags/cycle/**"]
    return [item for item in data["details"] if covers(item, "tag", needles)]


def known_rules(state):
    return state["rulesets"] == "ok" and state.get("ruleset_details") == "ok"


def classic(data, state):
    if state["protection"] == "ok" and isinstance(data["protection"], dict):
        return data["protection"]
    return None


def identity(data, state):
    user = data["user"] if state["user"] == "ok" and isinstance(data["user"], dict) else None
    repo = data["repo"] if state["repo"] == "ok" and isinstance(data["repo"], dict) else None
    if not user or not repo or not isinstance(repo.get("owner"), dict):
        return None
    login, owner = user.get("login"), repo["owner"].get("login")
    if not isinstance(login, str) or not isinstance(owner, str):
        return None
    owners = codeowner_logins(data["codeowners"]) if state["codeowners"] == "ok" else None
    return {
        "login": login,
        "owner": owner,
        "owner_id": repo["owner"].get("id"),
        "same": login.lower() == owner.lower(),
        "in_codeowners": None if owners is None else login.lower() in owners,
    }


def confirmed(ident):
    return bool(ident and ident["same"] and ident["in_codeowners"])


def unprotected(data, state):
    branch = data["branch"] if state["branch"] == "ok" and isinstance(data["branch"], dict) else None
    return branch is not None and branch.get("protected") is False


def line1(data, state):
    prot = classic(data, state)
    if prot is not None and isinstance(prot.get("required_pull_request_reviews"), dict):
        return "PASS", "classic bắt buộc qua PR"
    if any("pull_request" in rule_map(item) for item in main_rules(data)):
        return "PASS", "ruleset bắt buộc qua PR"
    classic_no = prot is not None and prot.get("required_pull_request_reviews") is None
    rules_no = known_rules(state) and not any("pull_request" in rule_map(item) for item in main_rules(data))
    if rules_no and (classic_no or unprotected(data, state)):
        return "FAIL", "không bắt buộc qua PR cho main"
    return "UNKNOWN", "không đọc được luật bắt buộc PR"


def line2(data, state):
    prot = classic(data, state)
    force = flag(prot.get("allow_force_pushes")) if prot else None
    delete = flag(prot.get("allow_deletions")) if prot else None
    if force is False and delete is False:
        return "PASS", "classic cấm ép đẩy và cấm xóa main"
    blocked = any(
        {"non_fast_forward", "deletion"} <= set(rule_map(item)) for item in main_rules(data)
    )
    if blocked:
        return "PASS", "ruleset cấm ép đẩy và cấm xóa main"
    classic_no = force is True or delete is True
    rules_no = known_rules(state) and not blocked
    if rules_no and (classic_no or unprotected(data, state)):
        return "FAIL", "chưa cấm ép đẩy hoặc chưa cấm xóa main"
    return "UNKNOWN", "không đọc được cấm ép đẩy hoặc cấm xóa"


def bypasses(detail):
    for actor in detail.get("bypass_actors") or []:
        if isinstance(actor, dict) and actor.get("bypass_mode", "always") in ("always", "exempt"):
            return True
    return False


def line3(data, state):
    prot = classic(data, state)
    enforced = None if prot is None else flag(prot.get("enforce_admins"))
    rules = main_rules(data)
    if any(bypasses(item) for item in rules):
        return "FAIL", "ruleset cho phép bỏ qua luật"
    if enforced is False:
        return "FAIL", "quản trị được bỏ qua luật"
    if known_rules(state) and enforced is True and not any(bypasses(item) for item in rules):
        return "PASS", "không cho bỏ qua, kể cả quản trị"
    if known_rules(state) and rules and enforced is None and not any(bypasses(item) for item in rules):
        return "PASS", "ruleset không cho bỏ qua"
    if known_rules(state) and not rules and (unprotected(data, state) or enforced is None):
        return "FAIL", "chưa bật luật chặn quản trị bỏ qua"
    return "UNKNOWN", "không đọc được quyền bỏ qua của quản trị"


def line4(data, state):
    prot = classic(data, state)
    classic_vote = None
    if prot is not None and isinstance(prot.get("required_pull_request_reviews"), dict):
        value = prot["required_pull_request_reviews"].get("require_code_owner_reviews")
        if value is True:
            return "PASS", "classic bắt buộc duyệt của code owner"
        if value is False:
            classic_vote = "no"
    for item in main_rules(data):
        rule = rule_map(item).get("pull_request") or {}
        if (rule.get("parameters") or {}).get("require_code_owner_review") is True:
            return "PASS", "ruleset bắt buộc duyệt của code owner"
    rules_no = known_rules(state) and not any(
        (rule_map(item).get("pull_request") or {}).get("parameters", {}).get("require_code_owner_review") is True
        for item in main_rules(data)
    )
    if rules_no and (classic_vote == "no" or unprotected(data, state) or (
        prot is not None and not isinstance(prot.get("required_pull_request_reviews"), dict)
    )):
        return "FAIL", "chưa bắt buộc duyệt của code owner"
    return "UNKNOWN", "không đọc được luật duyệt của code owner"


def line5(data, state, ident):
    if not known_rules(state):
        return "UNKNOWN", "không đọc được ruleset thẻ"
    owner_id = None if ident is None else ident.get("owner_id")
    matched = False
    for item in tag_rules(data):
        if not {"creation", "update", "deletion"} <= set(rule_map(item)):
            continue
        matched = True
        actors = item.get("bypass_actors") or []
        if not isinstance(owner_id, int):
            return "UNKNOWN", "không có id OWNER để đối chiếu ngoại lệ thẻ"
        if (
            len(actors) == 1
            and isinstance(actors[0], dict)
            and actors[0].get("actor_id") == owner_id
        ):
            return "PASS", "ruleset cycle/* chỉ OWNER được tạo, sửa, xóa"
    if matched:
        return "FAIL", "ruleset cycle/* không giới hạn đúng một tài khoản OWNER"
    return "FAIL", "không có luật thẻ cycle/*"


def line6(data, state):
    repo = data["repo"] if state["repo"] == "ok" and isinstance(data["repo"], dict) else None
    keys = ("allow_squash_merge", "allow_merge_commit", "allow_rebase_merge")
    if repo is None or any(key not in repo for key in keys):
        return "UNKNOWN", "không đọc được cách merge"
    if repo["allow_squash_merge"] is True and repo["allow_merge_commit"] is False and repo["allow_rebase_merge"] is False:
        return "PASS", "chỉ squash; merge commit tắt; rebase tắt"
    return (
        "FAIL",
        f"squash={repo['allow_squash_merge']} merge_commit={repo['allow_merge_commit']} rebase={repo['allow_rebase_merge']}",
    )


def line7(data, state):
    repo = data["repo"] if state["repo"] == "ok" and isinstance(data["repo"], dict) else None
    if repo is None or not isinstance(repo.get("allow_auto_merge"), bool):
        return "UNKNOWN", "không đọc được allow_auto_merge"
    if repo["allow_auto_merge"]:
        return "FAIL", "auto-merge bật"
    return "PASS", "auto-merge tắt"


def line8(data, state):
    repo = data["repo"] if state["repo"] == "ok" and isinstance(data["repo"], dict) else None
    if repo is None or not isinstance(repo.get("delete_branch_on_merge"), bool):
        return "UNKNOWN", "không đọc được delete_branch_on_merge"
    observed = "bật" if repo["delete_branch_on_merge"] else "tắt"
    return "PASS", f"giá trị quan sát {observed}; OWNER quyết; không đổi cài đặt"


def line9(ident, state):
    if ident is None:
        return "UNKNOWN", "không đọc được tài khoản đang dùng hoặc OWNER"
    if state["codeowners"] != "ok":
        return "UNKNOWN", "thiếu CODEOWNERS, không xác nhận tài khoản chung"
    if ident["same"] and ident["in_codeowners"]:
        return "PASS", "đang dùng tài khoản OWNER; trùng CODEOWNERS; không phân biệt được OWNER với tác tử"
    if not ident["same"]:
        return "FAIL", f"tài khoản đang dùng {ident['login']} khác OWNER {ident['owner']}"
    return "FAIL", f"tài khoản {ident['login']} không có trong CODEOWNERS"


def audit(directory):
    data, state = load(directory)
    ident = identity(data, state)
    lines = [
        (1, *line1(data, state)),
        (2, *line2(data, state)),
        (3, *line3(data, state)),
        (4, *line4(data, state)),
        (5, *line5(data, state, ident)),
        (6, *line6(data, state)),
        (7, *line7(data, state)),
        (8, *line8(data, state)),
        (9, *line9(ident, state)),
    ]
    if confirmed(ident):
        number, result, reason = lines[3]
        lines[3] = (number, result, reason + "; cảnh báo: tự duyệt PR cùng tài khoản không khả thi")
    return lines, data["manifest"]


def format_report(lines, manifest):
    commands = manifest.get("commands") or []
    rows = [
        "TK-0008 github audit",
        f"fetched_at: {manifest.get('fetched_at', 'UNKNOWN')}",
        f"platform: {manifest.get('platform', 'UNKNOWN')}",
        f"git_version: {manifest.get('git_version', 'UNKNOWN')}",
        "commands:",
    ]
    rows.extend(f"- {item}" for item in commands) if commands else rows.append("- UNKNOWN")
    rows.append("results:")
    rows.extend(f"{number} {result} {reason}" for number, result, reason in lines)
    rows.extend(
        [
            "limits:",
            "- Chỉ đọc cấu hình, không chứng minh máy chủ từ chối một lượt đẩy thật.",
            "- Tác tử không đẩy thử vào main hay thẻ. Phần máy chủ từ chối lượt đẩy thật: chưa kiểm, do OWNER tự kiểm.",
            "- Dùng chung tài khoản với OWNER thì luật không phân biệt được hai bên.",
            "- Quyền cần: đọc repo; đọc chi tiết luật nhánh có thể cần quyền quản trị, thiếu thì dòng đó là UNKNOWN.",
            "- Bật luật: quyền quản trị, chỉ OWNER. Lần kiểm này không đổi cài đặt.",
            "- Không lớp nào được mô tả là chặn tuyệt đối.",
        ]
    )
    return "\n".join(rows) + "\n"


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass
    parser = argparse.ArgumentParser(prog="github_audit")
    parser.add_argument("directory")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    directory = Path(args.directory)
    if not directory.is_dir():
        print("error: input directory missing", file=sys.stderr)
        return 2
    try:
        lines, manifest = audit(directory)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        payload = {"lines": [{"n": number, "result": result, "reason": reason} for number, result, reason in lines]}
        print(json.dumps(payload, ensure_ascii=False))
    else:
        for number, result, reason in lines:
            print(f"{number} {result} {reason}")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(format_report(lines, manifest), encoding="utf-8", newline="\n")
    if any(result != "PASS" for _, result, _ in lines):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
