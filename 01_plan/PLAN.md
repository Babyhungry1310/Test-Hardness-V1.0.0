---
schema: 1
id: PLAN
date: 2026-11-12
based_on: [DEC-0002, DEC-0006, DEC-0007, DEC-0010, DEC-0013]
---
## Status (newest first)
- 2026-11-13 | ACTIVE | version: 3
- 2026-11-12 | ACTIVE | version: 2
- 2026-11-12 | ACTIVE | version: 1
<!-- ANCHOR: CYC_01 -->
## CYC-01
- TK-0001 | Tìm id câu hỏi bị trùng | depends: none | assignee: W1
- TK-0002 | Tạo data/bank.json 5 câu và hàm đọc ngân hàng câu hỏi | depends: none | assignee: W2
- TK-0004 | Giới hạn pytest về tests/ để lệnh kiểm toàn repo chạy được | depends: TK-0001, TK-0002 | assignee: W1
<!-- END: CYC_01 -->
<!-- ANCHOR: CYC_02 -->
## CYC-02
- TK-0003 | Xuất handout Markdown từ ngân hàng câu hỏi | depends: TK-0001, TK-0002 | assignee: W1
- TK-0005 | Handout kết thúc bằng đúng một LF và ghi file với newline LF | depends: TK-0003 | assignee: W1
<!-- END: CYC_02 -->
<!-- ANCHOR: RISKS -->
## Risks
- RSK-0001
<!-- END: RISKS -->
