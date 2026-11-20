---
schema: 1
task: TK-0019
run: 1
outcome: DONE
model: "xai/grok-4.7"
branch: task/TK-0019-R1
outputs:
  - tools/assign_audit.py
  - tools/tests/test_assign_audit.py
evidence:
  - 03_output/CYC-04/checks/TK-0019_R1_L01_verify.txt
  - 03_output/CYC-04/checks/TK-0019_R1_L02_verify.txt
  - 03_output/CYC-04/checks/TK-0019_R1_L02_baseline.txt
  - 03_output/CYC-04/checks/TK-0019_R1_L03_verify.txt
  - 03_output/CYC-04/checks/TK-0019_R1_L03_baseline.txt
  - 03_output/CYC-04/checks/TK-0019_R1_L03_CYC-01.json
  - 03_output/CYC-04/checks/TK-0019_R1_L03_CYC-02.json
  - 03_output/CYC-04/checks/TK-0019_R1_L04_verify.txt
  - 03_output/CYC-04/checks/TK-0019_R1_L04_baseline.txt
  - 03_output/CYC-04/checks/TK-0019_R1_CYC-01.json
  - 03_output/CYC-04/checks/TK-0019_R1_CYC-02.json
done_check:
  - "1 -> tools/tests/test_assign_audit.py"
  - "2 -> tools/tests/test_assign_audit.py::test_same_group_different_code_exits_0"
  - "3 -> tools/tests/test_assign_audit.py::test_hardeness_is_unknown"
  - "3 -> tools/tests/test_assign_audit.py::test_probe_only_is_unknown_and_creates_no_rvw"
  - "3 -> tools/tests/test_assign_audit.py::test_comma_split_reports_overlap_on_one_code"
  - "4 -> 03_output/CYC-04/checks/TK-0019_R1_CYC-01.json"
  - "4 -> 03_output/CYC-04/checks/TK-0019_R1_CYC-02.json"
  - "5 -> tools/tests/test_assign_audit.py::test_script_does_not_write"
  - "6 -> 03_output/CYC-04/checks/TK-0019_R1_L04_verify.txt"
  - "6 -> 03_output/CYC-04/checks/TK-0019_R1_L04_baseline.txt"
loops:
  - "L01 | FAIL | passed=20 failed=1"
  - "L02 | FAIL | passed=21 failed=0 baseline=23 cli=ModuleNotFoundError"
  - "L03 | FAIL | passed=22 failed=0 baseline=23 cli=2 missing front matter"
  - "L04 | PASS | passed=24 failed=0 baseline=23 cyc01=0 cyc02=0"
deviations: {assumptions: [], differences: [], unverified: []}
escalate: no
escalation: {spec: "", problem: "", proposal: ""}
touched_protected: no
keywords: []
usage: []
---
