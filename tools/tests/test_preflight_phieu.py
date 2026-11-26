import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import preflight_phieu as pf

MUC_LUC = """# Mục lục

## 1. Nguồn chuẩn

| Loại | File chuẩn | Ngày | Ghi chú |
| --- | --- | --- | --- |
| Kế hoạch | `../DSG update/KE_HOACH_KAIZEN.md` | 2026-11-22 | |
| GSD | `../DSG update/GSD_CORE_DE_XUAT_KAIZEN.md` | 2026-11-22 | |

## 3. File cũ

| File | Thay bởi | Ghi chú |
| --- | --- | --- |
| `../KE_HOACH_KAIZEN.md` | `../DSG update/KE_HOACH_KAIZEN.md` | |

## 4. File trùng tên

| Tên | Các vị trí | Bản chuẩn |
| --- | --- | --- |
| `KE_HOACH_KAIZEN.md` | `../`, `../DSG update/` | `../DSG update/` |
| `GSD_CORE_DE_XUAT_KAIZEN.md` | `../DSG update/`, `P6D/x/` | `../DSG update/` |
"""

SRC = """# SRC

```yaml
id: TK-0058
write_scope:
  - 06_sources/SRC-0008_gsd.md
line_budget: 150
verify: >-
  python tools/verify_doc_artifact.py 06_sources/SRC-0008_gsd.md
  --regex "^xong$"
```

```yaml
id: TK-0040
write_scope:
  - a.md
line_budget: 50
verify: >-
  python tools/x.py
done_when:
  - "H0 nhom E co trang thai theo O2.1"
```

```yaml
id: TK-0039
write_scope:
  - a.md
  - b.md
  - c.md
  - d.md
  - e.md
  - f.md
line_budget: 50
verify: >-
  python tools/missing_tool.py a.md
```
"""

FAKE_SCAN = r'''import json, re, sys
t = open(sys.argv[1], encoding="utf-8").read()
hits = [{"rule": "zone3_openai_token"} for _ in re.finditer(r"sk-[A-Za-z0-9_-]{20,}", t, re.I)]
q = [{"rule": "dangerous_automerge"} for _ in re.finditer(r"bật\s+auto-merge", t)]
level = "BLOCK" if hits else ("QUARANTINE" if q else "ALLOW")
print(json.dumps({"level": level, "reasons": hits + q}))
'''

FRAME = """TỪ: LEAD → ĐẾN: WORKER     LOẠI: GIAO
MÃ: {task}     REF: origin/main @ {ref}
CẦN LÀM: {can_lam}
DỪNG KHI: lỗi     TRẢ LỜI: BẮT BUỘC
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        (self.d / "MUC_LUC.md").write_text(MUC_LUC, encoding="utf-8", newline="\n")
        (self.d / "SRC.md").write_text(SRC, encoding="utf-8", newline="\n")
        (self.d / "scan.py").write_text(FAKE_SCAN, encoding="utf-8", newline="\n")
        self.dsg = self.d / "DSG update"
        self.dsg.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def phieu(self, text, name="GIAO.md"):
        p = self.d / name
        p.write_text(text, encoding="utf-8", newline="\n")
        return p

    def run_pf(self, phieu, *extra):
        out = self.d / "out.json"
        rc = pf.main([str(phieu), "--muc-luc", str(self.d / "MUC_LUC.md"), "--card", str(self.d / "SRC.md"),
                      "--scan-cmd", f"{sys.executable} {self.d / 'scan.py'}", "--json-out", str(out), *extra])
        data = json.loads(out.read_text(encoding="utf-8"))
        return rc, {i["check"]: i for i in data["items"]}


class TestF41Source(Base):
    def test_f41_parent_folder_source_fails(self):
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Nạp bản 2026-11-22 (00, 01, KE_HOACH_KAIZEN.md) — đã thấy cả 5 ở thư mục cha."))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P1"]["level"], "FAIL")
        self.assertIn("DSG update", items["P1"]["msg"])
        self.assertEqual(rc, 1)

    def test_canonical_folder_named_passes(self):
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Nạp `DSG update` only: KE_HOACH_KAIZEN.md --contains E27"))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P1"]["level"], "PASS")

    def test_old_path_explicit_fails(self):
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Nguồn `../KE_HOACH_KAIZEN.md`; DSG update để tham khảo"))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P1"]["level"], "FAIL")
        self.assertIn("bản cũ", items["P1"]["msg"])


class TestF38Scan(Base):
    def test_f38_quarantine_source_fails(self):
        (self.dsg / "GSD_CORE_DE_XUAT_KAIZEN.md").write_text("Không bật auto-merge.\n", encoding="utf-8")
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Nạp DSG/GSD_CORE_DE_XUAT_KAIZEN.md từ DSG update; --contains GSD"))
        rc, items = self.run_pf(p, "--map", f"DSG/={self.dsg}")
        self.assertEqual(items["P3"]["level"], "FAIL")
        self.assertIn("QUARANTINE", items["P3"]["msg"])

    def test_f48_block_accepted_when_rule_named(self):
        (self.dsg / "GSD_CORE_DE_XUAT_KAIZEN.md").write_text("xem RSK-0004_agent-tag-and-merge-bypass\n", encoding="utf-8")
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Nạp DSG/GSD_CORE_DE_XUAT_KAIZEN.md (DSG update); OWNER chấp nhận zone3_openai_token (F48); --contains RSK"))
        rc, items = self.run_pf(p, "--map", f"DSG/={self.dsg}")
        self.assertEqual(items["P3"]["level"], "WARN")

    def test_clean_source_passes(self):
        (self.dsg / "GSD_CORE_DE_XUAT_KAIZEN.md").write_text("nội dung sạch\n", encoding="utf-8")
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Nạp DSG/GSD_CORE_DE_XUAT_KAIZEN.md (DSG update); --contains sạch"))
        rc, items = self.run_pf(p, "--map", f"DSG/={self.dsg}")
        self.assertEqual(items["P3"]["level"], "PASS")


class TestF40Budget(Base):
    def make_big(self):
        (self.dsg / "GSD_CORE_DE_XUAT_KAIZEN.md").write_text("dòng\n" * 1300, encoding="utf-8")

    def test_f40_copy_exceeds_budget_fails(self):
        self.make_big()
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Chép nguyên văn DSG/GSD_CORE_DE_XUAT_KAIZEN.md (DSG update); --contains dòng"))
        rc, items = self.run_pf(p, "--map", f"DSG/={self.dsg}")
        self.assertEqual(items["P4"]["level"], "FAIL")
        self.assertIn("1300", items["P4"]["msg"])

    def test_budget_note_passes(self):
        self.make_big()
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Chép nguyên văn DSG/GSD_CORE_DE_XUAT_KAIZEN.md (DSG update); line_budget chỉ tính dòng tự viết; --contains dòng"))
        rc, items = self.run_pf(p, "--map", f"DSG/={self.dsg}")
        self.assertEqual(items["P4"]["level"], "PASS")

    def test_copy_without_sources_warns(self):
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Chép nguyên văn từ DSG update; --contains x"))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P4"]["level"], "WARN")


class TestCardChecks(Base):
    def test_scope_over_five_fails(self):
        p = self.phieu(FRAME.format(task="TK-0039", ref="abc1234", can_lam="Ghi RETIRED"))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P5"]["level"], "FAIL")

    def test_f53_regex_dollar_warns(self):
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Ghi file"))
        rc, items = self.run_pf(p)
        self.assertIn(items["P6"]["level"], ("WARN",))

    def test_missing_frame_key_warns(self):
        p = self.phieu("MÃ: TK-0058 REF: origin/main @ abc1234\nlàm việc\n")
        rc, items = self.run_pf(p)
        self.assertEqual(items["P8"]["level"], "WARN")

    def test_machine_path_warns(self):
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Gốc %USERPROFILE%\\orca"))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P9"]["level"], "WARN")

    def test_missing_ref_fails(self):
        p = self.phieu("TỪ: A → ĐẾN: B LOẠI: GIAO\nMÃ: TK-0058\nCẦN LÀM: x\nDỪNG KHI: y TRẢ LỜI: z\n")
        rc, items = self.run_pf(p)
        self.assertEqual(items["P7"]["level"], "FAIL")

    def test_warn_only_exit_zero(self):
        p = self.phieu(FRAME.format(task="TK-0039", ref="abc1234", can_lam="Ghi RETIRED"))
        rc, items = self.run_pf(p, "--warn-only")
        self.assertEqual(rc, 0)


@unittest.skipUnless(subprocess.run(["git", "--version"], capture_output=True).returncode == 0, "cần git")
class TestF47AndRef(Base):
    def setUp(self):
        super().setUp()
        self.repo = self.d / "repo"
        self.repo.mkdir()
        env = dict(os.environ, GIT_AUTHOR_NAME="a", GIT_AUTHOR_EMAIL="a@x.invalid", GIT_COMMITTER_NAME="a", GIT_COMMITTER_EMAIL="a@x.invalid")
        (self.repo / "f.txt").write_text("x\n", encoding="utf-8")
        for cmd in (["init", "-q"], ["add", "."], ["commit", "-qm", "c"]):
            subprocess.run(["git", "-C", str(self.repo), *cmd], check=True, env=env, capture_output=True)
        self.sha = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    def test_f47_verify_tool_missing_fails(self):
        p = self.phieu(FRAME.format(task="TK-0039", ref=self.sha[:7], can_lam="Ghi RETIRED"))
        rc, items = self.run_pf(p, "--repo", str(self.repo), "--origin", "HEAD")
        self.assertEqual(items["P6"]["level"], "FAIL")
        self.assertIn("missing_tool.py", items["P6"]["msg"])

    def test_ref_matches(self):
        p = self.phieu(FRAME.format(task="TK-0058", ref=self.sha[:7], can_lam="x"))
        rc, items = self.run_pf(p, "--repo", str(self.repo), "--origin", "HEAD")
        self.assertEqual(items["P7"]["level"], "PASS")

    def test_stale_ref_fails(self):
        p = self.phieu(FRAME.format(task="TK-0058", ref="deadbee", can_lam="x"))
        rc, items = self.run_pf(p, "--repo", str(self.repo), "--origin", "HEAD")
        self.assertEqual(items["P7"]["level"], "FAIL")


class TestF57OwnerDecision(Base):
    def test_f57_missing_decision_fails(self):
        p = self.phieu(FRAME.format(task="TK-0040", ref="abc1234", can_lam="Làm theo thẻ TK-0040"))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P10"]["level"], "FAIL")
        self.assertIn("O2.1", items["P10"]["msg"])

    def test_decision_present_passes(self):
        p = self.phieu(FRAME.format(task="TK-0040", ref="abc1234", can_lam="O2.1 chốt: E20–E26 giữ nguyên"))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P10"]["level"], "PASS")

    def test_card_without_o_passes(self):
        p = self.phieu(FRAME.format(task="TK-0058", ref="abc1234", can_lam="x"))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P10"]["level"], "PASS")


class TestWindowsConsole(Base):
    def test_cp1252_stdout_does_not_crash(self):
        raw = io.BytesIO()
        fake = io.TextIOWrapper(raw, encoding="cp1252")
        old = sys.stdout
        sys.stdout = fake
        try:
            p = self.phieu(FRAME.format(task="TK-0039", ref="abc1234", can_lam="Ghi RETIRED"))
            rc = pf.main([str(p), "--muc-luc", str(self.d / "MUC_LUC.md"), "--card", str(self.d / "SRC.md")])
            fake.flush()
        finally:
            sys.stdout = old
        self.assertEqual(rc, 1)
        self.assertIn("PREFLIGHT", raw.getvalue().decode("utf-8"))


class TestCrlfPhieu(Base):
    def test_crlf_phieu_parsed(self):
        p = self.d / "crlf.md"
        p.write_bytes(FRAME.format(task="TK-0058", ref="abc1234", can_lam="Nạp `DSG update` only: KE_HOACH_KAIZEN.md --contains E27").replace("\n", "\r\n").encode("utf-8"))
        rc, items = self.run_pf(p)
        self.assertEqual(items["P1"]["level"], "PASS")
        self.assertEqual(items["P8"]["level"], "PASS")


if __name__ == "__main__":
    unittest.main()
