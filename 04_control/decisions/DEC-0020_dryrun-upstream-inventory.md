---
schema: 1
id: DEC-0020
date: 2026-11-14
title: "Kiểm kê đầy đủ thay đổi dry run trước khi đề xuất chuyển về repo mẹ"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: "REQ-0007"
supersedes: ""
cancels: []
waives: []
affects: [DEC-0016, "01_plan/PLAN.md", "01_plan/SPEC_DRYRUN.md", "01_plan/SPEC_ORCA_PROMPT.md"]
keywords: [dry-run, upstream, inventory, evidence, owner-approval]
---
## Status (newest first)
- 2026-11-14 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
OWNER yêu cầu mọi thay đổi dry run được kiểm kê để xem xét chuyển về repo mẹ, kèm bằng chứng; việc chạy thử không tự cho phép chuyển.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Chuyển tự động sau kiểm thử; lập danh sách đầy đủ và chờ OWNER quyết từng đề xuất. OWNER chọn phương án thứ hai.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Đối chiếu mọi thay đổi từ mốc dry run với PR, task, run và kiểm định, kể cả thay đổi chưa merge, bị loại, thất bại hoặc thiếu bằng chứng. Mỗi mục ghi nguồn, SHA, phạm vi, trạng thái, bằng chứng, rủi ro và đề xuất; không coi thay đổi dự án riêng là tự động phù hợp khung.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- TK-0028 tạo bản kiểm kê trước hồi quy cuối; LEAD cập nhật bản kiểm kê sau kiểm định CYC-07 và đối chiếu lại phạm vi trước khi trình OWNER.
- OWNER duyệt từng đề xuất và phiên bản đích trước PR riêng sang repo mẹ; không tự chuyển hay merge. Thiếu nguồn hoặc bằng chứng ghi chưa xác minh, không loại khỏi danh sách.
<!-- END: CONSEQUENCES -->
