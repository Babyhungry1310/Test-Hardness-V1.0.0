import json
import os
from pathlib import Path

from tools.batch_check import check_plan, main, normalize_scope, scopes_overlap

PLAN = """---
schema: 1
id: PLAN
---
## Status
- 2026-11-19 | ACTIVE | version: 1
<!-- ANCHOR: CYC_03 -->
## CYC-03
- TK-0101 | left | depends: none | assignee: W1
- TK-0102 | right | depends: none | assignee: W2
<!-- END: CYC_03 -->
<!-- ANCHOR: CYC_03_BATCHES -->
## CYC-03 batches
- B1 | tasks: TK-0101, TK-0102 | after: none
<!-- END: CYC_03_BATCHES -->
<!-- ANCHOR: CYC_01 -->
## CYC-01
- TK-0001 | old | depends: none | assignee: W1
<!-- END: CYC_01 -->
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def task_text(task_id, scope, depends=None, inputs=None, read_also=None):
    depends = depends or []
    inputs = inputs or []
    read_also = read_also or []
    lines = [
        "---",
        "schema: 1",
        "id: " + task_id,
        "write_scope: " + json.dumps(scope),
        "depends_on: " + json.dumps(depends),
        "inputs: " + json.dumps(inputs, ensure_ascii=False),
        "read_also: " + json.dumps(read_also),
        "---",
        "",
    ]
    return "\n".join(lines)


def fixture(tmp_path, plan, tasks):
    plan_path = write(tmp_path / "PLAN.md", plan)
    tasks_dir = tmp_path / "tasks" / "CYC-03"
    for task_id, fields in tasks.items():
        write(tasks_dir / (task_id + ".md"), task_text(task_id, **fields))
    return plan_path, tmp_path / "tasks"


def rules(data):
    return [item["rule"] for item in data["violations"]]


def test_normalize_slashes_dot_and_trailing_slash():
    assert normalize_scope(".\\tools\\scan.py") == "tools/scan.py"
    assert normalize_scope("./tools/scan.py") == "tools/scan.py"
    assert normalize_scope("tools/hooks/") == "tools/hooks/"
    assert scopes_overlap("tools/", "tools/scan.py")
    assert scopes_overlap("tools/hooks/", "tools/")
    assert not scopes_overlap("tools/scan.py", "tools/scan_wrap.py")
    assert not scopes_overlap("tools/hooks/", "tools/hooks_extra.py")


def test_same_path_and_spelling_variants(tmp_path):
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/scan.py"]},
        "TK-0102": {"scope": [".\\tools\\scan.py"]},
    })
    data = check_plan(plan, tasks, "CYC-03")
    assert 1 in rules(data)
    assert any("tools/scan.py" in item.get("paths", []) for item in data["violations"])


def test_directory_covers_file_both_ways(tmp_path):
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/"]},
        "TK-0102": {"scope": ["tools/scan.py"]},
    })
    assert 1 in rules(check_plan(plan, tasks, "CYC-03"))
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/scan.py"]},
        "TK-0102": {"scope": ["tools/"]},
    })
    assert 1 in rules(check_plan(plan, tasks, "CYC-03"))
    nested = PLAN.replace("TK-0102 | right", "TK-0102 | right").replace(
        "- B1 | tasks: TK-0101, TK-0102 | after: none",
        "- B1 | tasks: TK-0101, TK-0102 | after: none",
    )
    plan, tasks = fixture(tmp_path, nested, {
        "TK-0101": {"scope": ["tools/hooks/"]},
        "TK-0102": {"scope": ["tools/"]},
    })
    assert 1 in rules(check_plan(plan, tasks, "CYC-03"))


def test_prefix_lookalikes_are_not_overlaps(tmp_path):
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/scan.py", "tools/hooks/"]},
        "TK-0102": {"scope": ["tools/scan_wrap.py", "tools/hooks_extra.py"]},
    })
    data = check_plan(plan, tasks, "CYC-03")
    assert data["ok"]
    assert data["violations"] == []


def test_same_batch_depends_inputs_and_read_also(tmp_path):
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/a.py"], "depends": ["TK-0102"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    assert any(item["rule"] == 2 and "depends_on" in item["message"] for item in check_plan(plan, tasks, "CYC-03")["violations"])
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/a.py"], "inputs": ["needs TK-0102 output"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    assert any(item["rule"] == 2 and "inputs" in item["message"] and "TK-0102" in item["paths"] for item in check_plan(plan, tasks, "CYC-03")["violations"])
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/a.py"], "inputs": ["tools/b.py is produced elsewhere"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    assert any(item["rule"] == 2 and "tools/b.py" in item.get("paths", []) for item in check_plan(plan, tasks, "CYC-03")["violations"])
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/left.py"], "read_also": ["tools/right.py#API"]},
        "TK-0102": {"scope": ["tools/right.py"]},
    })
    assert any(item["rule"] == 2 and "read_also" in item["message"] for item in check_plan(plan, tasks, "CYC-03")["violations"])


def test_shared_file_owned_by_two_tasks(tmp_path):
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["pytest.ini", "tools/a.py"]},
        "TK-0102": {"scope": ["tools/requirements.txt"]},
    })
    data = check_plan(plan, tasks, "CYC-03")
    assert data["ok"]
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["pytest.ini"]},
        "TK-0102": {"scope": ["pytest.ini"]},
    })
    assert any(item["rule"] == 3 and "pytest.ini" in item["paths"] for item in check_plan(plan, tasks, "CYC-03")["violations"])
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/requirements.txt"]},
        "TK-0102": {"scope": ["./tools/requirements.txt"]},
    })
    assert any(item["rule"] == 3 for item in check_plan(plan, tasks, "CYC-03")["violations"])


def test_membership_missing_after_and_order(tmp_path):
    missing = PLAN.replace("- B1 | tasks: TK-0101, TK-0102 | after: none", "- B1 | tasks: TK-0101 | after: none")
    plan, tasks = fixture(tmp_path, missing, {
        "TK-0101": {"scope": ["tools/a.py"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    data = check_plan(plan, tasks, "CYC-03")
    assert any(item["rule"] == 4 and "TK-0102" in item["message"] and "0 batches" in item["message"] for item in data["violations"])
    doubled = PLAN.replace(
        "- B1 | tasks: TK-0101, TK-0102 | after: none",
        "- B1 | tasks: TK-0101 | after: none\n- B2 | tasks: TK-0101, TK-0102 | after: B1",
    )
    plan, tasks = fixture(tmp_path, doubled, {
        "TK-0101": {"scope": ["tools/a.py"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    assert any(item["rule"] == 4 and "2 batches" in item["message"] for item in check_plan(plan, tasks, "CYC-03")["violations"])
    dangling = PLAN.replace("after: none", "after: B9")
    plan, tasks = fixture(tmp_path, dangling, {
        "TK-0101": {"scope": ["tools/a.py"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    assert any(item["rule"] == 4 and "missing batch" in item["message"] for item in check_plan(plan, tasks, "CYC-03")["violations"])
    ordered = PLAN.replace(
        "- B1 | tasks: TK-0101, TK-0102 | after: none",
        "- B1 | tasks: TK-0102 | after: none\n- B2 | tasks: TK-0101 | after: none",
    )
    plan, tasks = fixture(tmp_path, ordered, {
        "TK-0101": {"scope": ["tools/a.py"], "depends": ["TK-0102"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    assert any(item["rule"] == 4 and "does not follow" in item["message"] for item in check_plan(plan, tasks, "CYC-03")["violations"])
    followed = PLAN.replace(
        "- B1 | tasks: TK-0101, TK-0102 | after: none",
        "- B1 | tasks: TK-0102 | after: none\n- B2 | tasks: TK-0101 | after: B1",
    )
    plan, tasks = fixture(tmp_path, followed, {
        "TK-0101": {"scope": ["tools/a.py"], "depends": ["TK-0102"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    assert check_plan(plan, tasks, "CYC-03")["ok"]


def test_cross_cycle_dependency_is_ignored(tmp_path):
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/a.py"], "depends": ["TK-0009"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    write(tmp_path / "tasks" / "CYC-04" / "TK-0009.md", task_text("TK-0009", scope=["tools/model_check.py"]))
    assert check_plan(plan, tasks, "CYC-03")["ok"]


def test_cycle_without_batches_is_sequential(tmp_path):
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/a.py"]},
        "TK-0102": {"scope": ["tools/a.py"]},
    })
    write(tmp_path / "tasks" / "CYC-01" / "TK-0001.md", task_text("TK-0001", scope=["src/dupes.py"]))
    data = check_plan(plan, tasks, "CYC-01")
    assert data["ok"]
    assert data["sequential"][0]["cycle"] == "CYC-01"
    assert data["violations"] == []


def test_script_writes_no_files(tmp_path, monkeypatch):
    plan, tasks = fixture(tmp_path, PLAN, {
        "TK-0101": {"scope": ["tools/a.py"]},
        "TK-0102": {"scope": ["tools/b.py"]},
    })
    before = {path.relative_to(tmp_path): path.stat().st_mtime_ns for path in tmp_path.rglob("*") if path.is_file()}
    code = main(["--plan", str(plan), "--tasks", str(tasks), "--json"])
    after = {path.relative_to(tmp_path): path.stat().st_mtime_ns for path in tmp_path.rglob("*") if path.is_file()}
    assert code == 0
    assert before == after
    monkeypatch.chdir(tmp_path)
    snapshot = set(os.listdir(tmp_path))
    assert main(["--plan", str(plan), "--tasks", str(tasks)]) == 0
    assert set(os.listdir(tmp_path)) == snapshot


def test_usage_errors():
    assert main([]) == 2
    assert main(["--plan", "missing.md", "--tasks", "missing-dir"]) == 2
    assert main(["--plan", "01_plan/PLAN.md", "--tasks", "02_work/tasks", "--cycle", "nope"]) == 2


def test_live_plan_passes_and_early_cycles_are_sequential():
    root = Path(__file__).resolve().parents[2]
    data = check_plan(root / "01_plan" / "PLAN.md", root / "02_work" / "tasks")
    assert data["ok"]
    sequential = {row["cycle"] for row in data["sequential"]}
    assert sequential == {"CYC-01", "CYC-02"}
    for cycle in ("CYC-03", "CYC-04", "CYC-05", "CYC-06", "CYC-07"):
        one = check_plan(root / "01_plan" / "PLAN.md", root / "02_work" / "tasks", cycle)
        assert one["ok"]
        assert one["sequential"] == []