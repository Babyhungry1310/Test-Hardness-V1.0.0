---
schema: 1
id: REQ-0012
date: 2026-11-19
title: "Tách TK-0033 để giữ ngân sách và thứ tự kiểm detector session"
proposed_by: OWNER
cycle: CYC-03
affects: [TK-0018, TK-0033, TK-0034, TK-0035, "01_plan/PLAN.md", "01_plan/ACCEPTANCE.md", "01_plan/SPEC_TOOLS.md"]
keywords: [hooks, crlf, line-budget, session]
---
## Status (newest first)
- 2026-11-19 | RESOLVED_BY DEC-0029
- 2026-11-19 | PENDING
<!-- ANCHOR: CONTEXT -->
## Context
OWNER chấp thuận hủy TK-0033 trước thi công. Draft detector session khoảng 620 dòng, vượt giới hạn task; chưa có run hoặc PR sản phẩm.
<!-- END: CONTEXT -->
<!-- ANCHOR: IMPACT -->
## Impact
DEC-0029 tạo TK-0034 và TK-0035 tuần tự, mỗi task 300 dòng. Không cấp quyền publication, không đổi harness, config, CI hay quyền GitHub.
<!-- END: IMPACT -->
