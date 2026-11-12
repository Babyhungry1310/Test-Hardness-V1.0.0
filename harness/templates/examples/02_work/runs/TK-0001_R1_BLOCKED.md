---
schema: 1
task: TK-0001
run: 1
outcome: BLOCKED
model: "model-a"
branch: task/TK-0001-R1
outputs: ["src/dupes.py", "tests/test_dupes.py"]
evidence: ["03_output/CYC-01/checks/TK-0001_R1_verify.txt"]
done_check: []
loops:
  - "L01 | FAIL | passed=1 failed=2"
  - "L02 | FAIL | passed=2 failed=1"
  - "L03 | FAIL | passed=2 failed=1"
deviations:
  assumptions: ["So sánh id phân biệt hoa thường vì task không nói"]
  differences: []
  unverified: ["done_when 1: chỉ tìm được Q-002, thiếu Q-001"]
escalate: yes
escalation:
  spec: "done_when 1 đòi Q-001 và Q-002 nhưng task không nói id có phân biệt hoa thường"
  problem: "Q-001 và q-001 chỉ trùng khi bỏ qua hoa thường"
  proposal: "Chốt so sánh id không phân biệt hoa thường"
touched_protected: no
keywords: [quiz-bank, duplicate-id]
usage: []
---
