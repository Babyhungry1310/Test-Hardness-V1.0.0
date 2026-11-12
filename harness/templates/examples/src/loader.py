import json
from pathlib import Path

REQUIRED_FIELDS = {"id", "text", "answer"}


def load_bank(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as handle:
        questions = json.load(handle)
    for question in questions:
        missing = REQUIRED_FIELDS - question.keys()
        if missing:
            raise ValueError(f"{question.get('id', '?')}: missing {sorted(missing)}")
    return questions
