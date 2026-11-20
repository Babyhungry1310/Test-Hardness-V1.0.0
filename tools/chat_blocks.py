import argparse
import json
import re
import sys
from pathlib import Path

HEADERS = {"SUMMARY", "QUESTION", "CONFIRM", "RESULT", "MERGE", "REVIEW"}
ENDING = {"CONFIRM", "RESULT", "MERGE", "REVIEW"}
GROUPS = {
    "SUMMARY": [("did",), ("changed",), ("decide",), ("limits",), ("evidence",)],
    "QUESTION": [("q",), ("a", "b"), ("recommend",)],
    "CONFIRM": [("understanding",), ("scope",), ("will_not_do",), ("result",)],
    "RESULT": [("task", "run", "outcome"), ("pr",), ("done",), ("loops", "last"), ("deviations",), ("escalate",)],
    "MERGE": [("pr", "type"), ("checks",), ("done", "tests"), ("deviations",), ("protected",), ("order",)],
    "REVIEW": [("cycle", "verdict"), ("tasks", "pass", "fail"), ("record",)],
}
FENCE = re.compile(r"^\s*(```|~~~)")
KEY = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
CELL_SEP = re.compile(r"^:?-{3,}:?$")


def issue(code, message):
    return {"code": code, "message": message}


def add_issue(found, code, message):
    if not any(item["code"] == code for item in found):
        found.append(issue(code, message))


def text_lines(text):
    if text.startswith("\ufeff"):
        text = text[1:]
    raw = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if raw and raw[-1] == "":
        raw.pop()
    return raw


def code_flags(lines):
    flags = []
    active = False
    for line in lines:
        if FENCE.match(line):
            flags.append(True)
            active = not active
        else:
            flags.append(active)
    return flags


def pipe_cells(line):
    stripped = line.strip()
    if "|" not in stripped:
        return []
    return [part.strip() for part in stripped.strip("|").split("|")]


def is_table(line):
    cells = pipe_cells(line)
    if len(cells) < 2:
        return False
    if line.strip().startswith("|"):
        return True
    return all(CELL_SEP.fullmatch(cell) for cell in cells)


def parse_keys(line):
    found = []
    for part in re.split(" \u00b7 (?=[A-Za-z_]+:)", line.strip()):
        match = KEY.match(part.strip())
        if not match:
            return None
        found.append((match.group(1), match.group(2).strip()))
    return found


def parse_blocks(lines, flags):
    blocks = []
    lead = False
    current = None
    for index, line in enumerate(lines):
        name = line.strip()
        if not flags[index] and name in HEADERS:
            current = {"name": name, "start": index, "lines": [], "flags": []}
            blocks.append(current)
            continue
        if current is None:
            if line.strip() and not flags[index]:
                lead = True
            continue
        current["lines"].append(line)
        current["flags"].append(flags[index])
    return blocks, lead


def section_count(lines, flags, start):
    end = start + 1
    while end < len(lines) and not (not flags[end] and lines[end].strip() in HEADERS):
        end += 1
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    return end - start


def key_info(block):
    groups = []
    values = {}
    for line, flag in zip(block["lines"], block["flags"]):
        if flag or not line.strip():
            continue
        parsed = parse_keys(line)
        if not parsed:
            continue
        groups.append(tuple(key for key, _value in parsed))
        for key, value in parsed:
            values[key] = value
    return groups, values


def content_after_keys(block):
    need = len(GROUPS[block["name"]])
    seen = 0
    for line, flag in zip(block["lines"], block["flags"]):
        if not line.strip():
            continue
        parsed = None if flag else parse_keys(line)
        if parsed and seen < need:
            seen += 1
            continue
        return True
    return False


def check_text(text):
    lines = text_lines(text)
    flags = code_flags(lines)
    blocks, lead = parse_blocks(lines, flags)
    found = []
    if any(is_table(line) for line, flag in zip(lines, flags) if not flag):
        add_issue(found, "table", "markdown table outside code block")
    if lead:
        add_issue(found, "lead_in", "lead-in before SUMMARY")
    names = [block["name"] for block in blocks]
    endings = [block for block in blocks if block["name"] in ENDING]
    questions = [block for block in blocks if block["name"] == "QUESTION"]
    summaries = [block for block in blocks if block["name"] == "SUMMARY"]
    if not endings:
        add_issue(found, "missing_end", "missing ending block")
    if len(endings) > 1:
        label = "two ending blocks" if len(endings) == 2 else f"{len(endings)} ending blocks"
        add_issue(found, "multiple_end", label)
    if len(questions) > 5:
        add_issue(found, "too_many_questions", f"{len(questions)} QUESTION blocks")
    if summaries and (len(summaries) != 1 or names[0] != "SUMMARY"):
        add_issue(found, "block_order", "SUMMARY is not first")
    question_count = len(questions)
    if endings:
        first = next(index for index, name in enumerate(names) if name in ENDING)
        question_count = sum(1 for name in names[:first] if name == "QUESTION")
        if any(name not in ENDING for name in names[first + 1:]):
            add_issue(found, "after_end", "content after ending block")
        if content_after_keys(endings[0]):
            add_issue(found, "after_end", "content after ending block")
    for block in blocks:
        expected = GROUPS[block["name"]]
        actual, values = key_info(block)
        missing = [key for group in expected for key in group if key not in values]
        if missing:
            add_issue(found, "missing_key", "missing required key: " + ", ".join(missing))
            continue
        if actual != expected:
            add_issue(found, "key_order", "wrong key order")
        if not summaries or block is not summaries[0]:
            continue
        count = section_count(lines, flags, block["start"])
        if count > 12:
            add_issue(found, "summary_lines", f"SUMMARY has {count} lines")
        decide = values.get("decide")
        if decide is None or not decide.isdigit() or int(decide) != question_count:
            add_issue(found, "decide_mismatch", "decide does not match QUESTION count")
    return (0 if not found else 1), {"ok": not found, "issues": found}


def emit(data, as_json):
    if as_json:
        print(json.dumps(data, ensure_ascii=False))
        return
    if data.get("error"):
        print(data["error"], file=sys.stderr)
    for item in data.get("issues", []):
        print(f"{item['code']}: {item['message']}")
    if data.get("ok"):
        print("PASS")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="chat_blocks")
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true", dest="json_output")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    try:
        text = Path(args.path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        emit({"ok": False, "error": str(exc), "issues": []}, args.json_output)
        return 2
    code, data = check_text(text)
    emit(data, args.json_output)
    return code


if __name__ == "__main__":
    sys.exit(main())
