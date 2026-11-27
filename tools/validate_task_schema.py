#!/usr/bin/env python3
"""Kiểm cơ học thẻ task trong bản kế hoạch (PLAN / SRC) trước khi gửi REVIEWER.

Chỉ dùng thư viện chuẩn của Python. Nếu có PyYAML hoặc jsonschema thì dùng thêm,
không có thì vẫn chạy.

Thẻ task = một khối mã rào (```yaml / ```yml / ```json / ```task hoặc rào trống)
có khóa `id`. Ví dụ:

    ```yaml
    id: TK-0057
    batch: B1b
    branch: lead/TK-0057-src0003-p6
    goal: Nạp SRC-0003 P6 và DEC-0032
    write_scope:
      - 06_sources/SRC-0003.md
      - 02_decisions/DEC-0032.md
    depends_on: [TK-0038]
    verify: python tools/validate_task_schema.py 06_sources/SRC-0003.md
    ```

Mã thoát:
    0   không có lỗi
    1   có vi phạm
    2   lỗi dùng lệnh hoặc lỗi đọc file
    66  không tìm thấy thẻ task nào (NO_INPUT: không có gì để kiểm thì không được báo đạt)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

EXIT_OK, EXIT_FAIL, EXIT_USAGE, EXIT_NO_INPUT = 0, 1, 2, 66

DEFAULT_ID_PATTERN = r"^TK-\d{4}$"
DEFAULT_REQUIRED = ["id", "branch", "goal", "write_scope", "depends_on", "verify"]
DEFAULT_BRANCH_PREFIXES = ["task/", "upgrade/", "lead/"]
DEFAULT_MAX_SCOPE = 5
# depends_on được phép rỗng ([]); các trường còn lại không được rỗng.
MAY_BE_EMPTY = {"depends_on"}

GLOB_CHARS = set("*?[]{}")
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w-]*)\s*$")
KEY_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$")
ID_SCAN_RE = re.compile(r"\bTK-\d{4}[A-Za-z]*\b")


@dataclass
class Card:
    source: str
    line: int
    data: dict


@dataclass
class Finding:
    source: str
    line: int
    task: str
    rule: str
    message: str

    def text(self) -> str:
        return f"{self.source}:{self.line}: {self.task}: {self.rule}: {self.message}"


@dataclass
class Config:
    id_pattern: re.Pattern
    required: list
    branch_prefixes: list
    max_scope: int
    allow_dirs: bool
    known_ids: set = field(default_factory=set)
    schema: dict | None = None


# ---------------------------------------------------------------- phân tích


def _strip_comment(value: str) -> str:
    out, quote = [], None
    for i, ch in enumerate(value):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "#" and (i == 0 or value[i - 1].isspace()):
            break
        out.append(ch)
    return "".join(out).strip()


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def _scalar(value: str):
    value = _strip_comment(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [_unquote(v) for v in inner.split(",") if v.strip()] if inner else []
    if value in ("null", "~"):
        return None
    return _unquote(value)


def parse_mini_yaml(text: str) -> dict:
    """Bộ đọc YAML tối giản cho thẻ phẳng: `k: v`, `k: [a, b]`, danh sách `- x`, khối `|`/`>`."""
    data: dict = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        if raw[0].isspace():
            raise ValueError(f"dòng {i + 1}: thụt lề không thuộc khóa nào: {raw.strip()!r}")
        m = KEY_RE.match(raw)
        if not m:
            raise ValueError(f"dòng {i + 1}: không phải dạng 'khóa: giá trị': {raw.strip()!r}")
        key, rest = m.group(1), _strip_comment(m.group(2))
        i += 1
        block = []
        while i < len(lines) and (not lines[i].strip() or lines[i][0].isspace()):
            block.append(lines[i])
            i += 1
        while block and not block[-1].strip():
            block.pop()
        if rest in ("|", ">", "|-", ">-"):
            body = [b.strip() for b in block]
            data[key] = ("\n" if rest.startswith("|") else " ").join(body).strip()
        elif rest:
            if block:
                rest = " ".join([rest] + [b.strip() for b in block])
            data[key] = _scalar(rest)
        elif block and all(b.strip().startswith("- ") or b.strip() == "-" or not b.strip() for b in block):
            data[key] = [_scalar(b.strip()[1:]) for b in block if b.strip()]
        elif block:
            data[key] = " ".join(b.strip() for b in block)
        else:
            data[key] = None
    return data


def parse_block(text: str, use_yaml: bool) -> dict:
    stripped = text.strip()
    if stripped.startswith("{"):
        return json.loads(stripped)
    if use_yaml:
        try:
            import yaml  # type: ignore
        except ImportError:
            pass
        else:
            loaded = yaml.safe_load(stripped)
            if not isinstance(loaded, dict):
                raise ValueError("khối không phải ánh xạ khóa–giá trị")
            return loaded
    return parse_mini_yaml(stripped)


def extract_cards(path: Path, use_yaml: bool) -> tuple[list[Card], list[Finding]]:
    cards, problems = [], []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if not m or m.group(3).lower() not in ("", "yaml", "yml", "json", "task"):
            i += 1
            continue
        fence, start = m.group(2), i + 1
        j = start
        while j < len(lines) and not lines[j].strip().startswith(fence):
            j += 1
        body = "\n".join(lines[start:j])
        i = j + 1
        if not re.search(r'^\s*"?id"?\s*:', body, re.M):
            continue
        try:
            data = parse_block(body, use_yaml)
        except Exception as exc:  # noqa: BLE001 — lỗi đọc là một vi phạm, không phải crash
            problems.append(Finding(str(path), start, "?", "PARSE", str(exc)))
            continue
        cards.append(Card(str(path), start, data))
    return cards, problems


# ---------------------------------------------------------------- kiểm


def _is_empty(value) -> bool:
    return value is None or (isinstance(value, (str, list, dict)) and len(value) == 0)


def _schema_allows_empty(schema: dict | None, key: str) -> bool:
    """Schema cho phép giá trị rỗng của khóa này? (vd `fixes: ""` với pattern ^(?:TK-\\d{4})?$)."""
    if not schema:
        return False
    prop = (schema.get("properties") or {}).get(key) or {}
    if prop.get("type") == "string" and not prop.get("minLength"):
        pattern = prop.get("pattern")
        return pattern is None or re.search(pattern, "") is not None
    if prop.get("type") == "array":
        return not prop.get("minItems")
    return False


def check_scope_entry(entry, cfg: Config) -> list[tuple[str, str]]:
    out = []
    if not isinstance(entry, str) or not entry.strip():
        return [("SCOPE_PATH", f"phần tử không phải đường dẫn: {entry!r}")]
    p = entry.strip()
    if GLOB_CHARS & set(p):
        out.append(("SCOPE_GLOB", f"không dùng wildcard, liệt kê từng file: {p!r}"))
    if re.search(r"\s", p):
        out.append(("SCOPE_PROSE", f"đường dẫn chứa khoảng trắng hoặc là văn xuôi: {p!r}"))
    if "\\" in p:
        out.append(("SCOPE_PATH", f"dùng dấu '/', không dùng '\\': {p!r}"))
    if p.startswith("/") or re.match(r"^[A-Za-z]:", p) or p.startswith("~"):
        out.append(("SCOPE_PATH", f"phải là đường dẫn tương đối trong repo: {p!r}"))
    if ".." in PurePosixPath(p.replace("\\", "/")).parts:
        out.append(("SCOPE_PATH", f"không dùng '..': {p!r}"))
    if p.endswith("/") and not cfg.allow_dirs:
        out.append(("SCOPE_PATH", f"thư mục không được phép (thiếu --allow-dirs): {p!r}"))
    return out


def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles, state, stack = [], {}, []

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for nxt in graph.get(node, []):
            if nxt not in graph:
                continue
            if state.get(nxt) == 1:
                cycles.append(stack[stack.index(nxt):] + [nxt])
            elif not state.get(nxt):
                visit(nxt)
        stack.pop()
        state[node] = 2

    for n in sorted(graph):
        if not state.get(n):
            visit(n)
    return cycles


def validate(cards: list[Card], cfg: Config) -> list[Finding]:
    findings: list[Finding] = []
    seen: dict[str, Card] = {}
    graph: dict[str, list[str]] = {}
    batch_paths: dict[tuple[str, str], str] = {}

    def add(card: Card, rule: str, msg: str) -> None:
        findings.append(Finding(card.source, card.line, str(card.data.get("id", "?")), rule, msg))

    jsonschema_validator = None
    if cfg.schema is not None:
        try:
            import jsonschema  # type: ignore
        except ImportError:
            jsonschema_validator = None
        else:
            jsonschema_validator = jsonschema.Draft202012Validator(cfg.schema)

    for card in cards:
        d = card.data
        tid = d.get("id")

        if not isinstance(tid, str) or not cfg.id_pattern.match(tid):
            add(card, "ID_FORMAT", f"id {tid!r} không khớp {cfg.id_pattern.pattern}"
                " — tách task thì cấp ID mới từ sổ, không thêm hậu tố chữ")
        elif tid in seen:
            add(card, "DUPLICATE_ID", f"trùng với thẻ ở {seen[tid].source}:{seen[tid].line}")
        else:
            seen[tid] = card

        for key in cfg.required:
            if key not in d:
                add(card, "MISSING_FIELD", f"thiếu trường bắt buộc '{key}'")
            elif _is_empty(d[key]) and key not in MAY_BE_EMPTY and not _schema_allows_empty(cfg.schema, key):
                add(card, "MISSING_FIELD", f"trường '{key}' rỗng")

        branch = d.get("branch")
        if isinstance(branch, str) and branch and cfg.branch_prefixes:
            if not any(branch.startswith(pfx) for pfx in cfg.branch_prefixes):
                add(card, "BRANCH_PREFIX", f"nhánh {branch!r} phải bắt đầu bằng một trong {cfg.branch_prefixes}")

        scope = d.get("write_scope")
        if scope is not None:
            if isinstance(scope, str):
                add(card, "SCOPE_TYPE", "write_scope phải là danh sách đường dẫn, không phải một chuỗi")
                scope = []
            elif not isinstance(scope, list):
                add(card, "SCOPE_TYPE", "write_scope phải là danh sách")
                scope = []
            if len(scope) > cfg.max_scope:
                add(card, "SCOPE_COUNT", f"{len(scope)} path > trần {cfg.max_scope} — tách thành task mới có ID riêng")
            dup = {p for p in scope if isinstance(p, str) and scope.count(p) > 1}
            for p in sorted(dup):
                add(card, "SCOPE_DUP", f"path lặp: {p!r}")
            for entry in scope:
                for rule, msg in check_scope_entry(entry, cfg):
                    add(card, rule, msg)
            batch = d.get("batch")
            if isinstance(batch, str) and batch:
                for p in {e for e in scope if isinstance(e, str)}:
                    owner = batch_paths.get((batch, p))
                    if owner and owner != tid:
                        add(card, "SCOPE_OVERLAP", f"{p!r} cũng thuộc {owner} trong cùng batch {batch}")
                    else:
                        batch_paths[(batch, p)] = str(tid)

        deps = d.get("depends_on")
        if deps is not None:
            if isinstance(deps, str):
                deps = [deps]
            if not isinstance(deps, list):
                add(card, "DEP_FORMAT", "depends_on phải là danh sách ID task")
                deps = []
            for dep in deps:
                if not isinstance(dep, str) or not cfg.id_pattern.match(dep):
                    add(card, "DEP_FORMAT", f"phụ thuộc {dep!r} không phải ID task hợp lệ")
                elif dep == tid:
                    add(card, "DEP_SELF", "task phụ thuộc chính nó")
            if isinstance(tid, str):
                graph[tid] = [x for x in deps if isinstance(x, str)]

        if jsonschema_validator is not None:
            for err in jsonschema_validator.iter_errors(d):
                loc = "/".join(str(x) for x in err.absolute_path) or "(gốc)"
                add(card, "SCHEMA", f"{loc}: {err.message}")

    defined = set(seen)
    for card in cards:
        deps = card.data.get("depends_on") or []
        if isinstance(deps, str):
            deps = [deps]
        if not isinstance(deps, list):
            continue
        for dep in deps:
            if isinstance(dep, str) and cfg.id_pattern.match(dep) and dep not in defined and dep not in cfg.known_ids:
                add(card, "DEP_UNKNOWN", f"phụ thuộc {dep} không có thẻ trong bản kế hoạch và không có trong --known-ids")

    for cycle in find_cycles(graph):
        first = seen.get(cycle[0])
        if first:
            add(first, "DEP_CYCLE", " → ".join(cycle))

    return findings


# ---------------------------------------------------------------- CLI


def load_schema(path: Path) -> tuple[dict, list | None, str | None]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    required = schema.get("required")
    pattern = ((schema.get("properties") or {}).get("id") or {}).get("pattern")
    return schema, required, pattern


def semantic_findings(plan: Path, cards: list[Card], base_ref: str | None, use_yaml: bool) -> list[Finding]:
    text = plan.read_text(encoding="utf-8")
    findings = []
    section = re.search(r"^## 3\. Bảng OWNER / LEAD[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    known_actions = set(re.findall(r"^\|\s*(O\d+\.\d+)\s*\|", section.group(1), re.M)) if section else None
    graph = {}
    for match in re.finditer(r"^\s*-\s*([\w.]+)\s*\|\s*tasks:\s*[^\n|]*\|\s*after:\s*([^\n]*)", text, re.M):
        graph[match.group(1)] = [item.strip() for item in match.group(2).split(",") if item.strip() and item.strip() != "—"]
    for cycle in find_cycles(graph):
        findings.append(Finding(str(plan), 1, "?", "GRAPH_CYCLE", " → ".join(cycle)))
    previous = {}
    if base_ref:
        root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()
        relative = plan.resolve().relative_to(Path(root).resolve()).as_posix()
        result = subprocess.run(["git", "show", f"{base_ref}:{relative}"], capture_output=True, encoding="utf-8")
        if result.returncode:
            raise ValueError(f"không đọc được {base_ref}:{relative}: {result.stderr.strip()}")
        with tempfile.TemporaryDirectory() as directory:
            baseline = Path(directory) / "plan.md"
            baseline.write_text(result.stdout, encoding="utf-8", newline="\n")
            baseline_cards, errors = extract_cards(baseline, use_yaml)
            if errors:
                raise ValueError("không đọc được thẻ tại base")
            previous = {card.data.get("id"): card.data for card in baseline_cards}
    for card in cards:
        data = card.data
        task = str(data.get("id", "?"))
        def add(rule, message):
            findings.append(Finding(str(plan), card.line, task, rule, message))
        if task in previous:
            changed = [key for key in ("goal", "write_scope", "done_when") if data.get(key) != previous[task].get(key)]
            if changed:
                add("ID_MEANING_CHANGED", ", ".join(changed))
        if known_actions is not None:
            for key in ("constraints", "inputs"):
                for action in re.findall(r"\bO\d+\.\d+\b", str(data.get(key, ""))):
                    if action not in known_actions:
                        add("O_UNKNOWN", action)
        goal = data.get("goal")
        scope = data.get("write_scope")
        if isinstance(goal, str) and isinstance(scope, list):
            for path in re.findall(r"(?<![\w./-])(?:[\w.-]+/)+[\w.-]+\.[A-Za-z0-9]+", goal):
                if path not in scope:
                    add("GOAL_PATH_OUT_OF_SCOPE", path)
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Kiểm cơ học thẻ task trước khi gửi REVIEWER.")
    ap.add_argument("plans", nargs="+", type=Path, help="file kế hoạch (.md) chứa thẻ task")
    ap.add_argument("--schema", type=Path, help="schema task JSON của repo; lấy 'required' và id.pattern từ đây")
    ap.add_argument("--id-pattern", help=f"regex ID task (mặc định {DEFAULT_ID_PATTERN})")
    ap.add_argument("--required", help="danh sách trường bắt buộc, phân tách bằng dấu phẩy")
    ap.add_argument("--max-scope", type=int, default=DEFAULT_MAX_SCOPE)
    ap.add_argument("--branch-prefixes", default=",".join(DEFAULT_BRANCH_PREFIXES),
                    help="tiền tố nhánh hợp lệ, phân tách bằng dấu phẩy; chuỗi rỗng để tắt")
    ap.add_argument("--allow-dirs", action="store_true", help="cho phép path thư mục (kết thúc bằng '/')")
    ap.add_argument("--known-ids", action="append", type=Path, default=[],
                    help="file (sổ, STATE, kế hoạch cũ) chứa ID task đã có; lặp lại được")
    ap.add_argument("--no-yaml", action="store_true", help="không dùng PyYAML, chỉ dùng bộ đọc tối giản")
    ap.add_argument("--json", action="store_true", help="in kết quả dạng JSON")
    ap.add_argument("--base-ref", help="đối chiếu ý nghĩa thẻ với Git ref")
    args = ap.parse_args(argv)
    # Console Windows mặc định không phải UTF-8: tránh UnicodeEncodeError khi in tiếng Việt.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    try:
        schema, required, pattern = (None, None, None)
        if args.schema:
            schema, required, pattern = load_schema(args.schema)
        if args.required:
            required = [x.strip() for x in args.required.split(",") if x.strip()]
        id_regex = re.compile(args.id_pattern or pattern or DEFAULT_ID_PATTERN)
        known: set[str] = set()
        for kp in args.known_ids:
            known |= {m for m in ID_SCAN_RE.findall(kp.read_text(encoding="utf-8")) if id_regex.match(m)}
        cfg = Config(
            id_pattern=id_regex,
            required=list(required or DEFAULT_REQUIRED),
            branch_prefixes=[x.strip() for x in args.branch_prefixes.split(",") if x.strip()],
            max_scope=args.max_scope,
            allow_dirs=args.allow_dirs,
            known_ids=known,
            schema=schema,
        )
        cards, findings = [], []
        for plan in args.plans:
            c, f = extract_cards(plan, use_yaml=not args.no_yaml)
            cards += c
            findings += f
            findings += semantic_findings(plan, c, args.base_ref, not args.no_yaml)
    except (OSError, ValueError, re.error, subprocess.CalledProcessError) as exc:
        print(f"validate_task_schema: lỗi dùng lệnh hoặc đọc file: {exc}", file=sys.stderr)
        return EXIT_USAGE

    if not cards and not findings:
        msg = "không tìm thấy thẻ task nào (khối mã rào có khóa 'id') — không có gì để kiểm"
        print(json.dumps({"status": "NO_INPUT", "message": msg}) if args.json else f"NO_INPUT: {msg}")
        return EXIT_NO_INPUT

    findings += validate(cards, cfg)
    status = "FAIL" if findings else "PASS"
    if args.json:
        print(json.dumps({
            "status": status,
            "cards": len(cards),
            "findings": [f.__dict__ for f in findings],
        }, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f.text())
        print(f"{status}: {len(cards)} thẻ, {len(findings)} vi phạm")
    return EXIT_FAIL if findings else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
