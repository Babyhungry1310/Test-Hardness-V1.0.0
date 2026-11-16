---
schema: 1
id: REQ-0010
date: "2026-11-16"
title: "Lập plan cấp quyền theo task để WORKER giảm hỏi quyền thường lệ"
proposed_by: OWNER
cycle: NONE
affects: ["01_plan/PLAN.md", "01_plan/SPEC_TOOLS.md", "harness/rules/LEAD.md", "harness/rules/WORKER.md"]
keywords: [worker, permissions, readiness, loop, isolation]
---
## Status (newest first)
- 2026-11-16 | RESOLVED_BY DEC-0027
- 2026-11-16 | PENDING
<!-- ANCHOR: CONTEXT -->
## Context
OWNER yêu cầu LEAD lập plan và task cụ thể để chuẩn bị thông tin, môi trường và quyền hẹp trong Planning, giúp WORKER tự xử lý loop thường lệ mà không hỏi lại OWNER về quyền đã cấp. OWNER đã cho phép bắt đầu phiên CHANGE; việc đó chưa tự quyết profile runtime, cách tính loop hay thay đổi phạm vi hiện hành.
<!-- END: CONTEXT -->
<!-- ANCHOR: IMPACT -->
## Impact
Cần đối chiếu plan dry run, SPEC_TOOLS, quyền runtime và bằng chứng; trình OWNER chốt các lựa chọn có ảnh hưởng trước khi ghi DEC và plan có hiệu lực. Không gỡ HOLD CYC-03, không tự cấp quyền hay sửa lịch sử loop. Gói task dự thảo ở 03_output/upstream/DRAFT_WORKER_PERMISSIONS.md chưa cấp mã task.
<!-- END: IMPACT -->
