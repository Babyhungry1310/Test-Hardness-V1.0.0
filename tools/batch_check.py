import argparse
import json
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tools.model_check import anchor_body, load_front_matter

TASK_ID = re.compile(r"TK-\d{4}")
CYCLE_ID = re.compile(r"CYC-\d{2}")
BATCH_LINE = re.compile(r"^- (?P<batch>B\d+) \| tasks: (?P<tasks>.+?) \| after: (?P<after>\S+)\s*$")
PLAN_TASK = re.compile(r"^- (TK-\d{4}) \|")
SHARED_NAMES = {
    "pytest.ini",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "tox.ini",
    "package.json",
    "cargo.toml",
    "go.mod",
    "gemfile",
    "composer.json",
    "requirements.txt",
    "pipfile",
    "environment.yml",
    "conftest.py",
    "index.md",
    "index.json",
}
LOCK_NAMES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "cargo.lock",
    "gemfile.lock",
    "composer.lock",
    "poetry.lock",
    "pipfile.lock",
    "uv.lock",
    "packages.lock.json",
}


def issue(rule, message, tasks=None, paths=None):
    item = {"rule": rule, "message": message}
    if tasks:
        item["tasks"] = list(tasks)
    if paths:
        item["paths"] = list(paths)
    return item


def normalize_scope(value):
    text = str(value).strip().replace("\\", "/")
    while text.startswith("./"):
        text = text[2:]
    text = text.lstrip("/")
    is_dir = text.endswith("/")
    text = text.rstrip("/")
    parts = [part for part in text.split("/") if part not in ("", ".")]
    cleaned = []
    for part in parts:
        if part == "..":
            if cleaned:
                cleaned.pop()
            continue
        cleaned.append(part)
    path = "/".join(cleaned)
    if is_dir and path:
        path += "/"
    return path


def is_dir_scope(path):
    return path.endswith("/")


def covers(scope, other):
    if scope == other:
        return True
    if is_dir_scope(scope) and (other == scope[:-1] or other.startswith(scope)):
        return True
    return False


def scopes_overlap(left, right):
    return covers(left, right) or covers(right, left)


def shared_path(path):
    name = path.rstrip("/").split("/")[-1].lower()
    if name in SHARED_NAMES or name in LOCK_NAMES:
        return True
    if name.endswith(".lock") or name.endswith("-lock.json"):
        return True
    return False


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def pointer_path(value):
    text = str(value).strip().replace("\\", "/")
    head = text.partition("#")[0].strip()
    if not head or "://" in head:
        return None
    if TASK_ID.fullmatch(head) or CYCLE_ID.fullmatch(head):
        return None
    if re.fullmatch(r"(?:DEC|RSK|REQ|SRC|RVW|DSC)-\S+", head):
        return None
    return normalize_scope(head)


def task_ids_in(value):
    return set(TASK_ID.findall(str(value)))


def text_mentions_path(text, scope):
    needle = scope.rstrip('/')
    if not needle:
        return False
    folded = str(text).replace('\\', '/')
    pattern = r'(?<![A-Za-z0-9_.-])' + re.escape(needle) + r'(?![A-Za-z0-9_.-])'
    return re.search(pattern, folded) is not None


def parse_batches(body, cycle):
    anchor = cycle.replace("-", "_") + "_BATCHES"
    chunk = anchor_body(body, anchor)
    if chunk is None:
        return None, []
    batches = []
    errors = []
    for raw in chunk.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = BATCH_LINE.fullmatch(line)
        if not match:
            errors.append(issue(4, "malformed batch line: " + line))
            continue
        tasks = [item.strip() for item in match.group("tasks").split(",") if item.strip()]
        batches.append({
            "id": match.group("batch"),
            "tasks": tasks,
            "after": match.group("after"),
        })
    return batches, errors


def plan_tasks(body, cycle):
    anchor = cycle.replace("-", "_")
    chunk = anchor_body(body, anchor)
    if chunk is None:
        return None
    found = []
    for raw in chunk.splitlines():
        match = PLAN_TASK.match(raw.strip())
        if match:
            found.append(match.group(1))
    return found


def load_plan(path):
    _data, body = load_front_matter(path)
    cycles = []
    for match in re.finditer(r"<!-- ANCHOR: (CYC_\d{2}) -->", body):
        cycles.append(match.group(1).replace("_", "-"))
    return body, cycles


def load_tasks(tasks_dir):
    root = Path(tasks_dir)
    loaded = {}
    errors = []
    if not root.is_dir():
        return loaded, [issue(0, "tasks directory missing")]
    for path in sorted(root.rglob("TK-*.md")):
        try:
            data, _body = load_front_matter(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(issue(0, str(exc) + ": " + path.name))
            continue
        task_id = data.get("id") or path.stem
        loaded[task_id] = {
            "id": task_id,
            "cycle": path.parent.name,
            "path": str(path).replace("\\", "/"),
            "write_scope": [normalize_scope(item) for item in as_list(data.get("write_scope"))],
            "depends_on": [str(item) for item in as_list(data.get("depends_on"))],
            "inputs": [str(item) for item in as_list(data.get("inputs"))],
            "read_also": [str(item) for item in as_list(data.get("read_also"))],
        }
    return loaded, errors


def reaches(batches, start, target, seen=None):
    if seen is None:
        seen = set()
    if start in seen:
        return False
    seen.add(start)
    after = batches[start]["after"]
    if after == "none":
        return False
    if after == target:
        return True
    if after not in batches:
        return False
    return reaches(batches, after, target, seen)


def check_cycle(cycle, body, tasks):
    planned = plan_tasks(body, cycle)
    batches, errors = parse_batches(body, cycle)
    if planned is None:
        return [issue(4, cycle + " missing plan anchor")]
    if batches is None:
        return [issue(4, cycle + " sequential", tasks=planned)]
    violations = list(errors)
    by_id = {batch["id"]: batch for batch in batches}
    membership = {}
    for batch in batches:
        if batch["after"] != "none" and batch["after"] not in by_id:
            violations.append(issue(4, "after points at missing batch " + batch["after"], tasks=batch["tasks"]))
        if len(batch["tasks"]) != len(set(batch["tasks"])):
            violations.append(issue(4, batch["id"] + " lists a task twice", tasks=batch["tasks"]))
        for task_id in batch["tasks"]:
            membership.setdefault(task_id, []).append(batch["id"])
    for task_id in planned:
        found = membership.get(task_id, [])
        if len(found) != 1:
            violations.append(issue(4, task_id + " belongs to " + str(len(found)) + " batches", tasks=[task_id]))
    for task_id, found in membership.items():
        if task_id not in planned and len(found) > 1:
            violations.append(issue(4, task_id + " belongs to " + str(len(found)) + " batches", tasks=[task_id]))
    batch_of = {}
    for task_id, found in membership.items():
        if len(found) == 1:
            batch_of[task_id] = found[0]
    for batch in batches:
        members = []
        for task_id in batch["tasks"]:
            task = tasks.get(task_id)
            if task is None:
                violations.append(issue(4, "missing task file " + task_id, tasks=[task_id]))
                continue
            if task["cycle"] == cycle or task["cycle"] == "":
                members.append(task)
        for index, left in enumerate(members):
            for right in members[index + 1:]:
                violations.extend(pair_issues(left, right, tasks))
        owned = {}
        for task in members:
            for path in task["write_scope"]:
                if shared_path(path):
                    owned.setdefault(path, []).append(task["id"])
        for path, owners in owned.items():
            if len(owners) > 1:
                violations.append(issue(3, "shared file in more than one task", tasks=owners, paths=[path]))
    for task_id in planned:
        task = tasks.get(task_id)
        if task is None or task_id not in batch_of:
            continue
        here = batch_of[task_id]
        for dep in task["depends_on"]:
            if not TASK_ID.fullmatch(dep):
                continue
            other = tasks.get(dep)
            if other is None or other["cycle"] != cycle:
                continue
            dep_batch = batch_of.get(dep)
            if dep_batch is None or dep_batch == here:
                continue
            if not reaches(by_id, here, dep_batch):
                violations.append(issue(4, task_id + " depends on " + dep + " but batch does not follow", tasks=[task_id, dep]))
    return violations


def read_hits(pointer, scopes):
    path = pointer_path(pointer)
    if not path:
        return None
    for scope in scopes:
        if path == scope or path == scope.rstrip("/"):
            return path
        if covers(scope, path) or covers(path, scope):
            return path
        if is_dir_scope(scope) and path.startswith(scope):
            return path
    return None



def scopes_named_in(text, task, other, tasks):
    foreign = set()
    for item in (tasks or {}).values():
        if item.get("id") in (task.get("id"), other.get("id")):
            continue
        if item.get("cycle") != task.get("cycle"):
            continue
        foreign.update(item.get("write_scope") or [])
    hits = []
    for scope in task["write_scope"]:
        if scope in foreign:
            continue
        if text_mentions_path(text, scope):
            hits.append(scope)
    return hits


def pair_issues(left, right, tasks=None):
    found = []
    left_id = left["id"]
    right_id = right["id"]
    pair = [left_id, right_id]
    overlaps = []
    for scope in left["write_scope"]:
        for other in right["write_scope"]:
            if scopes_overlap(scope, other):
                overlaps.append(scope if covers(scope, other) else other)
    if overlaps:
        found.append(issue(1, "write_scope overlap", tasks=pair, paths=sorted(set(overlaps))))
    if right_id in left["depends_on"] or left_id in right["depends_on"]:
        found.append(issue(2, "depends_on names a same-batch task", tasks=pair))
    input_hits = []
    for text in left["inputs"]:
        if right_id in task_ids_in(text):
            input_hits.append(right_id)
        for scope in scopes_named_in(text, right, left, tasks):
            input_hits.append(scope)
    for text in right["inputs"]:
        if left_id in task_ids_in(text):
            input_hits.append(left_id)
        for scope in scopes_named_in(text, left, right, tasks):
            input_hits.append(scope)
    if input_hits:
        found.append(issue(2, "inputs names a same-batch task or its file", tasks=pair, paths=sorted(set(input_hits))))
    reads = []
    for pointer in left["read_also"]:
        hit = read_hits(pointer, right["write_scope"])
        if hit:
            reads.append(hit)
    for pointer in right["read_also"]:
        hit = read_hits(pointer, left["write_scope"])
        if hit:
            reads.append(hit)
    if reads:
        found.append(issue(2, "read_also reads a file the other task writes", tasks=pair, paths=sorted(set(reads))))
    return found


def check_plan(plan_path, tasks_dir, cycle=None):
    body, cycles = load_plan(plan_path)
    tasks, errors = load_tasks(tasks_dir)
    selected = [cycle] if cycle else cycles
    violations = list(errors)
    sequential = []
    for name in selected:
        if cycle and name not in cycles:
            violations.append(issue(4, "unknown cycle " + name))
            continue
        rows = check_cycle(name, body, tasks)
        for row in rows:
            if row["message"].endswith(" sequential"):
                sequential.append({"cycle": name, "tasks": row.get("tasks", [])})
            else:
                violations.append(row)
    return {
        "ok": not violations,
        "violations": violations,
        "sequential": sequential,
    }


def render_text(data):
    for row in data["sequential"]:
        print(row["cycle"] + ": sequential")
    for item in data["violations"]:
        tasks = ",".join(item.get("tasks", []))
        paths = ",".join(item.get("paths", []))
        extra = ""
        if tasks:
            extra += " tasks=" + tasks
        if paths:
            extra += " paths=" + paths
        print("rule " + str(item["rule"]) + ": " + item["message"] + extra)
    print("PASS" if data["ok"] else "FAIL")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan")
    parser.add_argument("--tasks")
    parser.add_argument("--cycle")
    parser.add_argument("--json", action="store_true", dest="json_output")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    if not args.plan or not args.tasks:
        return 2
    plan = Path(args.plan)
    tasks = Path(args.tasks)
    if not plan.is_file() or not tasks.is_dir():
        return 2
    if args.cycle and not CYCLE_ID.fullmatch(args.cycle):
        return 2
    try:
        data = check_plan(plan, tasks, args.cycle)
    except (OSError, UnicodeError, ValueError) as exc:
        data = {"ok": False, "error": str(exc), "violations": [], "sequential": []}
        if args.json_output:
            print(json.dumps(data, ensure_ascii=False))
        else:
            print("error: " + str(exc))
        return 2
    if args.json_output:
        print(json.dumps(data, ensure_ascii=False))
    else:
        render_text(data)
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
