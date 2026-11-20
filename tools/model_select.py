import argparse
import json
import re
import sys
from pathlib import Path

from tools.model_check import ROUTE_LINE, anchor_body, base_code, load_front_matter

EVIDENCE = re.compile(r"^(?P<kind>run|log|rvw|route-check):(?P<ref>.+)$")
MODEL_KEY = {"run": "model", "rvw": "reviewer_model"}


def configure_text_streams():
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def catalog_models(data):
    models = data.get("models")
    if not isinstance(models, list):
        return []
    return [item for item in models if isinstance(item, dict) and isinstance(item.get("code"), str)]


def route_rows(body):
    section = anchor_body(body, "ROUTE_CHECKS")
    if section is None:
        return []
    rows = []
    for raw in section.splitlines():
        match = ROUTE_LINE.fullmatch(raw)
        if match:
            rows.append(match.groupdict())
    return rows


def newest_by_route(rows):
    newest = {}
    for row in rows:
        route = row["route"]
        if route not in newest or row["when"] > newest[route]["when"]:
            newest[route] = row
    return newest


def model_for_code(models, code):
    for model in models:
        if model["code"] == code:
            return model
    return None


def route_ok(row, code):
    if row["result"] != "OK":
        return False
    return base_code(row["actual"]) == code


def tools_ok(model, row):
    if model.get("availability") == "confirmed":
        return True
    return row["kind"] == "agent-tools"


def eligible_models(data, body, needs_tools):
    models = catalog_models(data)
    accepted = []
    rejected = []
    for route, row in sorted(newest_by_route(route_rows(body)).items()):
        actual = row["actual"]
        code_base = base_code(actual)
        model = model_for_code(models, code_base) if code_base else None
        if row["result"] == "FAIL":
            rejected.append({"code": actual, "reason": f"newest route check FAIL: {route}"})
            continue
        if model is None:
            rejected.append({"code": actual, "reason": f"actual does not resolve to a catalog code: {route}"})
            continue
        if not route_ok(row, model["code"]):
            rejected.append({"code": model["code"], "reason": f"newest route actual does not match code: {route}"})
            continue
        if needs_tools and not tools_ok(model, row):
            rejected.append({"code": model["code"], "reason": f"needs tools, route kind {row['kind']} and availability {model.get('availability')}: {route}"})
            continue
        if model["code"] not in accepted:
            accepted.append(model["code"])
    return sorted(accepted), rejected


def parse_evidence(value):
    match = EVIDENCE.fullmatch(value or "")
    if not match:
        raise ValueError(f"evidence needs a kind prefix: {value}")
    return match.group("kind"), match.group("ref")


def split_field(value):
    return [part.strip() for part in str(value).split(",")]


def field_status(value):
    if not isinstance(value, str) or not value.strip():
        return "UNKNOWN", value if isinstance(value, str) else ""
    parts = split_field(value)
    if any(not part or base_code(part) is None for part in parts):
        return "UNKNOWN", value
    return "ok", value


def read_record(path, key):
    try:
        data, _body = load_front_matter(path)
    except (OSError, UnicodeError, ValueError) as exc:
        raise ValueError(str(exc)) from exc
    if key not in data:
        raise ValueError(f"missing {key}")
    value = data[key]
    if not isinstance(value, str):
        raise ValueError(f"{key} is not a string")
    return value


def session_field(kind, ref):
    if kind == "route-check":
        raise ValueError("probe is not session actual")
    if kind not in MODEL_KEY:
        raise ValueError(f"unsupported session evidence: {kind}")
    return read_record(ref, MODEL_KEY[kind])


def compare_fields(left, right):
    left_status, left_raw = field_status(left)
    right_status, right_raw = field_status(right)
    if left_status == "UNKNOWN" or right_status == "UNKNOWN":
        raw = left_raw if left_status == "UNKNOWN" else right_raw
        return "UNKNOWN", raw
    left_bases = [base_code(part) for part in split_field(left)]
    right_bases = [base_code(part) for part in split_field(right)]
    if sorted(left_bases) == sorted(right_bases):
        return "same", left
    return "different", left


def compare_evidence(left_value, right_value):
    left_kind, left_ref = parse_evidence(left_value)
    right_kind, right_ref = parse_evidence(right_value)
    return compare_fields(session_field(left_kind, left_ref), session_field(right_kind, right_ref))


def log_actual(path):
    text = Path(path).read_text(encoding="utf-8")
    found = []
    for line in text.splitlines():
        if '"model"' not in line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        model = payload.get("payload", {}).get("model")
        if isinstance(model, str):
            found.append(model)
    if not found:
        raise ValueError("session log has no actual model")
    return found[-1]


def reviewer_actual(kind, ref):
    if kind == "log":
        return log_actual(ref)
    if kind == "rvw":
        return read_record(ref, "reviewer_model")
    raise ValueError(f"reviewer evidence cannot be {kind}")


def worker_models(values):
    found = []
    for value in values:
        kind, ref = parse_evidence(value)
        if kind != "run":
            raise ValueError(f"worker evidence must be a run: {value}")
        found.append(read_record(ref, "model"))
    return found


def independence(reviewer, workers):
    status, raw = field_status(reviewer)
    if status == "UNKNOWN":
        return "UNKNOWN", raw, "reviewer actual is not a valid code"
    reviewer_bases = {base_code(part) for part in split_field(reviewer)}
    for worker in workers:
        worker_status, worker_raw = field_status(worker)
        if worker_status == "UNKNOWN":
            return "UNKNOWN", worker_raw, "worker actual is not a valid code"
        overlap = reviewer_bases & {base_code(part) for part in split_field(worker)}
        if overlap:
            return "same", reviewer, f"reviewer matches worker base code: {', '.join(sorted(overlap))}"
    return "different", reviewer, ""


def emit(code, payload, json_output):
    if json_output:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(payload["text"])
    return code


def command_eligible(args):
    data, body = load_front_matter(args.catalog)
    accepted, rejected = eligible_models(data, body, args.needs_tools)
    excluded = []
    for value in args.exclude_evidence:
        kind, ref = parse_evidence(value)
        if kind != "run":
            raise ValueError(f"exclude evidence must be a run: {value}")
        field = read_record(ref, "model")
        status, _raw = field_status(field)
        if status == "UNKNOWN":
            raise ValueError(f"exclude evidence model is UNKNOWN: {field}")
        excluded.extend(base_code(part) for part in split_field(field))
    selected = [code for code in accepted if code not in excluded]
    for code in sorted(set(excluded)):
        if code in accepted:
            rejected.append({"code": code, "reason": "excluded by run evidence"})
    rejected.sort(key=lambda item: item["code"])
    lines = list(selected)
    if not selected:
        lines.append("no eligible model")
        for item in rejected:
            lines.append(f"{item['code']}: {item['reason']}")
    payload = {"verdict": "eligible" if selected else "empty", "models": selected, "rejected": rejected, "text": "\n".join(lines)}
    return emit(0 if selected else 1, payload, args.json_output)


def command_same(args):
    verdict, raw = compare_evidence(args.left_evidence, args.right_evidence)
    text = verdict if verdict != "UNKNOWN" else f"UNKNOWN {raw}"
    return emit(0 if verdict != "UNKNOWN" else 1, {"verdict": verdict, "text": text}, args.json_output)


def command_reviewer(args):
    workers = worker_models(args.worker_evidence)
    if args.stage == "select":
        if not args.requested:
            raise ValueError("missing requested model")
        status, raw = field_status(args.requested)
        if status == "UNKNOWN":
            return emit(1, {"verdict": "UNKNOWN", "text": f"UNKNOWN {raw}"}, args.json_output)
        for worker in workers:
            worker_status, worker_raw = field_status(worker)
            if worker_status == "UNKNOWN":
                return emit(1, {"verdict": "UNKNOWN", "text": f"UNKNOWN {worker_raw}"}, args.json_output)
        text = f"planned {args.requested.strip()}"
        return emit(0, {"verdict": "planned", "text": text}, args.json_output)
    if not args.reviewer_evidence:
        raise ValueError("missing reviewer evidence")
    kind, ref = parse_evidence(args.reviewer_evidence)
    expected = "log" if args.stage == "start" else "rvw"
    if kind != expected:
        raise ValueError(f"stage {args.stage} requires {expected} evidence")
    verdict, raw, reason = independence(reviewer_actual(kind, ref), workers)
    if verdict == "UNKNOWN":
        text = f"UNKNOWN {raw}"
    elif verdict == "different":
        text = "different"
    else:
        text = f"same {reason}"
    code = 0 if verdict == "different" else 1
    return emit(code, {"verdict": verdict, "reason": reason, "text": text}, args.json_output)


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--json", action="store_true", dest="json_output")
    commands = parser.add_subparsers(dest="command", required=True)
    eligible = commands.add_parser("eligible")
    eligible.add_argument("--needs-tools", action="store_true")
    eligible.add_argument("--exclude-evidence", action="append", default=[])
    same = commands.add_parser("same")
    same.add_argument("--left-evidence", required=True)
    same.add_argument("--right-evidence", required=True)
    reviewer = commands.add_parser("reviewer")
    reviewer.add_argument("--stage", required=True, choices=["select", "start", "pr"])
    reviewer.add_argument("--requested")
    reviewer.add_argument("--worker-evidence", action="append", default=[])
    reviewer.add_argument("--reviewer-evidence")
    return parser


def parse_args(argv):
    parser = build_parser()
    raw = list(sys.argv[1:] if argv is None else argv)
    catalog = None
    json_output = False
    rest = []
    index = 0
    while index < len(raw):
        item = raw[index]
        if item == "--catalog":
            catalog = raw[index + 1]
            index += 2
            continue
        if item == "--json":
            json_output = True
            index += 1
            continue
        rest.append(item)
        index += 1
    args = parser.parse_args(["--catalog", catalog or "", "--json", *rest] if json_output else ["--catalog", catalog or "", *rest])
    if catalog is None:
        parser.error("the following arguments are required: --catalog")
    args.catalog = catalog
    args.json_output = json_output
    return args


def main(argv=None):
    configure_text_streams()
    try:
        args = parse_args(argv)
    except SystemExit:
        return 2
    try:
        if args.command == "eligible":
            return command_eligible(args)
        if args.command == "same":
            return command_same(args)
        return command_reviewer(args)
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        message = str(exc)
        payload = {"verdict": "UNKNOWN", "error": message, "text": f"UNKNOWN {message}"}
        return emit(1, payload, args.json_output)


if __name__ == "__main__":
    sys.exit(main())
