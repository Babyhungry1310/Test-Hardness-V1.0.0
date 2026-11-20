import json
import subprocess
import sys
from pathlib import Path

from tools.assign_audit import main

CATALOG = """---
schema: 1
id: MODEL_CATALOG
updated: "2026-11-14"
models:
  - code: "gpt-5.6-luna"
    group: codex
  - code: "gpt-6.1-terra"
    group: codex
  - code: "grok-4.7"
    group: grok
  - code: "claude-opus-4-6-thinking"
    group: claude
  - code: "gemini-3.8-flash-n"
    group: gemini
---
<!-- ANCHOR: ROUTE_CHECKS -->
## Route checks
- 2026-11-14T06:32Z | route: Hardeness | actual: gpt-5.6-luna[1m] | kind: chat | result: OK | source: probe | note: combo
- 2026-11-14T06:32Z | route: cx/gpt-5.6-luna | actual: gpt-5.6-luna | kind: chat | result: OK | source: probe | note: none
- 2026-11-14T06:32Z | route: xai/grok-4.7 | actual: grok-4.7 | kind: chat | result: OK | source: probe | note: none
<!-- END: ROUTE_CHECKS -->
"""

MATRIX = """---
schema: 1
id: MODEL_MATRIX
---
<!-- ANCHOR: ASSIGNMENTS -->
## Assignments
- CYC-04 | WORKER | requested: gpt-5.6-luna | actual: gpt-5.6-luna | record: 02_work/runs/TK-0100_R1_DONE.md | match: yes
- CYC-04 | REVIEWER | requested: gemini-3.8-flash-n | actual: gemini-3.8-flash-n | record: RVW-CYC-04 | match: yes
<!-- END: ASSIGNMENTS -->
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def run_text(task="TK-0100", run="1", model="gpt-5.6-luna", extra=""):
    body = f"schema: 1\ntask: {task}\nrun: {run}\noutcome: DONE\n"
    if model is not None:
        body += f"model: \"{model}\"\n"
    if extra:
        body += extra
    return f"---\n{body}---\n"


def rvw_text(model="gemini-3.8-flash-n", include=True):
    body = "schema: 1\nid: RVW-CYC-04\ncycle: CYC-04\n"
    if include:
        body += f"reviewer_model: \"{model}\"\n"
    return f"---\n{body}---\n"


def build(tmp_path, run_model="gpt-5.6-luna", reviewer="gemini-3.8-flash-n", matrix=MATRIX, write_rvw=True, include_reviewer=True, run_extra="", write_run=True, write_task=True):
    root = tmp_path / "repo"
    write(root / "04_control" / "MODEL_CATALOG.md", CATALOG)
    write(root / "04_control" / "MODEL_MATRIX.md", matrix)
    if write_task:
        write(root / "02_work" / "tasks" / "CYC-04" / "TK-0100.md", "---\nschema: 1\n---\n")
    if write_run:
        write(root / "02_work" / "runs" / "TK-0100_R1_DONE.md", run_text(model=run_model, extra=run_extra))
    if write_rvw:
        write(root / "03_output" / "CYC-04" / "checks" / "RVW-CYC-04.md", rvw_text(reviewer, include_reviewer))
    return root


def invoke(root, cycle="CYC-04", extra=None):
    argv = ["--root", str(root), "--json"]
    if cycle is not None:
        argv.extend(["--cycle", cycle])
    if extra:
        argv.extend(extra)
    code = main(argv)
    return code


def payload(capsys):
    return json.loads(capsys.readouterr().out)


def reasons(data, kind="deviations"):
    return [item["reason"] for item in data[kind]]


def snapshot(root):
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}


def test_clean_cycle_exits_0(tmp_path, capsys):
    root = build(tmp_path)
    assert invoke(root) == 0
    data = payload(capsys)
    assert data["ok"] is True
    assert data["deviations"] == []
    assert data["notes"] == []


def test_missing_run_model(tmp_path, capsys):
    root = build(tmp_path, run_model=None)
    assert invoke(root) == 1
    data = payload(capsys)
    assert data["deviations"] == [{"cycle": "CYC-04", "record": "TK-0100_R1", "reason": "missing actual model", "detail": ""}]


def test_reviewer_matches_run_model(tmp_path, capsys):
    root = build(tmp_path, run_model="gpt-5.6-luna[1m]", reviewer="gpt-5.6-luna")
    assert invoke(root) == 1
    data = payload(capsys)
    assert {"cycle": "CYC-04", "record": "RVW-CYC-04", "reason": "reviewer_model matches run model", "detail": "TK-0100_R1 gpt-5.6-luna"} in data["deviations"]


def test_missing_reviewer_model(tmp_path, capsys):
    root = build(tmp_path, include_reviewer=False)
    assert invoke(root) == 1
    data = payload(capsys)
    assert {"cycle": "CYC-04", "record": "RVW-CYC-04", "reason": "missing reviewer_model", "detail": ""} in data["deviations"]


def test_assignment_record_missing(tmp_path, capsys):
    matrix = MATRIX.replace("02_work/runs/TK-0100_R1_DONE.md", "02_work/runs/TK-0199_R1_DONE.md")
    root = build(tmp_path, matrix=matrix)
    assert invoke(root) == 1
    data = payload(capsys)
    assert {"cycle": "CYC-04", "record": "02_work/runs/TK-0199_R1_DONE.md", "reason": "assignment record does not exist", "detail": "02_work/runs/TK-0199_R1_DONE.md"} in data["deviations"]


def test_match_yes_different_models(tmp_path, capsys):
    matrix = MATRIX.replace("actual: gpt-5.6-luna | record: 02_work/runs/TK-0100_R1_DONE.md | match: yes", "actual: gpt-6.1-terra | record: 02_work/runs/TK-0100_R1_DONE.md | match: yes")
    root = build(tmp_path, matrix=matrix)
    assert invoke(root) == 1
    data = payload(capsys)
    assert {"cycle": "CYC-04", "record": "02_work/runs/TK-0100_R1_DONE.md", "reason": "match yes with different models", "detail": "gpt-5.6-luna != gpt-6.1-terra"} in data["deviations"]


def test_match_pending_when_record_exists(tmp_path, capsys):
    matrix = MATRIX.replace("actual: gpt-5.6-luna | record: 02_work/runs/TK-0100_R1_DONE.md | match: yes", "actual: pending | record: 02_work/runs/TK-0100_R1_DONE.md | match: pending")
    root = build(tmp_path, matrix=matrix)
    assert invoke(root) == 1
    data = payload(capsys)
    assert {"cycle": "CYC-04", "record": "02_work/runs/TK-0100_R1_DONE.md", "reason": "match pending but record exists", "detail": "02_work/runs/TK-0100_R1_DONE.md"} in data["deviations"]


def test_match_no_is_note(tmp_path, capsys):
    matrix = MATRIX.replace("actual: gpt-5.6-luna | record: 02_work/runs/TK-0100_R1_DONE.md | match: yes", "actual: gpt-6.1-terra | record: 02_work/runs/TK-0100_R1_DONE.md | match: no")
    root = build(tmp_path, matrix=matrix)
    assert invoke(root) == 0
    data = payload(capsys)
    assert data["deviations"] == []
    assert {"cycle": "CYC-04", "record": "02_work/runs/TK-0100_R1_DONE.md", "reason": "match no", "detail": "02_work/runs/TK-0100_R1_DONE.md"} in data["notes"]


def test_actual_not_in_catalog_is_note(tmp_path, capsys):
    root = build(tmp_path, run_model="gpt-9.9-nova")
    assert invoke(root) == 0
    data = payload(capsys)
    assert data["deviations"] == []
    assert {"cycle": "CYC-04", "record": "TK-0100_R1", "reason": "actual not in catalog", "detail": "gpt-9.9-nova"} in data["notes"]


def test_same_group_different_code_exits_0(tmp_path, capsys):
    root = build(tmp_path, run_model="gpt-5.6-luna", reviewer="gpt-6.1-terra")
    assert invoke(root) == 0
    data = payload(capsys)
    assert data["ok"] is True
    assert data["deviations"] == []
    assert {"cycle": "CYC-04", "record": "RVW-CYC-04", "reason": "reviewer shares group with worker", "detail": "TK-0100_R1 codex"} in data["notes"]


def test_hardeness_is_unknown(tmp_path, capsys):
    root = build(tmp_path, run_model="hardeness")
    assert invoke(root) == 1
    data = payload(capsys)
    assert {"cycle": "CYC-04", "record": "TK-0100_R1", "reason": "UNKNOWN", "detail": "hardeness"} in data["deviations"]
    assert "reviewer_model matches run model" not in reasons(data)
    assert "same" not in reasons(data)
    assert "different" not in reasons(data)


def test_route_only_string_is_unknown(tmp_path, capsys):
    root = build(tmp_path, run_model="cx/gpt-5.6-luna", reviewer="gpt-5.6-luna")
    assert invoke(root) == 1
    data = payload(capsys)
    assert {"cycle": "CYC-04", "record": "TK-0100_R1", "reason": "UNKNOWN", "detail": "cx/gpt-5.6-luna"} in data["deviations"]
    assert "reviewer_model matches run model" not in reasons(data)


def test_bad_comma_part_is_unknown(tmp_path, capsys):
    root = build(tmp_path, run_model="gpt-5.6-luna, , grok-4.7", reviewer="gpt-5.6-luna")
    assert invoke(root) == 1
    data = payload(capsys)
    assert {"cycle": "CYC-04", "record": "TK-0100_R1", "reason": "UNKNOWN", "detail": "gpt-5.6-luna, , grok-4.7"} in data["deviations"]
    assert "reviewer_model matches run model" not in reasons(data)


def test_comma_split_reports_overlap_on_one_code(tmp_path, capsys):
    root = build(tmp_path, run_model="claude-opus-4-6-thinking, grok-4.7", reviewer="grok-4.7")
    assert invoke(root) == 1
    data = payload(capsys)
    assert {"cycle": "CYC-04", "record": "RVW-CYC-04", "reason": "reviewer_model matches run model", "detail": "TK-0100_R1 grok-4.7"} in data["deviations"]
    assert "UNKNOWN" not in reasons(data)


def test_probe_only_is_unknown_and_creates_no_rvw(tmp_path, capsys):
    matrix = """---
schema: 1
id: MODEL_MATRIX
---
<!-- ANCHOR: ASSIGNMENTS -->
## Assignments
- CYC-04 | WORKER | requested: gpt-5.6-luna | actual: gpt-5.6-luna | record: 02_work/runs/TK-0100_R1_DONE.md | match: yes
<!-- END: ASSIGNMENTS -->
"""
    root = build(tmp_path, matrix=matrix, write_rvw=False)
    before = snapshot(root)
    assert invoke(root) == 1
    data = payload(capsys)
    assert data["deviations"] == [{"cycle": "CYC-04", "record": "RVW-CYC-04", "reason": "UNKNOWN", "detail": "missing session file"}]
    assert "gpt-5.6-luna" not in json.dumps(data["deviations"])
    assert snapshot(root) == before
    assert not (root / "03_output" / "CYC-04" / "checks" / "RVW-CYC-04.md").exists()


def test_caller_session_label_ignored(tmp_path, capsys):
    root = build(tmp_path, run_model=None, run_extra="session_label: gpt-5.6-luna\n")
    assert invoke(root) == 1
    data = payload(capsys)
    assert data["deviations"] == [{"cycle": "CYC-04", "record": "TK-0100_R1", "reason": "missing actual model", "detail": ""}]
    assert invoke(root, extra=["--session", "gpt-5.6-luna"]) == 2


def test_script_does_not_write(tmp_path, capsys):
    root = build(tmp_path, run_model="grok-4.7", reviewer="grok-4.7")
    before = snapshot(root)
    assert invoke(root) == 1
    payload(capsys)
    assert snapshot(root) == before


def test_usage_exits_2(tmp_path, capsys):
    root = build(tmp_path)
    assert main([]) == 2
    capsys.readouterr()
    assert main(["--root", str(root), "--cycle", "nope", "--json"]) == 2
    capsys.readouterr()
    assert main(["--root", str(tmp_path / "missing"), "--json"]) == 2
    data = payload(capsys)
    assert data["error"] == "root is not a directory"


def test_old_group_requested_is_not_rejudged(tmp_path, capsys):
    matrix = """---
schema: 1
id: MODEL_MATRIX
---
<!-- ANCHOR: ASSIGNMENTS -->
## Assignments
- CYC-04 | WORKER | requested: nhóm Codex (DEC-0012) | actual: gpt-5.6-luna | record: 02_work/runs/TK-0100_R1_DONE.md | match: yes
- CYC-04 | REVIEWER | requested: nhóm Gemini (DEC-0012) | actual: gemini-3.8-flash-n | record: RVW-CYC-04 | match: yes
<!-- END: ASSIGNMENTS -->
"""
    root = build(tmp_path, matrix=matrix)
    assert invoke(root) == 0
    data = payload(capsys)
    assert data["deviations"] == []


def test_cli_script_reads_cycle(tmp_path):
    root = build(tmp_path)
    proc = subprocess.run(
        [sys.executable, "tools/assign_audit.py", "--root", str(root), "--cycle", "CYC-04", "--json"],
        capture_output=True,
        cwd=Path.cwd(),
    )
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["ok"] is True
    assert data["deviations"] == []


def test_imports_load_front_matter_without_copy():
    text = Path("tools/assign_audit.py").read_text(encoding="utf-8")
    assert "from tools.model_check import" in text
    assert "load_front_matter" in text
    assert "def load_front_matter" not in text


def test_text_mode_names_record(tmp_path, capsys):
    root = build(tmp_path, run_model=None)
    assert main(["--root", str(root), "--cycle", "CYC-04"]) == 1
    out = capsys.readouterr().out
    assert "deviation: TK-0100_R1: missing actual model" in out
    assert out.endswith("FAIL\n")

def test_bom_run_in_cycle_is_read(tmp_path, capsys):
    root = build(tmp_path)
    path = root / "02_work" / "runs" / "TK-0100_R1_DONE.md"
    path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())
    assert invoke(root) == 0
    data = payload(capsys)
    assert data["deviations"] == []
    assert data["ok"] is True


def test_other_cycle_bom_does_not_break_selected_cycle(tmp_path, capsys):
    root = build(tmp_path)
    write(root / "02_work" / "tasks" / "CYC-03" / "TK-0107.md", "---\nschema: 1\n---\n")
    raw = "---\nschema: 1\ntask: TK-0107\nrun: 1\noutcome: DONE\nmodel: \"grok-4.7\"\n---\n".encode("utf-8")
    (root / "02_work" / "runs" / "TK-0107_R1_DONE.md").write_bytes(b"\xef\xbb\xbf" + raw)
    assert invoke(root) == 0
    data = payload(capsys)
    assert data["deviations"] == []
