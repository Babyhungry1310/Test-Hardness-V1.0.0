import json

from tools.branch_names import classify, main

INPUTS = [
    "main",
    "upgrade/1.0.1",
    "lead/cyc-05",
    "task/TK-0001-R1",
    "task/TK-0002-R1",
    "task/TK-0003-R1",
    "task/TK-0004-R1",
    "task/TK-0005-R1",
    "review/CYC-01",
    "review/CYC-02",
    "review/CYC-02-R1",
]

NEAR = [
    "task/TK-12-R1",
    "task/TK-0001",
    "review/CYC-2-R1-a1b2",
    "review/CYC-02-R1-A1B2",
    "review/CYC-02-R1-a1b",
    "lead/Plan_X",
    "task/TK-0001-R1-2",
    "task/TK-0001-R1-copy",
]


def test_each_kind_has_exact_and_near_miss():
    exact = {
        "main": "main",
        "task": "task/TK-0001-R1",
        "lead": "lead/plan-x",
        "review": "review/CYC-02-R1-a1b2",
        "upgrade": "upgrade/1.0.1",
        "legacy-review": "review/CYC-02-R1",
    }
    for kind, name in exact.items():
        assert classify(name) == kind
    for name in NEAR:
        assert classify(name) == "unknown"


def test_new_and_legacy_review():
    assert classify("review/CYC-02-R1-a1b2") == "review"
    assert classify("review/CYC-02-R1") == "legacy-review"
    assert classify("review/CYC-02") == "legacy-review"
    assert classify("review/CYC-01") == "legacy-review"


def test_tool_suffix_is_unknown():
    assert classify("task/TK-0001-R1-2") == "unknown"
    assert classify("task/TK-0001-R1-copy") == "unknown"
    assert classify("upgrade/1.0.1-copy") == "unknown"


def test_input_names_are_classified():
    for name in INPUTS:
        assert classify(name) != "unknown"


def test_cli_exit_codes(capsys):
    assert main(["main", "task/TK-0001-R1"]) == 0
    text = capsys.readouterr().out
    assert "main: main" in text
    assert "task/TK-0001-R1: task" in text
    assert main(["review/CYC-02-R1-a1b2", "task/TK-12-R1"]) == 1
    assert main([]) == 2
    assert main(["--json"]) == 2


def test_json_output(capsys):
    assert main(["--json", "review/CYC-02", "lead/Plan_X"]) == 1
    rows = json.loads(capsys.readouterr().out)
    assert rows == [
        {"name": "review/CYC-02", "kind": "legacy-review"},
        {"name": "lead/Plan_X", "kind": "unknown"},
    ]
