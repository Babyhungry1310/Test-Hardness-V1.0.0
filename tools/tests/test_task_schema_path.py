import json
from pathlib import Path

import jsonschema
import pytest

SCHEMA = Path(__file__).resolve().parents[2] / "harness" / "schemas" / "task.schema.json"


def path_validator():
    defs = json.loads(SCHEMA.read_text(encoding="utf-8"))["$defs"]
    return jsonschema.Draft202012Validator({"$defs": defs, "$ref": "#/$defs/path"})


@pytest.mark.parametrize("value", [".github/workflows/verify.yml", "tools/gate.py"])
def test_path_valid(value):
    assert path_validator().is_valid(value)


@pytest.mark.parametrize("value", [".secrets.baseline", ".git/config", "../x"])
def test_path_invalid(value):
    assert not path_validator().is_valid(value)
