---
schema: 1
id: DEC-0007
date: 2026-11-12
title: "Phân công model CYC-01: WORKER dùng Codex, REVIEWER dùng Claude"
proposed_by: LEAD
decided_by: OWNER
cycle: CYC-01
origin: "RVW-CYC-01"
supersedes: "DEC-0003"
cancels: []
waives: []
affects: [DEC-0003, DEC-0005, RSK-0003, "01_plan/PLAN.md#CYC_01"]
keywords: [model-assignment, worker, reviewer]
---
## Status (newest first)
- 2026-11-12 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
DEC-0003 giao REVIEWER của CYC-01 cho nhóm Gemini; DEC-0005 giữ phân công đó dù run R1 của TK-0001 chạy `gemini-3.8-flash-k`. Khi kiểm định, các tuyến Gemini văn bản và code trên 9Router không hoạt động, tuyến còn lại là model ảnh. OWNER cho phép dùng REVIEWER khác cả `gemini-3.8-flash-k` và `gpt-6.1-sol`; RVW-CYC-01 vòng 2 chạy `claude-sonnet-4-6`.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Giữ Gemini làm REVIEWER, chờ tuyến Gemini hoạt động lại
- Đổi REVIEWER của CYC-01 sang nhóm Claude
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
| Vai | Nhóm model trên 9Router |
|---|---|
| W1 | Codex |
| W2 | Codex |
| REVIEWER của CYC-01 | Claude |

Nhóm Claude khác hãng với mọi model đã ghi trong run của CYC-01, kể cả run R1 `BLOCKED` của TK-0001, nên kiểm định độc lập mà không cần ngoại lệ. Nhóm REVIEWER không được có model dự phòng thuộc nhóm Codex hay Gemini.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
DEC-0003 bị thay; DEC-0005 hết căn cứ nên `RETIRED`; RSK-0003 đóng vì REVIEWER không còn cùng nhóm với run nào. Kiểm định vòng 3 của CYC-01 chạy nhóm Claude. Câu 2 của cổng `CYC-01_PASS` không còn phải trả `CONDITIONAL` theo RSK-0003.
<!-- END: CONSEQUENCES -->
