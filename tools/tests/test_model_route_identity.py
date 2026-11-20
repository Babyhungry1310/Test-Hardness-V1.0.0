import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def catalog(tmp_path, models, routes=""):
    body = (
        "---\nschema: 1\nid: MODEL_CATALOG\nupdated: \"2026-11-14\"\nmodels:\n"
        + models
        + "---\n<!-- ANCHOR: ROUTE_CHECKS -->\n"
        + routes
        + "<!-- END: ROUTE_CHECKS -->\n"
    )
    return write(tmp_path / "catalog.md", body)


def entry(code, aliases=""):
    return f"  - code: \"{code}\"\n    availability: confirmed\n    aliases: [{aliases}]\n"


def route(name, actual, when="2026-11-14T08:00Z"):
    return f"- {when} | route: {name} | actual: {actual} | kind: agent-tools | result: OK | source: probe | note: none\n"


def run_file(tmp_path, name, model_value):
    return write(tmp_path / "repo" / "02_work" / "runs" / name, f"---\nschema: 1\nmodel: \"{model_value}\"\n---\n")


def cli(catalog_file, args):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    done = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "model_select.py"), "--catalog", str(catalog_file), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return done.returncode, done.stdout


def test_probe_is_unknown_and_composite_run_splits(tmp_path):
    routes = route("xai/grok-4", "grok-4.7", "2026-11-14T09:00Z") + route("xai/grok-4", "claude-opus-4-6-thinking", "2026-11-14T06:00Z")
    routes += route("cx/claude-opus-4-6-thinking", "claude-opus-4-6-thinking") + route("cx/grok-4.7", "grok-4.7")
    catalog_file = catalog(tmp_path, entry("claude-opus-4-6-thinking") + entry("grok-4.7"), routes)
    run = run_file(tmp_path, "TK-0008_R4_DONE.md", "claude-opus-4-6-thinking, grok-4.7")
    flipped = run_file(tmp_path, "TK-0008_R4_FLIP.md", "grok-4.7, claude-opus-4-6-thinking")
    probe = "route-check:" + str(catalog_file) + "#xai/grok-4"
    code, out = cli(catalog_file, ["same", "--left-evidence", probe, "--right-evidence", "run:" + str(run)])
    assert code == 1 and out == "UNKNOWN probe is not session actual\n"
    code, out = cli(catalog_file, ["same", "--left-evidence", "run:" + str(run), "--right-evidence", "run:" + str(flipped)])
    assert code == 0 and out == "same\n"
    code, out = cli(catalog_file, ["eligible", "--exclude-evidence", "run:" + str(run)])
    assert code == 1 and "claude-opus-4-6-thinking: excluded by run evidence" in out
    assert "grok-4.7: excluded by run evidence" in out


def test_reviewer_stages_do_not_treat_run_as_actual(tmp_path):
    catalog_file = catalog(tmp_path, entry("gpt-5.6-terra") + entry("claude-opus-4-6-thinking") + entry("grok-4.7"))
    worker = run_file(tmp_path, "TK-0008_R4_DONE.md", "claude-opus-4-6-thinking, grok-4.7")
    other = run_file(tmp_path, "TK-0007_R1_DONE.md", "gpt-5.6-terra")
    code, out = cli(catalog_file, ["reviewer", "--stage", "select", "--requested", "gpt-5.6-terra", "--worker-evidence", "run:" + str(worker)])
    assert code == 0 and out == "planned gpt-5.6-terra\n"
    log = write(tmp_path / "new-session.jsonl", "{\"payload\": {\"model\": \"grok-4.7\"}}\n{\"payload\": {\"model\": \"gpt-5.6-terra\"}}\n")
    args = ["reviewer", "--stage", "start", "--worker-evidence", "run:" + str(worker), "--reviewer-evidence", "log:" + str(log)]
    code, out = cli(catalog_file, args)
    assert code == 0 and out == "different\n"
    args[-1] = "run:" + str(other)
    code, out = cli(catalog_file, args)
    assert code == 1 and out == "UNKNOWN stage start requires log evidence\n"
    rvw = write(tmp_path / "RVW-CYC-04.md", "---\nschema: 1\nreviewer_model: \"gpt-5.6-terra\"\n---\n")
    args = ["reviewer", "--stage", "pr", "--worker-evidence", "run:" + str(worker), "--reviewer-evidence", "rvw:" + str(rvw)]
    code, out = cli(catalog_file, args)
    assert code == 0 and out == "different\n"
    args[-1] = "run:" + str(other)
    code, out = cli(catalog_file, args)
    assert code == 1 and out == "UNKNOWN stage pr requires rvw evidence\n"
    args[-1] = "log:" + str(log)
    code, out = cli(catalog_file, args)
    assert code == 1 and out == "UNKNOWN stage pr requires rvw evidence\n"


def test_slash_and_empty_part_remain_unknown(tmp_path):
    catalog_file = catalog(tmp_path, entry("gpt-5.6-luna"))
    slash = run_file(tmp_path, "TK-slash_R1_DONE.md", "xai/grok-4.7")
    other = run_file(tmp_path, "TK-0006_R1_DONE.md", "gpt-5.6-luna")
    empty = run_file(tmp_path, "TK-empty_R1_DONE.md", "a, , b")
    code, out = cli(catalog_file, ["same", "--left-evidence", "run:" + str(slash), "--right-evidence", "run:" + str(other)])
    assert code == 1 and out == "UNKNOWN xai/grok-4.7\n"
    code, out = cli(catalog_file, ["same", "--left-evidence", "run:" + str(empty), "--right-evidence", "run:" + str(other)])
    assert code == 1 and out == "UNKNOWN a, , b\n"


def test_alias_only_route_is_not_eligible_and_bracket_is_same(tmp_path):
    models = entry("gpt-5.6-luna", "\"cx/gpt-5.6-luna\", \"gpt-5.6-terra\"") + entry("gpt-5.6-terra")
    catalog_file = catalog(tmp_path, models, route("cx/gpt-5.6-terra", "gpt-5.6-terra"))
    code, out = cli(catalog_file, ["eligible"])
    assert code == 0 and out == "gpt-5.6-terra\n"
    left = run_file(tmp_path, "TK-luna_R1_DONE.md", "gpt-5.6-luna")
    variant = run_file(tmp_path, "TK-luna_R1_1M.md", "gpt-5.6-luna[1m]")
    terra = run_file(tmp_path, "TK-terra_R1_DONE.md", "gpt-5.6-terra")
    code, out = cli(catalog_file, ["same", "--left-evidence", "run:" + str(left), "--right-evidence", "run:" + str(variant)])
    assert code == 0 and out == "same\n"
    code, out = cli(catalog_file, ["same", "--left-evidence", "run:" + str(left), "--right-evidence", "run:" + str(terra)])
    assert code == 0 and out == "different\n"
