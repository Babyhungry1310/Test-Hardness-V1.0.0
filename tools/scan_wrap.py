import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

CLOSING_TAG = b"</EXTERNAL_DATA>"


def escape_attr(val):
    s = str(val) if not isinstance(val, str) else val
    return s.replace("&", "&amp;").replace('"', "&quot;").replace(">", "&gt;").replace("<", "&lt;")


def wrap_bytes(raw, source="", scan="ALLOW", ruleset="1.0.0"):
    raw = raw.encode("utf-8") if isinstance(raw, str) else raw
    digest = hashlib.sha256(raw).hexdigest()
    count = raw.count(CLOSING_TAG)
    s_esc, sc_esc, r_esc = escape_attr(source), escape_attr(scan), escape_attr(ruleset)
    open_tag = f'<EXTERNAL_DATA source="{s_esc}" sha256="{digest}" scan="{sc_esc}" ruleset="{r_esc}" closing_tag_count="{count}">\n'.encode("utf-8")
    return open_tag + raw + b"\n</EXTERNAL_DATA>\n"


def wrap(content, source="", scan="ALLOW", ruleset="1.0.0"):
    is_str = isinstance(content, str)
    raw = content.encode("utf-8") if is_str else content
    wrapped = wrap_bytes(raw, source=source, scan=scan, ruleset=ruleset)
    return wrapped.decode("utf-8") if is_str else wrapped


def unwrap_bytes(wrapped):
    wrapped = wrapped.encode("utf-8") if isinstance(wrapped, str) else wrapped
    tag_end = wrapped.find(b">\n")
    body_start = tag_end + 2 if tag_end != -1 else wrapped.find(b">") + 1
    if body_start <= 0:
        raise ValueError("missing opening tag")
    close_pos = wrapped.rfind(CLOSING_TAG)
    if close_pos == -1 or close_pos < body_start:
        raise ValueError("missing closing tag")
    body_end = close_pos - 1 if (close_pos > body_start and wrapped[close_pos - 1 : close_pos] == b"\n") else close_pos
    header = wrapped[: body_start].decode("utf-8", errors="replace")
    attrs = {}
    for match in re.finditer(r'([A-Za-z0-9_:-]+)="([^"]*)"', header):
        attrs[match.group(1)] = (
            match.group(2)
            .replace("&quot;", '"')
            .replace("&gt;", ">")
            .replace("&lt;", "<")
            .replace("&amp;", "&")
        )
    return attrs, wrapped[body_start:body_end]


def unwrap(wrapped):
    is_str = isinstance(wrapped, str)
    attrs, body = unwrap_bytes(wrapped.encode("utf-8") if is_str else wrapped)
    return attrs, body.decode("utf-8") if is_str else body


def main(argv=None):
    parser = argparse.ArgumentParser(prog="scan_wrap")
    parser.add_argument("file", nargs="?", default=None)
    parser.add_argument("--source")
    parser.add_argument("--scan", default="ALLOW")
    parser.add_argument("--ruleset", default="1.0.0")
    parser.add_argument("--scan-json", dest="scan_json")
    parser.add_argument("--out")
    parser.add_argument("--json", action="store_true", dest="json_output")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2

    source, scan, ruleset = args.source, args.scan, args.ruleset
    if args.scan_json:
        s_path = Path(args.scan_json)
        if not s_path.is_file():
            return 2
        try:
            s_data = json.loads(s_path.read_text(encoding="utf-8"))
        except Exception:
            return 2
        scan = s_data.get("level", scan)
        ruleset = s_data.get("ruleset", ruleset)

    if args.file and args.file != "-":
        p = Path(args.file)
        if not p.is_file():
            return 2
        try:
            raw = p.read_bytes()
        except OSError:
            return 2
        source = str(p) if source is None else source
    else:
        if sys.stdin.isatty() and not args.file:
            return 2
        try:
            raw = sys.stdin.buffer.read()
        except OSError:
            return 2
        source = "stdin" if source is None else source

    wrapped = wrap_bytes(raw, source=source, scan=scan, ruleset=ruleset)
    if args.out:
        try:
            Path(args.out).write_bytes(wrapped)
        except OSError:
            return 2
    elif args.json_output:
        digest = hashlib.sha256(raw).hexdigest()
        info = {
            "ok": True,
            "source": source,
            "sha256": digest,
            "scan": scan,
            "ruleset": ruleset,
            "closing_tag_count": raw.count(CLOSING_TAG),
            "bytes": len(raw),
            "wrapped_bytes": len(wrapped),
        }
        print(json.dumps(info, ensure_ascii=True))
    else:
        sys.stdout.buffer.write(wrapped)
        sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
