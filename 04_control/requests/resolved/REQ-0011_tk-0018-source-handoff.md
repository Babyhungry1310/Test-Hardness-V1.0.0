---
schema: 1
id: REQ-0011
date: 2026-11-19
title: "Hoàn tất nguồn sửa và bàn giao TK-0018 sau draft PASS"
proposed_by: OWNER
cycle: CYC-03
affects: [TK-0018, TK-0032, TK-0033, "01_plan/PLAN.md", "01_plan/ACCEPTANCE.md", "01_plan/SPEC_TOOLS.md"]
keywords: [handoff, hooks, crlf, evidence, shared-account]
---
## Status (newest first)
- 2026-11-19 | RESOLVED_BY DEC-0028
- 2026-11-19 | PENDING
<!-- ANCHOR: CONTEXT -->
## Context
OWNER đã duyệt sửa nguồn hook và detector CRLF, giao Grok, reviewer độc lập Gemini qua 9Router. Sau draft PASS, OWNER yêu cầu LEAD ghi DEC và plan; nhận các chỉnh sửa về quyền publication riêng, bundle bất biến, Git blob, fixture runtime, cập nhật base và rủi ro tài khoản chung. Đây là ghi lại quyết định đã có, không yêu cầu duyệt lại cùng phạm vi.
<!-- END: CONTEXT -->
<!-- ANCHOR: IMPACT -->
## Impact
DEC-0028 chia hai task nguồn độc lập rồi mới tiếp tục TK-0018. L01 giữ 44 passed/3 failed; còn hai loop R1. Governance phải được OWNER merge trước khi chạy nguồn. Không cấp quyền commit, push, mở PR hoặc merge; không sửa rule, attributes, cấu hình hay quyền GitHub.
<!-- END: IMPACT -->
