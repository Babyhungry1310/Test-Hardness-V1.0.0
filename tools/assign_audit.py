import argparse
import json
import re
import sys
from pathlib import Path

from ruamel.yaml.error import YAMLError

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tools.model_check import ASSIGNMENT_LINE, anchor_body, base_code, configure_text_streams, load_front_matter

RUN_FILE = re.compile(r"^(TK-\d{4})_R(\d+)_")
TASK_ID = re.compile(r"^TK-\d{4}$")
CYCLE_ID = re.compile(r"^CYC-\d{2}$")
RVW_ID = re.compile(r"^RVW-(CYC-\d{2})$")
RUN_POINTER = re.compile(r"^(TK-\d{4}) R(\d+)$")
ROUTE_NAME = re.compile(r"\| route: (\S+)")


def item(cycle, record, reason, detail):
    return {"cycle": cycle, "record": record, "reason": reason, "detail": detail}


def route_names(body):
    section = anchor_body(body, "ROUTE_CHECKS")
    names = set()
    if not section:
        return names
    for raw in section.splitlines():
        match = ROUTE_NAME.search(raw)
        if match:
            names.add(match.group(1).casefold())
    return names


def parse_model(value, routes):
    if value is None:
        return None
    if not isinstance(value, str):
        return "UNKNOWN"
    text = value.strip()
    if text == "" or text.casefold() in {"pending", "none"}:
        return None
    codes = []
    for part in [piece.strip() for piece in text.split(",")]:
        if not part or "/" in part or part.casefold() == "hardeness" or part.casefold() in routes:
            return "UNKNOWN"
        base = base_code(part)
        if base is None:
            return "UNKNOWN"
        codes.append(base)
    return codes


def record_exists(root, record):
    text = record.strip()
    if not text or text == "none":
        return False
    if (root / text).is_file():
        return True
    rvw = RVW_ID.fullmatch(text)
    if rvw:
        cycle = rvw.group(1)
        return (root / "03_output" / cycle / "checks" / f"RVW-{cycle}.md").is_file()
    run = RUN_POINTER.fullmatch(text)
    if run:
        pattern = f"{run.group(1)}_R{run.group(2)}_*.md"
        return any((root / "02_work" / "runs").glob(pattern))
    return False


def cycle_of_task(root, task):
    if not TASK_ID.fullmatch(task):
        return None
    found = sorted((root / "02_work" / "tasks").glob(f"CYC-*/{task}.md"))
    if not found:
        return None
    return found[0].parent.name


def load_record(path):
    path = Path(path)
    raw = path.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        return load_front_matter(path)
    text = raw.decode("utf-8-sig")
    original = Path.read_text

    def read_text(self, *args, **kwargs):
        if self == path:
            return text
        return original(self, *args, **kwargs)

    Path.read_text = read_text
    try:
        return load_front_matter(path)
    finally:
        Path.read_text = original


def load_runs(root, cycle=None):
    directory = root / "02_work" / "runs"
    if not directory.is_dir():
        return []
    found = []
    for path in sorted(directory.glob("TK-*_R*_*.md")):
        match = RUN_FILE.match(path.name)
        if match is None:
            continue
        task = match.group(1)
        run_cycle = cycle_of_task(root, task)
        if cycle and run_cycle != cycle:
            continue
        data, _body = load_record(path)
        stated = str(data.get("task", "")).strip().strip("\"'")
        if TASK_ID.fullmatch(stated):
            task = stated
            run_cycle = cycle_of_task(root, task) or run_cycle
        code = f"{match.group(1)}_R{match.group(2)}"
        found.append({"code": code, "cycle": run_cycle, "data": data})
    return found


def load_rvw(root, cycle):
    path = root / "03_output" / cycle / "checks" / f"RVW-{cycle}.md"
    if not path.is_file():
        return None
    data, _body = load_record(path)
    return {"code": f"RVW-{cycle}", "data": data}


def parse_assignments(body):
    section = anchor_body(body, "ASSIGNMENTS")
    if section is None:
        raise ValueError("missing ASSIGNMENTS anchor")
    found = []
    for raw in section.splitlines():
        if not raw.startswith("- "):
            continue
        match = ASSIGNMENT_LINE.fullmatch(raw)
        if not match:
            raise ValueError("ASSIGNMENTS line has wrong shape")
        found.append(match.groupdict())
    return found


def catalog_index(data):
    models = data.get("models") or []
    if not isinstance(models, list):
        raise ValueError("catalog models is not a list")
    codes = set()
    groups = {}
    for entry in models:
        if not isinstance(entry, dict) or "code" not in entry:
            continue
        code = entry["code"]
        codes.add(code)
        groups[code] = str(entry.get("group") or "")
    return codes, groups


def add_catalog_notes(notes, cycle, record, codes, catalog_codes):
    for code in codes:
        if code not in catalog_codes:
            notes.append(item(cycle, record, "actual not in catalog", code))


def check_assignment(root, line, routes, deviations, notes):
    record = line["record"]
    cycle = line["cycle"]
    if not record_exists(root, record):
        deviations.append(item(cycle, record, "assignment record does not exist", record))
        return
    verdict = line["match"]
    if verdict == "pending":
        deviations.append(item(cycle, record, "match pending but record exists", record))
        return
    if verdict == "no":
        notes.append(item(cycle, record, "match no", record))
        return
    requested = parse_model(line["requested"], routes)
    actual = parse_model(line["actual"], routes)
    if actual == "UNKNOWN":
        deviations.append(item(cycle, record, "UNKNOWN", str(line["actual"]).strip()))
        return
    if not isinstance(requested, list) or not isinstance(actual, list):
        return
    if set(requested) != set(actual):
        deviations.append(item(cycle, record, "match yes with different models", f"{line['requested']} != {line['actual']}"))


def check_run(run, routes, catalog_codes, deviations, notes):
    cycle = run["cycle"]
    record = run["code"]
    if "model" not in run["data"]:
        deviations.append(item(cycle, record, "missing actual model", ""))
        return None
    value = run["data"].get("model")
    parsed = parse_model(value, routes)
    if parsed is None:
        deviations.append(item(cycle, record, "missing actual model", ""))
        return None
    if parsed == "UNKNOWN":
        deviations.append(item(cycle, record, "UNKNOWN", str(value).strip()))
        return "UNKNOWN"
    add_catalog_notes(notes, cycle, record, parsed, catalog_codes)
    return parsed


def note_groups(notes, cycle, reviewer, reviewer_codes, run, run_codes, groups):
    seen = set()
    for left in reviewer_codes:
        for right in run_codes:
            if left == right:
                continue
            group = groups.get(left) or ""
            if group and group == (groups.get(right) or ""):
                key = (run["code"], group)
                if key in seen:
                    continue
                seen.add(key)
                notes.append(item(cycle, reviewer, "reviewer shares group with worker", f"{run['code']} {group}"))


def check_reviewer(root, cycle, runs, parsed_runs, routes, catalog_codes, groups, deviations, notes):
    rvw = load_rvw(root, cycle)
    if rvw is None:
        if runs:
            deviations.append(item(cycle, f"RVW-{cycle}", "UNKNOWN", "missing session file"))
        return
    data = rvw["data"]
    record = rvw["code"]
    if "reviewer_model" not in data:
        deviations.append(item(cycle, record, "missing reviewer_model", ""))
        return
    value = data.get("reviewer_model")
    parsed = parse_model(value, routes)
    if parsed is None:
        deviations.append(item(cycle, record, "missing reviewer_model", ""))
        return
    if parsed == "UNKNOWN":
        deviations.append(item(cycle, record, "UNKNOWN", str(value).strip()))
        return
    add_catalog_notes(notes, cycle, record, parsed, catalog_codes)
    for run, run_codes in parsed_runs:
        if not isinstance(run_codes, list):
            continue
        shared = sorted(set(parsed) & set(run_codes))
        if shared:
            deviations.append(item(cycle, record, "reviewer_model matches run model", f"{run['code']} {','.join(shared)}"))
        note_groups(notes, cycle, record, parsed, run, run_codes, groups)


def select_cycles(root, cycle, assignments, runs):
    if cycle:
        return [cycle]
    found = {line["cycle"] for line in assignments}
    found.update(run["cycle"] for run in runs if run["cycle"])
    output = root / "03_output"
    if output.is_dir():
        for path in output.glob("CYC-*/checks/RVW-CYC-*.md"):
            if CYCLE_ID.fullmatch(path.parent.parent.name):
                found.add(path.parent.parent.name)
    return sorted(found)


def audit(root, cycle=None):
    root = Path(root)
    matrix_path = root / "04_control" / "MODEL_MATRIX.md"
    catalog_path = root / "04_control" / "MODEL_CATALOG.md"
    if not matrix_path.is_file() or not catalog_path.is_file():
        raise ValueError("missing control file")
    _matrix_data, matrix_body = load_record(matrix_path)
    catalog_data, catalog_body = load_record(catalog_path)
    catalog_codes, groups = catalog_index(catalog_data)
    routes = route_names(catalog_body)
    assignments = parse_assignments(matrix_body)
    runs = load_runs(root, cycle)
    deviations = []
    notes = []
    for current in select_cycles(root, cycle, assignments, runs):
        cycle_runs = [run for run in runs if run["cycle"] == current]
        for line in assignments:
            if line["cycle"] == current:
                check_assignment(root, line, routes, deviations, notes)
        parsed_runs = []
        for run in cycle_runs:
            parsed_runs.append((run, check_run(run, routes, catalog_codes, deviations, notes)))
        check_reviewer(root, current, cycle_runs, parsed_runs, routes, catalog_codes, groups, deviations, notes)
    deviations.sort(key=lambda entry: (entry["cycle"], entry["record"], entry["reason"], entry["detail"]))
    notes.sort(key=lambda entry: (entry["cycle"], entry["record"], entry["reason"], entry["detail"]))
    return {"ok": not deviations, "cycle": cycle, "deviations": deviations, "notes": notes}


def render(code, data, json_output):
    configure_text_streams()
    if json_output:
        print(json.dumps(data, ensure_ascii=False))
        return
    if data.get("error"):
        print(f"error: {data['error']}")
    for entry in data.get("deviations", []):
        detail = entry.get("detail") or ""
        if detail:
            print(f"deviation: {entry['record']}: {entry['reason']}: {detail}")
        else:
            print(f"deviation: {entry['record']}: {entry['reason']}")
    for entry in data.get("notes", []):
        detail = entry.get("detail") or ""
        if detail:
            print(f"note: {entry['record']}: {entry['reason']}: {detail}")
        else:
            print(f"note: {entry['record']}: {entry['reason']}")
    print("PASS" if code == 0 else "FAIL")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="assign_audit")
    parser.add_argument("--root", required=True)
    parser.add_argument("--cycle")
    parser.add_argument("--json", action="store_true", dest="json_output")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    configure_text_streams()
    if args.cycle is not None and not CYCLE_ID.fullmatch(args.cycle):
        render(2, {"ok": False, "cycle": args.cycle, "error": "invalid cycle", "deviations": [], "notes": []}, args.json_output)
        return 2
    root = Path(args.root)
    if not root.is_dir():
        render(2, {"ok": False, "cycle": args.cycle, "error": "root is not a directory", "deviations": [], "notes": []}, args.json_output)
        return 2
    try:
        result = audit(root, args.cycle)
    except (OSError, UnicodeError, YAMLError, ValueError) as exc:
        render(2, {"ok": False, "cycle": args.cycle, "error": str(exc), "deviations": [], "notes": []}, args.json_output)
        return 2
    code = 0 if result["ok"] else 1
    render(code, result, args.json_output)
    return code


if __name__ == "__main__":
    sys.exit(main())
