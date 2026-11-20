import json
import subprocess
import sys
from pathlib import Path

from tools.chat_blocks import check_text, main

ROOT = Path(__file__).resolve().parents[2]
DOT = " \u00b7 "
DASH = "\u2013"


def summary(decide="0"):
    return [
        "SUMMARY",
        "did: checked final message blocks",
        "changed: 2" + DOT + "tools/chat_blocks.py",
        f"decide: {decide}",
        "limits: none",
        "evidence: none",
    ]


def question(index=1):
    return [
        "QUESTION",
        f"q: choose layout {index} for the final message",
        "a: vertical list" + DOT + "b: wide table",
        "recommend: a",
    ]


def confirm():
    return [
        "CONFIRM",
        "understanding: check final chat blocks",
        "scope: tools/chat_blocks.py and tools/tests/test_chat_blocks.py",
        "will_not_do: edit src tests data pytest.ini harness",
        "result: checker reads one text file and pytest verifies it",
    ]


def result():
    return [
        "RESULT",
        "task: TK-0012" + DOT + "run: R1" + DOT + "outcome: DONE",
        "pr: https://example.invalid/pull/12",
        "done: 4/4",
        "loops: L01" + DASH + "L01" + DOT + "last: PASS",
        "deviations: 0",
        "escalate: no",
    ]


def merge():
    return [
        "MERGE",
        "pr: https://example.invalid/pull/12" + DOT + "type: run",
        "checks: C1" + DASH + "C14 PASS @ main f310d9d",
        "done: 4/4" + DOT + "tests: PASS",
        "deviations: 0",
        "protected: none",
        "order: none",
    ]


def review():
    return [
        "REVIEW",
        "cycle: CYC-05" + DOT + "verdict: PASS",
        "tasks: 4" + DOT + "pass: 4" + DOT + "fail: 0",
        "record: RVW-CYC-05",
    ]


ENDINGS = {
    "CONFIRM": confirm,
    "RESULT": result,
    "MERGE": merge,
    "REVIEW": review,
}


def text_of(*groups):
    lines = []
    for group in groups:
        lines.extend(group)
    return "\n".join(lines) + "\n"


def codes(text):
    _code, data = check_text(text)
    return [item["code"] for item in data["issues"]]


def issues(text):
    _code, data = check_text(text)
    return data["issues"]


def write_message(tmp_path, text):
    path = tmp_path / "message.txt"
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def test_valid_endings_with_and_without_summary():
    for builder in ENDINGS.values():
        assert codes(text_of(summary(), builder())) == []
        assert codes(text_of(builder())) == []


def test_questions_within_limit_match_decide():
    assert codes(text_of(summary("2"), question(1), question(2), result())) == []
    five = [summary("5")]
    five.extend(question(index) for index in range(1, 6))
    five.append(result())
    assert codes(text_of(*five)) == []
    assert codes(text_of(question(), result())) == []


def test_lead_in_before_summary():
    text = "See the final message.\n" + text_of(summary(), result())
    found = issues(text)
    assert [item["code"] for item in found] == ["lead_in"]
    assert "SUMMARY" in found[0]["message"]


def test_content_after_ending_block():
    text = text_of(summary(), result()) + "Thanks for reviewing.\n"
    found = issues(text)
    assert [item["code"] for item in found] == ["after_end"]
    assert "after ending block" in found[0]["message"]


def test_two_ending_blocks():
    found = issues(text_of(confirm(), result()))
    assert [item["code"] for item in found] == ["multiple_end"]
    assert "two ending blocks" in found[0]["message"]


def test_missing_ending_block():
    found = issues(text_of(summary("1"), question()))
    assert [item["code"] for item in found] == ["missing_end"]
    assert "missing ending block" in found[0]["message"]


def test_six_question_blocks():
    groups = [summary("6")]
    groups.extend(question(index) for index in range(1, 7))
    groups.append(result())
    found = issues(text_of(*groups))
    assert [item["code"] for item in found] == ["too_many_questions"]
    assert "6 QUESTION blocks" in found[0]["message"]


def test_summary_13_lines():
    lines = summary()
    while len(lines) < 13:
        lines.append(f"extra {len(lines)}")
    assert len(lines) == 13
    found = issues(text_of(lines, result()))
    assert [item["code"] for item in found] == ["summary_lines"]
    assert "13" in found[0]["message"]


def test_decide_does_not_match_question_count():
    found = issues(text_of(summary("1"), result()))
    assert [item["code"] for item in found] == ["decide_mismatch"]
    assert "decide" in found[0]["message"]


def test_wrong_key_order():
    bad = result()
    bad[1] = "run: R1" + DOT + "task: TK-0012" + DOT + "outcome: DONE"
    found = issues(text_of(bad))
    assert [item["code"] for item in found] == ["key_order"]
    assert "order" in found[0]["message"]


def test_missing_required_key():
    bad = [line for line in result() if not line.startswith("escalate:")]
    found = issues(text_of(summary(), bad))
    assert [item["code"] for item in found] == ["missing_key"]
    assert "escalate" in found[0]["message"]


def test_table_outside_code_is_reported():
    table = ["| left | right |", "| --- | --- |", "| a | b |"]
    found = issues(text_of(summary(), table, result()))
    assert [item["code"] for item in found] == ["table"]
    assert "table" in found[0]["message"]


def test_table_inside_code_is_not_reported():
    fenced = [
        "SUMMARY",
        "did: checked final message blocks",
        "```text",
        "| left | right |",
        "| --- | --- |",
        "| a | b |",
        "python tools/chat_blocks.py message.txt",
        "```",
        "changed: 2" + DOT + "tools/chat_blocks.py",
        "decide: 0",
        "limits: none",
        "evidence: none",
    ]
    assert len(fenced) == 12
    assert codes(text_of(fenced, result())) == []


def test_cli_json_and_text(tmp_path, capsys):
    path = write_message(tmp_path, text_of(summary(), result()))
    assert main([str(path), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data == {"ok": True, "issues": []}
    failed = write_message(tmp_path, text_of(result()) + "extra\n")
    assert main([str(failed)]) == 1
    assert "after_end:" in capsys.readouterr().out


def test_cli_usage_exit_2(tmp_path, capsys):
    assert main([]) == 2
    capsys.readouterr()
    missing = tmp_path / "missing.txt"
    assert main([str(missing), "--json"]) == 2
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is False
    assert data["issues"] == []


def test_script_reads_only_named_file(tmp_path):
    path = write_message(tmp_path, text_of(review()))
    good = subprocess.run(
        [sys.executable, "tools/chat_blocks.py", str(path), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert good.returncode == 0
    assert json.loads(good.stdout)["ok"] is True
    usage = subprocess.run(
        [sys.executable, "tools/chat_blocks.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert usage.returncode == 2
