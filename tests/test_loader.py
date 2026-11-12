import json
from pathlib import Path

import pytest

from src.loader import load_bank


def test_repository_bank():
    path = Path(__file__).resolve().parents[1] / "data" / "bank.json"
    expected = json.loads(path.read_text(encoding="utf-8"))

    assert isinstance(expected, list)
    assert [question["id"] for question in expected] == [
        f"Q-{number:03d}" for number in range(1, 6)
    ]
    assert all(set(question) == {"id", "text", "answer"} for question in expected)
    assert all(isinstance(value, str) and value for question in expected for value in question.values())
    assert load_bank(path) == expected


def test_preserves_file_order_and_unicode(tmp_path):
    questions = [
        {"id": identifier, "text": "Độ cứng", "answer": "Chống vết lõm"}
        for identifier in ["Q-003", "Q-001", "Q-002"]
    ]
    path = tmp_path / "questions.json"
    path.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")

    assert load_bank(str(path)) == questions


@pytest.mark.parametrize("missing", ["id", "text", "answer"])
def test_missing_required_field_raises_value_error(tmp_path, missing):
    questions = [
        {"id": "Q-001", "text": "Sample question", "answer": "A"},
        {"id": "Q-002", "text": "Another question", "answer": "B"},
    ]
    del questions[1][missing]
    path = tmp_path / "incomplete.json"
    path.write_text(json.dumps(questions), encoding="utf-8")

    with pytest.raises(ValueError):
        load_bank(path)
