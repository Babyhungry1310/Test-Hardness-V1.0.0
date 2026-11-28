---
schema: 1
task: TK-0055
run: 1
outcome: DONE
model: "UNKNOWN"
branch: task/TK-0055-R1
outputs:
  - harness/schemas/task.schema.json
  - harness/exit_codes.json
  - tools/tests/test_task_schema_path.py
  - harness/VERSION
  - harness/HARNESS.md
  - 02_work/runs/TK-0055_R1_DONE.md
  - 03_output/CYC-08/checks/TK-0055_R1_L02_verify.txt
evidence:
  - 03_output/CYC-08/checks/TK-0055_R1_L02_verify.txt
done_check:
  - "1 → 5 test PASS trên Windows"
  - "2 → exit_codes.json đúng tập mã, verify exit 0"
  - "3 → 25 thẻ SRC-0003 PASS"
  - "4 → VERSION và HARNESS 1.0.4 khớp"
loops:
  - "L01 | FAIL | cause=cmd_quoting"
  - "L02 | PASS | passed=5 failed=0 verify=exit_0"
deviations:
  assumptions: []
  differences:
    - "L-T55: OWNER cho phép năm file; HARNESS chỉ đổi phiên bản."
    - "D-T55: Terra thực hiện, Luna review; model chưa xác minh."
    - "D-T55a: chọn A; năm hash nguồn Claude 2 ghi dưới đây."
    - "task.schema.json SHA256 1974c45762ebda3565a60288a013d9495a8b7e1418874b54af1287ab19f83886"
    - "exit_codes.json SHA256 e2fee5b390b496f439a844b6651c70835206fa0a84a842f0d602466f4659f84a"
    - "test_task_schema_path.py SHA256 6275228970b08b4ee06279a8fecfc3ecdcd2875906a18bf32cedde2cd508398f"
    - "VERSION SHA256 d1b77b88f4b9f675a900e4143ac768a21218623cfe1703ca43162388c3271bd6"
    - "HARNESS.md SHA256 78d489ca5f8639e805fd5041101c83f66fda86929359e69a04e745802b92f8aa"
    - "D-T55b: nhánh task/TK-0055-R1 thay upgrade/."
    - "D-T55c: giữ pattern; ghi nhận lỗ hổng .. giữa path cho task sau."
    - "L01 lỗi trích dẫn cmd; L02 sửa cách gọi, không đổi năm file."
  unverified: []
escalate: "no"
escalation: {spec: "", problem: "", proposal: ""}
touched_protected: "yes"
keywords: [task-schema, exit-codes, tk-0055]
usage: []
---
