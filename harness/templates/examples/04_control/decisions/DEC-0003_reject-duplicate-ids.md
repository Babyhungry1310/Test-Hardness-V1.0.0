---
schema: 1
id: DEC-0003
date: 2026-11-03
title: "Báo mọi id câu hỏi trùng trước khi xuất"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "REQ-0001"
supersedes: ""
cancels: []
waives: []
affects: ["data/bank.json"]
keywords: [quiz-bank, duplicate-id]
---
## Status (newest first)
- 2026-11-03 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
REQ-0001: ngân hàng gộp có câu trùng id.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Tự xóa câu trùng
- Báo danh sách id trùng, để giáo viên sửa
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Báo danh sách id trùng, không tự xóa, vì hai câu trùng id có thể có nội dung khác nhau.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
Cần một hàm trả về danh sách id trùng theo thứ tự xuất hiện.
<!-- END: CONSEQUENCES -->
