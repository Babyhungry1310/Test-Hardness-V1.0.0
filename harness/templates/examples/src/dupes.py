def find_duplicate_ids(questions: list[dict]) -> list[str]:
    first_seen: dict[str, str] = {}
    duplicates: list[str] = []
    for question in questions:
        key = question["id"].casefold()
        if key not in first_seen:
            first_seen[key] = question["id"]
        elif first_seen[key] not in duplicates:
            duplicates.append(first_seen[key])
    return duplicates
