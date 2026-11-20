import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SEP = " \u00b7 "
ALLOWED = {
    "rev-parse": True,
    "for-each-ref": True,
    "worktree": {"list"},
    "status": {"--porcelain"},
    "rev-list": {"--count"},
    "merge-base": {"--is-ancestor"},
    "branch": {"--show-current"},
}


def delete_requested(argv):
    for index, token in enumerate(argv):
        low = token.lower()
        if low in {"--delete", "--prune", "--remove", "delete"}:
            return True
        if low.startswith("--mode=") and low.split("=", 1)[1] == "delete":
            return True
        if low == "--mode" and index + 1 < len(argv) and argv[index + 1].lower() == "delete":
            return True
    return False


def emit_bytes(stream, text):
    data = text.encode("utf-8")
    if not data.endswith(b"\n"):
        data += b"\n"
    buf = getattr(stream, "buffer", None)
    if buf is None:
        stream.write(data.decode("utf-8"))
        return
    buf.write(data)
    buf.flush()


def run_git(repo, args):
    if not args:
        raise RuntimeError("blocked git command")
    spec = ALLOWED.get(args[0])
    if spec is None or (spec is not True and (len(args) < 2 or args[1] not in spec)):
        raise RuntimeError("blocked git command")
    cmd = ["git", "-C", str(repo), "-c", "core.quotepath=false", *args]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = res.stdout.replace("\r\n", "\n").replace("\r", "\n")
    return res.returncode, out, res.stderr


def norm_sha(value):
    if not isinstance(value, str):
        return ""
    text = value.strip().lower()
    if text in {"", "none", "null"}:
        return ""
    return text


def as_int(value):
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def dec_codes(record):
    raw = record.get("dec", record.get("decision"))
    values = raw if isinstance(raw, list) else [raw]
    found = []
    for value in values:
        if isinstance(value, str) and value.strip() and value.strip() not in found:
            found.append(value.strip())
    return found


def parse_record(record):
    if not isinstance(record, dict):
        return None
    number = as_int(record.get("number", record.get("pr")))
    state = record.get("state", record.get("status"))
    branch = record.get("branch", record.get("source"))
    if number is None or not isinstance(state, str) or not isinstance(branch, str) or not branch.strip():
        return None
    state = state.strip().lower()
    if state not in {"open", "merged", "closed"}:
        return None
    return {
        "number": number,
        "state": state,
        "branch": branch.strip(),
        "head_sha": norm_sha(record.get("head_sha")),
        "merge_sha": norm_sha(record.get("merge_sha")),
        "decs": dec_codes(record),
    }


def load_prs(path):
    if not Path(path).is_file():
        return {}, False
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}, False
    trusted = True
    if isinstance(data, dict):
        if data.get("complete") is False or data.get("missing_pr") is True:
            trusted = False
        rows = data.get("prs")
        if not isinstance(rows, list):
            return {}, False
    elif isinstance(data, list):
        rows = data
    else:
        return {}, False
    grouped = {}
    for row in rows:
        parsed = parse_record(row)
        if parsed is None:
            trusted = False
            continue
        grouped.setdefault(parsed["branch"], []).append(parsed)
    return grouped, trusted


def choose_pr(records):
    if not records:
        return None
    chosen = records[-1]
    decs = []
    for record in records:
        for code in record["decs"]:
            if code not in decs:
                decs.append(code)
    state = chosen["state"]
    if any(record["state"] == "open" for record in records):
        state = "open"
        for record in reversed(records):
            if record["state"] == "open":
                chosen = record
                break
    return {
        "number": chosen["number"],
        "state": state,
        "head_sha": chosen["head_sha"],
        "merge_sha": chosen["merge_sha"],
        "decs": decs,
    }


def parse_refs(text):
    local = {}
    remote = {}
    for line in text.splitlines():
        if " " not in line:
            continue
        sha, ref = line.split(" ", 1)
        sha = sha.strip().lower()
        if ref.startswith("refs/heads/"):
            local[ref[len("refs/heads/"):]] = sha
        elif ref.startswith("refs/remotes/"):
            rest = ref[len("refs/remotes/"):]
            _remote_name, sep, branch = rest.partition("/")
            if sep and branch and branch != "HEAD":
                remote.setdefault(branch, []).append((_remote_name, sha))
    return local, remote


def parse_worktrees(text):
    found = {}
    current = {}

    def flush():
        ref = current.get("branch", "")
        path = current.get("worktree", "")
        if ref.startswith("refs/heads/") and path:
            found.setdefault(ref[len("refs/heads/"):], []).append(path)

    for line in text.splitlines():
        if not line.strip():
            if current:
                flush()
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    if current:
        flush()
    return found


def is_dirty(path):
    rc, out, _err = run_git(path, ["status", "--porcelain"])
    return rc != 0 or bool(out.strip())


def ancestor(repo, older, newer):
    if not older or not newer:
        return False
    rc, _out, _err = run_git(repo, ["merge-base", "--is-ancestor", older, newer])
    return rc == 0


def unmerged_count(repo, main_sha, head_sha, confirmed):
    if confirmed:
        return 0
    if not main_sha or not head_sha:
        return "none"
    rc, out, _err = run_git(repo, ["rev-list", "--count", f"{main_sha}..{head_sha}"])
    if rc != 0 or not out.strip().isdigit():
        return "none"
    return int(out.strip())


def decide(name, current, dirty, pr, trusted, matches, merge_on_main):
    if name == "main" or name.startswith("release/"):
        return "KEEP", "protected"
    if current and name == current:
        return "KEEP", "current branch"
    if dirty:
        return "KEEP", "dirty worktree"
    if not trusted:
        reasons = ["missing pr data"]
        if pr:
            reasons.extend(pr["decs"])
        return "ASK", "; ".join(reasons)
    if pr is None:
        return "ASK", "no pr"
    if pr["decs"]:
        reasons = []
        if pr["state"] == "closed":
            reasons.append("closed without merge")
        elif pr["state"] == "open":
            reasons.append("open pr")
        elif pr["state"] == "merged" and not matches:
            reasons.append("head sha differs")
        elif pr["state"] == "merged" and not merge_on_main:
            reasons.append("merge sha not on main")
        reasons.extend(pr["decs"])
        return "ASK", "; ".join(reasons)
    if pr["state"] == "open":
        return "KEEP", "open pr"
    if pr["state"] == "closed":
        return "ASK", "closed without merge"
    if pr["state"] == "merged" and matches and merge_on_main:
        return "SAFE", ""
    reasons = []
    if not matches:
        reasons.append("head sha differs")
    if not merge_on_main:
        reasons.append("merge sha not on main")
    return "ASK", "; ".join(reasons) if reasons else "missing pr data"


def where_of(name, local, remote):
    parts = []
    if name in remote:
        parts.append("remote")
    if name in local:
        parts.append("local")
    return ", ".join(parts) if parts else "local"


def head_of(name, local, remote):
    if name in local:
        return local[name]
    if name in remote and remote[name]:
        return sorted(remote[name])[0][1]
    return ""


def render_item(item):
    lines = [
        f"- branch: {item['branch']}",
        f"  where: {item['where']}",
        f"  pr: {item['pr']}{SEP}state: {item['state']}{SEP}merge_sha: {item['merge_sha']}",
        f"  head_sha: {item['head_sha']}{SEP}matches_pr_head: {item['matches_pr_head']}",
        f"  unmerged_commits: {item['unmerged_commits']}",
    ]
    if item["worktree"] == "none":
        lines.append("  worktree: none")
    else:
        lines.append(f"  worktree: {item['worktree']}{SEP}dirty: {item['dirty']}")
    verdict = f"  verdict: {item['verdict']}"
    if item["reason"]:
        verdict += f"{SEP}reason: {item['reason']}"
    lines.append(verdict)
    return "\n".join(lines)


def render(main_sha, created, items):
    body = "\n\n".join(render_item(item) for item in items)
    if body:
        body += "\n"
    code = hashlib.sha256(body.encode("utf-8")).hexdigest()
    header = f"clean-list: {code}{SEP}main: {main_sha or 'none'}{SEP}created: {created}"
    text = header + "\n" if not body else header + "\n\n" + body
    return code, text


def to_json(code, main_sha, created, items):
    payload = {"list_code": code, "main": main_sha or "none", "created": created, "items": items}
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def inside(root, dest):
    try:
        dest.resolve().relative_to(Path(root).resolve())
    except ValueError:
        return False
    return True


def build_list(repo, prs_path):
    rc, top, _err = run_git(repo, ["rev-parse", "--show-toplevel"])
    if rc != 0 or not top.strip():
        raise RuntimeError("not a git repo")
    root = Path(top.strip())
    rc, marker, _err = run_git(repo, ["rev-parse", "--is-inside-work-tree"])
    if rc != 0 or marker.strip() != "true":
        raise RuntimeError("not a git repo")
    rc, current_raw, _err = run_git(repo, ["branch", "--show-current"])
    current = current_raw.strip() if rc == 0 else ""
    rc, ref_text, _err = run_git(repo, ["for-each-ref", "--format=%(objectname) %(refname)", "refs/heads", "refs/remotes"])
    if rc != 0:
        raise RuntimeError("cannot read refs")
    local, remote = parse_refs(ref_text)
    rc, wt_text, _err = run_git(repo, ["worktree", "list", "--porcelain"])
    if rc != 0:
        raise RuntimeError("cannot read worktrees")
    worktrees = parse_worktrees(wt_text)
    main_sha = head_of("main", local, remote)
    grouped, trusted = load_prs(prs_path)
    items = []
    for name in sorted(set(local) | set(remote)):
        pr = choose_pr(grouped.get(name, []))
        head = head_of(name, local, remote)
        paths = worktrees.get(name, [])
        dirty_paths = [path for path in paths if is_dirty(path)]
        dirty = bool(dirty_paths)
        matches = bool(pr and pr["head_sha"] and head and pr["head_sha"] == head)
        merge_on_main = bool(pr and pr["state"] == "merged" and ancestor(repo, pr["merge_sha"], main_sha))
        confirmed = bool(pr and pr["state"] == "merged" and matches and merge_on_main)
        verdict, reason = decide(name, current, dirty, pr, trusted, matches, merge_on_main)
        items.append({
            "branch": name,
            "where": where_of(name, local, remote),
            "pr": pr["number"] if pr else "none",
            "state": pr["state"] if pr else "none",
            "merge_sha": pr["merge_sha"] if pr and pr["merge_sha"] else "none",
            "head_sha": head or "none",
            "matches_pr_head": "yes" if matches else "no",
            "unmerged_commits": unmerged_count(repo, main_sha, head, confirmed),
            "worktree": dirty_paths[0] if dirty_paths else (paths[0] if paths else "none"),
            "dirty": "yes" if dirty else "no",
            "verdict": verdict,
            "reason": reason,
        })
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    code, text = render(main_sha, created, items)
    roots = [root]
    for paths in worktrees.values():
        roots.extend(Path(path) for path in paths)
    return {"root": root, "roots": roots, "code": code, "text": text, "json": to_json(code, main_sha, created, items), "items": items}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if delete_requested(argv):
        emit_bytes(sys.stderr, "delete mode is not available")
        return 2
    parser = argparse.ArgumentParser(prog="clean_list")
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--prs", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    parser.add_argument("--mode", default="list")
    parser.add_argument("--delete", action="store_true")
    args = parser.parse_args(argv)
    if args.delete or args.mode.lower() != "list":
        emit_bytes(sys.stderr, "delete mode is not available")
        return 2
    try:
        report = build_list(args.repo, args.prs)
    except RuntimeError as exc:
        emit_bytes(sys.stderr, str(exc))
        return 2
    text = report["json"] if args.json_output else report["text"]
    if args.out is not None:
        if args.out.exists() and args.out.is_dir():
            emit_bytes(sys.stderr, "output path must be outside the repo")
            return 2
        if any(inside(root, args.out) for root in report["roots"]):
            emit_bytes(sys.stderr, "output path must be outside the repo")
            return 2
        try:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_bytes(text.encode("utf-8"))
        except OSError:
            emit_bytes(sys.stderr, "cannot write output")
            return 2
    emit_bytes(sys.stdout, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
