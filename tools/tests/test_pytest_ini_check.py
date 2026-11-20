import hashlib
import json
import subprocess
import sys
from pathlib import Path

from tools.pytest_ini_check import inspect_project, main

SCRIPT = Path(__file__).resolve().parent.parent / "pytest_ini_check.py"
TEMPLATE = Path(__file__).resolve().parent.parent.parent / "harness" / "templates" / "pytest.ini"


def snapshot(root):
    snap = {}
    for p in root.rglob("*"):
        if p.is_file():
            st = p.stat()
            snap[str(p.relative_to(root))] = (
                hashlib.sha256(p.read_bytes()).hexdigest(),
                st.st_mtime_ns,
                st.st_size,
            )
    return snap


def test_repo_is_same(capsys):
    repo_root = Path(__file__).resolve().parent.parent.parent
    code = main([str(repo_root), "--json"])
    assert code == 0
    data = json.loads(capsys.readouterr().out)
    assert data["status"] == "same"
    assert data["file"] == "pytest.ini"
    assert data["options"]["testpaths"] == "tests"


def test_absent_empty_project(tmp_path):
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "absent"
    assert res["file"] is None
    assert res["options"] == {}
    assert main([str(tmp_path)]) == 0


def test_differs_different_testpaths(tmp_path):
    (tmp_path / "pytest.ini").write_text("[pytest]\ntestpaths = other\n", encoding="utf-8")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "differs"
    assert res["file"] == "pytest.ini"
    assert main([str(tmp_path)]) == 1


def test_differs_same_testpaths_with_addopts(tmp_path, capsys):
    (tmp_path / "pytest.ini").write_text("[pytest]\ntestpaths = tests\naddopts = -ra -q\n", encoding="utf-8")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "differs"
    assert "addopts" in res["options"]
    assert any("addopts" in d for d in res["differences"])
    code = main([str(tmp_path), "--json"])
    assert code == 1
    data = json.loads(capsys.readouterr().out)
    assert "addopts" in data["options"]
    assert any("addopts" in d for d in data["differences"])


def test_shadowed_pyproject_toml(tmp_path):
    (tmp_path / "pyproject.toml").write_text('[tool.pytest.ini_options]\ntestpaths = ["tests"]\n', encoding="utf-8")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "shadowed"
    assert res["file"] == "pyproject.toml"
    assert main([str(tmp_path)]) == 1


def test_shadowed_tox_ini(tmp_path):
    (tmp_path / "tox.ini").write_text("[pytest]\ntestpaths = tests\n", encoding="utf-8")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "shadowed"
    assert res["file"] == "tox.ini"
    assert main([str(tmp_path)]) == 1


def test_shadowed_setup_cfg(tmp_path):
    (tmp_path / "setup.cfg").write_text("[tool:pytest]\ntestpaths = tests\n", encoding="utf-8")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "shadowed"
    assert res["file"] == "setup.cfg"
    assert main([str(tmp_path)]) == 1


def test_edge_pytest_ini_empty(tmp_path):
    (tmp_path / "pytest.ini").write_text("", encoding="utf-8")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "absent"
    assert main([str(tmp_path)]) == 0


def test_edge_pytest_ini_no_pytest_section(tmp_path):
    (tmp_path / "pytest.ini").write_text("[custom]\nfoo = bar\n", encoding="utf-8")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "absent"
    assert main([str(tmp_path)]) == 0


def test_edge_pyproject_toml_no_pytest_table(tmp_path):
    (tmp_path / "pyproject.toml").write_text('[tool.other]\nfoo = "bar"\n', encoding="utf-8")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "absent"
    assert main([str(tmp_path)]) == 0


def test_edge_testpaths_multiple_values(tmp_path):
    (tmp_path / "pytest.ini").write_text("[pytest]\ntestpaths = tests other\n", encoding="utf-8")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "differs"
    assert main([str(tmp_path)]) == 1


def test_edge_testpaths_variations(tmp_path):
    for val in ("tests/", "./tests", "./tests/", ".\\tests", ".\\tests\\", "tests\\"):
        (tmp_path / "pytest.ini").write_text(f"[pytest]\ntestpaths = {val}\n", encoding="utf-8")
        res = inspect_project(tmp_path, TEMPLATE)
        assert res["status"] == "same"
        assert main([str(tmp_path)]) == 0


def test_edge_bom_and_crlf(tmp_path):
    (tmp_path / "pytest.ini").write_bytes(b"\xef\xbb\xbf[pytest]\r\ntestpaths = tests\r\n")
    res = inspect_project(tmp_path, TEMPLATE)
    assert res["status"] == "same"
    assert main([str(tmp_path)]) == 0


def test_syntax_errors_exit_2(tmp_path, capsys):
    (tmp_path / "pytest.ini").write_text("invalid ini without header\n", encoding="utf-8")
    code = main([str(tmp_path)])
    assert code == 2
    err = capsys.readouterr().err
    assert "pytest.ini" in err

    (tmp_path / "pytest.ini").unlink()
    (tmp_path / "pyproject.toml").write_text("[tool\nfoo = ", encoding="utf-8")
    code = main([str(tmp_path)])
    assert code == 2
    err = capsys.readouterr().err
    assert "pyproject.toml" in err

    (tmp_path / "pyproject.toml").unlink()
    (tmp_path / "tox.ini").write_text("broken tox\n", encoding="utf-8")
    code = main([str(tmp_path)])
    assert code == 2
    err = capsys.readouterr().err
    assert "tox.ini" in err

    (tmp_path / "tox.ini").unlink()
    (tmp_path / "setup.cfg").write_text("broken setup\n", encoding="utf-8")
    code = main([str(tmp_path)])
    assert code == 2
    err = capsys.readouterr().err
    assert "setup.cfg" in err


def test_immutability_no_files_changed(tmp_path):
    (tmp_path / "pytest.ini").write_text("[pytest]\ntestpaths = tests\n", encoding="utf-8")
    sub = tmp_path / "tests"
    sub.mkdir()
    (sub / "test_a.py").write_text("def test_dummy(): pass\n", encoding="utf-8")
    (tmp_path / "data.txt").write_bytes(b"sample binary or text\n")
    before = snapshot(tmp_path)
    assert main([str(tmp_path)]) == 0
    assert main([str(tmp_path), "--json"]) == 0
    after = snapshot(tmp_path)
    assert before == after


def test_present_options_listing(tmp_path, capsys):
    (tmp_path / "pytest.ini").write_text(
        "[pytest]\n"
        "testpaths = tests\n"
        "addopts = -ra\n"
        "python_files = test_*.py\n"
        "norecursedirs = build dist\n"
        "markers =\n"
        "    slow: slow marker\n",
        encoding="utf-8",
    )
    code = main([str(tmp_path), "--json"])
    assert code == 1
    data = json.loads(capsys.readouterr().out)
    for opt in ("testpaths", "addopts", "python_files", "norecursedirs", "markers"):
        assert opt in data["options"]


def test_cli_subprocess_invocation(tmp_path):
    (tmp_path / "pytest.ini").write_text("[pytest]\ntestpaths = tests\n", encoding="utf-8")
    res = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path), "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0
    parsed = json.loads(res.stdout)
    assert parsed["status"] == "same"


def test_cli_usage_errors(tmp_path):
    assert main([str(tmp_path / "nonexistent")]) == 2
    assert main([str(tmp_path), "--template", str(tmp_path / "nonexistent.ini")]) == 2
    broken_tpl = tmp_path / "bad_tpl.ini"
    broken_tpl.write_text("bad template\n", encoding="utf-8")
    assert main([str(tmp_path), "--template", str(broken_tpl)]) == 2
