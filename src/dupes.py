from collections import Counter


def find_duplicate_ids(questions: list[dict]) -> list[str]:
    counts = Counter(question["id"].casefold() for question in questions)
    duplicates = {}
    for question in questions:
        original = question["id"]
        normalized = original.casefold()
        if counts[normalized] > 1:
            duplicates.setdefault(normalized, original)
    return list(duplicates.values())
