import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

COPY_WORDS = ("chép nguyên văn", "nạp", "sanitize", "đồng bộ", "verbatim", "copy", "ingest", "sync")
SELF_LINES_WORDS = ("chỉ tính dòng tự viết", "dòng tự viết", "self-authored", "source copy size excluded")
FRAME_KEYS = ("TỪ", "ĐẾN", "LOẠI", "MÃ", "REF", "CẦN LÀM", "DỪNG KHI", "TRẢ LỜI")
MACHINE_PATH = re.compile(r"[A-Za-z]:\\Users\\|%USERPROFILE%|/home/[a-z_][a-z0-9_-]*/|/Users/[A-Za-z]")
FILE_TOKEN = re.compile(r"[\w.\-/ ]*?([\w.\-]+\.(?:md|py|zip|json|txt|csv))")
SRC_CARD = "06_sources/SRC-0003_kaizen-chi-tiet-dot1.md"


class Result:
    def __init__(self):
        self.items = []

    def add(self, code, level, msg):
        self.items.append({"check": code, "level": level, "msg": msg})

    def levels(self, level):
        return sorted({i["check"] for i in self.items if i["level"] == level})


def read_text(path):
    return Path(path).read_bytes().decode("utf-8-sig").replace("\r\n", "\n")


def table_rows(section):
    rows = []
    for line in section.splitlines():
        s = line.strip()
        if not s.startswith("|") or set(s) <= set("|- :"):
            continue
        rows.append([c.strip() for c in s.strip("|").split("|")])
    return rows[1:] if rows else rows


def ticks(cell):
    return re.findall(r"`([^`]+)`", cell)


def split_sections(text):
    parts = re.split(r"^## ", text, flags=re.M)
    out = {}
    for p in parts[1:]:
        head, _, body = p.partition("\n")
        m = re.match(r"(\d+)\.", head.strip())
        if m:
            out[int(m.group(1))] = body
    return out


def load_muc_luc(path):
    secs = split_sections(read_text(path))
    canonical = {}
    for row in table_rows(secs.get(1, "")):
        if len(row) < 2:
            continue
        for t in ticks(row[1]):
            p = t.replace("\\", "/")
            if p.startswith("../") and p.count("/") >= 2:
                name = p.rsplit("/", 1)[1]
                canonical[name] = p.rsplit("/", 1)[0][3:]
    old = set()
    for row in table_rows(secs.get(3, "")):
        if row:
            for t in ticks(row[0]):
                old.add(t.replace("\\", "/"))
    dup = set()
    for row in table_rows(secs.get(4, "")):
        if row:
            for t in ticks(row[0]):
                if "…" not in t and "*" not in t:
                    dup.add(t)
    return {"canonical": canonical, "old": old, "dup": dup}


def referenced_names(text):
    names = set()
    for m in FILE_TOKEN.finditer(text):
        names.add(m.group(1))
    return names


def extract_card(src_text, task_id):
    for block in re.findall(r"```yaml\n(.*?)```", src_text, flags=re.S):
        if re.search(r"^id:\s*" + re.escape(task_id) + r"\s*$", block, flags=re.M):
            return parse_card(block)
    return None


def parse_card(block):
    card = {"write_scope": [], "verify": "", "line_budget": None, "o_codes": sorted(set(re.findall(r"\bO\d+\.\d+\b", block)))}
    m = re.search(r"^line_budget:\s*(\d+)", block, flags=re.M)
    if m:
        card["line_budget"] = int(m.group(1))
    m = re.search(r"^write_scope:\s*\n((?:\s+-.*\n?)+)", block, flags=re.M)
    if m:
        card["write_scope"] = [l.strip()[1:].strip().strip("\"'") for l in m.group(1).splitlines() if l.strip()]
    m = re.search(r"^verify:\s*>-?\s*\n((?:[ \t]+.*\n?)+)", block, flags=re.M)
    if m:
        card["verify"] = " ".join(l.strip() for l in m.group(1).splitlines())
    else:
        m = re.search(r"^verify:\s*(.+)$", block, flags=re.M)
        if m:
            card["verify"] = m.group(1).strip().strip("\"'")
    return card


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout.strip()


def resolve_sources(text, maps):
    found = []
    for prefix, base in maps:
        for m in re.finditer(re.escape(prefix) + r"([\w.\-/ ]+?\.(?:md|py|txt|json))", text):
            p = Path(base) / m.group(1)
            if p.is_file() and p not in found:
                found.append(p)
    return found


def check_sources(text, ml, res):
    names = referenced_names(text)
    bad = []
    for old in ml["old"]:
        if old.startswith("../") and old in text.replace("\\", "/"):
            bad.append(f"dùng bản cũ {old}")
    for name in sorted(names & ml["dup"]):
        canon = ml["canonical"].get(name)
        if canon and canon.lower() not in text.lower():
            bad.append(f"{name} trùng tên ở nhiều thư mục; phiếu không nêu thư mục chuẩn '{canon}'")
    if bad:
        res.add("P1", "FAIL", "; ".join(bad))
    else:
        res.add("P1", "PASS", "nguồn khớp mục lục")


def check_markers(text, res):
    is_copy = any(w in text.lower() for w in COPY_WORDS)
    if not is_copy:
        res.add("P2", "PASS", "không phải task nạp/chép")
    elif "--contains" in text or re.search(r"\bE\d{2}\b", text):
        res.add("P2", "PASS", "có dấu hiệu nội dung")
    elif ("--sha256" in text or "hash" in text.lower()) and "MUC_LUC" in text:
        res.add("P2", "PASS", "nguồn chốt bằng hash, đường dẫn từ mục lục")
    else:
        res.add("P2", "WARN", "task nạp/chép nhưng không có dấu hiệu nội dung (--contains, mã E)")


def check_scan(text, sources, scan_cmd, res):
    if not scan_cmd:
        res.add("P3", "WARN", "không chạy scan (thiếu --repo hoặc --scan-cmd)")
        return
    if not sources:
        res.add("P3", "WARN", "không đọc được file nguồn nào (thêm --map)")
        return
    problems, warns = [], []
    for src in sources:
        r = subprocess.run([*scan_cmd, str(src)], capture_output=True, text=True, encoding="utf-8")
        try:
            data = json.loads(r.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            problems.append(f"{src.name}: scan không trả JSON")
            continue
        level = data.get("level")
        if level == "ALLOW":
            continue
        rules = sorted({x.get("rule", "?") for x in data.get("reasons", [])})
        accepted = all(rule in text for rule in rules)
        note = f"{src.name}: {level} {','.join(rules)}"
        if accepted:
            warns.append(note + " (phiếu nêu quy tắc)")
        elif level == "WARN":
            warns.append(note)
        else:
            problems.append(note)
    if problems:
        res.add("P3", "FAIL", "; ".join(problems))
    elif warns:
        res.add("P3", "WARN", "; ".join(warns))
    else:
        res.add("P3", "PASS", f"{len(sources)} nguồn ALLOW")


def check_budget(text, card, sources, res):
    if not card or card["line_budget"] is None:
        res.add("P4", "WARN", "không có thẻ hoặc line_budget")
        return
    is_copy = any(w in text.lower() for w in COPY_WORDS)
    if is_copy and not sources:
        res.add("P4", "WARN", f"task nạp/chép nhưng không đọc được nguồn để so line_budget {card['line_budget']} (thêm --map)")
        return
    copied = sum(len(read_text(s).splitlines()) for s in sources) if is_copy else 0
    if copied > card["line_budget"] and not any(w in text for w in SELF_LINES_WORDS):
        res.add("P4", "FAIL", f"nguồn chép {copied} dòng > line_budget {card['line_budget']}; phiếu chưa ghi 'chỉ tính dòng tự viết'")
    else:
        res.add("P4", "PASS", f"line_budget {card['line_budget']}, dòng chép {copied}")


def check_scope(card, res):
    if not card:
        res.add("P5", "WARN", "không có thẻ")
        return
    ws = card["write_scope"]
    bad = [p for p in ws if "*" in p or "?" in p]
    if len(ws) > 5 or bad or not ws:
        res.add("P5", "FAIL", f"write_scope {len(ws)} path; wildcard: {bad}")
    else:
        res.add("P5", "PASS", f"write_scope {len(ws)} path")


def check_verify(card, repo, text, res):
    if not card or not card["verify"]:
        res.add("P6", "WARN", "không có lệnh verify")
        return
    missing = []
    if repo:
        for tool in sorted(set(re.findall(r"python\s+(tools/[\w./-]+\.py)", card["verify"]))):
            if not (Path(repo) / tool).is_file():
                missing.append(tool)
    notes = []
    if re.search(r"--regex\s+\"[^\"]*\$\"", card["verify"]):
        notes.append("regex có $ nhạy CRLF trên Windows (F53)")
    if missing:
        local_ok = "bản cục bộ" in text or "local `P6D/tools" in text or "P6D/tools/" in text
        lvl = "WARN" if local_ok else "FAIL"
        res.add("P6", lvl, f"verify gọi script chưa có trong repo: {missing}" + ("; phiếu chỉ bản cục bộ" if local_ok else ""))
    elif notes:
        res.add("P6", "WARN", "; ".join(notes))
    else:
        res.add("P6", "PASS", "verify chạy được trên checkout")


def check_ref(text, repo, origin_ref, res):
    m = re.search(r"(?:origin/main|main)\s*@\s*`?([0-9a-f]{7,40})", text)
    if not m:
        res.add("P7", "FAIL", "phiếu không ghi REF origin/main @ <sha>")
        return
    sha = m.group(1)
    if not repo:
        res.add("P7", "WARN", f"REF {sha}; không có --repo để đối chiếu")
        return
    rc, cur = git(repo, "rev-parse", origin_ref)
    if rc != 0:
        res.add("P7", "WARN", f"không đọc được {origin_ref}")
    elif cur.startswith(sha):
        res.add("P7", "PASS", f"REF khớp {origin_ref} {cur[:12]}")
    else:
        res.add("P7", "FAIL", f"REF {sha} khác {origin_ref} {cur[:12]}; rà lại phiếu (F42)")


def check_frame(text, res):
    missing = [k for k in FRAME_KEYS if not re.search(r"^\s*(?:\S.*?\s)?" + re.escape(k) + r"\b", text, flags=re.M)]
    res.add("P8", "WARN" if missing else "PASS", f"thiếu khóa khung F34: {missing}" if missing else "đủ khung F34")


def check_owner_decisions(text, card, res):
    if not card or not card.get("o_codes"):
        res.add("P10", "PASS", "thẻ không nhắc quyết định O")
        return
    missing = [c for c in card["o_codes"] if not re.search(re.escape(c) + r"\b\s*(?:\(|chốt|:|=|đã chốt)", text)]
    if missing:
        res.add("P10", "FAIL", f"thẻ cần quyết định {missing} nhưng phiếu không ghi nội dung đã chốt (F57)")
    else:
        res.add("P10", "PASS", f"phiếu có quyết định {card['o_codes']}")


def check_machine_paths(text, res):
    hits = sorted(set(MACHINE_PATH.findall(text)))
    res.add("P9", "WARN" if hits else "PASS", f"đường dẫn máy: {hits}" if hits else "không có đường dẫn máy")


def run(args):
    text = read_text(args.phieu)
    res = Result()
    ml = load_muc_luc(args.muc_luc) if args.muc_luc else {"canonical": {}, "old": set(), "dup": set()}
    maps = []
    for m in args.map or []:
        prefix, _, base = m.partition("=")
        maps.append((prefix, base))
    sources = resolve_sources(text, maps)
    card = None
    task = args.task or (re.search(r"MÃ:\s*(TK-\d{4})", text) or re.search(r"(TK-\d{4})", text) or [None, None])[1]
    if args.card:
        card = extract_card(read_text(args.card), task) if task else None
    elif args.repo and task:
        rc, out = git(args.repo, "show", f"{args.origin}:{SRC_CARD}")
        card = extract_card(out, task) if rc == 0 else None
    scan_cmd = args.scan_cmd.split() if args.scan_cmd else ([sys.executable, str(Path(args.repo) / "tools" / "scan.py")] if args.repo else None)
    check_sources(text, ml, res)
    check_markers(text, res)
    check_scan(text, sources, scan_cmd, res)
    check_budget(text, card, sources, res)
    check_scope(card, res)
    check_verify(card, args.repo, text, res)
    check_ref(text, args.repo, args.origin, res)
    check_frame(text, res)
    check_machine_paths(text, res)
    check_owner_decisions(text, card, res)
    fails, warns = res.levels("FAIL"), res.levels("WARN")
    total = len({i["check"] for i in res.items})
    ok = total - len(set(fails))
    line = f"PREFLIGHT {task or '?'}: {ok}/{total} đạt · FAIL: {','.join(fails) or '-'} · WARN: {','.join(warns) or '-'}"
    report = {"task": task, "phieu": str(args.phieu), "summary": line, "items": res.items}
    print(line)
    for i in res.items:
        if i["level"] != "PASS":
            print(f"  {i['check']} {i['level']}: {i['msg']}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    if fails and not args.warn_only:
        return 1
    return 0


def _utf8_console():
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass


def main(argv=None):
    _utf8_console()
    p = argparse.ArgumentParser(description="Kiểm phiếu giao việc trước khi giao (PREFLIGHT).")
    p.add_argument("phieu")
    p.add_argument("--muc-luc")
    p.add_argument("--repo")
    p.add_argument("--origin", default="origin/main")
    p.add_argument("--task")
    p.add_argument("--card")
    p.add_argument("--map", action="append", help="TIỀN_TỐ=THƯ_MỤC, ví dụ DSG/=../DSG update")
    p.add_argument("--scan-cmd")
    p.add_argument("--json-out")
    p.add_argument("--warn-only", action="store_true")
    try:
        args = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    if not Path(args.phieu).is_file():
        print(f"không thấy phiếu {args.phieu}", file=sys.stderr)
        return 2
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
