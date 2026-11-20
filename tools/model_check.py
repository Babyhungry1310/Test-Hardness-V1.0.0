import argparse
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

CODE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
BRACKET_SUFFIX = re.compile(r"\[[^\[\]]+\]$")

ROUTE_LINE = re.compile(
    r"^- (?P<when>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z)"
    r" \| route: (?P<route>\S+)"
    r" \| actual: (?P<actual>\S+)"
    r" \| kind: (?P<kind>chat|agent-tools)"
    r" \| result: (?P<result>OK|FAIL)"
    r" \| source: (?P<source>.+?)"
    r" \| note: (?P<note>\S.*)$"
)
ASSIGNMENT_LINE = re.compile(
    r"^- (?P<cycle>CYC-\d{2})"
    r" \| (?P<role>BRAINSTORM|PLANNING|REVIEWER|WORKER)"
    r" \| requested: (?P<requested>.+?)"
    r" \| actual: (?P<actual>.+?)"
    r" \| record: (?P<record>\S+(?: \S+)*?)"
    r" \| match: (?P<match>yes|no|pending)"
    r"(?: \| route: (?P<route>\S+) \| basis: (?P<basis>\S.*))?$"
)
ID_POINTER = re.compile(
    r"^(?:TK|DEC|RSK|REQ|SRC)-\d{4}$|^CYC-\d{2}$|^RVW-CYC-\d{2}$|^DSC-\d{8}-[a-z0-9]{4}$"
)

def load_front_matter(path):
    text = Path(path).read_text(encoding="utf-8")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError("missing front matter")
    end = normalized.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing front matter close")
    raw = normalized[4:end]
    body = normalized[end + 5:]
    yaml = YAML(typ="safe")
    yaml.constructor.yaml_constructors["tag:yaml.org,2002:timestamp"] = yaml.constructor.yaml_constructors["tag:yaml.org,2002:str"]
    data = yaml.load(raw)
    if not isinstance(data, dict):
        raise ValueError("front matter is not a mapping")
    return data, body

def schema_path(name):
    return Path(__file__).resolve().parent.parent / "harness" / "schemas" / name

def load_schema(name):
    return json.loads(schema_path(name).read_text(encoding="utf-8"))

def anchor_body(body, name):
    start = f"<!-- ANCHOR: {name} -->"
    end = f"<!-- END: {name} -->"
    start_at = body.find(start)
    end_at = body.find(end)
    if start_at < 0 or end_at < start_at:
        return None
    return body[start_at + len(start):end_at]

def word_count(text):
    return len(text.split())

def base_code(value):
    text = value.strip()
    if not text or "/" in text or "," in text:
        return None
    stem = BRACKET_SUFFIX.sub("", text)
    if not CODE_PATTERN.fullmatch(stem):
        return None
    suffix = text[len(stem):]
    if suffix and not BRACKET_SUFFIX.fullmatch(suffix):
        return None
    return stem

def same_model(left, right):
    left_base = base_code(left)
    right_base = base_code(right)
    if left_base is None or right_base is None:
        return "UNKNOWN"
    if left_base == right_base:
        return "same"
    return "different"

def repo_root(path):
    current = Path(path).resolve()
    if current.is_file():
        current = current.parent
    while current != current.parent:
        if (current / "04_control").is_dir() or (current / "harness").is_dir():
            return current
        current = current.parent
    return Path(path).resolve().parent

def pointer_exists(root, value):
    if value == "none" or value.startswith("https://"):
        return True
    pointer = value.partition("#")[0]
    if not pointer:
        return False
    if ID_POINTER.fullmatch(pointer):
        return any(item.name.startswith(pointer) for item in root.rglob(pointer + "*"))
    candidate = Path(pointer)
    if candidate.is_absolute():
        return candidate.exists()
    return (root / candidate).exists()

def issue(key, message, line=None):
    item = {"key": key, "message": message}
    if line is not None:
        item["line"] = line
    return item

def schema_issues(data, schema):
    validator = Draft202012Validator(schema)
    found = []
    for error in validator.iter_errors(data):
        path = "/".join(str(part) for part in error.path)
        key = path or "$"
        if error.validator == "required":
            parts = error.message.split("'")
            if len(parts) >= 2:
                key = parts[1] if not path else f"{path}/{parts[1]}"
        found.append(issue(key, error.message))
    return found

def catalog_issues(data, body, root):
    found = schema_issues(data, load_schema("model_catalog.schema.json"))
    models = data.get("models")
    if not isinstance(models, list):
        found.extend(route_issues(body))
        return found
    seen = {}
    owners = {}
    for index, model in enumerate(models):
        if not isinstance(model, dict):
            continue
        prefix = f"models/{index}"
        code = model.get("code")
        if isinstance(code, str):
            if BRACKET_SUFFIX.search(code):
                found.append(issue(f"{prefix}/code", "code has bracket suffix"))
            if code in seen:
                found.append(issue(f"{prefix}/code", "duplicate code"))
            seen[code] = index
        aliases = model.get("aliases")
        if isinstance(code, str) and isinstance(aliases, list):
            for alias in aliases:
                if not isinstance(alias, str):
                    continue
                prior = owners.get(alias)
                if prior is not None and prior != code:
                    found.append(issue(f"{prefix}/aliases", "alias belongs to two entries"))
                else:
                    owners[alias] = code
        if model.get("availability") == "confirmed":
            evidence = model.get("availability_evidence")
            if evidence == "none":
                found.append(issue(f"{prefix}/availability_evidence", "confirmed has no evidence"))
            elif isinstance(evidence, str) and not pointer_exists(root, evidence):
                found.append(issue(f"{prefix}/availability_evidence", "evidence pointer does not exist"))
    found.extend(route_issues(body))
    return found

def route_issues(body):
    section = anchor_body(body, "ROUTE_CHECKS")
    if section is None:
        return [issue("ROUTE_CHECKS", "missing ROUTE_CHECKS anchor")]
    found = []
    previous = None
    for raw in section.splitlines():
        if not raw.startswith("- "):
            continue
        match = ROUTE_LINE.fullmatch(raw)
        if not match:
            found.append(issue("ROUTE_CHECKS", "ROUTE_CHECKS line has wrong shape", raw))
            continue
        when = match.group("when")
        if previous is not None and when > previous:
            found.append(issue("ROUTE_CHECKS", "ROUTE_CHECKS line is not newest first", raw))
        previous = when
        count = word_count(match.group("note"))
        if count > 15:
            found.append(issue("ROUTE_CHECKS", f"note has {count} words", raw))
        actual = match.group("actual")
        result = match.group("result")
        if result == "OK" and actual == "none":
            found.append(issue("ROUTE_CHECKS", "result OK with actual none", raw))
        if result == "FAIL" and actual != "none":
            found.append(issue("ROUTE_CHECKS", "result FAIL with actual other than none", raw))
    return found

def assignment_issues(body):
    section = anchor_body(body, "ASSIGNMENTS")
    if section is None:
        return [issue("ASSIGNMENTS", "missing ASSIGNMENTS anchor")]
    found = []
    for raw in section.splitlines():
        if not raw.startswith("- "):
            continue
        match = ASSIGNMENT_LINE.fullmatch(raw)
        if not match:
            found.append(issue("ASSIGNMENTS", "ASSIGNMENTS line has wrong shape", raw))
            continue
        basis = match.group("basis")
        if basis is not None and word_count(basis) > 15:
            found.append(issue("ASSIGNMENTS", f"basis has {word_count(basis)} words", raw))
        verdict = match.group("match")
        if verdict not in ("yes", "no"):
            continue
        relation = same_model(match.group("requested"), match.group("actual"))
        if verdict == "yes" and relation == "different":
            found.append(issue("ASSIGNMENTS", "match yes with different base codes", raw))
        if verdict == "no" and relation == "same":
            found.append(issue("ASSIGNMENTS", "match no with same base code", raw))
    return found

def matrix_issues(data, body):
    found = schema_issues(data, load_schema("model_matrix.schema.json"))
    found.extend(assignment_issues(body))
    return found

def check_file(path, kind):
    try:
        data, body = load_front_matter(path)
    except (OSError, UnicodeError, YAMLError, ValueError) as exc:
        return 2, {"ok": False, "error": str(exc), "issues": []}
    if kind == "catalog":
        issues = catalog_issues(data, body, repo_root(path))
    else:
        issues = matrix_issues(data, body)
    return (0 if not issues else 1), {"ok": not issues, "issues": issues}

def configure_text_streams():
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")

def render_text(code, data):
    configure_text_streams()
    if data.get("error"):
        print(f"error: {data['error']}")
    for item in data.get("issues", []):
        line = item.get("line")
        if line:
            print(f"{item['key']}: {item['message']}: {line}")
        else:
            print(f"{item['key']}: {item['message']}")
    print("PASS" if code == 0 else "FAIL")

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=["catalog", "matrix"])
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true", dest="json_output")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    configure_text_streams()
    code, data = check_file(args.path, args.kind)
    if args.json_output:
        print(json.dumps(data, ensure_ascii=False))
    else:
        render_text(code, data)
    return code

if __name__ == "__main__":
    sys.exit(main())
