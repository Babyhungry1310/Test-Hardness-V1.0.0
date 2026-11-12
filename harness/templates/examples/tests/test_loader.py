import json
from pathlib import Path

import pytest

from src.loader import load_bank

BANK = Path(__file__).resolve().parent.parent / "data" / "bank.json"


def test_loads_all_questions():
    assert len(load_bank(BANK)) == 5


def test_keeps_order():
    assert [question["id"] for question in load_bank(BANK)][:2] == ["Q-001", "Q-002"]


def test_rejects_missing_field(tmp_path):
    path = tmp_path / "bank.json"
    path.write_text(json.dumps([{"id": "Q-9", "text": "?"}]), encoding="utf-8")
    with pytest.raises(ValueError):
        load_bank(path)
