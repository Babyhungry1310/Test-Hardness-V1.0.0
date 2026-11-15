import argparse
import json
import sys
from pathlib import Path

ACTOR_TYPES = {"Integration", "OrganizationAdmin", "RepositoryRole", "Team", "DeployKey", "User"}
BRANCH_MODES = {"always", "pull_request", "exempt"}
TAG_MODES = {"always", "exempt"}
NEED_PROTECTION = "cần GET repos/{owner}/{repo}/branches/main/protection, quyền đọc luật nhánh, có thể cần quản trị"
NEED_RULESET = "cần GET repos/{owner}/{repo}/rulesets và ruleset/{id} gồm target, enforcement, conditions, rules, bypass_actors"
NEED_TAG = "cần ruleset tag phủ hết refs/tags/cycle/*, actor_type User, actor_id trùng owner.id, owner.type User, bypass_mode always hoặc exempt"


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


def strip_codeowner_comment(line):
    return line.split("#", 1)[0].strip()


def parse_codeowners(text):
    rules = []
    for raw in text.splitlines():
        line = strip_codeowner_comment(raw)
        if not line:
            continue
        parts = line.split()
        owners = [part[1:].lower() for part in parts[1:] if part.startswith("@") and len(part) > 1]
        rules.append((parts[0], owners))
    return rules


def dir_status(base, right, anywhere):
    base_parts = [part for part in base.strip("/").split("/") if part]
    right_parts = [part for part in right.strip("/").split("/") if part]
    if not base_parts:
        return None
    width = len(base_parts)
    if not anywhere:
        if right_parts[:width] != base_parts:
            return False
        if len(right_parts) > width or right.endswith("/"):
            return True
        return None
    proven = False
    ambiguous = False
    for index in range(len(right_parts) - width + 1):
        if right_parts[index:index + width] != base_parts:
            continue
        if index + width < len(right_parts) or right.endswith("/"):
            proven = True
        else:
            ambiguous = True
    if proven:
        return True
    if ambiguous:
        return None
    return False


def co_match(pattern, path):
    if any(char in pattern for char in "[]\\?") or "**" in pattern:
        return None
    if pattern in ("*", "/*"):
        return True
    anchored = pattern.startswith("/")
    left = pattern[1:] if anchored else pattern
    right = path[1:] if path.startswith("/") else path
    body = left[:-1] if left.endswith("/") else left
    root_relative = anchored or "/" in body
    if "*" in left:
        if left.endswith("/") or not anchored:
            return None
        return glob_match(left, right)
    if left.endswith("/"):
        base = left.rstrip("/")
        if not base:
            return None
        return dir_status(base, right, anywhere=not root_relative)
    if root_relative:
        return right == left or right.startswith(left + "/")
    return left in right.split("/")


def glob_match(pattern, text):
    if "**" in pattern:
        return glob_match_cross(pattern, text)
    parts = pattern.split("*")
    if len(parts) == 1:
        return pattern == text
    if "/" in pattern and any("/" in piece for piece in parts[1:-1]):
        return False
    index = 0
    for i, piece in enumerate(parts):
        if "/" in piece and i not in (0, len(parts) - 1):
            return False
        if i == 0:
            if not text.startswith(piece):
                return False
            index = len(piece)
            continue
        if i == len(parts) - 1:
            return text.endswith(piece) and index + len(piece) <= len(text) and "/" not in text[index:len(text) - len(piece)]
        found = text.find(piece, index)
        if found < 0 or "/" in text[index:found]:
            return False
        index = found + len(piece)
    return True


def glob_match_cross(pattern, text):
    chunks = pattern.split("**")
    index = 0
    for i, chunk in enumerate(chunks):
        if i == 0:
            if chunk and not text.startswith(chunk):
                return False
            index = len(chunk)
            continue
        if i == len(chunks) - 1:
            return text.endswith(chunk) and index <= len(text) - len(chunk) if chunk else True
        found = text.find(chunk, index)
        if found < 0:
            return False
        index = found + len(chunk)
    return True


def pattern_hit(pattern, ref, default_branch, target):
    if not isinstance(pattern, str) or not pattern:
        return "unknown"
    if pattern == "~ALL":
        return "yes"
    if pattern == "~DEFAULT_BRANCH":
        if target != "branch" or not default_branch:
            return "no" if target != "branch" else "unknown"
        return "yes" if ref == f"refs/heads/{default_branch}" else "no"
    if pattern.startswith("~") or any(char in pattern for char in "[]{}\\?"):
        return "unknown"
    if glob_match(pattern, ref):
        return "yes"
    return "no"


def glob_covers(pattern, required):
    if not isinstance(pattern, str):
        return "unknown"
    if pattern == "~ALL":
        return "yes"
    if pattern == "~DEFAULT_BRANCH" or pattern.startswith("~"):
        return "no" if pattern == "~DEFAULT_BRANCH" else "unknown"
    if any(char in pattern for char in "[]{}\\"):
        return "unknown"
    if "**" in pattern:
        prefix, suffix = pattern.split("**", 1)
        if suffix:
            return "unknown"
        return "yes" if required.startswith(prefix) else "no"
    pseg = pattern.split("/")
    rseg = required.split("/")
    if len(pseg) != len(rseg):
        return "no"
    for left, right in zip(pseg, rseg):
        if left == "*":
            continue
        if right == "*" or left != right:
            return "no"
    return "yes"


def exclude_hits_prefix(pattern, prefix):
    if pattern == "~ALL":
        return "yes"
    if not isinstance(pattern, str) or pattern.startswith("~") or any(char in pattern for char in "[]{}\\"):
        return "unknown"
    if "**" in pattern or "*" in pattern or "?" in pattern:
        return "unknown"
    if pattern.startswith(prefix):
        return "yes"
    return "no"


def ref_name(detail):
    if not isinstance(detail, dict) or "conditions" not in detail:
        return None
    conditions = detail.get("conditions")
    if not isinstance(conditions, dict) or "ref_name" not in conditions:
        return None
    node = conditions.get("ref_name")
    if not isinstance(node, dict):
        return None
    return node


def pattern_lists(node):
    if not isinstance(node, dict) or not isinstance(node.get("include"), list):
        return None
    if "exclude" in node and not isinstance(node.get("exclude"), list):
        return None
    exclude = node.get("exclude", [])
    if not isinstance(exclude, list):
        return None
    if any(not isinstance(item, str) for item in node["include"]) or any(not isinstance(item, str) for item in exclude):
        return None
    return node["include"], exclude


def applies_exact(detail, kind, ref, default_branch):
    if not isinstance(detail, dict):
        return "unknown"
    target, enforcement = detail.get("target"), detail.get("enforcement")
    if not isinstance(target, str) or not isinstance(enforcement, str):
        return "unknown"
    if target != kind:
        return "no"
    if enforcement != "active":
        return "no" if enforcement in ("disabled", "evaluate") else "unknown"
    node = ref_name(detail)
    lists = pattern_lists(node)
    if lists is None:
        return "unknown"
    include, exclude = lists
    seen = "no"
    for pattern in include:
        hit = pattern_hit(pattern, ref, default_branch, kind)
        if hit == "yes":
            seen = "yes"
            break
        if hit == "unknown":
            seen = "unknown"
    if seen != "yes":
        return seen
    for pattern in exclude:
        hit = pattern_hit(pattern, ref, default_branch, kind)
        if hit == "yes":
            return "no"
        if hit == "unknown":
            return "unknown"
    return "yes"


def covers_cycle(detail):
    if not isinstance(detail, dict):
        return "unknown"
    target, enforcement = detail.get("target"), detail.get("enforcement")
    if not isinstance(target, str) or not isinstance(enforcement, str):
        return "unknown"
    if target != "tag":
        return "no"
    if enforcement != "active":
        return "no" if enforcement in ("disabled", "evaluate") else "unknown"
    node = ref_name(detail)
    lists = pattern_lists(node)
    if lists is None:
        return "unknown"
    include, exclude = lists
    covered = "no"
    for pattern in include:
        hit = glob_covers(pattern, "refs/tags/cycle/*")
        if hit == "yes":
            covered = "yes"
            break
        if hit == "unknown":
            covered = "unknown"
    if covered != "yes":
        return covered
    for pattern in exclude:
        hit = exclude_hits_prefix(pattern, "refs/tags/cycle/")
        if hit == "yes":
            return "no"
        if hit == "unknown":
            return "unknown"
    return "yes"


def rule_map(detail):
    if not isinstance(detail, dict) or "rules" not in detail:
        return None
    rules = detail.get("rules")
    if not isinstance(rules, list):
        return None
    found = {}
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("type"), str):
            return None
        found[rule["type"]] = rule
    return found


def fields_known(detail):
    return isinstance(detail, dict) and "rules" in detail and "bypass_actors" in detail


def detail_structure_bad(detail):
    if not isinstance(detail, dict):
        return True
    conditions = detail.get("conditions")
    if "conditions" in detail and not isinstance(conditions, dict):
        return True
    node = conditions.get("ref_name") if isinstance(conditions, dict) else None
    if isinstance(conditions, dict) and "ref_name" in conditions and not isinstance(node, dict):
        return True
    if isinstance(node, dict):
        if "include" in node and not isinstance(node.get("include"), list):
            return True
        if "exclude" in node and not isinstance(node.get("exclude"), list):
            return True
    rules = detail.get("rules")
    if "rules" in detail and not isinstance(rules, list):
        return True
    if isinstance(rules, list) and any(not isinstance(rule, dict) or not isinstance(rule.get("type"), str) for rule in rules):
        return True
    if "bypass_actors" in detail and not isinstance(detail.get("bypass_actors"), list):
        return True
    return False


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
    paths = root / "protected_paths.txt"
    if paths.is_file():
        data["protected_paths"] = [strip_codeowner_comment(line) for line in paths.read_text(encoding="utf-8").splitlines()]
        data["protected_paths"] = [item for item in data["protected_paths"] if item]
    else:
        data["protected_paths"] = None
    details, missing = [], False
    if isinstance(data["rulesets"], list):
        for item in data["rulesets"]:
            if not isinstance(item, dict) or not isinstance(item.get("id"), (int, str)):
                missing = True
                continue
            detail, detail_state = read_json(root / f"ruleset_{item['id']}.json")
            if detail_state != "ok" or not isinstance(detail, dict):
                missing = True
                continue
            if detail_structure_bad(detail):
                missing = True
            details.append(detail)
        state["ruleset_details"] = "incomplete" if missing else "ok"
    else:
        state["ruleset_details"] = state["rulesets"]
    data["details"] = details
    manifest, manifest_state = read_json(root / "manifest.json")
    data["manifest"] = manifest if manifest_state == "ok" and isinstance(manifest, dict) else {}
    return data, state


def default_branch(data):
    repo = data["repo"] if isinstance(data["repo"], dict) else {}
    branch = repo.get("default_branch")
    return branch if isinstance(branch, str) else None


def known_rules(state):
    return state["rulesets"] == "ok" and state.get("ruleset_details") == "ok"


def classic(data, state):
    if state["protection"] == "ok" and isinstance(data["protection"], dict):
        return data["protection"]
    return None


def branch_flag(data, state):
    branch = data["branch"] if state["branch"] == "ok" and isinstance(data["branch"], dict) else None
    if branch is None or not isinstance(branch.get("protected"), bool):
        return None
    return branch["protected"]


def effective_owners(text, protected_paths):
    rules = parse_codeowners(text)
    if not rules:
        return set(), "empty"
    if any(any(char in pattern for char in "[]\\") for pattern, _owners in rules):
        return None, "uncertain"
    if not protected_paths:
        if all(pattern in ("*", "/*") for pattern, _owners in rules):
            return set(rules[-1][1]), "ok"
        return None, "need-protected-paths"
    chosen_sets = []
    for path in protected_paths:
        chosen = None
        for pattern, owners in rules:
            hit = co_match(pattern, path)
            if hit is None:
                return None, "uncertain"
            if hit:
                chosen = owners
        if chosen is None:
            return set(), "uncovered"
        chosen_sets.append(set(chosen))
    if not chosen_sets:
        return set(), "empty"
    owners = chosen_sets[0]
    for item in chosen_sets[1:]:
        owners = owners & item
    return owners, "ok"


def identity(data, state):
    user = data["user"] if state["user"] == "ok" and isinstance(data["user"], dict) else None
    repo = data["repo"] if state["repo"] == "ok" and isinstance(data["repo"], dict) else None
    if not user or not repo or not isinstance(repo.get("owner"), dict):
        return None
    login, owner = user.get("login"), repo["owner"].get("login")
    if not isinstance(login, str) or not isinstance(owner, str):
        return None
    owners, how = (None, "missing")
    if state["codeowners"] == "ok":
        owners, how = effective_owners(data["codeowners"], data.get("protected_paths"))
    return {
        "login": login,
        "owner": owner,
        "owner_id": repo["owner"].get("id"),
        "owner_type": repo["owner"].get("type"),
        "same": login.lower() == owner.lower(),
        "in_codeowners": None if owners is None else login.lower() in owners,
        "codeowners_how": how,
    }


def confirmed(ident):
    return bool(ident and ident["same"] and ident["in_codeowners"])


def main_status(data):
    branch = default_branch(data)
    statuses = []
    for detail in data["details"]:
        statuses.append((detail, applies_exact(detail, "branch", "refs/heads/main", branch)))
    return statuses


def line1(data, state):
    prot = classic(data, state)
    if prot is not None and isinstance(prot.get("required_pull_request_reviews"), dict):
        return "PASS", "classic bắt buộc qua PR"
    uncertain = False
    for detail, status in main_status(data):
        if status == "unknown":
            uncertain = True
            continue
        if status != "yes":
            continue
        rules = rule_map(detail)
        if rules is None:
            uncertain = True
            continue
        if "pull_request" in rules:
            return "PASS", "ruleset bắt buộc qua PR"
    classic_no = prot is not None and prot.get("required_pull_request_reviews") is None
    rules_known = known_rules(state) and not uncertain
    if rules_known and (classic_no or branch_flag(data, state) is False):
        return "FAIL", "không bắt buộc qua PR cho main"
    return "UNKNOWN", NEED_PROTECTION + "; hoặc " + NEED_RULESET + " có rule pull_request cho refs/heads/main"


def line2(data, state):
    prot = classic(data, state)
    force = flag(prot.get("allow_force_pushes")) if prot else None
    delete = flag(prot.get("allow_deletions")) if prot else None
    if force is False and delete is False:
        return "PASS", "classic cấm ép đẩy và cấm xóa main"
    uncertain = False
    for detail, status in main_status(data):
        if status == "unknown":
            uncertain = True
            continue
        if status != "yes":
            continue
        rules = rule_map(detail)
        if rules is None:
            uncertain = True
            continue
        if "non_fast_forward" in rules and "deletion" in rules:
            return "PASS", "ruleset cấm ép đẩy và cấm xóa main"
    classic_no = force is True or delete is True
    if known_rules(state) and not uncertain and (classic_no or branch_flag(data, state) is False):
        return "FAIL", "chưa cấm ép đẩy hoặc chưa cấm xóa main"
    return "UNKNOWN", NEED_PROTECTION + " với allow_force_pushes và allow_deletions"


def bypasses(detail):
    if not fields_known(detail):
        return "unknown"
    actors = detail.get("bypass_actors")
    if not isinstance(actors, list):
        return "unknown"
    for actor in actors:
        if not isinstance(actor, dict):
            return "unknown"
        if "actor_id" in actor and type(actor.get("actor_id")) is not int:
            return "unknown"
        if "actor_type" in actor and not isinstance(actor.get("actor_type"), str):
            return "unknown"
        mode = actor.get("bypass_mode", "always")
        if not isinstance(mode, str) or mode not in BRANCH_MODES:
            return "unknown"
    if actors:
        return "yes"
    return "no"


def classic_bypass_status(prot):
    if prot is None or not isinstance(prot.get("required_pull_request_reviews"), dict):
        return "skip"
    reviews = prot["required_pull_request_reviews"]
    if "bypass_pull_request_allowances" not in reviews:
        return "unknown"
    bypass = reviews.get("bypass_pull_request_allowances")
    if not isinstance(bypass, dict):
        return "unknown"
    found = []
    for key in ("users", "teams", "apps"):
        if key not in bypass or not isinstance(bypass.get(key), list):
            return "unknown"
        found.extend(bypass[key])
    if found:
        return "fail"
    return "ok"


def line3(data, state):
    prot = classic(data, state)
    enforced = None if prot is None else flag(prot.get("enforce_admins"))
    if enforced is False:
        return "FAIL", "quản trị được bỏ qua luật"
    classic_ba = classic_bypass_status(prot)
    if classic_ba == "fail":
        return "FAIL", "classic bypass_pull_request_allowances có actors"
    if classic_ba == "unknown":
        return "UNKNOWN", NEED_PROTECTION + " trường bypass_pull_request_allowances.users/teams/apps phải là list"
    uncertain = not known_rules(state)
    applicable = False
    for detail, status in main_status(data):
        if status == "unknown":
            uncertain = True
            continue
        if status != "yes":
            continue
        applicable = True
        if not fields_known(detail):
            return "UNKNOWN", NEED_RULESET + "; detail thiếu rules hoặc bypass_actors"
        found = bypasses(detail)
        if found == "yes":
            return "FAIL", "ruleset cho phép bỏ qua luật, kể cả bypass_mode pull_request"
        if found == "unknown":
            return "UNKNOWN", NEED_RULESET + "; bypass_actors không đủ actor_type hoặc bypass_mode"
    if state.get("ruleset_details") == "incomplete":
        return "UNKNOWN", NEED_RULESET + "; rulesets thiếu id hoặc detail sai cấu trúc"
    protected = branch_flag(data, state)
    if known_rules(state) and not uncertain and applicable:
        if enforced is True:
            return "PASS", "ruleset không cho bỏ qua; enforce_admins bật"
        if protected is False:
            return "PASS", "ruleset không cho bỏ qua; main không bảo vệ classic"
        return "UNKNOWN", NEED_PROTECTION + " trường enforce_admins"
    if known_rules(state) and not uncertain and not applicable and enforced is True:
        return "PASS", "không cho bỏ qua, kể cả quản trị"
    if known_rules(state) and not uncertain and not applicable and protected is False:
        return "FAIL", "chưa bật luật chặn quản trị bỏ qua"
    if protected is True and (state["protection"] in ("missing", "denied", "invalid") or enforced is None):
        return "UNKNOWN", NEED_PROTECTION + " trường enforce_admins; ruleset rỗng không chứng minh khi main protected=true"
    return "UNKNOWN", NEED_PROTECTION + " trường enforce_admins"


def line4(data, state):
    prot = classic(data, state)
    classic_no = False
    if prot is not None and isinstance(prot.get("required_pull_request_reviews"), dict):
        value = prot["required_pull_request_reviews"].get("require_code_owner_reviews")
        if value is True:
            return "PASS", "classic bắt buộc duyệt của code owner"
        if value is False:
            classic_no = True
    uncertain = False
    for detail, status in main_status(data):
        if status == "unknown":
            uncertain = True
            continue
        if status != "yes":
            continue
        rules = rule_map(detail)
        if rules is None:
            uncertain = True
            continue
        if "pull_request" in rules:
            pull = rules.get("pull_request")
            params = pull.get("parameters") if isinstance(pull, dict) else None
            if not isinstance(pull, dict) or "parameters" not in pull or not isinstance(params, dict):
                uncertain = True
                continue
            if "require_code_owner_review" not in params or type(params.get("require_code_owner_review")) is not bool:
                uncertain = True
                continue
            if params["require_code_owner_review"] is True:
                return "PASS", "ruleset bắt buộc duyệt của code owner"
    if known_rules(state) and not uncertain and (classic_no or branch_flag(data, state) is False or (
        prot is not None and not isinstance(prot.get("required_pull_request_reviews"), dict)
    )):
        return "FAIL", "chưa bắt buộc duyệt của code owner"
    return "UNKNOWN", NEED_PROTECTION + " trường require_code_owner_reviews"


def owner_bypass(detail, ident):
    if not fields_known(detail):
        return "unknown", NEED_RULESET
    actors = detail.get("bypass_actors")
    if not isinstance(actors, list):
        return "unknown", NEED_RULESET
    if len(actors) != 1 or not isinstance(actors[0], dict):
        return "no", "bypass_actors không phải đúng một actor"
    actor = actors[0]
    kind = actor.get("actor_type")
    if not isinstance(kind, str) or kind not in ACTOR_TYPES:
        return "unknown", "cần actor_type là str thuộc schema GitHub: " + ", ".join(sorted(ACTOR_TYPES))
    mode = actor.get("bypass_mode", "always")
    if not isinstance(mode, str) or mode not in TAG_MODES:
        return "unknown", "cần bypass_mode là str always hoặc exempt cho thẻ; pull_request chỉ áp dụng branch ruleset"
    if kind != "User":
        if kind == "RepositoryRole":
            return "unknown", "schema GitHub GET không xác nhận RepositoryRole id là chỉ OWNER; cần actor_type User và actor_id trùng owner.id"
        return "no", f"actor_type {kind} không phải tài khoản OWNER"
    if ident is None or not isinstance(ident.get("owner_id"), int) or ident.get("owner_type") != "User":
        return "unknown", "cần repo.owner.id, repo.owner.type User và actor_id trùng owner.id"
    if actor.get("actor_id") != ident["owner_id"]:
        return "no", "actor_id không trùng OWNER"
    return "yes", "actor_type User trùng owner.id; bypass_mode cho phép tạo, sửa, xóa"


def line5(data, state, ident):
    if not known_rules(state):
        return "UNKNOWN", NEED_TAG
    if not data["details"] and state["rulesets"] == "ok":
        return "FAIL", "không có luật thẻ cycle/*"
    uncertain = False
    saw_rule = False
    for detail in data["details"]:
        status = covers_cycle(detail)
        if status == "unknown":
            uncertain = True
            continue
        if status != "yes":
            continue
        rules = rule_map(detail)
        if rules is None:
            return "UNKNOWN", NEED_TAG
        if not {"creation", "update", "deletion"} <= set(rules):
            continue
        saw_rule = True
        verdict, reason = owner_bypass(detail, ident)
        if verdict == "yes":
            return "PASS", "ruleset cycle/* chỉ OWNER được tạo, sửa, xóa; " + reason
        if verdict == "unknown":
            return "UNKNOWN", reason
        return "FAIL", reason
    if uncertain:
        return "UNKNOWN", NEED_TAG
    if saw_rule:
        return "FAIL", "ruleset cycle/* không giới hạn đúng tài khoản OWNER"
    return "FAIL", "không có luật thẻ cycle/*"


def repo_of(data, state):
    if state["repo"] == "ok" and isinstance(data["repo"], dict):
        return data["repo"]
    return None


def line6(data, state):
    repo = repo_of(data, state)
    keys = ("allow_squash_merge", "allow_merge_commit", "allow_rebase_merge")
    if repo is None or any(key not in repo for key in keys):
        return "UNKNOWN", "cần repo.json từ GET repos/{owner}/{repo} với allow_squash_merge, allow_merge_commit, allow_rebase_merge"
    if repo["allow_squash_merge"] is True and repo["allow_merge_commit"] is False and repo["allow_rebase_merge"] is False:
        return "PASS", "chỉ squash; merge commit tắt; rebase tắt"
    return (
        "FAIL",
        f"squash={repo['allow_squash_merge']} merge_commit={repo['allow_merge_commit']} rebase={repo['allow_rebase_merge']}",
    )


def line7(data, state):
    repo = repo_of(data, state)
    if repo is None or not isinstance(repo.get("allow_auto_merge"), bool):
        return "UNKNOWN", "cần repo.json trường allow_auto_merge từ GET repos/{owner}/{repo}"
    if repo["allow_auto_merge"]:
        return "FAIL", "auto-merge bật"
    return "PASS", "auto-merge tắt"


def line8(data, state):
    repo = repo_of(data, state)
    if repo is None or not isinstance(repo.get("delete_branch_on_merge"), bool):
        return "UNKNOWN", "cần repo.json trường delete_branch_on_merge từ GET repos/{owner}/{repo}"
    observed = "bật" if repo["delete_branch_on_merge"] else "tắt"
    return "PASS", f"giá trị quan sát {observed}; OWNER quyết; không đổi cài đặt"


def line9(ident, state):
    if ident is None:
        return "UNKNOWN", "cần user.json từ GET user và repo.json owner.login từ GET repos/{owner}/{repo}"
    if not ident["same"]:
        return "FAIL", f"tài khoản đang dùng {ident['login']} khác OWNER {ident['owner']}"
    if state["codeowners"] != "ok":
        return "UNKNOWN", "cần nội dung .github/CODEOWNERS để xác nhận tài khoản chung"
    if ident["in_codeowners"] is None:
        if ident.get("codeowners_how") == "need-protected-paths":
            return "UNKNOWN", "cần protected_paths để xác nhận CODEOWNERS hữu hiệu; không suy từ '/'"
        return "UNKNOWN", "cần CODEOWNERS hữu hiệu cho đường dẫn bảo vệ; mention trong comment hoặc bị ghi đè không tính"
    if ident["in_codeowners"]:
        return "PASS", "đang dùng tài khoản OWNER; trùng CODEOWNERS hữu hiệu; không phân biệt được OWNER với tác tử"
    return "FAIL", f"tài khoản {ident['login']} không có trong CODEOWNERS hữu hiệu"


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
