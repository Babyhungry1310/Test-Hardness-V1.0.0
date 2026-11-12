import json
from pathlib import Path

from src.dupes import find_duplicate_ids

BANK = Path(__file__).resolve().parent.parent / "data" / "bank.json"


def test_no_duplicates():
    assert find_duplicate_ids([{"id": "A"}, {"id": "B"}]) == []


def test_exact_duplicate():
    assert find_duplicate_ids([{"id": "A"}, {"id": "A"}, {"id": "A"}]) == ["A"]


def test_case_insensitive_duplicate():
    assert find_duplicate_ids([{"id": "Q-1"}, {"id": "q-1"}]) == ["Q-1"]


def test_bank_has_two_duplicates():
    questions = json.loads(BANK.read_text(encoding="utf-8"))
    assert find_duplicate_ids(questions) == ["Q-001", "Q-002"]
