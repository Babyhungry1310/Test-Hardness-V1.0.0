#!/usr/bin/env python3
"""Lệnh verify chuẩn cho task tài liệu, sổ, DEC, STATE, kế hoạch.

Thay cho `python -m pytest tools/tests` (lệnh đó kiểm công cụ, không kiểm tài liệu).
Mỗi điều kiện trong done_when ánh xạ sang một cờ dưới đây, nên lệnh verify tự mô tả
được điều nó chứng minh. Chỉ dùng thư viện chuẩn; cần `git` cho --append-only-vs.

Ví dụ (một dòng verify trong thẻ task):

    python tools/verify_doc_artifact.py 06_sources/SRC-0003.md \
        --contains "Phiên bản: P6" --heading "Bảng truy vết" \
        --regex "^\\| TK-0057 \\|" --max-words 6000

    python tools/verify_doc_artifact.py 02_decisions/DECISIONS.md --append-only-vs origin/main

    python tools/verify_doc_artifact.py 05_memory/upstream/00_tong_quan_upstream.md \
        --sha256 05_memory/upstream/00_tong_quan_upstream.md=<64 hex>

Kiểm mặc định (tắt bằng cờ --no-*):
  - file tồn tại, đọc được UTF-8, không rỗng
  - không chứa bí mật hay đường dẫn máy cá nhân (repo public)
  - link Markdown tương đối trỏ tới file có thật
  - bảng Markdown có số cột đồng đều

Mã thoát: 0 đạt · 1 vi phạm · 2 lỗi dùng lệnh / git · 66 không có phép kiểm nào để chạy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

EXIT_OK, EXIT_FAIL, EXIT_USAGE, EXIT_NO_INPUT = 0, 1, 2, 66

DEFAULT_FORBID = {
    "PRIVATE_KEY": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "GITHUB_TOKEN": r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}\b",
    "API_KEY": r"\bsk-[A-Za-z0-9_-]{20,}\b|\bAKIA[0-9A-Z]{16}\b|\bxox[abp]-[A-Za-z0-9-]{10,}\b",
    "WINDOWS_USER_PATH": r"\b[A-Za-z]:\\\\?Users\\\\?[^\\\s<>\"']+",
    "UNIX_HOME_PATH": r"(?<![\w.])/(?:home|Users)/[A-Za-z0-9._-]+/",
}

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


@dataclass
class Finding:
    path: str
    line: int
    rule: str
    message: str

    def text(self) -> str:
        loc = f"{self.path}:{self.line}" if self.line else self.path
        return f"{loc}: {self.rule}: {self.message}"


def iter_prose_lines(lines):
    """(số dòng, nội dung) của các dòng nằm ngoài khối mã rào."""
    fence = None
    for no, line in enumerate(lines, 1):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = marker[0]
                continue
            if marker[0] == fence:
                fence = None
                continue
        if fence is None:
            yield no, line


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    cells, cur, in_code = [], [], False
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body) and body[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
        i += 1
    cells.append("".join(cur))
    return cells


def check_tables(path: str, lines) -> list[Finding]:
    out, header_cols, prev_blank = [], None, True
    for no, line in iter_prose_lines(lines):
        is_row = line.lstrip().startswith("|")
        if not is_row:
            header_cols, prev_blank = None, not line.strip()
            continue
        cols = len(split_row(line))
        if header_cols is None:
            header_cols = cols
        elif cols != header_cols:
            out.append(Finding(path, no, "TABLE_COLUMNS", f"{cols} cột, tiêu đề bảng có {header_cols}"))
    return out


def check_links(path: Path, lines) -> list[Finding]:
    out = []
    for no, line in iter_prose_lines(lines):
        for target in LINK_RE.findall(line):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            if not (path.parent / file_part).exists():
                out.append(Finding(str(path), no, "BROKEN_LINK", f"link tới {file_part!r} không tồn tại"))
    return out


def git_removed_lines(path: str, base: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--no-color", "--unified=0", base, "--", path],
        capture_output=True, text=True, encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git diff {base} -- {path} lỗi: {proc.stderr.strip()}")
    return [ln[1:] for ln in proc.stdout.splitlines() if ln.startswith("-") and not ln.startswith("---")]


def verify(args) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    checks_run = 0
    forbid = {} if args.no_default_forbid else dict(DEFAULT_FORBID)
    for i, pat in enumerate(args.forbid or []):
        forbid[f"FORBID_{i + 1}"] = pat
    sha_expect = {}
    for item in args.sha256 or []:
        p, _, h = item.partition("=")
        if not re.fullmatch(r"[0-9a-fA-F]{64}", h):
            raise ValueError(f"--sha256 cần dạng path=<64 hex>: {item!r}")
        sha_expect[p] = h.lower()
    pairs = []
    for item in args.same_as or []:
        target, _, source = item.partition("=")
        if not target or not source:
            raise ValueError(f"--same-as cần dạng đích=nguồn: {item!r}")
        pairs.append((target, source))

    for raw in args.paths:
        path = Path(raw)
        checks_run += 1
        if not path.is_file():
            findings.append(Finding(raw, 0, "MISSING_FILE", "file không tồn tại"))
            continue
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            findings.append(Finding(raw, 0, "BOM", "file có UTF-8 BOM"))
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            findings.append(Finding(raw, 0, "ENCODING", f"không phải UTF-8: {exc}"))
            continue
        if not text.strip():
            findings.append(Finding(raw, 0, "EMPTY_FILE", "file rỗng"))
        if re.search("[\\u00c3\\u00c2][\\u0080-\\u00bf\\u00a0-\\u00bf]|\\u00e2[\\u0080-\\u00bf\\u20ac\\u2020\\u201a][\\u0080-\\u00bf\\u2122\\u2019\\u201c\\u201d]", text):
            findings.append(Finding(raw, 0, "MOJIBAKE", "nội dung có dấu hiệu sai mã hóa"))
        lines = text.splitlines()

        for needle in args.contains or []:
            checks_run += 1
            if needle not in text:
                findings.append(Finding(raw, 0, "CONTAINS", f"thiếu chuỗi {needle!r}"))
        for pat in args.regex or []:
            checks_run += 1
            if not re.search(pat, text.replace("\r\n", "\n"), re.M):
                findings.append(Finding(raw, 0, "REGEX", f"không có dòng khớp {pat!r}"))
        if args.heading:
            checks_run += 1
            heads = {HEADING_RE.match(ln).group(2).strip() for _, ln in iter_prose_lines(lines) if HEADING_RE.match(ln)}
            for h in args.heading:
                if not any(x == h or x.endswith(" " + h) or x.startswith(h) for x in heads):
                    findings.append(Finding(raw, 0, "HEADING", f"thiếu tiêu đề {h!r}"))
        if args.max_words is not None:
            checks_run += 1
            words = len(text.split())
            if words > args.max_words:
                findings.append(Finding(raw, 0, "MAX_WORDS", f"{words} từ > trần {args.max_words}"))
        if forbid:
            checks_run += 1
            for no, line in enumerate(lines, 1):
                for name, pat in forbid.items():
                    if re.search(pat, line):
                        findings.append(Finding(raw, no, f"FORBIDDEN:{name}", "nội dung cấm trong repo public"))
        if not args.no_links and path.suffix.lower() == ".md":
            checks_run += 1
            findings += check_links(path, lines)
        if not args.no_tables and path.suffix.lower() == ".md":
            checks_run += 1
            findings += check_tables(raw, lines)
        if raw in sha_expect:
            checks_run += 1
            got = hashlib.sha256(data).hexdigest()
            if got != sha_expect[raw]:
                findings.append(Finding(raw, 0, "SHA256", f"hash {got} khác giá trị khai {sha_expect[raw]}"))
        if args.append_only_vs:
            checks_run += 1
            removed = git_removed_lines(raw, args.append_only_vs)
            for ln in removed[:20]:
                findings.append(Finding(raw, 0, "APPEND_ONLY", f"dòng bị xóa/sửa so với {args.append_only_vs}: {ln[:120]!r}"))
            if len(removed) > 20:
                findings.append(Finding(raw, 0, "APPEND_ONLY", f"... và {len(removed) - 20} dòng khác"))

    for target, source in pairs:
        checks_run += 1
        t, s = Path(target), Path(source)
        if not t.is_file() or not s.is_file():
            findings.append(Finding(target, 0, "SAME_AS", f"thiếu file để so: {target} hoặc {source}"))
        elif hashlib.sha256(t.read_bytes()).digest() != hashlib.sha256(s.read_bytes()).digest():
            findings.append(Finding(target, 0, "SAME_AS", f"nội dung khác {source}"))
    for p in sha_expect:
        if p not in args.paths:
            raise ValueError(f"--sha256 cho {p!r} nhưng path này không nằm trong danh sách kiểm")
    return findings, checks_run


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Verify chuẩn cho task tài liệu / sổ / DEC / STATE.")
    ap.add_argument("paths", nargs="*", help="file cần kiểm (đường dẫn tương đối từ gốc repo)")
    ap.add_argument("--contains", action="append", help="chuỗi bắt buộc có (lặp được)")
    ap.add_argument("--regex", action="append", help="regex (đa dòng) bắt buộc khớp ít nhất một lần")
    ap.add_argument("--heading", action="append", help="tiêu đề Markdown bắt buộc có")
    ap.add_argument("--max-words", type=int, help="trần số từ (ví dụ LEAD.md ≤ 1300)")
    ap.add_argument("--forbid", action="append", help="regex cấm, thêm vào bộ mặc định")
    ap.add_argument("--sha256", action="append", help="path=<sha256> phải khớp")
    ap.add_argument("--same-as", action="append", help="đích=nguồn: hai file phải giống hệt (task đồng bộ)")
    ap.add_argument("--append-only-vs", metavar="GIT_REF", help="sổ chỉ thêm dòng so với ref (vd origin/main)")
    ap.add_argument("--no-default-forbid", action="store_true")
    ap.add_argument("--no-links", action="store_true")
    ap.add_argument("--no-tables", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    if not args.paths and not args.same_as:
        msg = "không có file nào để kiểm"
        print(json.dumps({"status": "NO_INPUT", "message": msg}) if args.json else f"NO_INPUT: {msg}")
        return EXIT_NO_INPUT
    try:
        findings, checks_run = verify(args)
    except (ValueError, re.error, RuntimeError, OSError) as exc:
        print(f"verify_doc_artifact: {exc}", file=sys.stderr)
        return EXIT_USAGE

    status = "FAIL" if findings else "PASS"
    if args.json:
        print(json.dumps({"status": status, "checks": checks_run,
                          "findings": [f.__dict__ for f in findings]}, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f.text())
        print(f"{status}: {len(args.paths)} file, {checks_run} phép kiểm, {len(findings)} vi phạm")
    return EXIT_FAIL if findings else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
