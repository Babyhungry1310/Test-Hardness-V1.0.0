import configparser
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = ROOT / "harness" / "templates" / "pytest.ini"


def run_collect(cwd, args=None):
    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
    if args:
        cmd.extend(args)
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
    return [
        line.strip().replace("\\", "/")
        for line in proc.stdout.splitlines()
        if "::" in line
    ]


def test_template_section_and_testpaths():
    assert TEMPLATE_PATH.is_file()
    parser = configparser.ConfigParser()
    parser.read(TEMPLATE_PATH, encoding="utf-8")
    assert parser.sections() == ["pytest"]
    assert parser.options("pytest") == ["testpaths"]
    assert parser.get("pytest", "testpaths") == "tests"


def test_repo_root_collects_exact_tests():
    collected = run_collect(ROOT)
    assert len(collected) == 23
    for name in collected:
        assert name.startswith("tests/")
        assert not name.startswith("harness/")
        assert not name.startswith("tools/")


def test_template_limits_collection_and_countercase(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    template_data = TEMPLATE_PATH.read_text(encoding="utf-8")
    ini_file = project / "pytest.ini"
    ini_file.write_text(template_data, encoding="utf-8")

    tests_dir = project / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_sample.py").write_text(
        "def test_sample():\n    assert True\n", encoding="utf-8"
    )

    bait_harness = project / "harness" / "templates" / "examples" / "tests"
    bait_harness.mkdir(parents=True)
    (bait_harness / "test_framework.py").write_text(
        "def test_bait1():\n    assert True\n", encoding="utf-8"
    )

    bait_other = project / "other" / "tests"
    bait_other.mkdir(parents=True)
    (bait_other / "test_other.py").write_text(
        "def test_bait2():\n    assert True\n", encoding="utf-8"
    )

    with_ini = run_collect(project)
    assert with_ini == ["tests/test_sample.py::test_sample"]
    assert not any("bait" in item for item in with_ini)
    assert not any("harness" in item for item in with_ini)
    assert not any("other" in item for item in with_ini)

    ini_file.unlink()
    without_ini = run_collect(project)
    assert any("harness" in item for item in without_ini)
    assert any("other" in item for item in without_ini)
    assert len(without_ini) == 3


def test_explicit_path_runs_outside_testpaths(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    template_data = TEMPLATE_PATH.read_text(encoding="utf-8")
    (project / "pytest.ini").write_text(template_data, encoding="utf-8")

    tests_dir = project / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_sample.py").write_text(
        "def test_sample():\n    assert True\n", encoding="utf-8"
    )

    bait_other = project / "other" / "tests"
    bait_other.mkdir(parents=True)
    (bait_other / "test_other.py").write_text(
        "def test_bait2():\n    assert True\n", encoding="utf-8"
    )

    explicit = run_collect(project, args=["other/tests/test_other.py"])
    assert explicit == ["other/tests/test_other.py::test_bait2"]
