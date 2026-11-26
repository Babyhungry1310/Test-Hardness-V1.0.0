import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC_CARD = "06_sources/SRC-0003_kaizen-chi-tiet-dot1.md"
LEDGER_DIRS = ("04_control/decisions/", "04_control/risks/", "04_control/requests/", "05_memory/discussions/")
TEXT_EXT = (".md", ".py", ".json", ".yml", ".yaml", ".txt", ".toml", ".ini", ".cfg")
STATUS_LINE = re.compile(r"^- \d{4}-\d{2}-\d{2} \| ")
DEC_STATUS = re.compile(r"^- \d{4}-\d{2}-\d{2} \| (?:ACTIVE|SUPERSEDED_BY DEC-\d{4}|RETIRED)$")
WORKER_EXTRA = (re.compile(r"^02_work/runs/TK-\d{4}_R\d+_[A-Z]+\.md$"), re.compile(r"^03_output/CYC-\d{2}/checks/[^/]+$"))
ANSI_ESC = re.compile(rb"\x1b\[[0-9;?]*[A-Za-z]")
GATE_VERSION = "v5"
TOOLS_TEST_TRIGGERS = ("tools/", "04_control/MODEL_CATALOG.md")
SEVERITY = {"ALLOW": 0, "WARN": 1, "QUARANTINE": 2, "BLOCK": 3}
BRANCH_OK = re.compile(r"^(?:task/TK-\d{4}-R\d+|lead/[A-Za-z0-9._-]+|upgrade/[A-Za-z0-9._-]+|review/CYC-\d{2}-R\d+-[a-z0-9]{4})$")


class Gate:
    def __init__(self, repo):
        self.repo = Path(repo)
        self.items = []

    def git(self, *args, binary=False):
        r = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True)
        out = r.stdout if binary else r.stdout.decode("utf-8", "replace").strip()
        return r.returncode, out

    def blob(self, ref, path):
        rc, out = self.git("show", f"{ref}:{path}", binary=True)
        return out if rc == 0 else None

    def add(self, code, level, msg):
        self.items.append({"check": code, "level": level, "msg": msg})


def extract_card(src_text, task_id):
    for block in re.findall(r"```yaml\n(.*?)```", src_text, flags=re.S):
        if re.search(r"^id:\s*" + re.escape(task_id) + r"\s*$", block, flags=re.M):
            card = {"write_scope": [], "verify": ""}
            m = re.search(r"^write_scope:\s*\n((?:\s+-.*\n?)+)", block, flags=re.M)
            if m:
                card["write_scope"] = [l.strip()[1:].strip().strip("\"'") for l in m.group(1).splitlines() if l.strip()]
            m = re.search(r"^verify:\s*>-?\s*\n((?:[ \t]+.*\n?)+)", block, flags=re.M)
            if m:
                card["verify"] = " ".join(l.strip() for l in m.group(1).splitlines())
            return card
    return None


def changed_files(g, base, head):
    rc, out = g.git("diff", "--name-status", "-M", f"{base}...{head}")
    if rc != 0:
        raise RuntimeError(f"không diff được {base}...{head}")
    files = []
    for line in out.splitlines():
        parts = line.split("\t")
        st = parts[0]
        if st.startswith("R"):
            files.append({"status": "R", "old": parts[1], "path": parts[2]})
        else:
            files.append({"status": st[0], "old": parts[1], "path": parts[1]})
    return files


def check_scope(g, files, scope, worker_extras, limit):
    if scope is None:
        g.add("G1", "WARN", "không có write_scope (thiếu --task và --scope)")
        return
    out, counted = [], 0
    for f in files:
        in_scope = f["path"] in scope or f["old"] in scope
        extra = worker_extras and any(p.match(f["path"]) for p in WORKER_EXTRA)
        if in_scope:
            counted += 1
        elif not extra:
            out.append(f["path"])
    if out:
        g.add("G1", "FAIL", f"file ngoài write_scope: {out}")
    elif counted > limit:
        g.add("G1", "FAIL", f"{counted} path trong scope > {limit} (đổi tên tính 1)")
    else:
        g.add("G1", "PASS", f"{counted} path trong scope; {len(files) - counted} file run/bằng chứng")


def check_authors(g, base, head, agent):
    rc, out = g.git("log", "--format=%h|%an|%ae|%cn|%ce", f"{base}..{head}")
    bad = []
    for line in out.splitlines():
        h, an, ae, cn, ce = line.split("|")
        if an != agent or cn not in (agent, "GitHub"):
            bad.append(f"{h} author={an} <{ae}> committer={cn}")
    if not out:
        g.add("G2", "FAIL", "không có commit nào trong base..head")
    elif bad:
        g.add("G2", "FAIL", f"commit không mang danh tính tác tử {agent} (F50): {bad}")
    else:
        g.add("G2", "PASS", f"{len(out.splitlines())} commit đều của {agent}")


def is_subsequence(small, big):
    it = iter(big)
    return all(line in it for line in small)


def check_ledgers(g, base, head, files, allow_edit):
    bad, notes = [], []
    for f in files:
        if f["status"] == "A" or not f["path"].startswith(LEDGER_DIRS):
            continue
        old = g.blob(base, f["old"])
        new = g.blob(head, f["path"])
        if old is None or new is None:
            continue
        o = old.decode("utf-8-sig").splitlines()
        n = new.decode("utf-8-sig").splitlines()
        if f["path"] in allow_edit or f["old"] in allow_edit:
            o_status = [l for l in o if STATUS_LINE.match(l)]
            n_status = [l for l in n if STATUS_LINE.match(l)]
            if not is_subsequence(o_status, n_status):
                bad.append(f"{f['path']}: mất hoặc sửa dòng Status cũ")
            else:
                notes.append(f"{f['path']}: OWNER cho sửa, chỉ kiểm dòng Status")
        elif not is_subsequence(o, n):
            bad.append(f"{f['path']}: sửa hoặc xóa dòng cũ (sổ chỉ thêm dòng)")
    for f in files:
        if f["path"].startswith("04_control/decisions/") and f["path"].endswith(".md") and f["status"] != "D":
            data = g.blob(head, f["path"])
            if data is None:
                continue
            lines = data.decode("utf-8-sig").splitlines()
            try:
                i = lines.index("## Status (newest first)")
                if not DEC_STATUS.match(lines[i + 1]):
                    bad.append(f"{f['path']}: dòng Status mới nhất sai ngữ pháp: {lines[i + 1]}")
            except (ValueError, IndexError):
                bad.append(f"{f['path']}: thiếu mục Status")
    if bad:
        g.add("G3", "FAIL", "; ".join(bad))
    else:
        g.add("G3", "PASS", "sổ chỉ thêm dòng; Status DEC đúng ngữ pháp" + (f" ({'; '.join(notes)})" if notes else ""))


def check_encoding(g, head, files):
    bad, ansi = [], []
    for f in files:
        if f["status"] == "D" or not f["path"].endswith(TEXT_EXT):
            continue
        data = g.blob(head, f["path"])
        if data is None:
            continue
        if data.startswith((b"\xff\xfe", b"\xfe\xff")):
            bad.append(f"{f['path']}: UTF-16 (BOM {data[:2].hex()})")
        elif b"\x00" in data:
            bad.append(f"{f['path']}: có byte NUL (nghi UTF-16 hoặc nhị phân)")
        else:
            if data.startswith(b"\xef\xbb\xbf"):
                bad.append(f"{f['path']}: BOM")
            if b"\r\n" in data:
                bad.append(f"{f['path']}: CRLF")
            try:
                data.decode("utf-8")
            except UnicodeDecodeError:
                bad.append(f"{f['path']}: không phải UTF-8")
            if ANSI_ESC.search(data):
                ansi.append(f["path"])
    if bad:
        g.add("G4", "FAIL", "; ".join(bad))
    elif ansi:
        g.add("G4", "WARN", f"mã màu ANSI trong file (chạy lại với --color=no hoặc lọc ESC): {ansi}")
    else:
        g.add("G4", "PASS", "UTF-8, không BOM, không CRLF, không NUL, không mã ANSI")


def export_tools(g, base, dest):
    rc, out = g.git("ls-tree", "-r", "--name-only", base, "tools/")
    if rc != 0 or "tools/scan.py" not in out.splitlines():
        return None
    for name in out.splitlines():
        if name.startswith("tools/tests/"):
            continue
        data = g.blob(base, name)
        p = Path(dest) / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    return Path(dest) / "tools" / "scan.py"


def parse_accept(values):
    """PATH=RULE:SỐ_HIT, lặp được; nhiều quy tắc cho cùng một PATH được gộp. Số hit là số hit MỚI (head trừ base)."""
    acc = {}
    for v in values or []:
        path, _, rest = v.partition("=")
        rule, _, count = rest.partition(":")
        if not path or not rule:
            raise RuntimeError(f"--accept-scan sai dạng PATH=RULE:SỐ_HIT: {v}")
        rules = acc.setdefault(path, {})
        if rule in rules:
            raise RuntimeError(f"--accept-scan lặp quy tắc {rule} cho {path}")
        rules[rule] = int(count) if count else None
    return acc


def load_rule_levels(tool_dir):
    p = Path(tool_dir) / "tools" / "scan_rules.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}
    return {r.get("rule"): r.get("level") for r in data.get("rules", []) if isinstance(r, dict) and r.get("rule")}


def scan_blob(scan, tmp, data, name):
    target = Path(tmp) / "in" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    r = subprocess.run([sys.executable, "-I", str(scan), str(target)], capture_output=True, text=True, encoding="utf-8")
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


def count_rules(res):
    counts = {}
    for x in (res or {}).get("reasons", []):
        rule = x.get("rule")
        counts[rule] = counts.get(rule, 0) + 1
    return counts


def fmt_counts(counts):
    return ", ".join(f"{k}:{v}" for k, v in sorted(counts.items())) or "-"


def check_scan(g, base, head, files, accept):
    """G5 chấm theo chênh lệch base–head: hit có sẵn ở bản base của cùng file là kế thừa, không FAIL."""
    with tempfile.TemporaryDirectory() as tmp:
        scan = export_tools(g, base, tmp)
        if scan is None:
            g.add("G5", "WARN", f"{base} không có tools/scan.py")
            return
        levels = load_rule_levels(tmp)
        bad, warns, notes, inherited = [], [], [], []
        unused = {p for p in accept if p not in {f["path"] for f in files}}
        for f in files:
            if f["status"] == "D" or not f["path"].endswith(TEXT_EXT):
                continue
            res = scan_blob(scan, tmp, g.blob(head, f["path"]), "head_" + Path(f["path"]).name)
            if res is None:
                bad.append(f"{f['path']}: scan không trả JSON")
                continue
            head_level = res.get("level", "BLOCK")
            if head_level == "ALLOW":
                continue
            head_counts = count_rules(res)
            base_counts, base_level = {}, "ALLOW"
            old = g.blob(base, f["old"]) if f["status"] != "A" else None
            if old is not None:
                bres = scan_blob(scan, tmp, old, "base_" + Path(f["old"]).name)
                if bres is None:
                    bad.append(f"{f['path']}: scan bản base không trả JSON")
                    continue
                base_counts, base_level = count_rules(bres), bres.get("level", "ALLOW")
            new = {r: n - base_counts.get(r, 0) for r, n in head_counts.items() if n > base_counts.get(r, 0)}
            kept = sum(min(n, base_counts.get(r, 0)) for r, n in head_counts.items())
            tag = f"{f['path']}: {head_level}, kế thừa {kept}, mới {sum(new.values())}"
            if not new:
                inherited.append(tag)
                continue
            sev = max(SEVERITY.get(levels.get(r) or head_level, 3) for r in new)
            if head_level == "QUARANTINE" and base_level != "QUARANTINE":
                sev = max(sev, SEVERITY["QUARANTINE"])
            want = accept.get(f["path"])
            if want is not None:
                if set(want) == set(new) and all(c is None or c == new[r] for r, c in want.items()):
                    notes.append(f"{tag} [{fmt_counts(new)}] (OWNER chấp nhận)")
                else:
                    bad.append(f"{tag} [{fmt_counts(new)}] ≠ chấp nhận [{fmt_counts({r: c if c is not None else '*' for r, c in want.items()})}]")
            elif sev >= SEVERITY["QUARANTINE"]:
                bad.append(f"{tag} [{fmt_counts(new)}]")
            else:
                warns.append(f"{tag} [{fmt_counts(new)}] (WARN, cần OWNER chấp nhận)")
        for p in sorted(unused):
            bad.append(f"--accept-scan nêu {p} nhưng file không có trong diff")
    tail = [s for s in (("kế thừa: " + "; ".join(inherited)) if inherited else "", "; ".join(notes)) if s]
    if bad:
        g.add("G5", "FAIL", "; ".join(bad + warns + tail))
    elif warns:
        g.add("G5", "WARN", "; ".join(warns + tail))
    else:
        g.add("G5", "PASS", "scan bằng tools/ của base: không có hit mới" + (f"; {'; '.join(tail)}" if tail else ""))


def check_frozen(g, head, frozen):
    if not frozen:
        return
    bad = []
    for v in frozen:
        path, _, want = v.partition("=")
        data = g.blob(head, path)
        got = hashlib.sha256(data).hexdigest() if data is not None else "không có file"
        if not got.startswith(want.lower()):
            bad.append(f"{path}: {got[:12]} ≠ {want}")
    g.add("G6", "FAIL" if bad else "PASS", "; ".join(bad) if bad else f"{len(frozen)} file khớp hash bản nháp")


def check_verify(g, head, card, timeout):
    if not card or not card["verify"]:
        g.add("G7", "WARN", "không có lệnh verify để chạy")
        return
    tmp = tempfile.mkdtemp(prefix="gate_")
    wt = Path(tmp) / "wt"
    rc, _ = g.git("worktree", "add", "--detach", str(wt), head)
    if rc != 0:
        g.add("G7", "FAIL", "không tạo được worktree để chạy verify")
        return
    try:
        cmd = card["verify"].replace("python ", f'"{sys.executable}" ', 1).replace("&& python ", f'&& "{sys.executable}" ')
        r = subprocess.run(cmd, shell=True, cwd=wt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
        g.add("G7", "PASS" if r.returncode == 0 else "FAIL", f"verify mã {r.returncode}: {' | '.join(tail)}")
    except subprocess.TimeoutExpired:
        g.add("G7", "FAIL", f"verify quá {timeout}s")
    finally:
        g.git("worktree", "remove", "--force", str(wt))
        shutil.rmtree(tmp, ignore_errors=True)


def pytest_failures(g, ref, timeout):
    """Chạy tools/tests trong worktree tạm của ref; trả (mã, tập test hỏng hoặc lỗi thu thập, dòng tóm tắt)."""
    tmp = tempfile.mkdtemp(prefix="gate_t_")
    wt = Path(tmp) / "wt"
    rc, _ = g.git("worktree", "add", "--detach", str(wt), ref)
    if rc != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        return None, set(), f"không tạo được worktree cho {ref[:12]}"
    try:
        cmd = [sys.executable, "-m", "pytest", "-q", "--tb=no", "-rfE", "--color=no", "-p", "no:cacheprovider",
               "--continue-on-collection-errors", "tools/tests"]
        r = subprocess.run(cmd, cwd=wt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        failed = set()
        for line in r.stdout.splitlines():
            m = re.match(r"^(FAILED|ERROR) (\S+)", line)
            if m:
                failed.add(m.group(2))
        lines = [l for l in r.stdout.strip().splitlines() if l.strip()]
        return r.returncode, failed, (lines[-1] if lines else (r.stderr.strip().splitlines() or [""])[-1])
    except subprocess.TimeoutExpired:
        return None, set(), f"tools/tests quá {timeout}s"
    finally:
        g.git("worktree", "remove", "--force", str(wt))
        shutil.rmtree(tmp, ignore_errors=True)


def check_tools_tests(g, base, head, files, run_tests, timeout):
    """G11: PR chạm tools/ hoặc MODEL_CATALOG.md phải chạy cả tools/tests; chấm theo chênh lệch (test hỏng mới = 0)."""
    touched = [f["path"] for f in files if f["path"].startswith(TOOLS_TEST_TRIGGERS) or f["old"].startswith(TOOLS_TEST_TRIGGERS)]
    if not touched:
        return
    if not run_tests:
        g.add("G11", "WARN", f"PR chạm {touched[:3]} nhưng chưa chạy tools/tests (thêm --run-tools-tests)")
        return
    hrc, hfail, hsum = pytest_failures(g, head, timeout)
    brc, bfail, bsum = pytest_failures(g, base, timeout)
    if hrc is None or brc is None:
        g.add("G11", "FAIL", f"head: {hsum}; base: {bsum}")
        return
    new = sorted(hfail - bfail)
    fixed = sorted(bfail - hfail)
    kept = sorted(hfail & bfail)
    info = f"head: {hsum} | base: {bsum}" + (f" | kế thừa {len(kept)} hỏng: {kept[:5]}" if kept else "") + (f" | đã sửa {len(fixed)}: {fixed[:5]}" if fixed else "")
    if new:
        g.add("G11", "FAIL", f"test hỏng mới {len(new)}: {new[:10]} | {info}")
    elif hrc not in (0, 1) and hrc != brc:
        g.add("G11", "FAIL", f"pytest trên head mã {hrc} (base mã {brc}) | {info}")
    else:
        g.add("G11", "PASS", f"không có test hỏng mới | {info}")


def check_run_schema(g, base, head, files):
    runs = [f for f in files if f["status"] in ("A", "M", "R") and f["path"].startswith("02_work/runs/") and f["path"].endswith(".md")]
    if not runs:
        return
    try:
        import jsonschema
        import yaml
    except ImportError:
        g.add("G10", "WARN", "thiếu jsonschema hoặc pyyaml; không kiểm schema file run")
        return
    raw = g.blob(base, "harness/schemas/run.schema.json")
    if raw is None:
        g.add("G10", "WARN", "base không có harness/schemas/run.schema.json")
        return
    schema = json.loads(raw.decode("utf-8-sig"))
    bad = []
    for f in runs:
        text = g.blob(head, f["path"]).decode("utf-8-sig")
        parts = text.split("---")
        if len(parts) < 3:
            bad.append(f"{f['path']}: không có front matter")
            continue
        try:
            data = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            bad.append(f"{f['path']}: YAML lỗi {str(e)[:60]}")
            continue
        errs = [e.message[:100] for e in jsonschema.Draft202012Validator(schema).iter_errors(data)]
        if errs:
            bad.append(f"{f['path']}: {errs[:3]}")
    g.add("G10", "FAIL" if bad else "PASS", "; ".join(bad) if bad else f"{len(runs)} file run qua run.schema.json")


def check_run_file(g, files, branch, task):
    if not branch or not branch.startswith("task/") or not task:
        return
    runs = [f["path"] for f in files if f["status"] == "A" and re.match(rf"^02_work/runs/{task}_R\d+_[A-Z]+\.md$", f["path"])]
    g.add("G9", "PASS" if runs else "FAIL", f"run: {runs}" if runs else f"nhánh task/ không có file run 02_work/runs/{task}_Rn_<OUTCOME>.md (WORKER luật 4, 10)")


def check_branch(g, branch):
    if not branch:
        return
    g.add("G8", "PASS" if BRANCH_OK.match(branch) else "WARN", f"nhánh {branch}" + ("" if BRANCH_OK.match(branch) else " không đúng mẫu"))


def run(args):
    g = Gate(args.repo)
    rc, head = g.git("rev-parse", args.head)
    rc2, base = g.git("rev-parse", args.base)
    if rc or rc2:
        print("không đọc được base hoặc head", file=sys.stderr)
        return 2
    card = None
    if args.task:
        src = g.blob(base, SRC_CARD)
        card = extract_card(src.decode("utf-8-sig"), args.task) if src else None
        if card is None:
            print(f"không thấy thẻ {args.task} trong {SRC_CARD} @ base", file=sys.stderr)
            return 2
    scope = args.scope if args.scope else (card["write_scope"] if card else None)
    files = changed_files(g, base, head)
    check_scope(g, files, scope, not args.no_worker_extras, args.limit)
    check_authors(g, base, head, args.agent)
    check_ledgers(g, base, head, files, set(args.allow_edit or []))
    check_encoding(g, head, files)
    check_scan(g, base, head, files, parse_accept(args.accept_scan))
    check_frozen(g, head, args.frozen)
    if args.run_verify:
        check_verify(g, head, card, args.timeout)
    branch = args.branch or (args.head if args.head.startswith(("task/", "lead/", "upgrade/", "review/")) else None)
    check_run_file(g, files, branch, args.task)
    check_run_schema(g, base, head, files)
    check_branch(g, branch)
    check_tools_tests(g, base, head, files, args.run_tools_tests, args.timeout)
    fails = sorted({i["check"] for i in g.items if i["level"] == "FAIL"})
    warns = sorted({i["check"] for i in g.items if i["level"] == "WARN"})
    line = f"GATE {args.task or '-'} {base[:12]}..{head[:12]}: {'ĐẠT' if not fails else 'KHÔNG ĐẠT'} · FAIL: {','.join(fails) or '-'} · WARN: {','.join(warns) or '-'}"
    print(line)
    for i in g.items:
        if i["level"] != "PASS":
            print(f"  {i['check']} {i['level']}: {i['msg']}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps({"summary": line, "gate_version": GATE_VERSION, "base": base, "head": head, "items": g.items}, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    return 1 if fails and not args.warn_only else 0


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
    p = argparse.ArgumentParser(description="Cổng máy sau khi làm: kiểm một nhánh so với base.")
    p.add_argument("--repo", default=".")
    p.add_argument("--base", default="origin/main")
    p.add_argument("--head", required=True)
    p.add_argument("--branch")
    p.add_argument("--task")
    p.add_argument("--scope", nargs="*")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--no-worker-extras", action="store_true")
    p.add_argument("--agent", default="conchonomoconmeo-AIAIAI")
    p.add_argument("--allow-edit", action="append")
    p.add_argument("--accept-scan", action="append", help="PATH=RULE:SỐ_HIT_MỚI; lặp để chấp nhận nhiều quy tắc cho một file")
    p.add_argument("--frozen", action="append", help="PATH=SHA256_12")
    p.add_argument("--run-verify", action="store_true")
    p.add_argument("--run-tools-tests", action="store_true", help="G11: chạy tools/tests ở base và head, chấm theo chênh lệch")
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--json-out")
    p.add_argument("--warn-only", action="store_true")
    try:
        args = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        return run(args)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
