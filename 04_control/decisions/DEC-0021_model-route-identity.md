---
schema: 1
id: DEC-0021
date: 2026-11-14
title: "Phân biệt tuyến 9Router và model thực tế khi so sánh định danh"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "REQ-0008"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0018, TK-0010, TK-0019, "harness/MODEL_POLICY.md", "01_plan/SPEC_ORCA_PROMPT.md"]
keywords: [model, route, aliases, actual, reviewer-independence]
---
## Status (newest first)
- 2026-11-14 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
Catalog có tên tuyến trong aliases; luật so sánh cũ coi mọi alias là định danh model, trong khi một tuyến có thể trả model khác theo thời điểm.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Giữ cách so mọi alias; phân biệt tuyến gọi với chuỗi model thực tế và yêu cầu bằng chứng định danh. OWNER yêu cầu rà và sửa điểm mơ hồ.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Giữ nguyên schema và dữ liệu catalog; route dùng để gọi, actual chép từ hệ thống, code là mã model. Không suy định danh từ tuyến hoặc combo; thiếu bằng chứng thì không kết luận model khác và hỏi OWNER.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- Điều chỉnh phần diễn giải aliases của DEC-0018; phần còn lại giữ nguyên. Run và RVW lịch sử không bị sửa hay xét lại.
- TK-0029 kiểm thử hồi quy các trường hợp tuyến đổi model và định danh chưa xác minh. Kiểm kê do OWNER nêu chưa có trong worktree; không coi danh sách tuyến là bằng chứng agent dùng được công cụ.
<!-- END: CONSEQUENCES -->
