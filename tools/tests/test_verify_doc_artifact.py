"""Test cho tools/verify_doc_artifact.py — gồm test đối chứng dương cho từng phép kiểm.

Chạy: python -m unittest discover -s tests -v
"""
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import verify_doc_artifact as v  # noqa: E402

DOC = """# SRC-0003

Phiên bản: P6

## Bảng truy vết

| E | Task |
| --- | --- |
| E20 | TK-0042 |
| E22 | TK-0055 |

Xem [H0](upstream/00.md).
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.cwd = os.getcwd()
        os.chdir(self.tmp)
        Path("upstream").mkdir()
        Path("upstream/00.md").write_text("# H0\n", encoding="utf-8")
        Path("SRC.md").write_text(DOC, encoding="utf-8", newline="\n")

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_v(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = v.main([*argv, "--json"])
        return code, json.loads(buf.getvalue())

    @staticmethod
    def rules(res):
        return {f["rule"] for f in res.get("findings", [])}


class TestVerifyDoc(Base):
    def test_good_doc_passes(self):
        code, res = self.run_v("SRC.md", "--contains", "Phiên bản: P6",
                               "--heading", "Bảng truy vết", "--regex", r"^\| E22 \| TK-0055 \|$")
        self.assertEqual(code, 0, res)

    def test_contains_regex_heading_fail(self):
        code, res = self.run_v("SRC.md", "--contains", "Phiên bản: P7",
                               "--heading", "Không có", "--regex", r"^\| E99 ")
        self.assertEqual(code, 1)
        self.assertEqual({"CONTAINS", "HEADING", "REGEX"}, self.rules(res))

    def test_missing_file(self):
        code, res = self.run_v("NOPE.md")
        self.assertEqual(code, 1)
        self.assertIn("MISSING_FILE", self.rules(res))

    def test_secret_and_personal_path(self):
        Path("SRC.md").write_text(DOC + "\nC:\\Users\\owner\\repo\ntoken ghp_" + "a" * 36 + "\n", encoding="utf-8")
        code, res = self.run_v("SRC.md")
        self.assertEqual(code, 1)
        self.assertIn("FORBIDDEN:WINDOWS_USER_PATH", self.rules(res))
        self.assertIn("FORBIDDEN:GITHUB_TOKEN", self.rules(res))

    def test_broken_link_and_table(self):
        Path("SRC.md").write_text(DOC.replace("upstream/00.md", "upstream/99.md")
                                  + "\n| a | b |\n| --- | --- |\n| 1 | 2 | 3 |\n", encoding="utf-8")
        code, res = self.run_v("SRC.md")
        self.assertEqual({"BROKEN_LINK", "TABLE_COLUMNS"}, self.rules(res))

    def test_table_escaped_pipe_and_code_ok(self):
        Path("T.md").write_text("| a | b |\n| --- | --- |\n| `x|y` | c \\| d |\n", encoding="utf-8")
        code, res = self.run_v("T.md")
        self.assertEqual(code, 0, res)

    def test_sha256_and_same_as(self):
        h = hashlib.sha256(Path("SRC.md").read_bytes()).hexdigest()
        self.assertEqual(self.run_v("SRC.md", "--sha256", f"SRC.md={h}")[0], 0)
        code, res = self.run_v("SRC.md", "--sha256", "SRC.md=" + "0" * 64)
        self.assertIn("SHA256", self.rules(res))
        shutil.copy("SRC.md", "COPY.md")
        self.assertEqual(self.run_v("--same-as", "COPY.md=SRC.md")[0], 0)
        Path("COPY.md").write_text(DOC + "x", encoding="utf-8")
        code, res = self.run_v("--same-as", "COPY.md=SRC.md")
        self.assertIn("SAME_AS", self.rules(res))

    def test_max_words(self):
        code, res = self.run_v("SRC.md", "--max-words", "5")
        self.assertIn("MAX_WORDS", self.rules(res))

    def test_no_input_66(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(v.main([]), 66)

    def test_bad_sha_arg_is_usage_error(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(v.main(["SRC.md", "--sha256", "SRC.md=xyz"]), 2)


@unittest.skipUnless(shutil.which("git"), "cần git")
class TestAppendOnly(Base):
    def git(self, *a):
        subprocess.run(["git", *a], check=True, capture_output=True)

    def setUp(self):
        super().setUp()
        self.git("init", "-q")
        self.git("config", "user.email", "t@example.invalid")
        self.git("config", "user.name", "t")
        Path("LEDGER.md").write_text("| ID | Trạng thái |\n| --- | --- |\n| DEC-0031 | ACTIVE |\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "base")

    def test_append_passes(self):
        with open("LEDGER.md", "a", encoding="utf-8") as f:
            f.write("| DEC-0032 | ACTIVE |\n")
        self.assertEqual(self.run_v("LEDGER.md", "--append-only-vs", "HEAD")[0], 0)

    def test_edit_fails(self):
        Path("LEDGER.md").write_text("| ID | Trạng thái |\n| --- | --- |\n| DEC-0031 | RETIRED |\n", encoding="utf-8")
        code, res = self.run_v("LEDGER.md", "--append-only-vs", "HEAD")
        self.assertEqual(code, 1)
        self.assertIn("APPEND_ONLY", self.rules(res))


if __name__ == "__main__":
    unittest.main()
