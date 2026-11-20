---
schema: 1
task: TK-0017
run: 1
outcome: DONE
model: "ag/gemini-3.8-flash-high"
branch: task/TK-0017-R1
outputs:
  - 03_output/CYC-07/checks/TK-0017_regression_windows.txt
evidence:
  - 03_output/CYC-07/checks/TK-0017_regression_windows.txt
  - 03_output/CYC-07/checks/TK-0017_R1_L01_verify.txt
  - 03_output/CYC-07/checks/TK-0017_R1_L01_baseline.txt
done_check:
  - "1 -> 03_output/CYC-07/checks/TK-0017_regression_windows.txt"
  - "2 -> 03_output/CYC-07/checks/TK-0017_regression_windows.txt"
  - "3 -> 03_output/CYC-07/checks/TK-0017_regression_windows.txt"
  - "4 -> 03_output/CYC-07/checks/TK-0017_regression_windows.txt"
  - "5 -> 03_output/CYC-07/checks/TK-0017_regression_windows.txt"
  - "6 -> 03_output/CYC-07/checks/TK-0017_regression_windows.txt"
  - "7 -> 03_output/CYC-07/checks/TK-0017_regression_windows.txt"
  - "8 -> 03_output/CYC-07/checks/TK-0017_regression_windows.txt"
  - "9 -> 03_output/CYC-07/checks/TK-0017_regression_windows.txt"
loops: ["L01 | PASS | verify=23 baseline=23 tools=338"]
deviations: {assumptions: [], differences: [], unverified: []}
escalate: no
escalation: {spec: "", problem: "", proposal: ""}
touched_protected: no
keywords: [regression, windows, pytest, freeze, batch, catalog, matrix]
usage: []
---
