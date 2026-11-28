---
schema: 1
task: TK-0043
run: 2
outcome: DONE
model: "UNKNOWN"
branch: task/TK-0043-R2
outputs:
  - tools/validate.py
  - tools/tests/test_validate_core.py
  - tools/README.md
  - 02_work/runs/TK-0043_R2_DONE.md
  - 03_output/CYC-08/checks/TK-0043_R2_L03_verify.txt
  - 03_output/CYC-08/checks/TK-0043_R2_L04_verify.txt
  - 03_output/CYC-08/checks/TK-0043_R2_base.txt
evidence:
  - 03_output/CYC-08/checks/TK-0043_R2_L03_verify.txt
  - 03_output/CYC-08/checks/TK-0043_R2_L04_verify.txt
  - 03_output/CYC-08/checks/TK-0043_R2_base.txt
  - tools/README.md
done_check:
  - "1 → 03_output/CYC-08/checks/TK-0043_R2_L04_verify.txt"
  - "2 → 03_output/CYC-08/checks/TK-0043_R2_L04_verify.txt"
  - "3 → 03_output/CYC-08/checks/TK-0043_R2_base.txt"
  - "4 → tools/README.md"
loops:
  - "L03 | PASS | passed=16 failed=0"
  - "L04 | PASS | passed=21 failed=0"
deviations:
  assumptions: []
  differences:
    - "DEC-0041 mở R2 và SPEC_TOOLS VALIDATE_R2 làm rõ cách kiểm."
  unverified: []
escalate: "no"
escalation: {spec: "", problem: "", proposal: ""}
touched_protected: "no"
keywords: [validate, tk-0043]
usage: []
---
