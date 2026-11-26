import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gate

AGENT = "conchonomoconmeo-AIAIAI"

FAKE_SCAN = r'''import json, re, sys
t = open(sys.argv[1], encoding="utf-8").read()
hits = [{"rule": "zone3_openai_token"} for _ in re.finditer(r"sk-[A-Za-z0-9_-]{20,}", t, re.I)]
w = [{"rule": "zone2_email"} for _ in re.finditer(r"\w+@example\.invalid", t)]
level = "BLOCK" if hits else ("WARN" if w else "ALLOW")
print(json.dumps({"level": level, "reasons": hits + w}))
'''

SRC = """# SRC

```yaml
id: TK-0099
write_scope:
  - docs/a.md
  - 04_control/decisions/DEC-0001_x.md
  - 04_control/decisions/DEC-0002_y.md
line_budget: 50
verify: >-
  python tools/check_a.py
```
"""

CHECK_A = 'import sys\nsys.exit(0 if open("docs/a.md", encoding="utf-8").read().startswith("ok") else 1)\n'

DEC = """---
id: DEC-0001
---
## Status (newest first)
- 2026-11-20 | ACTIVE
## Context
nội dung
"""


@unittest.skipUnless(subprocess.run(["git", "--version"], capture_output=True).returncode == 0, "cần git")
class GateBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.write("tools/scan.py", FAKE_SCAN)
        self.write("tools/check_a.py", CHECK_A)
        self.write("06_sources/SRC-0003_kaizen-chi-tiet-dot1.md", SRC)
        self.write("docs/a.md", "ok\n")
        self.write("04_control/decisions/DEC-0001_x.md", DEC)
        self.write("04_control/decisions/DEC-0002_y.md", DEC.replace("DEC-0001", "DEC-0002"))
        self.commit("base", AGENT)
        self.git("checkout", "-q", "-b", "task/TK-0099-R1")

    def tearDown(self):
        self.git("checkout", "-q", "main")
        subprocess.run(["git", "-C", str(self.repo), "worktree", "prune"], capture_output=True)
        self.tmp.cleanup()

    def git(self, *args, env=None):
        r = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True, text=True, env=env)
        if r.returncode:
            raise AssertionError(r.stderr)
        return r.stdout.strip()

    def write(self, path, text, raw=None):
        p = self.repo / path
        p.parent.mkdir(parents=True, exist_ok=True)
        if raw is not None:
            p.write_bytes(raw)
        else:
            p.write_text(text, encoding="utf-8", newline="\n")

    def commit(self, msg, author):
        env = dict(os.environ, GIT_AUTHOR_NAME=author, GIT_AUTHOR_EMAIL="x@users.noreply.github.com",
                   GIT_COMMITTER_NAME=author, GIT_COMMITTER_EMAIL="x@users.noreply.github.com")
        self.git("add", "-A")
        self.git("commit", "-qm", msg, env=env)

    def run_gate(self, *extra):
        out = Path(self.tmp.name) / "g.json"
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            rc = gate.main(["--repo", str(self.repo), "--base", "main", "--head", "task/TK-0099-R1",
                            "--task", "TK-0099", "--json-out", str(out), *extra])
        data = json.loads(out.read_text(encoding="utf-8"))
        return rc, {i["check"]: i for i in data["items"]}

    def add_run(self):
        self.write("02_work/runs/TK-0099_R1_DONE.md", "---\ntask: TK-0099\n---\n")


class TestScope(GateBase):
    def test_good_change_passes(self):
        self.write("docs/a.md", "ok mới\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--run-verify")
        self.assertEqual(rc, 0, items)
        self.assertEqual(items["G7"]["level"], "PASS")

    def test_out_of_scope_fails(self):
        self.write("docs/b.md", "lạ\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G1"]["level"], "FAIL")
        self.assertIn("docs/b.md", items["G1"]["msg"])

    def test_rename_counts_one_path(self):
        (self.repo / "04_control/decisions/superseded").mkdir(parents=True, exist_ok=True)
        self.git("mv", "04_control/decisions/DEC-0001_x.md", "04_control/decisions/superseded/DEC-0001_x.md")
        p = self.repo / "04_control/decisions/superseded/DEC-0001_x.md"
        p.write_text(DEC.replace("## Status (newest first)\n", "## Status (newest first)\n- 2026-11-24 | SUPERSEDED_BY DEC-0002\n"), encoding="utf-8", newline="\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--scope", "04_control/decisions/DEC-0001_x.md", "--limit", "1")
        self.assertEqual(items["G1"]["level"], "PASS", items["G1"])
        self.assertEqual(items["G3"]["level"], "PASS", items["G3"])


class TestF50Author(GateBase):
    def test_f50_owner_identity_fails(self):
        self.write("docs/a.md", "ok 2\n")
        self.add_run()
        self.commit("TK-0099", "Real Fork")
        rc, items = self.run_gate()
        self.assertEqual(items["G2"]["level"], "FAIL")
        self.assertIn("Real Fork", items["G2"]["msg"])


class TestLedger(GateBase):
    def test_edit_old_line_fails(self):
        self.write("04_control/decisions/DEC-0001_x.md", DEC.replace("nội dung", "nội dung đã sửa"))
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G3"]["level"], "FAIL")

    def test_allow_edit_keeps_status(self):
        self.write("04_control/decisions/DEC-0001_x.md", DEC.replace("id: DEC-0001", "id: DEC-0001\nsupersedes: \"\"").replace("## Status (newest first)\n", "## Status (newest first)\n- 2026-11-24 | ACTIVE\n"))
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--allow-edit", "04_control/decisions/DEC-0001_x.md")
        self.assertEqual(items["G3"]["level"], "PASS", items["G3"])

    def test_bad_status_grammar_fails(self):
        self.write("04_control/decisions/DEC-0002_y.md", DEC.replace("DEC-0001", "DEC-0002").replace("## Status (newest first)\n", "## Status (newest first)\n- 2026-11-24 | ACCEPTED\n"))
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G3"]["level"], "FAIL")
        self.assertIn("ACCEPTED", items["G3"]["msg"])


class TestEncoding(GateBase):
    def test_crlf_and_bom_fail(self):
        self.write("docs/a.md", None, raw=b"\xef\xbb\xbfok\r\nhai\r\n")
        self.add_run()
        self.git("config", "core.autocrlf", "false")
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G4"]["level"], "FAIL")
        self.assertIn("BOM", items["G4"]["msg"])
        self.assertIn("CRLF", items["G4"]["msg"])


class TestF24Utf16(GateBase):
    def setUp(self):
        super().setUp()
        self.git("config", "core.autocrlf", "false")

    def test_utf16_with_bom_fails(self):
        self.write("docs/a.md", None, raw="ok\nhai\n".encode("utf-16"))
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G4"]["level"], "FAIL")
        self.assertIn("UTF-16", items["G4"]["msg"])

    def test_utf16_without_bom_fails(self):
        self.write("docs/a.md", None, raw="ok\nhai\n".encode("utf-16-le"))
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G4"]["level"], "FAIL")
        self.assertIn("NUL", items["G4"]["msg"])

    def test_cp1258_not_utf8_fails(self):
        self.write("docs/a.md", None, raw="ok \xe0\xe1\n".encode("latin-1"))
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G4"]["level"], "FAIL")
        self.assertIn("UTF-8", items["G4"]["msg"])

    def test_clean_utf8_passes(self):
        self.write("docs/a.md", "ok tiếng Việt → đạt\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G4"]["level"], "PASS", items["G4"])


class TestScan(GateBase):
    TOKEN_LINE = "xem RSK-0004_agent-tag-and-merge-bypass\n"

    def test_block_fails(self):
        self.write("docs/a.md", "ok\n" + self.TOKEN_LINE)
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G5"]["level"], "FAIL")

    def test_f48_exact_accept_passes(self):
        self.write("docs/a.md", "ok\n" + self.TOKEN_LINE)
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--accept-scan", "docs/a.md=zone3_openai_token:1")
        self.assertEqual(items["G5"]["level"], "PASS", items["G5"])

    def test_f48_extra_hit_fails(self):
        self.write("docs/a.md", "ok\n" + self.TOKEN_LINE * 2)
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--accept-scan", "docs/a.md=zone3_openai_token:1")
        self.assertEqual(items["G5"]["level"], "FAIL")

    def test_scan_warn_is_gate_warn(self):
        self.write("docs/a.md", "ok t@example.invalid\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G5"]["level"], "WARN")

    def test_scan_uses_base_tools_not_head(self):
        self.write("tools/scan.py", 'print(\'{"level": "ALLOW", "reasons": []}\')\n')
        self.write("docs/a.md", "ok\n" + self.TOKEN_LINE)
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--scope", "docs/a.md", "tools/scan.py")
        self.assertEqual(items["G5"]["level"], "FAIL")


class TestFrozenAndVerify(GateBase):
    def test_frozen_hash_mismatch_fails(self):
        self.write("docs/a.md", "ok khác bản nháp\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        want = hashlib.sha256("ok bản nháp\n".encode("utf-8")).hexdigest()[:12]
        rc, items = self.run_gate("--frozen", f"docs/a.md={want}")
        self.assertEqual(items["G6"]["level"], "FAIL")

    def test_frozen_hash_match_passes(self):
        body = "ok bản nháp\n"
        self.write("docs/a.md", body)
        self.add_run()
        self.commit("TK-0099", AGENT)
        want = hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]
        rc, items = self.run_gate("--frozen", f"docs/a.md={want}")
        self.assertEqual(items["G6"]["level"], "PASS")

    def test_verify_failure_fails(self):
        self.write("docs/a.md", "hỏng\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--run-verify")
        self.assertEqual(items["G7"]["level"], "FAIL")
        self.assertEqual(rc, 1)


RUN_SCHEMA = '{"type": "object", "required": ["task", "outcome"], "properties": {"done_check": {"type": "array", "items": {"pattern": "^[1-9]\\\\d* \u2192 \\\\S.*$"}}}}'


class TestRunSchema(GateBase):
    def setUp(self):
        super().setUp()
        self.git("checkout", "-q", "main")
        self.write("harness/schemas/run.schema.json", RUN_SCHEMA)
        self.commit("schema", AGENT)
        self.git("checkout", "-q", "task/TK-0099-R1")
        self.git("rebase", "-q", "main")

    def test_f56_mojibake_arrow_fails(self):
        self.write("docs/a.md", "ok 4\n")
        self.write("02_work/runs/TK-0099_R1_DONE.md", "---\ntask: TK-0099\noutcome: DONE\ndone_check:\n  - \"1 \u00e2\u2020\u2019 docs/a.md\"\n---\n")
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G10"]["level"], "FAIL")

    def test_good_run_passes(self):
        self.write("docs/a.md", "ok 5\n")
        self.write("02_work/runs/TK-0099_R1_DONE.md", "---\ntask: TK-0099\noutcome: DONE\ndone_check:\n  - \"1 \u2192 docs/a.md\"\n---\n")
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G10"]["level"], "PASS", items["G10"])


class TestWindowsConsole(GateBase):
    def test_cp1252_stdout_does_not_crash(self):
        self.write("docs/a.md", "ok 6\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        raw = io.BytesIO()
        fake = io.TextIOWrapper(raw, encoding="cp1252")
        old = sys.stdout
        sys.stdout = fake
        try:
            rc = gate.main(["--repo", str(self.repo), "--base", "main", "--head", "task/TK-0099-R1", "--task", "TK-0099"])
            fake.flush()
        finally:
            sys.stdout = old
        self.assertEqual(rc, 0)
        self.assertIn("ĐẠT", raw.getvalue().decode("utf-8"))


EMAIL = "t" + "@example.invalid"
RULES_JSON = '{"ruleset": "t", "rules": [{"rule": "zone3_openai_token", "level": "BLOCK"}, {"rule": "zone2_email", "level": "WARN"}]}'


class TestV5ScanDelta(GateBase):
    TOKEN_LINE = TestScan.TOKEN_LINE

    def base_has(self, text, rules=False):
        self.git("checkout", "-q", "main")
        self.write("docs/a.md", text)
        if rules:
            self.write("tools/scan_rules.json", RULES_JSON)
        self.commit("base hit", AGENT)
        self.git("checkout", "-q", "task/TK-0099-R1")
        self.git("rebase", "-q", "main")

    def test_inherited_hit_passes(self):
        self.base_has("ok\n" + self.TOKEN_LINE)
        self.write("docs/a.md", "ok\n" + self.TOKEN_LINE + "dòng mới\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G5"]["level"], "PASS", items["G5"])
        self.assertIn("kế thừa 1, mới 0", items["G5"]["msg"])

    def test_inherited_plus_new_fails(self):
        self.base_has("ok\n" + self.TOKEN_LINE)
        self.write("docs/a.md", "ok\n" + self.TOKEN_LINE * 2)
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G5"]["level"], "FAIL")
        self.assertIn("kế thừa 1, mới 1", items["G5"]["msg"])

    def test_renamed_file_inherits_from_old_path(self):
        self.base_has("ok\n" + self.TOKEN_LINE)
        self.git("mv", "docs/a.md", "docs/c.md")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--scope", "docs/a.md")
        self.assertEqual(items["G5"]["level"], "PASS", items["G5"])

    def test_new_warn_rule_on_inherited_block_is_warn(self):
        self.base_has("ok\n" + self.TOKEN_LINE, rules=True)
        self.write("docs/a.md", "ok\n" + self.TOKEN_LINE + "liên hệ " + EMAIL + "\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G5"]["level"], "WARN", items["G5"])
        self.assertIn("zone2_email:1", items["G5"]["msg"])


class TestV5MultiAccept(GateBase):
    def setUp(self):
        super().setUp()
        self.write("docs/a.md", "ok\n" + TestScan.TOKEN_LINE + "liên hệ " + EMAIL + "\n")
        self.add_run()
        self.commit("TK-0099", AGENT)

    def test_all_rules_exact_passes(self):
        rc, items = self.run_gate("--accept-scan", "docs/a.md=zone3_openai_token:1", "--accept-scan", "docs/a.md=zone2_email:1")
        self.assertEqual(items["G5"]["level"], "PASS", items["G5"])
        self.assertIn("OWNER chấp nhận", items["G5"]["msg"])

    def test_missing_rule_fails(self):
        rc, items = self.run_gate("--accept-scan", "docs/a.md=zone3_openai_token:1")
        self.assertEqual(items["G5"]["level"], "FAIL")

    def test_wrong_count_fails(self):
        rc, items = self.run_gate("--accept-scan", "docs/a.md=zone3_openai_token:1", "--accept-scan", "docs/a.md=zone2_email:2")
        self.assertEqual(items["G5"]["level"], "FAIL")

    def test_path_not_in_diff_fails(self):
        rc, items = self.run_gate("--accept-scan", "docs/a.md=zone3_openai_token:1", "--accept-scan", "docs/a.md=zone2_email:1",
                                  "--accept-scan", "docs/khong_co.md=zone2_email:1")
        self.assertEqual(items["G5"]["level"], "FAIL")
        self.assertIn("docs/khong_co.md", items["G5"]["msg"])

    def test_duplicate_rule_is_usage_error(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = gate.main(["--repo", str(self.repo), "--base", "main", "--head", "task/TK-0099-R1", "--task", "TK-0099",
                            "--accept-scan", "docs/a.md=zone2_email:1", "--accept-scan", "docs/a.md=zone2_email:1"])
        self.assertEqual(rc, 2)


class TestV5AnsiEvidence(GateBase):
    def test_ansi_in_evidence_warns(self):
        self.write("docs/a.md", "ok 7\n")
        self.write("03_output/CYC-08/checks/TK-0099_R1_L01_verify.txt", "\x1b[32m3 passed\x1b[0m\nEXIT_CODE=0\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G4"]["level"], "WARN", items["G4"])
        self.assertIn("ANSI", items["G4"]["msg"])

    def test_plain_evidence_passes(self):
        self.write("docs/a.md", "ok 8\n")
        self.write("03_output/CYC-08/checks/TK-0099_R1_L01_verify.txt", "3 passed\nEXIT_CODE=0\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G4"]["level"], "PASS", items["G4"])


PASSING = "def test_ok():\n    assert True\n"
FAILING = "def test_bad():\n    assert False\n"


@unittest.skipUnless(importlib.util.find_spec("pytest") is not None, "cần pytest")
class TestV5ToolsTests(GateBase):
    def base_tests(self, **files):
        self.git("checkout", "-q", "main")
        for name, body in files.items():
            self.write(f"tools/tests/{name}.py", body)
        self.commit("base tests", AGENT)
        self.git("checkout", "-q", "task/TK-0099-R1")
        self.git("rebase", "-q", "main")

    def test_no_tools_change_no_g11(self):
        self.write("docs/a.md", "ok 9\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--run-tools-tests")
        self.assertNotIn("G11", items)

    def test_tools_change_without_flag_warns(self):
        self.write("tools/check_a.py", CHECK_A + "# đổi\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate()
        self.assertEqual(items["G11"]["level"], "WARN", items["G11"])

    def test_new_failure_fails(self):
        self.base_tests(test_ok=PASSING)
        self.write("tools/tests/test_new.py", FAILING)
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--run-tools-tests")
        self.assertEqual(items["G11"]["level"], "FAIL", items["G11"])
        self.assertIn("test_new.py::test_bad", items["G11"]["msg"])

    def test_inherited_failure_passes(self):
        self.base_tests(test_ok=PASSING, test_old=FAILING)
        self.write("tools/check_a.py", CHECK_A + "# đổi\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--run-tools-tests")
        self.assertEqual(items["G11"]["level"], "PASS", items["G11"])
        self.assertIn("kế thừa 1", items["G11"]["msg"])

    def test_collection_error_new_fails(self):
        self.base_tests(test_ok=PASSING)
        self.write("tools/tests/test_broken.py", "import khong_co_module_nay\n")
        self.add_run()
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--run-tools-tests")
        self.assertEqual(items["G11"]["level"], "FAIL", items["G11"])
        self.assertIn("test_broken.py", items["G11"]["msg"])


class TestRunFile(GateBase):
    def test_task_branch_without_run_fails(self):
        self.write("docs/a.md", "ok 3\n")
        self.commit("TK-0099", AGENT)
        rc, items = self.run_gate("--branch", "task/TK-0099-R1")
        self.assertEqual(items["G9"]["level"], "FAIL")


if __name__ == "__main__":
    unittest.main()
