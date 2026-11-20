import json
from pathlib import Path

from tools.model_check import check_file, load_front_matter, main

CATALOG = """---
schema: 1
id: MODEL_CATALOG
updated: "2026-11-14"
models:
  - code: "gpt-5.6-luna"
    provider: unverified
    provider_source: none
    group: codex
    group_source: none
    aliases: ["cx/gpt-5.6-luna"]
    recommended_roles: [WORKER]
    capability_source: none
    price_source: none
    availability: confirmed
    availability_evidence: 02_work/runs/TK-0003_R1_DONE.md
    updated: "2026-11-14"
---
<!-- ANCHOR: ROUTE_CHECKS -->
## Route checks
- 2026-11-14T06:32Z | route: cx/gpt-5.6-luna | actual: gpt-5.6-luna | kind: chat | result: OK | source: probe | note: none
<!-- END: ROUTE_CHECKS -->
"""

MATRIX = """---
schema: 1
id: MODEL_MATRIX
updated: "2026-11-18"
status: PROPOSED
tier1_candidate_families: []
tier1: []
tier1_approved_by: ""
tier2: []
tier3: []
roles:
  - role: BRAINSTORM
    min_tier: T1
    order: []
    fallback: []
    evidence: []
  - role: PLANNING
    min_tier: T2
    order: []
    fallback: []
    evidence: []
  - role: REVIEWER
    min_tier: T2
    order: []
    fallback: []
    evidence: []
  - role: WORKER
    min_tier: T3
    order: []
    fallback: []
    evidence: []
---
<!-- ANCHOR: ASSIGNMENTS -->
## Assignments
- CYC-02 | REVIEWER | requested: gemini-3.8-flash-n | actual: gemini-3.8-flash-n | record: RVW-CYC-02 | match: yes
- CYC-02 | WORKER | requested: gpt-6.1-terra | actual: gpt-6.1-terra | record: 02_work/runs/TK-0005_R1_DONE.md | match: yes
- CYC-02 | WORKER | requested: gpt-5.6-luna | actual: gpt-5.6-luna[1m] | record: 02_work/runs/TK-0003_R1_DONE.md | match: yes
<!-- END: ASSIGNMENTS -->
"""

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path

def catalog_file(tmp_path, text=CATALOG):
    evidence = tmp_path / "02_work" / "runs" / "TK-0003_R1_DONE.md"
    write(evidence, "---\nschema: 1\n---\n")
    return write(tmp_path / "04_control" / "MODEL_CATALOG.md", text)

def replace_model(text, old, new):
    return text.replace(old, new, 1)

def keys(data):
    return [item["key"] for item in data["issues"]]

def messages(data):
    return [item["message"] for item in data["issues"]]

def test_load_front_matter_returns_mapping_and_body(tmp_path):
    path = catalog_file(tmp_path)
    data, body = load_front_matter(path)
    assert data["id"] == "MODEL_CATALOG"
    assert data["updated"] == "2026-11-14"
    assert isinstance(data["updated"], str)
    assert "ROUTE_CHECKS" in body

def test_valid_catalog_and_matrix(tmp_path):
    catalog = catalog_file(tmp_path)
    matrix = write(tmp_path / "04_control" / "MODEL_MATRIX.md", MATRIX)
    assert check_file(catalog, "catalog")[0] == 0
    assert check_file(matrix, "matrix")[0] == 0

def test_missing_required_key(tmp_path):
    text = CATALOG.replace("    provider: unverified\n", "", 1)
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert "models/0/provider" in keys(data)

def test_key_outside_schema(tmp_path):
    text = CATALOG.replace("    provider: unverified\n", "    provider: unverified\n    extra: 1\n", 1)
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert any("extra" in item["message"] and item["key"] == "models/0" for item in data["issues"])

def test_confirmed_without_evidence(tmp_path):
    text = CATALOG.replace("availability_evidence: 02_work/runs/TK-0003_R1_DONE.md", "availability_evidence: none", 1)
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert "models/0/availability_evidence" in keys(data)
    assert "confirmed has no evidence" in messages(data)

def test_evidence_pointer_missing(tmp_path):
    text = CATALOG.replace("02_work/runs/TK-0003_R1_DONE.md", "02_work/runs/TK-9999_R1_DONE.md", 1)
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert "evidence pointer does not exist" in messages(data)

def test_code_bracket_suffix(tmp_path):
    text = CATALOG.replace("code: \"gpt-5.6-luna\"", "code: \"gpt-5.6-luna[1m]\"", 1)
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert "models/0/code" in keys(data)
    assert "code has bracket suffix" in messages(data)

def test_alias_belongs_to_two_entries(tmp_path):
    extra = """  - code: "gpt-6.1-sol"
    provider: unverified
    provider_source: none
    group: codex
    group_source: none
    aliases: ["cx/gpt-5.6-luna"]
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: "2026-11-14"
"""
    text = CATALOG.replace("---\n<!-- ANCHOR: ROUTE_CHECKS -->", extra + "---\n<!-- ANCHOR: ROUTE_CHECKS -->", 1)
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert "alias belongs to two entries" in messages(data)

def test_duplicate_code(tmp_path):
    extra = """  - code: "gpt-5.6-luna"
    provider: unverified
    provider_source: none
    group: codex
    group_source: none
    aliases: []
    recommended_roles: []
    capability_source: none
    price_source: none
    availability: unconfirmed
    availability_evidence: none
    updated: "2026-11-14"
"""
    text = CATALOG.replace("---\n<!-- ANCHOR: ROUTE_CHECKS -->", extra + "---\n<!-- ANCHOR: ROUTE_CHECKS -->", 1)
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert "duplicate code" in messages(data)

def test_route_line_wrong_shape(tmp_path):
    text = CATALOG.replace(
        "- 2026-11-14T06:32Z | route: cx/gpt-5.6-luna | actual: gpt-5.6-luna | kind: chat | result: OK | source: probe | note: none",
        "- bad route line",
        1,
    )
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert "ROUTE_CHECKS line has wrong shape" in messages(data)

def test_result_ok_actual_none(tmp_path):
    text = CATALOG.replace("actual: gpt-5.6-luna", "actual: none", 1)
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert "result OK with actual none" in messages(data)

def test_route_note_over_15_words(tmp_path):
    note = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen"
    text = CATALOG.replace("note: none", "note: " + note, 1)
    code, data = check_file(catalog_file(tmp_path, text), "catalog")
    assert code == 1
    assert "note has 16 words" in messages(data)

def test_live_catalog_note_line_rejected():
    code, data = check_file("04_control/MODEL_CATALOG.md", "catalog")
    assert code == 1
    hits = [item for item in data["issues"] if item["message"] == "note has 21 words"]
    assert len(hits) == 1
    assert "2026-11-18T06:28Z" in hits[0]["line"]

def test_assignment_wrong_shape(tmp_path):
    text = MATRIX.replace(
        "- CYC-02 | REVIEWER | requested: gemini-3.8-flash-n | actual: gemini-3.8-flash-n | record: RVW-CYC-02 | match: yes",
        "- not an assignment",
        1,
    )
    code, data = check_file(write(tmp_path / "04_control" / "MODEL_MATRIX.md", text), "matrix")
    assert code == 1
    assert "ASSIGNMENTS line has wrong shape" in messages(data)

def test_match_yes_different_base_codes(tmp_path):
    text = MATRIX.replace("actual: gpt-6.1-terra", "actual: gpt-5.6-sol", 1)
    code, data = check_file(write(tmp_path / "04_control" / "MODEL_MATRIX.md", text), "matrix")
    assert code == 1
    assert "match yes with different base codes" in messages(data)

def test_old_cyc02_assignment_shape_passes(tmp_path):
    code, data = check_file(write(tmp_path / "04_control" / "MODEL_MATRIX.md", MATRIX), "matrix")
    assert code == 0
    assert data["issues"] == []

def test_proposed_empty_tier_passes_without_tier_verdict(tmp_path, capsys):
    path = write(tmp_path / "04_control" / "MODEL_MATRIX.md", MATRIX)
    assert main(["matrix", str(path)]) == 0
    out = capsys.readouterr().out
    assert "tier" not in out.lower()
    assert "PASS" in out

def test_script_does_not_write_control(tmp_path):
    root = tmp_path / "repo"
    catalog = catalog_file(root)
    before = {path.relative_to(root): path.read_bytes() for path in (root / "04_control").rglob("*") if path.is_file()}
    assert main(["catalog", str(catalog), "--json"]) == 0
    after = {path.relative_to(root): path.read_bytes() for path in (root / "04_control").rglob("*") if path.is_file()}
    assert before == after

def test_usage_error_exits_2():
    assert main([]) == 2

def test_requirements_pins():
    text = Path("tools/requirements.txt").read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if line.strip()]
    assert lines == ["jsonschema==4.26.0", "ruamel.yaml==0.19.1", "pytest==9.1.1"]
