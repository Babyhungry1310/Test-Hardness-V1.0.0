---
schema: 1
id: DEC-0001
date: 2026-11-12
title: "Lưu ngân hàng câu hỏi dạng CSV và xuất handout Markdown"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "DSC-20261112-012x#E1"
supersedes: ""
cancels: []
waives: []
affects: ["data/bank.csv"]
keywords: [quiz-bank, storage, handout]
---
## Status (newest first)
- 2026-11-12 | SUPERSEDED_BY DEC-0002
- 2026-11-12 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
Cần một công cụ dòng lệnh đọc ngân hàng câu hỏi, báo câu trùng id và xuất handout cho lớp học.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- CSV vào, handout Markdown ra
- Xuất thẳng ra PDF
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Chọn CSV vì sửa được bằng bảng tính. Đầu ra là handout Markdown để in và sửa tay được. Không xuất PDF; người dùng tự chuyển từ Markdown khi cần.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
Ngân hàng câu hỏi nằm ở `data/bank.csv`. Công cụ chỉ sinh file Markdown.
<!-- END: CONSEQUENCES -->
