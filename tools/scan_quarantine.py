import argparse
import hashlib
import json
import sys
from pathlib import Path


def compute_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def quarantine(file_path, scan_json_path, quarantine_dir_path):
    src = Path(file_path)
    scan_file = Path(scan_json_path)
    qdir = Path(quarantine_dir_path)

    if not src.is_file():
        return 2, {"ok": False, "error": f"source file not found: {src}"}

    if not scan_file.is_file():
        return 2, {"ok": False, "error": f"scan json not found: {scan_file}"}

    try:
        scan_data = json.loads(scan_file.read_text(encoding="utf-8"))
    except Exception as exc:
        return 2, {"ok": False, "error": f"invalid scan json: {exc}"}

    if "level" not in scan_data or "sha256" not in scan_data:
        return 2, {"ok": False, "error": "scan json missing required fields"}

    level = scan_data["level"]
    expected_hash = scan_data["sha256"]

    if level not in {"ALLOW", "WARN", "QUARANTINE", "BLOCK"}:
        return 2, {"ok": False, "error": f"unknown scan level: {level}"}

    if level in {"ALLOW", "WARN"}:
        return 0, {"ok": True, "action": "none", "level": level, "source": str(src)}

    if level == "BLOCK":
        return 0, {"ok": True, "action": "none", "level": "BLOCK", "source": str(src)}

    if level == "QUARANTINE":
        hash_before = compute_sha256(src)
        if hash_before != expected_hash:
            return 2, {"ok": False, "error": "sha256 mismatch before move"}

        if qdir.is_file():
            return 2, {"ok": False, "error": "quarantine directory is a file"}

        try:
            qdir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            return 2, {"ok": False, "error": f"cannot create quarantine dir: {exc}"}

        dest = qdir / src.name
        if dest.exists():
            return 2, {"ok": False, "error": f"destination already exists: {dest}"}

        try:
            data = src.read_bytes()
            dest.write_bytes(data)
        except OSError as exc:
            if dest.exists():
                try:
                    dest.unlink()
                except OSError:
                    pass
            return 2, {"ok": False, "error": f"failed to copy file: {exc}"}

        hash_after = compute_sha256(dest)
        if hash_after != hash_before or hash_after != expected_hash:
            try:
                dest.unlink()
            except OSError:
                pass
            return 2, {"ok": False, "error": "sha256 mismatch after copy"}

        try:
            src.unlink()
        except OSError as exc:
            return 2, {"ok": False, "error": f"failed to remove original file: {exc}"}

        return 0, {
            "ok": True,
            "action": "quarantined",
            "level": "QUARANTINE",
            "source": str(src),
            "destination": str(dest),
            "sha256": hash_after,
        }

    return 2, {"ok": False, "error": "unhandled condition"}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="scan_quarantine")
    parser.add_argument("file")
    parser.add_argument("scan_json")
    parser.add_argument("quarantine_dir")
    parser.add_argument("--json", action="store_true", dest="json_output")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2

    code, info = quarantine(args.file, args.scan_json, args.quarantine_dir)
    if args.json_output:
        print(json.dumps(info, ensure_ascii=True))
    else:
        if code == 0:
            if info.get("action") == "quarantined":
                print(f"QUARANTINE {info.get('destination')}")
            else:
                print(f"{info.get('level')} {info.get('source')}")
        else:
            sys.stderr.write(f"error: {info.get('error')}\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
