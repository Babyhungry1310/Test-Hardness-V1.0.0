import json
from pathlib import Path

from tools.model_select import main

MODEL = """  - code: "{code}"
    provider: unverified
    provider_source: none
    group: codex
    group_source: none
    aliases: [{aliases}]
    recommended_roles: [WORKER]
    capability_source: none
    price_source: none
    availability: {availability}
    availability_evidence: none
    updated: "2026-11-14"
"""

ROUTE = "- {when} | route: {route} | actual: {actual} | kind: {kind} | result: {result} | source: probe | note: none\n"


def model(code, availability="unconfirmed", aliases=""):
    return MODEL.format(code=code, availability=availability, aliases=aliases)


def route(route_name, actual, when="2026-11-14T06:32Z", kind="chat", result="OK"):
    return ROUTE.format(when=when, route=route_name, actual=actual, kind=kind, result=result)


def catalog(models, routes):
    return (
        "---\n"
        "schema: 1\n"
        "id: MODEL_CATALOG\n"
        'updated: "2026-11-14"\n'
        "models:\n"
        + "".join(models)
        + "---\n"
        "<!-- ANCHOR: ROUTE_CHECKS -->\n"
        + "".join(routes)
        + "<!-- END: ROUTE_CHECKS -->\n"
    )


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def run_file(tmp_path, name, model_value):
    path = tmp_path / "repo" / "02_work" / "runs" / name
    write(path, "---\nschema: 1\nmodel: \"" + model_value + "\"\n---\n")
    return path


def rvw_file(tmp_path, model_value):
    path = tmp_path / "repo" / "03_output" / "RVW-CYC-04.md"
    write(path, "---\nschema: 1\nreviewer_model: \"" + model_value + "\"\n---\n")
    return path


def log_file(tmp_path, model_value):
    path = tmp_path / "session.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    row = json.dumps({"payload": {"model": model_value}}, ensure_ascii=False)
    write(path, row + "\n")
    return path


def catalog_path(tmp_path, text):
    return write(tmp_path / "catalog.md", text)


def run_cli(capsys, argv):
    code = main(argv)
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_same_bracket_variant_is_same_and_other_code_is_different(tmp_path, capsys):
    left = run_file(tmp_path, "TK-0006_R1_DONE.md", "gpt-5.6-luna")
    variant = run_file(tmp_path, "TK-0007_R1_DONE.md", "gpt-5.6-luna[1m]")
    other = run_file(tmp_path, "TK-0008_R1_DONE.md", "gpt-5.6-terra")
    catalog_file = catalog_path(tmp_path, catalog([model("gpt-5.6-luna")], []))
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "same", "--left-evidence", "run:" + str(left), "--right-evidence", "run:" + str(variant)])
    assert code == 0
    assert out.startswith("same")
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "same", "--left-evidence", "run:" + str(left), "--right-evidence", "run:" + str(other)])
    assert code == 0
    assert out.startswith("different")


def test_slash_model_and_empty_part_are_unknown(tmp_path, capsys):
    slash = run_file(tmp_path, "TK-slash_R1_DONE.md", "xai/grok-4.7")
    other = run_file(tmp_path, "TK-0006_R1_DONE.md", "gpt-5.6-luna")
    empty = run_file(tmp_path, "TK-empty_R1_DONE.md", "a, , b")
    catalog_file = catalog_path(tmp_path, catalog([model("gpt-5.6-luna")], []))
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "same", "--left-evidence", "run:" + str(slash), "--right-evidence", "run:" + str(other)])
    assert code == 1
    assert out.startswith("UNKNOWN")
    assert "xai/grok-4.7" in out
    assert "different" not in out
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "same", "--left-evidence", "run:" + str(empty), "--right-evidence", "run:" + str(other)])
    assert code == 1
    assert out.startswith("UNKNOWN")
    assert "a, , b" in out


def test_probe_is_not_session_evidence(tmp_path, capsys):
    other = run_file(tmp_path, "TK-0006_R1_DONE.md", "grok-4.3")
    catalog_file = catalog_path(tmp_path, catalog([model("grok-4.3")], [route("xai/grok-4", "grok-4.3")]))
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "same", "--left-evidence", "route-check:" + str(catalog_file) + "#xai/grok-4", "--right-evidence", "run:" + str(other)])
    assert code == 1
    assert out.startswith("UNKNOWN")
    assert "different" not in out
    assert "same" not in out


def test_free_string_label_is_rejected(tmp_path, capsys):
    catalog_file = catalog_path(tmp_path, catalog([model("gpt-5.6-luna")], []))
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "same", "--left-evidence", "model:gpt-5.6-luna", "--right-evidence", "model:gpt-5.6-luna"])
    assert code == 1
    assert out.startswith("UNKNOWN")


def test_eligible_uses_newest_route_and_ignores_old_actual(tmp_path, capsys):
    text = catalog(
        [model("gpt-5.6-luna", "confirmed"), model("gpt-5.6-terra", "unconfirmed")],
        [
            route("cx/gpt-5.6-luna", "gpt-5.6-terra", "2026-11-14T06:00Z"),
            route("cx/gpt-5.6-luna", "gpt-5.6-luna", "2026-11-14T08:00Z", "agent-tools"),
            route("cx/gpt-5.6-terra", "gpt-5.6-terra", "2026-11-14T07:00Z"),
        ],
    )
    catalog_file = catalog_path(tmp_path, text)
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "eligible", "--json"])
    assert code == 0
    data = json.loads(out)
    assert data["models"] == ["gpt-5.6-luna", "gpt-5.6-terra"]


def test_needs_tools_filters_chat_unconfirmed_and_fail(tmp_path, capsys):
    text = catalog(
        [
            model("gpt-5.6-luna", "unconfirmed"),
            model("gpt-5.6-terra", "confirmed"),
            model("gpt-6.1-sol", "unconfirmed"),
            model("grok-4.7", "unconfirmed"),
        ],
        [
            route("cx/gpt-5.6-luna", "gpt-5.6-luna", kind="chat"),
            route("cx/gpt-5.6-terra", "gpt-5.6-terra", kind="chat"),
            route("cx/gpt-6.1-sol", "gpt-6.1-sol", kind="agent-tools"),
            route("xai/grok-4.7", "grok-4.7", "2026-11-14T08:00Z", "agent-tools", "FAIL"),
            route("xai/grok-4.7", "grok-4.7", "2026-11-14T06:00Z", "agent-tools", "OK"),
        ],
    )
    catalog_file = catalog_path(tmp_path, text)
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "eligible", "--needs-tools", "--json"])
    assert code == 0
    data = json.loads(out)
    assert data["models"] == ["gpt-5.6-terra", "gpt-6.1-sol"]
    reasons = {item["code"]: item["reason"] for item in data["rejected"]}
    assert "gpt-5.6-luna" in reasons
    assert "unconfirmed" in reasons["gpt-5.6-luna"]
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "eligible", "--json"])
    data = json.loads(out)
    assert "gpt-5.6-luna" in data["models"]
    assert "grok-4.7" not in data["models"]


def test_alias_without_ok_route_is_not_eligible(tmp_path, capsys):
    text = catalog(
        [model("gpt-5.6-luna", "confirmed", '"cx/gpt-5.6-luna"')],
        [route("other/route", "gpt-5.6-terra")],
    )
    catalog_file = catalog_path(tmp_path, text)
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "eligible", "--json"])
    data = json.loads(out)
    assert code == 1
    assert data["models"] == []


def test_empty_list_exits_1_with_each_reason(tmp_path, capsys):
    text = catalog(
        [model("gpt-5.6-luna", "unconfirmed"), model("grok-4.7", "unconfirmed")],
        [
            route("cx/gpt-5.6-luna", "gpt-5.6-luna", result="FAIL"),
            route("xai/grok-4.7", "grok-4.7", result="FAIL"),
        ],
    )
    catalog_file = catalog_path(tmp_path, text)
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "eligible"])
    assert code == 1
    assert "no eligible model" in out
    assert out.count("FAIL") == 2
    assert "cx/gpt-5.6-luna" in out
    assert "xai/grok-4.7" in out


def test_exclude_evidence_removes_model_from_run(tmp_path, capsys):
    text = catalog(
        [model("gpt-5.6-luna", "confirmed"), model("gpt-5.6-terra", "confirmed")],
        [
            route("cx/gpt-5.6-luna", "gpt-5.6-luna"),
            route("cx/gpt-5.6-terra", "gpt-5.6-terra"),
        ],
    )
    catalog_file = catalog_path(tmp_path, text)
    excluded = run_file(tmp_path, "TK-0006_R1_DONE.md", "gpt-5.6-luna[1m]")
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "eligible", "--exclude-evidence", "run:" + str(excluded), "--json"])
    assert code == 0
    data = json.loads(out)
    assert data["models"] == ["gpt-5.6-terra"]
    assert any(item["code"] == "gpt-5.6-luna" for item in data["rejected"])


def test_reviewer_select_prints_planned_only(tmp_path, capsys):
    worker = run_file(tmp_path, "TK-0006_R1_DONE.md", "gpt-5.6-luna")
    other_session = run_file(tmp_path, "TK-0007_R1_DONE.md", "gpt-5.6-terra")
    catalog_file = catalog_path(tmp_path, catalog([model("gpt-5.6-terra", "confirmed")], [route("cx/gpt-5.6-terra", "gpt-5.6-terra", kind="agent-tools")]))
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "reviewer", "--stage", "select", "--requested", "gpt-5.6-terra", "--worker-evidence", "run:" + str(worker)])
    assert code == 0
    assert out.startswith("planned")
    assert "same" not in out
    assert "different" not in out
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "reviewer", "--stage", "start", "--requested", "gpt-5.6-terra", "--worker-evidence", "run:" + str(worker), "--reviewer-evidence", "run:" + str(other_session)])
    assert code == 1
    assert out.startswith("UNKNOWN")
    assert "planned" not in out


def test_reviewer_start_and_pr_require_different_base_code(tmp_path, capsys):
    worker = run_file(tmp_path, "TK-0006_R1_DONE.md", "gpt-5.6-luna")
    grouped = run_file(tmp_path, "TK-0008_R1_DONE.md", "gpt-6.1-terra")
    log = log_file(tmp_path, "gpt-5.6-terra")
    same_log = log_file(tmp_path / "same", "gpt-5.6-luna[1m]")
    rvw = rvw_file(tmp_path, "gpt-5.6-terra")
    catalog_file = catalog_path(tmp_path, catalog([model("gpt-5.6-luna"), model("gpt-5.6-terra"), model("gpt-6.1-terra")], []))
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "reviewer", "--stage", "start", "--worker-evidence", "run:" + str(worker), "--worker-evidence", "run:" + str(grouped), "--reviewer-evidence", "log:" + str(log)])
    assert code == 0
    assert out.startswith("different")
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "reviewer", "--stage", "pr", "--worker-evidence", "run:" + str(worker), "--reviewer-evidence", "rvw:" + str(rvw)])
    assert code == 0
    assert out.startswith("different")
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "reviewer", "--stage", "start", "--worker-evidence", "run:" + str(worker), "--reviewer-evidence", "log:" + str(same_log)])
    assert code == 1
    assert not out.startswith("different")
    unknown = log_file(tmp_path / "unknown", "xai/grok-4.7")
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "reviewer", "--stage", "start", "--worker-evidence", "run:" + str(worker), "--reviewer-evidence", "log:" + str(unknown)])
    assert code == 1
    assert out.startswith("UNKNOWN")
    assert "xai/grok-4.7" in out


def test_missing_reviewer_or_worker_model_exits_1(tmp_path, capsys):
    worker = write(tmp_path / "repo" / "02_work" / "runs" / "TK-0006_R1_DONE.md", "---\nschema: 1\n---\n")
    rvw = write(tmp_path / "repo" / "03_output" / "RVW-CYC-04.md", "---\nschema: 1\n---\n")
    catalog_file = catalog_path(tmp_path, catalog([model("gpt-5.6-luna")], []))
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "reviewer", "--stage", "pr", "--worker-evidence", "run:" + str(worker), "--reviewer-evidence", "rvw:" + str(rvw)])
    assert code == 1
    assert "missing model" in out
    present = run_file(tmp_path, "TK-0007_R1_DONE.md", "gpt-5.6-luna")
    code, out, _err = run_cli(capsys, ["--catalog", str(catalog_file), "reviewer", "--stage", "pr", "--worker-evidence", "run:" + str(present), "--reviewer-evidence", "rvw:" + str(rvw)])
    assert code == 1
    assert "missing reviewer_model" in out
