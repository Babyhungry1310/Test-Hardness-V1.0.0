---
schema: 1
id: DEC-0004
date: 2026-11-12
title: "So khớp id câu hỏi không phân biệt hoa thường"
proposed_by: W1
decided_by: OWNER
cycle: CYC-01
origin: "TK-0001"
supersedes: ""
cancels: []
waives: []
affects: [TK-0001]
keywords: [quiz-bank, duplicate-id]
---
## Status (newest first)
- 2026-11-12 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
Run R1 của TK-0001 nộp `BLOCKED`, `escalate: yes`: ràng buộc "so khớp id nguyên văn, phân biệt hoa thường" trái với điều kiện "q-001 và Q-001 được báo là trùng". Chưa có `DEC` nào quy định cách so khớp id.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Giữ phân biệt hoa thường, sửa `done_when` để `q-001` và `Q-001` không bị coi là trùng
- Không phân biệt hoa thường, id trả về giữ dạng gốc ở lần xuất hiện đầu tiên
- Không phân biệt hoa thường, id trả về ở dạng chuẩn hóa
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
So khớp id không phân biệt hoa thường: `q-001` và `Q-001` là trùng nhau. Danh sách id trùng giữ dạng gốc của id ở lần xuất hiện đầu tiên, theo thứ tự xuất hiện. Ngân hàng gộp từ nhiều người soạn nên cùng một id có thể được gõ khác kiểu chữ; giữ dạng gốc để người dùng tìm lại đúng câu trong file.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
`constraints` của TK-0001 đổi theo quyết định này; `done_when` giữ nguyên. TK-0001 được mở lại bằng run R2, thêm tối đa `max_loops` loop. RSK-0002 đóng.
<!-- END: CONSEQUENCES -->
