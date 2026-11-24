#!/usr/bin/env python3
"""Đọc usage theo từng lượt gọi từ DB của 9Router (chỉ đọc, thư viện chuẩn).

Nguồn: bảng `usageHistory` trong `<DATA_DIR>/db/data.sqlite`. DATA_DIR mặc định là
`%APPDATA%\\9router` trên Windows, `~/.9router` nơi khác; biến môi trường DATA_DIR ghi đè.
Đọc thẳng file gốc (chế độ chỉ đọc). Không đọc bản chép chỉ có data.sqlite: 9Router dùng
WAL, dòng mới có thể còn nằm trong data.sqlite-wal.
9Router ghi `prompt_tokens` đã GỒM phần cached (canonicalizeUsage), cached nằm riêng
trong cột JSON `tokens`.

Ví dụ (giờ địa phương +07:00, lọc theo model):
    python usage_9router.py --start "2026-11-23T14:00:00+07:00" --end "2026-11-23T14:30:00+07:00" --model grok
    python usage_9router.py --start ... --end ... --format csv --out l11_usage.csv

Mã thoát: 0 có dòng · 66 không có dòng nào trong khoảng · 2 lỗi DB/tham số.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path


def default_db() -> Path:
    """Theo src/lib/dataDir.js của 9Router: Windows = %APPDATA%\\9router, nơi khác = ~/.9router."""
    base = os.environ.get("DATA_DIR")
    if not base or (os.name == "nt" and base.startswith("/")):
        if os.name == "nt":
            base = os.path.join(os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming"), "9router")
        else:
            base = str(Path.home() / ".9router")
    return Path(base) / "db" / "data.sqlite"


def parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError(f"thiếu múi giờ: {value!r} (ví dụ 2026-11-23T14:00:00+07:00)")
    return dt.astimezone(timezone.utc)


def load_rows(db: Path, start: datetime, end: datetime, model: str | None) -> list[dict]:
    if not db.is_file():
        raise FileNotFoundError(f"không thấy DB 9Router: {db}")
    uri = f"file:{db.as_posix()}?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    try:
        cols = {r[1] for r in con.execute("PRAGMA table_info(usageHistory)")}
        if not cols:
            raise RuntimeError("DB không có bảng usageHistory (phiên bản 9Router cũ dùng usage.json?)")
        rows = con.execute(
            "SELECT timestamp, provider, model, promptTokens, completionTokens, tokens, status, endpoint "
            "FROM usageHistory WHERE timestamp >= ? AND timestamp <= ? ORDER BY timestamp",
            (start.strftime("%Y-%m-%dT%H:%M:%S.000Z"), end.strftime("%Y-%m-%dT%H:%M:%S.999Z")),
        ).fetchall()
    finally:
        con.close()
    out = []
    for ts, provider, mdl, p_tok, c_tok, tokens_json, status, endpoint in rows:
        if model and model.lower() not in (mdl or "").lower():
            continue
        try:
            tok = json.loads(tokens_json or "{}")
        except json.JSONDecodeError:
            tok = {}
        cached = tok.get("cached_tokens") or tok.get("cache_read_input_tokens") or 0
        if not cached and isinstance(tok.get("prompt_tokens_details"), dict):
            cached = tok["prompt_tokens_details"].get("cached_tokens") or 0
        local = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
        out.append({
            "time_local": local.isoformat(timespec="seconds"),
            "provider": provider,
            "model": mdl,
            "prompt_tokens": p_tok or tok.get("prompt_tokens") or 0,
            "cached_tokens": cached,
            "completion_tokens": c_tok or tok.get("completion_tokens") or 0,
            "status": status,
            "endpoint": endpoint,
        })
    return out


def render(rows: list[dict], fmt: str) -> str:
    fields = ["time_local", "provider", "model", "prompt_tokens", "cached_tokens",
              "completion_tokens", "status", "endpoint"]
    if fmt == "json":
        return json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    if fmt == "csv":
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
        return buf.getvalue()
    lines = ["| " + " | ".join(fields) + " |", "|" + " --- |" * len(fields)]
    lines += ["| " + " | ".join(str(r[f]) for f in fields) + " |" for r in rows]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Usage từng lượt gọi từ DB 9Router (chỉ đọc).")
    ap.add_argument("--db", type=Path, default=default_db())
    ap.add_argument("--start", required=True, help="ISO 8601 có múi giờ")
    ap.add_argument("--end", required=True, help="ISO 8601 có múi giờ")
    ap.add_argument("--model", help="lọc model chứa chuỗi này (không phân biệt hoa thường)")
    ap.add_argument("--format", choices=["md", "csv", "json"], default="md")
    ap.add_argument("--out", type=Path, help="ghi ra file và in sha256")
    args = ap.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    try:
        rows = load_rows(args.db, parse_time(args.start), parse_time(args.end), args.model)
    except (ValueError, OSError, RuntimeError, sqlite3.Error) as exc:
        print(f"usage_9router: {exc}", file=sys.stderr)
        return 2
    text = render(rows, args.format)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"{len(rows)} dòng → {args.out} · sha256 {hashlib.sha256(text.encode('utf-8')).hexdigest()}")
    else:
        sys.stdout.write(text)
        print(f"{len(rows)} dòng", file=sys.stderr)
    return 0 if rows else 66


if __name__ == "__main__":
    sys.exit(main())
