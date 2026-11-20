from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

EXIT_CLEAN = 0
EXIT_FAIL = 1
EXIT_USAGE = 2


class UsageError(Exception):
    pass


def emit(text, stream):
    data = text.encode("utf-8")
    if not data.endswith(b"\n"):
        data += b"\n"
    buf = getattr(stream, "buffer", None)
    if buf is None:
        stream.write(data.decode("utf-8"))
        return
    buf.write(data)
    buf.flush()


def git(cwd, args, check=True):
    cmd = ["git", "-C", str(cwd), "-c", "core.quotepath=false", *args]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = res.stdout.replace("\r\n", "\n").replace("\r", "\n")
    err = res.stderr.replace("\r\n", "\n").replace("\r", "\n")
    if check and res.returncode != 0:
        raise UsageError(err.strip() or out.strip() or "git failed")
    return res.returncode, out, err


def resolve_sha(repo, value):
    text = str(value).strip()
    if not text:
        raise UsageError("empty sha")
    rc, out, err = git(repo, ["rev-parse", "--verify", "--end-of-options", text + "^{commit}"], check=False)
    if rc != 0:
        raise UsageError(err.strip() or f"unknown sha {text}")
    return out.strip()


def norm_rel(value):
    text = str(value).replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    return text.strip("/")


def scope_match(path, scopes):
    rel = norm_rel(path)
    for item in scopes:
        scope = norm_rel(item)
        if not scope:
            continue
        if rel == scope or rel.startswith(scope + "/"):
            return True
    return False


def changed_files(repo, base, head):
    rc, out, err = git(repo, ["diff", "--name-only", "--diff-filter=ACDMRTUXB", f"{base}...{head}"], check=False)
    if rc != 0:
        rc, out, err = git(repo, ["diff", "--name-only", "--diff-filter=ACDMRTUXB", base, head], check=False)
    if rc != 0:
        raise UsageError(err.strip() or "diff failed")
    files = []
    seen = set()
    for line in out.split("\n"):
        name = norm_rel(line)
        if name and name not in seen:
            seen.add(name)
            files.append(name)
    return files


def conflict_files(repo):
    rc, out, err = git(repo, ["diff", "--name-only", "--diff-filter=U"], check=False)
    if rc != 0:
        raise UsageError(err.strip() or "conflict list failed")
    files = []
    seen = set()
    for line in out.split("\n"):
        name = norm_rel(line)
        if name and name not in seen:
            seen.add(name)
            files.append(name)
    return files


def load_scopes(path, heads):
    if path is None:
        return {head: [] for head in heads}
    file_path = Path(path)
    if not file_path.is_file():
        raise UsageError(f"scopes file missing: {file_path}")
    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise UsageError(f"scopes json invalid: {exc}") from exc
    if not isinstance(raw, dict):
        raise UsageError("scopes json must be an object")
    mapped = {}
    for key, value in raw.items():
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise UsageError(f"scopes for {key} must be a list of strings")
        mapped[str(key).strip().lower()] = [norm_rel(item) for item in value]
    result = {}
    for head in heads:
        result[head] = mapped.get(head.lower(), [])
    return result


def create_trial(repo, base):
    parent = Path(tempfile.mkdtemp(prefix="integrate-check-"))
    trial = parent / "trial worktree"
    git(repo, ["worktree", "add", "--detach", str(trial), base])
    return trial


def abort_merge(trial):
    rc, _out, err = git(trial, ["merge", "--abort"], check=False)
    if rc != 0:
        raise UsageError(err.strip() or "merge abort failed")


def merge_head(trial, head):
    rc, _out, err = git(
        trial,
        ["merge", "--no-ff", "--no-edit", "-m", f"integrate {head}", head],
        check=False,
    )
    if rc == 0:
        return []
    files = conflict_files(trial)
    abort_merge(trial)
    if not files:
        raise UsageError(err.strip() or "merge failed")
    return files


def tree_sha(trial):
    _, out, _err = git(trial, ["rev-parse", "HEAD^{tree}"])
    return out.strip()


def head_record(repo, base, head, scopes):
    files = changed_files(repo, base, head)
    outside = [name for name in files if scopes and not scope_match(name, scopes)]
    ancestor = git(repo, ["merge-base", "--is-ancestor", base, head], check=False)[0] == 0
    return {
        "sha": head,
        "files": files,
        "out_of_scope": outside,
        "base_offset": not ancestor,
    }


def overlaps(records):
    owners = {}
    for record in records:
        for name in record["files"]:
            owners.setdefault(name, []).append(record["sha"])
    shared = []
    for name in sorted(owners):
        shas = owners[name]
        if len(shas) >= 2:
            shared.append({"file": name, "heads": shas})
    return shared


def run_check(repo, base, heads, scopes_path):
    repo_path = Path(repo)
    if not repo_path.is_dir():
        raise UsageError(f"repo missing: {repo}")
    base_sha = resolve_sha(repo_path, base)
    head_shas = [resolve_sha(repo_path, item) for item in heads]
    scopes = load_scopes(scopes_path, head_shas)
    records = [head_record(repo_path, base_sha, head, scopes[head]) for head in head_shas]
    trial = create_trial(repo_path, base_sha)
    merged = []
    conflict = None
    for record in records:
        files = merge_head(trial, record["sha"])
        if files:
            other = base_sha
            for prev in records:
                if prev["sha"] == record["sha"]:
                    break
                if any(name in prev["files"] for name in files):
                    other = prev["sha"]
            conflict = {"files": files, "heads": [record["sha"], other]}
            break
        merged.append(record["sha"])
    result = {
        "base": base_sha,
        "merged": merged,
        "tree": tree_sha(trial),
        "worktree": str(trial),
        "heads": records,
        "out_of_scope": [
            {"sha": record["sha"], "files": record["out_of_scope"]}
            for record in records
            if record["out_of_scope"]
        ],
        "shared": overlaps(records),
        "conflict": conflict,
        "offset": [record["sha"] for record in records if record["base_offset"]],
    }
    failed = conflict is not None or bool(result["out_of_scope"])
    result["result"] = "fail" if failed else "clean"
    return EXIT_FAIL if failed else EXIT_CLEAN, result


def format_text(result):
    lines = [
        f"base: {result['base']}",
        f"merged: {', '.join(result['merged'])}",
        f"tree: {result['tree']}",
        f"worktree: {result['worktree']}",
        f"result: {result['result']}",
    ]
    for record in result["heads"]:
        files = ", ".join(record["files"])
        offset = "yes" if record["base_offset"] else "no"
        lines.append(f"head: {record['sha']} offset={offset} files={files}")
    if result["out_of_scope"]:
        for item in result["out_of_scope"]:
            lines.append(f"out_of_scope: {item['sha']} {', '.join(item['files'])}")
    else:
        lines.append("out_of_scope:")
    if result["shared"]:
        for item in result["shared"]:
            lines.append(f"shared: {item['file']} {', '.join(item['heads'])}")
    else:
        lines.append("shared:")
    if result["conflict"]:
        files = ", ".join(result["conflict"]["files"])
        shas = ", ".join(result["conflict"]["heads"])
        lines.append(f"conflict: {files} shas={shas}")
    else:
        lines.append("conflict:")
    return "\n".join(lines)


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="integrate_check.py")
    parser.add_argument("--repo")
    parser.add_argument("--base")
    parser.add_argument("--heads", nargs="+")
    parser.add_argument("--scopes")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if not args.repo or not args.base or not args.heads:
        emit("usage: python tools/integrate_check.py --repo <path> --base <sha> --heads <sha>...", sys.stderr)
        return EXIT_USAGE
    try:
        code, result = run_check(args.repo, args.base, args.heads, args.scopes)
    except UsageError as exc:
        emit(str(exc), sys.stderr)
        return EXIT_USAGE
    if args.json:
        emit(json.dumps(result, ensure_ascii=False, indent=2), sys.stdout)
    else:
        emit(format_text(result), sys.stdout)
    return code


if __name__ == "__main__":
    sys.exit(main())
