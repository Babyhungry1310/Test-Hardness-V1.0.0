import json


def load_bank(path):
    with open(path, encoding="utf-8") as source:
        questions = json.load(source)
    required = {"id", "text", "answer"}
    if any(not required.issubset(question) for question in questions):
        raise ValueError("Each question must include id, text, and answer")
    return questions
