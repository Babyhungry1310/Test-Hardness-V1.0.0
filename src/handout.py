import sys

from .dupes import find_duplicate_ids
from .loader import load_bank


def build_handout(questions):
    sections = ["# Handout"]
    for question in questions:
        sections.append(
            f"## {question['id']}\n\n"
            f"{question['text']}\n\n"
            f"**Đáp án:** {question['answer']}"
        )
    return "\n\n".join(sections).rstrip("\n") + "\n"


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("usage: python -m src.handout <bank.json> <handout.md>", file=sys.stderr)
        return 2
    bank_path, output_path = args
    if not output_path.endswith(".md"):
        print("output path must end with .md", file=sys.stderr)
        return 2
    questions = load_bank(bank_path)
    duplicates = find_duplicate_ids(questions)
    if duplicates:
        for question_id in duplicates:
            print(f"Duplicate id: {question_id}", file=sys.stderr)
        return 1
    with open(output_path, "w", encoding="utf-8", newline="\n") as output:
        output.write(build_handout(questions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
