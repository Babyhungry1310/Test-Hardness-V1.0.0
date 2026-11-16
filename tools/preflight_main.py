import argparse, io, json, re, subprocess, sys
from pathlib import Path


def run_git(args, cwd=None):
    res = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()


def check_branch_pattern(role, branch):
    if not branch or branch in ("main", "master"):
        return False
    pats = {
        "worker": r"^task/TK-\d{4}-R\d+$",
        "lead": r"^(lead/[a-zA-Z0-9._-]+|upgrade/[a-zA-Z0-9._-]+)$",
        "reviewer": r"^review/CYC-\d{2,}(-R\d+-[a-z0-9]{4}|-R\d+)?$",
    }
    pat = pats.get(role)
    return bool(re.match(pat, branch)) if pat else False


def run_preflight(role, stage, ref=None, cwd=None):
    rc, toplevel, _ = run_git(["rev-parse", "--show-toplevel"], cwd=cwd)
    if rc != 0:
        return 2, {"ok": False, "error": "Not a git repo", "checks": []}
    rc, branch, _ = run_git(["branch", "--show-current"], cwd=cwd)
    checks, warnings, ok = [], [], True

    def check(name, passed, reason, **kw):
        nonlocal ok
        d = {"name": name, "passed": passed, "reason": reason}
        d.update(kw)
        checks.append(d)
        if not passed:
            ok = False

    if stage in ("session", "commit"):
        not_main = bool(branch and branch not in ("main", "master"))
        check("not_main", not_main, "Not on main branch" if not_main else "On main branch")
        pat_ok = check_branch_pattern(role, branch)
        check("branch_pattern", pat_ok, f"Branch '{branch}' valid" if pat_ok else f"Branch '{branch}' invalid")

    if stage == "session":
        _, gd, _ = run_git(["rev-parse", "--git-dir"], cwd=cwd)
        _, gcd, _ = run_git(["rev-parse", "--git-common-dir"], cwd=cwd)
        is_wt = (Path(gd).resolve() != Path(gcd).resolve()) or (Path(toplevel).resolve() / ".git").is_file()
        check("worktree", is_wt, "In session worktree" if is_wt else "In main checkout")
        rc_h, hooks, _ = run_git(["config", "--get", "core.hooksPath"], cwd=cwd)
        h_stat = "installed" if (rc_h == 0 and bool(hooks.strip())) else "missing"
        check("hook", True, f"Hook path: {hooks.strip()}" if h_stat == "installed" else "Hook chưa cài", status=h_stat)
        if h_stat == "missing":
            warnings.append("Hook chưa cài")
        rc_s, st_out, _ = run_git(["status", "--porcelain"], cwd=cwd)
        clean = (rc_s == 0 and len(st_out.strip()) == 0)
        check("clean", True, "Worktree clean" if clean else "Worktree có thay đổi chưa commit", clean=clean)
        if not clean:
            warnings.append("Worktree có thay đổi chưa commit")

    elif stage == "push":
        t = ref if ref else branch
        if ":" in t:
            t = t.split(":", 1)[1]
        if t.startswith("+"):
            t = t[1:]
        norm = t[len("refs/heads/"):] if t.startswith("refs/heads/") else t
        is_tag = t.startswith("refs/tags/") or (ref.startswith("refs/tags/") if ref else False)
        is_main = t in ("main", "refs/heads/main") or norm == "main"
        match_sess = bool(branch and norm == branch and not is_tag and not is_main)
        check("not_main", not is_main, "Target not main" if not is_main else "Push target is main")
        check("not_tag", not is_tag, "Target not tag" if not is_tag else "Cannot push tag")
        check("target_matches_session", match_sess, f"Target matches {branch}" if match_sess else f"Target mismatch {branch}")
        pat_ok = check_branch_pattern(role, branch)
        check("branch_pattern", pat_ok, f"Branch '{branch}' valid" if pat_ok else f"Branch '{branch}' invalid")

    data = {"ok": ok, "role": role, "stage": stage, "checks": checks}
    if stage == "session":
        data["hook_status"] = h_stat
    if warnings:
        data["warnings"] = warnings
    return (0 if ok else 1), data


def configure_text_streams():
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name)
        if stream is None:
            continue
        encoding = (getattr(stream, "encoding", None) or "").lower().replace("-", "").replace("_", "")
        if encoding == "utf8":
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="strict")
                continue
            except (OSError, ValueError):
                pass
        buffer = getattr(stream, "buffer", None)
        if buffer is None:
            continue
        setattr(sys, name, io.TextIOWrapper(buffer, encoding="utf-8", errors="strict"))


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--role", required=True, choices=["worker", "lead", "reviewer"])
    p.add_argument("--stage", required=True, choices=["session", "commit", "push"])
    p.add_argument("--ref", default=None)
    p.add_argument("--json", action="store_true", dest="json_output")
    try:
        args = p.parse_args(argv)
    except SystemExit:
        sys.exit(2)
    configure_text_streams()
    code, data = run_preflight(args.role, args.stage, ref=args.ref)
    if args.json_output:
        print(json.dumps(data, indent=2))
    else:
        if data.get("error"):
            print(f"Lỗi: {data['error']}")
        for w in data.get("warnings", []):
            print(f"Cảnh báo: {w}")
        for c in data.get("checks", []):
            print(f"[{'PASS' if c['passed'] else 'FAIL'}] {c['name']}: {c['reason']}")
        print("Preflight PASSED" if code == 0 else "Preflight FAILED")
    sys.exit(code)


if __name__ == "__main__":
    main()