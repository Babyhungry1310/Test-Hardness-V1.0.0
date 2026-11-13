import json
import subprocess
import sys

from src.handout import build_handout


def test_build_handout_exact_layout():
    questions = [
        {"id": "Q-001", "text": "Câu hỏi", "answer": "Đáp án"},
        {"id": "Q-002", "text": "Câu hai", "answer": "Hai"},
    ]
    assert build_handout(questions) == (
        "# Handout\n\n"
        "## Q-001\n\nCâu hỏi\n\n**Đáp án:** Đáp án\n\n"
        "## Q-002\n\nCâu hai\n\n**Đáp án:** Hai\n"
    )


def test_build_handout_preserves_unicode_and_multiline_text():
    questions = [{"id": "Q-đ", "text": "Dòng một\nDòng hai 🌱", "answer": "Đáp án\nchi tiết"}]
    assert build_handout(questions) == (
        "# Handout\n\n## Q-đ\n\nDòng một\nDòng hai 🌱\n\n"
        "**Đáp án:** Đáp án\nchi tiết\n"
    )


def test_build_handout_empty_bank():
    assert build_handout([]) == "# Handout\n"


def test_cli_writes_real_bank_with_five_ids(tmp_path):
    output = tmp_path / "handout.md"
    result = subprocess.run(
        [sys.executable, "-m", "src.handout", "data/bank.json", str(output)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    content = output.read_text(encoding="utf-8")
    assert content.count("## Q-") == 5
    assert [f"## Q-{number:03}" in content for number in range(1, 6)] == [True] * 5


def test_cli_duplicate_casefold_reports_ids_and_does_not_write(tmp_path):
    bank = tmp_path / "bank.json"
    output = tmp_path / "result.md"
    bank.write_text(json.dumps([
        {"id": "Q-001", "text": "a", "answer": "b"},
        {"id": "q-001", "text": "c", "answer": "d"},
    ]), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "src.handout", str(bank), str(output)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "Q-001" in result.stderr
    assert not output.exists()


def test_cli_rejects_non_markdown_suffix_without_output(tmp_path):
    bank = tmp_path / "bank.json"
    output = tmp_path / "result.txt"
    bank.write_text(json.dumps([
        {"id": "Q-001", "text": "a", "answer": "b"},
    ]), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "src.handout", str(bank), str(output)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stderr
    assert not output.exists()
