from copy import deepcopy

import pytest

from src.dupes import find_duplicate_ids


@pytest.mark.parametrize(
    ("identifiers", "expected"),
    [
        ([], []),
        (["Q-001"], []),
        (["Q-001", "Q-002", "Q-003"], []),
        (["Q-001", "Q-001"], ["Q-001"]),
        (["q-001", "Q-001"], ["q-001"]),
        (["Q-001", "q-001", "Q-001", "q-001"], ["Q-001"]),
        (["q-002", "Q-001", "q-001", "Q-002"], ["q-002", "Q-001"]),
        (["Q-003", "q-002", "Q-001", "q-001", "Q-002"], ["q-002", "Q-001"]),
    ],
)
def test_duplicate_ids(identifiers, expected):
    questions = [
        {"id": identifier, "text": "Sample question", "answer": "A"}
        for identifier in identifiers
    ]
    before = deepcopy(questions)

    assert find_duplicate_ids(questions) == expected
    assert questions == before
