---
schema: 1
id: DEC-0027
date: "2026-11-16"
title: "Kiểm kê và thiết kế quyền WORKER theo task"
proposed_by: LEAD
decided_by: OWNER
cycle: NONE
origin: REQ-0010
supersedes: ""
cancels: []
waives: []
affects: ["01_plan/PLAN.md", "01_plan/ACCEPTANCE.md", "01_plan/SPEC_TOOLS.md"]
keywords: [worker, permissions, readiness, supervised, sandbox]
---
## Status (newest first)
- 2026-11-16 | ACTIVE
<!-- ANCHOR: CONTEXT -->
## Context
REQ-0010: OWNER yêu cầu chuẩn bị thông tin và quyền hẹp khi Planning để WORKER xử lý việc thường trong scope. OWNER chọn làm có giám sát trước, thử tự động trong sandbox sau; giữ rule loop hiện hành trong lúc kiểm kê và trình quy tắc mới sau.
<!-- END: CONTEXT -->
<!-- ANCHOR: OPTIONS -->
## Options considered
- Cấp quyền rộng để bỏ prompt: không chọn vì không kiểm soát phạm vi.
- Kiểm kê, chuẩn bị quyền hẹp và thử có giám sát trước: chọn; tự động là bước thử sau khi có thiết kế và quyền phù hợp.
<!-- END: OPTIONS -->
<!-- ANCHOR: RATIONALE -->
## Decision and rationale
Sau CYC-07, thực hiện CYC-08 kiểm kê bằng chứng và công cụ để thiết kế đề xuất quyền theo task. Quyền phải đủ cho việc đã cấp và có giới hạn; WORKER dừng khi thiếu quyền, có nguy cơ, vượt scope hoặc cần quyết định thuộc OWNER. Không tự trả lời prompt bắt buộc. Giữ rule loop và lịch sử hiện hành; quy tắc khác cần trình OWNER theo quy trình.
<!-- END: RATIONALE -->
<!-- ANCHOR: CONSEQUENCES -->
## Consequences
- CYC-08 chỉ kiểm kê; chưa cấp quyền runtime mới, chưa thay rule, schema, Git, mạng hoặc cấu hình. Chưa coi broker hay sandbox đã tồn tại.
- Bước có giám sát và thử sandbox sẽ thiết kế thành task sau kiểm kê, phụ thuộc quyết định quyền, rủi ro, môi trường và phạm vi được OWNER duyệt.
- Không gỡ HOLD CYC-03, không sửa ngân sách loop lịch sử. OWNER duyệt plan và merge; không đẩy main, merge hoặc bật auto-merge.
<!-- END: CONSEQUENCES -->
