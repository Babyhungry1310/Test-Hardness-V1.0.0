"""Test cho tools/validate_task_schema.py (chỉ dùng unittest).

Chạy: python -m unittest discover -s tests -v
Gồm test đối chứng dương: tái hiện 4 lỗi của P6b, kiểm phải FAIL đúng luật.
"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_task_schema as v  # noqa: E402

GOOD = """# Kế hoạch mẫu

```yaml
id: TK-0057
batch: B1b
branch: lead/TK-0057-src0003-p6
goal: Nạp SRC-0003 P6 và DEC-0032
write_scope:
  - 06_sources/SRC-0003.md
  - 02_decisions/DEC-0032.md
depends_on: [TK-0038]
verify: python tools/validate_task_schema.py 06_sources/SRC-0003.md
```

```yaml
id: TK-0058
batch: B1c
branch: lead/TK-0058-sync-upstream
goal: Đồng bộ H0–H2 vào 05_memory/upstream/
write_scope: [05_memory/upstream/00_tong_quan_upstream.md, 05_memory/upstream/01_brainstorm.md]
depends_on:
  - TK-0057
verify: |
  python tools/validate_task_schema.py PLAN.md
  git diff --stat
```

```yaml
id: TK-0039
batch: B2a
branch: upgrade/TK-0039-state
goal: Sửa STATE
write_scope: [harness/STATE.md]
depends_on: [TK-0058]
verify: python -m unittest
```
"""

# Tái hiện P6b: hậu tố chữ, thiếu trường, wildcard + văn xuôi, depends_on gãy.
P6B = """```yaml
id: TK-0053b
batch: B1b
goal: Đồng bộ tài liệu upstream
write_scope:
  - 05_memory/upstream/0x_*.md
  - các file H0–H4 còn lại nếu cần
depends_on: [TK-0053]
```

```yaml
id: TK-0053c
batch: B1b
write_scope: [06_sources/SRC-0003.md]
depends_on: [TK-0053b]
```

```yaml
id: TK-0039
batch: B2a
branch: upgrade/TK-0039-state
goal: Sửa STATE
write_scope: [harness/STATE.md]
depends_on: [TK-0053d]
verify: python -m unittest
```
"""


def run(text, *extra, use_yaml=True):
    with tempfile.TemporaryDirectory() as tmp:
        plan = Path(tmp) / "PLAN.md"
        plan.write_text(text, encoding="utf-8")
        known = Path(tmp) / "ledger.md"
        known.write_text("TK-0036 TK-0037 TK-0038 merged\n", encoding="utf-8")
        argv = [str(plan), "--known-ids", str(known), "--json", *extra]
        if not use_yaml:
            argv.append("--no-yaml")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = v.main(argv)
        return code, json.loads(buf.getvalue())


def rules(result):
    return {f["rule"] for f in result.get("findings", [])}


class TestValidator(unittest.TestCase):
    def test_good_plan_passes_both_parsers(self):
        for use_yaml in (True, False):
            code, res = run(GOOD, use_yaml=use_yaml)
            self.assertEqual(code, 0, res)
            self.assertEqual(res["cards"], 3)

    def test_p6b_fails_with_all_four_error_classes(self):
        for use_yaml in (True, False):
            code, res = run(P6B, use_yaml=use_yaml)
            self.assertEqual(code, 1)
            got = rules(res)
            self.assertIn("ID_FORMAT", got)        # lỗi 1: TK-0053b
            self.assertIn("MISSING_FIELD", got)    # lỗi 2: thiếu branch/goal/verify
            self.assertIn("SCOPE_GLOB", got)       # lỗi 3: wildcard
            self.assertIn("SCOPE_PROSE", got)      # lỗi 3: văn xuôi
            self.assertIn("DEP_FORMAT", got)       # lỗi 4: phụ thuộc TK-0053b/…d
            self.assertIn("DEP_UNKNOWN", got)      # lỗi 4: TK-0053 không có thẻ, không có trong sổ

    def test_scope_over_cap(self):
        text = GOOD.replace(
            "write_scope: [harness/STATE.md]",
            "write_scope: [a.md, b.md, c.md, d.md, e.md, f.md]",
        )
        code, res = run(text)
        self.assertEqual(code, 1)
        self.assertIn("SCOPE_COUNT", rules(res))

    def test_cycle_detected(self):
        text = GOOD.replace("depends_on: [TK-0038]", "depends_on: [TK-0039]")
        code, res = run(text)
        self.assertEqual(code, 1)
        self.assertIn("DEP_CYCLE", rules(res))

    def test_overlap_in_same_batch(self):
        text = GOOD.replace("batch: B1c", "batch: B1b").replace(
            "05_memory/upstream/01_brainstorm.md", "06_sources/SRC-0003.md")
        code, res = run(text)
        self.assertIn("SCOPE_OVERLAP", rules(res))

    def test_no_cards_returns_66(self):
        code, res = run("# Kế hoạch trống\n\nChưa có thẻ.\n")
        self.assertEqual(code, 66)
        self.assertEqual(res["status"], "NO_INPUT")

    def test_bad_branch_and_backslash_path(self):
        text = GOOD.replace("branch: upgrade/TK-0039-state", "branch: feature/x").replace(
            "write_scope: [harness/STATE.md]", 'write_scope: ["harness\\\\STATE.md"]')
        code, res = run(text)
        got = rules(res)
        self.assertIn("BRANCH_PREFIX", got)
        self.assertIn("SCOPE_PATH", got)

    def test_schema_file_overrides_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            schema = Path(tmp) / "task.schema.json"
            schema.write_text(json.dumps({
                "type": "object",
                "required": ["id", "goal", "owner_action"],
                "properties": {"id": {"type": "string", "pattern": "^TK-\\d{4}$"}},
            }), encoding="utf-8")
            code, res = run(GOOD, "--schema", str(schema))
            self.assertEqual(code, 1)
            msgs = " ".join(f["message"] for f in res["findings"])
            self.assertIn("owner_action", msgs)


class TestSchemaEmpty(unittest.TestCase):
    """Báo sai đã gặp ở HANDOFF_P6D: `fixes: ""` hợp lệ theo schema thì không được báo thiếu."""

    def test_empty_fixes_allowed_by_schema_pattern(self):
        card = ('```yaml\nid: TK-0039\ngoal: Sửa STATE\nwrite_scope: [harness/STATE.md]\n'
                'depends_on: []\nfixes: ""\n```\n')
        with tempfile.TemporaryDirectory() as tmp:
            schema = Path(tmp) / "task.schema.json"
            schema.write_text(json.dumps({
                "type": "object",
                "required": ["id", "goal", "fixes"],
                "properties": {
                    "id": {"type": "string", "pattern": "^TK-\\d{4}$"},
                    "fixes": {"type": "string", "pattern": "^(?:TK-\\d{4})?$"},
                    "goal": {"type": "string", "minLength": 1},
                },
            }), encoding="utf-8")
            code, res = run(card, "--schema", str(schema))
            msgs = [f["message"] for f in res.get("findings", [])]
            self.assertFalse(any("'fixes'" in m for m in msgs), msgs)
            # goal rỗng vẫn phải bị bắt (minLength 1)
            code, res = run(card.replace("goal: Sửa STATE", 'goal: ""'), "--schema", str(schema))
            self.assertTrue(any("'goal' rỗng" in f["message"] for f in res["findings"]))


if __name__ == "__main__":
    unittest.main()
