---
schema: 1
id: PLAN
date: 2026-11-04
based_on: [DEC-0002, DEC-0003]
---
## Status (newest first)
- 2026-11-04 | ACTIVE | version: 1
<!-- ANCHOR: CYC_01 -->
## CYC-01
- TK-0001 | Tìm id câu hỏi bị trùng | depends: none | assignee: W1
- TK-0002 | Đọc ngân hàng câu hỏi JSON và báo câu thiếu trường | depends: none | assignee: W2
<!-- END: CYC_01 -->
<!-- ANCHOR: CYC_02 -->
## CYC-02
- TK-0003 | Xuất handout Markdown từ ngân hàng câu hỏi | depends: TK-0001, TK-0002 | assignee: W1
<!-- END: CYC_02 -->
<!-- ANCHOR: RISKS -->
## Risks
- RSK-0002
<!-- END: RISKS -->
