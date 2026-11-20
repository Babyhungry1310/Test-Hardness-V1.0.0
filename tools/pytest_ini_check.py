import argparse
import configparser
import json
import sys
import tomllib
from pathlib import Path

CANDIDATES = [
    ("pytest.ini", "ini", "pytest"),
    ("pyproject.toml", "toml", "tool.pytest.ini_options"),
    ("tox.ini", "ini", "pytest"),
    ("setup.cfg", "ini", "tool:pytest"),
]


def normalize_path(p):
    p = p.strip().replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p.rstrip("/")


def extract_paths(val):
    items = [str(x) for x in val] if isinstance(val, (list, tuple)) else str(val).split()
    return [normalize_path(x) for x in items if normalize_path(x)]


def parse_ini(content, filename):
    cp = configparser.ConfigParser(interpolation=None, allow_no_value=True)
    cp.read_string(content, source=filename)
    return cp


def read_file(path):
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path.name}: decode error: {exc}") from exc


def inspect_project(root, template_path):
    try:
        tpl_cp = parse_ini(read_file(template_path), template_path.name)
    except configparser.Error as exc:
        raise ValueError(f"{template_path.name}: syntax error: {exc}") from exc
    if not tpl_cp.has_section("pytest"):
        raise ValueError(f"{template_path.name}: missing [pytest] section")
    tpl_opts = {k.lower(): v for k, v in tpl_cp["pytest"].items()}
    tpl_paths = extract_paths(tpl_opts.get("testpaths", ""))

    active_file, active_opts = None, {}
    for filename, kind, section in CANDIDATES:
        p = root / filename
        if not p.is_file():
            continue
        text = read_file(p)
        if kind == "ini":
            try:
                cp = parse_ini(text, filename)
            except configparser.Error as exc:
                raise ValueError(f"{filename}: syntax error: {exc}") from exc
            if cp.has_section(section) and active_file is None:
                active_file, active_opts = filename, {k.lower(): v for k, v in cp[section].items()}
        elif kind == "toml":
            try:
                data = tomllib.loads(text)
            except tomllib.TOMLDecodeError as exc:
                raise ValueError(f"{filename}: syntax error: {exc}") from exc
            tool = data.get("tool") if isinstance(data, dict) else None
            pyt = tool.get("pytest") if isinstance(tool, dict) else None
            ini_opt = pyt.get("ini_options") if isinstance(pyt, dict) else None
            if isinstance(ini_opt, dict) and active_file is None:
                active_file, active_opts = filename, {str(k).lower(): v for k, v in ini_opt.items()}

    if active_file is None:
        return {"status": "absent", "result": "absent", "file": None, "options": {}, "differences": [], "diff": []}

    if active_file != "pytest.ini":
        msg = f"configuration in {active_file} would be shadowed by pytest.ini"
        return {"status": "shadowed", "result": "shadowed", "file": active_file, "options": active_opts, "differences": [msg], "diff": [msg]}

    diffs = []
    active_paths = extract_paths(active_opts.get("testpaths", ""))
    if active_paths != tpl_paths:
        diffs.append(f"testpaths differs: expected {tpl_paths}, got {active_paths}")
    diffs.extend(f"extra option '{k}'" for k in sorted(active_opts.keys() - tpl_opts.keys()))
    diffs.extend(f"missing option '{k}'" for k in sorted(tpl_opts.keys() - active_opts.keys()))

    status = "differs" if diffs else "same"
    return {"status": status, "result": status, "file": active_file, "options": active_opts, "differences": diffs, "diff": diffs}


def render_text(res):
    print(f"status: {res['status']}\nfile: {res['file'] or 'none'}")
    print("options:" if res["options"] else "options: none")
    for k, v in res["options"].items():
        val = ", ".join(str(x) for x in v) if isinstance(v, list) else str(v).strip()
        print(f"  {k}: {val}")
    if res["differences"]:
        print("differences:\n" + "\n".join(f"  {d}" for d in res["differences"]))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pytest_ini_check")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--template", type=Path, default=None)
    parser.add_argument("--json", action="store_true", dest="json_output")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2

    tpl = args.template
    if tpl is None:
        tpl = Path("harness/templates/pytest.ini")
        if not tpl.is_file():
            tpl = Path(__file__).resolve().parent.parent / "harness" / "templates" / "pytest.ini"
    if not args.project_root.is_dir() or not tpl.is_file():
        sys.stderr.write("error: invalid project_root or template\n")
        return 2

    try:
        res = inspect_project(args.project_root, tpl)
    except ValueError as exc:
        if args.json_output:
            print(json.dumps({"status": "error", "result": "error", "error": str(exc)}, ensure_ascii=False))
        else:
            sys.stderr.write(f"error: {exc}\n")
        return 2

    if args.json_output:
        print(json.dumps(res, ensure_ascii=False))
    else:
        render_text(res)
    return 0 if res["status"] in ("absent", "same") else 1


if __name__ == "__main__":
    sys.exit(main())
