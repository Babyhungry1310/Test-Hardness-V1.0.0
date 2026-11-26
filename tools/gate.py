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
    bad = []
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
    g.add("G4", "FAIL" if bad else "PASS", "; ".join(bad) if bad else "UTF-8, không BOM, không CRLF, không NUL")


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
    acc = {}
    for v in values or []:
        path, _, rest = v.partition("=")
        rule, _, count = rest.partition(":")
        acc[path] = (rule, int(count) if count else None)
    return acc


def check_scan(g, base, head, files, accept):
    with tempfile.TemporaryDirectory() as tmp:
        scan = export_tools(g, base, tmp)
        if scan is None:
            g.add("G5", "WARN", f"{base} không có tools/scan.py")
            return
        bad, ok_notes, warns = [], [], []
        for f in files:
            if f["status"] == "D" or not f["path"].endswith(TEXT_EXT):
                continue
            data = g.blob(head, f["path"])
            target = Path(tmp) / "in" / Path(f["path"]).name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            r = subprocess.run([sys.executable, "-I", str(scan), str(target)], capture_output=True, text=True, encoding="utf-8")
            try:
                res = json.loads(r.stdout.strip().splitlines()[-1])
            except (ValueError, IndexError):
                bad.append(f"{f['path']}: scan không trả JSON")
                continue
            if res.get("level") == "ALLOW":
                continue
            rules = [x.get("rule") for x in res.get("reasons", [])]
            want = accept.get(f["path"])
            if want and set(rules) == {want[0]} and (want[1] is None or len(rules) == want[1]):
                ok_notes.append(f"{f['path']}: {res['level']} {len(rules)}× {want[0]} (OWNER chấp nhận)")
            elif res.get("level") == "WARN":
                warns.append(f"{f['path']}: WARN {sorted(set(rules))} (cần OWNER chấp nhận, BAN_GIAO 3.5)")
            else:
                bad.append(f"{f['path']}: {res.get('level')} {rules}")
    if bad:
        g.add("G5", "FAIL", "; ".join(bad + warns))
    elif warns:
        g.add("G5", "WARN", "; ".join(warns + ok_notes))
    else:
        g.add("G5", "PASS", "scan bằng tools/ của base: ALLOW" + (f"; {'; '.join(ok_notes)}" if ok_notes else ""))


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
    fails = sorted({i["check"] for i in g.items if i["level"] == "FAIL"})
    warns = sorted({i["check"] for i in g.items if i["level"] == "WARN"})
    line = f"GATE {args.task or '-'} {base[:12]}..{head[:12]}: {'ĐẠT' if not fails else 'KHÔNG ĐẠT'} · FAIL: {','.join(fails) or '-'} · WARN: {','.join(warns) or '-'}"
    print(line)
    for i in g.items:
        if i["level"] != "PASS":
            print(f"  {i['check']} {i['level']}: {i['msg']}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps({"summary": line, "base": base, "head": head, "items": g.items}, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
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
    p.add_argument("--accept-scan", action="append", help="PATH=RULE:SỐ_HIT")
    p.add_argument("--frozen", action="append", help="PATH=SHA256_12")
    p.add_argument("--run-verify", action="store_true")
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
