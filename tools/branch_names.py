import argparse
import json
import re
import sys

KINDS = (
    "main",
    "task",
    "lead"
    "review",
    "upgrade"
    "legacy-review"
    "unknown"
)

TASK = re.compile(r"task/TK-\d{4}-R\d+\Z")
LEAD = re.compile(r"lead/[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REVIEW = re.compile(r"review/CYC-\d{2}-R\d+-[a-z0-9]{4}\Z")
UPGRADE = re.compile(r"upgrade/\d+(?:\.\d+)*\Z")
LEGACY_REVIEW = re.compile(r"review/CYC-\d{2}(?:-R\d+)?\Z")


def classify(name):
    if not isinstance(name, str) or name == "" or name != name.strip() or "\\" in name:
        return "unknown"
    if name == "main":
        return "main"
    if TASK.fullmatch(name):
        return "task"
    if LEAD.fullmatch(name):
        return "lead"
    if REVIEW.fullmatch(name):
        return "review"
    if UPGRADE.fullmatch(name):
        return "upgrade"
    if LEGACY_REVIEW.fullmatch(name):
        return "legacy-review"
    return "unknown"


def classify_many(names):
    return [{ "name": name, "kind": classify(name) } for name in names]


def render_text(rows):
    for row in rows:
        print(row["name"] + ": " + row["kind"])


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="*")
    parser.add_argument("--json", action="store_true", dest="json_output")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    if not args.names:
        return 2
    rows = classify_many(args.names)
    if args.json_output:
        print(json.dumps(rows, ensure_ascii=False))
    else:
        render_text(rows)
    if any(row["kind"] == "unknown" for row in rows):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
