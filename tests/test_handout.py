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


def test_build_handout_final_answer_ends_with_one_lf():
    for trailing in ("", "\n", "\n\n"):
        questions = [
            {"id": "Q-001", "text": "Dòng một\nDòng hai", "answer": "Trước\n\n"},
            {"id": "Q-002", "text": "Câu hai", "answer": "Sau\nchi tiết" + trailing},
        ]
        result = build_handout(questions)
        assert result == (
            "# Handout\n\n## Q-001\n\nDòng một\nDòng hai\n\n"
            "**Đáp án:** Trước\n\n\n\n## Q-002\n\nCâu hai\n\n"
            "**Đáp án:** Sau\nchi tiết\n"
        )


def test_cli_multiline_output_preserves_lf_bytes(tmp_path):
    bank = tmp_path / "bank.json"
    output = tmp_path / "result.md"
    questions = [{"id": "Q-001", "text": "Một\nHai", "answer": "Ba\nBốn\n\n"}]
    bank.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "src.handout", str(bank), str(output)],
        capture_output=True,
    )
    assert result.returncode == 0
    assert output.read_bytes() == (
        "# Handout\n\n## Q-001\n\nMột\nHai\n\n**Đáp án:** Ba\nBốn\n".encode("utf-8")
    )


def test_cli_real_bank_ends_with_one_lf_byte(tmp_path):
    output = tmp_path / "handout.md"
    result = subprocess.run(
        [sys.executable, "-m", "src.handout", "data/bank.json", str(output)],
        capture_output=True,
    )
    assert result.returncode == 0
    assert output.read_bytes().endswith(b"\n")
    assert not output.read_bytes().endswith(b"\n\n")


def test_output_open_uses_explicit_lf_on_all_platforms(tmp_path, monkeypatch):
    import builtins

    from src.handout import main

    output = tmp_path / "handout.md"
    real_open = builtins.open
    output_newlines = []

    def recording_open(file, *args, **kwargs):
        if str(file) == str(output):
            output_newlines.append(kwargs.get("newline"))
        return real_open(file, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", recording_open)
    assert main(["data/bank.json", str(output)]) == 0
    assert output_newlines == ["\n"]
    assert output.read_bytes().endswith(b"\n")
