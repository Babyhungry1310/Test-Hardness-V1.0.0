import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tools.clean_list import run_git

SCRIPT = Path(__file__).resolve().parents[1] / "clean_list.py"
DOT = "\u00b7"
HEADER = re.compile(
    r"^clean-list: [0-9a-f]{64} " + re.escape(DOT) + r" main: [0-9a-f]{40} "
    + re.escape(DOT) + r" created: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)


def git(cwd, *args):
    res = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        raise AssertionError(res.stderr or res.stdout)
    return res.stdout.strip()


def init_pair(tmp_path):
    bare = tmp_path / "origin.git"
    repo = tmp_path / "repo"
    git(tmp_path, "init", "--bare", "-b", "main", str(bare))
    git(tmp_path, "init", "-b", "main", str(repo))
    git(repo, "config", "user.name", "Worker Test")
    git(repo, "config", "user.email", "worker@test.local")
    git(repo, "config", "commit.gpgsign", "false")
    git(repo, "config", "core.autocrlf", "false")
    (repo / "file.txt").write_bytes(b"initial\n")
    git(repo, "add", "file.txt")
    git(repo, "commit", "-m", "init")
    git(repo, "remote", "add", "origin", str(bare))
    git(repo, "push", "-u", "origin", "main")
    return repo


def commit_on(repo, branch, text, message, new=True):
    git(repo, "checkout", "-b" if new else branch, branch) if new else git(repo, "checkout", branch)
    (repo / "file.txt").write_bytes(text.encode("utf-8"))
    git(repo, "add", "file.txt")
    git(repo, "commit", "-m", message)
    sha = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "main")
    return sha


def write_prs(path, data):
    path.write_bytes(json.dumps(data).encode("utf-8"))


def run_clean(repo, prs, extra=None):
    args = [sys.executable, str(SCRIPT), "--repo", str(repo), "--prs", str(prs)]
    if extra:
        args.extend(extra)
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8")


def snap(repo):
    return (
        git(repo, "for-each-ref"),
        git(repo, "worktree", "list"),
        git(repo, "config", "--list"),
    )


def blocks(text):
    body = text.split("\n\n", 1)[1]
    return [part.strip("\n") for part in body.split("\n\n") if part.startswith("- branch:")]


def by_branch(text):
    found = {}
    for block in blocks(text):
        name = block.splitlines()[0].split(": ", 1)[1]
        found[name] = block
    return found


def verdict_of(block):
    line = [item for item in block.splitlines() if item.startswith("  verdict: ")][0]
    return line.split(": ", 1)[1]


def list_code(text):
    return text.splitlines()[0].split(" ", 1)[1].split(f" {DOT} ", 1)[0]


def pr(number, state, branch, head, merge, dec=None):
    row = {"number": number, "state": state, "branch": branch, "head_sha": head, "merge_sha": merge}
    if dec:
        row["dec"] = dec
    return row


def scenario(tmp_path):
    repo = init_pair(tmp_path)
    main_sha = git(repo, "rev-parse", "main")
    merged = commit_on(repo, "task/merged-safe", "merged\n", "merged")
    opened = commit_on(repo, "task/open-keep", "open\n", "open")
    closed = commit_on(repo, "task/closed-ask", "closed\n", "closed")
    old = commit_on(repo, "task/sha-ask", "old\n", "old")
    commit_on(repo, "task/sha-ask", "new\n", "new", new=False)
    dirty = commit_on(repo, "task/dirty-keep", "dirty\n", "dirty")
    current = commit_on(repo, "task/current-keep", "current\n", "current")
    dec = commit_on(repo, "task/dec-ask", "dec\n", "dec")
    clean = commit_on(repo, "task/clean-wt", "clean\n", "clean")
    commit_on(repo, "task/no-pr", "none\n", "none")
    git(repo, "branch", "release/1.0", "main")
    for name in ("task/merged-safe", "task/clean-wt", "task/dec-ask"):
        git(repo, "push", "origin", name)
    git(repo, "push", "origin", "main:task/remote-only")
    clean_wt = tmp_path / "clean wt"
    dirty_wt = tmp_path / "dirty wt"
    git(repo, "worktree", "add", str(clean_wt), "task/clean-wt")
    git(repo, "worktree", "add", str(dirty_wt), "task/dirty-keep")
    (dirty_wt / "extra.txt").write_bytes(b"dirty\n")
    git(repo, "checkout", "task/current-keep")
    rows = [
        pr(18, "merged", "task/merged-safe", merged, main_sha),
        pr(19, "open", "task/open-keep", opened, None),
        pr(21, "closed", "task/closed-ask", closed, None),
        pr(22, "merged", "task/sha-ask", old, main_sha),
        pr(23, "merged", "task/dirty-keep", dirty, main_sha),
        pr(24, "merged", "task/current-keep", current, main_sha),
        pr(20, "merged", "task/dec-ask", dec, main_sha, "DEC-0014"),
        pr(25, "merged", "task/clean-wt", clean, main_sha),
    ]
    path = tmp_path / "prs.json"
    write_prs(path, rows)
    return repo, path


def test_verdicts_format_and_refs_unchanged(tmp_path):
    repo, path = scenario(tmp_path)
    before = snap(repo)
    res = run_clean(repo, path)
    assert res.returncode == 0, res.stderr
    assert snap(repo) == before
    text = res.stdout
    assert HEADER.match(text.splitlines()[0])
    body = text.split("\n\n", 1)[1]
    assert list_code(text) == hashlib.sha256(body.encode("utf-8")).hexdigest()
    found = by_branch(text)
    assert verdict_of(found["main"]) == "KEEP" + f" {DOT} reason: protected"
    assert verdict_of(found["release/1.0"]) == "KEEP" + f" {DOT} reason: protected"
    assert verdict_of(found["task/current-keep"]) == "KEEP" + f" {DOT} reason: current branch"
    assert verdict_of(found["task/open-keep"]) == "KEEP" + f" {DOT} reason: open pr"
    assert verdict_of(found["task/dirty-keep"]) == "KEEP" + f" {DOT} reason: dirty worktree"
    assert verdict_of(found["task/no-pr"]) == "ASK" + f" {DOT} reason: no pr"
    assert verdict_of(found["task/remote-only"]) == "ASK" + f" {DOT} reason: no pr"
    assert verdict_of(found["task/closed-ask"]) == "ASK" + f" {DOT} reason: closed without merge"
    assert verdict_of(found["task/sha-ask"]) == "ASK" + f" {DOT} reason: head sha differs"
    assert "DEC-0014" in verdict_of(found["task/dec-ask"])
    assert verdict_of(found["task/dec-ask"]).startswith("ASK ")
    assert verdict_of(found["task/merged-safe"]) == "SAFE"
    assert verdict_of(found["task/clean-wt"]) == "SAFE"
    assert "SAFE" not in verdict_of(found["task/dec-ask"])
    safe = found["task/merged-safe"]
    assert safe.splitlines()[1] == "  where: remote, local"
    assert "matches_pr_head: yes" in safe
    assert "unmerged_commits: 0" in safe
    assert "worktree: none" in safe
    assert "pr: 18 " + DOT + " state: merged " + DOT + " merge_sha:" in safe
    clean = found["task/clean-wt"]
    assert "dirty: no" in clean
    assert "worktree: none" not in clean
    dirty = found["task/dirty-keep"]
    assert "dirty: yes" in dirty
    assert "dirty wt" in dirty or "dirty-wt" in dirty.replace("\\", "/")
    closed_block = found["task/closed-ask"]
    assert "merge_sha: none" in closed_block
    assert "unmerged_commits: 1" in closed_block
    assert "matches_pr_head: yes" in closed_block
    assert found["task/sha-ask"].count("matches_pr_head: no") == 1
    assert found["task/no-pr"].splitlines()[1] == "  where: local"
    assert found["task/remote-only"].splitlines()[1] == "  where: remote"
    keys = []
    for line in safe.splitlines():
        raw = line[2:] if line.startswith("- ") else line.strip()
        keys.append(raw.split(":", 1)[0])
    assert keys == ["branch", "where", "pr", "head_sha", "unmerged_commits", "worktree", "verdict"]
    again = run_clean(repo, path)
    assert again.returncode == 0
    assert list_code(again.stdout) == list_code(text)
    assert snap(repo) == before
    git(repo, "checkout", "task/no-pr")
    (repo / "file.txt").write_bytes(b"changed\n")
    git(repo, "add", "file.txt")
    git(repo, "commit", "-m", "change")
    git(repo, "checkout", "task/current-keep")
    changed = run_clean(repo, path)
    assert changed.returncode == 0
    assert list_code(changed.stdout) != list_code(text)


def test_missing_corrupt_or_incomplete_pr_never_safe(tmp_path):
    repo = init_pair(tmp_path)
    head = commit_on(repo, "task/merged-safe", "merged\n", "merged")
    main_sha = git(repo, "rev-parse", "main")
    valid = pr(18, "merged", "task/merged-safe", head, main_sha)
    missing = tmp_path / "missing.json"
    before = snap(repo)
    res = run_clean(repo, missing)
    assert res.returncode == 0, res.stderr
    assert "task/merged-safe" in res.stdout
    assert "verdict: SAFE" not in res.stdout
    assert snap(repo) == before
    corrupt = tmp_path / "bad.json"
    corrupt.write_bytes(b"{")
    res = run_clean(repo, corrupt)
    assert res.returncode == 0
    assert "verdict: SAFE" not in res.stdout
    assert snap(repo) == before
    incomplete = tmp_path / "incomplete.json"
    write_prs(incomplete, [valid, {"state": "closed", "branch": "task/other"}])
    res = run_clean(repo, incomplete)
    assert res.returncode == 0
    assert "verdict: SAFE" not in res.stdout
    omitted = tmp_path / "omitted.json"
    write_prs(omitted, {"complete": False, "prs": [valid]})
    res = run_clean(repo, omitted)
    assert res.returncode == 0
    assert "verdict: SAFE" not in res.stdout
    marked = tmp_path / "marked.json"
    write_prs(marked, {"missing_pr": True, "prs": [valid]})
    res = run_clean(repo, marked)
    assert res.returncode == 0
    assert "verdict: SAFE" not in res.stdout
    assert snap(repo) == before


def test_delete_exits_2_and_changes_nothing(tmp_path):
    repo, path = scenario(tmp_path)
    before = snap(repo)
    out = tmp_path / "should-not-exist.txt"
    for extra in (["--delete"], ["--mode", "delete"], ["--mode=delete"], ["--prune"]):
        res = run_clean(repo, path, extra + ["--out", str(out)])
        assert res.returncode == 2
        assert "clean-list:" not in res.stdout
        assert not out.exists()
        assert snap(repo) == before
    res = subprocess.run([sys.executable, str(SCRIPT), "delete"], capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 2
    assert snap(repo) == before


def test_output_outside_repo_and_json(tmp_path):
    repo, path = scenario(tmp_path)
    before = snap(repo)
    out = tmp_path / "nested" / "clean-list.txt"
    res = run_clean(repo, path, ["--out", str(out)])
    assert res.returncode == 0, res.stderr
    data = out.read_bytes()
    assert b"\r" not in data
    assert data.decode("utf-8") == res.stdout
    assert snap(repo) == before
    inside = repo / "inside.txt"
    res = run_clean(repo, path, ["--out", str(inside)])
    assert res.returncode == 2
    assert not inside.exists()
    assert snap(repo) == before
    res = run_clean(repo, path, ["--json"])
    assert res.returncode == 0, res.stderr
    payload = json.loads(res.stdout)
    assert payload["list_code"] == list_code(run_clean(repo, path).stdout)
    verdicts = {item["branch"]: item["verdict"] for item in payload["items"]}
    assert verdicts["task/merged-safe"] == "SAFE"
    assert verdicts["task/dec-ask"] == "ASK"
    assert "DEC-0014" in next(item["reason"] for item in payload["items"] if item["branch"] == "task/dec-ask")
    assert snap(repo) == before


def test_git_helper_blocks_mutations(tmp_path):
    repo = init_pair(tmp_path)
    before = snap(repo)
    for args in (
        ["reset", "--hard"],
        ["branch", "-D", "main"],
        ["worktree", "remove", "x"],
        ["worktree", "prune"],
        ["push"],
        ["gc"],
        ["fetch", "--prune"],
        ["config", "user.name", "nope"],
    ):
        with pytest.raises(RuntimeError):
            run_git(repo, args)
    assert snap(repo) == before
    source = SCRIPT.read_text(encoding="utf-8")
    for banned in ("gh ", "urllib", "requests", "socket.", "worktree remove", "fetch --prune"):
        assert banned not in source
